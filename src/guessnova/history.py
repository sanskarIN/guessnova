"""Bounded local session-history records."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime

from .domain import GameSummary

MAX_HISTORY_ENTRIES = 200


@dataclass(frozen=True, slots=True)
class HistoryEntry:
    mode: str
    difficulty: str
    won: bool
    attempts: int
    elapsed_seconds: float
    seed: int | None
    played_at: str


def entry_from_summary(summary: GameSummary, *, played_at: str | None = None) -> HistoryEntry:
    return HistoryEntry(
        mode=summary.mode.value,
        difficulty=summary.difficulty,
        won=summary.won,
        attempts=summary.attempts,
        elapsed_seconds=round(summary.elapsed_seconds, 3),
        seed=summary.seed,
        played_at=played_at or datetime.now(UTC).isoformat(),
    )


def append_history(
    entries: list[HistoryEntry], entry: HistoryEntry, *, limit: int = MAX_HISTORY_ENTRIES
) -> list[HistoryEntry]:
    if limit < 1:
        raise ValueError("history limit must be positive")
    return [*entries, entry][-limit:]


def serialize(entries: list[HistoryEntry]) -> list[dict[str, object]]:
    return [asdict(entry) for entry in entries]


def deserialize(items: object) -> list[HistoryEntry]:
    if not isinstance(items, list):
        return []
    result: list[HistoryEntry] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            seed = item.get("seed")
            result.append(
                HistoryEntry(
                    mode=str(item["mode"]),
                    difficulty=str(item["difficulty"]),
                    won=bool(item["won"]),
                    attempts=int(item["attempts"]),
                    elapsed_seconds=float(item["elapsed_seconds"]),
                    seed=int(seed) if seed is not None else None,
                    played_at=str(item["played_at"]),
                )
            )
        except (KeyError, TypeError, ValueError):
            continue
    return result[-MAX_HISTORY_ENTRIES:]
