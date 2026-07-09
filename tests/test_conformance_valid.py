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


@pytest.mark.parametrize(
    "fixture_path",
    [f for f in _fixtures if infer_schema(f) and infer_schema(f).name == "policy-set.json"],
    ids=[f.stem for f in _fixtures if infer_schema(f) and infer_schema(f).name == "policy-set.json"],
)
def test_policy_set_fixture_embedded_cedar_validates(fixture_path: pathlib.Path) -> None:
    cedarpy = pytest.importorskip("cedarpy")

    instance = json.loads(fixture_path.read_text())
    schema = (REPO_ROOT / "cedar" / "mip.cedarschema").read_text()
    for policy in instance.get("cedar_policies", []):
        cedar_text = str(policy.get("cedar_text") or "")
        result = cedarpy.validate_policies(cedar_text, schema)
        errors = [str(error) for error in (getattr(result, "errors", []) or [])]
        assert errors == []
