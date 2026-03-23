// ============================================================================
// Example: Pre-Boarding Clearance — Cedar Policies
// ============================================================================
//
// Scenario: Airport pre-boarding verification accepts DTC or MRZ
// credentials with extended offline tolerance (24hr freshness, 1hr
// revocation grace). This demonstrates relaxed policies for
// disconnected environments.
// ============================================================================

@id("boarding-permit-valid")
@description("Accept ICAO credentials within 24-hour freshness window")
permit (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    (context.compliance_code == "ICAO_DTC" ||
     context.compliance_code == "ICAO_MRZ") &&
    context.holder_binding_present &&
    !context.is_expired &&
    context.credential_age_seconds <= 86400 &&   // 24 hours
    context.issuer_trust_level >= 50
};

@id("boarding-soft-fail-revocation")
@description("Accept credentials with stale revocation data up to 1 hour (offline tolerance)")
permit (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    (context.compliance_code == "ICAO_DTC" ||
     context.compliance_code == "ICAO_MRZ") &&
    context.holder_binding_present &&
    !context.is_expired &&
    !context.is_revoked
};

@id("boarding-deny-non-icao")
@description("Only ICAO credentials accepted at boarding gate")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
unless {
    context.compliance_code == "ICAO_DTC" ||
    context.compliance_code == "ICAO_MRZ"
};

@id("boarding-deny-expired")
@description("Expired credentials never accepted")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.is_expired
};
