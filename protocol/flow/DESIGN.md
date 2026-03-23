# Flow — Design Notes

**Version:** 0.1.0

---

## Key Design Decisions

### Flows as Composable Templates

A Flow definition is reusable — many instances can run from it simultaneously. This matches how real identity programs work: one boarding-pass flow template serves all 200 flights today. Separating definition from execution enables analytics at the flow level and clean state tracking at the instance level.

### Optional Steps Array

The `steps` array is optional. When absent, implementations use the **convention-based** standard sequences (APPLICATION → APPROVAL → ISSUANCE for issuance flows). Explicit steps are for non-standard orchestration: custom retry logic, human-in-the-loop interruptions, conditional issuance based on approval outcome.

### Why Combined Flows Exist

Airport boarding is `COMBINED`: the airline both issues a boarding credential AND verifies it at the gate. A single Flow object keeps the trust configuration anchored in one place, preventing drift between the trust roots used for issuance vs. the trust roots used for verification.

### PAUSED Status

`PAUSED` flows still exist and are visible in dashboards, but create no new instances. This is useful for seasonal programs (e.g., a summer event credential program) that will resume without reconfiguration.

### Deployment Profile IDs on Flows

`deployment_profile_ids` declares where a VERIFICATION flow's presentation requests may be fulfilled. This allows operators to see "which gates is this flow deployed to" from the flow object, and enables future routing logic (e.g., proximity-based credential offers matched to the nearest deployment).
