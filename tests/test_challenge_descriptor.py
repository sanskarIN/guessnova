from __future__ import annotations

import json
from pathlib import Path

from guessnova.challenge_descriptor import PortableChallengeDescriptor

FIXTURES = Path(__file__).parent / "fixtures" / "portable_challenges_v1.json"


def test_shared_portable_challenge_vectors_match_python() -> None:
    payload = json.loads(FIXTURES.read_text(encoding="utf-8"))
    assert isinstance(payload, list)
    for vector in payload:
        descriptor_payload = vector["descriptor"]
        target = vector["target"]
        assert isinstance(descriptor_payload, dict)
        assert isinstance(target, int)
        descriptor = PortableChallengeDescriptor.from_dict(descriptor_payload)
        assert descriptor.to_dict() == descriptor_payload
        assert descriptor.target() == target
        assert descriptor.build_game().target == target
