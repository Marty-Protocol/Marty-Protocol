# Notification Target — Entity Specification

**Entity:** Notification Target
**Version:** 0.1.0
**Stability:** Operational
**Section in root spec:** §15

---

## Purpose

A Notification Target, combined with a Notification Payload, describes **multi-channel message delivery** to one or more recipients. Notification Targets enable device-targeted propagation of identity lifecycle events — credential offers, verification requests, approvals, and rejections.

## What It Contains

| Dimension | Description |
|-----------|-------------|
| Target | Org, user, device tokens, webhooks, emails |
| Payload | Title, body, structured data, event type, priority |
| Channels | FCM, SSE, Webhook, Email, SMS |
| Delivery Tracking | Per-channel success, error codes, retry info |

## Notification Target Properties

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `organization_id` | UUID | No | Organization-level target |
| `user_id` | string | No | User-level target |
| `device_tokens` | string[] | No | Direct FCM/SSE tokens |
| `webhook_endpoints` | string[] | No | Absolute HTTPS URLs |
| `email_addresses` | string[] | No | Valid email addresses |
| `channels` | ChannelType[] | Yes | At least one channel |

At least one of `organization_id`, `user_id`, `device_tokens`, `webhook_endpoints`, or `email_addresses` MUST be present.

## Notification Payload Properties

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `id` | UUID | Yes | Auto-generated |
| `title` | string | Yes | Max 256 characters |
| `body` | string | Yes | Max 2048 characters |
| `data` | object | No | Arbitrary JSON; max 4 KB |
| `event_type` | string | Yes | From standard event types or custom |
| `priority` | NotificationPriority | Yes | `LOW`, `NORMAL`, `HIGH`, `CRITICAL` |
| `target` | NotificationTarget | Yes | Targeting configuration |
| `ttl_seconds` | integer | No | Default 86400; must be > 0 |
| `collapse_key` | string | No | Collapse duplicate notifications |
| `correlation_id` | string | No | Tracing token for related events |
| `created_at` | datetime | Yes | ISO 8601 |

## Delivery Result Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `notification_id` | UUID | Yes | Reference to payload |
| `channel` | ChannelType | Yes | Delivery channel |
| `success` | boolean | Yes | True if delivered |
| `attempted_at` | datetime | Yes | Attempt timestamp |
| `delivered_at` | datetime | No | Delivery confirmation timestamp |
| `error_code` | string | No | Channel-specific error code |
| `should_retry` | boolean | No | Whether retry is appropriate |
| `retry_after` | integer | No | Seconds to wait before retry |

## ChannelType Values

| Value | Transport | When to Use |
|-------|-----------|-------------|
| `FCM` | Firebase Cloud Messaging | iOS and Android push notifications |
| `SSE` | Server-Sent Events | Web browser real-time delivery |
| `WEBHOOK` | HTTP POST | Server-to-server event delivery |
| `EMAIL` | SMTP | Async status updates; approvals/rejections |
| `SMS` | SMS gateway | Fallback for mobile; OTP delivery |

## Standard Event Types

| `event_type` | Description | Default Channels |
|-------------|-------------|-----------------|
| `credential.offered` | OID4VCI offer available | `FCM`, `SSE` |
| `credential.issued` | Credential successfully delivered | `FCM`, `SSE` |
| `credential.revoked` | Credential has been revoked | `FCM`, `SSE`, `EMAIL` |
| `verification.requested` | Presentation request to holder | `FCM`, `SSE` |
| `application.received` | Application received by issuer | `EMAIL` |
| `application.approved` | Application approved | `FCM`, `SSE`, `EMAIL` |
| `application.rejected` | Application rejected | `FCM`, `SSE`, `EMAIL` |
| `device.key_expiring` | Signing key nearing expiry | `FCM`, `SSE` |

## Message Propagation Flow

