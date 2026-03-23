"""MIP Protocol Models — generated from marty-protocol/schemas/*.json
Generated: 2026-03-15
DO NOT EDIT — regenerate with: python scripts/codegen.py python
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from .enums import (
    ApiKeyScope,
    ApprovalStrategy,
    ChannelType,
    ComplianceCode,
    CredentialFormat,
    CredentialRankingStrategy,
    DevicePlatform,
    FallbackPolicy,
    FlowInstanceStatus,
    FlowType,
    IssuanceProtocol,
    NetworkMode,
    NotificationPriority,
    PredicateType,
    RevocationCheckMode,
    RevocationMechanism,
    RevocationReason,
    RevocationTimingMode,
    TrustSourceType,
    ValidationAlgorithm,
    ZkCircuitSystem,
)


class ApiKey(BaseModel):
    """API key for authenticating programmatic access to the Marty gateway. Keys are either
ORGANIZATION-scoped (full org access within their scopes) or DEPLOYMENT-scoped
(restricted to a single deployment profile). The raw key value is only returned on
creation; subsequent reads show a masked representation. Managed via /v1/api-keys."""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    key_prefix: str
    scope_type: Literal["ORGANIZATION", "DEPLOYMENT"]
    deployment_profile_id: str | None = None
    scopes: list[ApiKeyScope]
    enabled: bool
    expires_at: datetime | None = None
    last_used_at: datetime | None = None
    created_at: datetime
    updated_at: datetime | None = None


class Applicant(BaseModel):
    """A person or entity that has applied for a credential through an application-approval
flow. Applicants are a first-class entity with a lifecycle that terminates in credential
issuance, rejection, or withdrawal."""

    id: str
    organization_id: str
    flow_id: str
    credential_template_id: str | None = None
    user_id: str | None = None
    external_id: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    email: str | None = None
    phone: str | None = None
    status: Literal["DRAFT", "SUBMITTED", "UNDER_REVIEW", "PENDING_INFORMATION", "APPROVED", "REJECTED", "WITHDRAWN", "CREDENTIALED", "SUSPENDED"]
    reviewer_id: str | None = None
    reviewer_lock_expires_at: datetime | None = None
    submitted_at: datetime | None = None
    reviewed_at: datetime | None = None
    approved_at: datetime | None = None
    credentialed_at: datetime | None = None
    rejection_reason: str | None = None
    rejection_code: Literal["IDENTITY_UNVERIFIABLE", "DOCUMENT_INVALID", "DOCUMENT_EXPIRED", "BIOMETRIC_MISMATCH", "POLICY_VIOLATION", "INCOMPLETE_APPLICATION", "DUPLICATE_APPLICATION", "OTHER", "None"] | None = None
    application_data: dict[str, Any] | None = None
    vetting_checks: list[dict[str, Any]] | None = None
    issued_credential_id: str | None = None
    metadata: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime | None = None


class ApplicationTemplate(BaseModel):
    """User-facing credential application workflow with form fields, evidence, and approval
config"""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    form_fields: list[dict[str, Any]] | None = None
    evidence_requirements: list[dict[str, Any]] | None = None
    claim_collection_rules: list[dict[str, Any]] | None = None
    approval_strategy: Literal["AUTO", "MANUAL", "RULES_BASED", "EXTERNAL"]
    approval_rules: dict[str, Any] | None = None
    approval_policy_set_id: str | None = None
    notification_config: dict[str, Any] | None = None
    ui_config: dict[str, Any] | None = None
    status: Literal["DRAFT", "ACTIVE", "DEPRECATED"]
    created_at: datetime
    updated_at: datetime | None = None


class BiometricEnrollment(BaseModel):
    """A record of a biometric enrollment event for an applicant. Stores only the modality,
hash of the biometric template, and metadata. Raw biometric data MUST NOT be stored in
this record and MUST NOT be transmitted via the MIP API."""

    id: str
    applicant_id: str
    organization_id: str
    modality: Literal["FACE", "FINGERPRINT", "IRIS", "VOICE", "PALM_VEIN", "SIGNATURE"]
    template_hash: str
    hash_algorithm: Literal["SHA-256", "SHA-384", "SHA-512"]
    provider: str | None = None
    capture_device: str | None = None
    quality_score: float | None = None
    liveness_verified: bool | None = None
    status: Literal["ENROLLED", "REVOKED", "SUPERSEDED"]
    revoked_at: datetime | None = None
    revocation_reason: str | None = None
    created_at: datetime


class CascadeRevocationOperation(BaseModel):
    """Tracks the cascade from a trust anchor or issuer revocation to dependent credentials.
