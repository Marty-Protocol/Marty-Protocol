"""Regression checks for revocation-mechanism standard references."""

import json

import pytest
from jsonschema import ValidationError

from .helpers import REPO_ROOT, validate_instance


def test_token_status_list_references_active_ietf_draft() -> None:
    enum_path = REPO_ROOT / "enums" / "revocation-methods.json"
    enum_data = json.loads(enum_path.read_text(encoding="utf-8"))
    token_status = enum_data["$defs"]["values"]["TOKEN_STATUS_LIST"]

    assert token_status["standard"] == "IETF draft-ietf-oauth-status-list"

    specification = (
        REPO_ROOT / "protocol" / "revocation-profile" / "SPECIFICATION.md"
    ).read_text(encoding="utf-8")
    assert "| `TOKEN_STATUS_LIST` | IETF draft-ietf-oauth-status-list |" in specification
    assert "RFC 9738" not in specification


@pytest.mark.parametrize(
    "mode, duration",
    [
        ("ALWAYS", None),
        ("CACHED", "cache_ttl_seconds"),
        ("OFFLINE_GRACE", "offline_grace_seconds"),
        ("DISABLED", None),
    ],
)
def test_revocation_timing_modes_require_their_configuration(mode, duration) -> None:
    schema = REPO_ROOT / "schemas" / "revocation-profile.json"
    profile = json.loads(
        (REPO_ROOT / "conformance" / "valid" / "revocation-profile.json").read_text()
    )
    profile.pop("cache_ttl_seconds", None)
    profile["check_mode"] = mode
    if duration:
        with pytest.raises(ValidationError):
            validate_instance(schema, profile)
        profile[duration] = 60
    validate_instance(schema, profile)

    # SKIP controls check failures in a different enum; it is never a timing mode.
    profile["check_mode"] = "SKIP"
    with pytest.raises(ValidationError):
        validate_instance(schema, profile)


def test_revocation_timing_vocabulary_is_distinct_from_failure_modes() -> None:
    timing = json.loads((REPO_ROOT / "enums" / "revocation-timing-modes.json").read_text())
    assert set(timing["enum"]) == {"ALWAYS", "CACHED", "OFFLINE_GRACE", "DISABLED"}