```
1. Identity event triggered
2. NotificationPayload constructed
3. Target resolution:
   - user_id → lookup Device Registrations
   - organization_id → lookup all active devices in org
   - device_tokens → direct FCM/SSE tokens
4. Per-platform routing:
   ios/android → FCM Adapter  → Firebase Cloud Messaging
   web         → SSE Adapter  → Server-Sent Events
   webhooks    → HTTP Adapter → POST to each endpoint
   email       → Email Adapter → SMTP
5. DeliveryResult recorded per channel per device
6. FCM permanent failures → mark Device Registration is_active=false
7. Transient failures → schedule retry with exponential backoff
```

## Security Requirements

1. Notification payloads MUST NOT contain raw credential material. Credentials travel via OID4VCI offer URIs only.
2. FCM tokens MUST NOT be logged in plaintext.
3. Webhook endpoints MUST be HTTPS. HTTP webhook endpoints MUST be rejected.
4. Webhook delivery MUST include an HMAC-SHA256 signature header (`X-MIP-Signature`) for the receiving server to verify.
5. Email notifications MUST NOT include credential data beyond the event type and a portal link.

## HMAC Webhook Signature

```
X-MIP-Signature: sha256=<hex(HMAC-SHA256(webhook_secret, payload_bytes))>
X-MIP-Notification-ID: <notification.id>
X-MIP-Event-Type: <event_type>
```

## Retry Policy

| Failure Type | Retry? | Backoff |
|-------------|--------|---------|
| FCM: `INTERNAL_ERROR` | Yes | Exponential: 1s, 2s, 4s, 8s |
| FCM: `UNAVAILABLE` | Yes | Exponential + jitter |
| FCM: `REGISTRATION_TOKEN_NOT_REGISTERED` | No | Deactivate token |
| Webhook: 5xx | Yes | Exponential up to 3 retries |
| Webhook: 4xx | No | Log error; no retry |
| Email: temporary bounce | Yes | After 30 minutes |
| Email: permanent bounce | No | Mark address invalid |

## API

```
POST   /v1/notifications/send
GET    /v1/notifications/{id}
GET    /v1/notifications/{id}/delivery-results
```

## Examples

### Credential Offer Notification

```json
{
  "title": "Your boarding credential is ready",
  "body": "Tap to add your pre-boarding clearance to your wallet.",
  "data": {
    "offer_uri": "openid-credential-offer://?credential_offer_uri=https://issuer.example.com/offers/abc123"
  },
  "event_type": "credential.offered",
  "priority": "HIGH",
  "target": {
    "user_id": "user-abc123",
    "channels": ["FCM", "SSE"]
  },
  "ttl_seconds": 3600
}
```

## Notification Preferences and Subscriptions

Users and organisation admins may manage their notification preferences via the Preferences resource. Preferences control which event types are delivered to which channels for a given context.

### Notification Preference Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | UUID | Preference record identifier |
| `organization_id` | UUID | Owning organisation |
| `user_id` | UUID (nullable) | If set, user-level preference; otherwise org-level default |
| `event_type` | string | Event type this preference applies to (or `*` for all) |
| `channels` | ChannelType[] | Enabled delivery channels for this event type |
| `enabled` | boolean | Whether notifications for this event type are active |
| `created_at` | datetime | ISO 8601 |

### Preference Resolution Order

1. User-level preference (matching `user_id` + `event_type`) — highest priority
2. User-level wildcard (`user_id` + `event_type: *`)
3. Organisation-level preference (matching `organization_id` + `event_type`)
4. Organisation-level wildcard (`organisation_id` + `event_type: *`)
5. System default (all channels enabled for the event type)

### Preferences API

```
GET    /v1/organizations/{org_id}/notification-preferences
POST   /v1/organizations/{org_id}/notification-preferences
PUT    /v1/organizations/{org_id}/notification-preferences/{id}
DELETE /v1/organizations/{org_id}/notification-preferences/{id}
GET    /v1/users/{user_id}/notification-preferences
POST   /v1/users/{user_id}/notification-preferences
PUT    /v1/users/{user_id}/notification-preferences/{id}
DELETE /v1/users/{user_id}/notification-preferences/{id}
```

---

## Alert Rules

Alert Rules define conditions under which administrative or operational alerts are sent to organisation administrators. Unlike standard lifecycle notifications (which go to credential holders), alert rules target internal users monitoring operational health.

