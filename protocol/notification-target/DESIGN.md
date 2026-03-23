# Notification Target — Design Notes

**Version:** 0.1.0

---

## Key Design Decisions

### Credentials Never in Notification Bodies

Notification bodies carry metadata and offer URIs only. The OID4VCI offer URI is a short-lived URL that the wallet resolves separately to fetch the credential. This preserves:
- Push notification body privacy (FCM pushes pass through Google servers)
- Credential delivery atomicity (credential fetch is a separate authenticated request)
- Revocability of the offer independent of the notification

### Multi-Level Targeting

The three targeting dimensions (org, user, direct tokens) enable:
- **Broadcast**: send to all devices in an organization
- **User-targeted**: send to all devices of a specific user
- **Device-targeted**: send to a specific already-known device token (e.g., in a proximity flow)

These can be mixed: `user_id` + `device_tokens` sends to both the user's registered devices AND additional tokens (e.g., a temporary kiosk token).

### fcm_token Reuse for SSE

The `fcm_token` field in Device Registration stores the SSE subscriber ID for web devices. Notification dispatch logic uses `platform` to determine whether to route to FCM or SSE. This is a pragmatic choice to avoid schema changes; a future version SHOULD separate these into `push_token` and `sse_subscriber_id`.

### Collapse Keys

`collapse_key` allows multiple pending notifications of the same type to collapse into one delivery. This is critical for verification requests: if a user holds their device near a gate scanner multiple times, only the most recent verification request needs to be delivered.

### Webhook HMAC Signatures

Webhook delivery includes an HMAC-SHA256 signature so receiving servers can verify the notification came from MIP, not an attacker. The signature uses a shared secret configured at webhook endpoint registration time.

### Delivery Results Are Immutable

`DeliveryResult` records are append-only. Each delivery attempt creates a new record. This gives operators a full audit trail of delivery attempts, failures, and retries for compliance and debugging.
