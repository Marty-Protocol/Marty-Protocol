# Credential Template — Entity Specification

**Entity:** Credential Template
**Version:** 0.3.1
**Stability:** Moderate
**Section in root spec:** §6

---

## Purpose

A Credential Template is the **master public issuance configuration**. It
combines the claims, compliance profile, issuer DID, validity rules, and
optional application workflow. Signing profiles, verification-method
selection, certificates, and key custody are resolved internally from the
owning organization and `issuer_did`; they are not fields in this public
entity.

Templates are reusable. Many credentials may be issued from a single template.

## What It Contains

| Dimension | Description |
|-----------|-------------|
| Claims | Claim definitions with type, namespace, disclosure config |
| Compliance | Which compliance profile governs format and encoding |
| Issuer | Public DID only; signing profiles and custody remain private |
| Validity | TTL, renewable, reissue window |
| Workflow | Optional application form + approval process |

## Properties

### Core Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `id` | UUID | Yes | Unique |
| `organization_id` | UUID | Yes | Must reference existing organization |
| `name` | string | Yes | 1–128 characters |
| `credential_type` | string | Yes | PascalCase type name; e.g., `EmployeeBadge` |
| `description` | string | No | Max 1024 characters |
| `compliance_profile_id` | UUID | Yes | Must reference existing Compliance Profile |
| `application_template_id` | UUID | No | Null for direct/batch issuance |
| `trust_profile_id` | UUID | No | Issuer trust constraints |
| `revocation_profile_id` | UUID | No | Revocation configuration |
| `claims` | ClaimDefinition[] | Yes | At least one claim required |
| `validity_rules` | ValidityRules | Yes | See below |
| `issuer_did` | string | Conditional | Required for every `ACTIVE` issuance template |
| `privacy_posture` | PrivacyPosture | No | See below |
| `status` | TemplateStatus | Yes | `DRAFT`, `ACTIVE`, `DEPRECATED` |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

### ValidityRules Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `ttl_seconds` | integer | Yes | > 0 |
| `renewable` | boolean | No | Default false |
| `reissue_within_seconds` | integer | No | < `ttl_seconds` when set |
| `not_before_offset_seconds` | integer | No | >= 0 |

### ClaimDefinition Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `name` | string | Yes | snake_case; unique within template |
| `type` | ClaimType | Yes | `STRING`, `INTEGER`, `BOOLEAN`, `DATE`, `OBJECT`, `ARRAY` |
| `description` | string | No | |
| `required` | boolean | Yes | |
| `selectively_disclosable` | boolean | No | Default false |
| `derived_from` | string | No | References another claim `name` in same template |
| `namespace` | string | No | mDoc namespace (e.g., `org.iso.18013.5.1`) |
| `display` | ClaimDisplay | No | UI display name and icon |

### PrivacyPosture Fields

| Property | Type | Description |
|----------|------|-------------|
| `default_disclose_all` | boolean | If true, all claims disclosed unless holder de-selects |
| `prefer_predicates` | boolean | Prefer ZK predicates for boolean-derivable claims |
| `sd_alg` | string | SD-JWT hash algorithm (default `sha-256`) |

## Constraints

1. Every `ACTIVE` issuance template MUST contain `issuer_did`.
2. The public entity MUST reject issuer-profile IDs, verification-method selectors, algorithms, certificate bindings, KMS providers, signing-service IDs, key references, and artifact-generation controls.
3. The implementation MUST resolve `organization_id` + `issuer_did` + operation/purpose + credential format + algorithm to exactly one authorized active internal issuer profile and fail closed for unknown, inactive, ambiguous, incompatible, mismatched, or cross-organization mappings.
4. Signing MUST execute through the resolved issuer profile. The public caller never selects or invokes KMS custody directly.
5. `claims` MUST NOT be empty.
6. Claim names MUST be unique within a template.
7. `derived_from` MUST reference a valid `name` in the same template's `claims` array.
8. A `DRAFT` template MUST NOT be used in an active Flow or issuance trigger.
9. When `application_template_id` is set, the template MUST NOT be used for direct API issuance.
10. `compliance_profile_id` MUST reference an existing Compliance Profile.

## Derived Entities

The Credential Template is the **primary input** to wallet compatibility derivation:

```
(credential_template.compliance_profile.credential_format,
 credential_template.compliance_profile.issuance_protocol,
 credential_template.compliance_profile.compliance_code)
→ Wallet Profile (derived)
```

## Cross-References

| Referencing Entity | Reference Field | Behavior |
|--------------------|-----------------|----------|
| Flow | `credential_template_id` | Required for issuance flows |
| Wallet Profile | (derivation input) | Derived; not a direct FK |

## Lifecycle

```
DRAFT → (configure claims + issuer DID) → ACTIVE
ACTIVE → (superseded by new version) → DEPRECATED
DRAFT  → (deleted before use)        → [removed]
DEPRECATED → MUST NOT be used for new issuance
```

## Examples

### mDL Template (AAMVA)

```json
{
  "id": "ct-001",
  "organization_id": "org-001",
  "name": "AAMVA Mobile Driver License",
  "credential_type": "MobileDriverLicense",
  "compliance_profile_id": "cp-aamva-mdl",
  "validity_rules": {
    "ttl_seconds": 31536000,
    "renewable": true,
    "reissue_within_seconds": 2592000
  },
  "claims": [
    {
      "name": "family_name",
      "type": "STRING",
      "required": true,
      "namespace": "org.iso.18013.5.1",
      "selectively_disclosable": true
    },
    {
      "name": "age_over_21",
      "type": "BOOLEAN",
      "required": false,
      "derived_from": "birth_date",
      "selectively_disclosable": true
    }
  ],
  "issuer_did": "did:web:issuer.example.gov",
  "status": "ACTIVE",
  "created_at": "2026-03-11T00:00:00Z"
}
```

## See Also

- Root specification: [§6 Credential Template](../../SPECIFICATION.md#6-credential-template)
- Schema: [../../schemas/credential-template.json](../../schemas/credential-template.json)
- Compliance Profiles: [../compliance-profile/SPECIFICATION.md](../compliance-profile/SPECIFICATION.md)
- Design decisions: [DESIGN.md](./DESIGN.md)
