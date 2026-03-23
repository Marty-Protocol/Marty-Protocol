# Subscription, Webhook & API Key — Entity Specification

**Entity:** Subscription, ApiKey
**Version:** 0.1.0
**Stability:** Stable
**Section in root spec:** §13

---

## Purpose

Subscriptions and API Keys are the **integration management layer** for the Marty platform:

- **Subscription** — event-driven delivery of identity lifecycle events to external systems
- **ApiKey** — authentication credential for programmatic API access

## Subscription

A Subscription routes events from the Marty event bus to a configured delivery target.

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/subscriptions` | List subscriptions |
| POST | `/v1/subscriptions` | Create subscription |
| GET | `/v1/subscriptions/{id}` | Get subscription |
| PUT | `/v1/subscriptions/{id}` | Update subscription |
| DELETE | `/v1/subscriptions/{id}` | Delete subscription |
| GET | `/v1/webhooks` | List webhook delivery logs |
| GET | `/v1/webhooks/{id}` | Get webhook delivery detail |

### Event Types

Subscriptions can filter on any of these event type strings:

| Event Type | Trigger |
|---|---|
| `credential.issued` | A credential was successfully issued |
| `credential.revoked` | A credential was revoked |
| `credential.expired` | A credential reached its `valid_until` |
| `flow.completed` | A FlowExecution completed |
| `flow.failed` | A FlowExecution failed |
| `application.submitted` | An application was submitted |
| `application.approved` | An application was approved |
| `application.rejected` | An application was rejected |
| `trust_anchor.revoked` | A CSCA or DSC anchor was revoked |
| `issuer.suspended` | An IssuerEntity was suspended |
| `issuer.revoked` | An IssuerEntity was revoked |

### Delivery Channels

| Channel | Delivery Method |
|---------|----------------|
| `WEBHOOK` | HTTP POST to `delivery.url`; signed with HMAC-SHA256 using `delivery.secret` |
| `EMAIL` | Plain-text email to `delivery.address` |
| `SSE` | Server-Sent Events stream; clients connect via long-lived GET to the SSE endpoint |

### WEBHOOK Signing

Webhooks include an `X-MIP-Signature` header:
```
X-MIP-Signature: sha256=<HMAC-SHA256(payload, secret)>
```

Retry policy: up to `retry_policy.max_attempts` attempts with `retry_policy.backoff_seconds` linear backoff.

### Properties

See `schemas/subscription.json` for full JSON Schema.

Key fields:

| Property | Type | Required | Note |
|----------|------|----------|------|
| `event_types` | string[] | Yes | Min 1; event type strings |
| `delivery.channel` | string | Yes | `WEBHOOK`, `EMAIL`, `SSE` |
| `filter` | object | No | Narrow by credential_types, flow_ids, deployment_profile_ids |
| `enabled` | boolean | Yes | Enable/disable without deleting |

---

## API Key

An ApiKey authenticates machine-to-machine API calls.

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/api-keys` | List API keys (masked) |
| POST | `/v1/api-keys` | Create API key (raw key returned once) |
| DELETE | `/v1/api-keys/{id}` | Revoke API key |

### Key Format

Keys are prefixed: `mk_live_` (production) or `mk_test_` (test environment). Only the first 8 characters (`key_prefix`) are stored; the full key is only returned in the creation response.

### Scopes

| Scope | Permissions |
|-------|-------------|
| `credentials:issue` | Issue credentials via API |
| `credentials:revoke` | Revoke credentials |
| `credentials:read` | List and read credential metadata |
| `flows:read` | Read flow and execution data |
| `flows:write` | Create/update flows |
| `trust:read` | Read trust profiles, frameworks |
| `trust:admin` | Manage trust anchors, issue entities |
| `admin` | Full access |

### Properties

See `schemas/api-key.json` for full JSON Schema.

## Constraints

1. API Key raw values are write-once; store securely on creation.
2. Deleting an API Key immediately invalidates it.
3. Subscription `delivery.secret` is write-only; it cannot be read back.
4. Subscriptions with `enabled: false` do not deliver events but retain their configuration.