Provides circuit-breaker protection (pauses when affected_credential_count >=
circuit_breaker_threshold), rollback support, and manual confirmation for high-impact
operations."""

    id: str
    organization_id: str
    operation_type: Literal["ISSUER_REVOCATION", "ANCHOR_REVOCATION"]
    trigger_entity_type: Literal["ISSUER", "TRUST_ANCHOR"]
    trigger_entity_id: str
    status: Literal["PENDING_CONFIRMATION", "IN_PROGRESS", "COMPLETED", "ROLLED_BACK", "FAILED"]
    affected_credential_count: int | None = None
    affected_credential_ids: list[str] | None = None
    requires_confirmation: bool | None = None
    confirmed_at: datetime | None = None
    confirmed_by: str | None = None
    max_cascade_depth: int | None = None
    current_depth: int | None = None
    circuit_breaker_threshold: int | None = None
    circuit_breaker_triggered: bool | None = None
    can_rollback: bool | None = None
    rollback_snapshot: dict[str, Any] | None = None
    rolled_back_at: datetime | None = None
    rolled_back_by: str | None = None
    error_message: str | None = None
    metadata: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime | None = None


class ComplianceProfile(BaseModel):
    """Abstraction of credential format complexity behind compliance-oriented identifiers"""

    id: str
    organization_id: str | None = None
    compliance_code: Literal["ICAO_DTC", "ICAO_MRZ", "AAMVA_MDL", "EUDI_PID", "EUDI_MDL", "OB3_JWT", "OB3_JSONLD", "OB2_COMPATIBILITY", "SD_JWT_VC", "ENTERPRISE_VC", "OID4VC", "PEX", "CUSTOM"]
    name: str
    description: str | None = None
    credential_format: Literal["MDOC", "SD_JWT_VC", "VC_JWT", "JSON_LD", "ZK_MDOC"]
    issuance_protocol: Literal["OID4VCI_PRE_AUTH", "OID4VCI_AUTH_CODE", "DIRECT"] | None = None
    issuer_artifact_requirements: dict[str, Any] | None = None
    default_verification_rules: dict[str, Any] | None = None
    verification_policy_set_id: str | None = None
    trust_profile_constraints: dict[str, Any] | None = None
    api_surface: list[dict[str, Any]] | None = None
    discoverable: bool | None = None
    is_system: bool
    created_at: datetime


class CredentialTemplate(BaseModel):
    """Master issuance configuration combining schema, compliance profile, and cryptographic
materials"""

    id: str
    organization_id: str
    name: str
    credential_type: str
    description: str | None = None
    compliance_profile_id: str
    vct: str | None = None
    credential_payload_format: Literal["SD_JWT_VC", "MDOC", "VC_JWT", "JSON_LD"] | None = None
    application_template_id: str | None = None
    trust_profile_id: str | None = None
    revocation_profile_id: str | None = None
    claims: list[dict[str, Any]]
    validity_rules: dict[str, Any]
    issuer_key_id: str | None = None
    issuer_algorithm: str | None = None
    key_access_mode: Literal["KEY_VAULT", "HSM", "LOCAL"] | None = None
    issuer_certificate_chain_pem: str | None = None
    issuer_did: str | None = None
    auto_generate_artifacts: bool | None = None
    privacy_posture: dict[str, Any] | None = None
    status: Literal["DRAFT", "ACTIVE", "DEPRECATED"]
    created_at: datetime
    updated_at: datetime | None = None


class DeploymentProfile(BaseModel):
    """Runtime configuration for a physical or logical identity verification endpoint. Enables
