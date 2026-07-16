# Flow - Entity Specification

**Entity:** Flow
**Version:** 0.3.1
**Stability:** Per use-case
**Section in root spec:** Section 9

## Purpose

A Flow is the reusable orchestration definition for an identity operation. Standard FlowTypes are protocol-aligned and have fixed ordered sequences. A FlowExecution is one runtime instance.

## Contract

The normative shape is `schemas/flow.json`. FlowType metadata, required references, categories, sequences, and extensible steps are defined once in `enums/flow-types.json`.

Standard flows configure organization, name, a standard FlowType, type-correct object references, approval strategy, trigger, declared hook points, and lifecycle status.

Custom flows configure `flow_type: custom` and a `schemas/flow-extension.json` envelope. A custom flow derives its category and intent from `extension.extends_flow_type`, but does not claim conformance to that standard sequence.

## Lifecycle

```text
DRAFT -> ACTIVE -> PAUSED -> ACTIVE
  |         |
  +---------+---------> ARCHIVED
```

- Creation MUST produce `DRAFT`.
- Activation MUST validate schema, references, compatibility, and runtime capabilities.
- `PAUSED` definitions create no new executions.
- `ARCHIVED` definitions are immutable and create no new executions.

## Physical Document Issuance

`physical_document_issuance` is normative for ICAO 9303 ePassport production. It requires an active ICAO eMRTD Credential Template, an active Application Template, a physical-production Delivery Destination Profile, and available document-signer and personalization capabilities.

Its fixed sequence is `accept_application`, `validate_evidence`, `approval_decision`, `generate_data_groups`, `sign_sod`, `submit_to_personalization`, `track_production`, `quality_verify`, and `activate_credential`.

## Validation

- Standard flows MUST NOT include `extension`.
- Custom flows MUST include a valid extension and a resolvable entry step.
- Custom step IDs MUST be unique, transitions MUST resolve, and the graph MUST be acyclic.
- Standard hooks MUST target only extensible steps declared for the selected FlowType.
- Active flows MUST reference active, organization-compatible objects and available runtime capabilities.
- Physical flows MUST fail activation when signing or personalization capabilities are unavailable.

## API

```text
GET    /v1/flows/capabilities
GET    /v1/flows/definitions
POST   /v1/flows/definitions
GET    /v1/flows/definitions/{id}
PATCH  /v1/flows/definitions/{id}
DELETE /v1/flows/definitions/{id}
POST   /v1/flows/definitions/{id}/validate
POST   /v1/flows/definitions/{id}/activate
POST   /v1/flows/instances
GET    /v1/flows/instances
GET    /v1/flows/instances/{id}
```

## See Also

- Root specification: Section 9
- Flow schema: `schemas/flow.json`
- Extension schema: `schemas/flow-extension.json`
- FlowType manifest: `enums/flow-types.json`
- Execution specification: `protocol/flow-execution/SPECIFICATION.md`
