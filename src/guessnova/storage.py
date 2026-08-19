"""Atomic, local-only persistence with validation and schema migration."""

from __future__ import annotations

import json
import os
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

from .constants import APP_NAME, DEFAULT_PROFILE, MAX_DELETED_PROFILES, SCHEMA_VERSION
from .leaderboard import LeaderboardEntry, add_entry, deserialize, serialize
from .profile import Profile


def default_data_dir() -> Path:
    override = os.getenv("GUESSNOVA_HOME")
    if override:
        return Path(override).expanduser()
    if os.name == "nt":
        root = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return root / APP_NAME
    xdg = os.getenv("XDG_DATA_HOME")
    return (
        Path(xdg).expanduser() / "guessnova"
        if xdg
        else Path.home() / ".local" / "share" / "guessnova"
    )


def _migrate(payload: dict[str, object]) -> dict[str, object]:
    raw_version = payload.get("schema_version", 0)
    if isinstance(raw_version, bool) or not isinstance(raw_version, int):
        raise ValueError("state schema_version must be an integer")
    version = raw_version
    if version < 0:
        raise ValueError("state schema_version cannot be negative")
    if version > SCHEMA_VERSION:
        raise ValueError("save data was created by a newer GuessNova version")

    if version == 0:
        payload.setdefault("profiles", {})
        payload.setdefault("active_profile", DEFAULT_PROFILE)
        payload["schema_version"] = 1
        version = 1

    if version == 1:
        # Schema 2 formalizes recoverable profile trash as a canonical top-level
        # container. GuessNova 1.1 wrote the field additively, so migration is
        # intentionally idempotent for schema-1 saves that already contain it.
        payload.setdefault("deleted_profiles", {})
        payload["schema_version"] = 2
        version = 2

    if version != SCHEMA_VERSION:
        raise ValueError("state schema migration did not reach the current version")
    return payload


