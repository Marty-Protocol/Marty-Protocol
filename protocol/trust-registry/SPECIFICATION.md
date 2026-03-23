# Trust Registry — Entity Specification

**Entity:** TrustRegistrySync
**Version:** 0.1.0
**Stability:** Stable
**Section in root spec:** §5.4

---

## Purpose

The Trust Registry provides **delta-sync endpoints for mobile wallet trust anchor updates**. Mobile wallets need an up-to-date set of CSCA/DSC certificates to verify travel documents and other X.509-backed credentials offline. Rather than downloading the full trust store on every launch, wallets use the delta-sync protocol: download the full set once, then request only changes since the last sync.

## API Endpoints

All endpoints are under `/v1/trust-registry`.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/trust-registry/sync` | Delta sync since `?since={sync_token}` |
| GET | `/v1/trust-registry/csca` | Full CSCA list |
| GET | `/v1/trust-registry/dsc` | Full DSC list |
| GET | `/v1/trust-registry/csca/{country_code}` | CSCAs for a specific country |
| GET | `/v1/trust-registry/status` | Registry health and last-sync timestamps |

## Sync Protocol

1. **First sync**: Request without `since` parameter. Receive all entries + `sync_token`.
2. **Subsequent syncs**: Pass `?since={sync_token}`. Receive only `ADD` / `REMOVE` deltas since that token.
3. **Pagination**: If `has_more: true`, follow `sync_token` in the response to fetch remaining pages.

```json
GET /v1/trust-registry/sync
→ {
    "sync_token": "abc123",
    "sequence": 4821,
    "entries": [...],
    "has_more": false,
    "generated_at": "2026-03-11T10:00:00Z"
  }
```

## Entry Types

| `anchor_type` | Description |
|---|---|
| `CSCA` | Country Signing Certificate Authority — root CAs for ICAO eMRTD |
| `DSC` | Document Signer Certificate — leaf certs in the CSCA hierarchy |

## Sources

| Source | Description |
|--------|-------------|
| `ICAO_PKD` | ICAO Public Key Directory (master source for travel documents) |
| `AAMVA` | AAMVA IACA trust list (US/CAN mDL issuers) |
| `EUDI_LOTL` | EU List of Trusted Lists (EUDI wallet ecosystem) |
| `MANUAL` | Manually added by platform administrators |

## Data Schema

See `schemas/trust-registry-sync.json` for the full JSON Schema.

## Constraints

1. Trust Registry endpoints are **read-only** for API consumers; trust anchors are populated by internal sync jobs.
2. `sync_token` values are opaque and must not be parsed or modified by clients.
3. A `sequence` number monotonically increases; gaps indicate deleted entries in intermediate batches.
4. Wallets MUST process `REMOVE` operations to maintain a consistent trust store.
5. Certificates MUST be validated (chain, expiry) by the wallet before trusting them.
