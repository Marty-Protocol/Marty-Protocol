// ============================================================================
// MIP Cedar Policies — API Access Control
// ============================================================================
//
// These policies govern who can call MIP API endpoints. They replace the
// opaque api-key-scopes permission strings with formally verifiable Cedar
// policies that support RBAC, ABAC, and fine-grained conditions.
//
// Evaluation: deny-by-default. At least one permit must match, and zero
// forbid policies may match, for the request to be authorized.
// ============================================================================

// ── Organization admin: full access ──────────────────────────────────────

@id("org-admin-full-access")
permit (
    principal,
    action == MIP::Action::"admin:full",
    resource
)
when {
    principal in resource   // principal must be a member of the target org
};

// ── Role-based access: grant all actions listed in role ──────────────────

// Users in the "Credential Manager" role can issue, revoke, and read
@id("role-credential-manager")
permit (
    principal,
    action in [
        MIP::Action::"credentials:issue",
        MIP::Action::"credentials:revoke",
        MIP::Action::"credentials:read",
        MIP::Action::"templates:read"
    ],
    resource
)
when {
    principal is MIP::User &&
    principal in MIP::Role::"credential-manager"
};

// Users in the "Auditor" role: read-only
@id("role-auditor")
permit (
    principal,
    action in [
        MIP::Action::"audit:read",
        MIP::Action::"credentials:read",
        MIP::Action::"flows:read",
        MIP::Action::"trust:read",
        MIP::Action::"compliance:read"
    ],
    resource
)
when {
    principal is MIP::User &&
    principal in MIP::Role::"auditor"
};

// ── API key: scoped to organization ──────────────────────────────────────

@id("org-apikey-credentials")
permit (
    principal is MIP::ApiKey,
    action in [
        MIP::Action::"credentials:issue",
        MIP::Action::"credentials:revoke",
        MIP::Action::"credentials:read"
    ],
    resource
)
when {
    principal.scope_type == "ORGANIZATION" &&
    principal.enabled
};

// ── Deployment-scoped API keys: restricted action set ────────────────────

@id("deployment-apikey-restricted")
permit (
    principal is MIP::ApiKey,
    action in [
        MIP::Action::"credentials:issue",
        MIP::Action::"credentials:revoke",
        MIP::Action::"credentials:read",
        MIP::Action::"flows:read",
        MIP::Action::"flows:execute",
        MIP::Action::"applications:read",
        MIP::Action::"applications:approve",
        MIP::Action::"trust:read",
        MIP::Action::"compliance:read",
        MIP::Action::"templates:read",
        MIP::Action::"audit:read",
        MIP::Action::"notifications:send"
    ],
    resource
)
when {
    principal.scope_type == "DEPLOYMENT" &&
    principal.enabled &&
    principal in resource  // resource must be within the deployment profile
};

// ── Forbid: disabled keys ────────────────────────────────────────────────

@id("deny-disabled-apikeys")
forbid (
    principal is MIP::ApiKey,
    action,
    resource
)
when {
    !principal.enabled
};

// ── Forbid: suspended users ──────────────────────────────────────────────

@id("deny-suspended-users")
forbid (
    principal is MIP::User,
    action,
    resource
)
when {
    principal.status == "SUSPENDED" ||
    principal.status == "DEACTIVATED"
};

// ── Forbid: write operations without MFA ─────────────────────────────────

@id("require-mfa-for-writes")
forbid (
    principal,
    action in [
        MIP::Action::"trust:write",
        MIP::Action::"trust:admin",
        MIP::Action::"compliance:write",
        MIP::Action::"roles:write",
        MIP::Action::"keys:write",
        MIP::Action::"deployment:write"
    ],
    resource
)
unless {
    context.mfa_authenticated
};
