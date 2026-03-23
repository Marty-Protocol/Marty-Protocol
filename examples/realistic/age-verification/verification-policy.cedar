// ============================================================================
// Example: Age Verification — Cedar Credential Verification Policy
// ============================================================================
//
// Scenario: A bar or venue verifies that a patron is over 21 using an
// AAMVA mobile driver's license. This policy enforces:
//   - MDOC format required (mDL is always MDOC)
//   - Holder binding must be present (device authentication)
//   - Credential must not be revoked
//   - Only AAMVA-compliant credentials accepted
// ============================================================================

@id("age-verify-permit-valid-mdl")
@description("Accept non-revoked, non-expired AAMVA mDL credentials")
permit (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.compliance_code == "AAMVA_MDL" &&
    context.credential_format == "MDOC" &&
    context.holder_binding_present &&
    !context.is_revoked &&
    !context.is_expired &&
    context.issuer_trust_level >= 50
};

@id("age-verify-deny-non-mdoc")
@description("Reject non-MDOC credentials for age verification")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.credential_format != "MDOC"
};

@id("age-verify-deny-no-holder-binding")
@description("Reject credentials without device authentication")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    !context.holder_binding_present
};

@id("age-verify-deny-revoked")
@description("Hard-fail on revoked credentials")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.is_revoked
};
