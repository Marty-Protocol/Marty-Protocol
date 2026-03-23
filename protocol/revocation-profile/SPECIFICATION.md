# Revocation Profile — Entity Specification

**Entity:** Revocation Profile
**Version:** 0.1.0
**Stability:** Stable
**Section in root spec:** §12

---

## Purpose

A Revocation Profile provides **format-agnostic revocation configuration** for both issuers and verifiers. Issuers use it to configure revocation index allocation and list publishing. Verifiers use it to configure how revocation is checked and how to handle offline scenarios.

## What It Contains

| Dimension | Description |
|-----------|-------------|
| Mechanisms | Supported revocation methods (OCSP, CRL, Status List, etc.) |
| Check Mode | How aggressively revocation is checked at verification time |
| Caching | How long revocation results are cached |
| Offline Grace | How long to accept credentials without a fresh revocation check |
| Issuer Config | Status list publishing, index allocation automation |

## Properties

### Core Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `id` | UUID | Yes | Unique |
| `organization_id` | UUID | Yes | Must reference existing organization |
| `name` | string | Yes | 1–128 characters |
| `revocation_mechanism` | RevocationMechanism[] | Yes | At least one; from `revocation-methods` enum |
| `mechanism_priority` | RevocationMechanism[] | No | Priority order; subset of `revocation_mechanism` |
| `check_mode` | RevocationCheckMode | Yes | See values below |
| `cache_ttl_seconds` | integer | Conditional | Required for `CACHED` mode |
| `offline_grace_seconds` | integer | Conditional | Required for `OFFLINE_GRACE` mode |
| `issuer_config` | IssuerRevocationConfig | No | Issuer-side automation |
| `status_list_url` | string | No | Published status list URL (HTTPS) |
| `created_at` | datetime | Yes | ISO 8601 |

### RevocationCheckMode Values

| Value | Description | Required Supplemental Fields |
|-------|-------------|------------------------------|
| `ALWAYS` | Live check required on every verification | None |
| `CACHED` | Accept cached check within TTL | `cache_ttl_seconds` |
| `OFFLINE_GRACE` | Accept last known status within grace period | `offline_grace_seconds` |
| `SKIP` | Revocation not checked | None (use with caution) |

### RevocationMechanism Values

| Value | Standard | Description |
|-------|----------|-------------|
| `OCSP` | RFC 6960 | Online Certificate Status Protocol |
| `CRL` | RFC 5280 | Certificate Revocation List |
| `STATUS_LIST_2021` | W3C Status List 2021 | Bitstring status list (W3C) |
| `BITSTRING_STATUS_LIST` | IETF draft-ietf-oauth-status-list | IETF Bitstring Status List |
| `TOKEN_STATUS_LIST` | IETF RFC 9738 | Token Status List (TS) |

### IssuerRevocationConfig Fields

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `auto_allocate_index` | boolean | No | Allocate status index on credential issuance |
| `batch_update_interval_seconds` | integer | No | Status list publishing cadence |
| `list_size` | integer | No | Status list bitstring size (default: 131072) |
| `uri_template` | string | No | Template for generating status_list_url per credential |

## Constraints

1. `revocation_mechanism` MUST NOT be empty.
2. `check_mode: CACHED` MUST have `cache_ttl_seconds` set to a positive integer.
3. `check_mode: OFFLINE_GRACE` MUST have `offline_grace_seconds` set to a positive integer.
4. `check_mode: SKIP` MUST NOT be used for credentials with `compliance_code: ICAO_DTC`, `AAMVA_MDL`, or `EUDI_PID`.
5. `status_list_url` MUST be an absolute HTTPS URI if present.
6. `mechanism_priority`, if present, MUST be a non-empty subset of `revocation_mechanism`.

## Mechanism Selection

When multiple mechanisms are supported, the verifier selects the mechanism using:
1. `mechanism_priority` order (if defined)
2. Credential-embedded revocation endpoint (e.g., OCSP URL in X.509 cert)
3. First mechanism in `revocation_mechanism` (fallback)

## Example

### Online First, Cached Fallback

```json
{
  "id": "rp-online-first",
  "organization_id": "org-airline",
  "name": "Online-First Revocation",
  "revocation_mechanism": ["OCSP", "STATUS_LIST_2021"],
  "mechanism_priority": ["STATUS_LIST_2021", "OCSP"],
  "check_mode": "CACHED",
  "cache_ttl_seconds": 300,
  "offline_grace_seconds": 3600,
  "issuer_config": {
    "auto_allocate_index": true,
    "batch_update_interval_seconds": 60,
    "list_size": 131072
  },
  "created_at": "2026-03-11T00:00:00Z"
}
```

## See Also

- Root specification: [§12 Revocation Profile](../../SPECIFICATION.md#12-revocation-profile)
- Schema: [../../schemas/revocation-profile.json](../../schemas/revocation-profile.json)
- Enums: [../../enums/revocation-methods.json](../../enums/revocation-methods.json)
- Design: [DESIGN.md](./DESIGN.md)
