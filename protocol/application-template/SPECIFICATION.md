# Application Template — Entity Specification

**Entity:** Application Template
**Version:** 0.4.0
**Stability:** Dynamic
**Section in root spec:** §11

---

## Purpose

An Application Template defines **how users apply for credentials**. It covers the user-facing form, evidence collection, approval workflow, and notification settings. Application Templates are deliberately separated from Credential Templates: the user experience of applying is independent of the cryptographic configuration of the credential.

## What It Contains

| Dimension | Description |
|-----------|-------------|
| Form Fields | User-facing input fields |
| Evidence | Documents, biometrics, or third-party verifications required |
| Claims Mapping | How form fields map to credential claim names |
| Approval Workflow | Auto, manual, or rules-based approval |
| Notifications | Email/SMS templates for status updates |
| UI Config | Theme, layout, welcome text |

## Properties

### Core Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `id` | UUID | Yes | Unique |
| `organization_id` | UUID | Yes | Must reference existing organization |
| `name` | string | Yes | 1–128 characters |
| `description` | string | No | Max 1024 characters |
| `credential_template_id` | UUID | Activation | Must reference an ACTIVE Credential Template in the same organization |
| `form_fields` | FormField[] | No | User-facing input fields |
| `evidence_requirements` | EvidenceRequirement[] | No | Required documents/biometrics |
| `required_checks` | RequiredCheck[] | No | Server-derived checks created for applications |
| `claim_collection_rules` | ClaimCollectionRule[] | No | Claim sourcing rules |
| `approval_strategy` | ApprovalStrategy | Yes | `AUTO`, `MANUAL`, `RULES_BASED` |
| `approval_policy_set_id` | UUID | Conditional | Required for `RULES_BASED`; references an ACTIVE APPROVAL_RULES PolicySet |
| `application_validity_days` | integer | Yes | 1-3650 days |
| `notification_config` | NotificationConfig | No | Status update templates |
| `ui_config` | UIConfig | No | Theme and layout configuration |
| `status` | TemplateStatus | Yes | `DRAFT`, `ACTIVE`, `DEPRECATED` |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

### FormField Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `field_id` | string | Yes | Unique within template |
| `label` | string | Yes | Display text |
| `field_type` | FieldType | Yes | `TEXT`, `DATE`, `DATETIME`, `SELECT`, `FILE_UPLOAD`, `INTEGER`, `NUMBER`, `BOOLEAN`, `EMAIL`, `URL` |
| `required` | boolean | Yes | |
| `claim_mapping` | string | No | Maps to claim `name` in Credential Template |
| `validation_pattern` | string | No | Regex pattern for TEXT fields |
| `options` | string[] | Conditional | Required for `SELECT` type |
| `minimum` | number | No | Inclusive numeric lower bound |
| `maximum` | number | No | Inclusive numeric upper bound |
| `placeholder` | string | No | UI placeholder text |
| `hint` | string | No | Helper text displayed to user |

### EvidenceRequirement Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `evidence_id` | string | Yes | Unique within template |
| `evidence_type` | EvidenceType | Yes | See enum |
| `description` | string | Yes | User-facing instructions |
| `required` | boolean | Yes | |
| `accepted_formats` | string[] | No | For `DOCUMENT_SCAN`: `jpg`, `png`, `pdf` |
| `max_file_size_bytes` | integer | No | For `DOCUMENT_SCAN` |
| `provider` | string | No | Provider namespace for normalized external facts |
| `fact_type` | string | No | Required normalized fact type, such as `passport.document_verified` |
| `scope` | object | No | Required fact scope keys and values |
| `pass_rule` | object | No | Provider-neutral fact assertions that must pass before Cedar evaluation |
| `api` | object | No | Declarative HTTP request for `EXTERNAL_API` requirements |
| `expected_response` | object | No | HTTP status and JSON/path conditions expected from the provider response |
| `response_mapping` | object | No | Mapping from provider response fields into a MIP `EvidenceFact` |
| `auto_issue_on_permit` | boolean | No | Allows automatic approval/issuance after Cedar permits |

