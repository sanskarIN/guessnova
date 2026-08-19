from guessnova.achievements import apply_summary
from guessnova.domain import GameMode, GameSummary, PlayerStats


def summary(
    *, won: bool = True, attempts: int = 1, difficulty: str = "normal", hint_penalty: int = 0
) -> GameSummary:
    return GameSummary(
        GameMode.CLASSIC,
        difficulty,
        42,
        won,
        attempts,
        1.0,
        (42,),
        hint_penalty=hint_penalty,
    )


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


def test_hint_penalty_reduces_winning_xp_without_dropping_below_floor() -> None:
    without_hint = PlayerStats()
    with_hint = PlayerStats()
    apply_summary(without_hint, summary(attempts=2))
    apply_summary(with_hint, summary(attempts=2, hint_penalty=20))
    assert with_hint.xp == without_hint.xp - 20

    floor = PlayerStats()
    apply_summary(floor, summary(attempts=20, hint_penalty=999))
    assert floor.xp == 10
