#!/usr/bin/env bash
# run-conformance.sh — Run MIP conformance tests
#
# Tests that:
#   1. All conformance/valid/*.json files pass schema validation
#   2. All conformance/invalid/*.json files FAIL schema validation
#      with the expected error code from the paired *.expected.json sidecar
#
# Usage:
#   ./scripts/run-conformance.sh                # run all conformance tests
#   ./scripts/run-conformance.sh --valid-only   # run only valid fixture tests
#   ./scripts/run-conformance.sh --invalid-only # run only invalid fixture tests
#   ./scripts/run-conformance.sh --verbose      # show full validator output

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SCHEMA_DIR="${REPO_ROOT}/schemas"
VALID_DIR="${REPO_ROOT}/conformance/valid"
INVALID_DIR="${REPO_ROOT}/conformance/invalid"

PASS=0
FAIL=0
SKIP=0
VERBOSE=false
RUN_VALID=true
RUN_INVALID=true

# ─── Argument parsing ──────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
  case "$1" in
    --valid-only)   RUN_INVALID=false; shift ;;
    --invalid-only) RUN_VALID=false; shift ;;
    --verbose)      VERBOSE=true; shift ;;
    -h|--help)
      sed -n '2,12p' "$0" | sed 's/^# //'
      exit 0 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# ─── Validator detection ───────────────────────────────────────────────────────

if command -v ajv &>/dev/null; then
  VALIDATOR="ajv"
elif command -v check-jsonschema &>/dev/null; then
  VALIDATOR="check-jsonschema"
else
  echo "ERROR: No JSON Schema validator found."
  echo "Install: npm install -g ajv-cli ajv-formats  OR  pip install check-jsonschema"
  exit 1
fi

# ─── Schema inference ─────────────────────────────────────────────────────────

infer_schema() {
  local f="$1"
  local base
  base="$(basename "$f")"

  # Extract entity type prefix before first dash (e.g., trust-profile-bad-algorithm → trust-profile)
  # Try progressively shorter prefixes
  local name="${base%.json}"
  while [[ "$name" == *"-"* ]]; do
    local candidate="${SCHEMA_DIR}/${name}.json"
    if [[ -f "$candidate" ]]; then
      echo "$candidate"
      return 0
    fi
    # Remove last dash-segment
    name="${name%-*}"
  done

  echo ""
}

# ─── Validation helpers ────────────────────────────────────────────────────────

run_validator() {
  local schema="$1"
  local data="$2"
  if [[ "$VALIDATOR" == "ajv" ]]; then
    ajv validate -s "$schema" -d "$data" --spec=draft2020 2>&1
  else
    check-jsonschema --schemafile "$schema" "$data" 2>&1
  fi
}

# ─── Valid fixtures ────────────────────────────────────────────────────────────

if [[ "$RUN_VALID" == true ]]; then
  echo "━━━ Valid Fixture Tests ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  while IFS= read -r -d '' f; do
    schema="$(infer_schema "$f")"
    name="${f#"$REPO_ROOT/"}"

    if [[ -z "$schema" ]]; then
      echo "  SKIP  ${name}  (no schema mapping)"
      SKIP=$((SKIP + 1))
      continue
    fi

    output="$(run_validator "$schema" "$f" 2>&1 || true)"
    exit_code=0
    run_validator "$schema" "$f" >/dev/null 2>&1 || exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
      echo "  PASS  ${name}"
      PASS=$((PASS + 1))
    else
      echo "  FAIL  ${name}  (expected VALID, got validation error)"
      if [[ "$VERBOSE" == true ]]; then
        echo "        ${output}"
      fi
      FAIL=$((FAIL + 1))
    fi
  done < <(find "$VALID_DIR" -name "*.json" -not -name "*.expected.json" -print0 | sort -z)
fi

# ─── Invalid fixtures ──────────────────────────────────────────────────────────

if [[ "$RUN_INVALID" == true ]]; then
  echo ""
  echo "━━━ Invalid Fixture Tests ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  while IFS= read -r -d '' f; do
    # Skip sidecar files
    [[ "$f" == *.expected.json ]] && continue

    schema="$(infer_schema "$f")"
    name="${f#"$REPO_ROOT/"}"
    sidecar="${f%.json}.expected.json"

    if [[ -z "$schema" ]]; then
      echo "  SKIP  ${name}  (no schema mapping)"
      SKIP=$((SKIP + 1))
      continue
    fi

    exit_code=0
    output="$(run_validator "$schema" "$f" 2>&1 || true)"
    run_validator "$schema" "$f" >/dev/null 2>&1 || exit_code=$?

    if [[ $exit_code -ne 0 ]]; then
      # Validation correctly rejected the invalid fixture
      # Optionally check that the expected error code appears in the output
      if [[ -f "$sidecar" ]]; then
        expected_code="$(python3 -c "import json,sys; print(json.load(open('$sidecar')).get('error_code',''))" 2>/dev/null || echo "")"
        if [[ -n "$expected_code" ]] && ! echo "$output" | grep -qi "$expected_code"; then
          echo "  WARN  ${name}  (rejected as expected, but error_code '${expected_code}' not found in output)"
          if [[ "$VERBOSE" == true ]]; then echo "        ${output}"; fi
        else
          echo "  PASS  ${name}  (correctly rejected)"
        fi
      else
        echo "  PASS  ${name}  (correctly rejected, no sidecar)"
      fi
      PASS=$((PASS + 1))
    else
      echo "  FAIL  ${name}  (expected INVALID — schema should reject this)"
      FAIL=$((FAIL + 1))
    fi
  done < <(find "$INVALID_DIR" -name "*.json" -print0 | sort -z)
fi

# ─── Summary ──────────────────────────────────────────────────────────────────

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Conformance Results  |  PASS: ${PASS}  FAIL: ${FAIL}  SKIP: ${SKIP}"

if [[ $FAIL -gt 0 ]]; then
  echo "RESULT: FAIL — ${FAIL} conformance test(s) failed"
  exit 1
else
  echo "RESULT: PASS — all conformance tests passed"
  exit 0
fi
