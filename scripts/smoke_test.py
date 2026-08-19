"""Small end-to-end smoke check used locally and in CI."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from guessnova.backup_inspection import inspect_backup
from guessnova.constants import SCHEMA_VERSION
from guessnova.diagnostics import diagnose, repair
from guessnova.engine import GuessGame, ReverseGuesser
from guessnova.entrypoint import main as app_main
from guessnova.history import filter_history
from guessnova.i18n import catalog_missing_keys, text
from guessnova.import_export import EXPORT_VERSION, export_state, import_state
from guessnova.replay import decode_replay, encode_replay
from guessnova.service import GameService
from guessnova.storage import Storage
from guessnova.tui_workspace import (
    build_workspace_game,
    load_workspace_snapshot,
    save_workspace_settings,
    select_history,
    select_leaderboard,
)


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
        assert storage.load_raw()["schema_version"] == SCHEMA_VERSION == 2
        assert diagnose(storage).healthy
        assert app_main(["doctor", "--compact", "--data-dir", str(storage.data_dir)]) == 0

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

        snapshot = load_workspace_snapshot(storage, "Smoke Nova")
        assert snapshot.profile.name == "Smoke Nova"
        assert snapshot.profile_names == ("Smoke Nova",)
        assert snapshot.deleted_profile_names == ()
        assert snapshot.leaderboard_count == 1
        assert snapshot.diagnostics.healthy
        assert len(select_history(snapshot.profile, result="win")) == 1
        assert select_leaderboard(storage.load_leaderboard(), player="smoke")[0].player == (
            "Smoke Nova"
        )

        configured = build_workspace_game(
            mode="timed",
            difficulty="hard",
            seed_text="20260819",
        )
        configured_again = build_workspace_game(
            mode="timed",
            difficulty="hard",
            seed_text="20260819",
        )
        assert configured.mode.value == "timed"
        assert configured.target_value == configured_again.target_value
        daily = build_workspace_game(
            mode="daily",
            difficulty="normal",
            day_text="2026-08-19",
        )
        daily_again = build_workspace_game(
            mode="daily",
            difficulty="normal",
            day_text="2026-08-19",
        )
        assert daily.seed == daily_again.seed
        assert daily.target_value == daily_again.target_value

        workspace_profile = save_workspace_settings(
            storage,
            "Smoke Nova",
            theme="mono",
            locale="hi",
            reduced_motion=True,
            high_contrast=True,
            sound=False,
            show_smart_hints=False,
        )
        assert workspace_profile.settings.locale == "hi"
        assert workspace_profile.settings.high_contrast is True
        assert workspace_profile.settings.show_smart_hints is False

        assert catalog_missing_keys("hi") == set()
        assert "7" in text("reverse.solved", locale="hi", attempts=7)

        backup = export_state(storage.load_raw(), root / "backup.json")
        wrapped = json.loads(backup.read_text(encoding="utf-8"))
        assert wrapped["version"] == EXPORT_VERSION == 2
        assert wrapped["schema_version"] == SCHEMA_VERSION
        assert len(wrapped["integrity"]["payload_sha256"]) == 64
        inspection = inspect_backup(backup)
        assert inspection.integrity_protected
        assert inspection.normalized_schema_version == SCHEMA_VERSION
        assert inspection.profile_count == 1
        assert app_main(["doctor", "--compact", "--verify-backup", str(backup)]) == 0
        imported = import_state(backup)
        assert imported["active_profile"] == "Smoke Nova"

        legacy = Storage(root / "legacy-data")
        legacy.data_dir.mkdir(parents=True, exist_ok=True)
        legacy.path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "active_profile": "Legacy",
                    "profiles": {
                        "Legacy": {"name": "Legacy", "stats": {}, "settings": {}}
                    },
                    "leaderboard": [],
                }
            ),
            encoding="utf-8",
        )
        before = diagnose(legacy)
        assert not before.healthy and before.source_schema_version == 1
        repair_backup = repair(legacy, backup_dir=root / "repair-backups")
        assert repair_backup is not None and repair_backup.exists()
        repair_inspection = inspect_backup(repair_backup)
        assert repair_inspection.schema_version == 1
        assert repair_inspection.normalized_schema_version == SCHEMA_VERSION
        assert import_state(repair_backup)["schema_version"] == 1
        assert legacy.load_raw()["schema_version"] == SCHEMA_VERSION
        assert diagnose(legacy).healthy

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
