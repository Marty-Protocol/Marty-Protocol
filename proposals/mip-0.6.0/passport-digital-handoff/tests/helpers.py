"""Validate proposed schemas with active 0.5.0 references as read-only fallbacks."""

import json
from pathlib import Path

from jsonschema import FormatChecker
from jsonschema.validators import validator_for
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

REPO_ROOT = Path(__file__).resolve().parents[1]
ACTIVE_ROOT = REPO_ROOT.parents[2]


def _registry() -> Registry:
    resources = {}
    for root in (ACTIVE_ROOT, REPO_ROOT):
        for directory in ("schemas", "enums"):
            for path in sorted((root / directory).glob("*.json")):
                schema = json.loads(path.read_text(encoding="utf-8"))
                uri = schema.get("$id")
                if uri:
                    resources[uri] = Resource.from_contents(schema, default_specification=DRAFT202012)
    return Registry().with_resources(resources.items())


REGISTRY = _registry()


def validate_instance(schema_path: Path, instance: object) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator_for(schema)(schema, registry=REGISTRY, format_checker=FormatChecker()).validate(instance)


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
