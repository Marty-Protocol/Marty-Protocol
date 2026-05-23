// ============================================================================
// Canvas Evidence Fact Approval Examples
// ============================================================================
//
// These policies are examples for organization-owned PolicySets with
// policy_type=APPROVAL_RULES. They assume the provider adapter has already
// normalized Canvas evidence into EvidenceFact records and the fact layer has
// evaluated scope and pass_rule requirements before Cedar runs.
//
// Use these examples as copyable starting points. Keep provider parsing and
// score threshold math outside Cedar; Cedar should approve or deny from the
// provider-neutral ApprovalContext.
// ============================================================================

@id("canvas-deny-unverified-evidence")
forbid (
    principal is MIP::ServiceAccount,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    principal.service_name == "canvas-evidence-policy" &&
    context has evidence_provider &&
    context has evidence_verification_status &&
    context.evidence_provider == "canvas" &&
    context.evidence_verification_status != "VERIFIED"
};

@id("canvas-deny-wrong-scope")
forbid (
    principal is MIP::ServiceAccount,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    principal.service_name == "canvas-evidence-policy" &&
    context has evidence_provider &&
    context has evidence_scope_matched &&
    context.evidence_provider == "canvas" &&
    !context.evidence_scope_matched
};

@id("canvas-course-completion")
permit (
    principal is MIP::ServiceAccount,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    principal.service_name == "canvas-evidence-policy" &&
    context.evidence_provider == "canvas" &&
    context.evidence_fact_type == "canvas.course_completion" &&
    context.evidence_verification_status == "VERIFIED" &&
    context.evidence_scope_matched &&
    context.all_required_evidence_satisfied &&
    context.satisfied_requirement_count >= context.required_evidence_count
};

@id("canvas-assignment-completion")
permit (
    principal is MIP::ServiceAccount,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    principal.service_name == "canvas-evidence-policy" &&
    context.evidence_provider == "canvas" &&
    context.evidence_fact_type == "canvas.assignment_completion" &&
    context.evidence_verification_status == "VERIFIED" &&
    context.evidence_scope_matched &&
    context.all_required_evidence_satisfied &&
    context.satisfied_requirement_count >= context.required_evidence_count
};

@id("canvas-assignment-score")
permit (
    principal is MIP::ServiceAccount,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    principal.service_name == "canvas-evidence-policy" &&
    context.evidence_provider == "canvas" &&
    context.evidence_fact_type == "canvas.assignment_score" &&
    context.evidence_verification_status == "VERIFIED" &&
    context.evidence_scope_matched &&
    context.all_required_evidence_satisfied &&
    context.satisfied_requirement_count >= context.required_evidence_count
};

@id("canvas-quiz-completion")
permit (
    principal is MIP::ServiceAccount,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    principal.service_name == "canvas-evidence-policy" &&
    context.evidence_provider == "canvas" &&
    context.evidence_fact_type == "canvas.quiz_completion" &&
    context.evidence_verification_status == "VERIFIED" &&
    context.evidence_scope_matched &&
    context.all_required_evidence_satisfied &&
    context.satisfied_requirement_count >= context.required_evidence_count
};

@id("canvas-quiz-score")
permit (
    principal is MIP::ServiceAccount,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    principal.service_name == "canvas-evidence-policy" &&
    context.evidence_provider == "canvas" &&
    context.evidence_fact_type == "canvas.quiz_score" &&
    context.evidence_verification_status == "VERIFIED" &&
    context.evidence_scope_matched &&
    context.all_required_evidence_satisfied &&
    context.satisfied_requirement_count >= context.required_evidence_count
};

@id("canvas-module-completion")
permit (
    principal is MIP::ServiceAccount,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    principal.service_name == "canvas-evidence-policy" &&
    context.evidence_provider == "canvas" &&
    context.evidence_fact_type == "canvas.module_completion" &&
    context.evidence_verification_status == "VERIFIED" &&
    context.evidence_scope_matched &&
    context.all_required_evidence_satisfied &&
    context.satisfied_requirement_count >= context.required_evidence_count
};

@id("canvas-manual-instructor-approval")
permit (
    principal is MIP::ServiceAccount,
    action == MIP::Action::"applications:approve",
    resource
)
when {
    principal.service_name == "canvas-evidence-policy" &&
    context.evidence_provider == "canvas" &&
    context.evidence_fact_type == "canvas.manual_instructor_approval" &&
    context.evidence_verification_status == "VERIFIED" &&
    context.evidence_scope_matched &&
    context.all_required_evidence_satisfied &&
    context.satisfied_requirement_count >= context.required_evidence_count
};
