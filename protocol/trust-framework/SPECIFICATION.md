# Trust Framework — Entity Specification

**Entity:** TrustFramework
**Version:** 0.1.0
**Stability:** Stable
**Section in root spec:** §5.1

---

## Purpose

A Trust Framework defines the **shared cryptographic and regulatory rules** for an identity ecosystem (ICAO, AAMVA, EUDI, or custom). It is system-managed and immutable — organisations cannot modify it, only reference it via `OrganizationTrustProfile`.

The three-tier trust hierarchy:
```
TrustFramework (system, shared)
    └── OrganizationTrustProfile (org-specific overlay)
            └── TrustProfile (simplified API entity for consumers)
```

This separation ensures:
- **SHARED**: Framework definitions, global trust anchors, PKD endpoints → `TrustFramework`
- **ORG-SPECIFIC**: Selected framework, policy overrides, jurisdiction filters → `OrganizationTrustProfile`
- **API SURFACE**: Simplified trust configuration for issuance/verification callers → `TrustProfile`

## Properties

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `id` | UUID | Yes | Unique |
| `code` | string | Yes | SCREAMING_SNAKE_CASE; e.g. `ICAO`, `AAMVA`, `EUDI`, `CUSTOM` |
| `display_name` | string | Yes | 1–128 characters |
| `description` | string | No | Max 1024 characters |
| `pkd_endpoints` | object | No | Key-value map of named PKD/trust-list URLs |
| `default_algorithms` | string[] | Yes | Cryptographic algorithms mandated by this framework |
| `default_formats` | CredentialFormat[] | Yes | Credential formats mandated or recommended |
| `validation_ruleset` | object | No | Framework-specific validation rules (clock skew, chain depth, etc.) |
| `sync_config` | object | No | Periodic trust anchor refresh configuration |
| `is_system` | boolean | Yes | `true` = platform-managed; `false` = custom org-defined |
| `created_at` | datetime | Yes | ISO 8601 |

## System Frameworks

The following frameworks are system-provided (`is_system: true`) and cannot be modified:

| Code | Display Name | Primary Use |
|------|------|------|
| `ICAO` | ICAO Digital Travel Credentials | Passports, ePassports, travel authority verification |
| `AAMVA` | AAMVA Mobile Driver's License | US/CA driver's licenses, state IDs |
| `EUDI` | European Digital Identity Wallet | EU PID, mDL, and EUDI-compliant credentials |

Custom frameworks (`CUSTOM`) can be created by organisations.

## PKD Endpoints

The `pkd_endpoints` field maps logical names to URLs for automatic trust anchor synchronisation:

```json
{
  "pkd_endpoints": {
    "icao_pkd": "https://pkddownloadsg.icao.int/download",
    "aamva_iaca": "https://trust-list.aamva.org/current"
  }
}
```

## Relationship to OrganizationTrustProfile

An organisation creates an `OrganizationTrustProfile` that references a `TrustFramework.id`. The org profile may:
- Override `revocation_policy`, `time_policy`, `allowed_algorithms`, `allowed_formats`
- Add `allowed_issuers` / `denied_issuers` restrictions
- Set `jurisdiction_filter` to limit accepted credential origins

## Constraints

1. `code` values are globally unique and immutable after creation.
2. System frameworks (`is_system: true`) cannot be modified or deleted by organisations.
3. `default_algorithms` MUST contain at least one algorithm from `validation-algorithms` enum.
4. `default_formats` MUST contain at least one format from `credential-formats` enum.
