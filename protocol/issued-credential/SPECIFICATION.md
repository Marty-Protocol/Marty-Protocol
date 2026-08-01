# Issued Credential — Entity Specification

**Entity:** IssuedCredential
**Version:** 0.3.1
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
          ISSUED
            │
            ▼
         ACTIVE ──────────────────────┐
            │                         │
     (holder request                  │ (compliance event,
      or admin action)                │  issuer revocation,
            │                         │  cascade revocation)
            ▼                         ▼
        SUSPENDED ──────────────→  REVOKED
            │
     (suspension lifted)
            │
            ▼
         ACTIVE
            │
     (valid_until reached)
            │
            ▼
         EXPIRED
```

| Status | Meaning |
|--------|---------|
| `ACTIVE` | Credential is valid and usable |
| `SUSPENDED` | Credential temporarily invalid; may be reactivated |
| `REVOKED` | Credential permanently invalid; cannot be reactivated |
| `EXPIRED` | Credential reached `valid_until`; informational only |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/issued-credentials` | List issued credentials (paginated) |
| GET | `/v1/issued-credentials/{id}` | Get issued credential record |
| POST | `/v1/issued-credentials/{id}/revoke` | Revoke a credential |
| POST | `/v1/issued-credentials/{id}/suspend` | Suspend a credential |
| POST | `/v1/issued-credentials/{id}/reinstate` | Reinstate a suspended credential |
| POST | `/v1/issued-credentials/{id}/renew` | Create a replacement offer for an eligible active credential |
| GET | `/v1/issued-credentials/mine?status&limit&offset` | Authenticated holder inventory |

IssuedCredentials are never created directly via API; they are created by the system when a FlowExecution completes.

All management endpoints are authenticated and tenant-bound. List operations require the selected `organization_id`; ID-based operations MUST hide a resource from callers authorized for another organization. Public records never include delivery routing records, issuer-profile IDs, signing-service IDs, key references, KMS/provider selectors, bearer tokens, or pre-authorized codes.

### Holder Inventory

`GET /v1/issued-credentials/mine` derives the holder from authenticated request state and returns `HolderCredentialInventory`. The response is display and lifecycle metadata only. It MUST NOT include credential material, subject claims, subject identifiers, credential hashes, claims hashes, signing-key references, or status-list internals. See `schemas/holder-credential-inventory.json`.

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
  "reason": "Holder reported device lost"
}
```

`reason` is optional public audit text of at most 2,000 characters. Services may map it to a controlled internal revocation taxonomy without exposing internal state.

## Renewal

`POST /v1/issued-credentials/{id}/renew` is available only when the source credential is active, its Credential Template allows renewal, and the stored renewal window has opened. The response is a fresh holder offer; creating the offer does not change the source credential.

After the replacement offer is redeemed successfully, the service MUST:

- set the replacement `renewed_from_credential_id` to the source credential;
- set the source `renewed_to_credential_id` to the replacement credential;
- revoke the source with a supersession reason; and
- reject any later renewal attempt for the same source.

An abandoned or expired replacement offer leaves the source active and may be retried.

### Cascade revocation

If the associated IssuerEntity is revoked, and the `TrustProfileIssuer.cascade_revocation_policy` is `AUTO_CASCADE`, a CascadeRevocationOperation is created covering all `ACTIVE` IssuedCredentials for that issuer. See `protocol/issuer-registry/SPECIFICATION.md` for details.

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
| `issuer_did` | string | No | Public DID that signed the credential; custody/profile selectors remain private |
| `subject_id` | string | Yes | DID, device key, or opaque holder identifier |
| `credential_format` | string | Yes | One of `enums/credential-formats.json` values: `MDOC`, `SD_JWT_VC`, `VC_JWT`, `JSON_LD` |
| `credential_hash` | string | No | SHA-256 hex of issued credential bytes |
| `subject_claims_hash` | string | No | SHA-256 hex of canonical subject claims JSON |
| `status` | string | Yes | `ACTIVE`, `SUSPENDED`, `REVOKED`, `EXPIRED` |
| `status_list_entries` | array | Yes | Zero or more status list slot references |
| `renewed_from_credential_id` | string | No | Source credential replaced by this credential |
| `renewed_to_credential_id` | string | No | Replacement credential that superseded this credential |
| `renewable` | boolean | No | Whether the source issuance policy permits renewal |
| `renewal_eligible_at` | datetime | No | Earliest time a renewal offer may be created |
| `can_renew` | boolean | No | Derived action readiness for the current lifecycle state and time |
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
          issuer_did       CredentialTemplate        StatusListEntry
```

- One FlowExecution creates zero or one IssuedCredential
- One IssuedCredential records its public `issuer_did` when available and references exactly one CredentialTemplate
- One IssuedCredential may have multiple StatusListEntries (one per revocation mechanism)
