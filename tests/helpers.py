"""Shared utilities for marty-protocol pytest suite.

Provides:
  REPO_ROOT      — absolute path to the repository root
  SCHEMAS_DIR    — path to schemas/
  REGISTRY       — jsonschema referencing.Registry built from all local schemas + enums
  infer_schema() — map a fixture path to its corresponding schema file
  validate_instance() — run Draft 2020-12 validation via the local registry
  all_error_pointers() — flatten a ValidationError tree into a set of JSON Pointers
"""

import json
import pathlib
import re

import referencing
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
from jsonschema.validators import validator_for
from jsonschema import ValidationError

REPO_ROOT = pathlib.Path(__file__).parent.parent
SCHEMAS_DIR = REPO_ROOT / "schemas"
ENUMS_DIR = REPO_ROOT / "enums"

# Base URI used by the protocol schemas' $id fields.
_BASE_URI = "https://raw.githubusercontent.com/did-report/marty-protocol/main/"


def _build_registry() -> Registry:
    """Load all schemas and enums into a referencing.Registry for local $ref resolution."""
    resources: list[tuple[str, Resource]] = []
    for search_dir, url_segment in [
        (SCHEMAS_DIR, "schemas"),
        (ENUMS_DIR, "enums"),
    ]:
        for json_file in sorted(search_dir.glob("*.json")):
            contents = json.loads(json_file.read_text())
            # Prefer the schema's own $id; fall back to a deterministic file URI.
            uri = contents.get("$id") or f"{_BASE_URI}{url_segment}/{json_file.name}"
            resources.append(
                (uri, Resource.from_contents(contents, default_specification=DRAFT202012))
            )
    return Registry().with_resources(resources)


REGISTRY = _build_registry()


def infer_schema(fixture_path: pathlib.Path) -> pathlib.Path | None:
    """Infer the schema file for *fixture_path* by progressively stripping trailing dash-segments.

    Examples
    --------
    trust-profile-bad-algorithm.json → trust-profile.json
    deployment-profile-empty-policies.json → deployment-profile.json
    wallet-profile-query.json → wallet-profile.json
    """
    name = fixture_path.stem
    while name:
        candidate = SCHEMAS_DIR / f"{name}.json"
        if candidate.exists():
            return candidate
        if "-" not in name:
            break
        name = name.rsplit("-", 1)[0]
    return None


def validate_instance(schema_path: pathlib.Path, instance: object) -> None:
    """Validate *instance* against the schema at *schema_path*.

    Uses the module-level REGISTRY so that all local ``$ref`` values resolve
    correctly against the raw.githubusercontent.com/did-report/marty-protocol namespace.

    Raises ``jsonschema.ValidationError`` on failure.
    """
    schema = json.loads(schema_path.read_text())
    cls = validator_for(schema)
    validator = cls(schema, registry=REGISTRY)
    validator.validate(instance)


_REQUIRED_RE = re.compile(r"'(.+?)' is a required property")


def all_error_pointers(exc: ValidationError) -> set[str]:
    """Recursively collect every JSON Pointer path present in a ValidationError tree.

    For ``required``-property errors the missing property is appended to the
    parent path, so ``public_key_kid`` missing at root produces ``/public_key_kid``.
    """
    pointers: set[str] = set()

    def _walk(e: ValidationError) -> None:
        if e.absolute_path:
            pointers.add("/" + "/".join(str(p) for p in e.absolute_path))
        if e.validator == "required":
            m = _REQUIRED_RE.match(e.message)
            if m:
                parent = ("/" + "/".join(str(p) for p in e.absolute_path)) if e.absolute_path else ""
                pointers.add(parent + "/" + m.group(1))
        for sub in e.context:
            _walk(sub)

    _walk(exc)
    return pointers
