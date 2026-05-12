# Trust Profile — Entity Specification

**Entity:** Trust Profile
**Version:** 0.1.0
**Stability:** Stable
**Section in root spec:** §5

---

## Purpose

A Trust Profile defines **who is trusted** and **how cryptographic validation occurs**. It is the security root for all issuance and verification operations that reference it. Without a Trust Profile, credentials cannot be issued or verified.

## What It Contains

| Dimension | Description |
|-----------|-------------|
| Trust Sources | Certificate roots, DID registries, trust list URLs |
| Algorithms | Accepted cryptographic signature algorithms |
| Formats | Accepted credential encoding formats |
| Revocation | Optional link to a Revocation Profile |
| Time Policy | Clock skew, freshness windows |

## Properties

### Core Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `id` | UUID | Yes | Unique |
| `organization_id` | UUID | Yes | Must reference existing organization |
| `name` | string | Yes | 1–128 characters |
| `description` | string | No | Max 1024 characters |
| `profile_type` | TrustProfileType | Yes | See enum |
| `trust_sources` | TrustSource[] | Yes | At least one entry required |
| `allowed_algorithms` | Algorithm[] | Yes | At least one; from `validation-algorithms` enum |
| `supported_formats` | CredentialFormat[] | Yes | At least one; from `credential-formats` enum |
| `compliance_status` | ComplianceStatus | Yes | Default `SETUP_REQUIRED` |
| `revocation_profile_id` | UUID | No | Must reference existing RevocationProfile |
| `time_policy` | TimePolicy | No | See below |
| `auto_generated` | boolean | No | Default `false` |
| `created_at` | datetime | Yes | ISO 8601; set on creation |
| `updated_at` | datetime | No | ISO 8601; updated on write |

### TrustSource Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `source_type` | TrustSourceType | Yes | From `trust-source-types` enum |
| `url` | string | Conditional | HTTPS URI; required for `TRUST_LIST` and `PKD_URL` |
| `certificate_pem` | string | Conditional | PEM-encoded cert; required for `ROOT_CA` and `PINNED_ISSUER` when no URL |
| `issuer_did` | string | Conditional | DID URI; required for DID-based trust |
| `organization_id` | UUID/string | No | Organization scope for issuer DID resolution |
| `verification_method_ids` | DID URL[] | No | Pinned DID verification methods accepted for this issuer |
| `did_resolution` | DidResolutionPolicy | No | Resolver strategy and cache/fallback policy |
| `description` | string | No | Human-readable label |

Exactly one of `url`, `certificate_pem`, or `issuer_did` MUST be present per TrustSource.

For `PINNED_ISSUER` entries with `issuer_did`, verifiers SHOULD set `organization_id` when the issuer is managed by the relying party's tenant or platform. When `organization_id` is present, verification MUST resolve the DID through the organization's issuer identity registry before using public DID resolution. Public fallback is allowed only when `did_resolution.allow_public_fallback` is true or `resolver_type` is `PUBLIC_DID` / `ORGANIZATION_REGISTRY_WITH_PUBLIC_FALLBACK`.

### DidResolutionPolicy Fields

| Property | Type | Default | Constraint |
|----------|------|---------|------------|
| `resolver_type` | enum | `ORGANIZATION_REGISTRY` | `ORGANIZATION_REGISTRY`, `PUBLIC_DID`, `ORGANIZATION_REGISTRY_WITH_PUBLIC_FALLBACK` |
| `allow_public_fallback` | boolean | `false` | Fail closed unless explicitly enabled |
| `cache_ttl_seconds` | integer | `300` | >= 0 |

### TimePolicy Fields

| Property | Type | Default | Constraint |
|----------|------|---------|------------|
| `clock_skew_seconds` | integer | 300 | 0–3600 |
| `max_credential_age_seconds` | integer | null | Positive or null |
| `require_freshness` | boolean | false | |
| `freshness_window_seconds` | integer | null | Must be set when `require_freshness` is true |

## Constraints

1. `trust_sources` MUST NOT be empty.
2. `allowed_algorithms` MUST NOT be empty.
3. `supported_formats` MUST NOT be empty.
4. A Trust Profile with `compliance_status: SETUP_REQUIRED` MUST NOT be referenced by an active Flow.
5. If `revocation_profile_id` is set, the referenced RevocationProfile MUST exist in the same organization.
6. When `time_policy.require_freshness` is `true`, `time_policy.freshness_window_seconds` MUST be a positive integer.
7. DID-backed `PINNED_ISSUER` sources MUST match the credential issuer DID and, when `verification_method_ids` are present, the credential signing method/kid MUST be one of those DID URLs.

## Validation Configuration — Normative Field Placement

Validation configuration is expressed as discrete top-level fields (`profile_type`, `allowed_algorithms`, `revocation_policy`, `time_policy`, `supported_formats`), not as a generic `validation_rules` wrapper object.

Implementations MUST NOT introduce a `validation_rules` envelope. All validation parameters must map to one of the named top-level properties. If a validation need arises that does not map to an existing property, a new top-level property MUST be added to the schema — the schema MUST NOT be extended via an opaque `validation_rules` bag.

The `profile_type` field (`ICAO` | `AAMVA` | `EUDI` | `CUSTOM`) determines the default trust anchor set and certificate chain validation rules applicable when the Trust Profile is instantiated. Implementations MUST apply profile-type-specific validation logic before evaluating the remaining fields.

## Cross-References

| Referencing Entity | Reference Field | Behavior |
|--------------------|-----------------|----------|
| Credential Template | `trust_profile_id` | Optional — validates issuer trust |
| Presentation Policy | `trust_profile_id` | Optional — validates credential issuer trust |
| Deployment Profile | `trust_profile_id` | Required — validates credentials at this deployment |
| Flow | `trust_profile_id` | Required — root of trust for the flow |

## Lifecycle

```
SETUP_REQUIRED → (configure trust_sources + algorithms) → COMPLIANT
COMPLIANT      → (trust source expires)                 → NEEDS_ATTENTION
NEEDS_ATTENTION → (updated)                             → COMPLIANT
```

## Examples

### Minimal Trust Profile (AAMVA MDL)

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "organization_id": "org-001",
  "name": "AAMVA mDL Trust",
  "profile_type": "AAMVA",
  "trust_sources": [
    {
      "source_type": "TRUST_LIST",
      "url": "https://trust-list.aamva.org/current",
      "description": "AAMVA IACA trust list"
    }
  ],
  "allowed_algorithms": ["ES256", "ES384"],
  "supported_formats": ["MDOC"],
  "compliance_status": "COMPLIANT",
  "created_at": "2026-03-11T00:00:00Z"
}
```

## See Also

- Root specification: [§5 Trust Profile](../../SPECIFICATION.md#5-trust-profile)
- Schema: [../../schemas/trust-profile.json](../../schemas/trust-profile.json)
- Enums: [../../enums/trust-source-types.json](../../enums/trust-source-types.json), [../../enums/validation-algorithms.json](../../enums/validation-algorithms.json)
- Design decisions: [DESIGN.md](./DESIGN.md)