specific Flows and governs network mode, key access, UX, and device grouping via Lanes.
Lanes are managed as sub-resources via POST /v1/identity/deployment-profiles/{id}/lanes."""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    site_id: str | None = None
    enabled_flow_ids: list[str]
    default_presentation_policy_id: str | None = None
    network_mode: Literal["ONLINE", "OFFLINE", "HYBRID"]
    key_access_mode: Literal["KEY_VAULT", "HSM", "DEVICE_KEYSTORE"] | None = None
    ux_config: dict[str, Any] | None = None
    update_policy: dict[str, Any] | None = None
    offline_cache_ttl_hours: int | None = None
    biometric_required: bool | None = None
    audit_all_events: bool | None = None
    lanes: list[Lane] | None = None
    created_at: datetime
    updated_at: datetime | None = None


class DeviceRegistration(BaseModel):
    """User device record for push notification delivery and challenge-response authentication"""

    id: str | None = None
    user_id: str
    organization_id: str | None = None
    device_id: str
    platform: Literal["ios", "android", "web"]
    fcm_token: str
    app_version: str | None = None
    os_version: str | None = None
    device_model: str | None = None
    preferences: dict[str, Any] | None = None
    public_key_der: str | None = None
    public_key_kid: str | None = None
    key_valid_from: datetime | None = None
    key_valid_until: datetime | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None
    last_seen_at: datetime | None = None


class FlowExecution(BaseModel):
    """Runtime state of a single flow instance. Tracks current step, step results, context
data, and lifecycle transitions. Created when a flow is initiated; updated as steps
complete."""

    id: str
    flow_id: str
    flow_type: FlowType
    organization_id: str
    status: FlowInstanceStatus
    current_step: str | None = None
    current_step_index: int | None = None
    step_results: dict[str, Any] | None = None
    context_data: dict[str, Any] | None = None
    issued_credential_id: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    expires_at: datetime | None = None
    error_code: str | None = None
    metadata: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime | None = None


class Flow(BaseModel):
    """End-to-end identity lifecycle orchestration. Each flow_type maps to a fixed protocol
step sequence defined by OID4VCI, OID4VP, mDL ISO 18013-5, or application-approval
workflows."""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    flow_type: Literal["oid4vci_pre_authorized", "oid4vci_authorization_code", "mdl_issuance", "oid4vp_presentation", "mdl_presentation", "siopv2", "application_approval_issuance", "credential_renewal", "credential_revocation", "combined"]
    flow_category: Literal["ISSUANCE", "VERIFICATION", "RENEWAL", "REVOCATION", "COMBINED"] | None = None
    trust_profile_id: str | None = None
    credential_template_id: str | None = None
    application_template_id: str | None = None
    presentation_policy_id: str | None = None
    deployment_profile_ids: list[str] | None = None
    approval_strategy: ApprovalStrategy
    enabled: bool
    hooks: dict[str, Any] | None = None
    trigger: dict[str, Any] | None = None
    status: Literal["DRAFT", "ACTIVE", "PAUSED", "ARCHIVED"]
    created_at: datetime
    updated_at: datetime | None = None


class IssuanceRecord(BaseModel):
    """Record of a credential issuance event"""

    id: str
    flow_id: str
    flow_execution_id: str | None = None
    application_id: str | None = None
    credential_template_id: str
    holder_id: str
    credential_id: str | None = None
    credential_format: Literal["MDOC", "SD_JWT_VC", "VC_JWT", "JSON_LD"] | None = None
    offer_uri: str | None = None
    offer_expires_at: datetime | None = None
    status: Literal["PENDING", "OFFER_SENT", "CLAIMED", "EXPIRED", "FAILED", "REVOKED"]
    revocation_index: int | None = None
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    created_at: datetime
    claimed_at: datetime | None = None


class IssuedCredential(BaseModel):
    """Lifecycle record for an issued credential. Stores metadata without raw credential data
(only a SHA-256 hash for integrity). Links FlowExecution to credential status, status
list entries, and revocation history."""

    id: str
    credential_id: str
    credential_type: str
    credential_format: Literal["MDOC", "SD_JWT_VC", "VC_JWT", "JSON_LD"]
    flow_execution_id: str
    credential_template_id: str
    application_id: str | None = None
    revocation_profile_id: str | None = None
    subject_id: str
    subject_claims_hash: str | None = None
    issued_at: datetime
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    status: Literal["ACTIVE", "SUSPENDED", "REVOKED", "EXPIRED"]
    status_list_entries: list[dict[str, Any]] | None = None
    credential_hash: str | None = None
    revoked_at: datetime | None = None
    revocation_reason: str | None = None
    revoked_by: str | None = None
    created_at: datetime
    updated_at: datetime | None = None


class IssuerEntity(BaseModel):
    """An organisation or authority that issues credentials. Separate from Trust Anchors
