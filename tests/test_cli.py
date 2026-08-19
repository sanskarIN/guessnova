from guessnova.cli import build_parser, main


def test_parser_defaults() -> None:
    args = build_parser().parse_args(["play", "--no-save"])
    assert args.difficulty == "normal"
    assert args.mode == "classic"


def test_help_without_subcommand() -> None:
    assert main([]) == 0
