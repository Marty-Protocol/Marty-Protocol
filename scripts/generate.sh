#!/usr/bin/env bash
# Generate typed language bindings from MIP JSON Schemas.
# Usage:
#   ./scripts/generate.sh            # all languages
#   ./scripts/generate.sh python     # Python only
#   ./scripts/generate.sh rust       # Rust only
#   ./scripts/generate.sh typescript # TypeScript only
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$REPO_ROOT"

echo "=== MIP Protocol Type Generator ==="
echo ""

python3 scripts/codegen.py "$@"

# Validate generated artifacts
echo ""
echo "Validating generated artifacts..."

if [[ -z "${1:-}" || "$1" == "python" ]]; then
    if python3 -c "import ast; ast.parse(open('reference/python/mip_types/enums.py').read()); ast.parse(open('reference/python/mip_types/models.py').read())" 2>/dev/null; then
        echo "  Python: syntax OK"
    else
        echo "  Python: SYNTAX ERROR" >&2
        exit 1
    fi
fi

if [[ -z "${1:-}" || "$1" == "typescript" ]]; then
    if [[ -f "reference/typescript/src/enums.ts" && -f "reference/typescript/src/models.ts" ]]; then
        echo "  TypeScript: files generated OK"
    else
        echo "  TypeScript: MISSING FILES" >&2
        exit 1
    fi
fi

if [[ -z "${1:-}" || "$1" == "rust" ]]; then
    if [[ -f "reference/rust/src/enums.rs" && -f "reference/rust/src/models.rs" && -f "reference/rust/Cargo.toml" ]]; then
        echo "  Rust: files generated OK"
    else
        echo "  Rust: MISSING FILES" >&2
        exit 1
    fi
fi

echo ""
echo "All done."
