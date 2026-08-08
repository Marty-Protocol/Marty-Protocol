# Flow - Design Notes

**Version:** 0.4.0

## Standard And Custom Boundaries

A standard FlowType is an interoperability claim. Its ordered sequence is fixed by `enums/flow-types.json`; implementations may configure references, triggers, approval strategy, and declared hooks, but MUST NOT replace or reorder standard steps.

Non-standard orchestration uses `flow_type: custom` with `FlowExtension`. The extension declares a URI, version, standard type being extended, entry step, graph, and configuration. This keeps proprietary automation available without weakening the meaning of standard FlowType names.

The ElevenID conditional orchestration extension is identified by `urn:elevenid:flow-extension:conditional-orchestration:v1`. Legacy preconditions and editable graphs migrate to that extension rather than remaining on a standard FlowType.

## Lifecycle

Flow creation is draft-first. `POST /v1/flows/definitions` creates `DRAFT`; validation resolves schema, reference, compatibility, and runtime capability blockers; activation is a distinct permission-protected transition. `status` is the only lifecycle source of truth.

## Deployments And Destinations

`deployment_profile_ids` describes runtime/device deployments and remains optional. `delivery_destination_profile_id` describes an operational delivery destination. Physical-document issuance requires a destination in `physical_production` mode backed by a configured personalization connector.

## Runtime

A Flow Definition is reusable and spawns many FlowExecution records. Runtime responses expose the derived fixed sequence for standard types or the extension graph for custom types. FlowExecution is the shared audit and troubleshooting unit.
