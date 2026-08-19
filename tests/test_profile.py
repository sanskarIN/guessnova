from guessnova.profile import Profile


def test_profile_round_trip() -> None:
    profile = Profile("Nova Player")
    profile.stats.games_played = 5
    profile.stats.achievements.add("first_win")
    restored = Profile.from_dict(profile.to_dict())
    assert restored.name == "Nova Player"
    assert restored.stats.games_played == 5
    assert restored.stats.achievements == {"first_win"}


def test_profile_sanitizes_name() -> None:
    assert Profile("  A<script>B  ").name == "AscriptB"
