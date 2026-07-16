"""Validate every bundled system Compliance Profile against the normative schema."""

import json

import pytest

from .helpers import REPO_ROOT, SCHEMAS_DIR, validate_instance


_profiles = sorted((REPO_ROOT / "compliance-profiles").rglob("*.json"))


@pytest.mark.parametrize(
    "profile_path",
    _profiles,
    ids=[str(path.relative_to(REPO_ROOT)) for path in _profiles],
)
def test_bundled_compliance_profile_passes_schema(profile_path):
    validate_instance(
        SCHEMAS_DIR / "compliance-profile.json",
        json.loads(profile_path.read_text(encoding="utf-8")),
    )
