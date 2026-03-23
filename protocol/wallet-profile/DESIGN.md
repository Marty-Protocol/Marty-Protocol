# Wallet Profile — Design Notes

**Version:** 0.1.0

---

## Key Design Decisions

### Derived, Not Configured

Wallet compatibility is a property of the ecosystem (which wallets support which specs), not a property that organizations configure. Allowing users to define custom wallet compatibility would lead to incorrect configurations and support issues. The derivation table is curated by MIP protocol implementers and updated as the wallet ecosystem evolves.

### The Registry API Exists But Doesn't Store

The `/v1/wallet-registry` API endpoint is preserved for backward compatibility and discovery UX. The API returns compatibility info derived at query time from the Credential Template's Compliance Profile, not from a stored wallet-registry table.

### Why compliance_profile_code Is an Optional Key Dimension

`null` compliance_profile_code returns a broader wallet list (all wallets that support the format+protocol combination). A specific `compliance_code` may narrow it (e.g., `AAMVA_MDL` narrows to AAMVA-certified mDL wallets specifically, not all ISO 18013-5 compliant wallets). This allows organizations to see minimum viable compatibility (any wallet supporting the format) vs. strict compliance (only AAMVA-certified wallets).

### Platform Coverage

Platform information is included because:
- iOS supports mDL via Apple Wallet (limited to AAMVA/ICAO certified issuers)
- Web wallets have different QR code vs. deep-link flows
- Deployment Profile `environment_config` may restrict platforms

This allows the dashboard to surface "this credential will only work on mobile" before an operator deploys.
