# Contributing to the Marty Identity Protocol

Thank you for your interest in contributing to MIP. This document describes the contribution process and guidelines.

---

## Types of Contributions

### 1. Specification Clarification

For ambiguities or errors in normative text:

- Open an issue with label `spec-clarification`
- Include: the section reference, the ambiguous text, and your proposed clarification
- Clarifications that do not change validation behavior → PATCH
- Clarifications that change behavior → MINOR or MAJOR

### 2. Schema Change

For adding, modifying, or removing fields:

- Open an issue with label `schema-change`
- Describe: the entity, the field, the motivation, and the impact
- Breaking changes require discussion before a PR is opened
- Include updates to conformance fixtures that reflect the change

### 3. New Compliance Profile

For adding support for a new standard or jurisdiction:

- Open an issue with label `compliance-profile`
- Provide: standard reference, compliance code, format mapping, and example credentials
- Include a PROFILE.md, mapping.json, constraints.json, and at least one example

### 4. Enum Proposal

For adding values to controlled vocabularies:

- Open an issue with label `enum-proposal`
- Provide: the enum file, the new value, definition, example_usage, and group
- Enum additions are backward-compatible (MINOR)

### 5. Conformance Test

For adding valid or invalid fixtures:

- Open a PR with label `conformance`
- Valid fixtures: must pass all schema validators
- Invalid fixtures: must include a `.expected.json` sidecar with `error_type`, `field_path`, and `spec_reference`

### 6. Cedar Policy Contribution

For adding or modifying Cedar policies:

- Open an issue with label `cedar-policy`
- Provide: the policy domain (`ACCESS_CONTROL`, `CREDENTIAL_VERIFICATION`, `APPROVAL_RULES`), the Cedar policy text, and a description of the authorization rule
- All Cedar policies MUST validate against the MIP Cedar schema (`cedar/mip.cedarschema`)
- Include a PolicySet JSON fixture in `examples/` demonstrating the policy in context
- Reference policies in `cedar/policies/` are normative examples — changes require review

### 7. Reference Implementation

For adding or updating reference implementations:

- Implementations must cover all 11 MIP entities
- Must include a validation function that accepts a document and returns pass/fail
- Must include tests demonstrating conformance suite passage

---

## Pull Request Process

1. Fork the repository and create a branch: `feat/`, `fix/`, `spec/`, `schema/`, `conformance/`
2. Make your changes with clear commit messages
3. Run conformance tests: `scripts/run-conformance.sh`
4. Validate all schemas: `scripts/validate-schemas.sh`
5. Update CHANGELOG.md under `[Unreleased]`
6. Open a PR against `main` with a description of the change and its version impact

---

## Architecture Decision Records

For changes that establish or reverse a significant design precedent:

- Create an ADR in `docs/decisions/`
- Follow the template in `docs/adr-template.md`
- ADRs are non-normative but must be referenced from the relevant spec section

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating you agree to abide by its terms.

---

## Developer Certificate of Origin (DCO)

All commits must be signed off to certify you have the right to submit the contribution under the Apache 2.0 license. Add a sign-off to every commit:

```
git commit -s -m "your commit message"
```

This adds a `Signed-off-by: Your Name <email@example.com>` trailer. See <https://developercertificate.org/> for the full DCO text. PRs with unsigned commits will not be merged.

---

## Version Impact Reference

| Contribution Type | Typical Version Impact |
|-------------------|----------------------|
| Spec clarification (no behavior change) | PATCH |
| Schema field removal | MAJOR |
| New required field | MAJOR |
| New optional field | MINOR |
| New compliance profile | MINOR |
| New enum value | MINOR |
| Conformance test (valid) | MINOR |
| Conformance test (invalid) | PATCH or MINOR |
| Cedar policy (reference) | MINOR |
| Cedar schema change | MINOR or MAJOR |
| Reference implementation | MINOR |
| Documentation fix | PATCH |
