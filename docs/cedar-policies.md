# Cedar Policy Integration

The Marty Identity Protocol uses [Cedar](https://www.cedarpolicy.com/) as its policy language for authorization decisions. Cedar provides formally verifiable, analyzable policies that replace the opaque JSON rule objects previously used throughout the protocol.

## Why Cedar?

| Property | Benefit for MIP |
|---|---|
| **Deny-by-default** | Matches MIP's security posture — no implicit trust |
| **Permit + Forbid** | Explicit deny always overrides any permit, preventing privilege escalation |
| **Schema validation** | Policies are validated against the MIP Cedar schema at deploy time |
| **Analyzable** | Automated reasoning can prove policy properties (e.g., "no user can issue credentials without MFA") |
| **Auditable** | Policy text is human-readable and stored alongside the decision for audit |
| **Language SDKs** | Rust, Java, Go SDKs with sub-millisecond evaluation |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     MIP Gateway                          │
│                                                          │
│  Request ──► Cedar Engine ──► Permit/Deny               │
│                  │                                       │
│         ┌────────┴────────┐                              │
│         │  Policy Store   │                              │
│         │  (PolicySets)   │                              │
│         └────────┬────────┘                              │
│                  │                                       │
│         ┌────────┴────────┐                              │
│         │  Entity Store   │                              │
│         │  (Users, Roles, │                              │
│         │   ApiKeys, Orgs)│                              │
│         └─────────────────┘                              │
└─────────────────────────────────────────────────────────┘
```

Every authorization request is modeled as:
- **Principal** — Who is making the request? (`User`, `ApiKey`, `ServiceAccount`)
- **Action** — What do they want to do? (`credentials:issue`, `flows:execute`, etc.)
- **Resource** — What are they acting on? (`Credential`, `Flow`, `Organization`, etc.)
- **Context** — Additional request attributes (`ip_address`, `mfa_authenticated`, `credential_format`, etc.)

## Schema

The MIP Cedar schema is defined in [`cedar/mip.cedarschema`](../cedar/mip.cedarschema). It declares:

### Entity types
| Entity | Role | Parent hierarchy |
|---|---|---|
| `User` | Human user | `Organization`, `Role` |
| `ApiKey` | Programmatic key | `Organization`, `DeploymentProfile` |
| `ServiceAccount` | Backend service | `Organization` |
| `Organization` | Tenant boundary | — |
| `Role` | RBAC group | `Organization` |
| `DeploymentProfile` | Deployment scope | `Organization` |
| `Credential` | Issued/presented credential | `Organization` |
| `Flow` | Flow definition | `Organization` |
| `FlowExecution` | Running flow instance | `Flow`, `Organization` |
| `TrustProfile` | Trust configuration | `Organization` |
| `ComplianceProfile` | Compliance abstraction | `Organization` |
| `CredentialTemplate` | Claim template | `Organization` |
| `PresentationPolicy` | Verification requirements | `Organization` |
| `Application` | Credential application | `Organization`, `Flow` |

### Context types
| Context | Used by | Fields |
|---|---|---|
| `RequestContext` | API access actions | `ip_address`, `timestamp`, `mfa_authenticated`, `session_id`, `user_agent` |
| `CredentialContext` | `credentials:verify` | `credential_format`, `compliance_code`, `issuer_id`, `issuer_trust_level`, `credential_age_seconds`, `is_revoked`, `is_expired`, `holder_binding_present`, `algorithm` |
| `ApprovalContext` | `applications:approve` | `risk_score`, `document_verification_passed`, `biometric_match_score`, `evidence_count`, `applicant_country` |

### Actions
All 32 API key scope strings are registered as Cedar actions (e.g., `MIP::Action::"credentials:issue"`). Each action declares which principal and resource types it applies to.

## Policy Domains

### 1. API Access Control

Governs who can call which MIP API endpoints. Replaces the flat `scopes[]` array on API keys with expressive policies supporting RBAC, ABAC, and conditional access.

**Example — require MFA for administrative writes:**
```cedar
@id("require-mfa-for-writes")
forbid (
    principal,
    action in [
        MIP::Action::"trust:write",
        MIP::Action::"trust:admin",
        MIP::Action::"roles:write",
        MIP::Action::"keys:write"
    ],
    resource
)
unless {
    context.mfa_authenticated
};
```

See: [`cedar/policies/api_access.cedar`](../cedar/policies/api_access.cedar)

### 2. Credential Verification Trust

Evaluated during the Trust Evaluation Algorithm (§5.7.3) to decide whether a presented credential should be accepted. Replaces the `allowed_issuers`/`denied_issuers` lists and opaque `default_verification_rules` with composable permit/forbid policies.

**Example — enforce MDOC format for ICAO DTC:**
```cedar
@id("icao-dtc-format-requirement")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.compliance_code == "ICAO_DTC" &&
    context.credential_format != "MDOC"
};
```

See: [`cedar/policies/credential_verification.cedar`](../cedar/policies/credential_verification.cedar)

### 3. Application Approval Rules

Replaces the opaque `approval_rules` object in `ApplicationTemplate` when `approval_strategy = RULES_BASED`. Cedar policies express auto-approval conditions, escalation triggers, and hard denial rules.

**Example — auto-approve low-risk applications:**
```cedar
@id("auto-approve-low-risk")
permit (
    principal,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    context.risk_score < 20 &&
    context.document_verification_passed &&
    context.biometric_match_score >= 80
};
```

See: [`cedar/policies/approval_rules.cedar`](../cedar/policies/approval_rules.cedar)

## PolicySet Entity

Cedar policies are stored in `PolicySet` entities (schema: [`schemas/policy-set.json`](../schemas/policy-set.json)). Each PolicySet:

- Has a `policy_type` (`ACCESS_CONTROL`, `CREDENTIAL_VERIFICATION`, `APPROVAL_RULES`, `CUSTOM`)
- Contains one or more `cedar_policies[]` with `policy_id`, `effect`, `cedar_text`, and `enabled` flag
- References `cedar_schema_version` for validation
- Has a lifecycle status (`DRAFT`, `ACTIVE`, `ARCHIVED`)

PolicySets are referenced by other entities via UUID foreign keys:
- `ApplicationTemplate.approval_policy_set_id` — approval rules for RULES_BASED flows
- `TrustProfile.verification_policy_set_id` — issuer trust and verification rules
- `ComplianceProfile.verification_policy_set_id` — compliance-level verification constraints
- `ScimRole.policy_set_id` — fine-grained ABAC rules augmenting the permissions array

## Evaluation Semantics

Cedar evaluation follows these rules:

1. **Deny by default** — If no `permit` policy matches, the request is denied
2. **Explicit deny wins** — If any `forbid` policy matches, the request is denied regardless of permits
3. **All conditions must hold** — Every `when` clause must be true, every `unless` clause must be false
4. **Disabled policies are skipped** — `enabled: false` policies do not participate in evaluation

## Migration from Legacy Rules

| Legacy field | Replacement | Migration path |
|---|---|---|
| `ApiKey.scopes[]` | Cedar permit policies on `Role` | Kept for backward compatibility; Cedar policies evaluated in addition |
| `ScimRole.permissions[]` | Cedar policies via `policy_set_id` | Kept for backward compatibility; Cedar forbid policies can restrict |
| `ApplicationTemplate.approval_rules` | `approval_policy_set_id` → PolicySet | Deprecated; Cedar takes precedence when both are set |
| `ComplianceProfile.default_verification_rules` | `verification_policy_set_id` → PolicySet | Deprecated; Cedar takes precedence when both are set |
| `TrustProfile.allowed_issuers` / `denied_issuers` | `verification_policy_set_id` → PolicySet | Kept; Cedar policies evaluated as an additional layer |

## SDK Integration

Cedar has official SDKs for:
- **Rust**: [`cedar-policy`](https://crates.io/crates/cedar-policy) — ideal for backend and verifier implementations
- **Java/Go/Python**: Community bindings wrapping the Rust core
- **WASM**: For browser-side or edge evaluation

The MIP Cedar schema (`cedar/mip.cedarschema`) can be loaded into any Cedar SDK for policy validation and evaluation.

For a complete guide on integrating Cedar into a MIP implementation, see [cedar-integration-guide.md](cedar-integration-guide.md).
