"""Tests that every conformance/valid/*.json fixture passes its JSON Schema."""

import json
import pathlib

import pytest

from .helpers import REPO_ROOT, infer_schema, validate_instance

_VALID_DIR = REPO_ROOT / "conformance" / "valid"
_fixtures = sorted(_VALID_DIR.glob("*.json"))


@pytest.mark.parametrize(
    "fixture_path",
    _fixtures,
    ids=[f.stem for f in _fixtures],
)
def test_valid_fixture_passes_schema(fixture_path: pathlib.Path) -> None:
    schema_path = infer_schema(fixture_path)
    if schema_path is None:
        pytest.skip(f"no schema mapping for {fixture_path.name}")

    validate_instance(schema_path, json.loads(fixture_path.read_text()))
