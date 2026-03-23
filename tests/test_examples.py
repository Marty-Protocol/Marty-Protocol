"""Tests that every examples/**/*.json file passes its JSON Schema.

Both minimal/ and realistic/ sub-trees are covered. Files whose schema
cannot be inferred from the filename are skipped (pytest.skip).
"""

import json
import pathlib

import pytest

from .helpers import REPO_ROOT, infer_schema, validate_instance

_EXAMPLES_DIR = REPO_ROOT / "examples"
_fixtures = sorted(_EXAMPLES_DIR.rglob("*.json"))


@pytest.mark.parametrize(
    "fixture_path",
    _fixtures,
    ids=[str(f.relative_to(REPO_ROOT)) for f in _fixtures],
)
def test_example_passes_schema(fixture_path: pathlib.Path) -> None:
    schema_path = infer_schema(fixture_path)
    if schema_path is None:
        pytest.skip(f"no schema mapping for {fixture_path.name}")

    validate_instance(schema_path, json.loads(fixture_path.read_text()))
