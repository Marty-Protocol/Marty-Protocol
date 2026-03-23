# Architecture Decision Record Template

Use this template for all MIP Architecture Decision Records (ADRs). ADR files live in `docs/adr/` and are named `adr-NNNN-brief-title.md`.

---

## ADR-NNNN: {Title}

**Date:** YYYY-MM-DD  
**Status:** {Draft | Proposed | Accepted | Deprecated | Superseded by ADR-XXXX}  
**Deciders:** {Names or roles of people involved in the decision}  
**Tags:** {e.g., security, privacy, schema, api, governance}

---

### Context

*What is the situation or problem that motivated this decision? Include any constraints, requirements, or forces at play. Be specific about what options were considered.*

---

### Decision

*What was decided? State the decision clearly and directly.*

---

### Rationale

*Why was this option chosen over the alternatives? Refer to the design principles in `docs/design-principles.md` where applicable.*

---

### Alternatives Considered

| Alternative | Why Not Chosen |
|-------------|----------------|
| ... | ... |

---

### Consequences

**Positive:**
- ...

**Negative / Tradeoffs:**
- ...

**Neutral:**
- ...

---

### Implementation Notes

*Any specific implementation guidance for developers applying this decision.*

---

### Related

- **Supersedes:** *(ADR number if this replaces an old decision)*
- **Related ADRs:** *(list any relevant existing ADRs)*
- **Spec sections:** *(link to relevant SPECIFICATION.md sections)*
- **Issues / PRs:** *(GitHub references)*

---

## How to Write a Good ADR

1. **Capture decisions when they are made** — an ADR written retroactively loses context.
2. **Include the forces** — what constraints, competing goals, or design principles were in tension?
3. **Be honest about tradeoffs** — every architectural decision has costs; name them.
4. **Link to spec** — if the decision changes normative behavior, update `SPECIFICATION.md` and reference it in the ADR.
5. **Status is a lifecycle** — move from Draft → Proposed (open for comment) → Accepted (merged). If a future decision supersedes this one, update the status and link the successor.

## Existing ADRs

| ADR | Title | Status |
|-----|-------|--------|
| ADR-0001 | Wallet Profile is derived, not stored | Accepted |
| ADR-0002 | Upsert semantics for Device Registration | Accepted |
| ADR-0003 | RSA PKCS#1 DER for device public keys | Accepted |
| ADR-0004 | Credentials prohibited in notification payloads | Accepted |
| ADR-0005 | Compliance Profiles immutable after active reference | Accepted |
| ADR-0006 | SKIP revocation prohibited for ICAO/AAMVA/EUDI | Accepted |
| ADR-0007 | Lanes embedded in Deployment Profiles | Accepted |
| ADR-0008 | Combined flows share a single Trust Profile reference | Accepted |
