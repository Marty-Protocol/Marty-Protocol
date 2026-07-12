# Applicant Application Specification

**Entity:** ApplicantApplication
**Version:** 0.3.0
**Stability:** Draft

## Purpose

An ApplicantApplication is a holder-owned request for a credential. It is created from an active ApplicationTemplate. The server derives the applicant profile, CredentialTemplate, issuer organization, required checks, approval strategy, validity, and claim mappings. Public clients cannot override those values.

The authenticated user owns the applicant profile. The application's persisted `organization_id` is authoritative for reviewer authorization; query parameters and a UI-selected organization never establish ownership.

## Creation Contract

`POST /v1/me/applications`

```json
{
  "organization_id": "uuid",
  "application_template_id": "uuid",
  "form_data": {},
  "integration_context": {}
}
```

The request MUST reject `applicant_id`, `credential_configuration_id`, `issuing_authority`, `required_checks`, reviewer identity, and generic `metadata`. `form_data` MUST be validated against the active ApplicationTemplate on creation and submission. Date values use ISO `YYYY-MM-DD`.

Validation failures return HTTP 422:

```json
{
  "error": "FIELD_VALIDATION_FAILED",
  "message": "Application data failed validation.",
  "details": {
    "field_errors": [
      {"field": "birth_date", "code": "INVALID_DATE", "message": "Use an ISO date in YYYY-MM-DD format."}
    ]
  }
}
```

## Lifecycle And Claim Readiness

Application lifecycle and claim readiness are separate state machines. An application remains `APPROVED` when the issuer is not ready to create an offer.

| Claim state | Meaning |
|---|---|
| `NOT_READY` | The application has not been approved. |
| `BLOCKED` | Approval exists, but a named owner must resolve a blocker. |
| `OFFER_READY` | A non-expired credential offer is available. |
| `CLAIMED` | Wallet issuance completed. |
| `EXPIRED` | The offer expired and must be regenerated. |

`claim_blocker` contains a machine code, an owner (`APPLICANT`, `ISSUER`, or `SYSTEM`), and a privacy-safe message. Failure to locate an active issuance flow MUST persist `BLOCKED / NO_ACTIVE_ISSUANCE_FLOW / ISSUER` without changing application status from `APPROVED`.

## Canonical API

### Self Service

| Method | Path | Description |
|---|---|---|
| `GET`, `PATCH` | `/v1/me/applicant-profile` | Read or update the caller's profile. |
| `GET`, `POST` | `/v1/me/applications` | List or create the caller's applications. |
| `GET` | `/v1/me/applications/{id}` | Read an owned application. |
| `POST` | `/v1/me/applications/{id}/submit` | Validate and submit. |
| `POST` | `/v1/me/applications/{id}/withdraw` | Withdraw an owned application. |
| `POST` | `/v1/me/applications/{id}/claim` | Generate an offer for an approved owned application. |

### Organization Review

All routes are authorized against the resource's persisted organization. Queue, detail, checks, locks, and information requests require `application:review`. Approval and rejection require their explicit permissions and the caller's active lock. Operator issuance requires `issuance:initiate`.

| Method | Path | Description |
|---|---|---|
| `GET` | `/v1/organizations/{org_id}/applicants` | Review queue. |
| `GET` | `/v1/organizations/{org_id}/applicants/{id}` | Review detail. |
| `GET`, `POST`, `DELETE` | `/v1/organizations/{org_id}/applicants/{id}/lock` | Inspect, acquire, or release the caller-derived lock. |
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/request-information` | Request applicant information. |
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/approve` | Approve with current lock. |
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/reject` | Reject with current lock. |
| `GET` | `/v1/organizations/{org_id}/applicants/{id}/checks` | List template-derived checks. |
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/checks/{check_id}/start` | Start a check with current lock. |
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/checks/{check_id}/complete` | Complete a check with current lock. |
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/issue` | Operator issuance. |
| `POST` | `/v1/organizations/{org_id}/applicants/{id}/withdraw` | Administrative withdrawal. |

## Security Requirements

1. Reviewer and lock-holder identity MUST come from authenticated request state, never bodies or query parameters.
2. Gateways MUST strip caller-supplied identity headers before injecting authenticated identity and permissions.
3. Resource ownership and permissions MUST be checked again in the applicant service.
4. Cross-organization access by resource ID MUST return HTTP 403.
5. Authorization denials, lock events, decisions, and issuance actions MUST emit privacy-safe audit events.
6. The removed `/v1/applicants/*` resource family has no alias and MUST return HTTP 404.

See [schemas/applicant.json](../../schemas/applicant.json).
