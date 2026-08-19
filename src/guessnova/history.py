"""Bounded local session-history records."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime

from .domain import DIFFICULTIES, GameMode, GameSummary

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
    valid_modes = {mode.value for mode in GameMode if mode != GameMode.REVERSE}
    result: list[HistoryEntry] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            mode = item["mode"]
            difficulty = item["difficulty"]
            won = item["won"]
            attempts_raw = item["attempts"]
            elapsed_raw = item["elapsed_seconds"]
            played_at = item["played_at"]
            seed_raw = item.get("seed")
            if not isinstance(mode, str) or mode not in valid_modes:
                continue
            if not isinstance(difficulty, str) or difficulty not in DIFFICULTIES:
                continue
            if not isinstance(won, bool):
                continue
            if isinstance(attempts_raw, bool) or isinstance(elapsed_raw, bool):
                continue
            attempts = int(attempts_raw)
            elapsed = float(elapsed_raw)
            if attempts < 0 or elapsed < 0:
                continue
            if not isinstance(played_at, str) or not played_at or len(played_at) > 80:
                continue
            if seed_raw is None:
                seed = None
            elif isinstance(seed_raw, bool):
                continue
            else:
                seed = int(seed_raw)
            result.append(
                HistoryEntry(
                    mode=mode,
                    difficulty=difficulty,
                    won=won,
                    attempts=attempts,
                    elapsed_seconds=elapsed,
                    seed=seed,
                    played_at=played_at,
                )
            )
        except (KeyError, TypeError, ValueError, OverflowError):
            continue
    return result[-MAX_HISTORY_ENTRIES:]