(cryptographic roots). An issuer may be backed by one or more trust anchors. Supports
full lifecycle: accreditation, suspension, and revocation."""

    id: str
    organization_id: str | None = None
    issuer_id: str
    issuer_type: Literal["ORGANIZATION", "GOVERNMENT", "DEVICE"]
    display_name: str
    description: str | None = None
    is_system_issuer: bool | None = None
    compliance_status: Literal["ACCREDITED", "COMPLIANT", "SUSPENDED", "REVOKED"]
    accreditation_body: str | None = None
    accreditation_date: datetime | None = None
    valid_from: datetime
    valid_until: datetime | None = None
    trust_anchor_id: str | None = None
    revoked_at: datetime | None = None
    revocation_reason: str | None = None
    revoked_by: str | None = None
    metadata: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime | None = None


class Lane(BaseModel):
    """Logical device grouping within a Deployment Profile"""

    id: str
    name: str
    deployment_profile_id: str
    default_policy_id: str | None = None
    device_ids: list[str] | None = None
    metadata: dict[str, Any] | None = None


class MipConfigurationDiscoveryDocument(BaseModel):
    """Schema for the /.well-known/mip-configuration endpoint response. This document describes
the capabilities, endpoints, and supported profiles of a MIP implementation. Analogous
to OpenID Connect Discovery (RFC 8414) but scoped to MIP-specific capabilities."""

    mip_version: str
    issuer: str
    mip_configuration_endpoint: str
    supported_versions: list[str] | None = None
    implementation_classes: list[str] | None = None
    issuance_endpoint: str | None = None
    openid_credential_issuer: str | None = None
    presentation_endpoint: str | None = None
    token_endpoint: str | None = None
    authorization_endpoint: str | None = None
    supported_credential_formats: list[str] | None = None
    supported_compliance_profiles: list[str] | None = None
    supported_flow_types: list[str] | None = None
    supported_signing_algorithms: list[str] | None = None
    proximity_supported: bool | None = None
    proximity_engagement_methods: list[str] | None = None
    scim_endpoint: str | None = None
    revocation_endpoint: str | None = None
    jwks_uri: str | None = None
    org_endpoints: list[dict[str, Any]] | None = None
    service_documentation: str | None = None
    policy_uri: str | None = None


class NotificationPayload(BaseModel):
    """Message content and routing metadata for multi-channel identity event notification"""

    id: str
    title: str
    body: str
    data: dict[str, Any] | None = None
    event_type: str
    priority: Literal["LOW", "NORMAL", "HIGH", "CRITICAL"]
    target: NotificationTarget
    ttl_seconds: int | None = None
    collapse_key: str | None = None
    correlation_id: str | None = None
    created_at: datetime


class NotificationTarget(BaseModel):
    """Multi-channel message delivery targeting configuration"""

    organization_id: str | None = None
    user_id: str | None = None
    device_tokens: list[str] | None = None
    webhook_endpoints: list[str] | None = None
    email_addresses: list[str] | None = None
    channels: list[str]


class OrganizationTrustProfile(BaseModel):
    """Organisation-specific overlay of a TrustFramework. Separates shared framework
definitions from per-org policy overrides, issuer allow/deny lists, and jurisdiction
filters."""

    id: str
    organization_id: str
    framework_id: str
    name: str
    display_name: str | None = None
    description: str | None = None
    enabled: bool | None = None
    use_case_tags: list[str] | None = None
    compliance_status: Literal["COMPLIANT", "NEEDS_ATTENTION", "SETUP_REQUIRED"]
    auto_generated: bool | None = None
    revocation_policy: dict[str, Any] | None = None
    time_policy: dict[str, Any] | None = None
    allowed_algorithms: list[str] | None = None
    allowed_formats: list[str] | None = None
    allowed_issuers: list[str] | None = None
    denied_issuers: list[str] | None = None
    jurisdiction_filter: list[str] | None = None
    metadata: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime | None = None


class Organization(BaseModel):
    """The primary multi-tenant boundary in MIP. All configuration resources are scoped to an
