# Issuer Registry — Entity Specification

**Entity:** IssuerEntity, TrustProfileIssuer
**Version:** 0.1.0
**Stability:** Stable
**Section in root spec:** §5.3

---

## Purpose

The Issuer Registry tracks the **lifecycle of credential-issuing authorities** as distinct entities from cryptographic Trust Anchors. An issuer is an organisation or authority; a Trust Anchor is a cryptographic root used to verify their signatures. One issuer may be backed by multiple trust anchors over time.

## Entities

### IssuerEntity

Represents a named credential issuer with full lifecycle management.

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `id` | UUID | Yes | Unique |
| `organization_id` | UUID\|null | Yes | `null` = global system issuer (auto-visible to all orgs) |
| `issuer_id` | string | Yes | DID, domain, X.509 subject DN, or custom ID |
| `issuer_type` | IssuerType | Yes | `ORGANIZATION`, `GOVERNMENT`, `DEVICE` |
| `display_name` | string | Yes | 1–256 characters |
| `description` | string | No | Max 1024 characters |
| `is_system_issuer` | boolean | No | `true` = auto-enrolled in all org trust profiles (ICAO/AAMVA states) |
| `compliance_status` | ComplianceStatus | Yes | `ACCREDITED`, `COMPLIANT`, `SUSPENDED`, `REVOKED` |
| `accreditation_body` | string | No | Who certified this issuer |
| `accreditation_date` | datetime | No | When certification was granted |
| `valid_from` | datetime | Yes | Start of validity period |
| `valid_until` | datetime\|null | No | `null` = indefinite |
| `trust_anchor_id` | UUID\|null | No | Optional link to trust anchor for X.509-backed issuers |
| `revoked_at` | datetime\|null | No | Populated on revocation |
| `revocation_reason` | string\|null | No | See `revocation-reasons` enum |
| `revoked_by` | string\|null | No | Who revoked |

#### Compliance Status Lifecycle

```
ACCREDITED → COMPLIANT → SUSPENDED → COMPLIANT  (reinstatement)
                     ↘
                   REVOKED (terminal)
```

### TrustProfileIssuer

Join entity between `TrustProfile` and `IssuerEntity` with trust scoring.

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `id` | UUID | Yes | Unique |
| `trust_profile_id` | UUID | Yes | References `TrustProfile.id` |
| `issuer_id` | UUID | Yes | References `IssuerEntity.id` |
| `trust_level` | integer | Yes | 0–100; default 100 |
| `relationship_status` | RelationshipStatus | Yes | `TRUSTED`, `DENIED`, `UNDER_REVIEW` |
| `cascade_revocation_policy` | CascadePolicy | Yes | `AUTO_CASCADE`, `MANUAL`, `NOTIFY_ONLY` |

## Trust Scoring

`trust_level` (0–100) is the consumer-facing trust score for an issuer within a specific Trust Profile. It is used by `PresentationPolicy.issuer_constraints.min_trust_level` to filter credentials at verification time.

**Planned: automatic trust_level adjustment** based on issuer history (failed validations, revocation events, compliance lapses). Currently set manually.

## Cascade Revocation

When an `IssuerEntity` or trust anchor is revoked, a `CascadeRevocationOperation` is created. The `TrustProfileIssuer.cascade_revocation_policy` determines the cascade behaviour:

| Policy | Behaviour |
|--------|-----------|
| `AUTO_CASCADE` | All credentials issued by this issuer are automatically revoked |
| `MANUAL` | Affected credentials are queued for human review |
| `NOTIFY_ONLY` | Affected parties are notified; credentials remain active until manually revoked |

If `affected_credential_count >= circuit_breaker_threshold` (default 1000), the operation pauses and `requires_confirmation` is set to `true`. A privileged user must confirm before the cascade proceeds.

## Constraints

1. `issuer_id` MUST be unique within an organisation (or globally for system issuers).
2. `trust_level` MUST be in range [0, 100].
3. A `TrustProfileIssuer` cannot exist without both a valid `TrustProfile` and `IssuerEntity`.
4. Revoking an `IssuerEntity` triggers a `CascadeRevocationOperation` based on its `TrustProfileIssuer.cascade_revocation_policy`.
5. A `REVOKED` issuer cannot be reinstated (use `superseded` + create new IssuerEntity instead).