### Alert Rule Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | UUID | Alert rule identifier |
| `organization_id` | UUID | Owning organisation |
| `name` | string | Human-readable rule name |
| `condition_type` | string | See condition types below |
| `threshold` | integer | Numeric threshold for count-based conditions |
| `window_seconds` | integer | Time window for rate-based conditions |
| `severity` | string | `INFO`, `WARNING`, `CRITICAL` |
| `recipient_user_ids` | UUID[] | Users to notify when condition fires |
| `channels` | ChannelType[] | Delivery channels for the alert |
| `enabled` | boolean | Default `true` |
| `created_at` | datetime | ISO 8601 |

### Alert Condition Types

| `condition_type` | Fires When |
|-----------------|------------|
| `revocation_spike` | Revocations exceed `threshold` within `window_seconds` |
| `issuance_failure_rate` | Issuance failure rate exceeds `threshold` percent |
| `key_expiring_soon` | An issuer key expires within `threshold` days |
| `application_queue_depth` | Unreviewed applicants exceed `threshold` count |
| `webhook_failure_rate` | Webhook delivery failures exceed `threshold` percent |
| `trust_profile_degraded` | A trust profile transitions to `NEEDS_ATTENTION` |
| `compliance_check_failed` | A compliance check run produces failures |
| `custom` | Implementation-defined condition; `config` holds condition details |

### Alert Rules API

```
GET    /v1/organizations/{org_id}/alert-rules
POST   /v1/organizations/{org_id}/alert-rules
GET    /v1/organizations/{org_id}/alert-rules/{id}
PUT    /v1/organizations/{org_id}/alert-rules/{id}
DELETE /v1/organizations/{org_id}/alert-rules/{id}
```

---

## Notification Read-State

For in-app (SSE/portal) notifications, MIP tracks per-user read state. This enables unread counts and mark-as-read semantics.

### Read-State Properties

| Property | Type | Description |
|----------|------|-------------|
| `notification_id` | UUID | Reference to the notification payload |
| `user_id` | UUID | Recipient user |
| `read_at` | datetime | Null if unread |
| `dismissed_at` | datetime | Null if not dismissed |

### Read-State Rules

1. A notification is **unread** if `read_at` is null.
2. `PATCH /v1/notifications/{id}/read` sets `read_at` to the current timestamp for the authenticated user.
3. `POST /v1/notifications/read-all` marks all notifications for the authenticated user as read.
4. Dismissed notifications (`dismissed_at` set) SHOULD be excluded from default list responses unless `?include_dismissed=true` is passed.

### Read-State API

```
PATCH  /v1/notifications/{id}/read
DELETE /v1/notifications/{id}/read      (mark as unread)
POST   /v1/notifications/read-all
GET    /v1/notifications/unread-count
```

---

## API

```
POST   /v1/notifications/send
GET    /v1/notifications/{id}
GET    /v1/notifications/{id}/delivery-results
PATCH  /v1/notifications/{id}/read
DELETE /v1/notifications/{id}/read
POST   /v1/notifications/read-all
GET    /v1/notifications/unread-count
```

## Examples

### Credential Offer Notification

```json
{
  "title": "Your boarding credential is ready",
  "body": "Tap to add your pre-boarding clearance to your wallet.",
  "data": {
    "offer_uri": "openid-credential-offer://?credential_offer_uri=https://issuer.example.com/offers/abc123"
  },
  "event_type": "credential.offered",
  "priority": "HIGH",
  "target": {
    "user_id": "user-abc123",
    "channels": ["FCM", "SSE"]
  },
  "ttl_seconds": 3600
}
```

## See Also

- Root specification: [§15 Notification Target](../../SPECIFICATION.md#15-notification-target)
- Schema: [../../schemas/notification-target.json](../../schemas/notification-target.json), [../../schemas/notification-payload.json](../../schemas/notification-payload.json), [../../schemas/webhook.json](../../schemas/webhook.json)
- Enums: [../../enums/channel-types.json](../../enums/channel-types.json), [../../enums/notification-priorities.json](../../enums/notification-priorities.json)
- Device Registration: [../device-registration/SPECIFICATION.md](../device-registration/SPECIFICATION.md)

