"""Atomic, local-only persistence with a small schema migration layer."""

from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from .constants import APP_NAME, SCHEMA_VERSION
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
    return Path(xdg).expanduser() / "guessnova" if xdg else Path.home() / ".local" / "share" / "guessnova"


def _migrate(payload: dict[str, object]) -> dict[str, object]:
    version = int(payload.get("schema_version", 0))
    if version == 0:
        payload.setdefault("profiles", {})
        payload.setdefault("active_profile", "Player")
        payload["schema_version"] = 1
        version = 1
    if version > SCHEMA_VERSION:
        raise ValueError("save data was created by a newer GuessNova version")
    return payload


class Storage:
    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = (data_dir or default_data_dir()).expanduser()
        self.path = self.data_dir / "state.json"

    def load_raw(self) -> dict[str, object]:
        if not self.path.exists():
            return {"schema_version": SCHEMA_VERSION, "active_profile": "Player", "profiles": {}}
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("state file root must be an object")
        return _migrate(payload)

    def save_raw(self, payload: dict[str, object]) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        payload = dict(payload)
        payload["schema_version"] = SCHEMA_VERSION
        with NamedTemporaryFile("w", encoding="utf-8", dir=self.data_dir, delete=False) as temp:
            json.dump(payload, temp, indent=2, sort_keys=True)
            temp.write("\n")
            temp.flush()
            os.fsync(temp.fileno())
            temp_path = Path(temp.name)
        temp_path.replace(self.path)

    def load_profile(self, name: str | None = None) -> Profile:
        payload = self.load_raw()
        profile_name = name or str(payload.get("active_profile", "Player"))
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
