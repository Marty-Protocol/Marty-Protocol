# Authorization Decision Receipt — Entity Specification

**Entity:** Authorization Decision Receipt
**Version:** 0.6.0-draft
**Stability:** Immutable operational record
**Schema:** `schemas/authorization-decision-receipt.json`

---

## Purpose

An Authorization Decision Receipt is a signed, privacy-safe record that MIP authenticated a principal and evaluated an identity-bound authorization request.

The receipt binds:

```text
principal identity
+ principal proof key or session
+ challenge and audience
+ opaque external action and resource identifiers
+ policy version
+ relevant identity evidence references
+ decision and lifetime
```

The receipt is evidence of MIP's decision. It is not a capability token unless an external profile explicitly defines it as one, and it never transfers ownership of the external resource or operation to MIP.

## External identifiers

`action` is a URI controlled by the external domain. `resource_id` is opaque to MIP. Implementations MUST compare both as exact strings and MUST NOT infer privileges from URI path hierarchy.

`external_context` exists only for correlation. Domain payloads, encryption keys, protected document contents, media metadata, execution obligations, or forensic evidence MUST NOT be embedded.

## Binding

For `CREDENTIAL_KEY`, `DEVICE_KEY`, and `MACHINE_KEY`, `principal_key_thumbprint` is required. The receipt signer MUST verify proof of control before issuing `PERMIT`.

For `MACHINE_KEY`, the thumbprint MUST identify an active key on the referenced Machine Identity. If attestation is required, `attestation_result_digest` and `identity_key_bound: true` MUST be recorded.

The challenge MUST be single use and the receipt MUST record `replay_checked: true`. The audience MUST identify the intended external relying party. Every receipt MUST carry a non-null expiry; a receipt replayed to another audience or outside its validity interval MUST be rejected. `MACHINE_KEY` receipts MUST record a non-null active-key thumbprint and `identity_key_bound: true`.

## Signature and immutability

Receipts are immutable after issuance. The signature covers all fields except transport metadata added outside the receipt. Implementations MUST retain the canonical policy version digest and enough identity-evidence references to reproduce or audit the decision without storing raw credential or attestation payloads.

## Domain enforcement boundary

The relying domain system:

1. Verifies the receipt signature, audience, decision, and expiry.
2. Confirms the action, resource, and external transaction correlation.
3. Applies its own domain policy.
4. Performs or denies the external operation.

For a secure cinema integration, the cinema system remains responsible for KDM generation, content keys, playback windows, projection, forensic marking, logs, and recording investigations. Marty provides machine identity and the identity-bound decision only.

## API

```text
POST  /v1/authorization-decisions/evaluate
GET   /v1/authorization-decisions/{id}
GET   /v1/organizations/{id}/authorization-decisions
```

Evaluation responses MUST include a signed receipt for both `PERMIT` and `DENY`. Receipt access MUST be organization scoped and audited.
