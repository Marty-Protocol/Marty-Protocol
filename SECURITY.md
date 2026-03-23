# Security Policy

## Supported Versions

| Version | Status |
|---------|--------|
| 0.1.x (draft) | Active development; security issues addressed on best-effort basis |

Once 0.1.0 stable is ratified, the maintainers will publish a formal supported-versions table.

## Reporting a Vulnerability

**Please do not file public GitHub issues for security vulnerabilities.**

To report a security issue privately:

1. Open a **GitHub Security Advisory** on this repository using the "Security" tab → "Advisories" → "New draft security advisory" (preferred).
2. Alternatively, email the maintainers at the address listed in the repository's GitHub profile.

Please include:

- A description of the vulnerability and the affected component (schema, protocol text, conformance fixture, reference implementation)
- Steps to reproduce or a proof-of-concept
- Any suggested remediation if you have one

## Response Timeline

- **Acknowledgement:** within 5 business days
- **Initial assessment:** within 10 business days
- **Fix or mitigation plan:** communicated before any public disclosure

We follow coordinated disclosure. We ask that you give us a reasonable window (typically 90 days) to remediate before publishing details publicly.

## Scope

This policy covers:

- The normative specification text in `SPECIFICATION.md` and `protocol/`
- JSON Schemas in `schemas/` and `enums/`
- Cedar policy schema in `cedar/mip.cedarschema`
- Reference implementations in `reference/`
- Conformance test fixtures in `conformance/`

Issues in third-party dependencies (e.g., `cedarpy`, `jsonschema`) should be reported to those projects directly.

## Out of Scope

- Theoretical attacks with no practical impact on implementors
- Issues requiring physical access to a device
- Social engineering
