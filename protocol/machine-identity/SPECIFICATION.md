# Machine Identity — Entity Specification

**Entity:** Machine Identity
**Version:** 0.6.0-draft
**Stability:** Operational
**Schema:** `schemas/machine-identity.json`

---

## Purpose

A Machine Identity represents a managed non-human runtime that participates in identity or secure-document operations. Examples include document-personalization systems, secure document printers, HSM-backed issuer workloads, inspection kiosks, verifier appliances, and secure processing runtimes.

A Machine Identity answers:

```text
Which managed runtime is acting?
Which keys identify it?
Which organization and deployment are responsible for it?
Which identity credentials and endorsements apply to it?
What is its current lifecycle status?
```

It does not describe the domain resource being operated on, the domain operation's effects, or domain-specific execution controls.

## Privacy boundary

Machine Identity is for managed infrastructure. Implementations MUST NOT require a holder-controlled consumer wallet to create or disclose a stable Machine Identity merely because a credential uses `DEVICE_KEY` holder binding.

Holder binding and machine binding are distinct:

| Binding | Purpose | Stable machine identity |
|---|---|---|
| Holder binding | Proves control of a credential, device, or session key during presentation | Not required |
| Machine binding | Proves that a registered managed runtime controls its identity key | Required |
| Transaction binding | Binds a proof to a challenge and audience | Not inherently stable |

## Key binding

Every `identity_keys` entry MUST include a SHA-256 thumbprint. An `ACTIVE` machine MUST have exactly one `ACTIVE` identity key; rotation candidates remain `ROTATING` until an atomic promotion retires the prior key. Implementations MUST verify that machine credentials, machine proof-of-control, attestation results when required, and authorization decision receipts refer to the same active key or an explicitly governed rotation relationship.

An active machine MUST NOT authenticate with a key whose status is `REVOKED` or `EXPIRED`.

## Lifecycle

```text
PROVISIONED -> ACTIVE -> SUSPENDED -> ACTIVE
                     \-> REVOKED
                     \-> RETIRED
```

- `PROVISIONED`: identity exists but is not authorized for operational use.
- `ACTIVE`: eligible for authentication and policy evaluation.
- `SUSPENDED`: temporarily ineligible; reversible after review.
- `REVOKED`: permanently ineligible because identity or key trust has been withdrawn.
- `RETIRED`: intentionally removed from service.

Revoked machine identities MUST NOT return to `ACTIVE`. Suspension, revocation, retirement, key rotation, and assignment changes MUST emit audit events.

## Attestation identity

`attestation_identity` records identifiers, formats, and endorsements the machine can use when producing attestation evidence. It does not establish that the evidence is acceptable. Acceptance requirements belong to `MachineAuthenticationPolicy`, and appraisal is performed by a trusted external attestation verifier.

## API

```text
GET    /v1/machine-identities
POST   /v1/machine-identities
GET    /v1/machine-identities/{id}
PATCH  /v1/machine-identities/{id}
POST   /v1/machine-identities/{id}/activate
POST   /v1/machine-identities/{id}/suspend
POST   /v1/machine-identities/{id}/revoke
POST   /v1/machine-identities/{id}/retire
```

Machine identities are organization scoped. Cross-organization reads or mutations MUST fail closed.

## Domain boundary

External systems MAY use Machine Identity to authenticate an actor before performing a protected operation. MIP does not become the owner of the external resource or operation. In particular, a media-security integration remains responsible for content packages, key delivery, playback, forensic marking, and recording investigations.
