# Application Template — Design Notes

**Version:** 0.1.0

---

## Key Design Decisions

### Separation of Workflow from Crypto

The application form and approval workflow are separated from cryptographic configuration. An HR system changing the employee onboarding form should not require touching the key vault. This separation also allows the same Credential Template to be issued both via form (onboarding) and directly (batch issuance), with different Application Templates or none at all.

### Claim Mapping

`claim_mapping` creates the link between what a user fills out and what appears in the credential. This allows form labels to be user-friendly ("First Name") while credential claims follow specification conventions (`given_name`). Implementations MUST validate all claim_mapping references against the associated Credential Template at template creation time.

### Rules-Based Approval

`approval_rules` is deliberately schema-flexible. The intent is to support various rules engines (simple comparisons, expression trees, decision tables) without mandating a single format. Implementations MUST document their supported `approval_rules` schema.

### Evidence vs. Form Fields

Evidence requirements (document scans, biometrics) are separate from form fields because they:
- Have different storage/retention requirements (PII-sensitive)
- Are processed by a different pipeline (document AI, biometric matching)
- Have different failure modes (OCR errors, liveness check failures)

Evidence processing outputs feed into `ClaimCollectionRules` via `EVIDENCE_EXTRACTION` source type.
