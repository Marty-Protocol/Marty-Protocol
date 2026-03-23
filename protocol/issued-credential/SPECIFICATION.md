# Issued Credential — Entity Specification

**Entity:** IssuedCredential
**Version:** 0.1.0
**Stability:** Stable
**Section in root spec:** §10

---

## Purpose

**IssuedCredential** is the authoritative lifecycle record for a credential issued by the platform. It is created when a FlowExecution of type `oid4vci_pre_authorized`, `oid4vci_authorization_code`, `mdl_issuance`, or `application_approval_issuance` completes successfully.

IssuedCredential does **not** store the credential payload. It stores only metadata and hashes sufficient to:
- Audit that a specific credential was issued at a specific time to a specific subject
- Drive revocation (via status list entries)
- Correlate credential lifecycle events across system components

---

## Lifecycle States

```
          issued
            │
            ▼
         active ──────────────────────┐
            │                         │
     (holder request                  │ (compliance event,
      or admin action)                │  issuer revocation,
            │                         │  cascade revocation)
            ▼                         ▼
        suspended ──────────────→  revoked
            │
     (suspension lifted)
            │
            ▼
         active
            │
     (valid_until reached)
            │
            ▼
         expired
```

| Status | Meaning |
|--------|---------|
| `active` | Credential is valid and usable |
| `suspended` | Credential temporarily invalid; may be reactivated |
| `revoked` | Credential permanently invalid; cannot be reactivated |
| `expired` | Credential reached `valid_until`; informational only |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/issued-credentials` | List issued credentials (paginated) |
| GET | `/v1/issued-credentials/{id}` | Get issued credential record |
| POST | `/v1/issued-credentials/{id}/revoke` | Revoke a credential |
| POST | `/v1/issued-credentials/{id}/suspend` | Suspend a credential |
| POST | `/v1/issued-credentials/{id}/reinstate` | Reinstate a suspended credential |

IssuedCredentials are never created directly via API; they are created by the system when a FlowExecution completes.

---

## Privacy Model

The IssuedCredential record stores **no PII**. Subject identity is preserved only as:

| Field | Value | Purpose |
|-------|-------|---------|
| `subject_id` | Opaque internal UUID | Correlate credentials for the same subject within the platform |
| `subject_claims_hash` | SHA-256 of canonical subject claims | Audit proof without revealing data |
| `credential_hash` | SHA-256 of the issued credential bytes | Tamper-evidence; does not reveal payload |

---

## Status List Entries

A single IssuedCredential may have multiple entries in different status lists (e.g. one for Status List 2021 and one for MDOC/mDL revocation). Each entry in `status_list_entries` tracks:

| Field | Example | Note |
|-------|---------|------|
| `list_uri` | `https://issuer.example/status/1` | URL of the published status list |
| `index` | 42 | Bit position in the status list |
| `status_purpose` | `revocation` | Purpose per W3C Status List 2021 spec |

Revocation writes to all entries atomically.

---

## Revocation

### Single-credential revocation

`POST /v1/issued-credentials/{id}/revoke`

Request body:
```json
{
  "reason": "KEY_COMPROMISE",
  "notes": "Holder reported device lost"
}
```

`reason` must be one of the values in `enums/revocation-reasons.json`.

### Cascade revocation

If the associated IssuerEntity is revoked, and the `TrustProfileIssuer.cascade_revocation_policy` is `AUTO_CASCADE`, a CascadeRevocationOperation is created covering all `active` IssuedCredentials for that issuer. See `protocol/issuer-registry/SPECIFICATION.md` for details.

---

## Properties

See `schemas/issued-credential.json` for full JSON Schema.

Key fields:

| Property | Type | Required | Note |
|----------|------|----------|------|
| `id` | UUID | Yes | System-generated |
| `organization_id` | UUID | Yes | |
| `flow_execution_id` | UUID | Yes | The FlowExecution that produced this credential |
| `application_id` | UUID | No | Set when flow_type is `application_approval_issuance` |
| `credential_template_id` | UUID | Yes | Template used during issuance |
| `issuer_entity_id` | UUID | Yes | The IssuerEntity that signed the credential |
| `subject_id` | UUID | Yes | Opaque subject identifier |
| `credential_format` | string | Yes | One of `enums/credential-formats.json` values: `MDOC`, `SD_JWT_VC`, `VC_JWT`, `JSON_LD` |
| `credential_hash` | string | Yes | SHA-256 hex of issued credential bytes |
| `subject_claims_hash` | string | Yes | SHA-256 hex of canonical subject claims JSON |
| `status` | string | Yes | `active`, `suspended`, `revoked`, `expired` |
| `status_list_entries` | array | No | Zero or more status list slot references |
| `issued_at` | datetime | Yes | |
| `valid_until` | datetime | No | Null = no expiry |
| `revoked_at` | datetime | No | Set on revocation |
| `revocation_reason` | string | No | One of `enums/revocation-reasons.json` values |

---

## Relationships

```
FlowExecution ──────────────→ IssuedCredential
                                     │
               ┌─────────────────────┼──────────────────────┐
               ▼                     ▼                       ▼
        IssuerEntity       CredentialTemplate        StatusListEntry
```

- One FlowExecution creates zero or one IssuedCredential
- One IssuedCredential references exactly one IssuerEntity and one CredentialTemplate
- One IssuedCredential may have multiple StatusListEntries (one per revocation mechanism)
