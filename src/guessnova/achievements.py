"""Achievement and XP rules."""

from __future__ import annotations

from .domain import GameSummary, PlayerStats
from .i18n import DEFAULT_LOCALE, text

ACHIEVEMENT_MESSAGE_KEYS = {
    "first_win": "achievement.first_win",
    "one_shot": "achievement.one_shot",
    "streak_5": "achievement.streak_5",
    "veteran_25": "achievement.veteran_25",
    "expert_win": "achievement.expert_win",
}

# English compatibility mapping retained for callers that consume the original constant.
ACHIEVEMENT_LABELS = {
    key: text(message_key, locale=DEFAULT_LOCALE)
    for key, message_key in ACHIEVEMENT_MESSAGE_KEYS.items()
}


def achievement_label(key: str, *, locale: str = DEFAULT_LOCALE) -> str:
    message_key = ACHIEVEMENT_MESSAGE_KEYS.get(key)
    return text(message_key, locale=locale) if message_key is not None else key


def apply_summary(stats: PlayerStats, summary: GameSummary) -> set[str]:
    before = set(stats.achievements)
    stats.games_played += 1
    if summary.won:
        stats.games_won += 1
        stats.current_streak += 1
        stats.best_streak = max(stats.best_streak, stats.current_streak)
        stats.total_guesses += summary.attempts
        stats.xp += max(10, 120 - summary.attempts * 8 - summary.hint_penalty)
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
