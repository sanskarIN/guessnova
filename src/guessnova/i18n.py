"""Small externalized message catalog with English as the shipped locale."""

from __future__ import annotations

from typing import Final

DEFAULT_LOCALE: Final = "en"

EN_MESSAGES: Final[dict[str, str]] = {
    "app.name": "GuessNova",
    "app.tagline": "Number Guessing, Supernova Style",
    "app.description": "A modern number guessing game",
    "play.correct": "Correct! A new star is born.",
    "play.too_low": "Too low.",
    "play.too_high": "Too high.",
    "play.out_of_range": "That number is outside this challenge range.",
    "play.timeout": "Time expired.",
    "play.exhausted": "No attempts remain.",
    "play.hint_prefix": "Hint: {hint}",
    "play.hint_instruction": "Type 'hint' for a narrowed range clue.",
    "play.abandoned": "Challenge abandoned.",
    "play.input_invalid": "Enter a whole number, 'hint', or q to quit.",
    "play.prompt": "Guess [{attempts_left} left] › ",
    "play.summary": "Target: {target} · Attempts: {attempts} · {elapsed:.1f}s · Hints: {hints}",
    "play.progress": "XP: {xp} · Win rate: {win_rate:.0%}",
    "play.replay": "Replay: {code}",
    "achievement.unlocked": "Achievement unlocked: {label}",
    "achievement.first_win": "First Light",
    "achievement.one_shot": "Nova Instinct",
    "achievement.streak_5": "On Fire",
    "achievement.veteran_25": "Seasoned Explorer",
    "achievement.expert_win": "Event Horizon",
    "reverse.intro": "Think of a number from 1 to 100. GuessNova will find it.",
    "reverse.prompt": "Is it {guess}? [higher/lower/correct] › ",
    "reverse.solved": "Solved in {attempts} guesses.",
    "stats.title": "{profile} · Statistics",
    "stats.games": "Games",
    "stats.wins": "Wins",
    "stats.win_rate": "Win rate",
    "stats.average_guesses": "Average guesses",
    "stats.current_streak": "Current streak",
    "stats.best_streak": "Best streak",
    "stats.xp": "XP",
    "stats.achievements": "Achievements",
    "stats.history_entries": "History entries",
    "history.empty": "No matching session history yet.",
    "history.title": "{profile} · Session History",
    "history.when": "When",
    "history.mode": "Mode",
    "history.difficulty": "Difficulty",
    "history.result": "Result",
    "history.attempts": "Attempts",
    "history.time": "Time",
    "history.win": "Win",
    "history.loss": "Loss",
    "leaderboard.empty": "No leaderboard entries yet.",
    "leaderboard.title": "Local Leaderboard",
    "leaderboard.player": "Player",
    "settings.title": "{profile} · Settings",
    "settings.setting": "Setting",
    "settings.value": "Value",
    "settings.saved": "Settings saved locally.",
    "about.title": "About GuessNova",
    "about.description": "Privacy-first open-source number guessing game",
    "about.license": "License: MIT",
    "about.repository": "Repository: {url}",
    "about.github": "GitHub: {url}",
    "about.business": "Business: {email}",
    "about.support": "Support: {email}",
    "about.funding": "Buy Me a Coffee: {url}",
    "data.exported": "Exported to {path}",
    "data.import_complete": "Import complete.",
    "onboarding.title": "Welcome to GuessNova",
    "onboarding.body": "Guess a hidden number, type 'hint' for help, or q to quit. Your profile, settings, history, and leaderboard stay local on this device.",
    "onboarding.settings": "Use `guessnova settings` for themes, high contrast, reduced motion, and smart-hint preferences.",
    "tui.title": "Guess the hidden number",
    "tui.input_placeholder": "Enter a whole number",
    "tui.submit": "Launch Guess",
    "tui.range": "Range {minimum}–{maximum} · {attempts_left} attempts",
    "tui.enter_first": "Enter a number first.",
    "tui.correct": "Correct! The target was {target}. Press R for a new game.",
    "tui.round_over": "Round over. Target: {target}. Press R for a new game.",
    "tui.outside_range": "Outside the current range.",
}

CATALOGS: Final[dict[str, dict[str, str]]] = {DEFAULT_LOCALE: EN_MESSAGES}


def available_locales() -> tuple[str, ...]:
    """Return stable locale identifiers exposed to settings/UI code."""
    return tuple(sorted(CATALOGS))


def text(key: str, /, *, locale: str = DEFAULT_LOCALE, **values: object) -> str:
    """Resolve and format a catalog message, falling back to English."""
    catalog = CATALOGS.get(locale, EN_MESSAGES)
    template = catalog.get(key) or EN_MESSAGES.get(key)
    if template is None:
        raise KeyError(f"unknown message key: {key}")
    try:
        return template.format(**values)
    except (KeyError, ValueError) as exc:
        raise ValueError(f"invalid values for message key: {key}") from exc
