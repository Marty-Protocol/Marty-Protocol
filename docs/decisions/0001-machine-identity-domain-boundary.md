# ADR-0001: Machine identity without domain-workflow ownership

**Status:** Accepted
**Date:** 2026-07-28

## Context

Secure document systems and other protected-operation environments need to authenticate managed machines, bind credentials and attestation to device-controlled keys, and preserve signed authorization evidence. Secure cinema is a useful stress test because its runtime authorization depends on certified equipment, time-bound authorization, and externally enforced controls.

Modeling cinema assets, key-delivery messages, playback, watermarking, or recording investigations as MIP entities would move the protocol away from digital identity and secure documents.

## Decision

MIP adds:

- `MachineIdentity`
- `MachineAuthenticationPolicy`
- `AuthorizationDecisionReceipt`
- Purpose-scoped trust for machine identity and attestation
- Separate machine-binding evidence in Verification Session
- Cedar machine-authorization entities, context, and actions

MIP does not add:

- Protected media or generic asset resources
- Content-key authorization formats
- Playback or showing executions
- Watermark controls or results
- Recording or forensic-investigation records
- Cinema-specific FlowTypes

External domains use opaque action, resource, transaction, and result references. They remain responsible for interpreting and enforcing those identifiers.

## Consequences

- Secure document printers, personalization systems, HSM workloads, verifier appliances, and other managed runtimes gain a common identity model.
- Existing holder and device binding remain unchanged.
- Consumer wallets are not required to disclose stable machine identity.
- Runtime attestation can strengthen machine authentication without becoming a hardware-attestation protocol.
- Cinema and other domains can integrate with MIP without expanding MIP into domain resource management.

## Promotion rule

Domain-specific controls or evidence types may enter MIP core only when independently required by multiple identity or secure-document use cases and when their ownership and lifecycle fit an existing MIP abstraction.
