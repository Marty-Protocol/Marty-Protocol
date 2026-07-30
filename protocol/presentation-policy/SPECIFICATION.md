# Presentation Policy — Entity Specification

**Entity:** Presentation Policy
**Version:** 0.3.1
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
| Holder Binding | Which credential, device, or session control proof is required |
| Freshness | How recent the credential or its revocation check must be |
| Issuer Constraints | Which issuers are accepted (via Trust Profile reference) |

## Properties

### Core Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `id` | UUID | Yes | Unique |
| `organization_id` | UUID | Yes | Must reference existing organization |
| `name` | string | Yes | 1–255 characters |
| `status` | string | Yes | `draft`, `active`, `suspended`, or `archived` |
| `description` | string | No | Max 2000 characters |
| `purpose` | string | No | Max 2000 characters; shown to the holder |
| `required_claims` | RequiredClaim[] | Yes | May be empty only when a template-bound or alternative requirement is present |
| `accepted_credential_types` | string[] | Yes | If empty, types are derived from template-bound requirements |
| `display_metadata` | object | No | Holder-facing verifier, purpose, privacy-policy, and terms metadata |
| `credential_requirements` | CredentialRequirement[] | No | Template-bound grouped claims and format/trust constraints |
| `alternative_requirements` | AlternativeRequirement[] | No | Threshold alternatives composed from credential requirements |
| `compliance_profile_id` | string | No | Compliance rules applied to verification |
| `trust_profile_id` | UUID | No | Issuer trust constraints |
| `holder_binding` | HolderBinding | No | See below |
| `freshness` | FreshnessConfig | No | See below |
| `prefer_predicates` | boolean | No | Default false |
| `supported_circuits` | string[] | No | ZK circuit identifiers |
| `fallback_policy` | FallbackPolicy | No | Default `ACCEPT_RAW` |
| `credential_ranking_strategy` | string | Yes | `FRESHEST_FIRST`, `HIGHEST_TRUST_FIRST`, or `CUSTOM` |
| `credential_ranking_weights` | object | No | Required for `CUSTOM` ranking |
| `version` | integer | Yes | Immutable policy version, starting at 1 |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | Yes | ISO 8601 |

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
| `binding_methods` | string[] | Conditional | `CREDENTIAL_KEY`, `DEVICE_KEY`, `SESSION_BINDING` |
| `proof_profiles` | string[] | Conditional | `OID4VP_VERIFIABLE_PRESENTATION`, `SD_JWT_KEY_BINDING`, `MDOC_DEVICE_AUTHENTICATION`, `CUSTOM` |
| `proof_freshness` | object | Conditional | Challenge, audience, replay, and proof-age checks |

All conditional fields are required when `required` is true and prohibited when false.

### ProofFreshness Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `challenge_required` | boolean | No | Default true; validate nonce or format-equivalent challenge inside the authenticated proof |
| `audience_binding_required` | boolean | No | Default true; bind proof to the verifier or transaction audience |
| `replay_detection_required` | boolean | No | Default true; reject reuse outside the original transaction |
| `max_proof_age_seconds` | integer | No | Positive maximum age when the proof profile carries time |

`NONCE` is not a binding method. A nonce establishes freshness only when it is covered by a valid signature, MAC, device-authentication structure, or authenticated session proof.

### Binding Method Semantics

- `CREDENTIAL_KEY`: the verifier validates control of the private key associated with the credential at issuance. SD-JWT Key Binding is the standard example.
- `DEVICE_KEY`: the verifier validates a format-defined device key proof, such as mdoc Device Authentication.
- `SESSION_BINDING`: the verifier validates that the presentation is cryptographically bound to the current authenticated session or session transcript.

The selected `proof_profiles` define the wire checks. Implementations MUST validate the profile's signature or MAC, credential-to-key association, challenge, audience, replay state, and permitted algorithms. `CUSTOM` requires a versioned custom Flow extension and MUST NOT be represented as standard MIP interoperability.

### FreshnessConfig Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `max_age_seconds` | integer | No | > 0 |
| `require_not_revoked` | boolean | No | Default false |
| `revocation_grace_seconds` | integer | No | Used when offline |

## Constraints

1. At least one of `required_claims`, `credential_requirements`, or
   `alternative_requirements` MUST NOT be empty. Template-bound requirements
   preserve the authoritative Credential Template identity and format; they
   are public policy semantics, not verifier implementation metadata.
2. A `predicate_spec` with `predicate_type: RANGE_PROOF` MUST have either (`threshold` + `comparison`) or (`min` + `max`) in `params`.
3. `fallback_policy: REQUIRE_PREDICATE` MUST only be used when `supported_circuits` is non-empty.
4. `trust_profile_id` MUST reference an existing Trust Profile if present.
5. A `predicate_spec` with `fallback_policy: REQUIRE_PREDICATE` applied to a credential format that does not support ZK (e.g., `VC_JWT`) MUST be treated as an error at policy creation time.
6. `holder_binding.required: true` requires non-empty, unique `binding_methods` and `proof_profiles`, plus `proof_freshness`.
7. `holder_binding.required: false` prohibits binding methods, proof profiles, and proof-freshness settings.
8. Policy activation MUST reject proof profiles incompatible with accepted credential formats or unavailable verifier capabilities.

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

## Public API Operations

The public create operation uses
[`presentation-policy-create-request.json`](../../schemas/presentation-policy-create-request.json).
It requires `organization_id`, `name`, and at least one canonical claim,
template-bound requirement, or alternative requirement.

The public partial-update operation uses
[`presentation-policy-update-request.json`](../../schemas/presentation-policy-update-request.json).
It always requires `organization_id` so the gateway can compare the caller's
tenant context with the resource owner before forwarding the mutation. The
tenant selector is a public authorization boundary and is not persisted as a
mutable policy field.

Both operation schemas reject unknown fields. Credential Template formats are
authoritative: a caller may identify a template but MUST NOT override the
template's configured credential format. Custody routing, issuer-profile IDs,
service IDs, key references, and KMS/provider selectors are never valid
Presentation Policy inputs.

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
  "holder_binding": {
    "required": true,
    "binding_methods": ["DEVICE_KEY", "SESSION_BINDING"],
    "proof_profiles": ["MDOC_DEVICE_AUTHENTICATION"],
    "proof_freshness": {
      "challenge_required": true,
      "audience_binding_required": true,
      "replay_detection_required": true
    }
  },
  "freshness": {"require_not_revoked": true},
  "created_at": "2026-03-11T00:00:00Z"
}
```

## See Also

- Root specification: [§7 Presentation Policy](../../SPECIFICATION.md#7-presentation-policy)
- Schema: [../../schemas/presentation-policy.json](../../schemas/presentation-policy.json)
- Enums: [../../enums/predicate-types.json](../../enums/predicate-types.json), [../../enums/fallback-policies.json](../../enums/fallback-policies.json)
- Design decisions: [DESIGN.md](./DESIGN.md)
