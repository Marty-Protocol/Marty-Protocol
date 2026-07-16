# Delivery Destination Profile - Entity Specification

**Entity:** Delivery Destination Profile  
**Version:** 0.3.1
**Stability:** Draft  
**Schema:** `schemas/delivery-destination-profile.json`

## Purpose

A Delivery Destination Profile describes where an issued credential can be delivered, opened, imported, or mirrored.

It is intentionally separate from Wallet Profile:

- **Wallet Profile** describes holder-wallet compatibility derived from credential format, issuance protocol, and compliance profile.
- **Delivery Destination Profile** describes an operational destination selected by an organization or holder.

Canvas Credentials institutional publishing is a delivery destination, not a holder wallet. A Canvas/Parchment learner backpack can be modeled as a learner-owned backpack destination when OAuth is configured.

## Modes

| Mode | Setup actor | Meaning |
|------|-------------|---------|
| `holder_wallet` | `learner` or `system` | The holder receives and controls the credential in a wallet using OID4VCI, DIDComm, or another wallet protocol. |
| `learner_backpack` | `learner` | The learner connects a personal backpack or account where the credential can be imported. |
| `organization_mirror` | `org_admin` | The issuer organization publishes a projected badge or delivery record into a destination it controls, such as Canvas Credentials. |
| `direct_delivery` | `system` or `org_admin` | A non-wallet delivery channel such as webhook, email, or partner API delivery. |

## Canvas Credentials Boundary

Canvas Credentials has two different product meanings:

1. **Learner backpack** - a student or learner authorizes their own backpack/account.
2. **Institutional mirror** - an organization publishes a credential or badge view into Canvas Credentials using issuer/admin authority.

The institutional mirror MUST NOT be configured by a student. It depends on organization-managed issuer/API/LTI setup. The learner may consent to showing the issued credential in Canvas, but the integration itself is an organization destination.

For a real Canvas Credentials institutional mirror, the destination profile SHOULD capture:

- provider mode, such as `badgr_api`
- Canvas Credentials API base URL
- issuer/entity ID
- badgeclass/entity ID
- assertion scope, normally `badgeclasses`
- claim projection policy
- canonical provenance URL policy

The API token is secret configuration and MUST NOT live inside the public profile document. The issuer signing key also MUST NOT live in Canvas Credentials; Canvas receives an assertion projection while MIP/ElevenID retains canonical issuer identity, credential status, revocation, and provenance.

## Claim Projection

Organization mirrors SHOULD use `claim_projection_policy` to avoid forwarding the complete credential payload by default.

Recommended policies:

- `public_badge` for Open Badge display fields, issuer, achievement, status URL, and canonical provenance reference.
- `allow_list` when a destination needs specific public claims.
- `full_credential_reference` only when the destination stores a pointer to the canonical credential rather than a raw credential copy.

## API

```text
GET    /v1/delivery-destinations
POST   /v1/delivery-destinations
GET    /v1/delivery-destinations/{id}
PATCH  /v1/delivery-destinations/{id}
DELETE /v1/delivery-destinations/{id}
```

System profiles are read-only. Organization profiles require organization membership and destination-management permission.

## See Also

- Wallet Profile: `protocol/wallet-profile/SPECIFICATION.md`
- Credential Template: `protocol/credential-template/SPECIFICATION.md`
- Application Template: `protocol/application-template/SPECIFICATION.md`
