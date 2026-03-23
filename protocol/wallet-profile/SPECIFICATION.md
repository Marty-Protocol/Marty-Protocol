# Wallet Profile — Entity Specification

**Entity:** Wallet Profile
**Version:** 0.1.0
**Stability:** Mixed (derived profiles: stable; override entries: mutable)
**Section in root spec:** §13

---

## Purpose

A Wallet Profile describes **which wallet applications can receive and hold** a specific credential configuration. The canonical set of wallet profiles is **derived** from the combination of credential format, issuance protocol, and compliance profile code. However, organisations with specialised deployment requirements MAY store **override entries** in the wallet registry to extend or customise derived profiles.

---

## Derivation vs. Override

| Aspect | Derived Profile | Override Entry |
|--------|----------------|----------------|
| Source | System derivation table | Operator-stored, per-organisation |
| `is_override` | `false` (implied) | `true` |
| `id` / `organization_id` | Absent | Required |
| Persistence | None — computed on read | Stored in `/v1/wallet-registry` |
| Mutability | Immutable | Full CRUD |
| Precedence | 0 (lowest) | Configurable (`override_precedence`, default 50) |

---

## Derivation Key

```
(credential_format, issuance_protocol, compliance_profile_code) → DerivedWalletProfile
```

This key is extracted from a Credential Template's associated Compliance Profile. Multiple Credential Templates that share the same key produce the same derived profile.

---

## Override Registry

Organisations that need to extend the standard wallet compatibility set — for example, to add a proprietary enterprise wallet, adjust deep link patterns, or restrict the default platform list — may POST override entries to `/v1/wallet-registry`.

### Merge Semantics

When `GET /v1/wallet-registry` is called (or when wallet compatibility is resolved for a credential template), the system produces a merged result:

1. Start with the system-derived profile for the matching derivation key.
2. Find all stored override entries for the organisation that match the same derivation key.
3. Sort overrides by `override_precedence` descending (highest first).
4. For each override:
   - If `merge_strategy = APPEND`: array fields (`wallet_apps`, `specifications`) are unioned; scalar fields from the override replace derived values.
   - If `merge_strategy = REPLACE`: all fields from the override replace corresponding derived fields entirely.
5. Return the merged profile.

If no override entries exist for a given derivation key, the derived profile is returned as-is.

### Override Constraints

1. An override MUST set `is_override: true`.
2. An override MUST include `id` and `organization_id`.
3. An override MUST NOT contradict the `credential_format` of the referenced compliance profile (the derivation key is immutable within an override entry).
4. Overrides are scoped to the creating organisation; they do not affect other organisations' derived profiles.

---

## Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | For overrides | Stored override identifier |
| `organization_id` | UUID | For overrides | Owning organisation |
| `is_override` | boolean | No | Default `false`; `true` for stored entries |
| `override_precedence` | integer | No | Merge priority 0–100; default 50 |
| `name` | string | Yes | Human-readable profile name |
| `description` | string | No | Capability description |
| `credential_format` | CredentialFormat | Yes | Primary key dimension |
| `issuance_protocol` | IssuanceProtocol | Yes | Primary key dimension |
| `compliance_profile_code` | string | No | Optional key dimension |
| `wallet_apps` | string[] | No | Compatible wallet application names |
| `merge_strategy` | string | No | `APPEND` or `REPLACE`; default `APPEND` |
| `specifications` | string[] | No | Supported standards |
| `supported_platforms` | Platform[] | No | `ios`, `android`, `web` |
| `deep_link_pattern` | string | No | URI template for credential offer delivery |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

---

## Compatibility Table (Normative — Derived Profiles)

