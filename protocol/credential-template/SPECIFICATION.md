# Credential Template — Entity Specification

**Entity:** Credential Template
**Version:** 0.1.0
**Stability:** Moderate
**Section in root spec:** §6

---

## Purpose

A Credential Template is the **master issuance configuration**. It combines:
- **Schema** — the claims the credential contains
- **Compliance Profile** — the encoding format and standards framework
- **Cryptographic Materials** — keys, certificates, or DID references
- **Validity Rules** — duration, renewability, reissuance
- **Optional Workflow** — link to an Application Template for user-facing collection

Templates are reusable. Many credentials may be issued from a single template.

## What It Contains

| Dimension | Description |
|-----------|-------------|
| Claims | Claim definitions with type, namespace, disclosure config |
| Compliance | Which compliance profile governs format and encoding |
| Crypto | Signing key, algorithm, certificate chain or DID |
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
| `issuer_key_id` | string | Conditional | Required unless `auto_generate_artifacts` |
| `issuer_algorithm` | Algorithm | No | From `validation-algorithms` enum |
| `key_access_mode` | KeyAccessMode | No | `KEY_VAULT`, `HSM`, `LOCAL`, `REMOTE_SIGNING` |
| `issuer_certificate_chain_pem` | string | Conditional | For X.509-based credentials |
| `issuer_did` | string | Conditional | For DID-based credentials |
| `issuer_identity` | IssuerIdentity | No | DID-first binding for KMS/remote-backed issuance |
| `remote_signing_config` | RemoteSigningConfig | No | Private deployment metadata for `REMOTE_SIGNING` |
| `auto_generate_artifacts` | boolean | No | Dev only; default false |
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

### IssuerIdentity Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `issuer_did` | DID URI | Yes | Public issuer identity that appears in issued credentials |
| `issuer_profile_id` | string | No | Organization issuer profile binding the DID to a signing service |
| `verification_method_id` | DID URL | No | DID verification method used as the public `kid` |
| `remote_key_binding` | object | No | Private resolver metadata such as KMS service/key references |

`remote_key_binding` is not a public trust anchor. It may include private deployment fields such as `organization_id`, `signing_service_id`, `signing_key_reference`, and `kms_provider`. Verifiers MUST validate credentials through `issuer_identity.issuer_did` and the matching DID verification method, not through opaque KMS key IDs.

## Constraints

1. For `ACTIVE` templates: exactly one of `issuer_key_id`, `issuer_certificate_chain_pem`, `issuer_did`, or `issuer_identity.issuer_did` MUST be present unless `auto_generate_artifacts` is `true`.
2. DID-backed templates SHOULD use `issuer_identity` instead of raw `issuer_key_id`; when `issuer_identity` is present, signing MUST resolve through the organization issuer identity registry.
3. `claims` MUST NOT be empty.
4. Claim names MUST be unique within a template.
5. `derived_from` MUST reference a valid `name` in the same template's `claims` array.
6. A `DRAFT` template MUST NOT be used in an active Flow or issuance trigger.
7. When `application_template_id` is set, the template MUST NOT be used for direct API issuance.
8. `compliance_profile_id` MUST reference an existing Compliance Profile.

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
DRAFT → (configure claims + crypto) → ACTIVE
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
  "issuer_certificate_chain_pem": "-----BEGIN CERTIFICATE-----\n...",
  "issuer_algorithm": "ES256",
  "status": "ACTIVE",
  "created_at": "2026-03-11T00:00:00Z"
}
```

## See Also

- Root specification: [§6 Credential Template](../../SPECIFICATION.md#6-credential-template)
- Schema: [../../schemas/credential-template.json](../../schemas/credential-template.json)
- Compliance Profiles: [../compliance-profile/SPECIFICATION.md](../compliance-profile/SPECIFICATION.md)
- Design decisions: [DESIGN.md](./DESIGN.md)