organization."""

    id: str
    name: str
    display_name: str
    description: str | None = None
    join_code: str | None = None
    visibility: Literal["PUBLIC", "PRIVATE"]
    owner_id: str
    status: Literal["ACTIVE", "SUSPENDED", "DELETED"]
    created_at: datetime
    updated_at: datetime | None = None


class PolicySet(BaseModel):
    """A named collection of Cedar policies that governs authorization decisions within the MIP
platform. PolicySets are referenced by ApplicationTemplate (approval_rules),
TrustProfile (issuer trust), ComplianceProfile (verification rules), and the API gateway
(access control). Each PolicySet contains one or more Cedar policy statements evaluated
using deny-by-default semantics: at least one permit must match and zero forbid policies
may match for the request to be authorized."""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    policy_type: Literal["ACCESS_CONTROL", "CREDENTIAL_VERIFICATION", "APPROVAL_RULES", "CUSTOM"]
    cedar_policies: list[dict[str, Any]]
    cedar_schema_version: str | None = None
    status: Literal["DRAFT", "ACTIVE", "ARCHIVED"]
    created_at: datetime
    updated_at: datetime | None = None


class PresentationPolicy(BaseModel):
    """Minimum disclosure requirements, predicates, and holder binding for credential
verification"""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    purpose: str | None = None
    required_claims: list[dict[str, Any]]
    accepted_credential_types: list[str] | None = None
    trust_profile_id: str | None = None
    holder_binding: dict[str, Any] | None = None
    freshness: dict[str, Any] | None = None
    prefer_predicates: bool | None = None
    supported_circuits: list[str] | None = None
    fallback_policy: Literal["REQUIRE_PREDICATE", "ACCEPT_RAW", "DENY"] | None = None
    issuer_constraints: dict[str, Any] | None = None
    credential_ranking_strategy: Literal["FRESHEST_FIRST", "HIGHEST_TRUST_FIRST", "CUSTOM"] | None = None
    credential_ranking_weights: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime | None = None


class ReviewerLock(BaseModel):
    """A time-bounded exclusive lock that prevents two reviewers from acting on the same
applicant simultaneously. A lock MUST be acquired before transitioning an applicant out
of SUBMITTED or UNDER_REVIEW. Locks expire automatically; the default TTL is 1800
seconds (30 minutes)."""

    id: str
    applicant_id: str
    organization_id: str
    holder_user_id: str
    ttl_seconds: int | None = None
    expires_at: datetime
    released_at: datetime | None = None
    status: Literal["ACTIVE", "RELEASED", "EXPIRED"] | None = None
    created_at: datetime


class RevocationBatch(BaseModel):
    """Privacy-preserving batched revocation. Instead of publishing status list updates
immediately (which enables timing-correlation attacks), the system batches revocations
and publishes at configurable intervals. Interval options: 1h, 6h, 24h."""

    id: str
    organization_id: str
    credential_format: Literal["MDOC", "SD_JWT_VC", "VC_JWT", "JSON_LD"]
    batch_interval: Literal["1h", "6h", "24h"]
    status: Literal["PENDING", "PUBLISHING", "PUBLISHED", "FAILED"]
    pending_credential_ids: list[str] | None = None
    published_credential_count: int | None = None
    status_list_uri: str | None = None
    scheduled_publish_at: datetime | None = None
    published_at: datetime | None = None
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime | None = None


class RevocationProfile(BaseModel):
    """Format-agnostic revocation configuration for issuers and verifiers"""

    id: str
    organization_id: str
    name: str
    revocation_mechanism: list[str]
    mechanism_priority: list[str] | None = None
    check_mode: RevocationTimingMode
    cache_ttl_seconds: int | None = None
    offline_grace_seconds: int | None = None
    issuer_config: dict[str, Any] | None = None
    status_list_url: str | None = None
    created_at: datetime
    updated_at: datetime | None = None


class MipScimRoleGroupExtension(BaseModel):
    """MIP extension attributes for SCIM 2.0 Group resources representing roles. Schema URI:
urn:mip:scim:schemas:extension:Organization:2.0:Role"""

    permissions: list[str] | None = None
    policy_set_id: str | None = None
    is_system_role: bool | None = None
    description: str | None = None


class MipScimUserExtension(BaseModel):
    """MIP extension attributes for SCIM 2.0 User resources. Schema URI:
