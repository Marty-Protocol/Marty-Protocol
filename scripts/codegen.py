#!/usr/bin/env python3
"""Generate typed language bindings from MIP JSON Schemas and Enums.

Reads all files in schemas/ and enums/, produces:
  - reference/python/mip_types/   — Pydantic v2 models + enum classes
  - reference/rust/src/           — Rust structs + enums (serde)
  - reference/typescript/src/     — TypeScript interfaces + enums

Usage:
  python scripts/codegen.py            # generate all
  python scripts/codegen.py python     # generate Python only
  python scripts/codegen.py rust       # generate Rust only
  python scripts/codegen.py typescript # generate TypeScript only
"""
from __future__ import annotations

import json
import re
import sys
import textwrap
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = REPO_ROOT / "schemas"
ENUMS_DIR = REPO_ROOT / "enums"

# Map from JSON filename (without .json) to the resolved type name.
# Built by build_ref_map() after loading enums + schemas.
REF_MAP: dict[str, str] = {}


# ─── Helpers ───────────────────────────────────────────────────────────────────


def build_ref_map(enums: list[dict], schemas: list[dict]) -> None:
    """Build a global map from JSON filenames to their resolved type names."""
    for item in enums + schemas:
        filename = item["_filename"]  # e.g. "approval-strategies"
        title = item.get("title", kebab_to_pascal(filename))
        resolved = sanitize_class_name(title)
        REF_MAP[filename] = resolved


def resolve_ref(ref_path: str) -> str:
    """Resolve a $ref path like '../enums/approval-strategies.json' to its type name."""
    filename = ref_path.split("/")[-1].replace(".json", "")
    if filename in REF_MAP:
        return REF_MAP[filename]
    return sanitize_class_name(kebab_to_pascal(filename))


# ─── Helpers ───────────────────────────────────────────────────────────────────


def load_all_enums() -> list[dict]:
    """Load all enum JSON files, sorted by filename."""
    enums = []
    for f in sorted(ENUMS_DIR.glob("*.json")):
        data = json.loads(f.read_text())
        data["_filename"] = f.stem  # e.g. "credential-formats"
        enums.append(data)
    return enums


def load_all_schemas() -> list[dict]:
    """Load all schema JSON files, sorted by filename."""
    schemas = []
    for f in sorted(SCHEMAS_DIR.glob("*.json")):
        data = json.loads(f.read_text())
        data["_filename"] = f.stem  # e.g. "trust-profile"
        schemas.append(data)
    return schemas


def sanitize_class_name(name: str) -> str:
    """Ensure a valid class/type name.

    If the name is already a valid PascalCase identifier (no spaces/special chars),
    return it as-is. Otherwise, clean it up.
    """
    # If it's already a valid identifier with no spaces, return as-is
    if re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
        return name
    # Remove anything that's not alphanumeric or underscore/space
    name = re.sub(r"[^a-zA-Z0-9_ ]", " ", name)
    # PascalCase from words
    name = "".join(word.capitalize() for word in name.split())
    # Ensure starts with uppercase letter
    if name and not name[0].isalpha():
        name = "X" + name
    return name


def kebab_to_snake(name: str) -> str:
    """credential-formats → credential_formats"""
    return name.replace("-", "_")


def kebab_to_pascal(name: str) -> str:
    """credential-formats → CredentialFormats"""
    return "".join(word.capitalize() for word in name.split("-"))


def kebab_to_camel(name: str) -> str:
    """credential-formats → credentialFormats"""
    pascal = kebab_to_pascal(name)
    return pascal[0].lower() + pascal[1:]


def snake_to_pascal(name: str) -> str:
    """credential_formats → CredentialFormats"""
    return "".join(word.capitalize() for word in name.split("_"))


