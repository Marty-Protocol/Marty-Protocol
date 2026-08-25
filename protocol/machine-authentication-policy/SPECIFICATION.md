# Machine Authentication Policy — Entity Specification

**Entity:** Machine Authentication Policy
**Version:** 0.6.0-draft
**Stability:** Dynamic
**Schema:** `schemas/machine-authentication-policy.json`

---

## Purpose

A Machine Authentication Policy defines the identity evidence a managed runtime must present before MIP evaluates an external-operation authorization request.

It governs:

- Required machine credential types
- Allowed machine types
- Proof-of-control methods and wire profiles
- Challenge, audience, replay, and proof-age checks
- Optional runtime attestation requirements
- The Cedar `MACHINE_AUTHORIZATION` PolicySet used after authentication

It does not govern domain execution controls.

## Authentication sequence

```text
resolve MachineIdentity
-> verify ACTIVE lifecycle state
-> verify required machine credentials
-> verify proof against an active registered key
-> validate challenge, audience, freshness, and replay state
-> appraise attestation result when required
-> verify attestation-to-identity-key binding
-> evaluate MACHINE_AUTHORIZATION policy
-> issue AuthorizationDecisionReceipt
```

Failure at any step MUST produce `DENY` and a privacy-safe audit event.

`challenge_required`, `audience_binding_required`, and `replay_detection_required` are mandatory and always true for machine proof freshness. When attestation is required, its challenge and identity-key binding controls are also mandatory and always true; an implementation cannot weaken these invariants through policy configuration.

## Machine binding

`MACHINE_KEY` proves control of an active key registered to a Machine Identity. `CREDENTIAL_KEY` permits a machine credential's subject key when the profile defines the association. `SESSION_BINDING` is limited to an authenticated session whose establishment proof is retained for audit.

Machine binding MUST NOT be reported as holder binding. A Verification Session result MUST NOT contain both `holder_binding_evidence` and `machine_binding_evidence`.

## Attestation

When `attestation_requirement.required` is true:

1. The result MUST use an accepted format.
2. Its verifier MUST chain to the referenced Trust Profile with purpose `ATTESTATION_VERIFIER`.
3. The result MUST be no older than `max_age_seconds`.
4. A required challenge MUST be authenticated by the evidence or attestation result.
5. When `identity_key_binding_required` is true, the appraisal result MUST bind the attested environment to the same machine identity key used for proof of control.

MIP consumes an attestation result. Hardware measurement, endorsement processing, and evidence appraisal remain responsibilities of the attestation system.

## Flow use

Until a standard machine-authentication FlowType is promoted through conformance, implementations MUST use `flow_type: custom` with a versioned extension based on a credential-presentation flow. The extension MAY reference a Machine Authentication Policy from its extension-owned `config`.

Such a flow authenticates a machine. It MUST NOT claim conformance to an external domain workflow.

## API

```text
GET    /v1/machine-authentication-policies
POST   /v1/machine-authentication-policies
GET    /v1/machine-authentication-policies/{id}
PATCH  /v1/machine-authentication-policies/{id}
POST   /v1/machine-authentication-policies/{id}/activate
POST   /v1/machine-authentication-policies/{id}/archive
```
