# CHANGELOG

All notable changes to the Marty Identity Protocol will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](VERSIONING.md).

---

## [Unreleased]

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
