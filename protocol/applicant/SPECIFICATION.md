# Applicant — Entity Specification

**Entity:** Applicant
**Version:** 0.1.0
**Stability:** Draft
**Section in root spec:** §18

---

## Purpose

An Applicant represents a person or entity who has applied for a credential through an **application-approval flow** (`flow_type: application_approval_issuance`). The applicant entity provides:

- A structured lifecycle that demarcates submission, review, approval, and credential issuance as distinct, auditable states.
- A queue abstraction so organisations can manage pending and in-review applications without building their own state machine.
- A reviewer concurrency control mechanism (ReviewerLock) preventing conflicting decisions on the same record.
- Sub-resource attachment points for identity-vetting checks (VettingCheck) and biometric enrollment records (BiometricEnrollment).

Applicants are **not** the same as platform users (SCIM `User`). A platform user is an account; an applicant is a credential application. A single user MAY have multiple applicant records across different flows, and an applicant MAY exist without a corresponding user account.

---

## Lifecycle

### States

| State | Description |
|-------|-------------|
| `DRAFT` | Application started but not yet submitted by the applicant |
| `SUBMITTED` | Application submitted; awaiting reviewer pick-up |
| `UNDER_REVIEW` | A reviewer has acquired a ReviewerLock and is actively reviewing |
| `PENDING_INFORMATION` | Application paused pending additional information from the applicant |
| `APPROVED` | Reviewer has approved; pending credential issuance |
| `REJECTED` | Application rejected |
| `WITHDRAWN` | Applicant withdrew before a decision was reached |
| `CREDENTIALED` | Credential has been issued; terminal success state |
| `SUSPENDED` | Credential-holder has been suspended post-issuance |

### Transition Rules

```
DRAFT             → SUBMITTED          (applicant action: submit)
SUBMITTED         → UNDER_REVIEW       (reviewer action: acquire lock + begin review)
SUBMITTED         → WITHDRAWN          (applicant action: withdraw)
UNDER_REVIEW      → PENDING_INFORMATION (reviewer action: request more info)
UNDER_REVIEW      → APPROVED           (reviewer action: approve; lock required)
UNDER_REVIEW      → REJECTED           (reviewer action: reject; lock required)
UNDER_REVIEW      → WITHDRAWN          (applicant or reviewer action: withdraw)
PENDING_INFORMATION → UNDER_REVIEW     (applicant action: resubmit)
PENDING_INFORMATION → WITHDRAWN        (applicant or reviewer action: withdraw)
APPROVED          → CREDENTIALED       (system action: credential issuance succeeds)
APPROVED          → REJECTED           (system action: issuance failed after max retries)
CREDENTIALED      → SUSPENDED          (org admin action: suspend)
SUSPENDED         → CREDENTIALED       (org admin action: reinstate)
```

### Finality

`REJECTED`, `WITHDRAWN`, and `CREDENTIALED` are **quasi-terminal** states. An applicant MAY reapply by submitting a new applicant record — the rejected/withdrawn record is preserved for audit purposes and MUST NOT be mutated.

`CREDENTIALED` → `SUSPENDED` is permitted to support post-issuance lifecycle management (e.g., employee offboarding).

---

## ReviewerLock

### Purpose

Multiple reviewers may have access to the same applicant queue. The ReviewerLock prevents race conditions where two reviewers simultaneously attempt to approve or reject the same application.

### Acquisition and Release

- A reviewer MUST acquire a lock (`POST /v1/applicants/{id}/lock`) before performing any status-transition action (approve, reject, request-information).
- A lock is associated with a single `holder_user_id`.
- The default TTL is **1800 seconds (30 minutes)**. The maximum TTL is 7200 seconds (2 hours).
- A lock is automatically released when it expires. An explicit release endpoint (`DELETE /v1/applicants/{id}/lock`) allows early release.
- Only one `ACTIVE` lock may exist per applicant. An attempt to acquire a lock on an applicant with an active, non-expired lock MUST return `HTTP 409 Conflict` with error code `APPLICANT_LOCKED`.

