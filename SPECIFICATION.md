# Marty Identity Protocol — Normative Specification

**Version:** 0.1.0
**Status:** Draft
**Date:** 2026-03-11
**Organization:** The MIP Authors

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Terminology](#2-terminology)
3. [Design Principles](#3-design-principles)
4. [Protocol Overview](#4-protocol-overview)
5. [Trust Profile](#5-trust-profile)
6. [Credential Template](#6-credential-template)
7. [Presentation Policy](#7-presentation-policy)
8. [Deployment Profile](#8-deployment-profile)
9. [Flow](#9-flow)
10. [Compliance Profile](#10-compliance-profile)
11. [Application Template](#11-application-template)
12. [Revocation Profile](#12-revocation-profile)
13. [Wallet Profile](#13-wallet-profile)
14. [Device Registration](#14-device-registration)
15. [Notification Target](#15-notification-target)
16. [Policy Set (Cedar)](#16-policy-set-cedar)
17. [API Surface](#17-api-surface)
18. [Organization & Identity Governance](#18-organization--identity-governance)
19. [Validation Rules](#19-validation-rules)
20. [Security Considerations](#20-security-considerations)
21. [Privacy Considerations](#21-privacy-considerations)
22. [Conformance](#22-conformance)
23. [Versioning](#23-versioning)
24. [Transport Bindings](#24-transport-bindings)
25. [Governance](#25-governance)
26. [Message Layer](#26-message-layer)

---

## 1. Introduction

The Marty Identity Protocol (MIP) is a formal specification for **cryptographically verifiable digital identity management**. MIP defines the minimum automatable set of primitives required for issuing, holding, and presenting digital credentials under explicit rules of trust and disclosure.

MIP standardizes a vendor-neutral model for cryptographically verifiable digital identity management. It is designed to align with and compose cleanly with:

- **ISO/IEC 18013-5:2021** (Mobile Driving License / mDoc)
- **ICAO Doc 9303** and the ICAO Digital Travel Credential (DTC) specification
- **OpenID for Verifiable Credential Issuance (OID4VCI)**
- **OpenID for Verifiable Presentations (OID4VP)**
- **W3C Verifiable Credentials Data Model**
- **IETF SD-JWT-VC**
- **EUDI Wallet Architecture and Reference Framework (ARF)**

MIP's trust model is intentionally infrastructure-neutral. The `TrustSource` abstraction (§5.3) and the extension mechanism (§25.2) are designed so that alternative identifier and key-event infrastructures — including event-sourced identifier systems such as [KERI (Key Event Receipt Infrastructure)](https://keri.one/) — can be expressed as custom trust sources without modification to normative protocol text.

### 1.1 Scope

MIP specifies:

- The data model and constraints for 11 protocol entities
- The relationships between those entities
- API resource naming and endpoint conventions
- Validation rules for each entity
- Conformance requirements for implementations
- Controlled vocabularies (enumerations)

MIP does **not** specify:

- Transport-level security (use TLS 1.3+)
- Authentication of API calls (use OAuth 2.0 / OIDC)
- Specific cryptographic algorithm implementations
- Key management infrastructure internals

### 1.2 Notational Conventions

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

JSON Schemas for all entities are in `/schemas/`. When normative text and a schema conflict, this specification takes precedence.

---

## 2. Terminology

**Claim**
A statement about a subject (e.g., `age_over_21: true`, `document_number: "X1234567"`).

**Credential**
A signed set of claims about a subject, issued by an authority and cryptographically bound.

**Credential Format**
The technical encoding of a credential. Examples: `mdoc`, `sd_jwt_vc`, `vc_jwt`, `ldp_vc`.

**Holder**
An entity that stores and presents credentials (typically a wallet application or device).

**Issuance Protocol**
The protocol used to deliver a credential from issuer to holder. Example: OID4VCI pre-authorized code flow.

**Issuer**
An entity that signs and issues credentials.

**Lane**
A logical grouping of devices within a Deployment Profile (e.g., "Gate 12", "Checkpoint North").

**Predicate**
A zero-knowledge proof that a claim satisfies a condition without revealing the raw value (e.g., `age >= 21` without revealing date of birth).

**Presentation**
A set of claims or proofs shared by a holder in response to a Presentation Policy request.

**Relying Party**
An entity that makes a decision based on a verified presentation (e.g., grants boarding, permits purchase).

**Trust Anchor**
A cryptographic root of trust (e.g., CSCA certificate, root CA) from which issuer trust is derived.

**Verifier**
An entity that evaluates a presentation against a Presentation Policy.

**Applicant**
A person or entity who has submitted a credential application through an `application_approval_issuance` Flow. An Applicant has a distinct lifecycle from a platform user account (SCIM User) and MUST NOT be conflated with it.

**Flow Instance**
A single execution of a Flow Definition. Each Flow Instance tracks state transitions, step results, and audit events for one atomic identity operation (one issuance, one verification, etc.).

**Governance Framework**
The set of policies, trust anchors, compliance profiles, and ecosystem rules that define what credentials are accepted within a jurisdiction or ecosystem (e.g., EUDI Trust Framework, AAMVA mDL Framework).

**Nonce**
A cryptographically random, single-use value used to prevent replay attacks in credential issuance (OID4VCI `c_nonce` for holder binding proofs) and presentation challenge-response. MUST be at minimum 128 bits of entropy, base64url-encoded.

**Proximity Protocol**
A short-range transport for credential exchange. In MIP, this refers to ISO 18013-5 Part 8 BLE/NFC engagement between a reader device and a holder wallet.

**Session**
A transient, cryptographically bound context established between two parties for a single protocol exchange (e.g., an ISO 18013-5 engagement session with its own session encryption keys).

**Status List**
A compact bitstring representation of credential revocation status as defined in IETF Bitstring Status List (draft-ietf-oauth-status-list) and W3C Status List 2021.

**Trust Framework**
A policy and governance framework that defines the rules under which issuers, holders, and verifiers operate within an identity ecosystem.

**Wallet**
A software application (mobile, web, or hardware) that stores credentials on behalf of a Holder, manages bound key material, enforces holder consent, and generates presentations in response to Verifier requests.

---

## 3. Design Principles

### 3.1 Policies Are Data

Verification behavior MUST be driven by Presentation Policy configuration, not by hardcoded logic. Changing what is verified requires updating a policy object, not modifying code.

### 3.2 Authorization Is Formally Verifiable

Access control, credential verification trust, and approval rules MUST be expressed in the [Cedar policy language](https://www.cedarpolicy.com/) via PolicySet entities (§16). Cedar policies are deny-by-default, statically analyzable, and auditable. Opaque JSON rule objects MUST NOT be used for new authorization decisions.

### 3.2 Trust Is Explicit

Every Trust Profile MUST explicitly enumerate its trust sources. Implicit trust of "any recognized authority" is prohibited. Trust decisions are auditable.

### 3.3 Disclosure Is Minimal

Presentation Policies MUST specify the minimum required claims. Implementations MUST prefer selective disclosure and predicates over raw claim values wherever the credential format supports it.

### 3.4 Deployment Is Declarative

Device and endpoint behavior MUST be driven by Deployment Profile configuration. Physical deployments do not contain business logic.

### 3.5 Flows Make Identity Automatable

All identity operations (issuance, presentation, approval) MUST be expressible as Flows with defined state transitions, enabling automation, audit, and retry.

### 3.6 Compliance Is Abstracted

Credential format complexity (mdoc vs. SD-JWT-VC vs. VC-JWT) MUST be hidden behind Compliance Profiles. Users select compliance standards, not encoding details.

---

## 4. Protocol Overview

### 4.1 Entity Relationship

```
Organization
    │
    ├── Trust Profile
    │       └── Revocation Profile (reference)
    │
    ├── Compliance Profile
    │
    ├── Application Template (optional — user-facing workflow)
    │
    ├── Credential Template (master issuance config)
    │       ├── compliance_profile_id → Compliance Profile
    │       ├── application_template_id → Application Template (optional)
    │       ├── trust_profile_id → Trust Profile (optional)
    │       └── revocation_profile_id → Revocation Profile (optional)
    │
    ├── Presentation Policy
    │       └── trust_profile_id → Trust Profile
    │
    ├── Deployment Profile
    │       ├── trust_profile_id → Trust Profile
    │       ├── presentation_policy_ids → [Presentation Policy]
    │       └── Lanes → [Devices]
    │
    ├── Flow
    │       ├── trust_profile_id → Trust Profile
    │       ├── credential_template_id → Credential Template (issuance)
    │       ├── presentation_policy_id → Presentation Policy (verification)
    │       └── deployment_profile_ids → [Deployment Profile]
    │
    ├── Policy Set (Cedar)
    │       └── cedar_policies[] → Cedar permit/forbid rules
    │
    ├── Wallet Profile (derived from Credential Template + Compliance Profile)
    │
    └── Device Registration
            └── Notification Target (references device tokens)

Policy Set references (Cedar):
    Trust Profile       → verification_policy_set_id → Policy Set
    Compliance Profile  → verification_policy_set_id → Policy Set
    Application Template→ approval_policy_set_id     → Policy Set
    SCIM Role           → policy_set_id              → Policy Set
```

### 4.2 Issuance Flow (High-Level)

```
1. Credential Template defined (schema + compliance + crypto)
2. Application Template defined (forms + evidence — optional)
3. Flow created (links TP + CT + DP)
4. Holder submits Application (if application-based)
5. Application approved (auto/manual/rules-based)
6. Issuance triggered → credential signed using CT crypto config
7. Credential delivered to Holder wallet (via OID4VCI or direct)
8. Device Notification sent (if Device Registration exists)
```

### 4.3 Verification Flow (High-Level)

```
1. Presentation Policy defined (required claims + trust constraints)
2. Deployment Profile packages Policy + Trust + UX
3. Verifier initiates Flow instance
4. Holder receives Presentation Request (via OID4VP or proximity)
5. Holder selects matching credential(s)
6. Holder sends Presentation Response
7. Verifier validates: trust chain + crypto + revocation + policy
8. Relying Party receives pass/fail + audit event
```

### 4.4 OID4VCI Pre-Authorized Issuance Sequence

```
 Issuer / Gateway          Holder Wallet
        |                        |
        |-- CredentialOffer ---->|  (QR / deep link / push notification)
        |                        |
        |<-- TokenRequest -------|  (pre-authorized_code grant)
        |-- TokenResponse ------>|  (access_token + c_nonce)
        |                        |
        |<-- CredentialRequest --|  (proof of holder binding using c_nonce)
        |-- CredentialResponse ->|  (signed credential or transaction_id)
        |                        |
        |<-- Notification -------|  (wallet stores credential; optional)
        |                        |
```

### 4.5 OID4VP Cross-Device Verification Sequence

```
 Relying Party    Verifier / Gateway       Holder Wallet
      |                   |                      |
      |-- Initiate ------->|                      |
      |                   |-- PresentationReq --->|  (QR / request_uri)
      |                   |                      |
      |                   |                      |-- select credential
      |                   |                      |-- compute proof
      |                   |<-- PresentationResp--|  (vp_token)
      |                   |                      |
      |                   |-- trust eval -------->|  (internal: §5.7.3)
      |                   |-- revocation check -->|  (internal: §20.7)
      |                   |                      |
      |<-- VerificationResult ---|               |
      |                   |                      |
```

### 4.6 ISO 18013-5 Proximity mDL Sequence

```
  Reader (Verifier)          Holder Device
        |                         |
        |-- DeviceEngagement ----->|  (QR code displayed by reader or NFC tap)
        |<-- SessionEstablishment -|  (session keys negotiated per ISO 18013-5 §8.3)
        |                         |
        |-- DeviceRequest -------->|  (namespace + data elements requested)
        |<-- DeviceResponse -------|  (signed mDoc response, selective disclosure)
        |                         |
        |-- SessionTermination --->|  (close session)
        |                         |
        |-- verify mdoc ---------->|  (internal: trust chain + signature + revocation)
```

### 4.7 Application-Approval Issuance Sequence

```
  Applicant         Gateway / Issuer        Reviewer
      |                    |                    |
      |-- ApplicationSubmission -->|            |
      |                    |                    |
      |                    |-- route to queue -->|
      |<-- evidence req ---|                    |
      |-- EvidenceSubmission ->|                |
      |                    |-- notify reviewer ->|
      |                    |                    |
      |                    |<-- ApplicantDecision (APPROVED)
      |                    |                    |
      |                    |-- issue credential (OID4VCI pre-auth)
      |<-- CredentialOffer -|                    |
      |                    |                    |
```

---

## 5. Trust Profile

**Stability:** Stable | **Owned by:** Security / Admin

### 5.1 Purpose

A Trust Profile defines **who is trusted** and **how cryptographic validation occurs**. It is the security root for all issuance and verification operations that reference it.

### 5.2 Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Unique identifier |
| `organization_id` | UUID | Yes | Owning organization |
| `name` | string | Yes | Human-readable name |
| `description` | string | No | Optional description |
| `profile_type` | TrustProfileType | Yes | `ICAO`, `AAMVA`, `EUDI`, `CUSTOM` |
| `trust_sources` | TrustSource[] | Yes | One or more trust anchors |
| `allowed_algorithms` | Algorithm[] | Yes | Accepted cryptographic algorithms |
| `revocation_profile_id` | UUID | No | Reference to a RevocationProfile |
| `verification_policy_set_id` | UUID | No | Reference to a Cedar PolicySet (§16) for conditional trust evaluation |
| `time_policy` | TimePolicy | No | Clock skew, freshness windows |
| `supported_formats` | CredentialFormat[] | Yes | Accepted credential formats |
| `compliance_status` | ComplianceStatus | Yes | `COMPLIANT`, `NEEDS_ATTENTION`, `SETUP_REQUIRED` |
| `compatible_compliance_codes` | ComplianceCode[] | No | Compliance codes this profile can serve (e.g., `["EUDI_PID", "EUDI_MDL"]`). When absent, inferred from `profile_type`. |
| `auto_generated` | boolean | No | Whether auto-generated from use-case selection |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

### 5.3 TrustSource

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `source_type` | TrustSourceType | Yes | `TRUST_LIST`, `PINNED_ISSUER`, `ROOT_CA`, `PKD_URL` |
| `url` | string (URI) | No | Download URL for trust material |
| `certificate_pem` | string | No | Pinned root certificate (PEM) |
| `issuer_did` | string | No | Issuer DID for DID-based trust |
| `description` | string | No | Human-readable label |

Exactly one of `url`, `certificate_pem`, or `issuer_did` MUST be present for each TrustSource.

### 5.4 TimePolicy

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `clock_skew_seconds` | integer | 300 | Allowed clock skew |
| `max_credential_age_seconds` | integer | null | Maximum credential age (null = no limit) |
| `require_freshness` | boolean | false | Reject credentials not issued within freshness window |
| `freshness_window_seconds` | integer | null | If `require_freshness`, credentials older than this are rejected |

### 5.5 Validation Rules

- `trust_sources` MUST contain at least one entry.
- `allowed_algorithms` MUST contain at least one value from `validation-algorithms` enum.
- `supported_formats` MUST contain at least one value from `credential-formats` enum.
- A Trust Profile with `compliance_status: SETUP_REQUIRED` MUST NOT be used in an active Flow.
- `revocation_profile_id` MUST reference an existing RevocationProfile if present.

### 5.6 API

```
GET    /v1/trust-profiles
POST   /v1/trust-profiles
GET    /v1/trust-profiles/{id}
PATCH  /v1/trust-profiles/{id}
DELETE /v1/trust-profiles/{id}
GET    /v1/trust-profiles/{id}/wallet-compatibility
```

### 5.7 Trust Architecture

#### 5.7.1 Root of Trust Models

MIP supports two root-of-trust models, which may be combined within a single Trust Profile:

**PKI Model (X.509)**
Trust is anchored in a root Certificate Authority (CA) certificate (e.g., ICAO CSCA, AAMVA CA). The verifier obtains root certificates from a trust list or ICAO PKD, and validates the issuer certificate chain up to that root. Applicable to `ROOT_CA` and `TRUST_LIST` TrustSource entries.

**DID Model**
Trust is anchored in a DID Document published to a verifiable data registry. The verifier resolves the issuer DID, retrieves the issuer's public key from the DID Document, and validates the credential signature against that key. Applicable to `PINNED_ISSUER` TrustSource entries with `issuer_did` set.

**Event-Sourced Identifier Model (e.g., KERI)**
Trust may alternatively be anchored in a cryptographically verifiable key-event log rather than a static registry. [KERI (Key Event Receipt Infrastructure)](https://keri.one/) is a representative example: an issuer's authoritative key state is established and rotated through a self-contained, hash-chained log of signed key events (a KEL), witnessed and replicated independently of any ledger. A MIP implementation that supports this model would resolve the issuer's current key state from its Key Event Log in place of a DID Document lookup, then proceed with signature validation against that key state. This integration point is accommodated via a `CUSTOM` `source_type` `TrustSource` entry; see §25.2 for the extension mechanism.

**Hybrid Model**
A Trust Profile with both `ROOT_CA` and `PINNED_ISSUER` (DID) trust sources operates in hybrid mode. Validation against any one source is sufficient unless the Trust Profile requires all sources to be satisfied.

#### 5.7.2 Trust Anchor Distribution

- PKI trust anchors MUST be distributed via HTTPS-accessible trust lists or ICAO PKD. The `url` field on a `TrustSource` entry specifies the retrieval endpoint.
- Trust list contents MUST be cryptographically signed by the trust list operator.
- Implementations MUST refresh trust list anchors at least every 24 hours for always-online deployments.
- Implementations MAY cache trust anchors for up to 72 hours provided freshness is validated on cache entry creation.
- DID-based trust anchors are resolved on-demand per the DID Method specification. Implementations SHOULD cache resolved DID Documents per the `cacheControl` metadata in the resolution result.

#### 5.7.3 Trust Evaluation Algorithm (Normative)

A verifier MUST execute the following steps before accepting a credential presentation:

1. **Identify credential format** — determine whether the credential is `MDOC`, `SD_JWT_VC`, `VC_JWT`, or `JSON_LD`.
2. **Locate trust sources** — retrieve the `trust_sources` array from the Trust Profile linked to the active Presentation Policy.
3. **Validate issuer identity** — for PKI credentials: verify the issuer certificate chain to a trusted root CA; for DID credentials: resolve the issuer DID and match the signing key identifier to the DID Document's `verificationMethod`.
4. **Verify credential signature** — validate the credential's cryptographic signature using the issuer's verified public key. The algorithm MUST be in `allowed_algorithms`.
5. **Check credential validity period** — confirm `not_before ≤ now ≤ expiry` within the clock skew defined by `time_policy.clock_skew_seconds` (default: 300 seconds).
6. **Check revocation status** — per the Revocation Profile associated with the Trust Profile (see §12 and §20.7).
7. **Evaluate policy claims** — verify all required claims from the Presentation Policy are present and satisfy any predicates or ZK proofs.
8. **Evaluate Cedar verification policies** — if the Trust Profile or its associated Compliance Profile links a `verification_policy_set_id`, evaluate the active Cedar policies in the PolicySet against the credential context. If any `forbid` policy matches, the credential MUST be rejected. This step is OPTIONAL when no PolicySet is linked.
9. **Record audit event** — log the verification result to the Audit Event log with sufficient detail for compliance reporting.

Steps 3–9 are normative. An implementation that skips any of these steps for a `VERIFICATION` flow type MUST emit a compliance warning to the audit log and MUST NOT mark the flow instance as `COMPLETED`.

#### 5.7.4 Trust Failure Handling

- If no trust source can verify the credential's issuer identity, the verifier MUST reject the credential with `error_code: ISSUER_UNTRUSTED`.
- If the trust list refresh fails and the cached version is stale beyond the configured `cache_ttl_seconds`, the verifier MUST fail closed (reject all presentations) unless `check_mode: OFFLINE_GRACE` is configured on the Revocation Profile.
- Implementations MUST NOT degrade to implicit trust (i.e., accept any issuer) on trust source failure.
- Trust failures MUST be logged as audit events with `overall_result: FAIL` and `error_code: ISSUER_UNTRUSTED`.

#### 5.7.5 Trust Registry Sharing

Multiple compliance codes MAY share a single Trust Profile when they rely on the same trust registry. For example:

- **EUDI_PID** (SD-JWT-VC) and **EUDI_MDL** (mDoc) both trust the EU List of Trusted Lists (LoTL). A single `profile_type: EUDI` Trust Profile with `supported_formats: ["SD_JWT_VC", "MDOC"]` serves both.
- **ICAO_DTC** and **ICAO_MRZ** both trust ICAO CSCA certificates. A single `profile_type: ICAO` Trust Profile serves both.

Sharing is declared via `compatible_compliance_codes` on the Trust Profile. When a CredentialTemplate or PresentationPolicy references a Trust Profile, the implementation MUST verify that the linked ComplianceProfile's `compliance_code` appears in the Trust Profile's `compatible_compliance_codes` array (or, when that array is absent, that the compliance code is consistent with the Trust Profile's `profile_type` per the default mapping in §10.7).

The `CUSTOM` profile type is always compatible with any compliance code, providing a universal fallback for non-standard trust configurations.

---

## 6. Credential Template

**Stability:** Moderate | **Owned by:** Program / Compliance

### 6.1 Purpose

A Credential Template is the **master issuance configuration**. It combines schema (what the credential contains), compliance profile (format and framework), cryptographic materials (keys, certs, DIDs), validity rules, and optional application workflow references.

### 6.2 Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Unique identifier |
| `organization_id` | UUID | Yes | Owning organization |
| `name` | string | Yes | Human-readable name |
| `credential_type` | string | Yes | Semantic type (e.g., `EmployeeBadge`, `PreBoardingClearance`) |
| `description` | string | No | Optional description |
| `compliance_profile_id` | UUID | Yes | Reference to Compliance Profile |
| `application_template_id` | UUID | No | Reference to Application Template (null = direct issuance) |
| `trust_profile_id` | UUID | No | Issuer validation requirements |
| `revocation_profile_id` | UUID | No | Revocation configuration |
| `claims` | ClaimDefinition[] | Yes | Claim schema |
| `validity_rules` | ValidityRules | Yes | TTL, reissue, renewable |
| `issuer_key_id` | string | No | Key ID in key vault |
| `issuer_algorithm` | Algorithm | No | Signing algorithm |
| `key_access_mode` | KeyAccessMode | No | `KEY_VAULT`, `HSM`, `LOCAL` |
| `issuer_certificate_chain_pem` | string | No | X.509 issuer cert chain (for mDoc/X.509 credentials) |
| `issuer_did` | string | No | Issuer DID (for DID-based credentials) |
| `auto_generate_artifacts` | boolean | No | Auto-generate keys/certs for dev environments |
| `vct` | string | Conditional | Verifiable Credential Type URI (per SD-JWT-VC §3.2.1). REQUIRED when `credential_format` is `SD_JWT_VC`. MUST be an absolute URI identifying the credential type. |
| `credential_payload_format` | string | No | Payload envelope format: `w3c_vcdm_v2_sd_jwt`, `ietf_sd_jwt_vc`, `iso_mdoc`, `jwt_vc`. Defaults from `credential_format` if omitted. |
| `privacy_posture` | PrivacyPosture | No | Fields intended for selective disclosure |
| `status` | TemplateStatus | Yes | `DRAFT`, `ACTIVE`, `DEPRECATED` |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

### 6.3 ClaimDefinition

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | Yes | Claim name (snake_case) |
| `type` | ClaimType | Yes | `STRING`, `INTEGER`, `BOOLEAN`, `DATE`, `OBJECT`, `ARRAY` |
| `description` | string | No | Human-readable description |
| `required` | boolean | Yes | Whether the claim is required |
| `selectively_disclosable` | boolean | No | May be omitted in selective disclosure |
| `derived_from` | string | No | Source claim for derived attributes (e.g., `age_over_21` from `birth_date`) |
| `namespace` | string | No | mDoc namespace (e.g., `org.iso.18013.5.1`) |
| `display` | ClaimDisplay | No | UI display configuration |

### 6.4 ValidityRules

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `ttl_seconds` | integer | Yes | Credential validity duration |
| `renewable` | boolean | No | Whether the credential can be renewed |
| `reissue_within_seconds` | integer | No | Auto-reissue window before expiry |
| `not_before_offset_seconds` | integer | No | Delay before credential becomes valid |

### 6.5 Validation Rules

- Exactly one of `issuer_key_id`, `issuer_certificate_chain_pem`, or `issuer_did` MUST be present for `ACTIVE` templates, unless `auto_generate_artifacts` is `true`.
- `compliance_profile_id` MUST reference an existing Compliance Profile by ID. Embedding a compliance profile object MUST be rejected.
- `claims` MUST contain at least one entry.
- `vct` MUST be present and MUST be an absolute URI when `credential_format` is `SD_JWT_VC`.
- A template with `status: DRAFT` MUST NOT be used in an active issuance.
- `application_template_id` MUST be null when the template is used for direct/batch issuance.
- Derived claims MUST reference an existing claim in the same template via `derived_from`.

### 6.6 API

```
GET    /v1/credential-templates
POST   /v1/credential-templates
GET    /v1/credential-templates/{id}
PATCH  /v1/credential-templates/{id}
DELETE /v1/credential-templates/{id}
POST   /v1/credential-templates/{id}/validate-artifacts
GET    /v1/credential-templates/{id}/wallet-compatibility
```

---

## 7. Presentation Policy

**Stability:** Dynamic | **Owned by:** Business / Compliance

### 7.1 Purpose

A Presentation Policy defines **what must be shown** to satisfy a verifier. It encodes minimum disclosure requirements, holder-binding rules, issuer constraints, freshness requirements, and optional zero-knowledge predicate configurations.

### 7.2 Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Unique identifier |
| `organization_id` | UUID | Yes | Owning organization |
| `name` | string | Yes | Human-readable name |
| `description` | string | No | Optional description |
| `required_claims` | RequiredClaim[] | Yes | Claims that must be present |
| `accepted_credential_types` | string[] | No | Accepted `credential_type` values |
| `trust_profile_id` | UUID | No | Issuer trust constraints |
| `holder_binding` | HolderBinding | No | Proof-of-possession configuration |
| `freshness` | FreshnessConfig | No | Issuance age constraints |
| `prefer_predicates` | boolean | No | Prefer ZK proofs over raw values |
| `supported_circuits` | string[] | No | ZK circuits supported by this policy |
| `fallback_policy` | FallbackPolicy | No | Default ZK fallback behavior |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

### 7.3 RequiredClaim

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `claim_name` | string | Yes | Claim name |
| `credential_type` | string | No | Which credential type this claim must come from |
| `value_constraint` | any | No | Exact value the claim must equal |
| `predicate_spec` | PredicateSpec | No | ZK predicate configuration |

### 7.4 PredicateSpec

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `predicate_type` | PredicateType | Yes | `RANGE_PROOF`, `MEMBERSHIP`, `EQUALITY`, `NON_MEMBERSHIP`, `INEQUALITY` |
| `params` | object | Yes | Type-specific parameters (see below) |
| `supported_circuits` | string[] | No | Acceptable ZK circuit identifiers (see `enums/zk-circuits.json`) |
| `fallback_policy` | FallbackPolicy | No | `REQUIRE_PREDICATE`, `ACCEPT_RAW`, `DENY` |

**Predicate Params by Type:**

| `predicate_type` | `params` schema |
|------------------|----------------|
| `RANGE_PROOF` | `{threshold: int, comparison: "gte"\|"gt"\|"lte"\|"lt"}` or `{min: int, max: int}` |
| `MEMBERSHIP` | `{allowed_values: any[]}` |
| `EQUALITY` | `{target_value: any}` |
| `NON_MEMBERSHIP` | `{excluded_values: any[]}` |
| `INEQUALITY` | `{target_value: any}` |

**ZK Circuit Identifiers:**

Entries in `supported_circuits` MUST use the format `{system_name}:{circuit_hash}` where `system_name` is a registered ZK circuit system from `enums/zk-circuits.json` and `circuit_hash` is the hex-encoded SHA-256 digest of the compressed circuit binary. The only currently registered system is `longfellow-libzk-v1`.

Example: `["longfellow-libzk-v1:8d079211715200ff06c5109639245502bfe94aa869908d31176aae4016182121"]`

The `longfellow-libzk-v1` system supports `EQUALITY` predicates on mDoc credentials, proving attribute values match expected CBOR-encoded values without revealing the signed credential. It supports up to 4 disclosed attributes per proof and operates over P-256 ECDSA issuer signatures. See `enums/zk-circuits.json` for the full active circuit registry and security parameters.

### 7.5 HolderBinding

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `required` | boolean | Yes | Whether holder binding is required |
| `binding_methods` | string[] | No | Accepted binding methods (`NONCE`, `DEVICE_KEY`, `SESSION_BINDING`) |
| `nonce_required` | boolean | No | Whether verifier-provided nonce is required |

### 7.6 FreshnessConfig

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `max_age_seconds` | integer | No | Maximum credential age |
| `require_not_revoked` | boolean | No | Require active revocation check |
| `revocation_grace_seconds` | integer | No | Offline grace period for revocation checks |

### 7.7 Validation Rules

- `required_claims` MUST contain at least one entry.
- A `predicate_spec` with `predicate_type: RANGE_PROOF` MUST have either `threshold`+`comparison` or `min`+`max` in `params`.
- `fallback_policy: REQUIRE_PREDICATE` MUST only be used when `supported_circuits` is non-empty.
- `trust_profile_id` MUST reference an existing Trust Profile if present.

### 7.8 API

```
GET    /v1/presentation-policies
POST   /v1/presentation-policies
GET    /v1/presentation-policies/{id}
PATCH  /v1/presentation-policies/{id}
DELETE /v1/presentation-policies/{id}
POST   /v1/presentation-policies/{id}/activate
POST   /v1/presentation-policies/{id}/evaluate    Evaluate a VP against a saved policy (stateless)
POST   /v1/presentation-policies/evaluate          Evaluate a VP with an inline policy (ad-hoc)
```

The `/evaluate` endpoints are **stateless** — they do not create a Flow Instance. They accept a Verifiable Presentation and a policy reference (or inline policy object) and return a synchronous pass/fail result. Use `/v1/flows/verify` for the full async flow with QR code and wallet interaction.

---

## 8. Deployment Profile

**Stability:** Operational | **Owned by:** Operations

### 8.1 Purpose

A Deployment Profile packages trust, policies, and runtime behavior for **real endpoints** (gates, kiosks, mobile apps, web portals). It bridges abstract identity policy to physical reality.

### 8.2 Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Unique identifier |
| `organization_id` | UUID | Yes | Owning organization |
| `name` | string | Yes | Human-readable name |
| `description` | string | No | Optional description |
| `trust_profile_id` | UUID | Yes | Trust configuration reference |
| `presentation_policy_ids` | UUID[] | Yes | Enabled presentation policies |
| `credential_template_ids` | UUID[] | No | Enabled credential templates (for issuance-capable deployments) |
| `default_policy_id` | UUID | No | Default presentation policy |
| `network_mode` | NetworkMode | Yes | `ONLINE`, `OFFLINE`, `HYBRID` |
| `key_access_mode` | KeyAccessMode | No | `KEY_VAULT`, `HSM`, `DEVICE_KEYSTORE` |
| `environment_config` | EnvironmentConfig | No | UX, language, accessibility settings |
| `update_channel` | UpdateChannel | No | Version pinning and rollout config |
| `lanes` | Lane[] | No | Logical device groupings |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

### 8.3 Lane

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Lane identifier |
| `name` | string | Yes | Lane name (e.g., "Gate 12") |
| `deployment_profile_id` | UUID | Yes | Parent deployment profile |
| `default_policy_id` | UUID | No | Lane-specific policy override |
| `device_ids` | string[] | No | Device identifiers assigned to this lane |
| `metadata` | object | No | Zone info, operator assignments |

### 8.4 EnvironmentConfig

| Property | Type | Description |
|----------|------|-------------|
| `language` | string | BCP 47 language tag (e.g., `en-US`) |
| `signage_text` | object | Key-value pairs for UI display text |
| `operator_mode` | boolean | Whether operator UI is visible |
| `accessibility_mode` | boolean | High-contrast / screen-reader support |
| `offline_cache_ttl_seconds` | integer | How long to cache trust material offline |

### 8.5 Hierarchy

```
Organization → Site → Deployment Profile → Lane(s) → Device(s)
```

### 8.6 Validation Rules

- `presentation_policy_ids` MUST contain at least one entry.
- `default_policy_id` MUST be in `presentation_policy_ids` if present.
- `trust_profile_id` MUST reference an existing Trust Profile.
- For `network_mode: OFFLINE`, `environment_config.offline_cache_ttl_seconds` SHOULD be set.
- All lane `device_ids`, if present, MUST be unique across all lanes in the same Deployment Profile.

### 8.7 API

```
GET    /v1/deployment-profiles
POST   /v1/deployment-profiles
GET    /v1/deployment-profiles/{id}
PATCH  /v1/deployment-profiles/{id}
DELETE /v1/deployment-profiles/{id}
POST   /v1/deployment-profiles/{id}/activate
GET    /v1/deployment-profiles/{id}/lanes
POST   /v1/deployment-profiles/{id}/lanes
GET    /v1/deployment-profiles/{id}/lanes/{lane_id}
PATCH  /v1/deployment-profiles/{id}/lanes/{lane_id}
DELETE /v1/deployment-profiles/{id}/lanes/{lane_id}
POST   /v1/deployment-profiles/{id}/lanes/{lane_id}/devices
POST   /v1/deployment-profiles/{id}/api-keys
GET    /v1/deployment-profiles/{id}/activity
```

---

## 9. Flow

**Stability:** Per use-case | **Owned by:** All stakeholders

### 9.1 Purpose

A Flow orchestrates the **end-to-end identity lifecycle**: application → approval → issuance → presentation → verification. Flows are the automation layer that makes identity operations repeatable, auditable, and stateful.

### 9.2 Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Unique identifier |
| `organization_id` | UUID | Yes | Owning organization |
| `name` | string | Yes | Human-readable name |
| `description` | string | No | Optional description |
| `flow_type` | FlowType | Yes | Protocol-aligned type; see §9.2.1 |
| `flow_category` | FlowCategory | No | Derived routing category; see §9.2.2 |
| `trust_profile_id` | UUID | No | Trust configuration |
| `credential_template_id` | UUID | No | Required for issuance flow types |
| `presentation_policy_id` | UUID | No | Required for verification flow types |
| `application_template_id` | UUID | No | Required for `application_approval_issuance` |
| `deployment_profile_ids` | UUID[] | No | Where this flow runs |
| `approval_strategy` | ApprovalStrategy | Yes | `AUTO`, `MANUAL`, `RULES_BASED` |
| `trigger` | FlowTrigger | No | What initiates the flow |
| `hooks` | object | No | Pre/post step hooks keyed by step name |
| `status` | FlowStatus | Yes | `DRAFT`, `ACTIVE`, `PAUSED`, `ARCHIVED` |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

#### 9.2.1 FlowType Values (Normative)

| `flow_type` | Category | Required Field | Spec Reference |
|-------------|----------|----------------|----------------|
| `oid4vci_pre_authorized` | ISSUANCE | `credential_template_id` | OID4VCI §6.1 |
| `oid4vci_authorization_code` | ISSUANCE | `credential_template_id` | OID4VCI §6.2 |
| `mdl_issuance` | ISSUANCE | `credential_template_id` | ISO 18013-5 |
| `application_approval_issuance` | ISSUANCE | `application_template_id` | MIP §11 |
| `credential_renewal` | RENEWAL | `credential_template_id` | MIP §9 |
| `credential_revocation` | REVOCATION | `credential_template_id` | MIP §12 |
| `oid4vp_presentation` | VERIFICATION | `presentation_policy_id` | OID4VP |
| `mdl_presentation` | VERIFICATION | `presentation_policy_id` | ISO 18013-5 |

#### 9.2.2 FlowCategory Values (Non-Normative)

`flow_category` is a derived, non-normative field computed from `flow_type`. Implementations MAY use it for routing and filtering. It MUST NOT drive cryptographic or compliance logic.

| `flow_category` | Included `flow_type` values |
|-----------------|-----------------------------|
| `ISSUANCE` | `oid4vci_pre_authorized`, `oid4vci_authorization_code`, `mdl_issuance`, `application_approval_issuance` |
| `VERIFICATION` | `oid4vp_presentation`, `mdl_presentation` |
| `RENEWAL` | `credential_renewal` |
| `REVOCATION` | `credential_revocation` |

### 9.3 FlowTrigger

| Property | Type | Description |
|----------|------|-------------|
| `trigger_type` | TriggerType | `API_CALL`, `WEBHOOK`, `SCHEDULE`, `APPLICATION_SUBMITTED` |
| `config` | object | Trigger-specific configuration |

### 9.4 Hooks

Flows support pre/post hooks on named steps via the `hooks` object. Keys are `pre_{step_name}` or `post_{step_name}`. Each hook entry is an array of hook configurations:

| Property | Type | Description |
|----------|------|-------------|
| `hook_type` | string | `WEBHOOK`, `EXTERNAL_API`, `SCRIPT` |
| `url` | string (URI) | Endpoint for webhook/API hooks |
| `config` | object | Hook-specific configuration |

### 9.5 Standard Step Sequences (Normative)

| `flow_type` | Step Sequence |
|-------------|---------------|
| `oid4vci_pre_authorized` | `create_offer → token_exchange → credential_request → issue_credential` |
| `oid4vci_authorization_code` | `create_offer → authorization → token_exchange → credential_request → issue_credential` |
| `mdl_issuance` | `application_submit → validate_evidence → approval_decision → issue_mdl → deliver_credential` |
| `application_approval_issuance` | `accept_application → validate_evidence → approval_decision → issue_credential → deliver_credential` |
| `credential_renewal` | `validate_existing → create_offer → token_exchange → credential_request → issue_renewed_credential → revoke_old_credential` |
| `credential_revocation` | `validate_revocation_request → update_status_list → notify_holder` |
| `oid4vp_presentation` | `create_request → wallet_selection → presentation_submission → verify_presentation` |
| `mdl_presentation` | `device_engagement → session_establishment → request_items → response_items → session_termination` |
| `siopv2` | `create_request → authentication_submission → verify_id_token` |
| `combined` | `accept_application → approval_decision → issue_credential → create_request → presentation_submission → verify_presentation` |

### 9.6 Approval Strategy with Auto-Issue

For `application_approval_issuance` flows, setting `approval_strategy: AUTO` with `auto_issue: true` on the Application Template causes the `approval_decision` and `issue_credential` steps to execute atomically without manual intervention. This is not a separate endpoint — it is a configuration of the `application_approval_issuance` flow type.

### 9.7 Validation Rules

- Issuance `flow_type` values (`oid4vci_pre_authorized`, `oid4vci_authorization_code`, `mdl_issuance`, `credential_renewal`, `credential_revocation`) MUST have `credential_template_id`.
- `application_approval_issuance` MUST have `application_template_id` and MUST NOT have `credential_template_id`.
- Verification `flow_type` values (`oid4vp_presentation`, `mdl_presentation`, `siopv2`) MUST have `presentation_policy_id`.
- `siopv2` flows MUST have `presentation_policy_id`. The presentation policy governs the ID token claims requested from the Self-Issued OP.
- `combined` flows MUST have both `credential_template_id` and `presentation_policy_id`.
- `credential_template_id` and `application_template_id` are mutually exclusive.
- Active flows MUST NOT reference `DRAFT` or `DEPRECATED` Credential Templates or Application Templates.
- `deployment_profile_ids` MUST each reference an existing Deployment Profile.

### 9.8 API

#### Flow Definitions

```
GET    /v1/flows/definitions
POST   /v1/flows/definitions
GET    /v1/flows/definitions/{id}
PATCH  /v1/flows/definitions/{id}
DELETE /v1/flows/definitions/{id}
POST   /v1/flows/definitions/{id}/activate
```

#### Flow Instances (Runtime)

```
POST   /v1/flows/instances                          Start a flow instance
GET    /v1/flows/instances                          List flow instances
GET    /v1/flows/instances/{id}                     Get instance state
POST   /v1/flows/instances/{id}/advance             Advance to next step
```

#### Verification Runtime (Wallet-Facing, No Auth Required)

```
POST   /v1/flows/verify                             Start async verification (returns QR/request_uri)
GET    /v1/flows/instances/{id}/request             Get OID4VP request object
POST   /v1/flows/instances/{id}/submit              Submit VP token
GET    /v1/flows/instances/{id}/result              Poll for verification result
```

#### SIOPv2 (Self-Issued OpenID Provider v2)

SIOPv2 enables holder authentication using self-issued ID tokens, per the Self-Issued OpenID Provider v2 specification. The flow consists of three steps: `create_request`, `authentication_submission`, and `verify_id_token`.

```
POST   /v1/flows/siop                               Start SIOPv2 cross-device flow
GET    /v1/flows/siop/{id}/request                   Get SIOPv2 authorization request (wallet-facing, no auth)
POST   /v1/flows/siop/submit                        Submit SIOPv2 ID token (wallet-facing, no auth)
GET    /v1/flows/siop/{id}/result                    Poll for SIOPv2 verification result
```

**`POST /v1/flows/siop`** (Auth Required)

Starts a SIOPv2 cross-device authentication flow. Creates a flow instance of type `siopv2` and returns a `request_uri` for the wallet to retrieve the authorization request.

Request body:
```json
{
  "flow_definition_id": "uuid",
  "presentation_policy_id": "uuid",
  "nonce": "string (optional — auto-generated if omitted)",
  "client_metadata": {
    "client_name": "string",
    "logo_uri": "string (optional)",
    "policy_uri": "string (optional)",
    "tos_uri": "string (optional)"
  }
}
```

Response (`201 Created`):
```json
{
  "flow_instance_id": "uuid",
  "request_uri": "string (URI for wallet to retrieve the authorization request)",
  "qr_code_uri": "string (openid-vc://... deep link for QR code rendering)",
  "expires_in": 300
}
```

**`GET /v1/flows/siop/{id}/request`** (No Auth Required — Wallet-Facing)

Returns the SIOPv2 authorization request as a signed JWT (`request` parameter per SIOPv2 §7). The request includes:
- `response_type`: `id_token`
- `scope`: `openid`
- `client_id`: the verifier's `client_id` from the Deployment Profile
- `nonce`: unique per-request nonce
- `response_uri`: the SIOPv2 submit endpoint URI
- `presentation_definition`: (optional) if VP is also requested alongside the ID token

**`POST /v1/flows/siop/submit`** (No Auth Required — Wallet-Facing)

Submits the self-issued ID token from the wallet.

Request body (`application/x-www-form-urlencoded`):
```
id_token={signed_jwt}&state={flow_instance_id}
```

The server validates:
1. The `sub` claim matches the `sub_jwk` (self-issued subject)
2. The `nonce` matches the authorization request
3. The `aud` matches the verifier's `client_id`
4. The ID token signature is valid against the `sub_jwk` public key
5. The ID token is not expired (`exp` claim)

Response (`200 OK`):
```json
{
  "status": "verified",
  "flow_instance_id": "uuid"
}
```

**`GET /v1/flows/siop/{id}/result`** (Auth Required)

Polls for the verification result of a SIOPv2 flow instance. Returns the current state and, when complete, the verified claims.

Response (`200 OK`):
```json
{
  "flow_instance_id": "uuid",
  "status": "COMPLETED | IN_PROGRESS | FAILED",
  "verified_claims": {
    "sub": "string (self-issued subject identifier)",
    "claims": {}
  }
}
```

### 9.9 Flow Instance State Machine

A **Flow Instance** represents one runtime execution of a Flow Definition. Its state machine governs all execution behavior. Flow Instances are distinct from Flow Definitions: a definition is the template, an instance is the execution.

#### 9.9.1 FlowInstance Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Unique instance identifier |
| `flow_definition_id` | UUID | Yes | The Flow Definition that spawned this instance |
| `flow_type` | FlowType | Yes | Copied from the definition at instantiation time |
| `organization_id` | UUID | Yes | Owning organization |
| `status` | FlowInstanceStatus | Yes | Current state machine state |
| `current_step` | string | No | Name of the currently executing step |
| `applicant_id` | UUID | No | Associated Applicant record (if applicable) |
| `credential_id` | UUID | No | Issued credential ID (set on COMPLETED issuance instances) |
| `error_code` | string | No | Terminal error code (present when `status: FAILED`) |
| `started_at` | datetime | No | When execution began |
| `completed_at` | datetime | No | When instance reached a terminal state |
| `expires_at` | datetime | No | Hard expiry deadline |
| `created_at` | datetime | Yes | ISO 8601 |

#### 9.9.2 FlowInstance States

| State | Terminal | Description |
|-------|----------|-------------|
| `PENDING` | No | Instance created; not yet started |
| `IN_PROGRESS` | No | Active execution; a step is running |
| `AWAITING_APPROVAL` | No | Paused pending a manual reviewer decision |
| `AWAITING_WALLET` | No | Paused pending a holder action (credential request or VP response) |
| `AWAITING_EVIDENCE` | No | Paused pending supplementary evidence from the applicant |
| `COMPLETED` | Yes | All steps finished successfully |
| `FAILED` | Yes | A step failed with no further retries |
| `EXPIRED` | Yes | Instance exceeded TTL before completing |
| `CANCELLED` | Yes | Explicitly cancelled by an authorized party |

#### 9.9.3 State Transitions (Normative)

| From State | Triggering Event | To State |
|------------|-----------------|----------|
| `PENDING` | Instance started via API or trigger | `IN_PROGRESS` |
| `IN_PROGRESS` | Manual approval required by flow strategy | `AWAITING_APPROVAL` |
| `IN_PROGRESS` | Wallet interaction required (OID4VCI or OID4VP) | `AWAITING_WALLET` |
| `IN_PROGRESS` | Additional evidence requested from applicant | `AWAITING_EVIDENCE` |
| `IN_PROGRESS` | All steps complete successfully | `COMPLETED` |
| `IN_PROGRESS` | Unrecoverable step failure | `FAILED` |
| `AWAITING_APPROVAL` | Reviewer approves via `ApplicantDecision` | `IN_PROGRESS` |
| `AWAITING_APPROVAL` | Reviewer rejects via `ApplicantDecision` | `FAILED` |
| `AWAITING_WALLET` | Holder responds (VP token or credential request) | `IN_PROGRESS` |
| `AWAITING_WALLET` | Wallet response timeout exceeded | `EXPIRED` |
| `AWAITING_EVIDENCE` | Evidence submitted by applicant | `IN_PROGRESS` |
| `AWAITING_EVIDENCE` | Evidence deadline exceeded | `EXPIRED` |
| `IN_PROGRESS` | Instance TTL (`expires_at`) exceeded | `EXPIRED` |
| Any non-terminal | Explicit cancel request by authorized party | `CANCELLED` |

Terminal states are `COMPLETED`, `FAILED`, `EXPIRED`, and `CANCELLED`. Implementations MUST NOT transition out of a terminal state.

#### 9.9.4 Normative Invariants

- Implementations MUST record a timestamped audit event for every state transition. The audit event MUST include the prior state, new state, triggering event, and actor identity.
- Implementations MUST NOT skip states (e.g., transition directly from `PENDING` to `COMPLETED`).
- Every state transition MUST be persisted atomically. Partial transitions are not permitted.
- `AWAITING_WALLET` MUST have a configured timeout. If no timeout is explicitly configured, implementations MUST default to 600 seconds (10 minutes).
- `AWAITING_APPROVAL` has no mandatory timeout but the instance MUST appear in the reviewer queue within 60 seconds of state entry.
- A Flow Instance MUST inherit `flow_definition_id`, `flow_type`, and `organization_id` from the definition that created it. These fields are immutable after creation.
- Instances with `status: EXPIRED` or `status: FAILED` MUST be retained in the audit log and MUST NOT be deleted.

#### 9.9.5 API

```
GET   /v1/flows/instances/{id}/state     Get current state + step + history
POST  /v1/flows/instances/{id}/cancel    Cancel a non-terminal instance
GET   /v1/flows/instances/{id}/audit     Get ordered list of state transitions
```

---

## 10. Compliance Profile

**Stability:** Stable (system profiles), Moderate (custom) | **Owned by:** Compliance / Security

### 10.1 Purpose

A Compliance Profile abstracts credential format complexity behind compliance-focused profiles. It hides technical encoding details (mdoc vs. SD-JWT vs. VC-JWT) from users by presenting recognized compliance standards.

### 10.2 Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Unique identifier |
| `organization_id` | UUID | No | Null for system profiles |
| `compliance_code` | ComplianceCode | Yes | `ICAO_DTC`, `ICAO_MRZ`, `AAMVA_MDL`, `EUDI_PID`, `EUDI_MDL`, `OB3_JWT`, `OB3_JSONLD`, `SD_JWT_VC`, `ENTERPRISE_VC`, `OID4VC`, `PEX`, `CUSTOM` |
| `name` | string | Yes | Human-readable name |
| `description` | string | No | Optional description |
| `credential_format` | CredentialFormat | Yes | `MDOC`, `SD_JWT_VC`, `VC_JWT`, `JSON_LD` |
| `issuance_protocol` | IssuanceProtocol | No | `OID4VCI_PRE_AUTH`, `OID4VCI_AUTH_CODE`, `DIRECT` |
| `issuer_artifact_requirements` | ArtifactRequirements | No | Required keys, certs, DIDs |
| `default_verification_rules` | object | No | **Deprecated** — use `verification_policy_set_id`. Format-specific verification defaults |
| `verification_policy_set_id` | UUID | No | Reference to a Cedar PolicySet (§16) for credential verification rules |
| `trust_profile_constraints` | TrustProfileConstraints | No | Trust profile compatibility requirements |
| `is_system` | boolean | Yes | System-provided vs. organization-custom |
| `created_at` | datetime | Yes | ISO 8601 |

### 10.3 ArtifactRequirements

| Property | Type | Description |
|----------|------|-------------|
| `requires_x509_cert` | boolean | Requires X.509 issuer certificate |
| `requires_did` | boolean | Requires issuer DID |
| `requires_jwk` | boolean | Requires JSON Web Key |
| `cert_key_usage` | string[] | Required X.509 key usages |

### 10.4 System Compliance Profiles

System profiles are pre-defined and cannot be modified:

| Code | Format | Protocol | Description |
|------|--------|----------|-------------|
| `ICAO_DTC` | `MDOC` | OID4VCI_PRE_AUTH | ICAO Digital Travel Credential |
| `ICAO_MRZ` | `MDOC` | — | ICAO Machine Readable Zone extraction and verification |
| `AAMVA_MDL` | `MDOC` | OID4VCI_PRE_AUTH | AAMVA Mobile Driver's License |
| `EUDI_PID` | `SD_JWT_VC` | OID4VCI_PRE_AUTH | EUDI Personal Identification Data |
| `EUDI_MDL` | `MDOC` | OID4VCI_PRE_AUTH | EUDI Mobile Driving Licence |
| `OB3_JWT` | `VC_JWT` | OID4VCI_PRE_AUTH | Open Badge v3 (JWT) |
| `OB3_JSONLD` | `JSON_LD` | OID4VCI_PRE_AUTH | Open Badge v3 (JSON-LD) |
| `SD_JWT_VC` | `SD_JWT_VC` | OID4VCI_PRE_AUTH | Generic SD-JWT VC |
| `ENTERPRISE_VC` | `VC_JWT` | OID4VCI_PRE_AUTH | Generic enterprise VC |
| `OID4VC` | `SD_JWT_VC` | OID4VCI_PRE_AUTH / OID4VCI_AUTH_CODE | Generic OID4VCI + OID4VP interop (OIDF certification target) |
| `PEX` | `SD_JWT_VC` | — | DIF Presentation Exchange v2 (verifier-side query protocol) |

### 10.5 TrustProfileConstraints

Each Compliance Profile declares the Trust Profile configurations it is compatible with:

| Property | Type | Description |
|----------|------|-------------|
| `compatible_profile_types` | TrustProfileType[] | `profile_type` values that provide a suitable trust registry. `CUSTOM` is always implicitly allowed. |
| `required_source_types` | TrustSourceType[] | `source_type` values that MUST appear in the Trust Profile's `trust_sources`. |
| `required_formats` | CredentialFormat[] | Formats that MUST appear in `supported_formats`. |

**Default mapping** (when `trust_profile_constraints` is absent):

| Compliance Code | Compatible Profile Types | Required Source Types |
|----------------|-------------------------|----------------------|
| `ICAO_DTC`, `ICAO_MRZ` | `ICAO`, `CUSTOM` | `PKD_URL` or `ROOT_CA` |
| `AAMVA_MDL` | `AAMVA`, `CUSTOM` | `TRUST_LIST` or `ROOT_CA` |
| `EUDI_PID`, `EUDI_MDL` | `EUDI`, `CUSTOM` | `TRUST_LIST` |
| `OB3_JWT`, `OB3_JSONLD` | `CUSTOM` | — |
| `SD_JWT_VC`, `ENTERPRISE_VC`, `OID4VC`, `PEX` | `CUSTOM` | — |

Implementations MUST validate that a CredentialTemplate does not pair an incompatible ComplianceProfile and TrustProfile. When `trust_profile_constraints.compatible_profile_types` is present, the Trust Profile's `profile_type` MUST appear in that list. When absent, the default mapping above applies.

### 10.6 api_surface Declaration

A Compliance Profile MAY declare an `api_surface` array that describes the runtime endpoints an implementation MUST expose when this profile is active. This mechanism allows standards-specific APIs (e.g., OID4VCI well-known metadata, mDL device engagement) to be derived from the compliance profile rather than hardcoded into the implementation.

Each entry in `api_surface` has the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rel` | string | Yes | IANA link relation or MIP-defined identifier |
| `path_template` | string | Yes | Path using `{org_id}` and `{deployment_id}` tokens |
| `org_scoped_path` | string | No | Org-specific alternative path |
| `method` | string | Yes | HTTP method (`GET`, `POST`) |
| `auth_required` | boolean | Yes | Whether the endpoint requires authentication |
| `response_schema_ref` | string | No | JSON Schema `$id` of the response |
| `standard_ref` | string | No | Standards citation (e.g., `OID4VCI §11.2.2`) |

Implementations MUST expose all endpoints declared in `api_surface` for every active Compliance Profile.

**MIP Configuration Discovery**: Every MIP implementation MUST expose `GET /.well-known/mip-configuration` returning the active compliance profiles and their `api_surface` declarations. This is MIP's deployment-level metadata document.

### 10.7 API

```
GET    /v1/compliance-profiles
POST   /v1/compliance-profiles
GET    /v1/compliance-profiles/{id}
PATCH  /v1/compliance-profiles/{id}
DELETE /v1/compliance-profiles/{id}
POST   /v1/compliance-profiles/{id}/activate
GET    /.well-known/mip-configuration              Active compliance profiles + api_surface (no auth)
```

---

## 11. Application Template

**Stability:** Dynamic | **Owned by:** Operations / Product

### 11.1 Purpose

An Application Template defines **how users apply for credentials**. It specifies the user-facing form, evidence requirements, claim collection strategy, approval workflow, and notification settings.

Application Templates are **purely user-facing**. They have no cryptographic concerns. Cryptographic configuration lives in the Credential Template.

### 11.2 Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Unique identifier |
| `organization_id` | UUID | Yes | Owning organization |
| `name` | string | Yes | Human-readable name |
| `description` | string | No | Optional description |
| `form_fields` | FormField[] | No | User-facing form fields |
| `evidence_requirements` | EvidenceRequirement[] | No | Documents or biometrics required |
| `claim_collection_rules` | ClaimCollectionRule[] | No | How claims are gathered |
| `approval_strategy` | ApprovalStrategy | Yes | `AUTO`, `MANUAL`, `RULES_BASED`, `EXTERNAL` |
| `approval_rules` | object | No | **Deprecated** — use `approval_policy_set_id`. Legacy rules engine config |
| `approval_policy_set_id` | UUID | No | Reference to a Cedar PolicySet (§16) for `RULES_BASED` approval |
| `notification_config` | NotificationConfig | No | Email/SMS templates for status updates |
| `ui_config` | UIConfig | No | Theme, wizard vs. single-page, welcome text |
| `status` | TemplateStatus | Yes | `DRAFT`, `ACTIVE`, `DEPRECATED` |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

### 11.3 FormField

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `field_id` | string | Yes | Unique field identifier |
| `label` | string | Yes | Display label |
| `field_type` | FieldType | Yes | `TEXT`, `DATE`, `SELECT`, `FILE_UPLOAD`, `BOOLEAN` |
| `required` | boolean | Yes | Whether the field is mandatory |
| `claim_mapping` | string | No | Maps to claim name in Credential Template |
| `validation_pattern` | string | No | Regex validation |
| `options` | string[] | No | Options for `SELECT` type |

### 11.4 EvidenceRequirement

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `evidence_id` | string | Yes | Unique identifier |
| `evidence_type` | EvidenceType | Yes | `DOCUMENT_SCAN`, `BIOMETRIC`, `SELFIE`, `THIRD_PARTY_VERIFICATION` |
| `description` | string | Yes | User-facing instructions |
| `required` | boolean | Yes | Whether the evidence is mandatory |
| `accepted_formats` | string[] | No | Accepted file formats (for `DOCUMENT_SCAN`) |

### 11.5 Validation Rules

- `approval_strategy: RULES_BASED` MUST have a non-null `approval_policy_set_id` or non-empty `approval_rules` (legacy). Cedar PolicySets take precedence when both are present.
- All `claim_mapping` values MUST reference claims in the associated Credential Template.
- A `DEPRECATED` Application Template MUST NOT be the target of a new credential application.

### 11.6 API

```
GET    /v1/application-templates
POST   /v1/application-templates
GET    /v1/application-templates/{id}
PATCH  /v1/application-templates/{id}
DELETE /v1/application-templates/{id}
POST   /v1/applications
GET    /v1/applications/{id}
PATCH  /v1/applications/{id}/approve
PATCH  /v1/applications/{id}/reject
```

---

## 12. Revocation Profile

**Stability:** Stable | **Owned by:** Security

### 12.1 Purpose

A Revocation Profile provides **format-agnostic revocation configuration** for both issuer-side automation (index allocation, publishing, batch updates) and verifier-side behavior (check mode, caching, offline grace).

### 12.2 Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Unique identifier |
| `organization_id` | UUID | Yes | Owning organization |
| `name` | string | Yes | Human-readable name |
| `revocation_mechanism` | RevocationMechanism[] | Yes | Supported mechanisms |
| `mechanism_priority` | RevocationMechanism[] | No | Priority order for multi-mechanism profiles |
| `check_mode` | RevocationCheckMode | Yes | `ALWAYS`, `CACHED`, `OFFLINE_GRACE`, `SKIP` |
| `cache_ttl_seconds` | integer | No | Cache validity duration |
| `offline_grace_seconds` | integer | No | Offline grace period |
| `issuer_config` | IssuerRevocationConfig | No | Issuer-side automation |
| `status_list_url` | string (URI) | No | Published status list URL |
| `created_at` | datetime | Yes | ISO 8601 |

### 12.3 IssuerRevocationConfig

| Property | Type | Description |
|----------|------|-------------|
| `auto_allocate_index` | boolean | Automatically allocate revocation index on issuance |
| `batch_update_interval_seconds` | integer | How often to publish status list updates |
| `list_size` | integer | Size of the status list bitstring |

### 12.4 Supported Mechanisms

| Value | Description |
|-------|-------------|
| `OCSP` | Online Certificate Status Protocol |
| `CRL` | Certificate Revocation List |
| `STATUS_LIST_2021` | W3C Status List 2021 |
| `BITSTRING_STATUS_LIST` | IETF Bitstring Status List |
| `TOKEN_STATUS_LIST` | IETF Token Status List |

### 12.5 Validation Rules

- `revocation_mechanism` MUST NOT be empty.
- `check_mode: OFFLINE_GRACE` MUST have `offline_grace_seconds` set.
- `check_mode: CACHED` MUST have `cache_ttl_seconds` set.
- `status_list_url` MUST be an absolute HTTPS URI if present.

### 12.6 API

```
GET    /v1/revocation-profiles
POST   /v1/revocation-profiles
GET    /v1/revocation-profiles/{id}
PATCH  /v1/revocation-profiles/{id}
DELETE /v1/revocation-profiles/{id}
POST   /v1/revocation-profiles/{id}/activate
```

### 12.7 Revocation Batches

Revocation Batches provide **privacy-preserving batched revocation**. Instead of publishing status list updates immediately (which enables timing-correlation attacks linking a revocation event to a specific holder interaction), the system queues revocations and publishes them at configurable intervals.

#### 12.7.1 Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Unique identifier |
| `organization_id` | UUID | Yes | Owning organization |
| `credential_format` | CredentialFormat | Yes | `MDOC`, `SD_JWT_VC`, `VC_JWT`, `JSON_LD`. Determines status list type: MDOC uses Token Status List; SD_JWT_VC uses Bitstring Status List. |
| `batch_interval` | string | Yes | Publishing cadence: `1h`, `6h`, or `24h`. Lower intervals reduce revocation latency; higher intervals provide stronger timing-correlation resistance. |
| `status` | BatchStatus | Yes | `PENDING`, `PUBLISHING`, `PUBLISHED`, `FAILED` |
| `pending_credential_ids` | UUID[] | No | Credentials queued in this batch, not yet published |
| `published_credential_count` | integer | No | Count of credentials published in this batch |
| `status_list_uri` | string (URI) | No | URI of the published status list after publication |
| `scheduled_publish_at` | datetime | No | When this batch is scheduled to publish |
| `published_at` | datetime | No | When the batch was published |
| `error_message` | string | No | Error details if publication failed |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

#### 12.7.2 Batch Status Lifecycle

```
PENDING → PUBLISHING → PUBLISHED
              ↓
           FAILED → PENDING (retry)
```

- `PENDING`: Credentials are being queued. The batch has not yet reached its `scheduled_publish_at` time.
- `PUBLISHING`: The status list update is being computed and published.
- `PUBLISHED`: The status list has been published at `status_list_uri`.
- `FAILED`: Publication failed. The batch returns to `PENDING` for retry.

#### 12.7.3 Validation Rules

- `batch_interval` MUST be one of `1h`, `6h`, `24h`.
- `credential_format` MUST be a valid CredentialFormat enum value.
- `status_list_uri`, if present, MUST be an absolute HTTPS URI.
- A credential MUST NOT appear in more than one `PENDING` batch for the same organization.

#### 12.7.4 API

```
GET    /v1/revocation-batches                        List revocation batches
POST   /v1/revocation-batches                        Create a revocation batch
GET    /v1/revocation-batches/{id}                   Get batch details
POST   /v1/revocation-batches/{id}/publish           Force-publish a pending batch
DELETE /v1/revocation-batches/{id}                   Cancel a pending batch
```

### 12.8 Cascade Revocation Operations

When an `IssuerEntity` or trust anchor is revoked, a **Cascade Revocation Operation** tracks the propagation of that revocation to all dependent credentials. Cascade operations provide circuit-breaker protection, rollback support, and manual confirmation for high-impact revocations.

The cascade policy is determined by `TrustProfileIssuer.cascade_revocation_policy` (see §5.3 Issuer Registry):

| Policy | Behaviour |
|--------|----------|
| `AUTO_CASCADE` | All credentials issued by this issuer are automatically revoked |
| `MANUAL` | Affected credentials are queued for human review |
| `NOTIFY_ONLY` | Affected parties are notified; credentials remain active until manually revoked |

#### 12.8.1 Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Unique identifier |
| `organization_id` | UUID | Yes | Owning organization |
| `operation_type` | string | Yes | `ISSUER_REVOCATION` or `ANCHOR_REVOCATION` |
| `trigger_entity_type` | string | Yes | `ISSUER` or `TRUST_ANCHOR` |
| `trigger_entity_id` | UUID | Yes | ID of the revoked IssuerEntity or trust anchor |
| `status` | CascadeStatus | Yes | See lifecycle below |
| `affected_credential_count` | integer | No | Number of credentials affected by the cascade |
| `affected_credential_ids` | UUID[] | No | IDs of affected credentials |
| `requires_confirmation` | boolean | No | `true` when `affected_credential_count >= circuit_breaker_threshold` |
| `confirmed_at` | datetime | No | When manual confirmation was provided |
| `confirmed_by` | string | No | Identity of the confirming user |
| `max_cascade_depth` | integer | No | Maximum depth to traverse in the revocation cascade tree (default: 3) |
| `current_depth` | integer | No | Current traversal depth |
| `circuit_breaker_threshold` | integer | No | Credential count that triggers manual confirmation (default: 1000) |
| `circuit_breaker_triggered` | boolean | No | Whether the circuit breaker has been triggered |
| `can_rollback` | boolean | No | Whether a snapshot was captured for rollback |
| `rollback_snapshot` | object | No | Pre-revocation state captured for rollback |
| `rolled_back_at` | datetime | No | When rollback was executed |
| `rolled_back_by` | string | No | Identity of the user who rolled back |
| `error_message` | string | No | Error details if the cascade failed |
| `metadata` | object | No | Additional context |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

#### 12.8.2 Cascade Status Lifecycle

```
PENDING_CONFIRMATION → IN_PROGRESS → COMPLETED
        ↓                    ↓
     (rejected)           FAILED
                             ↓
                        ROLLED_BACK
```

- `PENDING_CONFIRMATION`: Operation was created but requires manual sign-off (circuit breaker triggered or `MANUAL` policy).
- `IN_PROGRESS`: Cascade is actively revoking credentials.
- `COMPLETED`: All affected credentials have been revoked.
- `FAILED`: The cascade encountered an error.
- `ROLLED_BACK`: A completed cascade was reversed using the rollback snapshot.

#### 12.8.3 Circuit Breaker

If `affected_credential_count >= circuit_breaker_threshold` (default: 1000), the operation pauses and `requires_confirmation` is set to `true`. A privileged user MUST confirm the operation via `POST /v1/cascade-revocations/{id}/confirm` before the cascade proceeds. This prevents accidental mass revocation.

#### 12.8.4 Rollback

If `can_rollback` is `true`, the pre-revocation state is captured in `rollback_snapshot`. After a cascade reaches `COMPLETED`, it can be rolled back within 72 hours using `POST /v1/cascade-revocations/{id}/rollback`. Rollback restores credential status list entries to their pre-cascade values. `rollback_snapshot` is deleted after rollback completes.

#### 12.8.5 Validation Rules

- `operation_type` MUST be `ISSUER_REVOCATION` or `ANCHOR_REVOCATION`.
- `trigger_entity_id` MUST reference an existing `IssuerEntity` or trust anchor.
- `max_cascade_depth` MUST be in range [1, 10].
- `circuit_breaker_threshold` MUST be a positive integer ≥ 1.
- A cascade operation in `PENDING_CONFIRMATION` state MUST NOT proceed without explicit confirmation.
- `ROLLED_BACK` is a terminal state; no further transitions are permitted.

#### 12.8.6 API

```
GET    /v1/cascade-revocations                       List cascade revocation operations
POST   /v1/cascade-revocations                       Trigger a cascade revocation
GET    /v1/cascade-revocations/{id}                  Get operation details
POST   /v1/cascade-revocations/{id}/confirm          Confirm a paused cascade
POST   /v1/cascade-revocations/{id}/rollback         Roll back a completed cascade
DELETE /v1/cascade-revocations/{id}                  Cancel a pending cascade
```

---

## 13. Wallet Profile

**Stability:** Derived (normative) / Override (operational) | **Owned by:** System

### 13.1 Purpose

A Wallet Profile describes **which wallet applications are compatible** with a given credential configuration. The normative semantic is **derivation**: wallet compatibility MUST be computable from `(credential_format, issuance_protocol, compliance_profile_code)` without requiring a stored record. The wallet registry provides an **override table** for custom or non-standard wallet apps not covered by the derivation algorithm.

### 13.2 Derivation (Normative)

Wallet Profiles MUST be computed from:

```
(credential_format, issuance_protocol, compliance_profile_code) → WalletProfile
```

This key is extracted from a Credential Template's associated Compliance Profile. The derivation table (§13.4) is maintained by protocol implementers, not end users.

### 13.3 Override Semantics

`POST /v1/wallet-registry` creates an override entry for a `(credential_format, issuance_protocol, compliance_profile_code)` combination. Override entries:

- MUST set `override_precedence` (integer 0–100, higher value wins) to supersede a derived entry on conflict; default is `50`
- SHOULD be used only for custom/organization-specific wallet apps not in the derivation table
- Are OPTIONAL — their absence does not indicate lack of wallet compatibility

`GET /v1/wallet-registry` MUST return derived entries merged with stored overrides. When both exist for the same key, the stored entry wins only if the stored override's `override_precedence` exceeds `50`.

### 13.4 Properties

| Property | Type | Stored? | Description |
|----------|------|---------|-------------|
| `id` | UUID | Override only | UUID for stored override entries |
| `organization_id` | UUID | Override only | Owning organization |
| `name` | string | Both | Human-readable profile name |
| `description` | string | Both | Capability description |
| `credential_format` | CredentialFormat | Both | Format used (key dimension) |
| `issuance_protocol` | IssuanceProtocol | Both | Protocol used (key dimension) |
| `compliance_profile_code` | string | Both | Optional — narrows compatibility further |
| `wallet_apps` | string[] | Both | Compatible wallet application names |
| `specifications` | string[] | Both | Supported standards |
| `supported_platforms` | Platform[] | Both | `ios`, `android`, `web` |
| `deep_link_pattern` | string | Both | URI template for credential delivery |
| `override_precedence` | integer (0–100) | Override only | Numeric precedence; higher value wins on conflict; default `50` |
| `is_override` | boolean | Response | `true` for stored override entries, `false` for system-derived profiles |

### 13.5 Compatible Wallet Matrix (Normative)

| Format | Protocol | Compliance | Compatible Wallets |
|--------|----------|-----------|-------------------|
| `MDOC` | `OID4VCI_PRE_AUTH` | `AAMVA_MDL` | Apple Wallet (mDL), Google Wallet (mDL), ISO-compliant mDL wallets |
| `MDOC` | `OID4VCI_PRE_AUTH` | `ICAO_DTC` | ICAO DTC-compatible wallets |
| `MDOC` | `OID4VCI_PRE_AUTH` | `EUDI_MDL` | EUDI Wallet, eIDAS-compliant wallets |
| `SD_JWT_VC` | `OID4VCI_PRE_AUTH` | `EUDI_PID` | EUDI Wallet, eIDAS-compliant wallets |
| `VC_JWT` | `OID4VCI_PRE_AUTH` | `OB3_JWT` | 1EdTech Open Badge Passport, Learning Credentials Wallet |
| `JSON_LD` | `OID4VCI_PRE_AUTH` | `OB3_JSONLD` | 1EdTech Open Badge Passport, DIF Universal Wallet |
| `SD_JWT_VC` | `OID4VCI_PRE_AUTH` | null | EUDI Wallet, OID4VCI-compatible wallets |
| `VC_JWT` | `OID4VCI_PRE_AUTH` | `ENTERPRISE_VC` | Organization-managed wallets |

### 13.6 API

```
GET    /v1/credential-templates/{id}/wallet-compatibility    Derived compatibility (read-only)
GET    /v1/trust-profiles/{id}/wallet-compatibility          Derived compatibility (read-only)
GET    /v1/wallet-registry                                   Merged derived + overrides
POST   /v1/wallet-registry                                   Create override entry
GET    /v1/wallet-registry/{id}                              Get override entry
PATCH  /v1/wallet-registry/{id}                              Update override entry
DELETE /v1/wallet-registry/{id}                              Delete override entry
```

---

## 14. Device Registration

**Stability:** Operational | **Owned by:** Platform

### 14.1 Purpose

A Device Registration records a **user's device** for push notification delivery and secure challenge-response authentication. Device registrations enable device-targeted message propagation for credential offers, verification requests, and approval notifications.

### 14.2 Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Primary key |
| `user_id` | string | Yes | Owner user identifier |
| `organization_id` | UUID | No | Organization scope |
| `device_id` | string | Yes | Client-provided device identifier |
| `platform` | Platform | Yes | `ios`, `android`, `web` |
| `fcm_token` | string | Yes | FCM token (mobile) or SSE connection ID (web) |
| `app_version` | string | No | Application version |
| `os_version` | string | No | Operating system version |
| `device_model` | string | No | Device model name |
| `preferences` | object | No | Notification preferences |
| `public_key_der` | bytes | No | RSA public key for challenge signatures (base64 DER, PKCS#1) |
| `public_key_kid` | string | No | Key ID (SHA-256 thumbprint, RFC 7638) |
| `key_valid_from` | datetime | No | Key validity start |
| `key_valid_until` | datetime | No | Key validity end (for rotation grace) |
| `is_active` | boolean | Yes | Active status |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |
| `last_seen_at` | datetime | No | Last activity ISO 8601 |

### 14.3 Unique Constraints

The combination of (`user_id`, `device_id`) MUST be unique. Registering the same device again MUST update (upsert) the existing record rather than create a duplicate.

### 14.4 Platform-Specific Behavior

| Platform | Token Type | Delivery Channel | Secondary |
|----------|-----------|------------------|-----------|
| `ios` | FCM token | Firebase Cloud Messaging | Polling |
| `android` | FCM token | Firebase Cloud Messaging | Polling |
| `web` | SSE connection ID | Server-Sent Events | Polling |

### 14.5 Key Rotation

When a device rotates its signing key:
1. Submit a new registration with a new `public_key_der`
2. The existing `key_valid_until` provides a grace period for in-flight challenges
3. After the grace period, the old key is rejected

### 14.6 Validation Rules

- `fcm_token` MUST NOT be empty for active registrations.
- `platform` MUST be a value from the `device-platforms` enum.
- If `public_key_der` is present, `public_key_kid` MUST also be present.
- `public_key_kid` MUST be the SHA-256 thumbprint of `public_key_der`.
- Implementations MUST invalidate registrations when FCM reports an invalid token (set `is_active: false`).

### 14.7 API

```
GET    /v1/devices
POST   /v1/devices
GET    /v1/devices/{device_id}
PATCH  /v1/devices/{device_id}
DELETE /v1/devices/{device_id}
GET    /v1/users/{user_id}/devices
```

---

## 15. Notification Target

**Stability:** Operational | **Owned by:** Platform

### 15.1 Purpose

A Notification Target describes **multi-channel message delivery** to one or more recipients. Combined with a Notification Payload, it enables device-targeted propagation of identity events (credential offers, verification requests, approvals).

### 15.2 Notification Target Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `organization_id` | UUID | No | Organization-level targeting |
| `user_id` | string | No | User-level targeting |
| `device_tokens` | string[] | No | Direct device tokens (FCM or SSE IDs) |
| `webhook_endpoints` | string[] | No | HTTP callback URLs |
| `email_addresses` | string[] | No | Email recipients |
| `channels` | ChannelType[] | Yes | Target channels |

At least one of `organization_id`, `user_id`, `device_tokens`, `webhook_endpoints`, or `email_addresses` MUST be present.

### 15.3 Notification Payload Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Notification ID |
| `title` | string | Yes | Notification title |
| `body` | string | Yes | Notification body text |
| `data` | object | No | Structured payload |
| `event_type` | string | Yes | Event classification |
| `priority` | NotificationPriority | Yes | `LOW`, `NORMAL`, `HIGH`, `CRITICAL` |
| `target` | NotificationTarget | Yes | Targeting configuration |
| `ttl_seconds` | integer | No | Time-to-live (default: 86400) |
| `collapse_key` | string | No | For collapsing similar notifications |
| `created_at` | datetime | Yes | ISO 8601 |
| `correlation_id` | string | No | For tracing related notifications |

### 15.4 Delivery Result

| Property | Type | Description |
|----------|------|-------------|
| `notification_id` | UUID | Reference to payload |
| `channel` | ChannelType | Delivery channel |
| `success` | boolean | Delivery success |
| `attempted_at` | datetime | Attempt timestamp |
| `delivered_at` | datetime | Delivery timestamp (if successful) |
| `error_code` | string | Error code (if failed) |
| `should_retry` | boolean | Whether retry is appropriate |
| `retry_after` | integer | Retry delay in seconds |

### 15.5 Standard Event Types

| `event_type` | Description | Primary Channel |
|-------------|-------------|----------------|
| `credential.offered` | Credential offer available | FCM/SSE |
| `credential.issued` | Credential successfully issued | FCM/SSE |
| `credential.revoked` | Credential has been revoked | FCM/SSE + Email |
| `verification.requested` | Verification request to holder | FCM/SSE |
| `application.received` | Application received by issuer | Email |
| `application.approved` | Application approved | FCM/SSE + Email |
| `application.rejected` | Application rejected | FCM/SSE + Email |

### 15.6 Message Propagation Flow

```
1. Event triggered (e.g., credential issuance complete)
2. event_type determines default channels (via routing rules)
3. user_id resolved to Device Registrations
4. Per-platform routing:
   ios/android  → FCM Adapter → Firebase Cloud Messaging
   web          → SSE Adapter → Server-Sent Events
   webhooks     → HTTP Adapter → POST to endpoint
   email        → Email Adapter → SMTP
5. Delivery Results tracked per channel
6. Invalid tokens marked in Device Registry on permanent failure
7. Retries scheduled for transient failures
```

### 15.7 Validation Rules

- `channels` MUST NOT be empty.
- `ttl_seconds` MUST be a positive integer if present.
- Webhook `endpoint` URLs in `webhook_endpoints` MUST be absolute HTTPS URIs.
- Implementations MUST NOT deliver notification payloads containing raw credential material (credentials travel via OID4VCI offer URIs, not notification bodies).

### 15.8 API

```
POST   /v1/notifications/send
GET    /v1/notifications/{id}
GET    /v1/notifications/{id}/delivery-results
```

---

## 16. Policy Set (Cedar)

**Stability:** Moderate | **Owned by:** Security / Platform

### 16.1 Purpose

A Policy Set stores [Cedar](https://www.cedarpolicy.com/) authorization policies that govern access control, credential verification trust, and approval decisions. Cedar is a deny-by-default policy language that is statically analyzable, formally verifiable, and auditable. Policy Sets replace opaque JSON rule objects (`approval_rules`, `default_verification_rules`) with structured, machine-verifiable policies.

MIP defines three policy domains:

| Domain | Description | Referenced By |
|--------|-------------|---------------|
| **Access Control** | API authorization via RBAC + ABAC | ScimRole (`policy_set_id`) |
| **Credential Verification** | Trust evaluation rules (issuer trust, format requirements, algorithm restrictions) | TrustProfile, ComplianceProfile (`verification_policy_set_id`) |
| **Approval Rules** | Application approval decisions (risk scoring, biometric thresholds, evidence requirements) | ApplicationTemplate (`approval_policy_set_id`) |

### 16.2 Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Unique identifier |
| `organization_id` | UUID | Yes | Owning organization |
| `name` | string | Yes | Human-readable name |
| `description` | string | No | Optional description |
| `policy_type` | PolicyType | Yes | `ACCESS_CONTROL`, `CREDENTIAL_VERIFICATION`, `APPROVAL_RULES`, `CUSTOM` |
| `cedar_policies` | CedarPolicy[] | Yes | One or more Cedar policy entries |
| `cedar_schema_version` | string | Yes | Cedar schema namespace and version (e.g., `MIP/1.0`) |
| `status` | PolicySetStatus | Yes | `DRAFT`, `ACTIVE`, `ARCHIVED` |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

### 16.3 CedarPolicy

Each entry in `cedar_policies` defines a single Cedar permit or forbid rule:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `policy_id` | string | Yes | Unique identifier within the PolicySet |
| `effect` | string | Yes | `permit` or `forbid` |
| `cedar_text` | string | Yes | The Cedar policy source text |
| `description` | string | No | Human-readable description |
| `enabled` | boolean | Yes | Whether this policy is active |

### 16.4 Cedar Schema

The MIP Cedar schema is defined in `cedar/mip.cedarschema` under the `MIP` namespace. It declares:

- **Entity types** corresponding to MIP protocol entities (User, ApiKey, ServiceAccount, Organization, Role, Credential, Flow, TrustProfile, ComplianceProfile, etc.)
- **Action declarations** corresponding to API key scopes and operational permissions (e.g., `Action::"credential_templates:read"`, `Action::"flows:execute"`)
- **Context types** for runtime evaluation: `RequestContext` (IP address, timestamp, MFA status), `CredentialContext` (format, compliance, issuer trust, revocation/expiry, binding, algorithm), `ApprovalContext` (risk score, document verification, biometric match score)

Implementations MUST validate Cedar policy text against the MIP Cedar schema before persisting a PolicySet.

### 16.5 Evaluation Semantics

Cedar evaluation follows **deny-by-default** semantics:

1. If any `forbid` policy matches, the request is **denied** regardless of `permit` policies.
2. If no `forbid` policy matches and at least one `permit` policy matches, the request is **allowed**.
3. If no policy matches at all, the request is **denied** (deny-by-default).

This means `forbid` policies act as hard security constraints that cannot be overridden by `permit` policies.

### 16.6 Relationship to Existing Fields

Cedar PolicySets augment — rather than replace — existing enum-based fields:

- **Trust Profile**: `allowed_algorithms`, `supported_formats`, and `trust_sources` remain the primary trust configuration. A `verification_policy_set_id` provides additional conditional trust rules (e.g., deny weak algorithms, require holder binding for specific compliance codes).
- **Compliance Profile**: `verification_policy_set_id` replaces the deprecated `default_verification_rules` opaque object.
- **Application Template**: `approval_policy_set_id` replaces the deprecated `approval_rules` opaque object. The `approval_strategy` MUST be `RULES_BASED` or `EXTERNAL` to use Cedar approval policies.
- **SCIM Role**: `policy_set_id` provides ABAC rules beyond the static `permissions[]` array. When present, Cedar policies are evaluated in addition to permission checks.

When both legacy fields and Cedar PolicySet references are present, the Cedar PolicySet takes precedence.

### 16.7 Validation Rules

- `cedar_policies` MUST contain at least one entry.
- All `cedar_text` values MUST parse successfully against the MIP Cedar schema.
- A PolicySet with `status: DRAFT` MUST NOT be referenced by any active entity.
- Disabled policies (`enabled: false`) MUST be excluded from evaluation at runtime.
- `policy_type: ACCESS_CONTROL` PolicySets MUST only be referenced by ScimRole entities.
- `policy_type: CREDENTIAL_VERIFICATION` PolicySets MUST only be referenced by TrustProfile or ComplianceProfile entities.
- `policy_type: APPROVAL_RULES` PolicySets MUST only be referenced by ApplicationTemplate entities.

### 16.8 API

```
GET    /v1/policy-sets
POST   /v1/policy-sets
GET    /v1/policy-sets/{id}
PATCH  /v1/policy-sets/{id}
DELETE /v1/policy-sets/{id}
POST   /v1/policy-sets/{id}/activate
POST   /v1/policy-sets/{id}/archive
POST   /v1/policy-sets/{id}/validate          Validate Cedar text against schema
```

### 16.9 Reference Policies

MIP provides reference Cedar policies in `cedar/policies/`:

| File | Domain | Description |
|------|--------|-------------|
| `api_access.cedar` | Access Control | RBAC + ABAC for API authorization (org-admin, role-based, API key scoping, MFA requirements) |
| `credential_verification.cedar` | Credential Verification | Trust evaluation rules (revoked/expired deny, compliance-specific format + binding requirements, weak algorithm denial, freshness enforcement) |
| `approval_rules.cedar` | Approval Rules | Application approval policies (risk-based auto-approve, biometric threshold, evidence verification) |

See [Cedar Policies Documentation](docs/cedar-policies.md) for detailed architecture, migration guide, and SDK integration instructions.

---

## 17. API Surface

All MIP-compliant implementations MUST expose the following resource endpoints. The canonical path prefix for all MIP resources is `/v1/`. There is no `/v1/identity/` sub-prefix.

### 17.1 Configuration Resources

| Resource | Base Path | Auth |
|----------|-----------|------|
| Organizations | `/v1/organizations` | Required |
| Trust Profiles | `/v1/trust-profiles` | Required |
| Credential Templates | `/v1/credential-templates` | Required |
| Compliance Profiles | `/v1/compliance-profiles` | Required |
| Application Templates | `/v1/application-templates` | Required |
| Revocation Profiles | `/v1/revocation-profiles` | Required |
| Presentation Policies | `/v1/presentation-policies` | Required |
| Deployment Profiles | `/v1/deployment-profiles` | Required |
| Policy Sets (Cedar) | `/v1/policy-sets` | Required |

All configuration resources support full CRUD: `GET` (list), `POST` (create), `GET /{id}` (read), `PATCH /{id}` (update), `DELETE /{id}` (delete), `POST /{id}/activate` (lifecycle transition).

### 17.2 Identity Governance Resources

| Resource | Base Path | Auth |
|----------|-----------|------|
| Organization Members | `/v1/organizations/{id}/members` | Required |
| Organization Roles | `/v1/organizations/{id}/roles` | Required |
| Organization Invites | `/v1/organizations/{id}/invites` | Required |
| SCIM Users | `/v1/organizations/{id}/scim/v2/Users` | Required |
| SCIM Groups | `/v1/organizations/{id}/scim/v2/Groups` | Required |
| SCIM ServiceProviderConfig | `/v1/organizations/{id}/scim/v2/ServiceProviderConfig` | Required |
| Permission Catalog | `/v1/organizations/{id}/permissions` | Required |

See §18 (Organization & Identity Governance) for full SCIM alignment specification.

### 17.3 Operational Resources

| Resource | Base Path | Auth |
|----------|-----------|------|
| Flow Definitions | `/v1/flows/definitions` | Required |
| Flow Instances | `/v1/flows/instances` | Required |
| Issuance (admin) | `/v1/issuance` | Required |
| Applications | `/v1/applications` | Required |
| Applicants | `/v1/organizations/{id}/applicants` | Required |
| API Keys | `/v1/api-keys` | Required |
| Webhooks | `/v1/organizations/{id}/webhooks` | Required |
| Alert Rules | `/v1/organizations/{id}/alert-rules` | Required |
| Notification Preferences | `/v1/organizations/{id}/notification-preferences` | Required |
| User Notification Preferences | `/v1/users/{id}/notification-preferences` | Required |
| Wallet Registry | `/v1/wallet-registry` | Required |
| User Preferences | `/v1/me/preferences` | Required |
| MRZ Read | `POST /v1/flows/mrz/read` | Required |
| MRZ Verify | `POST /v1/flows/mrz/verify` | Required |
| Revocation Batches | `/v1/revocation-batches` | Required |
| Cascade Revocation Operations | `/v1/cascade-revocations` | Required |

### 17.4 Wallet-Facing Endpoints (No Auth Required)

Wallet-facing endpoints are called directly by wallets and MUST NOT require API key or bearer token authentication. They form the OID4VCI/OID4VP protocol surface.

| Endpoint | Path | Standard |
|----------|------|----------|
| Credential Offer | `GET /v1/issuance/offers/{tx_id}` | OID4VCI §5 |
| Token Endpoint | `POST /v1/issuance/token` | OID4VCI §7 |
| Credential Endpoint | `POST /v1/issuance/credential` | OID4VCI §8 |
| Nonce Endpoint | `POST /v1/issuance/nonce` | OID4VCI §8.3 |
| Deferred Credential | `POST /v1/issuance/deferred-credential` | OID4VCI §9 |
| Notification | `POST /v1/issuance/notification` | OID4VCI §10 |
| VP Request | `GET /v1/flows/instances/{id}/request` | OID4VP §5 |
| VP Submit | `POST /v1/flows/instances/{id}/submit` | OID4VP §6 |
| SIOPv2 Request | `GET /v1/flows/siop/{id}/request` | SIOPv2 §7 |
| SIOPv2 Submit | `POST /v1/flows/siop/submit` | SIOPv2 §7 |

### 17.5 Discovery Endpoints (No Auth Required)

| Endpoint | Path | Description |
|----------|------|-------------|
| MIP Configuration | `GET /.well-known/mip-configuration` | Active profiles + API surface (see §10.5) |
| OID4VCI Issuer Metadata | `GET /.well-known/openid-credential-issuer` | Global OID4VCI metadata |
| OID4VCI Issuer Metadata (per-org) | `GET /org/{org_id}/.well-known/openid-credential-issuer` | Org-scoped OID4VCI metadata |
| OAuth Server Metadata | `GET /.well-known/oauth-authorization-server` | OAuth 2.0 server metadata |

Discovery endpoints for OID4VCI and OID4VP are **declared by the active Compliance Profile** via `api_surface` (see §10.5) — they are not hardcoded into the core MIP API surface.

### 17.6 Observability & Audit

| Resource | Base Path | Auth |
|----------|-----------|------|
| Audit Events | `/v1/organizations/{id}/audit-events` | Required |
| Audit Event Detail | `/v1/organizations/{id}/audit-events/{event_id}` | Required |
| Audit Export | `GET /v1/organizations/{id}/audit-events/export` | Required |
| Webhook Deliveries | `GET /v1/organizations/{id}/webhooks/{webhook_id}/deliveries` | Required |
| Notifications | `GET /v1/notifications` | Required |
| Notification Read-State | `PATCH /v1/notifications/{id}/read` | Required |
| Unread Count | `GET /v1/notifications/unread-count` | Required |
| Device Registrations | `/v1/devices` | Required |
| Health | `GET /health` | None |

### 17.7 Conventions

- All IDs are UUIDs (v4)
- All timestamps are ISO 8601 with timezone (UTC preferred)
- Pagination: `limit` + `offset` query parameters
- Organization scoping: `organization_id` query parameter or JWT claim
- Error responses: `{ "error": string, "code": string, "field": string? }`
- Versioning: URL path prefix `/v1/`
- SCIM responses: RFC 7644 `ListResponse` with `totalResults`, `startIndex`, `itemsPerPage`, `Resources`

---

## 18. Organization & Identity Governance

**Stability:** Moderate | **Owned by:** Platform

### 18.1 Purpose

MIP defines first-class resources for organization management and member identity governance. Organization and member management are native MIP protocol concerns — not delegated entirely to the IdP — because credential issuance, presentation policy authorization, and audit event attribution all require a well-defined org/member model.

### 18.2 Organization Entity

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Unique identifier |
| `name` | string | Yes | Machine-friendly slug (1–64 chars, `[a-z0-9-]`) |
| `display_name` | string | Yes | Human-readable name (1–128 chars) |
| `description` | string | No | Optional description |
| `join_code` | string | No | Short code for discoverable org joining |
| `visibility` | string | Yes | `PUBLIC` or `PRIVATE` |
| `owner_id` | string | Yes | User ID of the current owner |
| `status` | string | Yes | `ACTIVE`, `SUSPENDED`, `DELETED` |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

### 18.3 Organization API

```
GET    /v1/organizations                            List organizations
POST   /v1/organizations                            Create organization
GET    /v1/organizations/{id}                       Get organization
PUT    /v1/organizations/{id}                       Update organization
DELETE /v1/organizations/{id}                       Delete organization
GET    /v1/organizations/mine                       Get caller's organizations
GET    /v1/organizations/discover                   List PUBLIC organizations
POST   /v1/organizations/join/code                  Join by join_code
GET    /v1/organizations/join/code/validate         Validate join code (no auth)
POST   /v1/organizations/{id}/join                  Join by org ID
POST   /v1/organizations/{id}/transfer-ownership    Initiate ownership transfer
```

### 18.4 Invitation Workflow

Invitations are short-lived (default TTL: 7 days), single-use JWT tokens signed by the issuing organization's key. The invite workflow:
1. Admin creates invite: `POST /v1/organizations/{id}/invites` → returns `invite_token`
2. Invitee validates: `GET /v1/organizations/invitations/validate?token={token}` (no auth)
3. Invitee accepts: `POST /v1/organizations/invitations/accept` with `{ token }`

```
GET    /v1/organizations/{id}/invites
POST   /v1/organizations/{id}/invites
POST   /v1/organizations/{id}/invites/{invite_id}/resend
DELETE /v1/organizations/{id}/invites/{invite_id}
GET    /v1/organizations/invitations/validate       Validate invitation token (no auth)
POST   /v1/organizations/invitations/accept
```

### 18.5 SCIM Alignment (RFC 7643 / RFC 7644)

MIP adopts SCIM 2.0 core schema (RFC 7643) for User and Group resources scoped under an organization. SCIM provides a standard interface for cross-domain identity management — provisioning, deprovisioning, and group membership — that is compatible with existing IdP integrations (Keycloak, Okta, Ping, etc.).

**MIP SCIM Extension Schema**: `urn:mip:scim:schemas:extension:Organization:2.0:User`

Extended User attributes:

| Attribute | Type | Description |
|-----------|------|-------------|
| `role_ids` | string[] | MIP role UUIDs assigned to this member |
| `is_owner` | boolean | Whether this user is the organization owner |
| `joined_at` | datetime | When the user joined this organization |

**MIP Role Extension Schema**: `urn:mip:scim:schemas:extension:Organization:2.0:Role`

| Attribute | Type | Description |
|-----------|------|-------------|
| `permissions` | string[] | Permission strings from the permission catalog. Correspond to Cedar Action entities in the MIP namespace (see §16). |
| `policy_set_id` | UUID | Optional reference to a Cedar PolicySet (§16) for fine-grained ABAC beyond static permission strings |
| `is_system_role` | boolean | System-defined (read-only) vs. custom role |

SCIM Groups map directly to MIP Roles.

**SCIM Endpoints** (org-scoped):

```
GET    /v1/organizations/{id}/scim/v2/ServiceProviderConfig
GET    /v1/organizations/{id}/scim/v2/Schemas
GET    /v1/organizations/{id}/scim/v2/ResourceTypes
GET    /v1/organizations/{id}/scim/v2/Users
POST   /v1/organizations/{id}/scim/v2/Users
GET    /v1/organizations/{id}/scim/v2/Users/{userId}
PUT    /v1/organizations/{id}/scim/v2/Users/{userId}
PATCH  /v1/organizations/{id}/scim/v2/Users/{userId}
DELETE /v1/organizations/{id}/scim/v2/Users/{userId}
GET    /v1/organizations/{id}/scim/v2/Groups
POST   /v1/organizations/{id}/scim/v2/Groups
GET    /v1/organizations/{id}/scim/v2/Groups/{groupId}
PUT    /v1/organizations/{id}/scim/v2/Groups/{groupId}
PATCH  /v1/organizations/{id}/scim/v2/Groups/{groupId}
DELETE /v1/organizations/{id}/scim/v2/Groups/{groupId}
```

**SCIM PATCH** (RFC 7644 §3.5.2) uses `add`, `remove`, `replace` operations. Implementations MUST support SCIM filtering (`filter` query parameter) on `userName`, `emails`, `externalId`, and MIP extension attributes.

### 18.6 Native Member & RBAC API

For implementations that do not expose SCIM, the following native endpoints provide equivalent member and role management:

```
GET    /v1/organizations/{id}/members
POST   /v1/organizations/{id}/members
PATCH  /v1/organizations/{id}/members/{member_id}
DELETE /v1/organizations/{id}/members/{member_id}
GET    /v1/organizations/{id}/permissions             Read-only permission catalog
GET    /v1/organizations/{id}/roles
POST   /v1/organizations/{id}/roles
GET    /v1/organizations/{id}/roles/{role_id}
PATCH  /v1/organizations/{id}/roles/{role_id}
DELETE /v1/organizations/{id}/roles/{role_id}
PUT    /v1/organizations/{id}/members/{member_id}/roles
POST   /v1/organizations/{id}/members/{member_id}/roles/{role_id}
DELETE /v1/organizations/{id}/members/{member_id}/roles/{role_id}
GET    /v1/organizations/{id}/members/me/permissions
```

Conforming implementations SHOULD support both the SCIM interface (§18.5) and the native interface (§18.6). The SCIM interface is RECOMMENDED for integrations with external IdPs.

---

## 19. Validation Rules

See per-entity sections (5–15) for entity-specific rules.

### 19.1 Cross-Entity Rules

- A Credential Template MUST NOT reference a Compliance Profile with an incompatible combination of `credential_format` and `issuer_key_id` algorithm.
- A Presentation Policy MUST NOT reference claim names that contradict the ZK circuit requirements of its `supported_circuits`.
- A Deployment Profile MUST NOT be `ACTIVE` in a Flow if any of its Presentation Policies are in `DRAFT` status.

### 19.2 Referential Integrity

All UUID references MUST resolve to existing records within the same organization unless otherwise noted (system Compliance Profiles have no `organization_id`).

---

## 20. Security Considerations

### 20.1 Cryptographic Requirements

- Signing keys MUST be stored in a hardware-backed key store (HSM or secure enclave) for production deployments.
- Implementations MUST NOT accept credentials signed with deprecated algorithms (RS256 with key size < 2048 bits, PS256 with key size < 2048 bits are deprecated).
- Nonces in holder-binding MUST be cryptographically random (min 128 bits) and single-use.

### 20.2 Revocation

- Verifiers MUST check revocation status unless explicitly configured with `check_mode: SKIP`.
- `SKIP` revocation mode MUST NOT be used for credentials with legal or regulatory significance.
- Offline grace periods SHOULD NOT exceed 24 hours for high-assurance credentials.

### 20.3 Device Registration

- Device public keys MUST be verified with a challenge-response before being stored.
- Notification payloads MUST NOT contain credential material — only offer URIs and metadata.
- FCM tokens MUST be treated as sensitive and not logged in plaintext.

### 20.4 API Security

- All API endpoints MUST require authentication (OAuth 2.0 bearer token or equivalent).
- Webhook endpoints receiving notifications MUST validate HMAC signatures.
- Rate limiting MUST be applied to all public-facing endpoints.
- API authorization SHOULD be enforced via Cedar policies (§16) evaluated against the MIP Cedar schema. Implementations MUST NOT rely solely on static permission strings for access control decisions involving conditional or contextual factors (e.g., MFA status, IP address, organization scope).

### 20.5 Threat Model

#### 20.5.1 Threat Enumeration

| Threat | Description | Affected Component |
|--------|-------------|-------------------|
| Replay Attack | Attacker reuses a captured VP token or credential offer that has already been consumed | Flow, Issuance, Verification |
| Credential Cloning | Attacker extracts bound key material to create holder-equivalent copies of a credential | Wallet, Key Storage |
| Issuer Impersonation | Attacker presents credential signed by an unauthorized key while claiming trusted issuer status | Trust Profile, Trust Evaluation |
| Verifier Phishing | Attacker presents a fake verifier `client_id` to collect holder credential data | OID4VP, Presentation Policy |
| Revocation Bypass | Attacker presents a revoked credential to a verifier with a stale revocation cache or permissive grace period | Revocation Profile, Verification |
| Wallet Compromise | Attacker gains unauthorized access to the holder wallet and its key material | Wallet, Device Registration |
| Nonce Reuse | Attacker re-uses a challenge nonce to bind a proof to a different request | Issuance, Verification |
| Man-in-the-Middle | Attacker intercepts and modifies messages between parties during session establishment | Transport, Session |
| Metadata Injection | Attacker modifies or replaces the OID4VCI issuer metadata endpoint response | Capability Discovery |
| Offline Grace Abuse | Attacker exploits an excessively long offline grace period to present revoked credentials | Revocation Profile |

#### 20.5.2 Normative Mitigations

| Threat | Normative Requirement |
|--------|----------------------|
| Replay Attack | Implementations MUST reject any proof or VP token where the `nonce` has been previously seen. Nonces MUST be stored with sufficient retention to cover `offline_grace_seconds + clock_skew_seconds`. |
| Credential Cloning | Issuance MUST require holder binding proof when `holder_binding_required: true` in the Compliance Profile (see §20.6). Wallet implementations SHOULD use hardware-backed key storage. |
| Issuer Impersonation | Verifiers MUST validate the full issuer certificate chain or DID resolution per §5.7.3. |
| Verifier Phishing | Wallets SHOULD validate `client_id` against registered verifier metadata. Verifiers SHOULD register their `client_id` in the organization's Deployment Profile. |
| Revocation Bypass | Verifiers MUST NOT use `check_mode: SKIP` for credentials with legal or regulatory significance. Offline grace MUST NOT exceed 24 hours for credentials at assurance level IAL2 or higher. |
| Wallet Compromise | Device Registrations SHOULD include device attestation proofs. Wallets SHOULD require biometric or PIN authentication before presenting. |
| Nonce Reuse | Nonce endpoints MUST invalidate nonces immediately upon first use. Issued nonces MUST have an expiry (`c_nonce_expires_in` in OID4VCI token responses). |
| Man-in-the-Middle | All REST endpoints MUST use TLS 1.3+. Proximity sessions MUST use session encryption per ISO 18013-5:2021 §9. |
| Metadata Injection | Issuer metadata endpoints MUST be served over HTTPS. Implementations SHOULD validate metadata document integrity via sub-resource integrity or signed metadata JWT. |
| Offline Grace Abuse | `offline_grace_seconds` values MUST be logged in audit events when applied. A configurable alert threshold SHOULD be set for grace period usage frequency. |

### 20.6 Holder Binding Requirements

When a Compliance Profile sets `holder_binding_required: true`:

1. The issuer MUST include a `c_nonce` in the `TokenResponse` and require a `proof` object in the `CredentialRequest`.
2. The wallet MUST respond with a `proof` containing a holder-bound JWT signed by the holder's private key, including the `c_nonce` as the `nonce` claim.
3. The credential MUST be cryptographically bound to the holder's public key: `DeviceKey` for mDocs (ISO 18013-5 §7.2.2), `cnf.jwk` for SD-JWT-VC (IETF SD-JWT-VC §3.5).
4. Verifiers MUST verify the holder binding proof during presentation validation before accepting any presented claims.
5. A credential lacking holder binding MUST NOT be accepted by a verifier whose active Presentation Policy requires holder-bound presentations.

### 20.7 Normative Revocation Check Algorithm

For every credential in a verification flow, a verifier MUST perform the following steps:

1. Identify the `revocation_mechanism` from the Revocation Profile linked to the Presentation Policy's Trust Profile.
2. **For `BITSTRING_STATUS_LIST` or `STATUS_LIST_2021`:** Fetch the status list from `status_list_url`; decode the bitstring; verify the bit at `credential.credentialStatus.statusListIndex` is `0` (not revoked).
3. **For `OCSP`:** Send an OCSP request to the responder URL from the credential's AIA extension; validate the OCSP response signature; check `certStatus` is `good`.
4. **For `CRL`:** Fetch the CRL from the distribution point; verify CRL signature; confirm the credential serial number is not listed.
5. Apply `cache_ttl_seconds` caching. Cached results MUST be invalidated immediately if the status list URL returns a more recent version.
6. If the revocation check fails due to a network error and `offline_grace_seconds` has not elapsed since last successful check: log a warning on the audit event and proceed.
7. If `offline_grace_seconds` has elapsed: reject the credential with `error_code: REVOCATION_CHECK_FAILED`.
8. Record the revocation check outcome (mechanism, result, cache age, grace period applied) in the Audit Event for every verification.

---

## 21. Privacy Considerations

### 21.1 Data Minimization

Presentation Policies MUST be configured to request the minimum claims necessary. Where a boolean predicate suffices (e.g., `age_over_21`), implementations SHOULD NOT request the raw date of birth.

### 21.2 Selective Disclosure

Implementations MUST support selective disclosure for all credential formats that support it (SD-JWT-VC, mDoc). Claim-level `selectively_disclosable` flags MUST be respected.

### 21.3 Audit Logging

All issuance and verification events MUST be logged to Audit Events with sufficient detail for compliance reporting. Audit logs MUST NOT contain raw credential payload data.

### 21.4 Notification Payloads

Notification payloads (Section 15) MUST NOT include raw personal data. Credential offers MUST be delivered via OID4VCI URI references, not inline in push notification bodies.

### 21.5 Pairwise Subject Identifiers

Implementations SHOULD support pairwise pseudonymous identifiers that vary per verifier, preventing cross-verifier correlation of holder identity. When `allow_pairwise: true` is configured on a Trust Profile, issuers MUST NOT embed globally unique subject identifiers in issued credentials except where legally required by the governing compliance framework.

#### 21.5.1 Derivation Algorithm (Normative)

Pairwise identifiers MUST be computed using HMAC-SHA256 (RFC 2104) with the following inputs:

1. **Key**: A 256-bit (32-byte) cryptographically secure random secret, unique per holder. This secret MUST be generated at wallet provisioning using a CSPRNG and stored securely in the wallet's key store. The secret MUST NOT be derivable from the holder's subject identifier.

2. **Message**: The UTF-8 encoded concatenation of the verifier's `client_id` and the holder's subject identifier, separated by the ASCII colon character (U+003A):
   ```
   message = UTF-8(client_id) || 0x3A || UTF-8(subject_identifier)
   ```

3. **Input Normalization**:
   - `client_id` MUST be used exactly as registered in the verifier's Deployment Profile. No case folding, trimming, or percent-encoding normalization is applied.
   - `subject_identifier` MUST be the canonical DID or subject URI used in the credential's `credentialSubject.id` field. If the credential uses a DID, the DID MUST be in its canonical form per the applicable DID method specification.

4. **Output**: The 32-byte HMAC output MUST be encoded as URL-safe Base64 without padding (RFC 4648 Section 5). The resulting string is the pairwise subject identifier.

#### 21.5.2 Properties

- **Determinism**: The same holder MUST produce the same pairwise identifier for the same verifier across multiple presentations.
- **Unlinkability**: Different verifiers (`client_id` values) MUST receive different pairwise identifiers for the same holder, preventing cross-verifier correlation.
- **Non-reversibility**: Given a pairwise identifier and a `client_id`, it MUST be computationally infeasible to recover the holder's subject identifier without the holder-specific secret.

#### 21.5.3 Test Vector

```
Holder secret (hex):     0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b
client_id:               verifier.example.com
subject_identifier:      did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK
message (UTF-8):         verifier.example.com:did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK
HMAC-SHA256 output (hex): d98ba39822d3cfa26f718dd1b5872e99c083adc9cb24274c0d86460aa1d022f7
pairwise_id (base64url): 2YujmCLTz6JvcY3RtYcumcCDrcnLJCdMDYZGCqHQIvc
```

### 21.6 Unlinkability

| Credential Format | Unlinkability Support |
|---|---|
| `SD_JWT_VC` | Selective disclosure of claims reduces data exposure. Holder identity remains linkable across presentations to the same verifier unless pairwise pseudonyms are used. |
| `MDOC` | Per-request selective disclosure of data elements. MAC-based holder authentication (`DeviceAuth`) reduces linkability compared to signature-based binding. ZK presentations via `longfellow-libzk-v1` circuits provide unlinkable attribute disclosure (see §7.4). |
| `VC_JWT` | No native unlinkability. Callers MUST use pairwise pseudonyms to reduce cross-verifier correlation. |
| `JSON_LD` with BBS+ | Full unlinkable selective disclosure; BBS+ proofs are unlinkable by construction. RECOMMENDED for high-privacy use cases. Implementations MUST use `BBS_BLS12381_SHA256` or `BBS_BLS12381_SHAKE256` from `enums/validation-algorithms.json`. |

Implementations MUST document which credential formats they issue and their unlinkability properties in their conformance declaration (§22.3).

### 21.7 Data Retention Restrictions

- Verifiers MUST NOT retain raw credential payloads after a verification event is recorded. Audit events MUST contain only claim-level pass/fail results, not raw claim values, unless retention of raw values is required by applicable law.
- Applicant `application_data` MUST be treated as sensitive personal data. Implementations MUST provide a mechanism to delete applicant records and associated evidence upon request, subject to any legal retention obligations.
- Notification delivery systems MUST NOT log notification body content (which may include credential offer URIs). Only delivery metadata (timestamp, channel, status) SHOULD be retained.

---

## 22. Conformance

### 22.1 Implementation Conformance

A conformant MIP implementation MUST:

1. Implement all five core primitives (Trust Profile, Credential Template, Presentation Policy, Deployment Profile, Flow) with the required fields and validation rules.
2. Expose the API endpoints specified in Section 16.
3. Accept all valid fixtures in `/conformance/valid/`.
4. Reject all invalid fixtures in `/conformance/invalid/` with the error codes specified in their `.expected.json` sidecars.
5. Support at least one credential format from `credential-formats` enum.
6. Enforce all validation rules in Sections 5–15 and 17.

### 22.2 Partial Conformance

Implementations MAY claim partial conformance by identifying which entities they implement, provided they pass the corresponding conformance fixtures.

### 22.3 Implementation Classes

MIP defines four implementation classes. Claiming conformance to a class requires satisfying all MUST requirements for that class.

#### Issuer Implementation

| Feature | Requirement |
|---------|-------------|
| Create and manage Credential Templates | MUST |
| Implement at least one OID4VCI issuance flow | MUST |
| Validate Trust Profile before issuance | MUST |
| Publish `/.well-known/openid-credential-issuer` metadata | MUST |
| Publish `/.well-known/mip-configuration` discovery document | SHOULD |
| Support holder binding proofs when `holder_binding_required: true` | MUST |
| Support deferred credential issuance | MAY |
| Support `application_approval_issuance` flows | MAY |
| Pass `conformance/valid/` issuance fixtures | MUST |

#### Verifier Implementation

| Feature | Requirement |
|---------|-------------|
| Create and manage Presentation Policies | MUST |
| Implement at least one OID4VP or proximity verification flow | MUST |
| Execute full trust evaluation algorithm per §5.7.3 | MUST |
| Perform revocation checks per §20.7 | MUST |
| Log audit events for all verification results | MUST |
| Support cross-device OID4VP via `request_uri` | SHOULD |
| Support proximity mDL presentation (ISO 18013-5) | MAY |
| Pass `conformance/valid/` verification fixtures | MUST |

#### Wallet Implementation

| Feature | Requirement |
|---------|-------------|
| Store credentials in format-native secure storage | MUST |
| Accept OID4VCI credential offers (`pre-authorized_code` grant) | MUST |
| Respond to OID4VP presentation requests | MUST |
| Obtain holder consent before presenting any credential | MUST |
| Implement selective disclosure for SD-JWT-VC and mDoc | MUST |
| Use hardware-backed key storage for production credentials | SHOULD |
| Support BLE/NFC proximity engagement (ISO 18013-5) | MAY |

#### Registry Implementation

| Feature | Requirement |
|---------|-------------|
| Serve Trust Profile and Compliance Profile registry APIs | MUST |
| Publish `/.well-known/mip-configuration` | MUST |
| Implement SCIM 2.0 API for organization and user management | MUST |
| Serve revocation status lists | MUST (when RevocationProfile is ACTIVE) |
| Implement Applicant lifecycle API | SHOULD |
| Pass all `conformance/valid/` registry fixtures | MUST |

### 22.4 Protocol Conformance Targets

MIP defines five first-class protocol conformance targets. Each target corresponds to a system Compliance Profile and an integration test suite in the `marty-integration-tests` repository.

| Target | Compliance Code | Test Module | Standard Reference |
|--------|----------------|-------------|--------------------|
| **DTC** | `ICAO_DTC` | `test_oid4vci_issuer_conformance.py` + ICAODTCConformanceTest | ICAO Doc 9303 Part 13; OID4VCI §8 |
| **MRZ** | `ICAO_MRZ` | `test_icao_mrz_conformance.py` + MRZExtractionConformanceTest | ICAO Doc 9303 Parts 1–13 |
| **OpenBadge** | `OB3_JWT`, `OB3_JSONLD` | `test_openbadge_conformance.py` + OB3ConformanceTest | 1EdTech OB3 §8; W3C VCDM v2 |
| **OID4VC** | `OID4VC` | `test_oid4vci_issuer_conformance.py` + VCIIssuerHappyFlow; `test_oid4vp_verifier_conformance.py` | OID4VCI 1.0 Final; OID4VP 1.0 Final |
| **PEX** | `PEX` | `test_oid4vp_verifier_conformance.py` + test_verifier_presentation_definition_structure | DIF PE v2.0.0 |

#### 22.4.1 DTC Conformance

A conformant DTC implementation MUST:

- Issue ICAO DTC credentials in MDOC format with required namespaces `com.icao.dtc`.
- Include data group 1 (MRZ mirror), data group 2 (facial biometric), and Document Security Object.
- Sign with EC key using ES256 or ES384 algorithm.
- Expose OID4VCI pre-authorized flow endpoints per the `ICAO_DTC` compliance profile `api_surface`.
- Pass all DTC fixtures in `conformance/valid/` and reject all in `conformance/invalid/`.

#### 22.4.2 MRZ Conformance

A conformant MRZ implementation MUST:

- Parse TD1, TD2, and TD3 MRZ line formats per ICAO Doc 9303 Part 3.
- Validate all MRZ check digits using the algorithm in ICAO Doc 9303 Part 3 §4.3.
- Map parsed MRZ fields to claims in the `com.icao.mrz` namespace.
- Return structured MRZ verification results at the `/v1/flows/mrz/verify` endpoint.
- Reject documents where any check digit is invalid.

#### 22.4.3 OpenBadge Conformance

A conformant OpenBadge implementation MUST:

- Issue `jwt_vc_json` (OB3_JWT) credentials with `type` array including `OpenBadgeCredential`.
- Issue JSON-LD Linked Data Proof (OB3_JSONLD) credentials with the 1EdTech OB3 context.
- Support the 1EdTech Achievement Credential JSON-LD context at version ≥ 3.0.3.
- Include required claims: `name`, `issuer`, `validFrom`, `credentialSubject` with activity achievement.
- Expose OID4VCI metadata with `jwt_vc_json` format identifier in `credential_configurations_supported`.

#### 22.4.4 OID4VC Conformance (OIDF Certification Target)

A conformant OID4VC implementation MUST pass the OIDF conformance suite tests mirrored in
`test_oid4vci_issuer_conformance.py` and `test_oid4vp_verifier_conformance.py`:

- **VCIIssuerMetadataTest** — metadata endpoint returns all required OID4VCI 1.0 Final fields.
- **VCIIssuerHappyFlow** — full pre-authorized issuance flow succeeds with `credentials` array response.
- **VCIIssuerHappyFlow (dc+sd-jwt)** — SD-JWT VC issuance with `dc+sd-jwt` format identifier.
- **VCIIssuerHappyFlow (mso_mdoc)** — mDoc issuance with `mso_mdoc` format identifier.
- **OID4VPVerifierHappyFlow** — VP token submission accepted and verification result returned.
- **Nonce Endpoint** — `nonce_endpoint` returns unique `c_nonce` per request with `no-store` cache control.

Implementations SHOULD target OIDF Certification Program level **Issuer** and **Verifier** classes.

#### 22.4.5 PEX Conformance (DIF Presentation Exchange v2)

A conformant PEX implementation MUST:

- Include a `presentation_definition` conformant to DIF PE v2 §5 in every OID4VP authorization request.
- Each `presentation_definition` MUST have a string `id` and a non-empty `input_descriptors` array.
- Each `input_descriptor` MUST have `id` and `constraints.fields` with JSONPath `path` values.
- Supporting `filter` (JSON Schema) on each field is REQUIRED for implementations claiming PEX conformance.
- `submission_requirements` support is RECOMMENDED.
- Submitted `presentation_submission` MUST have `definition_id` matching the request `presentation_definition.id`.
- Submitted `descriptor_map` entries MUST use JSONPath `path` values referencing the VP token structure.

---

## 23. Versioning

See [VERSIONING.md](VERSIONING.md) for the full versioning policy.

This specification is at version **0.1.0 (Draft)**. Breaking changes may occur before 1.0.0.

### 23.1 Version Negotiation

All MIP messages MUST carry a `mip_version` field in the message envelope (see §26). Implementations that receive a message with an unsupported version MUST respond with `error_code: UNSUPPORTED_VERSION` and SHOULD include a `supported_versions` array in the error body.

The `/.well-known/mip-configuration` document MUST include a `supported_versions` array listing all versions the deployment can serve. Clients SHOULD inspect the discovery document before initiating a flow to confirm version compatibility.

Version negotiation uses a **highest-common-version** strategy: if both parties support overlapping versions, the higher common version MUST be used. If no overlap exists, the request MUST fail with `UNSUPPORTED_VERSION`.

---

## 24. Transport Bindings

### 24.1 Overview

MIP is transport-aware, not transport-agnostic. The protocol defines explicit transport bindings for each operation class. This section is normative.

### 24.2 Administrative API Transport

All CRUD operations on MIP entities (Trust Profile, Credential Template, Presentation Policy, Deployment Profile, Flow Definition, etc.) and organization management operations MUST be performed over:

- **Transport:** HTTPS (TLS 1.3+)
- **Protocol:** REST/JSON
- **Authentication:** OAuth 2.0 Bearer token
- **Path prefix:** `/v1/`

### 24.3 Credential Issuance Transports

| Flow Type | Required Transport | Reference |
|-----------|-------------------|-----------|
| `oid4vci_pre_authorized` | HTTPS REST per OID4VCI ≥Draft 13 | OID4VCI §6.1 |
| `oid4vci_authorization_code` | HTTPS REST per OID4VCI + OAuth 2.0 PKCE | OID4VCI §6.2 / RFC 7636 |
| `mdl_issuance` (online) | HTTPS REST, OID4VCI | ISO 18013-5 + OID4VCI |
| `mdl_issuance` (proximity) | ISO 18013-5 Part 8 BLE/NFC | ISO 18013-5:2021 §8 |
| `application_approval_issuance` | HTTPS REST | MIP §11 |
| `credential_renewal` | HTTPS REST, OID4VCI pre-authorized | OID4VCI §6.1 |
| `credential_revocation` | HTTPS REST | MIP §12 |

### 24.4 Credential Presentation Transports

| Flow Type | Required Transport | Reference |
|-----------|-------------------|-----------|
| `oid4vp_presentation` (cross-device) | HTTPS REST, OID4VP with `request_uri` | OID4VP §6 |
| `oid4vp_presentation` (same-device) | HTTPS redirect or custom URI scheme | OID4VP §7 |
| `mdl_presentation` (online) | HTTPS REST, OID4VP + ISO 18013-5 | OID4VP + ISO 18013-5 |
| `mdl_presentation` (proximity) | BLE or NFC per ISO 18013-5:2021 §8 | ISO 18013-5:2021 §8 |

### 24.5 Proximity Transport Requirements

For proximity-based mDL flows, implementations MUST:

- Implement device engagement per ISO 18013-5:2021 §8.2 (QR code or NFC tap).
- Implement session encryption per ISO 18013-5:2021 §9 (session keys derived from device and reader ephemeral keys).
- Implement at least one engagement method (QR code or NFC); supporting both is RECOMMENDED.
- Emit `DeviceEngagement`, `SessionEstablishment`, `DeviceRequest`, `DeviceResponse`, and `SessionTermination` messages per the catalog in §26.

### 24.6 Notification Transport

Notification delivery (§15) operates over implementation-chosen adapter transports:

- **FCM/APNs** — mobile push notifications (iOS/Android)
- **Server-Sent Events (SSE)** — web real-time delivery
- **HTTPS Webhooks** — server-to-server event delivery (HMAC-signed)
- **SMTP** — email delivery

Implementations MUST NOT use any notification transport to deliver credential material (see §15.7 and §20.5.2).

### 24.7 Protocol and Policy Separation

MIP enforces a strict separation between the **protocol layer** and the **policy layer**:

- The **protocol layer** defines message exchanges, state machines, transport bindings, and cryptographic validation rules (this specification).
- The **policy layer** comprises Presentation Policies, Trust Profiles, Compliance Profiles, and Cedar Policy Sets — persistent data objects that parameterize protocol behavior at runtime.
- The **authorization layer** uses Cedar policies (§16) to express access control, credential verification trust, and approval decisions in a formally verifiable language.

Transport-level message security (TLS, BLE session encryption) is a transport-layer concern. Credential-level cryptographic validation (signature verification, revocation checks, claim evaluation) is a protocol-layer concern. Presentation Policies define *what* is verified; the protocol defines *how* verification proceeds. Cedar Policy Sets define *who may act* and *under what conditions* — authorization decisions that are statically analyzable and auditable.

This separation ensures that MIP implementations remain stable while policies evolve independently, and that a change in policy (e.g., changing accepted credential formats or authorization rules) never requires a code change.

---

## 25. Governance

### 25.1 Specification Stewardship

The Marty Identity Protocol (MIP) is maintained by **the MIP maintainers**. The specification is published under the license at the canonical repository root. Changes to normative text require:

1. A written proposal describing the change, rationale, and affected sections.
2. Review for consistency with existing conformance fixtures.
3. A version increment per the policy in §23 and [VERSIONING.md](VERSIONING.md).
4. Publication of updated conformance fixtures in `/conformance/` alongside the specification change.

Proposals that add new normative requirements on existing entities MUST include a migration path for existing implementations to achieve continued conformance.

### 25.2 Extension Mechanism

Implementations MAY extend MIP without forking or modifying normative text through these mechanisms:

**Custom Compliance Profiles**
Organizations MAY define compliance profiles with `compliance_code: CUSTOM` and a defined `organization_id`. Custom profiles MUST NOT claim a reserved `compliance_code` value listed in the `compliance-codes` enum.

**Custom Trust Sources**
Organizations MAY define Trust Profile entries with `source_type: CUSTOM` to integrate identifier or key-management infrastructure not covered by the `ROOT_CA`, `TRUST_LIST`, or `PINNED_ISSUER` source types. The custom resolver is responsible for returning a verified public key (or set of keys) that the standard §5.7.3 signature-validation step can consume. As a concrete illustration, an event-sourced identifier system such as [KERI](https://keri.one/) would expose a key-state resolver that a `CUSTOM` trust source entry could reference; the remainder of the §5.7.3 algorithm is unchanged.

**Custom Flow Types**
Implementations MAY define additional flow types by prefixing with a reverse-domain namespace (e.g., `com.example.custom_enrollment`). Custom flow type identifiers MUST NOT conflict with normative values defined in §9.2.1. Custom flow types SHOULD follow the same step-sequence and state machine rules (§9.5, §9.9) as normative types.

**Claim Namespace Extensions**
Credential Templates MAY define claims in custom namespaces. The namespaces `org.iso.18013.5.1`, `org.aamva.16`, `urn:mip:`, and `eu.europa.ec.eudi.*` are reserved. Organizations SHOULD use their reverse-domain namespace for custom claims (e.g., `com.example.employee.*`).

**Webhook Event Extensions**
Implementations MAY emit custom event types prefixed with their reverse-domain namespace (e.g., `com.example.custom_event`). The event types in §15.5 are reserved.

**Custom Cedar Policies**
Organizations MAY define custom Cedar Policy Sets with `policy_type: CUSTOM` for authorization scenarios not covered by the three standard domains (Access Control, Credential Verification, Approval Rules). Custom policies MUST validate against the MIP Cedar schema (`cedar/mip.cedarschema`). Organizations MAY extend the Cedar schema with custom entity types and actions under their own namespace, but MUST NOT modify the `MIP` namespace.

### 25.3 System Compliance Profile Registry

System Compliance Profiles (§10, `is_system: true`) are maintained in the canonical repository under `compliance-profiles/`. Proposals to promote a custom profile to system status MUST provide:

1. A reference implementation with passing conformance fixtures in `/conformance/valid/`.
2. A normative specification reference (ISO standard, IETF RFC, W3C Recommendation, or government-published rule book).
3. A complete `api_surface` array with `standard_ref` for each endpoint.
4. Approval from the specification maintainers.

System profiles are immutable once merged. Changes that alter `credential_format`, `compliance_code`, or required claims MUST be published as a new profile entry with a new identifier rather than updating the existing entry.

### 25.4 Terminology Registry

Normative terms in §2 are controlled by this specification. Proposals to add terms require:

- A precise, protocol-relevant definition.
- A rationale explaining why the term is needed (avoidance of ambiguity, alignment with a referenced standard, etc.).
- Cross-references to any existing terms that relate to the new term.

---

## 26. Message Layer

This section provides a normative summary of the MIP message layer. Full message payload definitions and error codes are in [`protocol/messages/SPECIFICATION.md`](protocol/messages/SPECIFICATION.md).

### 26.1 Message Envelope

All MIP cross-party messages MUST conform to the message envelope defined in `protocol/messages/SPECIFICATION.md` §1. The envelope fields are:

| Field | Required | Description |
|-------|----------|-------------|
| `mip_version` | Yes | Protocol version string (e.g., `"0.1"`) |
| `message_type` | Yes | One of the message type identifiers in §26.2 |
| `message_id` | Yes | UUID unique within the deployment |
| `correlation_id` | No | `FlowInstance.id` linking messages in one flow |
| `timestamp` | Yes | ISO 8601 UTC creation timestamp |
| `nonce` | Conditional | REQUIRED for proof-bearing messages |
| `payload` | Yes | Message-specific payload object |
| `signature` | Conditional | JWS signature; REQUIRED for cross-party proof messages |

### 26.2 Message Types by Category

**Issuance:** `CredentialOffer`, `TokenRequest`, `TokenResponse`, `CredentialRequest`, `CredentialResponse`, `DeferredCredentialRequest`, `DeferredCredentialResponse`, `NotificationRequest`

**Verification:** `PresentationRequest`, `PresentationResponse`, `VerificationResult`

**Application:** `ApplicationSubmission`, `EvidenceRequest`, `EvidenceSubmission`, `ApplicantDecision`, `CredentialReadyNotification`

**Proximity:** `DeviceEngagement`, `SessionEstablishment`, `DeviceRequest`, `DeviceResponse`, `SessionTermination`

**Revocation:** `RevocationNotice`, `StatusListResponse`

### 26.3 Normative Message Rules

1. Messages MUST carry a unique `message_id`.
2. Nonces in proof-bearing messages MUST be single-use. Duplicated nonces MUST be rejected (see §20.5.2).
3. `timestamp` MUST be within `time_policy.clock_skew_seconds` of the receiver's current time.
4. `mip_version` MUST be validated before processing. Unsupported versions MUST be rejected with `error_code: UNSUPPORTED_VERSION` (see §23.1).
5. All messages in a flow instance MUST share the same `correlation_id`.

