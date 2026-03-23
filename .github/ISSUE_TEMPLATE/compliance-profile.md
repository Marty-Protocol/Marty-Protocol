---
name: New Compliance Profile
about: Propose adding support for a new standard or jurisdiction
labels: compliance-profile
---

## Standard / Jurisdiction

> e.g., "ISO 23220-3 — Mobile eID", "California AB-1234 — Digital ID Act"

## Compliance Code

> Proposed value for the `compliance_code` field (must not conflict with existing values in `enums/compliance-codes.json`)

## Credential Format

> e.g., `MDOC`, `SD_JWT_VC`, `VC_JWT`

## Standard Reference

> Link to the published standard, RFC, W3C Recommendation, or government rule book

## Checklist

- [ ] `PROFILE.md` with normative description
- [ ] `mapping.json` with field mappings
- [ ] `constraints.json` with validation constraints
- [ ] At least one example credential in `examples/`
- [ ] Conformance fixtures in `conformance/valid/`
- [ ] `response_schema_ref` if the profile requires a specific API response shape
