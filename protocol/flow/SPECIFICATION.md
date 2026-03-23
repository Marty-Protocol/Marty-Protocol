# Flow — Entity Specification

**Entity:** Flow
**Version:** 0.1.0
**Stability:** Per use-case
**Section in root spec:** §9

---

## Purpose

A Flow orchestrates the **end-to-end identity lifecycle**. It is the automation layer that makes identity operations — application, approval, issuance, presentation, verification — repeatable, auditable, and stateful. Flows are the top-level composable unit of the Marty identity protocol.

Each `flow_type` maps to a **fixed, ordered step sequence** defined by the underlying protocol (OID4VCI, OID4VP, ISO 18013-5, or application-approval workflow). Steps are not arbitrarily configurable — they are protocol-fixed. Extensible steps allow custom hook injection (pre/post).

See also: `FlowExecution` (runtime state), `enums/flow-types.json` (step sequences).

## What It Contains

| Dimension | Description |
|-----------|-------------|
| Flow Type | Protocol-aligned type determining the step sequence |
| Trust | Optional root Trust Profile for the entire flow |
| Template | Credential Template (direct issuance flows) |
| Application Template | Application Template (application_approval_issuance only; mutually exclusive with credential_template_id) |
| Policy | Presentation Policy (verification flows) |
| Deployments | Which Deployment Profiles have this flow enabled |
| Approval | Strategy for the approval_decision step |
| Hooks | Pre/post hooks on extensible steps |
| Trigger | What initiates the flow |

## Properties

### Core Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `id` | UUID | Yes | Unique |
| `organization_id` | UUID | Yes | Must reference existing organization |
| `name` | string | Yes | 1–128 characters |
| `description` | string | No | Max 1024 characters |
| `flow_type` | FlowType | Yes | See `enums/flow-types.json`; protocol-named values only |
| `trust_profile_id` | UUID | No | Optional root Trust Profile |
| `credential_template_id` | UUID | Conditional | Required for `oid4vci_pre_authorized`, `oid4vci_authorization_code`, `mdl_issuance`. Mutually exclusive with `application_template_id`. |
| `application_template_id` | UUID | Conditional | Required for `application_approval_issuance`. Mutually exclusive with `credential_template_id`. |
| `presentation_policy_id` | UUID | Conditional | Required for `oid4vp_presentation`, `mdl_presentation`, `siopv2` |
| `deployment_profile_ids` | UUID[] | No | Deployment Profiles that have this flow in their `enabled_flow_ids` |
| `approval_strategy` | ApprovalStrategy | Yes | `AUTO`, `MANUAL`, `RULES_BASED`, `EXTERNAL` |
| `enabled` | boolean | Yes | Whether the flow is active; default `true` |
| `hooks` | object | No | Pre/post hooks keyed by `pre_{step_name}` / `post_{step_name}` |
| `trigger` | FlowTrigger | No | Initiation trigger configuration |
| `status` | FlowStatus | Yes | `DRAFT`, `ACTIVE`, `PAUSED`, `ARCHIVED` |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

### FlowTrigger Fields

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `trigger_type` | TriggerType | Yes | `API_CALL`, `WEBHOOK`, `SCHEDULE`, `APPLICATION_SUBMITTED` |
| `config` | object | No | Type-specific configuration |

**SCHEDULE config:**
```json
{"cron": "0 0 * * *", "timezone": "UTC"}
```

**WEBHOOK config:**
```json
{"event_type": "enrollment.completed", "source": "external-hr-system"}
```

### FlowStep Fields

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `step_id` | string | Yes | Unique within this flow |
| `action` | StepAction | Yes | See action types below |
| `on_success` | string | No | `step_id` of next step on success |
| `on_failure` | string | No | `step_id` of next step on failure |
| `config` | object | No | Step-specific configuration |

### Step Actions

| Action | Description | Required Config |
|--------|-------------|-----------------|
| `APPLICATION` | Collect user application | `application_template_id` |
| `APPROVAL` | Manual or rules-based approval | `approval_strategy` |
| `ISSUANCE` | Issue credential | Uses flow's `credential_template_id` |
| `PRESENTATION_REQUEST` | Request credential presentation | `policy_id` |
| `VERIFICATION` | Verify presented credential | Uses flow's `presentation_policy_id` |
| `NOTIFICATION` | Send notification to holder/verifier | `notification_config` |

## Constraints

1. `flow_type: ISSUANCE` MUST have `credential_template_id`.
2. `flow_type: VERIFICATION` MUST have `presentation_policy_id`.
3. `flow_type: combined` MUST have both `credential_template_id` and `presentation_policy_id`.
4. An `ACTIVE` flow MUST NOT reference a `DRAFT` or `DEPRECATED` Credential Template.
5. An `ACTIVE` flow MUST NOT reference a `DRAFT` Presentation Policy.
6. All `deployment_profile_ids`, if present, MUST reference existing Deployment Profiles.
7. Flow step graph MUST be a DAG (no cycles).
8. All `on_success` and `on_failure` step references MUST resolve to valid `step_id` values within the same flow.

## Standard Sequences

### Issuance with Application

```
APPLICATION → APPROVAL → ISSUANCE → NOTIFICATION
     │                      │
   (rejected)             (failed)
     ↓                      ↓
NOTIFICATION           NOTIFICATION
```

### Direct Issuance (API-triggered)

```
ISSUANCE → NOTIFICATION
```

### Verification

```
PRESENTATION_REQUEST → VERIFICATION → NOTIFICATION
                             │
                          (failed)
                             ↓
                        NOTIFICATION
```

### Combined (Credential Delivery + Verification)

```
APPLICATION → APPROVAL → ISSUANCE → PRESENTATION_REQUEST → VERIFICATION → NOTIFICATION
```

### SIOPv2 (Self-Issued OP Authentication)

```
PRESENTATION_REQUEST → VERIFICATION → NOTIFICATION
         │                   │
    (create_request)    (verify_id_token)
         ↓                   ↓
  authentication_submission  result
```

SIOPv2 flows use the Self-Issued OpenID Provider v2 protocol for holder authentication. The verifier creates a signed authorization request; the wallet submits a self-issued ID token. See root spec §9.8 for the full API specification.

## Flow Instances

A Flow is a **template**. A Flow Instance is a running execution. Instances track state:

| State | Description |
|-------|-------------|
| `PENDING` | Created but not started |
| `IN_PROGRESS` | Currently executing |
| `COMPLETED` | Successfully finished |
| `FAILED` | Terminated due to error |
| `CANCELLED` | Manually terminated |

## Examples

### Pre-Boarding Clearance Flow

```json
{
  "id": "flow-pbc",
  "organization_id": "org-airline",
  "name": "Pre-Boarding Clearance",
  "flow_type": "combined",
  "trust_profile_id": "tp-icao-dtc",
  "credential_template_id": "ct-airline-pass",
  "presentation_policy_id": "pp-pre-boarding",
  "deployment_profile_ids": ["dp-gate-12", "dp-gate-13"],
  "trigger": {
    "trigger_type": "API_CALL"
  },
  "status": "ACTIVE",
  "created_at": "2026-03-11T00:00:00Z"
}
```

## See Also

- Root specification: [§9 Flow](../../SPECIFICATION.md#9-flow)
- Schema: [../../schemas/flow.json](../../schemas/flow.json)
- Design decisions: [DESIGN.md](./DESIGN.md)
