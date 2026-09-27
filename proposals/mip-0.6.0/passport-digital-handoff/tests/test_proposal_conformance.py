"""Validate only proposal fixtures against proposal-local schema overrides."""

import json

import pytest
from jsonschema import ValidationError

from .helpers import REPO_ROOT, infer_schema, validate_instance


@pytest.mark.parametrize("fixture", sorted((REPO_ROOT / "conformance" / "valid").glob("*.json")))
def test_proposed_valid_fixture(fixture) -> None:
    schema = infer_schema(fixture)
    assert schema is not None, fixture.name
    validate_instance(schema, json.loads(fixture.read_text(encoding="utf-8")))


@pytest.mark.parametrize(
    "fixture",
    sorted(
        path for path in (REPO_ROOT / "conformance" / "invalid").glob("*.json")
        if not path.name.endswith(".expected.json")
    ),
)
def test_proposed_invalid_fixture(fixture) -> None:
    schema = infer_schema(fixture)
    assert schema is not None, fixture.name
    with pytest.raises(ValidationError):
        validate_instance(schema, json.loads(fixture.read_text(encoding="utf-8")))
