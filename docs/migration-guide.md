# MIP Migration Guide

This guide documents coordinated, breaking upgrades between MIP releases. MIP
0.3.1 does not provide a mixed-version wire compatibility window: protocol,
services, clients, generated bindings, and fixtures must move together. A
bounded read-only compatibility path is permitted for persisted legacy values
and explicitly documented inbound aliases; canonical writers never emit them.

## DID-only public issuer migration

The next coordinated release removes signing custody and issuer-profile
selection from public Credential Templates.

1. Preserve existing profile, certificate, verification-method, algorithm, and
   KMS bindings in the implementation's private issuer-profile store.
2. Backfill every issuance template with the canonical public `issuer_did`
   already bound to that profile. Abort on missing, inactive, ambiguous,
   incompatible, or cross-organization mappings.
3. Remove `issuer_profile_id`, `issuer_key_id`, `issuer_algorithm`,
   `key_access_mode`, `issuer_certificate_chain_pem`, `issuer_identity`,
   `remote_signing_config`, and `auto_generate_artifacts` from public request
   and response shapes.
4. Resolve `organization_id` + `issuer_did` + operation/purpose + credential
   format + algorithm to exactly one internal issuer profile, and execute
   signing through that profile. Do not invoke KMS directly from a public
   request handler.
5. Keep any bounded legacy profile-ID reader internal. It may only assert an
   exact match with the DID-resolved profile; canonical writers and public APIs
   never emit it.
6. Run issuance and verification vectors for every supported credential
   format, algorithm, certificate profile, and Python/browser client before
   activating the release.

This migration changes selection, not functionality: managed-key custody,
X.509/mdoc certificate profiles, RSA compatibility, and all supported
credential formats remain available behind issuer profiles.

## Holder Binding and OID4VCI Final Nonce Migration

This migration changes Presentation Policy holder binding and removes draft-era OID4VCI nonce handling.

1. Replace `binding_methods: ["NONCE"]` with an actual control method: `CREDENTIAL_KEY`, `DEVICE_KEY`, or `SESSION_BINDING`.
2. Remove `nonce_required`. Add `proof_profiles` and `proof_freshness`; configure challenge, audience, replay, and optional proof-age checks explicitly.
3. Reject holder-binding configurations when `required` is true but methods, profiles, or freshness rules are missing. Remove all three fields when `required` is false.
4. Stop reading `c_nonce` and `c_nonce_expires_in` from OAuth Token Responses. Discover `nonce_endpoint`, POST an empty body, and use the returned `c_nonce` in the OID4VCI Final `proofs` parameter.
5. Normalize stored Deployment Profiles from `biometric_required` to `operator_biometric_authentication_required`. During the bounded storage migration, readers accept either field, writers emit only the canonical field, and payloads containing both are rejected.
6. Store holder-binding evidence with verification results: required method, validated proof profile, challenge, audience, replay result, proof age when available, and failure reason.

The deployment alias concerns operator authentication only. It MUST NOT be interpreted as credential-holder biometric comparison.

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