### ClaimCollectionRule Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `claim_name` | string | Yes | Credential Template claim populated by this rule |
| `source` | string | Yes | `FORM_FIELD`, `EVIDENCE_EXTRACTION`, `EXTERNAL_API`, or `SYSTEM` |
| `source_config` | object | No | Source-specific configuration |

`FORM_FIELD` uses `source_config.field_id`. `SYSTEM` uses one of the canonical
`source_config.system_field` values: `applicant.user_id`, `applicant.email`,
`applicant.given_name`, `applicant.family_name`, `application.id`,
`application.reference_number`, `application.organization_id`, `current.date`,
`current.datetime`, `validity.expiry_date`, `template.name`,
`template.description`, or `constant`. A constant also requires
`source_config.value`. Clients cannot submit values for `SYSTEM` claims.

`provider` and `fact_type` are required when `evidence_type` is
`EXTERNAL_FACT` or `EXTERNAL_API`. `api`, `expected_response`, and
`response_mapping` are required when `evidence_type` is `EXTERNAL_API`.

`EXTERNAL_API` evidence is intended for request/response provider checks an
organization can configure without writing a provider adapter. Examples include
passport checks, professional license checks, sanctions checks, employment
verification, or other authoritative lookups. Signed protocols, event streams,
LTI/AGS/NRPS integrations, and provider-specific replay semantics should still
use adapters that emit `EvidenceFact` records.

#### EXTERNAL_API Contract

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `api.method` | string | No | `GET`, `POST`, `PUT`, or `PATCH` |
| `api.url` | URI | Yes | Implementations MUST restrict unsafe schemes and private-network targets unless deployment policy allows them |
| `api.timeout_seconds` | number | No | MUST be bounded by implementation limits |
| `api.headers` | object | No | Non-secret static or templated headers |
| `api.secret_headers` | object | No | Header name to deployment secret reference map; secret values MUST NOT be persisted in facts |
| `api.params` | object | No | Query parameters with template interpolation |
| `api.body` / `api.json` | object/string | No | Request body with template interpolation |
| `expected_response.status_codes` | integer[] | No | Defaults to implementation-defined success range when omitted |
| `expected_response.json` | object | No | Provider response path predicates using `all`, `any`, `not`, `path`, `op`, and `value` |
| `response_mapping.scope` | object | No | Constants or response paths mapped to `EvidenceFact.scope` |
| `response_mapping.assertion` | object | No | Constants or response paths mapped to `EvidenceFact.assertion` |
| `response_mapping.verification_status_path` | string | No | Provider response path used to derive `EvidenceFact.verification.status` |
| `response_mapping.provider_event_id_path` | string | No | Provider response path used for source idempotency/audit metadata |

`pass_rule` is evaluated over the normalized `EvidenceFact`, not the raw
provider response. Path rules may refer to `assertion.*`, `scope.*`,
`verification.*`, or `source.*` fields. Approval policies receive only the fact
summary in `ApprovalContext`; they MUST NOT depend on raw API responses.

Implementations MAY expose operator/reviewer run controls for configured
`EXTERNAL_API` requirements. Those surfaces SHOULD identify checks by
`evidence_id`/`check_id` and MAY show provider, fact type, scope, method, and
auto-issue eligibility. They MUST NOT expose resolved secret values,
`api.secret_headers`, or raw provider responses. Running a check MUST produce a
normalized `EvidenceFact` and evaluate the same approval policy path as
adapter-generated facts.

### EvidenceType Values

| Value | Description |
|-------|-------------|
| `DOCUMENT_SCAN` | Physical document upload (passport, license) |
| `BIOMETRIC` | Face scan or fingerprint |
| `SELFIE` | Selfie-with-document capture |
| `THIRD_PARTY_VERIFICATION` | External identity verification (e.g., Persona, Jumio) |
| `EXTERNAL_FACT` | Requirement satisfied by a normalized `EvidenceFact` from an adapter or event source |
| `EXTERNAL_API` | Requirement satisfied by running a declarative provider API check that emits an `EvidenceFact` |

