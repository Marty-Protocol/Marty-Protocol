"""Validate only proposal fixtures against proposal-local schema overrides."""

import json
from urllib.parse import urljoin

import pytest
from jsonschema import ValidationError

from .helpers import REPO_ROOT, infer_schema, validate_instance

CANDIDATE_BASE = "https://raw.githubusercontent.com/marty-protocol/marty-protocol/0.6.0-beta.1/"


def _external_refs(value: object):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref" and isinstance(child, str) and not child.startswith("#"):
                yield child
            else:
                yield from _external_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from _external_refs(child)


def test_candidate_schema_ids_are_versioned_and_reference_closed() -> None:
    schemas = {}
    for directory in ("schemas", "enums"):
        for path in sorted((REPO_ROOT / directory).glob("*.json")):
            schema = json.loads(path.read_text(encoding="utf-8"))
            expected_id = CANDIDATE_BASE + path.relative_to(REPO_ROOT).as_posix()
            assert schema["$id"] == expected_id
            assert expected_id not in schemas
            schemas[expected_id] = schema

    for schema_id, schema in schemas.items():
        for reference in _external_refs(schema):
            assert urljoin(schema_id, reference).split("#", 1)[0] in schemas


@pytest.mark.parametrize("fixture", sorted((REPO_ROOT / "conformance" / "valid").glob("*.json")))
def test_proposed_valid_fixture_with_candidate_only_registry(fixture) -> None:
    schema = infer_schema(fixture)
    assert schema is not None, fixture.name
    if schema.is_relative_to(REPO_ROOT):
        validate_instance(schema, json.loads(fixture.read_text(encoding="utf-8")), candidate_only=True)


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
