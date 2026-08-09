# ADR 0003: Versioned device-key rotation with challenge-bound grace

**Date:** 2026-08-09
**Status:** Proposed
**Deciders:** MIP maintainers
**Tags:** security, device-registration, key-lifecycle, concurrency

## Context

MIP previously stored one public key on a Device Registration while saying the
"existing `key_valid_until`" kept the old key usable for in-flight challenges.
An upsert necessarily erased that old key, and the contract did not define an
in-flight challenge, grace ownership, replica concurrency, or revocation
precedence. Product code consequently attached a caller-provided deadline to
the replacement key and could not implement the promised grace behavior.

Registered device keys may authorize authentication, holder binding, approvals,
or notification actions. Permissive ambiguity can let an old key authorize new
work; overwrite-only behavior loses audit history and rejects legitimate
in-flight proofs.

## Decision

Device keys are immutable, versioned children of a Device Registration. Exactly
one key is `CURRENT`; prior keys transition through `RETIRING` to `RETIRED`, or
directly to `REVOKED`. Rotation is one compare-and-set transaction using the
authoritative storage clock and a server-bounded grace policy.

A retiring key is accepted only for an exact, single-use challenge issued before
the rotation commit and bound to that registration, key version/KID, purpose,
audience, and expiry. New challenges target only the current key. Deactivation
or revocation overrides grace immediately. Clients cannot select or extend a
retirement deadline.

The public Device Registration remains a current-key compatibility projection.
It exposes the current `key_version`; historical keys remain behind an
explicitly authorized audit or key-resolution boundary.

## Rationale

Versioned children preserve audit history and make the one-current-key invariant
enforceable with database constraints. Challenge binding distinguishes genuine
in-flight work from a new operation attempted with an old key. Server-owned time
and grace prevent retries, skewed replicas, or callers from extending authority.

## Alternatives considered

| Alternative | Why not chosen |
|-------------|----------------|
| Add `previous_public_key_der` to the registration | Supports only one rotation, has no monotonic concurrency rule, and repeats the overwrite problem. |
| Let callers set `key_valid_until` | Lets a key holder select or extend its own authorization lifetime and confuses new-key expiry with old-key grace. |
| Accept any old-key proof during grace | Turns grace into general authorization rather than recovery for an already-issued challenge. |
| Reject the old key immediately | Safe but contradicts the operational in-flight-challenge requirement. |

## Consequences

Positive:

- old-key authority is narrow, bounded, and independently auditable;
- concurrent rotations have one deterministic winner;
- deactivation and revocation have unambiguous precedence; and
- compatibility responses do not disclose complete key history.

Tradeoffs:

- implementations need owned schema migration and key-history storage;
- challenge records must carry exact key-version and purpose bindings; and
- consumers must handle rotation conflicts and the current key version.

## Implementation notes

Use a partial unique constraint for one current key per registration and a
monotonic unique `(registration_id, key_version)` constraint. Rotation should
lock or compare the expected current version, update the old row, insert the new
row, and append audit evidence in one transaction. Legacy single-key records
migrate as version 1 without inventing prior history. Verification computes an
effective retired state from the deadline even before background cleanup.

## Related

- Spec: §14.2, §14.5, §14.6, and §20.3
- Issue: Marty-Protocol/Marty-Protocol#34
- Implementation: ElevenID/marty-ui#345
