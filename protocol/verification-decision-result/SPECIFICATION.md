# Verification Decision Result — Entity Specification

**Entity:** Verification Decision Result

**Version:** 1.0.0

**Stability:** Draft

**Schema:** `schemas/verification-decision-result.json`

## Purpose

Verification Decision Result is the canonical, framework-neutral record of a
Marty verification decision. It preserves what processing completed, which
policy-required checks ran, what each check established, and which exact
software, policy, and trust artifacts produced the decision. It never contains
raw credentials, presentations, disclosed claim values, keys, or tokens.

Format adapters produce check results and evidence references. They do not set
the final decision. The versioned `mip.required-check-reducer` derives the
decision from processing status and required-check outcomes.

## Required-check reducer

The version 1.0.0 reducer is pure and deterministic:

1. `processing_status != COMPLETED` produces `INDETERMINATE`.
2. With completed processing, any required `FAILED` check produces `FAIL`.
3. Otherwise, any required `NOT_PERFORMED`, `UNSUPPORTED`, `ERROR`, or
   `NOT_APPLICABLE` check produces `INDETERMINATE`.
4. Otherwise every required check is `PASSED`, producing `PASS`.
5. At least one required check is mandatory; an empty or optional-only check
   set cannot pass.
6. The compatibility field `valid` is true if and only if the decision is
   `PASS`.
7. Check IDs are unique within one result. Duplicate identifiers are invalid
   even when the remaining fields differ.
8. Category summaries are reducer outputs. Their counts and outcome MUST match
   the canonical check set, with exactly one summary per represented category;
   callers cannot submit independent summaries.

Optional checks remain in the record but do not override the required-check
decision. A policy that wants an unavailable condition to deny access must
materialize a required failed policy check; an adapter must not silently turn
unavailability into success or failure.

## Check categories

The category vocabulary keeps distinct cryptographic and policy meanings:

- structure and document integrity;
- credential and presentation proofs;
- issuer trust, validity, and status/revocation;
- holder/device and transaction binding;
- claim constraints, biometrics, and final policy evaluation.

One passing proof cannot populate another category. For example, a valid outer
presentation signature is not issuer trust, credential proof, holder binding,
or status evidence.

## Transaction context

Online decisions require an organization, transaction identifier, and audience.
Offline decisions require a named offline authorization profile. Empty-string
transaction matching and ambient tenant selection are not valid contexts. The
two shapes are mutually exclusive: online results cannot carry an offline
profile, and offline results cannot carry online organization, transaction, or
audience fields. A caller cannot make authorization scope ambiguous by filling
both shapes.

## Provenance and privacy

Every result identifies exact policy and trust-profile versions and canonical
digests, the reducer version, and all software/adapter artifact digests.
`input_digest` and `evidence_digest` bind the result to transient inputs and
normalized evidence without retaining those inputs.

Component IDs are unique within the `components` list. Every check's
`component_id` MUST resolve to exactly one entry in that list; dangling or
ambiguous component references invalidate the result. This cross-array
referential-integrity rule is enforced by the canonical-result
builder/validator because JSON Schema cannot express it. Multiple checks MAY
reference the same declared component.

Check messages are bounded operator-safe text. Evidence references are opaque
URNs. They MUST NOT encode claim values, credential/presentation bytes, device
tokens, authorization values, keys, or free-form adapter exceptions.

## Compatibility and migration

Existing `VerificationSession.result`, `VerificationResultResponse`, format
booleans, and service-specific response objects remain compatibility
projections during migration. They are not additional decision authorities.
Writers migrate first to the canonical reducer; API, gRPC, Tauri, CLI, and audit
projections then derive legacy fields from the canonical result. Legacy `valid`
or `passed` inputs MUST NOT be expanded into trust, status, or binding checks.
