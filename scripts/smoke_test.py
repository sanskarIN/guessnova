"""Small end-to-end smoke check used locally and in CI."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from guessnova.engine import GuessGame, ReverseGuesser
from guessnova.history import filter_history
from guessnova.i18n import catalog_missing_keys, text
from guessnova.import_export import export_state, import_state
from guessnova.replay import decode_replay, encode_replay
from guessnova.service import GameService
from guessnova.storage import Storage


def main() -> int:
    with TemporaryDirectory(prefix="guessnova-smoke-") as directory:
        root = Path(directory)
        storage = Storage(root / "data")

        game = GuessGame(difficulty_name="easy", seed=20260819, target=42)
        game.guess(42)
        summary = game.summary()
        assert summary.won and summary.target == 42

        profile, unlocked = GameService(storage).record(summary, "Smoke Player")
        assert profile.stats.games_played == 1
        assert profile.stats.games_won == 1
        assert "first_win" in unlocked
        assert storage.load_leaderboard()
        assert len(filter_history(profile.history, result="win")) == 1

        replay = encode_replay(summary)
        assert decode_replay(replay) == summary

        renamed = storage.rename_profile("Smoke Player", "Smoke Nova")
        assert renamed.name == "Smoke Nova"
        assert storage.active_profile_name() == "Smoke Nova"
        assert storage.load_leaderboard()[0].player == "Smoke Nova"

        storage.delete_profile("Smoke Nova")
        assert storage.list_deleted_profile_names() == ["Smoke Nova"]
        restored = storage.restore_profile("Smoke Nova")
        assert restored.stats.games_won == 1
        assert storage.load_leaderboard()[0].player == "Smoke Nova"

        assert catalog_missing_keys("hi") == set()
        assert "7" in text("reverse.solved", locale="hi", attempts=7)

        backup = export_state(storage.load_raw(), root / "backup.json")
        imported = import_state(backup)
        assert imported["active_profile"] == "Smoke Nova"

        reverse = ReverseGuesser(1, 100)
        secret = 73
        while not reverse.finished:
            guess = reverse.next_guess()
            response = "correct" if guess == secret else "higher" if guess < secret else "lower"
            reverse.respond(response)
        assert reverse.attempts <= 7

    print("GuessNova smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
