# Deployment Profile — Entity Specification

**Entity:** Deployment Profile
**Version:** 0.1.0
**Stability:** Operational
**Section in root spec:** §8

---

## Purpose

A Deployment Profile packages trust configuration, verification policies, and runtime behavior for **physical or logical endpoints**: boarding gates, kiosks, mobile apps, web portals, API clients. It is the bridge between abstract identity policy and real-world operational context.

## What It Contains

| Dimension | Description |
|-----------|-------------|
| Trust | Which Trust Profile governs credential validation |
| Policies | Which Presentation Policies are active |
| Network Mode | Online, offline, or hybrid operation |
| Lanes | Physical/logical zones with device assignments |
| UX Config | Language, signage, operator mode, accessibility |
| Credential Templates | Optional issuance capability at this endpoint |

## Properties

### Core Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `id` | UUID | Yes | Unique |
| `organization_id` | UUID | Yes | Must reference existing organization |
| `name` | string | Yes | 1–128 characters |
| `description` | string | No | Max 1024 characters |
| `trust_profile_id` | UUID | Yes | Must reference existing Trust Profile |
| `presentation_policy_ids` | UUID[] | Yes | At least one; each must reference existing policy |
| `credential_template_ids` | UUID[] | No | For issuance-capable deployments |
| `default_policy_id` | UUID | No | Must be in `presentation_policy_ids` |
| `network_mode` | NetworkMode | Yes | `ONLINE`, `OFFLINE`, `HYBRID` |
| `key_access_mode` | KeyAccessMode | No | `KEY_VAULT`, `HSM`, `DEVICE_KEYSTORE` |
| `environment_config` | EnvironmentConfig | No | See below |
| `update_channel` | UpdateChannel | No | See below |
| `lanes` | Lane[] | No | Logical device groupings |
| `created_at` | datetime | Yes | ISO 8601 |
| `updated_at` | datetime | No | ISO 8601 |

### Lane Fields

| Property | Type | Required | Constraint |
|----------|------|----------|------------|
| `id` | UUID | Yes | Unique |
| `name` | string | Yes | 1–128 characters |
| `deployment_profile_id` | UUID | Yes | Parent; must reference this profile |
| `default_policy_id` | UUID | No | Must be in parent's `presentation_policy_ids` |
| `device_ids` | string[] | No | Device identifiers; unique across all lanes in profile |
| `metadata` | object | No | Zone info, operator assignments, physical location |

### EnvironmentConfig Fields

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `language` | string | `en-US` | BCP 47 language tag |
| `signage_text` | object | {} | Key-value UI display strings |
| `operator_mode` | boolean | false | Show operator UI elements |
| `accessibility_mode` | boolean | false | High-contrast / screen-reader |
| `offline_cache_ttl_seconds` | integer | 86400 | Cache duration for offline use |

### UpdateChannel Fields

| Property | Type | Description |
|----------|------|-------------|
| `channel` | string | `stable`, `beta`, `pinned` |
| `pinned_version` | string | Semantic version (for `pinned` channel) |
| `auto_update` | boolean | Apply updates automatically |

## Constraints

1. `presentation_policy_ids` MUST NOT be empty.
2. `default_policy_id`, if present, MUST appear in `presentation_policy_ids`.
3. `trust_profile_id` MUST reference an existing, `COMPLIANT` Trust Profile for production use.
4. For `network_mode: OFFLINE`, `environment_config.offline_cache_ttl_seconds` SHOULD be explicitly set.
5. Device IDs MUST be unique across all lanes within the same Deployment Profile.
6. A lane `default_policy_id` MUST be in the parent profile's `presentation_policy_ids`.
7. `credential_template_ids`, if present, each MUST reference an `ACTIVE` Credential Template.

## Hierarchy

```
Organization
└── Site (metadata only)
    └── Deployment Profile
        ├── Lane: Gate A
        │   ├── Device: gate-a-scanner-01
        │   └── Device: gate-a-scanner-02
        └── Lane: Gate B
            └── Device: gate-b-kiosk-01
```

## Network Modes

| Mode | Description | Trust Check | Revocation Policy |
|------|-------------|-------------|-------------------|
| `ONLINE` | Full connectivity required | Real-time | Online preferred |
| `OFFLINE` | No network required | Cached trust | Grace period allowed |
| `HYBRID` | Best-effort connectivity | Cached + live fallback | Cached with retry |

## Examples

### Airport Gate Deployment

```json
{
  "id": "dp-gate-12",
  "organization_id": "org-airline",
  "name": "Terminal B Gate 12",
  "trust_profile_id": "tp-icao-dtc",
  "presentation_policy_ids": ["pp-pre-boarding", "pp-boarding"],
  "default_policy_id": "pp-pre-boarding",
  "network_mode": "HYBRID",
  "environment_config": {
    "language": "en-US",
    "operator_mode": true,
    "offline_cache_ttl_seconds": 3600
  },
  "lanes": [
    {
      "id": "lane-gate12-north",
      "name": "Gate 12 North",
      "deployment_profile_id": "dp-gate-12",
      "device_ids": ["scanner-g12n-01", "scanner-g12n-02"]
    }
  ],
  "created_at": "2026-03-11T00:00:00Z"
}
```

## See Also

- Root specification: [§8 Deployment Profile](../../SPECIFICATION.md#8-deployment-profile)
- Schema: [../../schemas/deployment-profile.json](../../schemas/deployment-profile.json), [../../schemas/lane.json](../../schemas/lane.json)
- Enums: [../../enums/network-modes.json](../../enums/network-modes.json)
- Design decisions: [DESIGN.md](./DESIGN.md)
