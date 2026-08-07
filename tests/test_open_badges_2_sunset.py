"""Keep the one approved compatibility profile narrow and time-bounded."""

import json

from .helpers import REPO_ROOT


def test_open_badges_2_is_a_documented_temporary_exception() -> None:
    document = json.loads(
        (REPO_ROOT / "enums" / "compliance-codes.json").read_text(encoding="utf-8")
    )
    policy = document["$defs"]["values"]["OB2_COMPATIBILITY"]

    assert "OB2_COMPATIBILITY" in document["enum"]
    assert policy["deprecated"] is True
    assert policy["migration_target"] == "OB3_JWT or OB3_JSONLD"
    assert policy["review_date"] == "2026-09-01"
    assert policy["target_removal_date"] == "2026-10-01"


def test_open_badges_3_remains_the_current_profile() -> None:
    document = json.loads(
        (REPO_ROOT / "enums" / "compliance-codes.json").read_text(encoding="utf-8")
    )

    assert {"OB3_JWT", "OB3_JSONLD"} <= set(document["enum"])
    assert not list((REPO_ROOT / "compliance-profiles").rglob("*ob2*.json"))
