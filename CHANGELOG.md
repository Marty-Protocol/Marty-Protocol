# CHANGELOG

All notable changes to the Marty Identity Protocol will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](VERSIONING.md).

---

## [Unreleased]

## [0.4.0] - 2026-08-07

### Changed
- Added the organization-scoped Marty Trust Registry Sync v1 import contract.
  URL trust sources now declare their wire adapter explicitly; registry URLs
  require HTTPS without credentials, query strings, fragments, or non-default
  ports, and sync results expose only public source counts and sequence state.
  Native ICAO PKD, EU LoTL, and AAMVA formats remain separately scoped and are
  not implied by configuring a raw distribution URL.
- Hardened delta feeds with bounded cursors, entries, certificates, and key
  identifiers; required source attribution; and operation-aware certificate
  rules. Importing implementations must reject rollback and malformed deltas
  and apply complete feeds atomically.
- Made issuer accreditation evidence first-class. `IssuerEntity` responses now
  carry an explicit `accreditations` set; create defaults it to empty and update
  replaces the complete set. `accreditation_body` remains the certifying
  authority and cannot satisfy an accreditation requirement by itself.
- Made Flow definition creation, partial update, execution start, execution
  projection, verification result, issuance initiation, issuance transaction,
  issued-credential lifecycle, and renewal-offer operations explicit public
  contracts. Every management operation is tenant-bound; Flow context and
  responses recursively prohibit custody selectors and reusable secrets, and
  public issuance responses expose wallet offer URIs without separate
  pre-authorized codes.
- Distinguished issuer trust records from signing identities. Added strict,
  organization-scoped IssuerEntity create and partial-update contracts plus a
  DID-only IssuerIdentity projection. Public callers cannot create or mutate
  global/system issuers, forge revocation attribution, or pass custody/KMS
  selectors through metadata; ambiguous active DID mappings fail closed.
- Aligned the Organization resource with the production tenant, discovery,
  admission, contact, and caller-membership semantics. Added strict create and
  tenant-bound partial-update schemas, made `PATCH` canonical, and removed the
  unimplemented delete operation from the public contract. Internal settings,
  plan/billing data, and custody selectors remain prohibited.
- Classified Presentation Policy status, version, holder-facing display
  metadata, compliance linkage, authoritative Credential Template
  requirements, and alternative requirements as public protocol semantics.
  A policy must contain at least one canonical claim, template-bound
  requirement, or alternative requirement; private custody routing remains
  prohibited. Added separate tenant-scoped create and partial-update request
  schemas so operation input cannot be confused with the persisted resource.
- Defined canonical public issuance and verification-flow operation schemas.
  Public callers select signing identities only with `organization_id` and
  `issuer_did` (or a DID-bearing Credential Template); issuer-profile IDs,
  signing-service IDs, key references, KMS/provider selectors, and internal
  flow-definition routing are rejected.
- Made public Credential Templates DID-only. Every template now requires
  `issuer_did`; issuer-profile IDs, verification-method selectors, algorithms,
  certificate bindings, KMS providers, signing-service IDs, key references,
  remote-signing configuration, and artifact-generation controls are rejected.
  Implementations resolve and sign through an organization-scoped internal
  issuer profile without exposing custody metadata.
- Replaced Presentation Policy `NONCE` binding with explicit credential, device, or session control methods plus proof-profile and proof-freshness requirements.
- Aligned OID4VCI issuance with the 1.0 Final Nonce Endpoint and plural `proofs` parameter; Token Responses no longer carry draft-era credential nonce fields.
- Renamed Deployment Profile `biometric_required` to `operator_biometric_authentication_required` with a bounded read-compatibility alias.
- Retained `OB2_COMPATIBILITY` as the sole short-lived compatibility exception
  while existing deployments migrate to Open Badges 3. It is reviewed on
  2026-09-01 and targets removal on 2026-10-01 before 1.0; no new OB2-only
  capabilities may be added.
- Application Template evidence requirements now use only `auto_issue_on_permit`.
- Application Template claim rules now use only `claim_name`, `source`, and `source_config`.
- Removed Deployment Profile request/response aliases `default_presentation_policy_id` and `ux_config`.
- Removed the opaque Compliance Profile `default_verification_rules` field.
- Replaced compatibility/deprecation guidance with exact-version, atomic-release requirements.

### Fixed
- Aligned Flow and issued-credential documentation, conformance fixtures, and
  generated bindings with production response fields, uppercase lifecycle
  states, public `issuer_did`, and private delivery-routing state.
- Model ISO mdoc `doctype` explicitly in the public Credential Template
  contract while keeping every signing-custody selector private.
- Brought bundled system Compliance Profiles under schema validation, including `holder_binding_required` and their ecosystem requirement fields.
- Added structured holder-binding evidence to Verification Session results.
- Generated Python, Rust, and TypeScript bindings now model `claim_blocker` as the typed nullable `ClaimBlocker` object instead of degrading it to `Any` or `string`.
- Corrected the `TOKEN_STATUS_LIST` standard reference from unrelated RFC 9738 to the active `draft-ietf-oauth-status-list` specification.

## [0.3.1] - 2026-07-12

### Changed
- Declared `0.3.1` as the only supported MIP message and discovery version.
- Added the browser lifecycle gate as conformance evidence for canonical OID4VCI receipt and DCQL OID4VP presentation.
- Removed Draft 13 singular credential proof compatibility from the reference wallet and issuance contract.

