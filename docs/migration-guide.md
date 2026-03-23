# MIP Migration Guide

This guide covers migration paths for upgrading between MIP specification versions. It documents breaking changes, deprecations, and recommended migration steps.

---

## How to Read This Guide

Each migration section covers a **from → to** version pair. Follow the steps in order. Test against the conformance suite after each step.

```sh
./scripts/run-conformance.sh --endpoint https://your-instance.example.com
```

---

## 0.1.0-draft → 0.1.0

This section will be populated when the 0.1.0 final specification is ratified.

No breaking changes are expected between 0.1.0-draft and 0.1.0. The draft-to-final transition is expected to include:

- Finalized `$id` URLs in JSON Schemas (currently using `https://raw.githubusercontent.com/did-report/marty-protocol/main/schemas/`)
- Any field renames or type changes identified during implementation review
- Conformance test additions

---

## Cedar Policy Migration

This section covers migrating from legacy opaque JSON rule objects to Cedar PolicySets. This migration is backward-compatible — legacy fields are deprecated but still accepted.

### Step 1: Create Policy Sets

For each entity that previously used opaque JSON rule objects, create a corresponding Cedar PolicySet:

| Legacy Field | Entity | New Field | PolicySet Type |
|---|---|---|---|
| `approval_rules` | Application Template | `approval_policy_set_id` | `APPROVAL_RULES` |
| `default_verification_rules` | Compliance Profile | `verification_policy_set_id` | `CREDENTIAL_VERIFICATION` |
| Inline permission checks | SCIM Role | `policy_set_id` | `ACCESS_CONTROL` |

### Step 2: Write Cedar Policies

Author Cedar policies that replicate your existing rule logic. Reference policies are available in `cedar/policies/` for the three standard domains. See `docs/cedar-policies.md` for authoring guidance.

### Step 3: Validate Against Schema

Use the `/v1/policy-sets/{id}/validate` endpoint or the MIP Cedar schema (`cedar/mip.cedarschema`) to validate your policies before activation:

```sh
./scripts/validate.sh --schema schemas/policy-set.json --data your-policy-set.json
```

### Step 4: Link PolicySets

Update entities to reference their PolicySet:

```json
{
  "approval_policy_set_id": "<policy-set-uuid>",
  "approval_strategy": "RULES_BASED"
}
```

When both legacy fields and Cedar PolicySet references are present, the Cedar PolicySet takes precedence.

### Step 5: Remove Legacy Fields

Once all consumers have migrated, remove the deprecated fields (`approval_rules`, `default_verification_rules`). These fields will be removed in a future MINOR or MAJOR version after the deprecation window.

---

## Future Migration Notes

### When MINOR versions are published

MINOR version increments (e.g., 0.1.x → 0.2.0) may add new:
- Protocol entities
- Optional fields on existing entities
- Enum values in existing vocabularies

These are backwards-compatible. Existing payloads continue to validate. New optional fields have sensible defaults if absent.

**Action required:** Update `$schema` references if you hard-pin schema versions.

### When MAJOR versions are published (post 1.0)

Major version increments (e.g., 1.x → 2.0) are reserved for breaking changes to normative requirements. These will include:

- Explicit migration paths for each breaking change
- Minimum 90-day deprecation notice before stable adoption
- Migration tooling in `scripts/`

---

## Deprecation Policy

When a field, entity, or behavior is deprecated:

1. It is marked as `deprecated` in the JSON Schema with a `$comment` explaining the replacement
2. A deprecation notice appears in `CHANGELOG.md`
3. The field/behavior is OPTIONAL (not REQUIRED) during the deprecation window
4. After the deprecation window expires, the field is removed in the next MINOR or MAJOR version

Deprecated features are indicated in this guide with a ⚠️ symbol.

---

## Tooling

Run schema validation for a full directory of entity files:

```sh
# Validate all JSON files in a directory against their schemas
./scripts/validate.sh --schema-dir schemas/ --data-dir examples/realistic/pre-boarding-clearance/

# Validate a single file
./scripts/validate.sh --schema schemas/credential-template.json --data examples/minimal/credential-template.json

# Run full conformance suite (valid + invalid fixtures)
./scripts/run-conformance.sh
```
