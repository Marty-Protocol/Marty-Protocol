# Flow Execution — Entity Specification

**Entity:** FlowExecution
**Version:** 0.4.0
**Stability:** Stable
**Section in root spec:** §9.2

---

## Purpose

A `FlowExecution` is the **runtime instance of a Flow**. When a flow is initiated (via API call, webhook, schedule, or application submission), a `FlowExecution` is created to track progress through the fixed step sequence defined by the flow's `flow_type`.

One `Flow` definition → many `FlowExecution` instances over time.

## Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Unique execution identifier |
| `flow_id` | string\|null | Yes | References `Flow.id`; null only for a supported system-defined verification flow |
| `flow_type` | FlowType\|null | Yes | Flow type copied at instantiation time |
| `organization_id` | string | Yes | Tenant that owns the execution |
| `status` | FlowStatus | Yes | See lifecycle below; from `enums/flow-statuses.json` |
| `current_step` | string\|null | No | Name of the currently executing step |
| `current_step_index` | integer | No | 0-based index into the flow's step sequence |
| `step_results` | object | Yes | Public result values keyed by step name |
| `context_data` | object | Yes | Public, non-secret context shared across steps |
| `issued_credential_id` | string\|null | No | References `IssuedCredential.id`; populated after successful issuance |
| `started_at` | datetime\|null | No | When `status` first transitioned to `IN_PROGRESS` |
| `completed_at` | datetime\|null | No | When `status` reached a terminal state |
| `expires_at` | datetime\|null | No | Execution expiry |
| `error_code` | string\|null | No | Stable public error code; no internal exception text |
| `metadata` | object | Yes | Public execution metadata |
| `state_history` | array | Yes | Public lifecycle transitions |
| `created_at` | datetime | Yes | Creation time |
| `updated_at` | datetime | Yes | Last update time |

## Lifecycle

All state names correspond to values in `enums/flow-statuses.json`.

```
PENDING
   ↓
IN_PROGRESS ──────────────────────────────────────────────► COMPLETED
   ↓                    ↓                                        │
AWAITING_APPROVAL   AWAITING_WALLET                             │
   ↓                    ↓                                        │
   ├── (approved) ──► IN_PROGRESS (resumes)                     │
   ↓                                            ↓               │
FAILED (terminal, includes rejections)   FAILED (terminal) ◄───┘
   │
AWAITING_EVIDENCE ──► IN_PROGRESS (resumes when evidence submitted)
   │
EXPIRED (terminal, if TTL exceeded in any non-terminal state)
   │
CANCELLED (terminal, from any non-terminal state)
```

| Status | Meaning |
|--------|---------|
| `PENDING` | Execution created but not yet started |
| `IN_PROGRESS` | Actively executing steps |
| `AWAITING_APPROVAL` | Paused at an approval_decision step |
| `AWAITING_WALLET` | Waiting for wallet interaction (e.g. OID4VCI token exchange, OID4VP submission) |
| `AWAITING_EVIDENCE` | Waiting for applicant to submit required evidence |
| `COMPLETED` | All steps finished successfully |
| `FAILED` | Terminated due to error or rejection |
| `EXPIRED` | Execution TTL exceeded without completion |
| `CANCELLED` | Manually terminated by operator or system |

Full state transition map: see `enums/flow-statuses.json`.

## Step Sequences per Flow Type

Each `flow_type` has a fixed step sequence. Steps cannot be reordered. Steps marked **extensible** support pre/post hooks.

### `oid4vci_pre_authorized`
1. `create_offer` — generate OID4VCI credential offer
2. `token_exchange` — wallet exchanges pre-auth code for access token
3. `credential_request` — wallet sends credential request
4. `issue_credential` — issue and deliver credential

### `oid4vci_authorization_code`
1. `create_offer`
2. `authorization` — OAuth2 authorization code exchange
3. `token_exchange`
4. `credential_request`
5. `issue_credential`

### `mdl_issuance`
1. `application_submit`
2. `validate_evidence`
3. `approval_decision` *(extensible)*
4. `issue_mdl`
5. `deliver_credential` *(extensible)*

### `oid4vp_presentation`
1. `create_request` — generate presentation request
2. `wallet_selection` — holder selects wallet/credential
3. `presentation_submission` — holder submits VP
4. `verify_presentation` — verifier validates claims

### `mdl_presentation`
1. `device_engagement` — NFC/QR device engagement
2. `session_establishment` — BLE/Wi-Fi session
3. `request_items` — verifier sends mDL data request
4. `response_items` — holder device responds
5. `session_termination`

### `application_approval_issuance`
1. `accept_application`
2. `validate_evidence`
3. `approval_decision` *(extensible)*
4. `issue_credential`
5. `deliver_credential` *(extensible)*

### `physical_document_issuance`
1. `accept_application`
2. `validate_evidence`
3. `approval_decision` *(extensible)*
4. `generate_data_groups`
5. `sign_sod`
6. `submit_to_personalization` *(extensible)*
7. `track_production`
8. `quality_verify` *(extensible)*
9. `activate_credential`

### `custom`

The execution sequence is read from the validated FlowExtension envelope. The execution retains the extension URI and version in its audit context and does not report conformance to the extended standard sequence.

## Hooks

Extensible steps accept pre/post hooks. Hooks are defined in `Flow.hooks` and executed when a `FlowExecution` reaches that step. Hook types: `WEBHOOK`, `EXTERNAL_API`, `SCRIPT`.

```json
{
  "hooks": {
    "pre_approval_decision": [
      {"hook_type": "WEBHOOK", "url": "https://hr.example.com/marty/pre-approval"}
    ],
    "post_deliver_credential": [
      {"hook_type": "WEBHOOK", "url": "https://hr.example.com/marty/credential-issued"}
    ]
  }
}
```

## Relationship to IssuedCredential

On successful completion of an issuance flow, `FlowExecution.issued_credential_id` is populated with the `IssuedCredential.id`. The `IssuedCredential` record holds the SHA-256 credential hash, status list entries, and revocation history.

## Constraints

1. A `FlowExecution` is immutable once it reaches a terminal status (`COMPLETED`, `FAILED`, `EXPIRED`, `CANCELLED`).
2. `current_step` MUST be a valid step name from the flow's step sequence.
3. `issued_credential_id` MUST only be set on executions with `flow_type` in the issuance category.
4. `context_data`, `step_results`, `metadata`, and `state_history` are public projections. They MUST NOT contain custody selectors or reusable secrets, including issuer-profile IDs, signing-service IDs, key references, KMS/provider selectors, private keys, bearer tokens, pre-authorized codes, client secrets, session tokens, or API keys.
5. The start request is tenant-bound and MUST reject private service state at any nesting depth. Internal orchestration may retain that state separately, but it is never accepted from or returned to a public caller.
