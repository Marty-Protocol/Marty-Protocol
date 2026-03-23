# Device Registration — Entity Specification

**Entity:** Device Registration
**Version:** 0.1.0
**Stability:** Operational
**Section in root spec:** §14

---

## Purpose

A Device Registration records a **user's device** for two purposes:
1. **Push notification delivery** — FCM tokens for iOS/Android, SSE connection IDs for web
2. **Secure challenge-response** — RSA public key for device-bound message authentication

Device Registrations enable device-targeted message propagation for credential offers, verification requests, and other identity lifecycle events.

## What It Contains

| Dimension | Description |
|-----------|-------------|
| Identity | User, organization, device ID |
| Platform | `ios`, `android`, `web` |
| Notification Token | FCM token or SSE connection ID |
| Device Info | App version, OS version, model |
| Signing Key | RSA public key with thumbprint and validity window |
| Preferences | Per-device notification settings |

## Properties

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `id` | UUID | Yes | Primary key; auto-generated |
| `user_id` | string | Yes | Owner user identifier |
| `organization_id` | UUID | No | Organization scope (if multi-tenant) |
| `device_id` | string | Yes | Client-provided; max 256 chars |
| `platform` | Platform | Yes | `ios`, `android`, `web` |
| `fcm_token` | string | Yes | FCM token (mobile) or SSE connection ID (web) |
| `app_version` | string | No | Semantic version string |
| `os_version` | string | No | OS version string |
| `device_model` | string | No | Human-readable model name |
| `preferences` | DevicePreferences | No | Per-device notification config |
| `public_key_der` | string | No | Base64url-encoded RSA public key (PKCS#1 DER) |
| `public_key_kid` | string | Conditional | SHA-256 thumbprint per RFC 7638 |
| `key_valid_from` | datetime | No | Key validity start |
| `key_valid_until` | datetime | No | Key validity end (rotation grace) |
| `is_active` | boolean | Yes | Default true |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |
| `last_seen_at` | datetime | No | Last activity timestamp |

### DevicePreferences Fields

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `credential_notifications` | boolean | true | Credential lifecycle events |
| `verification_notifications` | boolean | true | Verification request events |
| `system_notifications` | boolean | true | System/admin notifications |
| `quiet_hours_start` | string | null | HH:MM (24h) quiet start |
| `quiet_hours_end` | string | null | HH:MM (24h) quiet end |

## Unique Constraints

The pair (`user_id`, `device_id`) MUST be unique. Registering the same user + device combination MUST produce an upsert (update in place), not a duplicate record.

## Platform Routing

| Platform | Token Type | Primary Channel | Fallback |
|----------|-----------|-----------------|---------|
| `ios` | FCM registration token | Firebase Cloud Messaging | Polling |
| `android` | FCM registration token | Firebase Cloud Messaging | Polling |
| `web` | SSE connection ID | Server-Sent Events | Polling |

## Key Management

### Initial Registration (No Key)

A device may register without a public key. Notification delivery works without a key; challenge-response authentication requires one.

### Registration With Key

When `public_key_der` is present:
1. `public_key_kid` MUST be the SHA-256 thumbprint of the public key (RFC 7638)
2. Server MUST verify the key with a challenge-response before storing it
3. `key_valid_from` MUST be set to the time of registration

### Key Rotation

When a device rotates its key:
1. Submit a new `public_key_der`
2. The old key remains valid until `key_valid_until`
3. After `key_valid_until`, old key challenges are rejected
4. Any in-flight challenges from the old key are resolved using the grace period

### Key Retirement

When `key_valid_until` has passed:
- Old challenges using the expired key MUST be rejected
- The `public_key_der` field retains the new key; old key is not stored

## Token Invalidation

When FCM returns a permanent token error (e.g., `REGISTRATION_TOKEN_NOT_REGISTERED`), the implementation MUST:
1. Set `is_active: false` on the registration
2. Log the invalidation event
3. NOT delete the record (audit history)

## Constraints

1. `fcm_token` MUST NOT be empty for `is_active: true` registrations.
2. `platform` MUST be a value from `device-platforms` enum.
3. If `public_key_der` is present, `public_key_kid` MUST also be present.
4. `public_key_kid` MUST be the SHA-256 thumbprint of `public_key_der` (RFC 7638).
5. `key_valid_until`, if set, MUST be after `key_valid_from`.
6. The combination (`user_id`, `device_id`) MUST be unique per upsert.

## API

```
GET    /v1/devices
POST   /v1/devices            (upsert: unique on user_id + device_id)
GET    /v1/devices/{id}
PATCH  /v1/devices/{id}
DELETE /v1/devices/{id}       (soft delete: sets is_active=false)
GET    /v1/users/{user_id}/devices
POST   /v1/devices/{id}/rotate-key
```

## Examples

### Android Device Registration

```json
{
  "user_id": "user-abc123",
  "organization_id": "org-airline",
  "device_id": "android-device-xyz789",
  "platform": "android",
  "fcm_token": "fMjK9zX...(FCM token)...",
  "app_version": "2.4.1",
  "os_version": "Android 14",
  "device_model": "Pixel 8 Pro",
  "is_active": true
}
```

### Device With Signing Key

```json
{
  "user_id": "user-abc123",
  "device_id": "ios-device-abc456",
  "platform": "ios",
  "fcm_token": "aP3kL7W...",
  "public_key_der": "MIIBCgKCAQEA...(base64url)...",
  "public_key_kid": "aYkGQ7m-K8...(SHA-256 thumbprint)...",
  "key_valid_from": "2026-03-11T00:00:00Z",
  "is_active": true
}
```

## See Also

- Root specification: [§14 Device Registration](../../SPECIFICATION.md#14-device-registration)
- Schema: [../../schemas/device-registration.json](../../schemas/device-registration.json)
- Enums: [../../enums/device-platforms.json](../../enums/device-platforms.json)
- Notification Target: [../notification-target/SPECIFICATION.md](../notification-target/SPECIFICATION.md)
- Design: [DESIGN.md](./DESIGN.md)