| `credential_format` | `issuance_protocol` | `compliance_profile_code` | Compatible Wallets | Platforms |
|--------------------|--------------------|--------------------------|-------------------|-----------|
| `MDOC` | `OID4VCI_PRE_AUTH` | `AAMVA_MDL` | Apple Wallet (mDL), Google Wallet (mDL), ISO mDL wallets | ios, android |
| `MDOC` | `OID4VCI_PRE_AUTH` | `ICAO_DTC` | ICAO DTC-compliant wallets | ios, android |
| `MDOC` | `OID4VCI_PRE_AUTH` | `EUDI_MDL` | EUDI Wallet, eIDAS wallets | ios, android, web |
| `SD_JWT_VC` | `OID4VCI_PRE_AUTH` | `EUDI_PID` | EUDI Wallet, eIDAS wallets | ios, android, web |
| `SD_JWT_VC` | `OID4VCI_PRE_AUTH` | null | EUDI Wallet, OID4VCI-compatible wallets | ios, android, web |
| `VC_JWT` | `OID4VCI_PRE_AUTH` | `OB3_JWT` | 1EdTech Open Badge Passport, Learning Credential Wallet | ios, android, web |
| `JSON_LD` | `OID4VCI_PRE_AUTH` | `OB3_JSONLD` | 1EdTech Open Badge Passport, DIF Universal Wallet | ios, android, web |
| `VC_JWT` | `OID4VCI_PRE_AUTH` | `ENTERPRISE_VC` | Organization-managed wallets | ios, android, web |

---

## Deep Link Patterns (Normative)

| Format | Deep Link Pattern |
|--------|------------------|
| `MDOC` + Apple/Google | `openid-credential-offer://?credential_offer_uri={offer_uri}` |
| `SD_JWT_VC` + EUDI | `openid-credential-offer://?credential_offer_uri={offer_uri}` |
| `VC_JWT` + generic | `openid-credential-offer://?credential_offer_uri={offer_uri}` |

---

## API Surface

### Derivation Endpoints (Read-Only)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/v1/credential-templates/{id}/wallet-compatibility` | Merged wallet profile for a credential template |
| `GET` | `/v1/trust-profiles/{id}/wallet-compatibility` | Merged wallet profile for a trust profile |

### Override Registry Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/v1/wallet-registry` | List all override entries for the authenticated organisation (merged with derived) |
| `POST` | `/v1/wallet-registry` | Create a new override entry (`is_override` forced to `true`) |
| `GET` | `/v1/wallet-registry/{id}` | Get a specific override entry |
| `PUT` | `/v1/wallet-registry/{id}` | Replace an override entry |
| `PATCH` | `/v1/wallet-registry/{id}` | Partially update an override entry |
| `DELETE` | `/v1/wallet-registry/{id}` | Delete an override entry (reverts to derived profile) |

### Response Format Example

```json
{
  "derived_from": {
    "credential_format": "MDOC",
    "issuance_protocol": "OID4VCI_PRE_AUTH",
    "compliance_profile_code": "AAMVA_MDL"
  },
  "is_override": false,
  "name": "AAMVA mDL Wallet",
  "wallet_apps": ["Apple Wallet (mDL)", "Google Wallet (mDL)"],
  "specifications": ["ISO 18013-5", "ISO 23220-3", "OID4VCI"],
  "supported_platforms": ["ios", "android"],
  "deep_link_pattern": "openid-credential-offer://?credential_offer_uri={offer_uri}"
}
```

---

## See Also

