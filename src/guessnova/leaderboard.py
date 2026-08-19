"""Local leaderboard logic."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from datetime import UTC, datetime

from .domain import DIFFICULTIES, GameMode, GameSummary
from .security import sanitize_profile_name


@dataclass(frozen=True, slots=True)
class LeaderboardEntry:
    player: str
    difficulty: str
    mode: str
    attempts: int
    elapsed_seconds: float
    created_at: str

    @property
    def score_key(self) -> tuple[int, float, str]:
        return (self.attempts, self.elapsed_seconds, self.created_at)


def entry_from_summary(player: str, summary: GameSummary) -> LeaderboardEntry | None:
    if not summary.won:
        return None
    return LeaderboardEntry(
        player=sanitize_profile_name(player),
        difficulty=summary.difficulty,
        mode=summary.mode.value,
        attempts=summary.attempts,
        elapsed_seconds=round(summary.elapsed_seconds, 3),
        created_at=datetime.now(UTC).isoformat(),
    )


def add_entry(
    entries: list[LeaderboardEntry], entry: LeaderboardEntry, limit: int = 100
) -> list[LeaderboardEntry]:
    if limit < 1:
        raise ValueError("leaderboard limit must be positive")
    return sorted([*entries, entry], key=lambda item: item.score_key)[:limit]


def serialize(entries: list[LeaderboardEntry]) -> list[dict[str, object]]:
    return [asdict(entry) for entry in entries]


def deserialize(items: object) -> list[LeaderboardEntry]:
    if not isinstance(items, list):
        return []
    valid_modes = {mode.value for mode in GameMode if mode != GameMode.REVERSE}
    result: list[LeaderboardEntry] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        player = item.get("player")
        difficulty = item.get("difficulty")
        mode = item.get("mode")
        attempts = item.get("attempts")
        elapsed = item.get("elapsed_seconds")
        created_at = item.get("created_at")
        if not isinstance(player, str):
            continue
        if not isinstance(difficulty, str) or difficulty not in DIFFICULTIES:
            continue
        if not isinstance(mode, str) or mode not in valid_modes:
            continue
        if isinstance(attempts, bool) or not isinstance(attempts, int):
            continue
        rules = DIFFICULTIES[difficulty]
        if attempts < 1 or attempts > rules.max_attempts:
            continue
        if isinstance(elapsed, bool) or not isinstance(elapsed, (int, float)):
            continue
        elapsed_seconds = float(elapsed)
        if elapsed_seconds < 0 or not math.isfinite(elapsed_seconds):
            continue
        if not isinstance(created_at, str) or not created_at or len(created_at) > 80:
            continue
        try:
            safe_player = sanitize_profile_name(player)
        except ValueError:
            continue
        result.append(
            LeaderboardEntry(
                player=safe_player,
                difficulty=difficulty,
                mode=mode,
                attempts=attempts,
                elapsed_seconds=elapsed_seconds,
                created_at=created_at,
            )
        )
    return result