### ClaimCollectionRule Fields

| Property | Type | Description |
|----------|------|-------------|
| `claim_name` | string | Target claim in Credential Template |
| `source` | ClaimSource | `FORM_FIELD`, `EVIDENCE_EXTRACTION`, `EXTERNAL_API`, `SYSTEM` |
| `source_config` | object | Source-specific configuration |

### ApprovalStrategy Values

| Value | Description |
|-------|-------------|
| `AUTO` | Approved immediately on submission (no review) |
| `MANUAL` | Requires manual reviewer action |
| `RULES_BASED` | Automated rules engine evaluates application |

## Constraints

1. `approval_strategy: RULES_BASED` MUST have a non-null `approval_policy_set_id` referencing an ACTIVE `APPROVAL_RULES` PolicySet.
2. All `form_field.claim_mapping` values MUST reference valid claim `name` values in the associated Credential Template.
3. `SELECT` field_type MUST have non-empty `options`.
4. `EXTERNAL_API` requirements MUST NOT store secret values directly. Store only deployment secret references in `api.secret_headers`.
5. `EXTERNAL_API` implementations MUST persist only normalized `EvidenceFact` and audit metadata, not raw provider secrets.
6. A `DEPRECATED` Application Template MUST NOT be the target of new applications.
7. An `ACTIVE` Application Template MUST reference an `ACTIVE` Credential Template in the same organization.
8. Creation MUST produce `DRAFT`. Status is server-derived and MUST NOT be accepted in create or patch payloads.
9. Only `DRAFT` templates may be patched or deleted. Active templates transition to `DEPRECATED` and remain available for historical applications.
10. Field validation MUST run on create, submit, and issuance. Date values use `YYYY-MM-DD`; datetime values use RFC 3339.

## Application Lifecycle

```
DRAFT → ACTIVE → DEPRECATED

Application Instance States:
SUBMITTED → UNDER_REVIEW (manual) → APPROVED → (triggers issuance)
                              └→ REJECTED → (notified)
SUBMITTED → APPROVED (auto/rules)  → (triggers issuance)
```

## HTTP API

```text
GET    /v1/application-templates?organization_id={organization_id}
POST   /v1/application-templates
GET    /v1/application-templates/{id}
PATCH  /v1/application-templates/{id}
DELETE /v1/application-templates/{id}
POST   /v1/application-templates/{id}/validate
POST   /v1/application-templates/{id}/activate
POST   /v1/application-templates/{id}/deprecate
```

List responses are direct JSON arrays. `DELETE` returns 204 for a draft and 409 for any other lifecycle state. Validation returns `{valid, errors}` where each error contains `section`, `field`, `code`, and a safe `message`.

`RULES_BASED` approval is governed only by the referenced Cedar PolicySet. Opaque approval-rule objects are not part of MIP 0.3.

## Examples

### Employee Badge Application

```json
{
  "id": "at-employee-badge",
  "organization_id": "org-enterprise",
  "name": "Employee Badge Application",
  "approval_strategy": "MANUAL",
  "form_fields": [
    {
      "field_id": "employee_id",
      "label": "Employee ID",
      "field_type": "TEXT",
      "required": true,
      "claim_mapping": "employee_id",
      "validation_pattern": "^EMP-[0-9]{6}$"
    },
    {
      "field_id": "department",
      "label": "Department",
      "field_type": "SELECT",
      "required": true,
      "claim_mapping": "department",
      "options": ["Engineering", "Operations", "Finance", "Sales"]
    }
  ],
  "status": "ACTIVE",
  "created_at": "2026-03-11T00:00:00Z"
}
```

## See Also

- Root specification: [§11 Application Template](../../SPECIFICATION.md#11-application-template)
- Schema: [../../schemas/application-template.json](../../schemas/application-template.json)
- Design: [DESIGN.md](./DESIGN.md)
