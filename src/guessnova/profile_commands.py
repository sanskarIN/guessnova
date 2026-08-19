"""Rich CLI handlers for safe local profile lifecycle operations."""

from __future__ import annotations

import argparse

from rich.console import Console
from rich.markup import escape
from rich.table import Table

from .i18n import text
from .storage import Storage


def run_profiles(args: argparse.Namespace, console: Console) -> int:
    """Execute a profile-management subcommand."""
    storage = Storage()
    action = args.profile_action
    locale = args.locale

    if action == "list":
        names = storage.list_profile_names()
        active = storage.active_profile_name()
        if not names:
            console.print(text("profiles.empty", locale=locale))
            return 0
        if args.compact:
            for name in names:
                marker = "*" if name == active else "-"
                console.print(f"{marker} {escape(name)}")
            return 0
        table = Table(title=text("profiles.title", locale=locale))
        table.add_column(text("profiles.name", locale=locale))
        table.add_column(text("profiles.active", locale=locale))
        for name in names:
            table.add_row(escape(name), "yes" if name == active else "")
        console.print(table)
        return 0

    if action == "create":
        profile = storage.create_profile(args.name, make_active=not args.no_activate)
        console.print(text("profiles.created", locale=locale, name=escape(profile.name)))
        return 0

    if action == "use":
        profile = storage.set_active_profile(args.name)
        console.print(text("profiles.activated", locale=locale, name=escape(profile.name)))
        return 0

    if action == "rename":
        profile = storage.rename_profile(args.current_name, args.new_name)
        console.print(text("profiles.renamed", locale=locale, name=escape(profile.name)))
        return 0

    if action == "delete":
        normalized = storage.load_profile(args.name).name
        if not args.yes:
            prompt = text("profiles.delete_confirm", locale=locale, name=normalized)
            response = console.input(prompt).strip()
            if response != normalized:
                console.print(text("profiles.delete_cancelled", locale=locale))
                return 1
        storage.delete_profile(normalized)
        console.print(text("profiles.deleted", locale=locale, name=escape(normalized)))
        console.print(text("profiles.restore_hint", locale=locale, name=escape(normalized)))
        return 0

    if action == "trash":
        names = storage.list_deleted_profile_names()
        if not names:
            console.print(text("profiles.trash_empty", locale=locale))
            return 0
        for name in names:
            console.print(f"- {escape(name)}")
        return 0

    if action == "restore":
        profile = storage.restore_profile(args.name, make_active=not args.no_activate)
        console.print(text("profiles.restored", locale=locale, name=escape(profile.name)))
        return 0

    raise ValueError(f"unsupported profile action: {action}")


def configure_profiles_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Attach the profile-management command tree to the main parser."""
    parser = subparsers.add_parser("profiles", help="manage local profiles safely")
    actions = parser.add_subparsers(dest="profile_action", required=True)

    list_parser = actions.add_parser("list", help="list saved profiles")
    list_parser.set_defaults(func=run_profiles)

    create_parser = actions.add_parser("create", help="create a local profile")
    create_parser.add_argument("name")
    create_parser.add_argument("--no-activate", action="store_true")
    create_parser.set_defaults(func=run_profiles)

    use_parser = actions.add_parser("use", help="set the active profile")
    use_parser.add_argument("name")
    use_parser.set_defaults(func=run_profiles)

    rename_parser = actions.add_parser("rename", help="rename a saved profile")
    rename_parser.add_argument("current_name")
    rename_parser.add_argument("new_name")
    rename_parser.set_defaults(func=run_profiles)

    delete_parser = actions.add_parser("delete", help="move a profile to recoverable trash")
    delete_parser.add_argument("name")
    delete_parser.add_argument("--yes", action="store_true", help="skip typed-name confirmation")
    delete_parser.set_defaults(func=run_profiles)

    trash_parser = actions.add_parser("trash", help="list recoverable deleted profiles")
    trash_parser.set_defaults(func=run_profiles)

    restore_parser = actions.add_parser("restore", help="restore a deleted profile")
    restore_parser.add_argument("name")
    restore_parser.add_argument("--no-activate", action="store_true")
    restore_parser.set_defaults(func=run_profiles)
