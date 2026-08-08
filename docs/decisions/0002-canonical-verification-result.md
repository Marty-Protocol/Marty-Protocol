# ADR 0002: Canonical verification result and required-check reducer

- Status: Proposed
- Date: 2026-08-08
- Decision owners: Marty Protocol and verification maintainers
- Tracking: GitHub issue #32

## Context

Marty repositories currently expose incompatible verification booleans, status
enums, evidence objects, and reducers. Information is lost at adapter and API
boundaries, allowing one generic validity value to be reinterpreted as issuer
trust, revocation, holder binding, or policy success even when those checks did
not run.

## Decision

`marty-protocol` owns the versioned external Verification Decision Result wire
contract. `marty-core` will own the framework-neutral domain types and pure
`mip.required-check-reducer` implementation. Format adapters emit explicit
checks and evidence references only. Services and user interfaces project the
canonical result; they do not independently reduce it.

The reducer has exactly three decisions: `PASS`, `FAIL`, and `INDETERMINATE`.
PASS requires completed processing and every required check passed. Required
failures produce FAIL. Required unresolved checks or incomplete processing
produce INDETERMINATE. Vacuous success is forbidden and `valid` is derived.

Policy, trust, transaction, software, adapter, input-digest, and evidence-digest
provenance are mandatory. Raw credentials, presentations, claim values, tokens,
keys, and unbounded exception text are prohibited from the result.

The reducer also rejects duplicate check/component/category identifiers and
derives category summaries from the check set. JSON Schema enforces the core
decision/outcome invariants; the pure reducer enforces cross-item uniqueness and
summary arithmetic that JSON Schema cannot express.

## Consequences

- Format-specific details remain available as transient or separately governed
  evidence, but cannot set the final decision.
- Cross-language golden vectors can exercise one reducer and serialization
  contract.
- Existing public responses require a bounded compatibility period and explicit
  derived mappings.
- Consumers must preserve unknown/unperformed outcomes instead of collapsing
  them to booleans.
- Coordinated releases and exact dependency pins are required before capability
  claims move to the new contract.

## Rejected alternatives

- Keeping per-service reducers preserves the current information-loss defect.
- Reusing the authorization-decision receipt conflates document verification
  evidence with a separate identity-bound authorization decision.
- Treating every missing check as failure loses availability semantics; treating
  it as pass is fail-open. `INDETERMINATE` preserves the distinction.
- Carrying raw claims in the result violates the verification data-lifecycle
  boundary and increases breach and correlation impact.
