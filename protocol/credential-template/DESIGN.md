# Credential Template — Design Notes

**Version:** 0.1.0

---

## Key Design Decisions

### Template vs. Instance

A Credential Template is a definition, not a credential. Many issued credentials (instances) reference one template. This separation allows batch issuance from a single config, analytics by template, and clean revocation at the template level.

### auto_generate_artifacts

`auto_generate_artifacts: true` is a development-time convenience that allows the system to generate ephemeral keys and self-signed certificates. This flag MUST trigger a warning in any dashboard or audit log. It MUST NOT be available in production environments without explicit administrative override.

### Why credential_type Is PascalCase

`credential_type` is a semantic type identifier that appears in VC payloads and SD-JWT-VC `vct` claims. PascalCase ensures compatibility with W3C VC type conventions (e.g., `VerifiableCredential`, `EmployeeBadge`).

### Claim Namespaces

For mDoc credentials, claim namespaces (e.g., `org.iso.18013.5.1`) are normative. The schema system MUST preserve namespace information during credential construction. For SD-JWT-VC and VC-JWT, namespaces are informational only.

### Derived Claims

Common pattern: issuer holds `birth_date` but relying parties want `age_over_21`. The `derived_from` field signals that the claim value is computed (by the issuer's issuance engine) from another claim. This enables:
- ZK predicates in Presentation Policies
- Wallet UI hint: "derived value, original not disclosed"
- Privacy analysis tooling
