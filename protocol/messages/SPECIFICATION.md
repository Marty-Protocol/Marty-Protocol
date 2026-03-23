# Protocol Messages — Specification

**Entity:** Protocol Messages
**Version:** 0.1.0
**Stability:** Draft
**Section in root spec:** §4 (Message Layer)

---

## Overview

Every MIP protocol exchange is carried by a typed **message**. This document defines the normative message envelope, the full catalog of message types, the fields each message type carries, and the flow steps that produce and consume each message.

Messages are the atomic units of protocol behavior. Unlike MIP entities (Trust Profile, Credential Template, etc.) which are persistent store objects, messages are transient: they are produced at a step transition, consumed by the next party, and then retained only as audit evidence.

---

## 1. Message Envelope

All MIP messages MUST be wrapped in the following envelope when transmitted between separately-operated parties (e.g., Issuer ↔ Wallet, Verifier ↔ Wallet). Internal step-to-step transitions within a single gateway implementation MAY omit the envelope.

### 1.1 Envelope Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mip_version` | string | Yes | Protocol version. MUST be `"0.1"` for this spec revision. |
| `message_type` | MessageType | Yes | Identifies the message (see §2). |
| `message_id` | UUID | Yes | Unique identifier for this message instance. |
| `correlation_id` | UUID | No | Links messages belonging to the same flow instance. Set to `FlowInstance.id`. |
| `timestamp` | datetime | Yes | ISO 8601 UTC timestamp of message creation. |
| `sender_id` | string | No | Identifier of the sending party (DID, organization ID, or service identifier). |
| `nonce` | string | Conditional | Single-use cryptographic nonce. REQUIRED for messages that carry proofs or bind holder responses. Min 128 bits, base64url-encoded. |
| `payload` | object | Yes | Message-specific payload (see §3). |
| `signature` | object | No | JWS detached signature over the canonical payload (see §1.2). |

### 1.2 Envelope Signature

When `signature` is present it MUST be a JSON object with fields:

| Field | Type | Description |
|-------|------|-------------|
| `alg` | string | JWA algorithm identifier (e.g., `ES256`) |
| `kid` | string | Key identifier of the signing key |
| `value` | string | Base64url-encoded JWS signature over `SHA-256(canonical(payload))` |

Signature is OPTIONAL for administrative messages (where TLS client auth is used) and REQUIRED for cross-party messages that carry holder proofs or issuer assertions.

---

## 2. Message Type Catalog

### 2.1 Issuance Messages

| `message_type` | Direction | Step | Description |
|----------------|-----------|------|-------------|
| `CredentialOffer` | Issuer → Holder | `create_offer` | OID4VCI credential offer (by reference or by value) |
| `TokenRequest` | Holder → Issuer | `token_exchange` | OAuth2 token request (pre-authorized or auth code) |
| `TokenResponse` | Issuer → Holder | `token_exchange` | Access token + optional `c_nonce` |
| `CredentialRequest` | Holder → Issuer | `credential_request` | OID4VCI credential request with holder proof |
| `CredentialResponse` | Issuer → Holder | `issue_credential` | Signed credential or deferred acceptance ID |
| `DeferredCredentialRequest` | Holder → Issuer | `deferred_retrieve` | Poll for deferred credential |
| `DeferredCredentialResponse` | Issuer → Holder | `deferred_retrieve` | Deferred credential payload or pending status |
| `NotificationRequest` | Wallet → Issuer | `notify` | OID4VCI holder notification of credential storage result |

### 2.2 Verification Messages

| `message_type` | Direction | Step | Description |
|----------------|-----------|------|-------------|
| `PresentationRequest` | Verifier → Holder | `create_request` | OID4VP authorization request |
| `PresentationResponse` | Holder → Verifier | `presentation_submission` | VP token + descriptor map |
| `VerificationResult` | Verifier → Relying Party | `verify_presentation` | Pass/fail + claim-level results |

### 2.3 Application / Approval Messages

