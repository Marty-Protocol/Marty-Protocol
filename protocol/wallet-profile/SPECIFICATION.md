# Wallet Profile - Entity Specification

**Entity:** Wallet Profile
**Version:** 0.4.0
**Stability:** Mixed (derived profiles: stable; override entries: mutable)
**Section in root spec:** §13

---

## Purpose

A Wallet Profile describes the requirements a holder wallet must satisfy for a credential configuration and, when supported by evidence, the named wallet applications verified for that exact configuration.

The derivation key is:

```text
(credential_format, issuance_protocol, compliance_profile_code) -> WalletRequirements
```

Derivation establishes requirements. It MUST NOT, by itself, assert that a named wallet is compatible. Format support, protocol support, platform availability, issuer enrollment, regional policy, certification, and an end-to-end issuance or presentation test are separate facts.

Organization-managed destinations such as Canvas Credentials institutional mirroring are Delivery Destination Profiles, not Wallet Profiles.

## Derived Requirements and Verified Compatibility

| Concern | Derived Requirements | Verified Compatibility Record |
|---|---|---|
| Source | Credential format, protocol, and compliance profile | Versioned system catalog evidence or organization override |
| Meaning | Capabilities a wallet would need | A named wallet demonstrated with the exact configuration |
| Named `wallet_apps` | Empty unless evidence exists | One or more evidence-backed names |
| Platforms | Empty unless evidence exists | Platforms covered by evidence |
| Mutability | Maintained with the protocol mapping | Updated as products and programs change |

An empty `wallet_apps` array means compatibility has not been verified. It does not mean every wallet is incompatible.

Evidence for a named wallet SHOULD identify:

- the exact credential format and document or credential type;
- the issuance and/or presentation protocol and version;
- the wallet product and platform version;
- issuer enrollment, entitlement, regional, or certification prerequisites;
- the test date, result, and authoritative documentation;
- whether evidence covers issuance, storage, presentation, or all three.

A documentation link alone is useful provenance but is not a substitute for an interoperability result when the system presents the mapping as verified.

## Override Registry

Organizations MAY store evidence-backed entries in `/v1/wallet-registry` for proprietary or deployment-specific wallets.

1. An override MUST set `is_override: true`.
2. It MUST include `id` and `organization_id`.
3. Its derivation key MUST match the credential configuration.
4. `APPEND` unions array fields; `REPLACE` replaces the derived requirement result.
5. An override that names a wallet MUST carry documentation and SHOULD carry test evidence in the implementation's evidence store.
6. Overrides are organization-scoped and MUST NOT become global compatibility claims.

## Properties

| Property | Type | Required | Description |
|---|---|---|---|
| `id` | UUID | Overrides | Stored override identifier |
| `organization_id` | UUID | Overrides | Owning organization |
| `is_override` | boolean | No | `true` for stored organization records |
| `override_precedence` | integer | No | Merge priority from 0 through 100 |
| `name` | string | Yes | Requirement or verified-compatibility label |
| `description` | string | No | Scope and evidence limitations |
| `credential_format` | CredentialFormat | Yes | Derivation key dimension |
| `issuance_protocol` | IssuanceProtocol | Yes | Derivation key dimension |
| `compliance_profile_code` | string | No | Optional narrowing dimension |
| `wallet_apps` | string[] | No | Evidence-backed compatible wallet names; empty when unverified |
| `merge_strategy` | string | No | `APPEND` or `REPLACE` |
| `specifications` | string[] | No | Required or tested standards |
| `supported_platforms` | Platform[] | No | Evidence-backed platforms |
| `deep_link_pattern` | string | No | Tested credential-offer route, when applicable |
| `docs_url` | URI | No | Authoritative product or program documentation |
| `created_at` | datetime | Overrides | Record creation time |
| `updated_at` | datetime | No | Last review time |

## Baseline Derivation Rules

| Credential configuration | Derived result |
|---|---|
| `MDOC` + `AAMVA_MDL` | ISO/IEC 18013-5 and AAMVA profile requirements; no default issuance protocol or named wallet |
| `MDOC` + `EUDI_MDL` | Version-pinned EUDI mDL requirements; no named wallet until the exact profile is mapped and tested |
| OID4VCI credential configuration | OID4VCI offer and proof requirements for the exact wire format; named wallets require evidence |
| Organization-specific wallet | Organization override scoped to its tested configuration |

MIP does not define a normative Apple Wallet, Google Wallet, or generic "any wallet" compatibility row. Those products have program-specific contracts and capabilities that can change independently of MIP.

## Deep Links

The `openid-credential-offer` URI identifies an OID4VCI offer. Its presence does not prove that a particular wallet accepts the credential configuration. A wallet-specific outer link or operating-system routing API MUST be recorded separately and tested without rewriting the signed or referenced inner offer.

ISO/IEC 18013-5 device engagement is a presentation bootstrap. It MUST NOT be represented as an HTTP issuance endpoint or an OID4VCI compatibility signal.

## API Surface

```text
GET    /v1/credential-templates/{id}/wallet-compatibility
GET    /v1/trust-profiles/{id}/wallet-compatibility
GET    /v1/wallet-registry
POST   /v1/wallet-registry
GET    /v1/wallet-registry/{id}
PUT    /v1/wallet-registry/{id}
PATCH  /v1/wallet-registry/{id}
DELETE /v1/wallet-registry/{id}
```

The compatibility endpoints MUST distinguish an unverified requirement result from a verified named-wallet result. They MUST NOT synthesize named wallets or platforms for an unknown derivation key.

## See Also

- Root specification: [Section 13 Wallet Profile](../../SPECIFICATION.md#13-wallet-profile)
- Credential Template: [../credential-template/SPECIFICATION.md](../credential-template/SPECIFICATION.md)
- Compliance Profile: [../compliance-profile/SPECIFICATION.md](../compliance-profile/SPECIFICATION.md)
- Design notes: [DESIGN.md](./DESIGN.md)
