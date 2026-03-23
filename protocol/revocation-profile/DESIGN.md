# Revocation Profile — Design Notes

**Version:** 0.1.0

---

## Key Design Decisions

### Format-Agnostic Model

Revocation is modeled independently of credential format. OCSP works for X.509-based credentials (mDoc, VC-JWT with X.509 issuer); Status List 2021 and Token Status List work for SD-JWT-VC and OID4VCI credentials. The RevocationProfile can contain multiple mechanisms, allowing one profile to serve multiple credential types.

### SKIP Mode: Guarded

`check_mode: SKIP` is provided for test environments and offline use cases where no revocation infrastructure exists. The constraint that `SKIP` MUST NOT be used for ICAO, AAMVA, or EUDI credentials enforces compliance requirements that mandate revocation checks for regulated identity documents.

### Two Timescales: Cache and Grace

- `cache_ttl_seconds`: how long a successful revocation check result is considered fresh (verifier side)
- `offline_grace_seconds`: how long to accept a credential without being able to reach the revocation endpoint

These operate independently. A verifier may cache results for 5 minutes but accept offline grace for 1 hour. This handles intermittent network outages at gate locations without cached results from a prior online session.

### IssuerRevocationConfig

Issuer-side config (batch publishing, auto-index allocation) is embedded in the same object as verifier-side config. This is intentional: the same RevocationProfile may be referenced by both the Credential Template (issuer side) and the Trust Profile (verifier side), ensuring both halves of the revocation system are configured consistently.
