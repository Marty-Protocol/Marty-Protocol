// ============================================================================
// MIP Cedar Policies — Application Approval Rules
// ============================================================================
//
// These policies replace the opaque approval_rules object in
// ApplicationTemplate when approval_strategy = RULES_BASED. They express
// auto-approval conditions, manual review triggers, and denial rules as
// formally verifiable Cedar policies.
//
// The ApprovalContext is passed in context{} during evaluation, providing:
//   - risk_score, document_verification_passed, biometric_match_score
//   - evidence_count, applicant_country
// ============================================================================

// ── Auto-approve: low-risk applications with verified documents ──────────

@id("auto-approve-low-risk")
permit (
    principal,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    context.risk_score < 20 &&
    context.document_verification_passed &&
    context.biometric_match_score >= 80 &&
    context.evidence_count >= 1
};

// ── Auto-approve: medium-risk with strong biometrics ─────────────────────

@id("auto-approve-strong-biometrics")
permit (
    principal,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    context.risk_score < 50 &&
    context.document_verification_passed &&
    context.biometric_match_score >= 95
};

// ── Deny: high-risk applications (require escalation) ────────────────────

@id("deny-high-risk-applications")
forbid (
    principal is MIP::ApiKey,            // automated systems cannot approve
    action == MIP::Action::"applications:approve",
    resource
)
when {
    context.risk_score >= 80
};

// ── Deny: no document verification ───────────────────────────────────────

@id("deny-unverified-documents")
forbid (
    principal,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    !context.document_verification_passed
};

// ── Deny: biometric score too low ────────────────────────────────────────

@id("deny-low-biometric-match")
forbid (
    principal,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    context.biometric_match_score < 50
};
