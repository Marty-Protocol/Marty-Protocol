# Device Registration — Design Notes

**Version:** 0.1.0

---

## Key Design Decisions

### Upsert Semantics

Device registrations use upsert semantics (unique on `user_id` + `device_id`) because mobile devices re-register on app reinstall, OS update, and token rotation. Silently creating duplicates leads to double notifications and stale token accumulation.

### Why RSA (Not ECDSA) for Device Keys

The implementation uses PKCS#1 DER-encoded RSA keys. This is because:
- Broader compatibility across mobile device secure enclaves (many iOS secure enclaves use RSA 2048)
- Challenge-response signing is not a high-frequency operation (no latency concern)
- Existing implementation uses RSA; migrating to ECDSA is a future enhancement

Future versions of MIP MAY specify ECDSA P-256 as the preferred algorithm and SHOULD support both during transition.

### SHA-256 Thumbprint as KID

Key IDs follow RFC 7638 (JWK Thumbprint). This ensures:
- KIDs are deterministic (not server-generated)
- Clients can compute their own KID before contacting the server
- KIDs change when the key changes (rotation is detectable)

### Soft Delete

Deregistering a device sets `is_active: false` rather than deleting the record. This preserves:
- Audit trail of which devices received which notifications
- Token history for FCM invalidation analytics
- Device key history for challenge-response forensics

### FCM Tokens Are Sensitive

FCM tokens are sufficient to send push notifications to a specific device without any other credential. The specification requires treating them as sensitive (no plaintext logging) equivalent to access tokens.

### Why web Uses "SSE Connection ID" Stored in fcm_token

The `fcm_token` field is named from its primary use case but also stores the SSE subscriber key for web sessions. This avoids a separate field for web. The field name may be renamed in a future version; implementations SHOULD NOT rely on the field name for routing logic.
