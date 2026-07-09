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
//
// Separation of duties: the user who submitted or created an application cannot
// approve that same application. Implementations should map the applicant or
// internal submitter identity onto resource.submitted_by or resource.created_by
// before evaluation.
//

@id("deny-self-approval")
forbid (
    principal is MIP::User,
    action == MIP::Action::"applications:approve",
    resource is MIP::Application
)
when {
    principal has user_id &&
    (
        (resource has submitted_by && principal.user_id == resource.submitted_by) ||
        (resource has created_by && principal.user_id == resource.created_by)
    )
};
// ============================================================================

// ── Auto-approve: low-risk applications with verified documents ──────────

// External evidence: verified evidence can approve when all required facts are
// satisfied by the normalized EvidenceFact layer.

@id("auto-approve-verified-external-evidence")
permit (
    principal is MIP::ServiceAccount,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    principal.service_name == "canvas-evidence-policy" &&
    context has evidence_provider &&
    context has evidence_verification_status &&
    context has evidence_scope_matched &&
    context has all_required_evidence_satisfied &&
    context has satisfied_requirement_count &&
    context has required_evidence_count &&
    context.evidence_verification_status == "VERIFIED" &&
    context.evidence_scope_matched &&
    context.all_required_evidence_satisfied &&
    context.satisfied_requirement_count >= context.required_evidence_count
};

@id("deny-unverified-external-evidence")
forbid (
    principal is MIP::ServiceAccount,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    principal.service_name == "canvas-evidence-policy" &&
    context has evidence_provider &&
    context has evidence_verification_status &&
    context.evidence_verification_status != "VERIFIED"
};

@id("deny-wrong-scope-external-evidence")
forbid (
    principal is MIP::ServiceAccount,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    principal.service_name == "canvas-evidence-policy" &&
    context has evidence_provider &&
    context has evidence_scope_matched &&
    !context.evidence_scope_matched
};

@id("auto-approve-low-risk")
permit (
    principal is MIP::User,
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
    principal is MIP::User,
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