def json_type_to_python(prop: dict, prop_name: str, required: bool) -> str:
    """Map a JSON Schema property to a Python type annotation."""
    ref = prop.get("$ref")
    if ref:
        return resolve_ref(ref)

    t = prop.get("type")
    fmt = prop.get("format")
    enum = prop.get("enum")

    if enum:
        # Inline literal union
        members = ", ".join(f'"{v}"' for v in enum)
        return f"Literal[{members}]"

    if isinstance(t, list):
        # e.g. ["string", "null"]
        non_null = [x for x in t if x != "null"]
        base = json_type_to_python({"type": non_null[0], "format": fmt, "items": prop.get("items")}, prop_name, True)
        return f"{base} | None"

    if t == "string":
        if fmt == "date-time":
            return "datetime"
        if fmt == "uuid":
            return "str"
        return "str"
    if t == "integer":
        return "int"
    if t == "number":
        return "float"
    if t == "boolean":
        return "bool"
    if t == "array":
        items = prop.get("items", {})
        if "$ref" in items:
            item_type = resolve_ref(items["$ref"])
        elif items.get("type") == "object":
            item_type = "dict[str, Any]"
        elif items.get("type") == "string":
            item_type = "str"
        elif items.get("type") == "integer":
            item_type = "int"
        else:
            item_type = "Any"
        return f"list[{item_type}]"
    if t == "object":
        return "dict[str, Any]"

    return "Any"


def json_type_to_rust(prop: dict, prop_name: str, required: bool) -> str:
    """Map a JSON Schema property to a Rust type."""
    ref = prop.get("$ref")
    if ref:
        return resolve_ref(ref)

    t = prop.get("type")
    fmt = prop.get("format")
    enum = prop.get("enum")

    if enum:
        return "String"  # inline enums become String in Rust

    is_nullable = False
    if isinstance(t, list):
        non_null = [x for x in t if x != "null"]
        if "null" in t:
            is_nullable = True
        t = non_null[0] if non_null else "string"

    base = "String"
    if t == "string":
        if fmt == "date-time":
            base = "String"  # chrono::DateTime<Utc> in real use, String for portability
        elif fmt == "uuid":
            base = "String"
        else:
            base = "String"
    elif t == "integer":
        base = "i64"
    elif t == "number":
        base = "f64"
    elif t == "boolean":
        base = "bool"
    elif t == "array":
        items = prop.get("items", {})
        if "$ref" in items:
            item_type = resolve_ref(items["$ref"])
        elif items.get("type") == "object":
            item_type = "serde_json::Value"
        elif items.get("type") == "string":
            item_type = "String"
        elif items.get("type") == "integer":
            item_type = "i64"
        else:
            item_type = "serde_json::Value"
        base = f"Vec<{item_type}>"
    elif t == "object":
        base = "serde_json::Value"

    if is_nullable:
        return f"Option<{base}>"
    return base


def json_type_to_ts(prop: dict, prop_name: str, required: bool) -> str:
    """Map a JSON Schema property to a TypeScript type."""
    ref = prop.get("$ref")
    if ref:
        return resolve_ref(ref)

    t = prop.get("type")
    fmt = prop.get("format")
    enum = prop.get("enum")

    if enum:
        return " | ".join(f"'{v}'" for v in enum)

    is_nullable = False
    if isinstance(t, list):
        non_null = [x for x in t if x != "null"]
        if "null" in t:
            is_nullable = True
        t = non_null[0] if non_null else "string"

    base = "string"
    if t == "string":
        base = "string"
    elif t == "integer" or t == "number":
        base = "number"
    elif t == "boolean":
        base = "boolean"
    elif t == "array":
        items = prop.get("items", {})
        if "$ref" in items:
            item_type = resolve_ref(items["$ref"])
        elif items.get("type") == "object":
            item_type = "Record<string, unknown>"
        elif items.get("type") == "string":
            item_type = "string"
        elif items.get("type") == "integer":
            item_type = "number"
        else:
            item_type = "unknown"
        base = f"{item_type}[]"
    elif t == "object":
        base = "Record<string, unknown>"

    if is_nullable:
        return f"{base} | null"
    return base


# ─── Python Generator ─────────────────────────────────────────────────────────


