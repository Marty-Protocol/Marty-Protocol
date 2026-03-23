# Compliance Profile — Entity Specification

**Entity:** Compliance Profile
**Version:** 0.1.0
**Stability:** Stable (system profiles), Moderate (custom)
**Section in root spec:** §10

---

## Purpose

A Compliance Profile abstracts **credential format complexity** behind compliance-oriented identifiers. Users choose a compliance framework (`ICAO_DTC`, `AAMVA_MDL`, `EUDI_PID`), not an encoding format (`MDOC`, `SD_JWT_VC`). Compliance Profiles make it possible to compare "does this credential conform to AAMVA?" without understanding mDoc encoding internals.

## What It Contains

| Dimension | Description |
|-----------|-------------|
| Compliance Code | The recognized standard or framework |
| Credential Format | Technical encoding (mdoc, sd_jwt_vc, vc_jwt, json_ld) |
| Issuance Protocol | How credentials are delivered |
| Artifact Requirements | What keys, certs, or DIDs are needed |
| Verification Defaults | Format-specific verification rules |

## Properties

### Core Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `id` | UUID | Yes | Unique |
| `organization_id` | UUID | No | Null for system profiles |
| `compliance_code` | ComplianceCode | Yes | From `compliance-codes` enum |
| `name` | string | Yes | 1–128 characters |
| `description` | string | No | Max 1024 characters |
| `credential_format` | CredentialFormat | Yes | From `credential-formats` enum |
| `issuance_protocol` | IssuanceProtocol | No | From `issuance-protocols` enum |
| `issuer_artifact_requirements` | ArtifactRequirements | No | See below |
| `default_verification_rules` | object | No | Format-specific overrides |
| `trust_profile_constraints` | object | No | Trust requirements for this format |
| `is_system` | boolean | Yes | System vs. organization-custom |
| `created_at` | datetime | Yes | ISO 8601 |

### ArtifactRequirements Fields

| Property | Type | Description |
|----------|------|-------------|
| `requires_x509_cert` | boolean | Requires X.509 issuer certificate |
| `requires_did` | boolean | Requires issuer DID |
| `requires_jwk` | boolean | Requires JSON Web Key |
| `cert_key_usage` | string[] | Required X.509 key usages (e.g., `digitalSignature`) |
| `recommended_algorithms` | Algorithm[] | Recommended signing algorithms |

## System Profiles (Normative)

System profiles are read-only and pre-installed. They cannot be modified or deleted.

| Profile ID | Code | Format | Protocol | Description |
|------------|------|--------|----------|-------------|
| `cp-icao-dtc` | `ICAO_DTC` | `MDOC` | `OID4VCI_PRE_AUTH` | ICAO Digital Travel Credential |
| `cp-aamva-mdl` | `AAMVA_MDL` | `MDOC` | `OID4VCI_PRE_AUTH` | AAMVA Mobile Driver's License |
| `cp-eudi-pid` | `EUDI_PID` | `SD_JWT_VC` | `OID4VCI_PRE_AUTH` | EUDI Personal Identification Data |
| `cp-eudi-mdl` | `EUDI_MDL` | `MDOC` | `OID4VCI_PRE_AUTH` | EUDI Mobile Driving Licence |
| `cp-ob3-jwt` | `OB3_JWT` | `VC_JWT` | `OID4VCI_PRE_AUTH` | Open Badge v3 (JWT encoding) |
| `cp-ob3-jsonld` | `OB3_JSONLD` | `JSON_LD` | `OID4VCI_PRE_AUTH` | Open Badge v3 (JSON-LD) |
| `cp-sd-jwt-vc` | `SD_JWT_VC` | `SD_JWT_VC` | `OID4VCI_PRE_AUTH` | Generic SD-JWT VC |
| `cp-enterprise-vc` | `ENTERPRISE_VC` | `VC_JWT` | `OID4VCI_PRE_AUTH` | Generic Enterprise VC (JWT) |
| `cp-icao-mrz` | `ICAO_MRZ` | `MDOC` | — | ICAO Machine Readable Zone (MRZ) |
| `cp-oid4vc` | `OID4VC` | `SD_JWT_VC` | `OID4VCI_PRE_AUTH` / `OID4VCI_AUTH_CODE` | Generic OpenID4VC Interop (OIDF certification target) |
| `cp-pex-v2` | `PEX` | `SD_JWT_VC` | — | DIF Presentation Exchange v2 (verifier-side) |

## Constraints

1. System profiles (`is_system: true`) MUST NOT be modified or deleted.
2. `organization_id` MUST be null for system profiles.
3. Custom profiles with `compliance_code: CUSTOM` MUST have `organization_id` set.
4. `credential_format` and `compliance_code` combinations MUST be internally consistent (e.g., `ICAO_DTC` requires `MDOC`).
5. A Compliance Profile is immutable once referenced by an `ACTIVE` Credential Template.

## Format–Code Compatibility Matrix