- Root specification: [§13 Wallet Profile](../../SPECIFICATION.md#13-wallet-profile)
- Credential Template: [../credential-template/SPECIFICATION.md](../credential-template/SPECIFICATION.md)
- Compliance Profile: [../compliance-profile/SPECIFICATION.md](../compliance-profile/SPECIFICATION.md)


---

## Purpose

A Wallet Profile describes **which wallet applications can receive and hold** a specific credential configuration. It is derived from the combination of credential format, issuance protocol, and compliance profile code — it is **not independently stored or created**.

## Derivation Key

```
(credential_format, issuance_protocol, compliance_profile_code) → WalletProfile
```

This key is extracted from a Credential Template's associated Compliance Profile.

## Why Derived, Not Stored

Wallet compatibility is a property of the **format × protocol × compliance framework** combination, not something operators configure. Storing it independently would lead to drift between what the system says is compatible and what is actually compatible. The derivation table is maintained by protocol implementers, not end users.

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Human-readable profile name |
| `description` | string | Capability description |
| `credential_format` | CredentialFormat | Primary key dimension |
| `issuance_protocol` | IssuanceProtocol | Primary key dimension |
| `compliance_profile_code` | string | Optional key dimension; narrows compatibility |
| `wallet_apps` | string[] | Compatible wallet application names |
| `specifications` | string[] | Supported standards |
| `supported_platforms` | Platform[] | `ios`, `android`, `web` |
| `deep_link_pattern` | string | URI template for credential offer delivery |

## Compatibility Table (Normative)

| `credential_format` | `issuance_protocol` | `compliance_profile_code` | Compatible Wallets | Platforms |
|--------------------|--------------------|--------------------------|-------------------|-----------|
| `MDOC` | `OID4VCI_PRE_AUTH` | `AAMVA_MDL` | Apple Wallet (mDL), Google Wallet (mDL), ISO mDL wallets | ios, android |
| `MDOC` | `OID4VCI_PRE_AUTH` | `ICAO_DTC` | ICAO DTC-compliant wallets | ios, android |
| `MDOC` | `OID4VCI_PRE_AUTH` | `EUDI_MDL` | EUDI Wallet, eIDAS wallets | ios, android, web |
| `SD_JWT_VC` | `OID4VCI_PRE_AUTH` | `EUDI_PID` | EUDI Wallet, eIDAS wallets | ios, android, web |
| `SD_JWT_VC` | `OID4VCI_PRE_AUTH` | null | EUDI Wallet, OID4VCI-compatible wallets | ios, android, web |
| `VC_JWT` | `OID4VCI_PRE_AUTH` | `OB3_JWT` | 1EdTech Open Badge Passport, Learning Credential Wallet | ios, android, web |
| `JSON_LD` | `OID4VCI_PRE_AUTH` | `OB3_JSONLD` | 1EdTech Open Badge Passport, DIF Universal Wallet | ios, android, web |
| `VC_JWT` | `OID4VCI_PRE_AUTH` | `ENTERPRISE_VC` | Organization-managed wallets | ios, android, web |

## Deep Link Pattern

Wallet compatibility includes the credential offer delivery URI format:

| Format | Deep Link Pattern |
|--------|------------------|
| `MDOC` + Apple/Google | `openid-credential-offer://?credential_offer_uri={offer_uri}` |
| `SD_JWT_VC` + EUDI | `openid-credential-offer://?credential_offer_uri={offer_uri}` |
| `VC_JWT` + generic | `openid-credential-offer://?credential_offer_uri={offer_uri}` |

## API Endpoints (Read-Only)

```
GET /v1/credential-templates/{id}/wallet-compatibility
GET /v1/trust-profiles/{id}/wallet-compatibility
```

### Response Format

```json
{
  "derived_from": {
    "credential_format": "MDOC",
    "issuance_protocol": "OID4VCI_PRE_AUTH",
    "compliance_profile_code": "AAMVA_MDL"
  },
  "name": "AAMVA mDL Wallet",
  "wallet_apps": [
    "Apple Wallet (mDL)",
    "Google Wallet (mDL)"
  ],
  "specifications": [
    "ISO 18013-5",
    "ISO 23220-3",
    "OID4VCI"
  ],
  "supported_platforms": ["ios", "android"],
  "deep_link_pattern": "openid-credential-offer://?credential_offer_uri={offer_uri}"
}
```

## See Also

- Root specification: [§13 Wallet Profile](../../SPECIFICATION.md#13-wallet-profile)
- Credential Template: [../credential-template/SPECIFICATION.md](../credential-template/SPECIFICATION.md)
- Compliance Profile: [../compliance-profile/SPECIFICATION.md](../compliance-profile/SPECIFICATION.md)
- Design: [DESIGN.md](./DESIGN.md)