def generate_python(enums: list[dict], schemas: list[dict]) -> None:
    out_dir = REPO_ROOT / "reference" / "python" / "mip_types"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Generate enums module
    lines = [
        '"""MIP Protocol Enums — generated from marty-protocol/enums/*.json',
        f'Generated: {datetime.now().strftime("%Y-%m-%d")}',
        'DO NOT EDIT — regenerate with: python scripts/codegen.py python',
        '"""',
        "from enum import Enum",
        "",
    ]

    for e in enums:
        title = sanitize_class_name(e.get("title", kebab_to_pascal(e["_filename"])))
        desc = e.get("description", "")
        values = e.get("enum", [])
        if not values:
            continue

        lines.append("")
        lines.append(f"class {title}(str, Enum):")
        if desc:
            lines.append(f'    """{desc}"""')
        lines.append("")
        for v in values:
            safe_name = v.upper().replace("-", "_").replace(" ", "_").replace(":", "_").replace(".", "_")
            # Ensure valid Python identifier
            if safe_name[0].isdigit():
                safe_name = f"V_{safe_name}"
            lines.append(f'    {safe_name} = "{v}"')
        lines.append("")

    (out_dir / "enums.py").write_text("\n".join(lines) + "\n")

    # Generate models module
    lines = [
        '"""MIP Protocol Models — generated from marty-protocol/schemas/*.json',
        f'Generated: {datetime.now().strftime("%Y-%m-%d")}',
        'DO NOT EDIT — regenerate with: python scripts/codegen.py python',
        '"""',
        "from __future__ import annotations",
        "",
        "from datetime import datetime",
        "from typing import Any, Literal",
        "",
        "from pydantic import BaseModel, Field",
        "",
        "from .enums import (",
    ]
    # Import all enum classes
    for e in enums:
        title = sanitize_class_name(e.get("title", kebab_to_pascal(e["_filename"])))
        if e.get("enum"):
            lines.append(f"    {title},")
    lines.append(")")
    lines.append("")

    for schema in schemas:
        title = sanitize_class_name(schema.get("title", kebab_to_pascal(schema["_filename"])))
        desc = schema.get("description", "")
        required_fields = set(schema.get("required", []))
        props = schema.get("properties", {})
        if not props:
            continue

        lines.append("")
        lines.append(f"class {title}(BaseModel):")
        if desc:
            wrapped = textwrap.fill(desc, width=88)
            lines.append(f'    """{wrapped}"""')
        lines.append("")

        for prop_name, prop_def in props.items():
            is_required = prop_name in required_fields
            py_type = json_type_to_python(prop_def, prop_name, is_required)

            if not is_required:
                if "| None" not in py_type:
                    py_type = f"{py_type} | None"
                lines.append(f"    {prop_name}: {py_type} = None")
            else:
                lines.append(f"    {prop_name}: {py_type}")

        lines.append("")

    # Add model_rebuild() calls for models with forward references.
    # With `from __future__ import annotations`, Pydantic defers type
    # resolution, so any model that references another model defined later
    # needs a rebuild() call after all classes are defined.
    model_names = []
    for schema in schemas:
        title = sanitize_class_name(schema.get("title", kebab_to_pascal(schema["_filename"])))
        if schema.get("properties"):
            model_names.append(title)

    if model_names:
        lines.append("")
        lines.append("# Rebuild models with forward references")
        for name in model_names:
            lines.append(f"{name}.model_rebuild()")

    (out_dir / "models.py").write_text("\n".join(lines) + "\n")

    # Generate __init__.py
    init_lines = [
        '"""MIP Protocol Types — generated from marty-protocol JSON Schemas."""',
        "from .enums import *  # noqa: F401,F403",
        "from .models import *  # noqa: F401,F403",
        "",
    ]
    (out_dir / "__init__.py").write_text("\n".join(init_lines))

    # Generate py.typed marker
    (out_dir / "py.typed").write_text("")

    print(f"  Python: {out_dir}")


# ─── Rust Generator ───────────────────────────────────────────────────────────