| `compliance_code` | Required `credential_format` |
|-------------------|------------------------------|
| `ICAO_DTC` | `MDOC` |
| `AAMVA_MDL` | `MDOC` |
| `EUDI_PID` | `SD_JWT_VC` |
| `EUDI_MDL` | `MDOC` |
| `OB3_JWT` | `VC_JWT` |
| `OB3_JSONLD` | `JSON_LD` |
| `SD_JWT_VC` | `SD_JWT_VC` |
| `ENTERPRISE_VC` | `VC_JWT` or `SD_JWT_VC` |
| `ICAO_MRZ` | `MDOC` |
| `OID4VC` | `SD_JWT_VC` (also compatible with `VC_JWT`, `MDOC`) |
| `PEX` | `SD_JWT_VC` (also compatible with `VC_JWT`, `JSON_LD`, `MDOC`) |
| `CUSTOM` | Any |

## API Surface

The `api_surface` property declares the HTTP endpoints that a MIP implementation MUST expose when an organization activates a credential type governed by this profile. This is the mechanism by which OID4VCI well-known metadata, proximity session endpoints, and revocation feed endpoints are derived from the profile rather than hardcoded.

### Endpoint Descriptor Fields

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `rel` | string | Yes | IANA link relation or MIP-defined endpoint identifier |
| `path_template` | string | No | Global (non-org-scoped) URL path, e.g. `/.well-known/openid-credential-issuer` |
| `org_scoped_path` | string | No | Per-org variant, e.g. `/org/{org_id}/.well-known/openid-credential-issuer` |
| `method` | string | Yes | HTTP method: `GET`, `POST`, `PUT`, `PATCH`, or `DELETE` |
| `auth_required` | boolean | No | Whether the endpoint requires Bearer token auth. Default: `false` |
| `discoverable` | boolean | No | Whether this endpoint appears in `/.well-known/mip-configuration`. Default: `true` |
| `standard_ref` | string | No | Human-readable reference to the defining standard and section |
| `response_schema_ref` | URI | No | URI of the JSON Schema describing the response body |

### Normative Requirements

1. An implementation activating a credential type MUST expose all endpoints declared in `api_surface` for the governing compliance profile.
2. Endpoints where `discoverable: true` MUST appear in the `/.well-known/mip-configuration` response for the issuer or org.
3. Global `path_template` endpoints are served at the platform root. Org-scoped `org_scoped_path` endpoints are additionally served per-organization.
4. If both `path_template` and `org_scoped_path` are present, both MUST be exposed.
5. System profile `api_surface` arrays are normative and MUST NOT be overridden by implementations.

### Well-Known Discovery: `/.well-known/mip-configuration`

A MIP-compliant deployment MUST expose a `GET /.well-known/mip-configuration` endpoint. The response is a JSON object whose keys are endpoint `rel` values and whose values are the resolved URLs for that endpoint:

```json
{
  "openid-credential-issuer-metadata": "https://issuer.example.com/.well-known/openid-credential-issuer",
  "token": "https://issuer.example.com/v1/issuance/token",
  "credential": "https://issuer.example.com/v1/issuance/credential",
  "nonce": "https://issuer.example.com/v1/issuance/nonce",
  "deferred-credential": "https://issuer.example.com/v1/issuance/deferred-credential"
}
```

For per-organization endpoints, the `/.well-known/mip-configuration` response MAY include an `org_endpoints` array in which each entry has an `org_id` key alongside the resolved URLs.

### Standard `rel` Values

| `rel` | Standard Reference | Meaning |
|-------|-------------------|---------|
| `openid-credential-issuer-metadata` | OID4VCI §11.2.3 | OID4VCI issuer metadata document |
| `token` | RFC 6749 §3.2 / OID4VCI §6 | OAuth2 token endpoint |
| `credential` | OID4VCI §7 | Credential issuance endpoint |
| `nonce` | OID4VCI §8 | Nonce endpoint |
| `deferred-credential` | OID4VCI §9 | Deferred credential retrieval |
| `notification` | OID4VCI §10 | Holder notification endpoint |
| `status-list` | IETF Token Status List | Revocation status list endpoint |
| `device-engagement` | ISO/IEC 18013-5:2021 §8.2.1 | mDoc device engagement (QR/NFC) |
| `session-establishment` | ISO/IEC 18013-5:2021 §8.3 | mDoc proximity session establishment |

## Cross-References

| Referencing Entity | Reference Field | Behavior |
|--------------------|-----------------|----------|
| Credential Template | `compliance_profile_id` | Required — determines format |
| Wallet Profile | (derivation input) | Used to look up compatible wallets |

## Examples

### Organization Custom Profile

```json
{
  "id": "cp-custom-employee",
  "organization_id": "org-enterprise",
  "compliance_code": "ENTERPRISE_VC",
  "name": "Enterprise Employee Badge",
  "credential_format": "SD_JWT_VC",
  "issuance_protocol": "OID4VCI_PRE_AUTH",
  "issuer_artifact_requirements": {
    "requires_jwk": true,
    "recommended_algorithms": ["ES256"]
  },
  "is_system": false,
  "created_at": "2026-03-11T00:00:00Z"
}
```

## See Also

- Root specification: [§10 Compliance Profile](../../SPECIFICATION.md#10-compliance-profile)
- Schema: [../../schemas/compliance-profile.json](../../schemas/compliance-profile.json)
- Enums: [../../enums/compliance-codes.json](../../enums/compliance-codes.json), [../../enums/credential-formats.json](../../enums/credential-formats.json)
- Design: [DESIGN.md](./DESIGN.md)
