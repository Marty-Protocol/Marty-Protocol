"""Regression checks for revocation-mechanism standard references."""

import json

from .helpers import REPO_ROOT


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