### Fixed
- Corrected stale normative message-version examples that still required `0.1`.
- Corrected the MIP discovery conformance fixture to advertise the current supported version.
- Corrected holder proof audience/nonce validation and DCQL response serialization in the reference wallet engine.

## [0.3.0] - 2026-07-11

### Changed
- Replaced applicant-ID and legacy `/v1/applicants/*` APIs with canonical organization-scoped reviewer and `/v1/me/*` self-service contracts.
- Application creation now accepts only `organization_id`, `application_template_id`, `form_data`, and `integration_context`; policy and identity fields are server-derived.
- Added independent `claim_state` and privacy-safe `claim_blocker` semantics.
- Added authenticated holder inventory at `/v1/issued-credentials/mine`.
- Added `FIELD_VALIDATION_FAILED` and `NO_ACTIVE_ISSUANCE_FLOW` errors.

### Deprecated
- `OB2_COMPATIBILITY` is now on a formal sunset path:
  - no new integrations should adopt it after `v0.2.0`
  - migrate to `OB3_JWT` or `OB3_JSONLD`
  - planned removal in `v1.0.0`

### Fixed
- Added `combined` flow type to `enums/flow-types.json` to match Flow entity spec (S1)
- Aligned webhook signature header to `X-MIP-Signature` across notification-target and subscription specs (S2)
- Fixed `IssuedCredential.credential_format` to reference protocol enum values (`MDOC`, `SD_JWT_VC`, `VC_JWT`, `JSON_LD`) instead of OID4VCI wire identifiers (S3)
- Reconciled FlowExecution lifecycle states with `enums/flow-statuses.json` (S4)
- Updated implementation guide to use current field names (`source_type`, `issuer_did`, `revocation_policy.check_mode`) (S5)
- Aligned Flow entity spec version to 0.1.0 (S6)
- Renamed `RevocationTimingMode.SKIP` to `DISABLED` to avoid ambiguity with `RevocationCheckMode.SKIP` (S7)
- Fixed `validate_phase1.py` to check for `DISABLED` instead of stale `SKIP` value

### Added
- **Cedar policy integration** for formally verifiable authorization
  - Cedar schema (`cedar/mip.cedarschema`) defining MIP entity types, actions, and context types
  - `PolicySet` entity schema (`schemas/policy-set.json`) for storing Cedar policies
  - Three policy domains: API access control, credential verification trust, approval rules
  - Reference policies: `cedar/policies/api_access.cedar`, `credential_verification.cedar`, `approval_rules.cedar`
  - Cedar policy examples for age verification, employee access, and pre-boarding clearance
  - Cedar integration documentation (`docs/cedar-policies.md`)
- Cedar policy references in all protocol documentation: SPECIFICATION.md (§16 Policy Set), README.md, implementation guide, glossary, design principles, migration guide, contributing guide
- `EXTERNAL` approval strategy added to `ApplicationTemplate.approval_strategy` enum
- `approval_policy_set_id` on `ApplicationTemplate` — Cedar PolicySet for RULES_BASED approval
- `verification_policy_set_id` on `TrustProfile` and `ComplianceProfile` — Cedar PolicySet for verification rules
- `policy_set_id` on `ScimRole` — Cedar PolicySet for fine-grained ABAC
- `ZK_MDOC` credential format for zero-knowledge mDoc (experimental)
- `OB2_COMPATIBILITY` compliance code for Open Badge v2.0 legacy support
- Wire-format mapping (`$defs.wire_format_mapping` + `$defs.wire_format_aliases`) in `credential-formats.json`
- Format mapping documentation (`docs/format-mapping.md`)
- Code generation pipeline (`scripts/codegen.py`) producing typed bindings from JSON schemas
  - Python: Pydantic v2 models + StrEnum classes (`reference/python/`)
  - Rust: serde structs + enums (`reference/rust/`)
  - TypeScript: interfaces + enums (`reference/typescript/`)
- Orchestrator script (`scripts/generate.sh`) for one-command regeneration
- Extended entity specifications: Organization, Applicant, FlowExecution, IssuedCredential, IssuerRegistry, Messages, SCIM, Subscription, TrustFramework, TrustRegistry
- JSON Schemas for all core primitives and supporting abstractions (33 schemas)
- Controlled vocabulary enumerations (20 enum files)
- Minimal and realistic example corpus (15 fixtures across 5 scenarios)
- Conformance test suite (7 valid fixtures, 5 invalid test cases)
- Compliance profiles: ICAO DTC, ICAO MRZ, AAMVA mDL, EUDI PID, EUDI mDL, Enterprise VC, DIF PEX, OB3 JWT, OB3 JSON-LD, OID4VC

### Not Yet Implemented
- CI/CD automation for codegen validation on schema changes
- Advanced examples (ZK predicates, offline scenarios, multi-lane) — `examples/advanced/` is a placeholder
- Architecture Decision Records — `docs/decisions/` is a placeholder

---

## [0.1.0] - 2026-03-11

### Added
- Initial repository structure
- Core primitive specifications: Trust Profile, Credential Template, Presentation Policy, Deployment Profile, Flow
- Supporting abstractions: Compliance Profile, Application Template, Revocation Profile, Wallet Profile, Device Registration, Notification Target
- Foundational documentation: README, SPECIFICATION outline, VERSIONING, CONTRIBUTING
