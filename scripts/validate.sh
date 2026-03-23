#!/usr/bin/env bash
# validate.sh — Validate MIP JSON entity files against their schemas
#
# Usage:
#   ./scripts/validate.sh                                    # validate all examples/ against schemas/
#   ./scripts/validate.sh --data FILE --schema SCHEMA_FILE   # validate a single file
#   ./scripts/validate.sh --data-dir DIR --schema SCHEMA_FILE # validate all JSON files in a dir
#
# Dependencies:
#   - ajv-cli (npm install -g ajv-cli) OR
#   - check-jsonschema (pip install check-jsonschema)
#
# The script auto-detects which validator is available.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SCHEMA_DIR="${REPO_ROOT}/schemas"
EXAMPLES_DIR="${REPO_ROOT}/examples"

ERRORS=0
CHECKED=0

# ─── Validator detection ───────────────────────────────────────────────────────

if command -v ajv &>/dev/null; then
  VALIDATOR="ajv"
elif command -v check-jsonschema &>/dev/null; then
  VALIDATOR="check-jsonschema"
else
  echo "ERROR: No JSON Schema validator found."
  echo "Install one of:"
  echo "  npm install -g ajv-cli ajv-formats"
  echo "  pip install check-jsonschema"
  exit 1
fi

# ─── Validation function ───────────────────────────────────────────────────────

validate_file() {
  local data_file="$1"
  local schema_file="$2"

  if [[ ! -f "$data_file" ]]; then
    echo "ERROR: Data file not found: $data_file"
    return 1
  fi
  if [[ ! -f "$schema_file" ]]; then
    echo "SKIP: Schema not found (${schema_file}), skipping ${data_file}"
    return 0
  fi

  CHECKED=$((CHECKED + 1))

  if [[ "$VALIDATOR" == "ajv" ]]; then
    if ajv validate -s "$schema_file" -d "$data_file" --spec=draft2020 2>/dev/null; then
      echo "  OK  ${data_file#"$REPO_ROOT/"}"
    else
      echo "FAIL  ${data_file#"$REPO_ROOT/"}"
      ERRORS=$((ERRORS + 1))
    fi
  else
    # check-jsonschema
    if check-jsonschema --schemafile "$schema_file" "$data_file" 2>/dev/null; then
      echo "  OK  ${data_file#"$REPO_ROOT/"}"
    else
      echo "FAIL  ${data_file#"$REPO_ROOT/"}"
      ERRORS=$((ERRORS + 1))
    fi
  fi
}

# ─── Schema name inference ─────────────────────────────────────────────────────

# Infer schema filename from data filename (strip path, strip .json, look up)
infer_schema() {
  local data_file="$1"
  local basename
  basename="$(basename "$data_file")"

  # Direct match: trust-profile.json → schemas/trust-profile.json
  local candidate="${SCHEMA_DIR}/${basename}"
  if [[ -f "$candidate" ]]; then
    echo "$candidate"
    return 0
  fi

  # Wallet profile query files use wallet-profile schema
  if [[ "$basename" == "wallet-profile-query.json" ]]; then
    echo "${SCHEMA_DIR}/wallet-profile.json"
    return 0
  fi

  echo ""
}

# ─── Argument parsing ──────────────────────────────────────────────────────────

DATA_FILE=""
SCHEMA_FILE=""
DATA_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --data)
      DATA_FILE="$2"; shift 2 ;;
    --schema)
      SCHEMA_FILE="$2"; shift 2 ;;
    --data-dir)
      DATA_DIR="$2"; shift 2 ;;
    --schema-dir)
      SCHEMA_DIR="$2"; shift 2 ;;
    -h|--help)
      sed -n '2,12p' "$0" | sed 's/^# //'
      exit 0 ;;
    *)
      echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# ─── Execute ───────────────────────────────────────────────────────────────────

echo "MIP Schema Validator — using ${VALIDATOR}"
echo "Schema directory: ${SCHEMA_DIR}"
echo ""

if [[ -n "$DATA_FILE" && -n "$SCHEMA_FILE" ]]; then
  # Single file mode
  validate_file "$DATA_FILE" "$SCHEMA_FILE"

elif [[ -n "$DATA_DIR" && -n "$SCHEMA_FILE" ]]; then
  # Directory against single schema
  while IFS= read -r -d '' f; do
    validate_file "$f" "$SCHEMA_FILE"
  done < <(find "$DATA_DIR" -name "*.json" -not -name "*.expected.json" -print0)

else
  # Default: validate all example files
  echo "Validating examples/..."
  while IFS= read -r -d '' f; do
    schema="$(infer_schema "$f")"
    if [[ -n "$schema" ]]; then
      validate_file "$f" "$schema"
    else
      echo "SKIP  ${f#"$REPO_ROOT/"} (no schema mapping)"
    fi
  done < <(find "$EXAMPLES_DIR" -name "*.json" -not -name "*.expected.json" -print0 | sort -z)
fi

echo ""
echo "─────────────────────────────────────────────────"
echo "Checked: ${CHECKED} | Errors: ${ERRORS}"

if [[ $ERRORS -gt 0 ]]; then
  echo "FAIL — ${ERRORS} validation error(s)"
  exit 1
else
  echo "PASS — all files valid"
  exit 0
fi
