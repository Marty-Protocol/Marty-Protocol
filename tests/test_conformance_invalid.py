"""Tests that every conformance/invalid/*.json fixture FAILS its JSON Schema.

For each invalid fixture a paired *.expected.json sidecar may exist. When it
does, the test additionally asserts that the error JSON Pointer recorded in
that sidecar appears somewhere in the jsonschema ValidationError tree.
"""

import json
import pathlib

import pytest
from jsonschema import ValidationError

from .helpers import REPO_ROOT, infer_schema, validate_instance, all_error_pointers

_INVALID_DIR = REPO_ROOT / "conformance" / "invalid"
_fixtures = sorted(
    f for f in _INVALID_DIR.glob("*.json") if not f.name.endswith(".expected.json")
)


@pytest.mark.parametrize(
    "fixture_path",
    _fixtures,
    ids=[f.stem for f in _fixtures],
)
def test_invalid_fixture_fails_schema(fixture_path: pathlib.Path) -> None:
    schema_path = infer_schema(fixture_path)
    if schema_path is None:
        pytest.skip(f"no schema mapping for {fixture_path.name}")

    instance = json.loads(fixture_path.read_text())

    with pytest.raises(ValidationError) as exc_info:
        validate_instance(schema_path, instance)

    # ── Pointer check from .expected.json sidecar ────────────────────────────
    sidecar = fixture_path.parent / (fixture_path.stem + ".expected.json")
    if not sidecar.exists():
        return

    expected = json.loads(sidecar.read_text())
    if "pointer" not in expected:
        return

    pointers = all_error_pointers(exc_info.value)
    assert expected["pointer"] in pointers, (
        f"Expected validation error at pointer {expected['pointer']!r} "
        f"but only found: {sorted(pointers)}\n"
        f"Top-level message: {exc_info.value.message}"
    )
