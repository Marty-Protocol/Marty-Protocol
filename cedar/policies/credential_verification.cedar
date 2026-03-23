// ============================================================================
// MIP Cedar Policies — Credential Verification Trust Rules
// ============================================================================
//
// These policies replace the opaque issuer allow/deny lists and inline
// revocation_policy objects in TrustProfile with formally verifiable Cedar
// policies. They are evaluated during the Trust Evaluation Algorithm (§5.7.3)
// to determine whether a presented credential should be accepted.
//
// The CredentialContext is passed in context{} during evaluation, providing:
//   - credential_format, compliance_code, issuer_id, issuer_trust_level
//   - credential_age_seconds, is_revoked, is_expired
//   - holder_binding_present, algorithm
// ============================================================================

// ── Base rule: permit verification for valid, non-revoked credentials ────

@id("permit-valid-credentials")
permit (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    !context.is_revoked &&
    !context.is_expired &&
    context.issuer_trust_level >= 50
};

// ── Forbid: revoked credentials (hard fail) ──────────────────────────────

@id("deny-revoked-credentials")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.is_revoked
};

// ── Forbid: expired credentials ──────────────────────────────────────────

@id("deny-expired-credentials")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.is_expired
};

// ── Forbid: untrusted issuers (trust_level below threshold) ──────────────

@id("deny-untrusted-issuers")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.issuer_trust_level < 10
};

// ── ICAO DTC: require MDOC format + holder binding ───────────────────────

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

@id("icao-dtc-holder-binding")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.compliance_code == "ICAO_DTC" &&
    !context.holder_binding_present
};

// ── AAMVA mDL: require MDOC format + holder binding ──────────────────────

@id("aamva-mdl-format-requirement")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.compliance_code == "AAMVA_MDL" &&
    context.credential_format != "MDOC"
};

@id("aamva-mdl-holder-binding")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.compliance_code == "AAMVA_MDL" &&
    !context.holder_binding_present
};

// ── EUDI PID: require SD_JWT_VC format + holder binding ──────────────────

@id("eudi-pid-format-requirement")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.compliance_code == "EUDI_PID" &&
    context.credential_format != "SD_JWT_VC"
};

@id("eudi-pid-holder-binding")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.compliance_code == "EUDI_PID" &&
    !context.holder_binding_present
};

// ── Algorithm restrictions: forbid weak algorithms ───────────────────────

@id("deny-weak-algorithms")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    context.algorithm == "RS256" ||
    context.algorithm == "RS384"
};

// ── Freshness: reject credentials older than 24 hours for high-assurance ─

@id("high-assurance-freshness")
forbid (
    principal,
    action == MIP::Action::"credentials:verify",
    resource
)
when {
    (context.compliance_code == "ICAO_DTC" ||
     context.compliance_code == "AAMVA_MDL" ||
     context.compliance_code == "EUDI_PID") &&
    context.credential_age_seconds > 86400
};
