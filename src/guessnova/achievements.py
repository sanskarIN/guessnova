"""Achievement and XP rules."""

from __future__ import annotations

from .domain import GameSummary, PlayerStats

ACHIEVEMENT_LABELS = {
    "first_win": "First Light",
    "one_shot": "Nova Instinct",
    "streak_5": "On Fire",
    "veteran_25": "Seasoned Explorer",
    "expert_win": "Event Horizon",
}


def apply_summary(stats: PlayerStats, summary: GameSummary) -> set[str]:
    before = set(stats.achievements)
    stats.games_played += 1
    if summary.won:
        stats.games_won += 1
        stats.current_streak += 1
        stats.best_streak = max(stats.best_streak, stats.current_streak)
        stats.total_guesses += summary.attempts
        stats.xp += max(10, 120 - summary.attempts * 8)
    else:
        stats.current_streak = 0
        stats.xp += 2

    if stats.games_won >= 1:
        stats.achievements.add("first_win")
    if summary.won and summary.attempts == 1:
        stats.achievements.add("one_shot")
    if stats.current_streak >= 5:
        stats.achievements.add("streak_5")
    if stats.games_played >= 25:
        stats.achievements.add("veteran_25")
    if summary.won and summary.difficulty == "expert":
        stats.achievements.add("expert_win")
    return stats.achievements - before
