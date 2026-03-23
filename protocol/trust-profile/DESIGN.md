# Trust Profile — Design Notes

**Version:** 0.1.0

---

## Key Design Decisions

### Why Trust Is Explicit

Implicit trust hierarchies (e.g., "trust any IACA-signed credential") are operationally risky. MIP requires trust_sources to be explicitly enumerated so that:
- Trust changes are auditable events
- Operators can comply with certificate revocations at trust anchor level
- Testing environments cannot accidentally pick up production trust material

### Why Compliance Status Is On the Profile, Not Computed

ComplianceStatus is stored and explicitly set (not computed at query time) to allow background validation jobs to flag issues without blocking the read path. An implementation MAY run a background job that periodically checks trust source freshness and promotes/demotes compliance_status.

### Auto-Generated Profiles

For development and low-security use cases, `auto_generated: true` indicates the profile was generated from a wizard rather than manually configured. This flag informs operators that the profile should be reviewed before production use.

### TrustProfileType

The `profile_type` field provides a high-level classification for filtering and display:
- `ICAO` — ICAO CSCA/IACA-based trust (international travel documents)
- `AAMVA` — AAMVA IACA-based trust (US/Canadian driver licenses)
- `EUDI` — eIDAS-based trust (European Digital Identity)
- `CUSTOM` — Organization-specific or mixed trust

This does NOT constrain which trust_source types can be used. A `CUSTOM` profile may still use `TRUST_LIST` sources.

### Revocation Profile Reference

Trust Profiles can reference a Revocation Profile to specify how revocation is checked when verifying credentials that match this trust profile. This allows organizations to have one strict trust profile with mandatory online OCSP and one with offline grace periods for different deployment contexts.