urn:mip:scim:schemas:extension:Organization:2.0:User"""

    role_ids: list[str] | None = None
    is_owner: bool | None = None
    joined_at: datetime | None = None


class Subscription(BaseModel):
    """Event subscription that routes identity lifecycle events to a configured delivery target
(webhook, email, or SSE channel). Managed via /v1/subscriptions."""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    event_types: list[str]
    delivery: dict[str, Any]
    filter: dict[str, Any] | None = None
    enabled: bool
    retry_policy: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime | None = None


class TrustFramework(BaseModel):
    """System-managed trust framework definition for ICAO, AAMVA, EUDI, or custom identity
ecosystems. Immutable at the system level; organisations reference frameworks via
OrganizationTrustProfile."""

    id: str
    code: str
    display_name: str
    description: str | None = None
    pkd_endpoints: dict[str, Any] | None = None
    default_algorithms: list[str]
    default_formats: list[str]
    validation_ruleset: dict[str, Any] | None = None
    sync_config: dict[str, Any] | None = None
    is_system: bool
    created_at: datetime
    updated_at: datetime | None = None


class TrustProfileIssuer(BaseModel):
    """Join entity between TrustProfile and IssuerEntity with trust scoring and cascade
revocation policy. trust_level is a 0–100 score; future versions will auto-adjust based
on issuer history (failed validations, revocation events, compliance lapses)."""

    id: str
    trust_profile_id: str
    issuer_id: str
    trust_level: int
    relationship_status: Literal["TRUSTED", "DENIED", "UNDER_REVIEW"]
    cascade_revocation_policy: Literal["AUTO_CASCADE", "MANUAL", "NOTIFY_ONLY"]
    metadata: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime | None = None


class TrustProfile(BaseModel):
    """Cryptographic trust configuration for credential issuance and verification. Used by both
issuance flows (which issuer keys are trusted) and verification flows (which credential
issuers/roots are accepted). For org-specific framework overrides, see
OrganizationTrustProfile."""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    profile_type: Literal["ICAO", "AAMVA", "EUDI", "CUSTOM"]
    trust_sources: list[dict[str, Any]]
    allowed_algorithms: list[str]
    revocation_policy: dict[str, Any] | None = None
    revocation_services: dict[str, Any] | None = None
    time_policy: dict[str, Any] | None = None
    supported_formats: list[str]
    allowed_issuers: list[str] | None = None
    denied_issuers: list[str] | None = None
    system_issuer_overrides: dict[str, Any] | None = None
    compliance_status: Literal["COMPLIANT", "NEEDS_ATTENTION", "SETUP_REQUIRED"]
    revocation_profile_id: str | None = None
    verification_policy_set_id: str | None = None
    auto_generated: bool | None = None
    created_at: datetime
    updated_at: datetime | None = None


class TrustRegistrySync(BaseModel):
    """Delta-sync resource for mobile wallet trust registry updates. Provides CSCA/DSC anchor
data from the /v1/trust-registry endpoints so wallets can sync incrementally rather than
downloading the full trust store on every launch."""

    sync_token: str
    sequence: int
    entries: list[dict[str, Any]]
    has_more: bool | None = None
    generated_at: datetime


class VerificationSession(BaseModel):
    """A single presentation-request/response cycle instance"""

    id: str
    flow_id: str
    flow_instance_id: str | None = None
    presentation_policy_id: str
    deployment_profile_id: str | None = None
    verifier_nonce: str | None = None
    holder_id: str | None = None
    status: Literal["PENDING", "AWAITING_PRESENTATION", "VERIFYING", "PASSED", "FAILED", "EXPIRED", "CANCELLED"]
    result: dict[str, Any] | None = None
    expires_at: datetime | None = None
    created_at: datetime
    completed_at: datetime | None = None
    updated_at: datetime | None = None
    error: str | None = None


class VettingCheck(BaseModel):
    """A discrete identity or document verification check performed as part of the applicant
