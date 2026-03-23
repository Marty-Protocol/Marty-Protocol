# Presentation Policy — Entity Specification

**Entity:** Presentation Policy
**Version:** 0.1.0
**Stability:** Dynamic
**Section in root spec:** §7

---

## Purpose

A Presentation Policy defines **what must be presented** to satisfy a verifier. It encodes the minimum disclosure required, optional zero-knowledge predicate configurations, holder-binding requirements, and credential freshness constraints.

Presentation Policies change when business rules change — they are the most frequently updated protocol entity.

## What It Contains

| Dimension | Description |
|-----------|-------------|
| Required Claims | Which claims must be present |
| ZK Predicates | Boolean proofs over claims without revealing raw values |
| Holder Binding | Whether device-bound or nonce proof-of-possession is required |
| Freshness | How recent the credential or its revocation check must be |
| Issuer Constraints | Which issuers are accepted (via Trust Profile reference) |

## Properties

### Core Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `id` | UUID | Yes | Unique |
| `organization_id` | UUID | Yes | Must reference existing organization |
| `name` | string | Yes | 1–128 characters |
| `description` | string | No | Max 1024 characters |
| `required_claims` | RequiredClaim[] | Yes | At least one entry |
| `accepted_credential_types` | string[] | No | If empty, all types accepted |
| `trust_profile_id` | UUID | No | Issuer trust constraints |
| `holder_binding` | HolderBinding | No | See below |
| `freshness` | FreshnessConfig | No | See below |
| `prefer_predicates` | boolean | No | Default false |
| `supported_circuits` | string[] | No | ZK circuit identifiers |
| `fallback_policy` | FallbackPolicy | No | Default `ACCEPT_RAW` |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

### RequiredClaim Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `claim_name` | string | Yes | snake_case claim name |
| `credential_type` | string | No | Restrict to specific credential type |
| `value_constraint` | any | No | Exact value match |
| `predicate_spec` | PredicateSpec | No | ZK predicate configuration |

### PredicateSpec Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `predicate_type` | PredicateType | Yes | From `predicate-types` enum |
| `params` | object | Yes | Type-specific; see matrix below |
| `supported_circuits` | string[] | No | Overrides policy-level circuits |
| `fallback_policy` | FallbackPolicy | No | Overrides policy-level fallback |

**RANGE_PROOF params:**
```json
{"threshold": 21, "comparison": "gte"}
// OR
{"min": 18, "max": 65}
```

**MEMBERSHIP params:**
```json
{"allowed_values": ["US", "CA", "MX"]}
```

**EQUALITY params:**
```json
{"target_value": true}
```

**NON_MEMBERSHIP params:**
```json
{"excluded_values": ["REVOKED", "SUSPENDED"]}
```

**INEQUALITY params:**
```json
{"target_value": null}
```

### HolderBinding Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `required` | boolean | Yes | |
| `binding_methods` | string[] | No | `NONCE`, `DEVICE_KEY`, `SESSION_BINDING` |
| `nonce_required` | boolean | No | Default false |

### FreshnessConfig Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `max_age_seconds` | integer | No | > 0 |
| `require_not_revoked` | boolean | No | Default false |
| `revocation_grace_seconds` | integer | No | Used when offline |

## Constraints

1. `required_claims` MUST NOT be empty.
2. A `predicate_spec` with `predicate_type: RANGE_PROOF` MUST have either (`threshold` + `comparison`) or (`min` + `max`) in `params`.
3. `fallback_policy: REQUIRE_PREDICATE` MUST only be used when `supported_circuits` is non-empty.
4. `trust_profile_id` MUST reference an existing Trust Profile if present.
5. A `predicate_spec` with `fallback_policy: REQUIRE_PREDICATE` applied to a credential format that does not support ZK (e.g., `VC_JWT`) MUST be treated as an error at policy creation time.

## ZK Predicate Evaluation Order

When a claim has a `predicate_spec`:

```
1. Does the verifier support the specified circuits?
   YES → request ZK proof
   NO  → consult fallback_policy:
     REQUIRE_PREDICATE → reject the presentation request (cannot be satisfied)
     ACCEPT_RAW        → fall back to requesting raw claim value
     DENY              → reject the presentation outright
```

## Cross-References

| Referencing Entity | Reference Field | Behavior |
|--------------------|-----------------|----------|
| Deployment Profile | `presentation_policy_ids` | Required — at least one policy |
| Flow | `presentation_policy_id` | Required for verification flows |

## Examples

### Age Verification with ZK Predicate

```json
{
  "id": "pp-age-21",
  "organization_id": "org-001",
  "name": "Age 21+ Verification",
  "required_claims": [
    {
      "claim_name": "age_over_21",
      "predicate_spec": {
        "predicate_type": "EQUALITY",
        "params": {"target_value": true},
        "fallback_policy": "ACCEPT_RAW"
      }
    }
  ],
  "prefer_predicates": true,
  "holder_binding": {"required": true, "binding_methods": ["NONCE"], "nonce_required": true},
  "freshness": {"require_not_revoked": true},
  "created_at": "2026-03-11T00:00:00Z"
}
```

## See Also

- Root specification: [§7 Presentation Policy](../../SPECIFICATION.md#7-presentation-policy)
- Schema: [../../schemas/presentation-policy.json](../../schemas/presentation-policy.json)
- Enums: [../../enums/predicate-types.json](../../enums/predicate-types.json), [../../enums/fallback-policies.json](../../enums/fallback-policies.json)
- Design decisions: [DESIGN.md](./DESIGN.md)
