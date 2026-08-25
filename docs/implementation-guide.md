# MIP Implementation Guide

This guide walks implementors through integrating the Marty Identity Protocol into a new deployment. It covers entity creation order, required validations, API surface, and common patterns.

---

## Prerequisites

- Familiarity with OID4VCI and OID4VP specifications
- An active MIP-compatible gateway deployment
- Access to a MIP reference implementation or the MIP REST API
- Compliance profile IDs for the credential types you need (see `compliance-profiles/`)

---

## 1. Entity Creation Order

MIP entities reference each other and must be created in dependency order:

```
1. Trust Profile            (no dependencies)
2. Compliance Profile       (no dependencies — system profiles pre-exist)
3. Revocation Profile       (no dependencies)
4. Policy Set (Cedar)       (no dependencies — optional, for Cedar-based authorization)
5. Credential Template      (→ Trust Profile, Compliance Profile, Revocation Profile)
6. Presentation Policy      (→ Trust Profile, Credential Template)
7. Application Template     (→ Credential Template, optionally → Policy Set)
8. Deployment Profile       (→ Trust Profile, Presentation Policy)
9. Flow                     (→ Credential Template, Presentation Policy, Deployment Profile)
10. Machine Identity        (→ Deployment Profile; optional managed-runtime feature)
11. Machine Authentication Policy (→ Trust Profile, optionally → Policy Set)
```

Device Registration and Notification Target are operational entities created per user at runtime.
Machine Identity is an independent managed-infrastructure record and MUST NOT replace Device Registration or ordinary wallet holder binding.

---

## 2. Trust Profile Setup

### Minimum viable trust profile

```json
{
  "organization_id": "example-org-id",
  "name": "My Trust Profile",
  "trust_sources": [
    {
      "source_type": "PINNED_ISSUER",
      "issuer_did": "did:web:your-issuer.example.com"
    }
  ],
  "accepted_formats": ["SD_JWT_VC"],
  "accepted_algorithms": ["ES256"],
  "revocation_policy": {
    "check_mode": "HARD_FAIL"
  },
  "require_holder_binding": false,
  "status": "ACTIVE"
}
```

### For ICAO travel documents

Use `source_type: "PKD_URL"` for an approved ICAO PKD distribution endpoint or `source_type: "ROOT_CA"` for authenticated CSCA trust anchors. Distribution does not establish acceptance by itself; the verifier still needs an explicit trust policy. The `ICAO_DTC` Compliance Profile remains draft and has no active issuance transport.

### For AAMVA mDL

Use `source_type: "TRUST_LIST"` with the relevant IACA trust-list URL. Set `revocation_policy.check_mode: "HARD_FAIL"` — `SKIP` is prohibited for this credential type.

You can link a Cedar PolicySet for additional conditional trust evaluation:

```json
{
  "verification_policy_set_id": "<policy-set-uuid>"
}
```

See [Cedar Policies Documentation](cedar-policies.md) for policy authoring details.

---

## 3. Credential Template Setup

### Choosing a compliance profile

| Use case | compliance_profile_id | credential_format |
|----------|----------------------|-------------------|
| Internal badge/access | `cp-enterprise-vc` | `SD_JWT_VC` |
| ICAO Digital Travel Credential | `cp-icao-dtc` | `ICAO_DTC` (draft; no active issuance transport) |
| ICAO Machine Readable Zone | `cp-icao-mrz` | `ICAO_MRZ` (draft; parsing/check digits only) |
| ICAO TD3 ePassport | `cp-icao-passport` | `ICAO_EMRTD` (draft; no conformance claim) |
| US mDL | `cp-aamva-mdl` | `MDOC` (draft; no active issuance transport or conformance claim) |
| EU PID | `cp-eudi-pid` | `SD_JWT_VC` |
| EU mDL | `cp-eudi-mdl` | `MDOC` (draft; current rulebook mapping pending) |

### credential_type naming conventions

- VC and SD-JWT VC semantic types MUST be PascalCase:
  `EmployeeAccessBadge`, `PreBoardingClearance`
- ISO mdoc templates MUST use the reverse-domain ISO document type as both
  `credential_type` and `doctype`, for example `org.iso.18013.5.1.mDL`
- SHOULD be descriptive and globally unique within your organization
- Signing algorithms, keys, certificates, and custody providers are not
  Credential Template inputs; implementations resolve them from
  `organization_id` and `issuer_did`

### Claim naming conventions

- MUST be `snake_case`
- MUST start with a lowercase letter
- MUST match the pattern `^[a-z][a-z0-9_]*$`

---

## 4. Presentation Policy

### Setting predicate preferences

For age-gated use cases, set `prefer_predicates: true` and configure a `RANGE_PROOF` predicate on the age claim:

```json
{
  "claim_name": "age",
  "predicate": {
    "type": "RANGE_PROOF",
    "threshold": 21,
    "comparison": "GTE"
  },
  "fallback_policy": "ACCEPT_RAW"
}
```

For clearance-level gating, use `RANGE_PROOF` with `fallback_policy: "DENY"` — never accept a raw clearance level value.

### Holder binding

For high-assurance contexts (physical access, travel), set:
```json
"holder_binding": {
  "required": true,
  "binding_methods": ["DEVICE_KEY", "SESSION_BINDING"],
  "proof_profiles": ["MDOC_DEVICE_AUTHENTICATION"],
  "proof_freshness": {
    "challenge_required": true,
    "audience_binding_required": true,
    "replay_detection_required": true
  }
}
```

