# Issuer Registry — Entity Specification

**Entity:** IssuerEntity, IssuerIdentity, TrustProfileIssuer
**Version:** 0.3.1
**Stability:** Stable
**Section in root spec:** §5.3

---

## Purpose

The Issuer Registry tracks the **lifecycle of credential-issuing authorities** as distinct entities from cryptographic Trust Anchors. An issuer is an organisation or authority; a Trust Anchor is a cryptographic root used to verify their signatures. One issuer may be backed by multiple trust anchors over time.

## Entities

### IssuerEntity

Represents a named credential issuer with full lifecycle management.

`IssuerEntity` is a trust-registry record. It does not identify a KMS service,
key reference, or internal issuer profile and MUST NOT be used as a custody
selector.

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
| `metadata` | object | Yes | Public descriptive metadata only; custody and key-routing selectors are prohibited recursively |
| `created_at` | datetime | Yes | Creation time |
| `updated_at` | datetime | Yes | Last update time |

#### Public operations

```
GET     /v1/issuer-entities                         List issuer trust records
POST    /v1/issuer-entities                         Create a tenant record
GET     /v1/issuer-entities/{id}                    Get a trust record
PATCH   /v1/issuer-entities/{id}                    Partially update a tenant record
DELETE  /v1/issuer-entities/{id}                    Delete a tenant record
GET     /v1/signing-keys/issuer-identities          List public DID signing identities
POST    /v1/signing-keys/issuer-identities          Provision or adopt a managed DID identity
POST    /v1/signing-keys/issuer-identities/resolve  Resolve the exact identity's public JWK
PUT     /v1/signing-keys/issuer-identities/certificate  Attach a matching public certificate chain
DELETE  /v1/signing-keys/issuer-identities          Retire exactly one DID identity
```

- Public create requires `organization_id`; callers cannot create or claim a
  global/system issuer.
- Public partial update requires `organization_id` and uses `PATCH` semantics.
- `revoked_by` is assigned from the authenticated actor and is never accepted
  from the public request.
- Global/system issuer mutation is an internal governance operation. A public
  endpoint MUST fail closed for update or deletion of such a record.
- Successful public responses MUST be validated against `issuer-entity.json`
  before they leave an implementation boundary.

#### Compliance Status Lifecycle

```
ACCREDITED → COMPLIANT → SUSPENDED → COMPLIANT  (reinstatement)
                     ↘
                  REVOKED (terminal)
```

### IssuerIdentity

`IssuerIdentity` is the tenant-scoped public DID projection used to select a
signing identity. It is deliberately distinct from both `IssuerEntity` and the
private issuer profile that resolves to managed custody.

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `issuer_did` | DID URI | Yes | Public signing identity |
| `key_purpose` | enum | Yes | Intended signing or trust purpose |
| `algorithm` | enum | Yes | Public algorithm compatibility dimension |
| `status` | string | Yes | Always `active` in the public projection |

The list operation is authenticated and organization-scoped. It MUST project
only active identities. If the same organization, DID, purpose, and algorithm
resolve to more than one active private issuer profile, the operation MUST fail
with an ambiguity error rather than choose one. Internal profile IDs,
verification-method selectors, signing-service IDs, key references, provider
names, KMS coordinates, or key versions MUST NOT appear in the response.
The public identity projection includes `credential_format`; implementations
MUST NOT collapse format-specific identities into a purpose/algorithm-only
projection.
Public-key resolution accepts the same complete tuple and returns only the
provider-neutral identity plus its public JWK. The implementation selects the
DID verification method internally; callers MUST NOT supply a verification
method, key ID, profile, service, provider, or KMS coordinate.

Create, certificate, and delete operations select the identity with the complete
tuple `(organization_id, issuer_did, key_purpose, credential_format,
algorithm)`. The implementation MUST resolve that tuple to exactly one active,
compatible private issuer profile and MUST fail closed when it is unknown,
inactive, ambiguous, incompatible, or owned by a different organization.
Creation MAY provision a new managed key, but service, provider, key reference,
and KMS selection are implementation decisions and MUST NOT be accepted from or
returned to the public caller. A repeated create is idempotent only when the
tuple resolves to exactly one compatible active identity. Certificate attachment
MUST verify that the leaf certificate contains the same public key as the DID's
managed verification method before persisting the public chain.

Creation MAY include `key_attestation_policy`, a provider-neutral holder-key
trust policy containing public trust anchors and validation requirements. This
policy governs proofs accepted during issuance; it is not an issuer-key or KMS
selector and MUST be validated before the private profile is activated.

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
6. Public `IssuerEntity` metadata MUST reject custody and key-routing selectors
   at every nesting depth.
7. `IssuerIdentity` lookup MUST be scoped by the authenticated organization and
   MUST fail closed for inactive or ambiguous mappings.
