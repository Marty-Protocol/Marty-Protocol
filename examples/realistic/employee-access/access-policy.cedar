// ============================================================================
// Example: Employee Access Control — Cedar Policies
// ============================================================================
//
// Scenario: An enterprise grants building access based on employee
// credentials. Requires:
//   - Active employment status (ZK equality proof preferred)
//   - Clearance level >= 3 (ZK range proof preferred)
//   - Credential freshness within 8 hours
//   - Holder binding for device authentication
// ============================================================================

// ── Credential verification ──────────────────────────────────────────────

@id("employee-access-permit")
@description("Accept fresh, valid enterprise credentials with holder binding")
permit (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.holder_binding_present &&
    !context.is_revoked &&
    !context.is_expired &&
    context.credential_age_seconds <= 28800 &&  // 8 hours
    context.issuer_trust_level >= 80
};

@id("employee-access-deny-stale")
@description("Reject credentials older than 8 hours for facility access")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.credential_age_seconds > 28800
};

@id("employee-access-deny-revoked")
@description("Hard-fail on revoked employee credentials")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.is_revoked
};

// ── API access: facility security system ─────────────────────────────────

@id("facility-system-read-only")
@description("Facility security kiosk can verify but not issue")
permit (
    principal is MIP::ApiKey,
    action in [
        MIP::Action::"credentials:verify",
        MIP::Action::"credentials:read",
        MIP::Action::"flows:execute"
    ],
    resource
)
when {
    principal.scope_type == "DEPLOYMENT" &&
    principal.enabled
};

@id("facility-system-deny-issuance")
@description("Facility kiosk cannot issue credentials")
forbid (
    principal is MIP::ApiKey,
    action == MIP::Action::"credentials:issue",
    resource
)
when {
    principal.scope_type == "DEPLOYMENT"
};
