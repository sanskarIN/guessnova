"""Local leaderboard logic."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime

from .domain import GameSummary


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
        player=player,
        difficulty=summary.difficulty,
        mode=summary.mode.value,
        attempts=summary.attempts,
        elapsed_seconds=round(summary.elapsed_seconds, 3),
        created_at=datetime.now(UTC).isoformat(),
    )


def add_entry(entries: list[LeaderboardEntry], entry: LeaderboardEntry, limit: int = 100) -> list[LeaderboardEntry]:
    return sorted([*entries, entry], key=lambda item: item.score_key)[:limit]


def serialize(entries: list[LeaderboardEntry]) -> list[dict[str, object]]:
    return [asdict(entry) for entry in entries]


def deserialize(items: object) -> list[LeaderboardEntry]:
    if not isinstance(items, list):
        return []
    result: list[LeaderboardEntry] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            result.append(
                LeaderboardEntry(
                    player=str(item["player"]),
                    difficulty=str(item["difficulty"]),
                    mode=str(item["mode"]),
                    attempts=int(item["attempts"]),
                    elapsed_seconds=float(item["elapsed_seconds"]),
                    created_at=str(item["created_at"]),
                )
            )
        except (KeyError, TypeError, ValueError):
            continue
    return result
