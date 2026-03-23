# MIP Design Principles

This document captures the foundational design principles that guide decisions in the Marty Identity Protocol (MIP). When evaluating changes, additions, or tradeoffs, these principles serve as the deciding criteria.

---

## 1. Separation of Concerns

**Protocol entities are separated by their rate of change and their audience.**

- **Cryptographic trust** (Trust Profile) is owned by security engineers and changes only when trust anchors change.
- **Claim schema** (Credential Template) is owned by product/compliance teams and changes when business requirements evolve.
- **Disclosure policy** (Presentation Policy) is owned by verifier-side product teams and changes when privacy requirements evolve.
- **Operational configuration** (Deployment Profile) is owned by field operations and changes per deployment.
- **Orchestration** (Flow) connects these entities and reflects business process changes.

This separation means a compliance update to a trust anchor does not require redeployment of application-layer configs, and a UX update to a presentation policy does not require cryptographic re-signing.

---

## 2. Privacy by Default

**MIP encodes privacy-preserving choices as the path of least resistance.**

- `prefer_predicates: true` is the recommended setting for any age or threshold claim.
- Selective disclosure is the default in SD-JWT-VC flows — all claims have `sd_disclosure` explicitly set.
- Notifications never carry credential material — only offer URIs.
- Wallet Profiles are derived, not stored, to avoid accumulating device-to-capability fingerprints.
- Device Registration performs a soft delete, never purging records, to support audit trails.

Implementors choosing less-private options (e.g., `fallback_policy: ACCEPT_RAW`, `holder_binding: false`) must explicitly set those values.

---

## 3. Explicit Over Implicit

**Every configurable behavior is named, not inferred.**

- Algorithm support lists are explicit allowlists, not "use best available."
- Revocation check mode (`ONLINE`, `CACHED`, `OFFLINE_GRACE`, `SKIP`) is explicitly set per Revocation Profile — no default.
- Network mode (`ONLINE`, `OFFLINE`, `HYBRID`) is explicitly set per Deployment Profile lane.
- Compliance code references are explicit foreign keys, not inferred from format strings.
- Authorization decisions are expressed as Cedar policies with explicit `permit` and `forbid` rules — no implicit grants.

This prevents silent degradation: if a configuration is incomplete, validation fails loudly rather than silently falling back to an insecure default.

---

## 4. Authorization Is Formally Verifiable

**Access control, trust evaluation, and approval decisions are expressed in a formally verifiable policy language.**

MIP uses [Cedar](https://www.cedarpolicy.com/) as its authorization policy language. Cedar policies provide:

- **Deny-by-default semantics** — a request is denied unless at least one `permit` policy matches and no `forbid` policy matches.
- **Static analysis** — policies can be analyzed offline to verify properties such as "no user outside the organization can delete credentials."
- **Auditability** — every authorization decision can be traced to a specific policy rule.
- **Separation of authorization from code** — changing who can do what never requires a code change.

Authorization rules are stored in PolicySet entities and referenced by Trust Profiles (verification trust), Application Templates (approval rules), Compliance Profiles (verification defaults), and SCIM Roles (API access control). The MIP Cedar schema (`cedar/mip.cedarschema`) defines all entity types, actions, and context types.

---

## 5. Compliance as a First-Class Concept

**Standards compliance is not an annotation — it is a structural constraint.**

Compliance Profile objects are:
- **Immutable** once referenced by an active Credential Template.
- **Version-locked** — a template references a specific version of a compliance profile.
- **System profiles are sealed** — ICAO_DTC, AAMVA_MDL, EUDI_PID, EUDI_MDL cannot be copied and modified.

This ensures that a credential claiming ICAO_DTC compliance actually enforces ICAO_DTC rules, not a user-modified approximation.

---

## 6. Operational Resilience

**Verifier-side deployments must degrade gracefully, not fail silently.**

- `HYBRID` network mode is preferred for physical-world deployments (airports, retail POS).
- `offline_tolerance_seconds` is a first-class field, not a hidden config.
- Revocation Profile provides `offline_grace_seconds` for regulated credential types where SKIP is prohibited.
- Deployment Profiles embed Lanes rather than referencing external lane objects — a deployment profile is self-contained and can be fully evaluated offline.

---

## 7. Derivation Over Registry

**Entities that can be computed SHOULD be derived, not stored.**

Wallet Profile is the canonical example: wallet compatibility is a function of `(credential_format, issuance_protocol, compliance_code)`. Building a static registry of wallet capabilities introduces drift and becomes stale within one release cycle.

The `/v1/wallet-registry` API exists for backward compatibility and developer tooling, but it derives results at query time from the three source-of-truth dimensions.

---

## 8. Upsert Semantics for Device State

**Device registration is naturally upsert-prone and the protocol accommodates this.**

Mobile app uninstall/reinstall, FCM token rotation, and key rotation all result in the same device re-registering with new credentials. The unique key `(user_id, device_id)` ensures idempotent upserts rather than duplicate records. The `key_version` integer supports ordered key rotation without requiring explicit delete-then-create.

---

## 9. Credentials Never Cross Notification Channels

**OID4VCI offer URIs are the only credential-adjacent payload allowed in notifications.**

FCM messages pass through Google infrastructure. Email passes through mail relays. Webhook endpoints may be operated by third parties. Any of these channels could log, intercept, or forward notification payloads.

MIP prohibits credential data in notification bodies. The offer URI is a short-lived, single-use token that has no value without the OID4VCI exchange flow completing.

---

## 10. Stability Tiers

**Different entities have different expected rates of change and different governance.**

| Tier | Entities | Change Frequency |
|------|----------|-----------------|
| **Stable** | Trust Profile, Compliance Profile, Revocation Profile | Months–years |
| **Moderate** | Credential Template | Weeks–months |
| **Dynamic** | Presentation Policy, Application Template | Days–weeks |
| **Operational** | Deployment Profile, Device Registration, Notification Target | Hours–days |
| **Derived** | Wallet Profile | No storage |
| **Per use-case** | Flow | Per business process |

Protocol changes to Stable entities require a minor version bump. Changes to Dynamic/Operational entities are backwards-compatible patches.

---

## 11. Machine-Readable First

**Every normative requirement in the specification has a corresponding JSON Schema constraint.**

The schemas in `schemas/` are not documentation supplements — they are the normative validation artifact. A compliant implementation MUST reject payloads that fail schema validation before applying any business logic.

Human-readable specification text in `SPECIFICATION.md` and `protocol/*/SPECIFICATION.md` is authoritative for intent; JSON Schema is authoritative for structure.