| `message_type` | Direction | Step | Description |
|----------------|-----------|------|-------------|
| `ApplicationSubmission` | Applicant → Issuer | `accept_application` | Application form data + evidence references |
| `EvidenceRequest` | Issuer → Applicant | `validate_evidence` | Request for additional documentation |
| `EvidenceSubmission` | Applicant → Issuer | `validate_evidence` | Evidence payload in response to `EvidenceRequest` |
| `ApplicantDecision` | Reviewer → System | `approval_decision` | Approval or rejection with reason code |
| `CredentialReadyNotification` | Issuer → Applicant | `deliver_credential` | Notification that credential is available for collection |

### 2.4 Proximity (ISO 18013-5) Messages

| `message_type` | Direction | Step | Description |
|----------------|-----------|------|-------------|
| `DeviceEngagement` | Reader → Device | `device_engagement` | QR or NFC engagement payload per ISO 18013-5 §8.2 |
| `SessionEstablishment` | Reader → Device | `session_establishment` | Session keys and reader engagement |
| `DeviceRequest` | Reader → Device | `request_items` | mDoc request payload with namespaces and data elements |
| `DeviceResponse` | Device → Reader | `response_items` | mDoc response payload |
| `SessionTermination` | Either | `session_termination` | Close session flag |

### 2.5 Revocation Messages

| `message_type` | Direction | Step | Description |
|----------------|-----------|------|-------------|
| `RevocationNotice` | Issuer → Holder | `notify` | Out-of-band revocation notice (non-normative; advisory only) |
| `StatusListResponse` | Issuer → Verifier | (discovery) | IETF Bitstring Status List payload |

---

## 3. Message Payload Definitions

### 3.1 CredentialOffer

Conforms to OID4VCI §4.1. MIP adds the following extension field:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `credential_issuer` | URI | Yes | Issuer base URL |
| `credential_configuration_ids` | string[] | Yes | Offered credential configuration identifiers |
| `grants` | object | Yes | Pre-authorized or authorization code grant parameters |
| `mip_flow_instance_id` | UUID | No | MIP-extension: links offer to a FlowInstance for audit correlation |

Implementations MUST set `mip_flow_instance_id` when the offer is generated from a MIP Flow. Wallets MUST store this value and include it in `correlation_id` on subsequent issuance messages.

### 3.2 TokenRequest

Conforms to RFC 6749. For pre-authorized flows, the `pre-authorized_code` grant type is used per OID4VCI §6.1.

### 3.3 TokenResponse

Conforms to RFC 6749. MUST include `c_nonce` and `c_nonce_expires_in` when the issuer requires a holder binding proof on the subsequent credential request.

### 3.4 CredentialRequest

Conforms to OID4VCI §7.2. MUST include a `proof` object when `holder_binding_required: true` in the Compliance Profile. The proof MUST use the `c_nonce` received in the `TokenResponse`.

The `proof` object MUST contain:

| Field | Type | Description |
|-------|------|-------------|
| `proof_type` | string | `jwt` or `cwt` |
| `jwt` | string | Signed JWT with `iss` (holder DID or key thumbprint), `aud` (issuer URL), `iat`, and `nonce` (`c_nonce` value) |

### 3.5 CredentialResponse

Conforms to OID4VCI §7.3. Contains either:
- `credential`: the signed credential (base64url mDoc CBOR or SD-JWT string)
- `transaction_id`: deferred issuance identifier

### 3.6 PresentationRequest

Conforms to OID4VP §5. MIP-specific extension fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `client_id` | string | Yes | Verifier identifier |
| `response_type` | string | Yes | `vp_token` |
| `presentation_definition` | object | Yes | W3C Presentation Exchange definition |
| `nonce` | string | Yes | Server-generated random nonce; single-use |
| `mip_flow_instance_id` | UUID | No | MIP-extension: links request to FlowInstance |
| `mip_policy_id` | UUID | No | MIP-extension: Presentation Policy ID that generated this request |

### 3.7 PresentationResponse

Conforms to OID4VP §6. MUST be encrypted with the verifier's public key in cross-device flows when `jarm` response mode is used.

### 3.8 VerificationResult

