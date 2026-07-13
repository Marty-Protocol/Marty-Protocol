# MIP Migration Guide

This guide documents coordinated, breaking upgrades between MIP releases. MIP
0.3.1 does not provide a compatibility window: protocol, services, clients,
generated bindings, fixtures, and stored data must move together.

## 0.1.x to 0.3.1

Deploy this release atomically. Mixed MIP versions fail readiness and are not a
supported operating mode.

1. Stop writes and create a restorable database backup.
2. Verify every referenced Credential Template, Application Template, PolicySet,
   Trust Profile, Presentation Policy, and Deployment Profile can be resolved.
3. Run the one-way migrations. Abort on unresolved references.
4. Deploy protocol-generated bindings and every service/client image from the
   same release manifest.
5. Run the MIP version, canonical-route, removed-route, issuance, inventory,
   login, and verification probes before restoring traffic.

Rollback restores the pre-migration database and the complete prior release.
Rolling back individual services is unsupported.

## Required Contract Changes

- Use organization-scoped reviewer routes under
  `/v1/organizations/{org_id}/applicants` and self-service routes under
  `/v1/me/applicant-profile` and `/v1/me/applications`.
- Use `/v1/issued-credentials/mine` for holder inventory.
- Replace `credential_configuration_id` with `credential_template_id` and move
  applicant-entered claims to `form_data`.
- Derive applicant identity, issuer organization, checks, locks, and reviewer
  identity on the server.
- Use `verification_policy_set_id` on Compliance Profiles.
- Use `approval_policy_set_id` for `RULES_BASED` Application Templates.
- Use `auto_issue_on_permit` for Application Template evidence requirements.
- Use canonical Application Template field names: `field_id`, `field_type`,
  `validation_pattern`, `options`, `minimum`, and `maximum`.
- Use `default_policy_id` and `environment_config` on Deployment Profiles.

Removed routes and fields are rejected. They are not aliases and are not read
from historical payload shapes at runtime.

## Validation

Run the schema and conformance checks after migration:

```sh
./scripts/run-conformance.sh
./scripts/generate-bindings.sh --check
```

The release gate must also prove every removed HTTP route returns `404`, every
removed request field returns `422`, and all responses advertise the exact MIP
version from the coordinated release manifest.
