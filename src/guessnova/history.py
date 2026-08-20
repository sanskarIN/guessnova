"""Bounded local session-history records and query helpers."""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
from typing import Literal

from .domain import DIFFICULTIES, GameMode, GameSummary

MAX_HISTORY_ENTRIES = 200
HistoryResult = Literal["win", "loss"]
HistoryGroup = Literal["day", "mode", "difficulty", "result"]


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


def _entry_date(entry: HistoryEntry) -> date | None:
    try:
        return datetime.fromisoformat(entry.played_at.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def filter_history(
    entries: list[HistoryEntry],
    *,
    mode: str | None = None,
    difficulty: str | None = None,
    result: HistoryResult | None = None,
    query: str | None = None,
    since: date | None = None,
    until: date | None = None,
) -> list[HistoryEntry]:
    """Return entries matching optional structured and free-text filters."""
    needle = query.casefold().strip() if query else ""
    filtered: list[HistoryEntry] = []
    for entry in entries:
        if mode is not None and entry.mode != mode:
            continue
        if difficulty is not None and entry.difficulty != difficulty:
            continue
        if result == "win" and not entry.won:
            continue
        if result == "loss" and entry.won:
            continue
        played_on = _entry_date(entry)
        if since is not None and (played_on is None or played_on < since):
            continue
        if until is not None and (played_on is None or played_on > until):
            continue
        if needle:
            searchable = " ".join(
                (
                    entry.played_at,
                    entry.mode,
                    entry.difficulty,
                    "win" if entry.won else "loss",
                    str(entry.attempts),
                    str(entry.seed) if entry.seed is not None else "",
                )
            ).casefold()
            if needle not in searchable:
                continue
        filtered.append(entry)
    return filtered


def group_history(
    entries: list[HistoryEntry], *, by: HistoryGroup
) -> dict[str, list[HistoryEntry]]:
    """Group history while preserving the first-seen group ordering."""
    groups: defaultdict[str, list[HistoryEntry]] = defaultdict(list)
    for entry in entries:
        if by == "day":
            played_on = _entry_date(entry)
            key = played_on.isoformat() if played_on is not None else "unknown-date"
        elif by == "mode":
            key = entry.mode
        elif by == "difficulty":
            key = entry.difficulty
        elif by == "result":
            key = "win" if entry.won else "loss"
        else:
            raise ValueError(f"unsupported history grouping: {by}")
        groups[key].append(entry)
    return dict(groups)


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
        mode = item.get("mode")
        difficulty = item.get("difficulty")
        won = item.get("won")
        attempts_raw = item.get("attempts")
        elapsed_raw = item.get("elapsed_seconds")
        played_at = item.get("played_at")
        seed_raw = item.get("seed")
        if not isinstance(mode, str) or mode not in valid_modes:
            continue
        if not isinstance(difficulty, str) or difficulty not in DIFFICULTIES:
            continue
        if not isinstance(won, bool):
            continue
        if isinstance(attempts_raw, bool) or not isinstance(attempts_raw, int):
            continue
        if isinstance(elapsed_raw, bool) or not isinstance(elapsed_raw, (int, float)):
            continue
        attempts = attempts_raw
        elapsed = float(elapsed_raw)
        rules = DIFFICULTIES[difficulty]
        if attempts < 0 or attempts > rules.max_attempts:
            continue
        if won and attempts < 1:
            continue
        if elapsed < 0 or not math.isfinite(elapsed):
            continue
        if not isinstance(played_at, str) or not played_at or len(played_at) > 80:
            continue
        if seed_raw is None:
            seed = None
        elif isinstance(seed_raw, bool) or not isinstance(seed_raw, int):
            continue
        else:
            seed = seed_raw
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
    return result[-MAX_HISTORY_ENTRIES:]
