"""Resolve beta candidate schemas independently of active 0.5.0 schemas."""

import json
from pathlib import Path

from jsonschema import FormatChecker
from jsonschema.validators import validator_for
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

REPO_ROOT = Path(__file__).resolve().parents[1]
ACTIVE_ROOT = REPO_ROOT.parents[2]


def _registry(roots: tuple[Path, ...]) -> Registry:
    resources = {}
    for root in roots:
        for directory in ("schemas", "enums"):
            for path in sorted((root / directory).glob("*.json")):
                schema = json.loads(path.read_text(encoding="utf-8"))
                uri = schema.get("$id")
                if uri:
                    if uri in resources:
                        raise ValueError(f"duplicate schema ID: {uri}")
                    resources[uri] = Resource.from_contents(schema, default_specification=DRAFT202012)
    return Registry().with_resources(resources.items())


REGISTRY = _registry((ACTIVE_ROOT, REPO_ROOT))
CANDIDATE_REGISTRY = _registry((REPO_ROOT,))


def validate_instance(schema_path: Path, instance: object, *, candidate_only: bool = False) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    registry = CANDIDATE_REGISTRY if candidate_only else REGISTRY
    validator_for(schema)(schema, registry=registry, format_checker=FormatChecker()).validate(instance)


def infer_schema(fixture_path: Path) -> Path | None:
    name = fixture_path.stem
    while name:
        for root in (REPO_ROOT, ACTIVE_ROOT):
            path = root / "schemas" / f"{name}.json"
            if path.exists():
                return path
        if "-" not in name:
            break
        name = name.rsplit("-", 1)[0]
    return None
