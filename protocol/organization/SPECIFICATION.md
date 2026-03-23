# Organization — Entity Specification

**Entity:** Organization
**Version:** 0.1.0
**Stability:** Moderate
**Section in root spec:** §17

---

## Purpose

An Organization is the **primary multi-tenant boundary** in MIP. All configuration resources (Trust Profiles, Credential Templates, Compliance Profiles, Flows, etc.) are scoped to an organization. Identity governance — members, roles, invitations, and RBAC — operate within the organization boundary.

Organizations are a MIP-native entity. They are distinct from the IdP (Keycloak, Okta, etc.) that authenticates users. An organization in MIP represents a business or operational unit that issues credentials, configures verification policies, or runs deployment profiles.

---

## Organization Properties

| Property | Type | Required | Constraint |
|----------|------|----------|-----------|
| `id` | UUID | Yes | Unique, auto-generated |
| `name` | string | Yes | Machine-friendly slug: 1–64 chars, pattern `^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$` |
| `display_name` | string | Yes | Human-readable name: 1–128 chars |
| `description` | string | No | Max 1024 chars |
| `join_code` | string | No | 6–16 char alphanumeric code for discoverability |
| `visibility` | string | Yes | `PUBLIC`: discoverable/joinable; `PRIVATE`: invite-only |
| `owner_id` | string | Yes | User ID of the current owner |
| `status` | string | Yes | `ACTIVE`, `SUSPENDED`, `DELETED` |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

---

## Lifecycle States

```
ACTIVE ──► SUSPENDED ──► ACTIVE
  │
  └──► DELETED  (terminal; not reversible via API)
```

- `SUSPENDED` organizations cannot issue credentials or start flows, but existing credentials remain valid until their TTL.
- `DELETED` is a soft delete. Records are retained for audit purposes. All associated operational data is deactivated.

---

## Organization API

```
GET    /v1/organizations                  List organizations (filtered to caller's memberships)
POST   /v1/organizations                  Create organization
GET    /v1/organizations/{id}             Get organization
PUT    /v1/organizations/{id}             Update organization
DELETE /v1/organizations/{id}             Soft-delete organization (owner only)
GET    /v1/organizations/mine             Get all organizations the caller belongs to
GET    /v1/organizations/discover         List PUBLIC organizations (no auth required)
POST   /v1/organizations/join/code        Join organization by join_code
GET    /v1/organizations/join/code/validate  Validate join_code (no auth)
POST   /v1/organizations/{id}/join        Join organization by ID (must be PUBLIC or have invite)
POST   /v1/organizations/{id}/transfer-ownership  Initiate ownership transfer
GET    /v1/organizations/{id}/team/snapshot  Team dashboard (member count, role breakdown)
```

---

## Invitation Workflow

Invitations are short-lived, single-use tokens for adding members to PRIVATE organizations.

### Invitation Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | UUID | Yes | Unique identifier |
| `organization_id` | UUID | Yes | Target organization |
| `invited_by` | string | Yes | User ID of the inviter |
| `email` | string | Yes | Invitee's email address |
| `role_ids` | UUID[] | No | Roles to assign on acceptance |
| `token` | string | Yes | Single-use JWT (returned once at creation) |
| `expires_at` | datetime | Yes | Default: 7 days from creation |
| `accepted_at` | datetime | No | Set when accepted |
| `status` | string | Yes | `PENDING`, `ACCEPTED`, `REVOKED`, `EXPIRED` |

### Invite Token Semantics

- Tokens are JWT-signed by the MIP platform key
- Claims: `{ sub: invite_id, org: organization_id, email: email, exp: expires_at, jti: nonce }`
- Single-use: once accepted, the token MUST be invalidated regardless of `expires_at`
- Token value is returned **only at POST time**; subsequent GET operations return masked `token_prefix` only

### Invitation API

```
GET    /v1/organizations/{id}/invites                   List pending invites
POST   /v1/organizations/{id}/invites                   Create invite (returns token once)
POST   /v1/organizations/{id}/invites/{invite_id}/resend  Resend invite email
DELETE /v1/organizations/{id}/invites/{invite_id}       Revoke invite
GET    /v1/organizations/invitations/validate           Validate token (no auth)
POST   /v1/organizations/invitations/accept             Accept invitation (bearer token required)
```

---

## Ownership Transfer

Ownership transfer is a two-step atomic operation:

1. Current owner initiates: `POST /v1/organizations/{id}/transfer-ownership { "new_owner_id": "..." }`
2. A transfer token is sent to `new_owner_id` via notification
3. New owner confirms: `POST /v1/organizations/{id}/transfer-ownership/confirm { "token": "..." }`

Constraints:
- `new_owner_id` MUST be an existing member of the organization
- Transfer is cancelled if the token is not confirmed within 24 hours
- Current owner retains ownership until step 3 completes

---

## Validation Rules

1. `name` MUST be unique within MIP (case-insensitive).
2. `owner_id` MUST reference an active user with membership in the organization.
3. `join_code` MUST be unique if set.
4. Only the current `owner_id` or a platform super-admin may DELETE an organization.
5. `visibility: PRIVATE` organizations MUST NOT appear in `/v1/organizations/discover`.
6. Deleting an organization MUST deactivate all associated Deployment Profiles and set all active Flows to `PAUSED`.

---

## See Also

- Root specification: [§17 Organization & Identity Governance](../../SPECIFICATION.md#17-organization--identity-governance)
- SCIM specification: [../scim/SPECIFICATION.md](../scim/SPECIFICATION.md)
- Schema: [../../schemas/organization.json](../../schemas/organization.json)
