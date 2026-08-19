from guessnova.achievements import apply_summary
from guessnova.domain import GameMode, GameSummary, PlayerStats


def summary(*, won: bool = True, attempts: int = 1, difficulty: str = "normal") -> GameSummary:
    return GameSummary(GameMode.CLASSIC, difficulty, 42, won, attempts, 1.0, (42,))


def test_first_win_and_one_shot_unlock() -> None:
    stats = PlayerStats()
    unlocked = apply_summary(stats, summary())
    assert {"first_win", "one_shot"} <= unlocked
    assert stats.games_won == 1
    assert stats.xp > 0


def test_loss_breaks_streak() -> None:
    stats = PlayerStats(current_streak=3)
    apply_summary(stats, summary(won=False, attempts=9))
    assert stats.current_streak == 0


def test_expert_win_unlocks() -> None:
    stats = PlayerStats()
    apply_summary(stats, summary(difficulty="expert"))
    assert "expert_win" in stats.achievements
