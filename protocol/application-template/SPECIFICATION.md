# Application Template — Entity Specification

**Entity:** Application Template
**Version:** 0.1.0
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
| `form_fields` | FormField[] | No | User-facing input fields |
| `evidence_requirements` | EvidenceRequirement[] | No | Required documents/biometrics |
| `claim_collection_rules` | ClaimCollectionRule[] | No | Claim sourcing rules |
| `approval_strategy` | ApprovalStrategy | Yes | `AUTO`, `MANUAL`, `RULES_BASED` |
| `approval_rules` | object | Conditional | Required for `RULES_BASED` |
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
| `field_type` | FieldType | Yes | `TEXT`, `DATE`, `SELECT`, `FILE_UPLOAD`, `BOOLEAN` |
| `required` | boolean | Yes | |
| `claim_mapping` | string | No | Maps to claim `name` in Credential Template |
| `validation_pattern` | string | No | Regex pattern for TEXT fields |
| `options` | string[] | Conditional | Required for `SELECT` type |
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

### EvidenceType Values

| Value | Description |
|-------|-------------|
| `DOCUMENT_SCAN` | Physical document upload (passport, license) |
| `BIOMETRIC` | Face scan or fingerprint |
| `SELFIE` | Selfie-with-document capture |
| `THIRD_PARTY_VERIFICATION` | External identity verification (e.g., Persona, Jumio) |

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

1. `approval_strategy: RULES_BASED` MUST have non-empty `approval_rules`.
2. All `form_field.claim_mapping` values MUST reference valid claim `name` values in the associated Credential Template.
3. `SELECT` field_type MUST have non-empty `options`.
4. A `DEPRECATED` Application Template MUST NOT be the target of new applications.
5. A `DRAFT` Application Template MUST NOT be referenced by an `ACTIVE` Credential Template.

## Application Lifecycle

```
DRAFT → ACTIVE → DEPRECATED

Application Instance States:
SUBMITTED → UNDER_REVIEW (manual) → APPROVED → (triggers issuance)
                              └→ REJECTED → (notified)
SUBMITTED → APPROVED (auto/rules)  → (triggers issuance)
```

## Approval Rules Schema (RULES_BASED)

When `approval_strategy: RULES_BASED`, `approval_rules` contains a JSON-serialized rules engine configuration. The minimum schema:

```json
{
  "rules": [
    {
      "condition": {"field": "age", "operator": "gte", "value": 18},
      "action": "APPROVE"
    },
    {
      "condition": {"field": "country_code", "operator": "in", "value": ["US", "CA"]},
      "action": "APPROVE"
    }
  ],
  "default_action": "MANUAL"
}
```

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