review process. Each check corresponds to a single automated or manual verification
step."""

    id: str
    applicant_id: str
    organization_id: str
    check_type: Literal["DOCUMENT_AUTHENTICITY", "DOCUMENT_EXPIRY", "FACIAL_MATCH", "LIVENESS_DETECTION", "IDENTITY_DATABASE", "WATCHLIST_SCREENING", "ADDRESS_VERIFICATION", "EMAIL_VERIFICATION", "PHONE_VERIFICATION", "BACKGROUND_CHECK", "MANUAL_REVIEW", "CUSTOM"]
    provider: str | None = None
    provider_reference_id: str | None = None
    status: Literal["PENDING", "IN_PROGRESS", "PASSED", "FAILED", "INCONCLUSIVE", "SKIPPED", "EXPIRED"]
    score: float | None = None
    threshold: float | None = None
    failure_reason: str | None = None
    evidence_refs: list[dict[str, Any]] | None = None
    performed_by: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    expires_at: datetime | None = None
    raw_result: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime | None = None


class WalletProfile(BaseModel):
    """Wallet compatibility record for a credential format × protocol × compliance combination.
The canonical wallet profile set is auto-derived from CredentialTemplate configuration
via the derivation key (credential_format, issuance_protocol, compliance_profile_code).
Organizations MAY store override entries at /v1/wallet-registry to extend or customise
the derived profile for their specific deployment. GET /v1/wallet-registry returns
merged results: derived profiles supplemented (or overridden) by stored entries."""

    id: str | None = None
    organization_id: str | None = None
    is_override: bool | None = None
    override_precedence: int | None = None
    name: str
    description: str | None = None
    credential_format: Literal["MDOC", "SD_JWT_VC", "VC_JWT", "JSON_LD"]
    issuance_protocol: Literal["OID4VCI_PRE_AUTH", "OID4VCI_AUTH_CODE", "DIRECT"]
    compliance_profile_code: str | None = None
    wallet_apps: list[str] | None = None
    merge_strategy: Literal["APPEND", "REPLACE"] | None = None
    specifications: list[str] | None = None
    supported_platforms: list[str] | None = None
    deep_link_pattern: str | None = None
    created_at: datetime
    updated_at: datetime | None = None


class Webhook(BaseModel):
    """A persistent webhook subscription that delivers signed HTTP POST callbacks to an
operator-controlled endpoint when specified identity lifecycle events occur. Managed via
/v1/organizations/{org_id}/webhooks."""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    endpoint_url: str
    events: list[str]
    signing_secret: str | None = None
    signing_secret_masked: str | None = None
    enabled: bool
    api_version: str | None = None
    filter: dict[str, Any] | None = None
    delivery_config: dict[str, Any] | None = None
    status: Literal["ACTIVE", "PAUSED", "DISABLED_PERMANENTLY"] | None = None
    failure_count: int | None = None
    last_triggered_at: datetime | None = None
    last_success_at: datetime | None = None
    created_at: datetime
    updated_at: datetime | None = None


# Rebuild models with forward references
ApiKey.model_rebuild()
Applicant.model_rebuild()
ApplicationTemplate.model_rebuild()
BiometricEnrollment.model_rebuild()
CascadeRevocationOperation.model_rebuild()
ComplianceProfile.model_rebuild()
CredentialTemplate.model_rebuild()
DeploymentProfile.model_rebuild()
DeviceRegistration.model_rebuild()
FlowExecution.model_rebuild()
Flow.model_rebuild()
IssuanceRecord.model_rebuild()
IssuedCredential.model_rebuild()
IssuerEntity.model_rebuild()
Lane.model_rebuild()
MipConfigurationDiscoveryDocument.model_rebuild()
NotificationPayload.model_rebuild()
NotificationTarget.model_rebuild()
OrganizationTrustProfile.model_rebuild()
Organization.model_rebuild()
PolicySet.model_rebuild()
PresentationPolicy.model_rebuild()
ReviewerLock.model_rebuild()
RevocationBatch.model_rebuild()
RevocationProfile.model_rebuild()
MipScimRoleGroupExtension.model_rebuild()
MipScimUserExtension.model_rebuild()
Subscription.model_rebuild()
TrustFramework.model_rebuild()
TrustProfileIssuer.model_rebuild()
TrustProfile.model_rebuild()
TrustRegistrySync.model_rebuild()
VerificationSession.model_rebuild()
VettingCheck.model_rebuild()
WalletProfile.model_rebuild()
Webhook.model_rebuild()