def _normalize_deleted_profiles(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        return {}
    normalized: list[tuple[str, dict[str, object]]] = []
    for key, raw_record in value.items():
        if not isinstance(key, str) or not isinstance(raw_record, dict):
            continue
        raw_profile = raw_record.get("profile")
        deleted_at = raw_record.get("deleted_at")
        if not isinstance(raw_profile, dict) or not isinstance(deleted_at, str):
            continue
        profile_data = dict(raw_profile)
        profile_data.setdefault("name", key)
        profile = Profile.from_dict(profile_data)
        deleted_leaderboard = serialize(deserialize(raw_record.get("leaderboard", [])))
        normalized.append(
            (
                profile.name,
                {
                    "deleted_at": deleted_at[:80],
                    "profile": profile.to_dict(),
                    "leaderboard": deleted_leaderboard,
                },
            )
        )
    normalized.sort(key=lambda item: str(item[1]["deleted_at"]))
    return dict(normalized[-MAX_DELETED_PROFILES:])


def normalize_state(payload: dict[str, object]) -> dict[str, object]:
    """Validate and normalize untrusted/local state into the supported schema."""
    migrated = _migrate(dict(payload))
    raw_profiles = migrated.get("profiles", {})
    if not isinstance(raw_profiles, dict):
        raise ValueError("state profiles must be an object")

    profiles: dict[str, object] = {}
    for key, raw_profile in raw_profiles.items():
        if not isinstance(key, str) or not isinstance(raw_profile, dict):
            continue
        profile_data = dict(raw_profile)
        profile_data.setdefault("name", key)
        profile = Profile.from_dict(profile_data)
        profiles[profile.name] = profile.to_dict()

    raw_active = migrated.get("active_profile", DEFAULT_PROFILE)
    active = Profile(raw_active if isinstance(raw_active, str) else DEFAULT_PROFILE).name
    if profiles and active not in profiles:
        active = sorted(profiles)[0]
    leaderboard = serialize(deserialize(migrated.get("leaderboard", [])))
    deleted_profiles = _normalize_deleted_profiles(migrated.get("deleted_profiles", {}))
    return {
        "schema_version": SCHEMA_VERSION,
        "active_profile": active,
        "profiles": profiles,
        "leaderboard": leaderboard,
        "deleted_profiles": deleted_profiles,
    }


class Storage:
    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = (data_dir or default_data_dir()).expanduser()
        self.path = self.data_dir / "state.json"

    def load_raw(self) -> dict[str, object]:
        if not self.path.exists():
            return normalize_state(
                {
                    "schema_version": SCHEMA_VERSION,
                    "active_profile": DEFAULT_PROFILE,
                    "profiles": {},
                }
            )
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise ValueError("state file contains invalid JSON") from exc
        if not isinstance(payload, dict):
            raise ValueError("state file root must be an object")
        return normalize_state(payload)

    def save_raw(self, payload: dict[str, object]) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        normalized = normalize_state(payload)
        temp_path: Path | None = None
        try:
            with NamedTemporaryFile(
                "w", encoding="utf-8", dir=self.data_dir, delete=False
            ) as temp:
                json.dump(normalized, temp, indent=2, sort_keys=True)
                temp.write("\n")
                temp.flush()
                os.fsync(temp.fileno())
                temp_path = Path(temp.name)
            temp_path.replace(self.path)
        finally:
            if temp_path is not None and temp_path.exists():
                temp_path.unlink(missing_ok=True)

    def load_profile(self, name: str | None = None) -> Profile:
        payload = self.load_raw()
        profile_name = name or str(payload.get("active_profile", DEFAULT_PROFILE))
        profiles = payload.get("profiles", {})
        if not isinstance(profiles, dict):
            profiles = {}
        raw = profiles.get(profile_name)
        return Profile.from_dict(raw) if isinstance(raw, dict) else Profile(profile_name)

    def list_profile_names(self) -> list[str]:
        payload = self.load_raw()
        profiles = payload.get("profiles", {})
        if not isinstance(profiles, dict):
            return []
        return sorted(key for key in profiles if isinstance(key, str))

    def active_profile_name(self) -> str:
        payload = self.load_raw()
        return str(payload.get("active_profile", DEFAULT_PROFILE))

    def create_profile(self, name: str, *, make_active: bool = True) -> Profile:
        profile = Profile(name)
        payload = self.load_raw()
        profiles = payload.get("profiles", {})
        if not isinstance(profiles, dict):
            raise ValueError("state profiles must be an object")
        if profile.name in profiles:
            raise ValueError(f"profile already exists: {profile.name}")
        profiles[profile.name] = profile.to_dict()
        if make_active:
            payload["active_profile"] = profile.name
        self.save_raw(payload)
        return profile

    def set_active_profile(self, name: str) -> Profile:
        normalized_name = Profile(name).name
        payload = self.load_raw()
        profiles = payload.get("profiles", {})
        if not isinstance(profiles, dict) or normalized_name not in profiles:
            raise ValueError(f"profile does not exist: {normalized_name}")
        payload["active_profile"] = normalized_name
        self.save_raw(payload)
        raw = profiles[normalized_name]
        if not isinstance(raw, dict):
            raise ValueError("stored profile is invalid")
        return Profile.from_dict(raw)

    def rename_profile(self, current_name: str, new_name: str) -> Profile:
        current = Profile(current_name).name
        replacement = Profile(new_name).name
        payload = self.load_raw()
        profiles = payload.get("profiles", {})
        if not isinstance(profiles, dict) or current not in profiles:
            raise ValueError(f"profile does not exist: {current}")
        if replacement != current and replacement in profiles:
            raise ValueError(f"profile already exists: {replacement}")
        raw = profiles.pop(current)
        if not isinstance(raw, dict):
            raise ValueError("stored profile is invalid")
        existing = Profile.from_dict(raw)
        renamed = Profile(replacement, existing.stats, existing.settings, existing.history)
        profiles[replacement] = renamed.to_dict()
        if payload.get("active_profile") == current:
            payload["active_profile"] = replacement
        leaderboard = [
            replace(entry, player=replacement) if entry.player == current else entry
            for entry in deserialize(payload.get("leaderboard", []))
        ]
        payload["leaderboard"] = serialize(leaderboard)
        self.save_raw(payload)
        return renamed

    def delete_profile(self, name: str) -> None:
        normalized_name = Profile(name).name
        payload = self.load_raw()
        profiles = payload.get("profiles", {})
        if not isinstance(profiles, dict) or normalized_name not in profiles:
            raise ValueError(f"profile does not exist: {normalized_name}")
        raw_profile = profiles.pop(normalized_name)
        if not isinstance(raw_profile, dict):
            raise ValueError("stored profile is invalid")

        leaderboard = deserialize(payload.get("leaderboard", []))
        owned = [entry for entry in leaderboard if entry.player == normalized_name]
        payload["leaderboard"] = serialize(
            [entry for entry in leaderboard if entry.player != normalized_name]
        )
        deleted = _normalize_deleted_profiles(payload.get("deleted_profiles", {}))
        deleted[normalized_name] = {
            "deleted_at": datetime.now(UTC).isoformat(),
            "profile": Profile.from_dict(raw_profile).to_dict(),
            "leaderboard": serialize(owned),
        }
        payload["deleted_profiles"] = _normalize_deleted_profiles(deleted)
        if payload.get("active_profile") == normalized_name:
            remaining = sorted(key for key in profiles if isinstance(key, str))
            payload["active_profile"] = remaining[0] if remaining else DEFAULT_PROFILE
        self.save_raw(payload)

    def list_deleted_profile_names(self) -> list[str]:
        payload = self.load_raw()
        deleted = payload.get("deleted_profiles", {})
        if not isinstance(deleted, dict):
            return []
        return sorted(key for key in deleted if isinstance(key, str))

    def restore_profile(self, name: str, *, make_active: bool = True) -> Profile:
        normalized_name = Profile(name).name
        payload = self.load_raw()
        profiles = payload.get("profiles", {})
        deleted = payload.get("deleted_profiles", {})
        if not isinstance(profiles, dict) or not isinstance(deleted, dict):
            raise ValueError("profile state is invalid")
        if normalized_name in profiles:
            raise ValueError(f"profile already exists: {normalized_name}")
        raw_record = deleted.pop(normalized_name, None)
        if not isinstance(raw_record, dict):
            raise ValueError(f"deleted profile does not exist: {normalized_name}")
        raw_profile = raw_record.get("profile")
        if not isinstance(raw_profile, dict):
            raise ValueError("deleted profile record is invalid")
        profile = Profile.from_dict(raw_profile)
        profiles[profile.name] = profile.to_dict()
        leaderboard = deserialize(payload.get("leaderboard", []))
        for entry in deserialize(raw_record.get("leaderboard", [])):
            leaderboard = add_entry(leaderboard, entry)
        payload["leaderboard"] = serialize(leaderboard)
        if make_active:
            payload["active_profile"] = profile.name
        self.save_raw(payload)
        return profile

    def load_leaderboard(self) -> list[LeaderboardEntry]:
        payload = self.load_raw()
        return deserialize(payload.get("leaderboard", []))

    def save_leaderboard(self, entries: list[LeaderboardEntry]) -> None:
        payload = self.load_raw()
        payload["leaderboard"] = serialize(entries)
        self.save_raw(payload)

    def save_profile(self, profile: Profile, make_active: bool = True) -> None:
        payload = self.load_raw()
        profiles = payload.setdefault("profiles", {})
        if not isinstance(profiles, dict):
            profiles = {}
            payload["profiles"] = profiles
        profiles[profile.name] = profile.to_dict()
        if make_active:
            payload["active_profile"] = profile.name
        self.save_raw(payload)