MIP-proprietary message (internal). Produced by the verification engine after executing trust evaluation (§5.7.3).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `flow_instance_id` | UUID | Yes | The FlowInstance that generated this result |
| `policy_id` | UUID | Yes | Presentation Policy that was evaluated |
| `overall_result` | string | Yes | `PASS` or `FAIL` |
| `claim_results` | ClaimResult[] | Yes | Per-claim evaluation results |
| `trust_chain_valid` | boolean | Yes | Whether issuer trust chain validated |
| `revocation_checked` | boolean | Yes | Whether revocation was checked |
| `revocation_status` | string | No | `VALID`, `REVOKED`, `UNKNOWN`, `SKIPPED` |
| `evaluated_at` | datetime | Yes | ISO 8601 UTC |
| `verifier_nonce` | string | Yes | The nonce from the `PresentationRequest` (for replay detection) |

#### ClaimResult

| Field | Type | Description |
|-------|------|-------------|
| `claim_name` | string | Claim identifier |
| `required` | boolean | Whether the claim was required by policy |
| `present` | boolean | Whether the claim was present in the presentation |
| `satisfies_predicate` | boolean | Whether any predicate on the claim was satisfied |
| `result` | string | `PASS`, `FAIL`, `SKIPPED` |

### 3.9 ApplicationSubmission

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `flow_id` | UUID | Yes | The `application_approval_issuance` Flow this submission targets |
| `applicant_id` | UUID | No | Pre-existing applicant record ID (for resubmissions) |
| `form_data` | object | Yes | Key-value pairs matching the ApplicationTemplate field names |
| `evidence_references` | string[] | No | URIs to uploaded evidence documents |
| `submitted_at` | datetime | Yes | ISO 8601 UTC |

### 3.10 ApplicantDecision

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `applicant_id` | UUID | Yes | Applicant record being decided |
| `reviewer_id` | UUID | Yes | Reviewer user ID making the decision |
| `decision` | string | Yes | `APPROVED` or `REJECTED` |
| `reason_code` | string | No | Rejection reason code (see Applicant schema) |
| `reason_text` | string | No | Free-text explanation |
| `decided_at` | datetime | Yes | ISO 8601 UTC |

---

## 4. Normative Constraints

1. All messages MUST carry a `message_id` that is unique within the lifetime of the MIP deployment.
2. Messages bearing a `nonce` MUST be validated as single-use. Implementations MUST reject any message where a previously-seen `nonce` value is reused.
3. All messages in a flow instance MUST share the same `correlation_id` (set to the `FlowInstance.id`).
4. `timestamp` MUST be within the clock skew window of the receiving party. Messages older than `time_policy.clock_skew_seconds` from the expected time MUST be rejected.
5. `mip_version` MUST be validated before processing. If the receiver does not support the declared version, it MUST return an error with `error_code: UNSUPPORTED_VERSION` (see §21 / §22.2 for version negotiation).
6. Message envelope signatures MUST be validated when present. If a signature is present and invalid, the message MUST be rejected regardless of payload validity.

---

## 5. Error Response Envelope

When processing fails, the responding party MUST return a structured error:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `error` | string | Yes | Machine-readable error code |
| `error_description` | string | No | Human-readable error description |
| `message_id` | UUID | Yes | The `message_id` of the failed message |
| `correlation_id` | UUID | No | The `correlation_id` from the failed message |

### Standard Error Codes

| Code | Meaning |
|------|---------|
| `invalid_message` | Malformed envelope or required field missing |
| `unsupported_version` | `mip_version` not supported by receiver |
| `invalid_proof` | Holder binding proof is invalid or missing |
| `nonce_reused` | The `nonce` value has been seen before |
| `issuer_untrusted` | Issuer could not be validated against trust anchors |
| `revocation_check_failed` | Revocation could not be confirmed |
| `credential_revoked` | The presented credential has been revoked |
| `policy_not_satisfied` | Required claims missing or predicates failed |
| `expired_message` | `timestamp` is outside allowed clock skew |
| `unauthorized` | Sender is not authorized to perform this operation |

---

## See Also

- Root specification: [§4 Protocol Overview and Message Layer](../../SPECIFICATION.md#4-protocol-overview)
- Flow state machine: [§9.9 Flow Instance State Machine](../../SPECIFICATION.md#9-flow)
- Transport bindings: [§22 Transport Bindings](../../SPECIFICATION.md#22-transport-bindings)
- Security considerations: [§18 Security Considerations](../../SPECIFICATION.md#18-security-considerations)