A nonce is proof-freshness input, not a binding method. The verifier validates it inside the authenticated proof defined by the selected proof profile.

---

## 5. Credential Issuance Flow

### OID4VCI Pre-Authorized Code (recommended)

1. Backend system calls Marty's issuance API to generate a pre-authorized code
2. Marty generates an OID4VCI offer URI: `openid-credential-offer://...?credential_offer=...`
3. Marty calls the Notification Target delivery API with the offer URI  
   ⚠️ **The offer URI is the only thing in the notification — never the credential itself**
4. User receives push notification, taps to open wallet
5. Wallet exchanges pre-authorized code for credential
6. Credential stored in wallet

### OID4VCI Authorization Code

Use this when the user is actively present in your application:

1. Backend generates authorization request
2. User authenticates in your IdP (Keycloak, etc.)
3. Redirect delivers `code` to wallet
4. Wallet exchanges code at credential endpoint

---

## 6. Device Registration

Register devices on first app launch and on any FCM token rotation:

```json
{
  "user_id": "string",
  "device_id": "string (app instance UUID, stable across re-opens)",
  "device_name": "User's iPhone 15",
  "platform": "ios",
  "fcm_token": "current FCM token",
  "app_version": "1.2.3"
}
```

The API uses upsert semantics on `(user_id, device_id)` — safe to call on every app launch.

### RSA Challenge-Response (high-assurance)

For high-assurance flows, include a device RSA public key for challenge-response verification:

```json
{
  "public_key_der": "base64url-encoded PKCS#1 DER",
  "public_key_kid": "RFC 7638 JWK Thumbprint"
}
```

`public_key_kid` is REQUIRED when `public_key_der` is present.

---

## 7. Notification Delivery

### Notification Target creation

Create a Notification Target per user, specifying all delivery channels:

```json
{
  "user_id": "user-id",
  "channels": [
    {"type": "FCM", "device_id": "device-id", "enabled": true},
    {"type": "SSE", "enabled": true}
  ],
  "preferences": {
    "priority_minimum": "NORMAL"
  }
}
```

### Delivering a credential offer

POST to `/v1/notifications/send`:

```json
{
  "user_id": "user-id",
  "event_type": "CREDENTIAL_OFFER",
  "priority": "HIGH",
  "data": {
    "offer_uri": "openid-credential-offer://..."
  }
}
```

The gateway routes the notification to all active channels for the user. Credential data MUST NOT appear in `data`.

---

## 8. Verification Flow

### Initiating verification at a deployment device

1. Device sends a presentation request to the gateway with `policy_id` and `deployment_profile_id`
2. Gateway generates a nonce and returns an OID4VP request
3. Wallet presents the credential with a holder binding proof
4. Gateway validates:
   - Trust chain via Trust Profile
   - Credential format and algorithm
   - Predicate constraints
   - Revocation status (per Revocation Profile)
   - Holder binding proof
5. Gateway returns a verification result to the device

### Reading a verification result

```json
{
  "session_id": "vs-...",
  "status": "VERIFIED",
  "presented_claims": {
    "member_id": "12345",
    "tier": "GOLD"
  },
  "verified_at": "2026-03-11T12:00:00Z"
}
```

---

## 9. Validation

### Schema validation

Validate your entity payloads against the JSON Schemas in `schemas/`:

```sh
./scripts/validate.sh --schema schemas/credential-template.json --data your-template.json
```

### Conformance testing

Run the full conformance suite against your implementation:

```sh
./scripts/run-conformance.sh --endpoint https://your-marty-instance.example.com
```

---

## 10. Common Mistakes

| Mistake | Correct Approach |
|---------|-----------------|
| `credential_type: "myCredential"` | Must be PascalCase: `"MyCredential"` |
| MDOC template without `doctype` | Set both `credential_type` and `doctype` to the reverse-domain ISO document type |
| Including credential data in FCM notification | Include only the OID4VCI offer URI |
| `fallback_policy: "DENY"` + `fallback_claim_name` set | DENY means no fallback; remove `fallback_claim_name` |
| Missing `public_key_kid` when setting `public_key_der` | Compute RFC 7638 JWK Thumbprint and include it |
| Empty `policy_ids` array in Deployment Profile | Must reference at least one Presentation Policy |
| Setting `revocation_policy.check_mode: "SKIP"` on ICAO/AAMVA/EUDI | `SKIP` is prohibited; use `SOFT_FAIL` with `OFFLINE_GRACE` timing for offline tolerance |
| Modifying a system Compliance Profile | System profiles are immutable; create a `CUSTOM` profile if you need customization |
| Using opaque JSON for `approval_rules` | Migrate to Cedar PolicySet with `approval_policy_set_id` (see `docs/cedar-policies.md`) |
| Writing authorization logic in application code | Express authorization as Cedar policies in a PolicySet and evaluate at runtime |

---

## 11. Reference

- Full normative specification: [`SPECIFICATION.md`](../SPECIFICATION.md)
- JSON Schemas: [`schemas/`](../schemas/)
- Enum vocabularies: [`enums/`](../enums/)
- Realistic examples: [`examples/realistic/`](../examples/realistic/)
- Compliance profiles: [`compliance-profiles/`](../compliance-profiles/)
- Glossary: [`docs/glossary.md`](glossary.md)
- Cedar policies: [`docs/cedar-policies.md`](cedar-policies.md)
- Cedar schema: [`cedar/mip.cedarschema`](../cedar/mip.cedarschema)
