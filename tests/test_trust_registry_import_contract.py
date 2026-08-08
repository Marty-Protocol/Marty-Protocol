"""Public Marty Trust Registry Sync v1 contract invariants."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from .helpers import REPO_ROOT, validate_instance


TRUST_PROFILE_SCHEMA = REPO_ROOT / "schemas" / "trust-profile.json"
SYNC_SCHEMA = REPO_ROOT / "schemas" / "trust-registry-sync.json"
RESULT_SCHEMA = REPO_ROOT / "schemas" / "trust-profile-registry-sync-result.json"


def _load(relative_path: str) -> object:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    ("schema", "fixture"),
    [
        (TRUST_PROFILE_SCHEMA, "conformance/valid/trust-profile.json"),
        (SYNC_SCHEMA, "conformance/valid/trust-registry-sync.json"),
        (RESULT_SCHEMA, "conformance/valid/trust-profile-registry-sync-result.json"),
    ],
)
def test_public_registry_contract_accepts_canonical_fixtures(
    schema: Path,
    fixture: str,
) -> None:
    validate_instance(schema, _load(fixture))


@pytest.mark.parametrize(
    ("schema", "fixture"),
    [
        (TRUST_PROFILE_SCHEMA, "conformance/invalid/trust-profile-missing-registry-sync.json"),
        (TRUST_PROFILE_SCHEMA, "conformance/invalid/trust-profile-unsafe-registry-url.json"),
        (SYNC_SCHEMA, "conformance/invalid/trust-registry-sync-add-without-certificate.json"),
        (SYNC_SCHEMA, "conformance/invalid/trust-registry-sync-missing-source.json"),
        (RESULT_SCHEMA, "conformance/invalid/trust-profile-registry-sync-result-http-url.json"),
        (
            RESULT_SCHEMA,
            "conformance/invalid/trust-profile-registry-sync-result-internal-state.json",
        ),
    ],
)
def test_public_registry_contract_rejects_unsafe_or_private_shapes(
    schema: Path,
    fixture: str,
) -> None:
    with pytest.raises(ValidationError):
        validate_instance(schema, _load(fixture))


def test_every_bundled_url_registry_example_declares_its_wire_adapter() -> None:
    candidates = [REPO_ROOT / "conformance" / "valid" / "trust-profile.json"]
    candidates.extend((REPO_ROOT / "examples").glob("**/trust-profile.json"))

    for candidate in candidates:
        profile = json.loads(candidate.read_text(encoding="utf-8"))
        for source in profile.get("trust_sources", []):
            if source.get("source_type") not in {"TRUST_LIST", "PKD_URL"}:
                continue
            assert source.get("registry_sync") == {
                "protocol": "MARTY_TRUST_REGISTRY_SYNC_V1",
                "refresh_interval_hours": 24,
            }, candidate