def generate_rust(enums: list[dict], schemas: list[dict]) -> None:
    out_dir = REPO_ROOT / "reference" / "rust" / "src"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Generate enums
    lines = [
        "//! MIP Protocol Enums — generated from marty-protocol/enums/*.json",
        f"//! Generated: {datetime.now().strftime('%Y-%m-%d')}",
        "//! DO NOT EDIT — regenerate with: python scripts/codegen.py rust",
        "",
        "use serde::{Deserialize, Serialize};",
        "",
    ]

    for e in enums:
        title = sanitize_class_name(e.get("title", kebab_to_pascal(e["_filename"])))
        desc = e.get("description", "")
        values = e.get("enum", [])
        if not values:
            continue

        if desc:
            lines.append(f"/// {desc}")
        lines.append("#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]")
        lines.append(f"pub enum {title} {{")
        for v in values:
            # Create Rust variant name: PascalCase from the value
            # Split on any non-alphanumeric character (handles _, -, :, ., etc.)
            parts = re.split(r'[^a-zA-Z0-9]+', v)
            variant = "".join(word.capitalize() for word in parts if word)
            if not variant:
                variant = f"Value{values.index(v)}"
            lines.append(f'    #[serde(rename = "{v}")]')
            lines.append(f"    {variant},")
        lines.append("}")
        lines.append("")

    (out_dir / "enums.rs").write_text("\n".join(lines) + "\n")

    # Generate models
    lines = [
        "//! MIP Protocol Models — generated from marty-protocol/schemas/*.json",
        f"//! Generated: {datetime.now().strftime('%Y-%m-%d')}",
        "//! DO NOT EDIT — regenerate with: python scripts/codegen.py rust",
        "",
        "use serde::{Deserialize, Serialize};",
        "",
        "use crate::enums::*;",
        "",
    ]

    for schema in schemas:
        title = sanitize_class_name(schema.get("title", kebab_to_pascal(schema["_filename"])))
        desc = schema.get("description", "")
        required_fields = set(schema.get("required", []))
        props = schema.get("properties", {})
        if not props:
            continue

        if desc:
            for line in textwrap.wrap(desc, width=88):
                lines.append(f"/// {line}")
        lines.append("#[derive(Debug, Clone, Serialize, Deserialize)]")
        lines.append(f"pub struct {title} {{")

        for prop_name, prop_def in props.items():
            is_required = prop_name in required_fields
            rust_type = json_type_to_rust(prop_def, prop_name, is_required)

            # Rename field if it's a Rust keyword
            rename = ""
            field_name = prop_name
            if prop_name in ("type", "ref", "self", "move", "match"):
                rename = f'    #[serde(rename = "{prop_name}")]\n'
                field_name = f"r#{prop_name}"

            if not is_required:
                if not rust_type.startswith("Option<"):
                    rust_type = f"Option<{rust_type}>"
                lines.append(f"    #[serde(skip_serializing_if = \"Option::is_none\")]")
            if rename:
                lines.append(rename.rstrip())
            lines.append(f"    pub {field_name}: {rust_type},")

        lines.append("}")
        lines.append("")

    (out_dir / "models.rs").write_text("\n".join(lines) + "\n")

    # Generate lib.rs
    lib_lines = [
        "//! MIP Protocol Types — generated from marty-protocol JSON Schemas.",
        "",
        "pub mod enums;",
        "pub mod models;",
        "",
    ]
    (out_dir / "lib.rs").write_text("\n".join(lib_lines))

    # Generate Cargo.toml
    cargo = textwrap.dedent("""\
        [package]
        name = "mip-protocol-types"
        version = "0.1.0"
        edition = "2021"
        description = "Generated Rust types for the Marty Identity Protocol"
        license = "Apache-2.0"

        [dependencies]
        serde = { version = "1", features = ["derive"] }
        serde_json = "1"
    """)
    (out_dir.parent / "Cargo.toml").write_text(cargo)

    print(f"  Rust: {out_dir}")


# ─── TypeScript Generator ─────────────────────────────────────────────────────


