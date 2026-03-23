# Presentation Policy — Design Notes

**Version:** 0.1.0

---

## Key Design Decisions

### Why Policies Are Data

Presentation policies encode the "what must be shown" rule set as configuration. This means business rule changes (new regulation: must check age more strictly) are policy updates, not code deployments. Auditors can review the policy history to understand what was verified at any given time.

### Predicate-First by Default

Where `prefer_predicates: true`, implementations SHOULD first attempt to satisfy claims with ZK proofs. The `fallback_policy` provides the graceful degradation. This allows a single policy to work across wallets with varying ZK support levels without separate policy versions.

### Why FallbackPolicy Matters

ZK circuits are ecosystem-dependent. A RANGE_PROOF circuit may be available in EUDI wallets but not in older mDL wallets. Rather than blocking verification, `ACCEPT_RAW` fallback allows the system to degrade to raw claim disclosure. `REQUIRE_PREDICATE` is reserved for contexts where unlinkability is a hard requirement.

### Freshness vs. Revocation

`max_age_seconds` checks when the credential was issued. `require_not_revoked` checks whether it was revoked after issuance. Both can be used independently:
- A driving license can be valid (not revoked) but old (issued > 1 year ago)
- An access badge can be fresh (issued today) but revoked (employee terminated)

### Trust Profile Is Optional

Presentation Policies can be trust-agnostic (accept credentials from any compliant issuer) or constrain to a specific Trust Profile. The Deployment Profile's trust_profile_id provides the default constraint; the policy-level `trust_profile_id` can further narrow it (e.g., "only accept this specific airline's credentials at this gate").
