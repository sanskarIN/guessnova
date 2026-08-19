"""Atomic, local-only persistence with validation and schema migration."""

from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from .constants import APP_NAME, DEFAULT_PROFILE, SCHEMA_VERSION
from .leaderboard import LeaderboardEntry, deserialize, serialize
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
    if version == 0:
        payload.setdefault("profiles", {})
        payload.setdefault("active_profile", DEFAULT_PROFILE)
        payload["schema_version"] = 1
        version = 1
    if version > SCHEMA_VERSION:
        raise ValueError("save data was created by a newer GuessNova version")
    return payload


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
    leaderboard = serialize(deserialize(migrated.get("leaderboard", [])))
    return {
        "schema_version": SCHEMA_VERSION,
        "active_profile": active,
        "profiles": profiles,
        "leaderboard": leaderboard,
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