def generate_typescript(enums: list[dict], schemas: list[dict]) -> None:
    out_dir = REPO_ROOT / "reference" / "typescript" / "src"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Generate enums
    lines = [
        "// MIP Protocol Enums — generated from marty-protocol/enums/*.json",
        f"// Generated: {datetime.now().strftime('%Y-%m-%d')}",
        "// DO NOT EDIT — regenerate with: python scripts/codegen.py typescript",
        "",
    ]

    for e in enums:
        title = sanitize_class_name(e.get("title", kebab_to_pascal(e["_filename"])))
        desc = e.get("description", "")
        values = e.get("enum", [])
        if not values:
            continue

        if desc:
            lines.append(f"/** {desc} */")
        lines.append(f"export enum {title} {{")
        for v in values:
            safe_name = re.sub(r'[^a-zA-Z0-9]+', '_', v).upper()
            if safe_name[0].isdigit():
                safe_name = f"V_{safe_name}"
            lines.append(f"  {safe_name} = '{v}',")
        lines.append("}")
        lines.append("")

    (out_dir / "enums.ts").write_text("\n".join(lines) + "\n")

    # Generate models
    lines = [
        "// MIP Protocol Models — generated from marty-protocol/schemas/*.json",
        f"// Generated: {datetime.now().strftime('%Y-%m-%d')}",
        "// DO NOT EDIT — regenerate with: python scripts/codegen.py typescript",
        "",
        "import {",
    ]
    # Import all enum types
    enum_names = []
    for e in enums:
        title = sanitize_class_name(e.get("title", kebab_to_pascal(e["_filename"])))
        if e.get("enum"):
            enum_names.append(title)
    for name in enum_names:
        lines.append(f"  {name},")
    lines.append("} from './enums';")
    lines.append("")

    for schema in schemas:
        title = sanitize_class_name(schema.get("title", kebab_to_pascal(schema["_filename"])))
        desc = schema.get("description", "")
        required_fields = set(schema.get("required", []))
        props = schema.get("properties", {})
        if not props:
            continue

        if desc:
            lines.append(f"/** {desc} */")
        lines.append(f"export interface {title} {{")

        for prop_name, prop_def in props.items():
            is_required = prop_name in required_fields
            ts_type = json_type_to_ts(prop_def, prop_name, is_required)

            optional = "" if is_required else "?"
            lines.append(f"  {prop_name}{optional}: {ts_type};")

        lines.append("}")
        lines.append("")

    (out_dir / "models.ts").write_text("\n".join(lines) + "\n")

    # Generate index.ts
    index_lines = [
        "// MIP Protocol Types — generated from marty-protocol JSON Schemas.",
        "export * from './enums';",
        "export * from './models';",
        "",
    ]
    (out_dir / "index.ts").write_text("\n".join(index_lines))

    # Generate package.json
    pkg = {
        "name": "@mip-protocol/types",
        "version": "0.1.0",
        "description": "Generated TypeScript types for the Marty Identity Protocol",
        "main": "dist/index.js",
        "types": "dist/index.d.ts",
        "license": "Apache-2.0",
        "scripts": {
            "build": "tsc",
            "prepublishOnly": "npm run build"
        },
        "devDependencies": {
            "typescript": "^5.0.0"
        }
    }
    (out_dir.parent / "package.json").write_text(json.dumps(pkg, indent=2) + "\n")

    # Generate tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "declaration": True,
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": True,
            "esModuleInterop": True,
            "moduleResolution": "node"
        },
        "include": ["src/**/*"]
    }
    (out_dir.parent / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2) + "\n")

    print(f"  TypeScript: {out_dir}")


# ─── Main ─────────────────────────────────────────────────────────────────────


def main():
    targets = set(sys.argv[1:]) if len(sys.argv) > 1 else {"python", "rust", "typescript"}

    enums = load_all_enums()
    schemas = load_all_schemas()
    build_ref_map(enums, schemas)

    print(f"Loaded {len(enums)} enums, {len(schemas)} schemas")
    print()

    if "python" in targets:
        print("Generating Python types...")
        generate_python(enums, schemas)
    if "rust" in targets:
        print("Generating Rust types...")
        generate_rust(enums, schemas)
    if "typescript" in targets:
        print("Generating TypeScript types...")
        generate_typescript(enums, schemas)

    print()
    print("Done. Generated types are in reference/{python,rust,typescript}/")


if __name__ == "__main__":
    main()
