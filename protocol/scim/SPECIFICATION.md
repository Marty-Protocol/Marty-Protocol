# SCIM — Identity Governance Specification

**Entity:** SCIM User, Group, Role
**Version:** 0.1.0
**Stability:** Moderate
**Standards:** RFC 7643 (SCIM Core Schema), RFC 7644 (SCIM Protocol)
**Section in root spec:** §17.5

---

## Purpose

MIP adopts [SCIM 2.0](https://www.rfc-editor.org/rfc/rfc7643) (System for Cross-domain Identity Management) for user and group provisioning within organizations. SCIM provides a standard HTTP-based interface for creating, reading, updating, and deleting identity resources across domain boundaries — compatible with major IdPs (Keycloak, Okta, Ping Identity, Azure AD, etc.).

SCIM in MIP is **org-scoped**: all SCIM endpoints are prefixed with `/v1/organizations/{id}/scim/v2/`. This provides multi-tenant isolation while enabling standard IdP SCIM provisioning integrations.

---

## Conformance Level

MIP implementations MUST conform to:
- RFC 7643 §4 (SCIM Core Schema for User)
- RFC 7643 §4.2 (SCIM Core Schema for Group)
- RFC 7644 §3 (SCIM Protocol)
- RFC 7644 §3.4 (Query/Retrieve resources)
- RFC 7644 §3.5.2 (PATCH with `add`, `remove`, `replace` operations)
- RFC 7644 §3.4.2 (Filtering: `filter` query parameter on `userName`, `emails.value`, `externalId`)

---

## Base URL

```
/v1/organizations/{org_id}/scim/v2/
```

All SCIM paths below are relative to this base.

---

## Discovery Endpoints

```
GET ServiceProviderConfig    SCIM capabilities advertisement (required by RFC 7644 §4)
GET Schemas                  All supported schema URIs
GET ResourceTypes            Supported resource type descriptors
```

### ServiceProviderConfig

Implementations MUST respond with the following capabilities:

```json
{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig"],
  "patch": { "supported": true },
  "bulk": { "supported": false, "maxOperations": 0, "maxPayloadSize": 0 },
  "filter": { "supported": true, "maxResults": 200 },
  "changePassword": { "supported": false },
  "sort": { "supported": true },
  "etag": { "supported": true },
  "authenticationSchemes": [
    {
      "type": "oauthbearertoken",
      "name": "OAuth Bearer Token",
      "description": "Authentication scheme using the OAuth Bearer Token standard"
    }
  ]
}
```

---

## User Resource

### Schema URI
`urn:ietf:params:scim:schemas:core:2.0:User`

### MIP Extension Schema URI
`urn:mip:scim:schemas:extension:Organization:2.0:User`

### Core User Attributes (RFC 7643 §4.1)

| Attribute | Type | Multi-Valued | Description |
|-----------|------|--------------|-------------|
| `id` | string | No | Server-assigned UUID |
| `externalId` | string | No | IdP-provided external identifier |
| `userName` | string | No | Unique username (typically email) — REQUIRED |
| `displayName` | string | No | Full display name |
| `emails` | complex[] | Yes | Email addresses; `primary: true` on exactly one |
| `active` | boolean | No | Active status; `false` = deprovisioned (not deleted) |
| `meta` | complex | No | Resource metadata: `resourceType`, `created`, `lastModified`, `location` |

### MIP Extension Attributes

| Attribute | Type | Multi-Valued | Description |
|-----------|------|--------------|-------------|
| `role_ids` | string[] | Yes | MIP role UUIDs assigned to this member within this organization |
| `is_owner` | boolean | No | Whether this user is the organization owner |
| `joined_at` | datetime | No | ISO 8601 timestamp of when the user joined |

### Example User Response

```json
{
  "schemas": [
    "urn:ietf:params:scim:schemas:core:2.0:User",
    "urn:mip:scim:schemas:extension:Organization:2.0:User"
  ],
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "externalId": "auth0|abc123",
  "userName": "alice@example.com",
  "displayName": "Alice Smith",
  "emails": [
    { "value": "alice@example.com", "primary": true }
  ],
  "active": true,
  "urn:mip:scim:schemas:extension:Organization:2.0:User": {
    "role_ids": ["role-uuid-1", "role-uuid-2"],
    "is_owner": false,
    "joined_at": "2025-01-15T10:30:00Z"
  },
  "meta": {
    "resourceType": "User",
    "created": "2025-01-15T10:30:00Z",
    "lastModified": "2025-03-01T14:22:00Z",
    "location": "/v1/organizations/org-uuid/scim/v2/Users/550e8400-e29b-41d4-a716-446655440000"
  }
}
```

### User Endpoints

```
GET    Users                 List users (supports ?filter=)
POST   Users                 Provision a new user into this organization
GET    Users/{id}            Get user by SCIM ID
PUT    Users/{id}            Replace user (full update)
PATCH  Users/{id}            Partial update (RFC 7644 §3.5.2)
DELETE Users/{id}            Deprovision (sets active=false; does NOT delete records)
```

### Filtering

SCIM `filter` query parameter support is REQUIRED for:
- `userName eq "alice@example.com"`
- `emails.value eq "alice@example.com"`
- `externalId eq "auth0|abc123"`
- `active eq true`
- MIP extension: `urn:mip:scim:schemas:extension:Organization:2.0:User:is_owner eq true`

---

## Group Resource (MIP Roles)

SCIM Groups map directly to **MIP Roles** within an organization. A Group member is a User whose `role_ids` includes this role's UUID.

### Schema URI
`urn:ietf:params:scim:schemas:core:2.0:Group`

### MIP Role Extension Schema URI
`urn:mip:scim:schemas:extension:Organization:2.0:Role`

### Core Group Attributes (RFC 7643 §4.2)

| Attribute | Type | Multi-Valued | Description |
|-----------|------|--------------|-------------|
| `id` | string | No | Server-assigned UUID (same as MIP role UUID) |
| `displayName` | string | No | Role display name — REQUIRED |
| `members` | complex[] | Yes | Members: each has `value` (User SCIM ID) and `display` |
| `meta` | complex | No | Resource metadata |

### MIP Role Extension Attributes

| Attribute | Type | Multi-Valued | Description |
|-----------|------|--------------|-------------|
| `permissions` | string[] | Yes | Permission strings from the permission catalog (e.g., `credentials:issue`, `flows:read`) |
| `is_system_role` | boolean | No | System-defined (read-only) vs. custom role |
| `description` | string | No | Role description |

### Example Group Response

```json
{
  "schemas": [
    "urn:ietf:params:scim:schemas:core:2.0:Group",
    "urn:mip:scim:schemas:extension:Organization:2.0:Role"
  ],
  "id": "role-uuid-1",
  "displayName": "Credential Issuer",
  "members": [
    { "value": "user-scim-id-1", "display": "Alice Smith" }
  ],
  "urn:mip:scim:schemas:extension:Organization:2.0:Role": {
    "permissions": ["credentials:issue", "flows:read", "credential-templates:read"],
    "is_system_role": false,
    "description": "Can issue credentials and read flow state"
  },
  "meta": {
    "resourceType": "Group",
    "created": "2025-01-10T08:00:00Z",
    "lastModified": "2025-02-20T11:45:00Z",
    "location": "/v1/organizations/org-uuid/scim/v2/Groups/role-uuid-1"
  }
}
```

### Group Endpoints

```
GET    Groups                List groups/roles
POST   Groups                Create custom role
GET    Groups/{id}           Get role by SCIM ID
PUT    Groups/{id}           Replace role (full update)
PATCH  Groups/{id}           Partial update (add/remove members, update permissions)
DELETE Groups/{id}           Delete custom role (system roles cannot be deleted)
```

---

## Permission Catalog

The permission catalog is a read-only resource listing all valid permission strings. It is not a standard SCIM resource but is exposed at:

```
GET    /v1/organizations/{id}/permissions
```

Each permission entry has:
- `permission` (string): the permission string (e.g., `credentials:issue`)
- `category` (string): grouping (e.g., `credentials`, `flows`, `trust`, `audit`)
- `description` (string): human-readable description
- `is_destructive` (boolean): whether the permission allows destructive operations

---

## PATCH Operations

SCIM PATCH (RFC 7644 §3.5.2) MUST be supported for both User and Group resources. Operations:

```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
  "Operations": [
    { "op": "add", "path": "members", "value": [{ "value": "user-scim-id" }] },
    { "op": "remove", "path": "members[value eq \"user-scim-id\"]" },
    { "op": "replace", "path": "urn:mip:scim:schemas:extension:Organization:2.0:Role:permissions",
      "value": ["credentials:issue", "flows:read"] }
  ]
}
```

Setting `active: false` on a User via PATCH MUST:
1. Remove the user from all roles in this organization
2. Deactivate their membership (not delete the record)
3. NOT affect the user's membership in other organizations

---

## List Response Format

All list operations return RFC 7644 `ListResponse`:

```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
  "totalResults": 42,
  "startIndex": 1,
  "itemsPerPage": 20,
  "Resources": [ ... ]
}
```

Pagination uses `startIndex` (1-based) and `count` query parameters per RFC 7644 §3.4.2.4.

---

## Error Responses

SCIM errors MUST use RFC 7644 §3.12 error format:

```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
  "status": "400",
  "scimType": "uniqueness",
  "detail": "userName already exists in this organization"
}
```

Standard `scimType` values: `invalidFilter`, `tooMany`, `uniqueness`, `mutability`, `invalidSyntax`, `invalidPath`, `noTarget`, `invalidValue`, `invalidVers`, `sensitive`.

---

## Native Member API

Implementations MAY also expose a non-SCIM native member API for direct MIP-style access. The native API and SCIM API MUST remain consistent — a change via SCIM MUST be visible via the native API and vice versa.

See [§17.6 in the root specification](../../SPECIFICATION.md#176-native-member--rbac-api) for native API paths.

---

## Validation Rules

1. `userName` MUST be unique within an organization.
2. System roles (`is_system_role: true`) MUST NOT be modified or deleted via SCIM or native API.
3. The organization owner (`is_owner: true`) cannot be `DELETE`d or have `active` set to `false` without first completing an ownership transfer.
4. `permissions` values MUST be from the permission catalog. Unknown values MUST be rejected with `scimType: invalidValue`.
5. Deprovisioning (DELETE User) MUST set `active: false`, not physically remove the record.

---

## See Also

- RFC 7643: [SCIM Core Schema](https://www.rfc-editor.org/rfc/rfc7643)
- RFC 7644: [SCIM Protocol](https://www.rfc-editor.org/rfc/rfc7644)
- Root specification: [§17 Organization & Identity Governance](../../SPECIFICATION.md#17-organization--identity-governance)
- Organization specification: [../organization/SPECIFICATION.md](../organization/SPECIFICATION.md)
- Schema: [../../schemas/scim-user-extension.json](../../schemas/scim-user-extension.json)
- Schema: [../../schemas/scim-role.json](../../schemas/scim-role.json)