### Heartbeat / Renewal

Implementations SHOULD support lock renewal via `POST /v1/applicants/{id}/lock/renew`, which resets the TTL. Renewal MAY be rejected if the caller is not the current lock holder.

### Queue Visibility

An applicant with `reviewer_id` populated shows as "in review" in the queue. Implementations MUST expose reviewer identity to other org members with the appropriate permission so that they can contact the reviewer rather than attempting to acquire a competing lock.

---

## VettingCheck Sub-Resource

VettingChecks are discrete identity-verification steps attached to an applicant. They are typically created automatically when the application is submitted (triggered by the flow's vetting configuration) or manually by a reviewer.

### Check Lifecycle

```
PENDING → IN_PROGRESS → PASSED
                      → FAILED
                      → INCONCLUSIVE
         → SKIPPED
         → EXPIRED
```

### Result Interpretation

| Status | Meaning |
|--------|---------|
| `PASSED` | Check passed the required threshold |
| `FAILED` | Check did not meet the threshold and constitutes a vetting failure |
| `INCONCLUSIVE` | Result is ambiguous; requires manual review |
| `SKIPPED` | Check was bypassed by policy or reviewer override |
| `EXPIRED` | Result is stale; check must be rerun |

### Evidence References

A VettingCheck MAY reference evidence artefacts (document captures, selfie images) by their storage reference ID. MIP stores only the reference; the artefact itself is held in the organisation's configured document storage.

---

## BiometricEnrollment Sub-Resource

BiometricEnrollment records capture that a biometric template was enrolled for an applicant. MIP stores only the **hash of the template**, not the raw biometric sample.

### Privacy Constraints (Normative)

1. Raw biometric samples (images, audio, sensor data) MUST be deleted immediately after template extraction by the capture SDK.
2. Raw samples MUST NOT be stored in MIP storage at any point.
3. Raw samples MUST NOT be transmitted via the MIP API in any request or response body.
4. `template_hash` MUST be computed over the provider-normalised template representation, not the raw sample.
5. `template_hash` alone MUST NOT be sufficient to reconstruct the biometric.

### Modality Uniqueness

An applicant SHOULD NOT have two `ENROLLED` BiometricEnrollment records for the same `modality`. When a new enrollment for an existing modality is created, the previous record MUST be transitioned to `SUPERSEDED`.

---

## Auto-Issue Strategy

When a flow's `approval_strategy` is `AUTO_APPROVE`, the system transitions the applicant directly from `SUBMITTED` to `APPROVED` and then to `CREDENTIALED` without human review, provided all automated VettingChecks return `PASSED`.

If any automated VettingCheck returns `FAILED` or `INCONCLUSIVE`, the auto-issue path MAY halt and escalate to manual review, depending on the flow's `auto_issue_on_check_failure` configuration.

---

## Organisation Queue

The applicant queue is the filtered view of all applicants within an organisation at a given status. Implementations MUST expose:

| Endpoint | Description |
|----------|-------------|
| `GET /v1/organizations/{org_id}/applicants` | Paginated applicant list with status/flow filters |
| `GET /v1/organizations/{org_id}/applicants?status=SUBMITTED` | Queue of unreviewed submissions |
| `GET /v1/organizations/{org_id}/applicants?status=UNDER_REVIEW` | Applications currently being reviewed |

The queue MAY be surfaced per-flow via `?flow_id=` filter.

---

## API Surface

### Applicant Resource

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/v1/organizations/{org_id}/applicants` | Org admin | Create a new applicant (pre-fill by staff) |
| `GET` | `/v1/organizations/{org_id}/applicants` | Org member | List applicants with filtering + pagination |
| `GET` | `/v1/organizations/{org_id}/applicants/{id}` | Org member | Get applicant by ID |
| `PATCH` | `/v1/organizations/{org_id}/applicants/{id}` | Reviewer (with lock) | Update applicant fields |
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/submit` | Applicant | Submit application |
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/approve` | Reviewer (with lock) | Approve application |
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/reject` | Reviewer (with lock) | Reject application |
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/request-information` | Reviewer (with lock) | Request more info |
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/withdraw` | Applicant or Org admin | Withdraw application |

### ReviewerLock Sub-Resource

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/lock` | Reviewer | Acquire reviewer lock |
| `DELETE` | `/v1/organizations/{org_id}/applicants/{id}/lock` | Lock holder | Release reviewer lock |
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/lock/renew` | Lock holder | Renew lock TTL |
| `GET` | `/v1/organizations/{org_id}/applicants/{id}/lock` | Org member | Get current lock status |

### VettingCheck Sub-Resource

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/v1/organizations/{org_id}/applicants/{id}/vetting-checks` | Reviewer | List vetting checks |
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/vetting-checks` | Reviewer | Create manual vetting check |
| `GET` | `/v1/organizations/{org_id}/applicants/{id}/vetting-checks/{check_id}` | Reviewer | Get vetting check detail |
| `PATCH` | `/v1/organizations/{org_id}/applicants/{id}/vetting-checks/{check_id}` | Reviewer | Update vetting check result |

### BiometricEnrollment Sub-Resource

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/v1/organizations/{org_id}/applicants/{id}/biometric-enrollments` | Reviewer | List enrollment records |
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/biometric-enrollments` | Org admin | Create enrollment record (hash only) |
| `DELETE` | `/v1/organizations/{org_id}/applicants/{id}/biometric-enrollments/{enroll_id}` | Org admin | Revoke enrollment record |

---

## Self-Service Applicant Portal

MIP implementations MAY expose a public-facing applicant portal where individuals apply without a pre-existing user account. In this case:

1. The applicant record is created without `user_id`.
2. Upon submission, the platform sends a notification to `email` or `phone` containing an applicant reference token.
3. The applicant uses the reference token to check status, provide additional information, or withdraw.
4. If the applicant later creates a user account, the `user_id` field MAY be backfilled via `PATCH /v1/organizations/{org_id}/applicants/{id}` by an org admin.

---

## Constraints

1. An Applicant MUST be associated with a flow whose `flow_type` is `application_approval_issuance`.
2. Status-transition actions (`approve`, `reject`, `request-information`) MUST NOT be accepted without an active ReviewerLock held by the requesting user, unless `approval_strategy` is `AUTO_APPROVE`.
3. BiometricEnrollment records MUST NOT contain `raw_biometric_data` or any derivative that allows template reconstruction.
4. Applicant records in `REJECTED`, `WITHDRAWN`, or `CREDENTIALED` state MUST NOT be deleted; they MUST be retained for the organisation's configured audit retention period.
5. A new VettingCheck of the same `check_type` supersedes older checks; the older check transitions to `EXPIRED`.

---

## Cross-References

| Referencing Entity | Reference Field | Behavior |
|--------------------|-----------------|----------|
| Flow | `flow_type: application_approval_issuance` | Governs applicant lifecycle |
| Credential Template | `application_template_id` | Template issued on approval |
| SCIM User | `user_id` | Optional account linkage |
| VettingCheck | `applicant_id` | Sub-resource |
| ReviewerLock | `applicant_id` | Sub-resource |
| BiometricEnrollment | `applicant_id` | Sub-resource |

## See Also

- Root specification: [§18 Applicant](../../SPECIFICATION.md#18-applicant)
- [schemas/applicant.json](../../schemas/applicant.json)
- [schemas/vetting-check.json](../../schemas/vetting-check.json)
- [schemas/reviewer-lock.json](../../schemas/reviewer-lock.json)
- [schemas/biometric-enrollment.json](../../schemas/biometric-enrollment.json)
