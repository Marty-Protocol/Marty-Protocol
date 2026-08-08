from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from .helpers import REPO_ROOT, validate_instance


SCHEMA = REPO_ROOT / "schemas" / "trust-profile.json"
FIXTURE = REPO_ROOT / "conformance" / "valid" / "trust-profile.json"


@pytest.mark.parametrize("status", ["draft", "active", "suspended", "archived"])
def test_trust_profile_accepts_only_canonical_lowercase_lifecycle_status(
    status: str,
) -> None:
    instance = json.loads(FIXTURE.read_text(encoding="utf-8"))
    instance["status"] = status
    validate_instance(SCHEMA, instance)


def test_trust_profile_rejects_legacy_uppercase_lifecycle_status() -> None:
    instance = json.loads(FIXTURE.read_text(encoding="utf-8"))
    instance["status"] = "ACTIVE"

    with pytest.raises(ValidationError):
        validate_instance(SCHEMA, instance)


def test_generated_bindings_publish_the_lifecycle_contract() -> None:
    python_enums = (REPO_ROOT / "reference/python/mip_types/enums.py").read_text()
    python = (REPO_ROOT / "reference/python/mip_types/models.py").read_text()
    typescript_enums = (REPO_ROOT / "reference/typescript/src/enums.ts").read_text()
    typescript = (REPO_ROOT / "reference/typescript/src/models.ts").read_text()
    rust_enums = (REPO_ROOT / "reference/rust/src/enums.rs").read_text()
    rust = (REPO_ROOT / "reference/rust/src/models.rs").read_text()

    assert "class TrustProfileStatus(str, Enum):" in python_enums
    assert "status: TrustProfileStatus" in python
    assert "export enum TrustProfileStatus" in typescript_enums
    assert "status: TrustProfileStatus;" in typescript
    assert "pub enum TrustProfileStatus" in rust_enums
    assert "pub status: TrustProfileStatus," in rust
