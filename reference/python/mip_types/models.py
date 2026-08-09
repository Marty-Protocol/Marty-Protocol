"""MIP Protocol Models — generated from marty-protocol/schemas/*.json
Protocol version: 0.5.0
DO NOT EDIT — regenerate with: python scripts/codegen.py python
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from .enums import (
    ApiKeyScope,
    ApplicantStatus,
    ApprovalStrategy,
    ChannelType,
    ClaimBlockerOwner,
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
    TrustProfileStatus,
    TrustSourceType,
    ValidationAlgorithm,
    VerificationCheckCategory,
    VerificationCheckOutcome,
    VerificationDecision,
    VerificationProcessingStatus,
    ZkCircuitSystem,
)


class ActiveComplianceProfile(BaseModel):
    """Deployment discovery projection of an active Compliance Profile and the discoverable API
surface it requires."""

    compliance_code: str
    credential_format: CredentialFormat | None = None
    issuance_protocol: IssuanceProtocol | None = None
    api_surface: list[dict[str, Any]]


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


class ApplicantApplication(BaseModel):
    """A holder-owned credential application created from an active ApplicationTemplate.
Identity, credential policy, checks, and issuer data are server-derived."""

    id: str
    applicant_id: str
    organization_id: str
    reference_number: str | None = None
    application_template_id: str
    credential_template_id: str
    form_data: dict[str, Any]
    integration_context: dict[str, Any]
    status: Literal["DRAFT", "SUBMITTED", "UNDER_REVIEW", "PENDING_INFORMATION", "APPROVED", "REJECTED", "WITHDRAWN", "OFFERED", "CREDENTIALED", "SUSPENDED"]
    claim_state: Literal["NOT_READY", "BLOCKED", "OFFER_READY", "CLAIMED", "EXPIRED"]
    claim_blocker: ClaimBlocker | None = None
    credential_display_name: str | None = None
    credential_offer_uri: str | None = None
    credential_offer_uris: dict[str, Any] | None = None
    credential_offer_labels: dict[str, Any] | None = None
    offer_expires_at: datetime | None = None
    submitted_at: datetime | None = None
    reviewed_at: datetime | None = None
    issued_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class ApplicationTemplate(BaseModel):
    """MIP 0.3 user-facing credential application workflow with canonical form fields,
evidence, checks, approval policy, and lifecycle state"""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    credential_template_id: str | None = None
    form_fields: list[dict[str, Any]] | None = None
    evidence_requirements: list[dict[str, Any]] | None = None
    claim_collection_rules: list[dict[str, Any]] | None = None
    required_checks: list[dict[str, Any]] | None = None
    approval_strategy: Literal["AUTO", "MANUAL", "RULES_BASED", "EXTERNAL"]
    approval_policy_set_id: str | None = None
    application_validity_days: int | None = None
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


class ClaimBlocker(BaseModel):
    """A privacy-safe, recoverable reason that an approved application cannot yet produce a
credential offer."""

    code: str
    owner: ClaimBlockerOwner
    message: str


class ComplianceProfile(BaseModel):
    """Abstraction of credential format complexity behind compliance-oriented identifiers"""

    id: str
    organization_id: str | None = None
    compliance_code: Literal["ICAO_DTC", "ICAO_MRZ", "ICAO_PASSPORT", "AAMVA_MDL", "EUDI_PID", "EUDI_MDL", "OB3_JWT", "OB3_JSONLD", "SD_JWT_VC", "ENTERPRISE_VC", "OID4VC", "PEX", "CUSTOM"]
    name: str
    description: str | None = None
    version: str | None = None
    specification_reference: str | None = None
    credential_format: CredentialFormat
    issuance_protocol: IssuanceProtocol | None = None
    issuer_artifact_requirements: dict[str, Any] | None = None
    verification_policy_set_id: str | None = None
    trust_profile_constraints: dict[str, Any] | None = None
    api_surface: list[dict[str, Any]] | None = None
    discoverable: bool | None = None
    required_claims: list[dict[str, Any]] | None = None
    optional_claims: list[dict[str, Any]] | None = None
    required_namespaces: list[str] | None = None
    optional_namespaces: list[str] | None = None
    required_contexts: list[str] | None = None
    supported_proof_types: list[str] | None = None
    supported_algorithms: list[str] | None = None
    key_requirements: dict[str, Any] | None = None
    revocation_methods: list[RevocationMechanism] | None = None
    revocation_required: bool | None = None
    allow_skip_revocation: bool | None = None
    trust_source_types: list[str] | None = None
    holder_binding_required: bool | None = None
    selective_disclosure_required: bool | None = None
    immutable: bool | None = None
    oid4vci_features: dict[str, Any] | None = None
    oid4vp_features: dict[str, Any] | None = None
    pex_requirements: dict[str, Any] | None = None
    physical_production: dict[str, Any] | None = None
    pki_hierarchy: dict[str, Any] | None = None
    vetting_requirements: dict[str, Any] | None = None
    conformance_tests: list[dict[str, Any]] | None = None
    status: Literal["DRAFT", "ACTIVE", "SUSPENDED", "DEPRECATED"]
    is_system: bool
    created_at: datetime
    updated_at: datetime | None = None


class CredentialRenewalOfferResponse(BaseModel):
    """Public wallet handoff produced for an eligible issued-credential renewal."""

    source_credential_id: str
    transaction_id: str
    credential_offer_uri: str
    credential_offer_uris: dict[str, Any]
    credential_offer_labels: dict[str, Any]
    expires_at: datetime


class CredentialTemplate(BaseModel):
    """Public issuance configuration combining claims, compliance, issuer DID, and validity
rules. Custody and signing-profile metadata are resolved internally from the
organization and issuer DID."""

    id: str
    organization_id: str
    name: str
    credential_type: str
    description: str | None = None
    compliance_profile_id: str
    vct: str | None = None
    doctype: str | None = None
    credential_payload_format: CredentialFormat | None = None
    application_template_id: str | None = None
    trust_profile_id: str | None = None
    revocation_profile_id: str | None = None
    claims: list[dict[str, Any]]
    validity_rules: dict[str, Any]
    issuer_did: str
    privacy_posture: dict[str, Any] | None = None
    status: Literal["DRAFT", "ACTIVE", "DEPRECATED"]
    created_at: datetime
    updated_at: datetime | None = None


class DeliveryDestinationProfile(BaseModel):
    """A delivery destination describes where an issued credential can be delivered, opened,
imported, or mirrored. Unlike WalletProfile, it can represent holder wallets, learner-
owned backpacks, organization-managed mirrors such as Canvas Credentials, or custom
delivery channels."""

    id: str
    organization_id: str | None = None
    is_system: bool | None = None
    name: str
    description: str | None = None
    provider: Literal["elevenid_wallet", "oid4vci_wallet", "didcomm_v2", "canvas_credentials", "canvas_credentials_backpack", "open_badges_backpack", "physical_personalization_bureau", "custom"]
    mode: Literal["holder_wallet", "learner_backpack", "organization_mirror", "direct_delivery", "physical_production"]
    setup_actor: Literal["learner", "org_admin", "system"]
    delivery_target: Literal["wallet", "didcomm_v2", "canvas_credentials", "external_api", "webhook", "physical_document"]
    wallet_profile_id: str | None = None
    credential_format: Literal["MDOC", "SD_JWT_VC", "VC_JWT", "JSON_LD", "ICAO_EMRTD", "None"] | None = None
    issuance_protocol: Literal["OID4VCI_PRE_AUTH", "OID4VCI_AUTH_CODE", "DIRECT", "PHYSICAL_DOCUMENT", "None"] | None = None
    compliance_profile_code: str | None = None
    connector_type: str | None = None
    connector_id: str | None = None
    requires_consent: bool | None = None
    claim_projection_policy: dict[str, Any] | None = None
    setup_requirements: list[str] | None = None
    capabilities: dict[str, Any] | None = None
    docs_url: str | None = None
    is_enabled: bool | None = None
    created_at: datetime
    updated_at: datetime | None = None


class DeploymentProfile(BaseModel):
    """Runtime configuration for a physical or logical identity verification endpoint. Packages
trust, policies, issuance capability, network mode, user experience, and device grouping
via Lanes."""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    trust_profile_id: str
    presentation_policy_ids: list[str]
    credential_template_ids: list[str] | None = None
    default_policy_id: str | None = None
    site_id: str | None = None
    enabled_flow_ids: list[str] | None = None
    network_mode: Literal["ONLINE", "OFFLINE", "HYBRID"]
    key_access_mode: Literal["KEY_VAULT", "HSM", "DEVICE_KEYSTORE"] | None = None
    environment_config: dict[str, Any] | None = None
    update_channel: Literal["stable", "beta", "pinned"] | None = None
    update_policy: dict[str, Any] | None = None
    offline_cache_ttl_hours: int | None = None
    operator_biometric_authentication_required: bool | None = None
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
    key_version: int | None = None
    key_valid_from: datetime | None = None
    key_valid_until: datetime | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None
    last_seen_at: datetime | None = None


class DidcommDeliverRequest(BaseModel):
    """Tenant-scoped request to deliver an already-authorized issuance transaction over
encrypted DIDComm v2"""

    organization_id: str
    transaction_id: str
    holder_did: str


class DidcommDeliveryResponse(BaseModel):
    """Result of encrypted DIDComm v2 credential delivery"""

    transaction_id: str
    credential_id: str
    holder_did: str
    service_endpoint: str
    didcomm_message_id: str
    status: Literal["delivered", "delivery_failed"]
    error: str | None = None


class EvidenceFact(BaseModel):
    """Immutable normalized fact derived from verified evidence. Provider adapters create
EvidenceFacts from receipts so approval policy can evaluate facts without parsing
provider payloads."""

    id: str
    organization_id: str
    application_id: str
    subject_id: str
    provider: str
    fact_type: str
    scope: dict[str, Any]
    assertion: dict[str, Any]
    verification: dict[str, Any]
    source: dict[str, Any]
    created_at: datetime


class FlowCreateRequest(BaseModel):
    """Create a tenant-scoped orchestration definition through the public API."""

    organization_id: str
    name: str
    description: str | None = None
    flow_type: FlowType
    trust_profile_id: str | None = None
    credential_template_id: str | None = None
    application_template_id: str | None = None
    presentation_policy_id: str | None = None
    delivery_destination_profile_id: str | None = None
    deployment_profile_ids: list[str] | None = None
    approval_strategy: ApprovalStrategy | None = None
    hooks: dict[str, Any] | None = None
    trigger: dict[str, Any] | None = None
    extension: dict[str, Any] | None = None


class FlowExecutionStartRequest(BaseModel):
    """Start an authorized Flow execution in an explicitly selected organization."""

    organization_id: str
    flow_definition_id: str
    subject_id: str | None = None
    subject_type: str | None = None
    external_reference: str | None = None
    initial_context: dict[str, Any] | None = None


class FlowExecution(BaseModel):
    """Public, tenant-scoped projection of a single Flow execution. Internal custody selectors,
bearer credentials, pre-authorized codes, and service state are never part of this
representation."""

    id: str
    flow_id: str | None
    flow_type: FlowType | None
    organization_id: str
    status: FlowInstanceStatus
    current_step: str | None = None
    current_step_index: int | None = None
    step_results: dict[str, Any]
    context_data: dict[str, Any]
    issued_credential_id: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    expires_at: datetime | None = None
    error_code: str | None = None
    metadata: dict[str, Any]
    state_history: list[dict[str, Any]]
    created_at: datetime
    updated_at: datetime


class FlowExtension(BaseModel):
    """Versioned non-standard orchestration envelope. A custom Flow uses this object so it
cannot claim the conformance semantics of a standard FlowType."""

    extension_uri: str
    extension_version: str
    extends_flow_type: dict[str, Any]
    entry_step_id: str
    steps: list[dict[str, Any]]
    transitions: list[dict[str, Any]]
    config: dict[str, Any] | None = None


class FlowUpdateRequest(BaseModel):
    """Patch a tenant-scoped Flow. The service validates the complete merged definition before
persisting it."""

    organization_id: str
    name: str | None = None
    description: str | None = None
    flow_type: FlowType | None = None
    trust_profile_id: str | None = None
    credential_template_id: str | None = None
    application_template_id: str | None = None
    presentation_policy_id: str | None = None
    delivery_destination_profile_id: str | None = None
    deployment_profile_ids: list[str] | None = None
    approval_strategy: ApprovalStrategy | None = None
    hooks: dict[str, Any] | None = None
    trigger: dict[str, Any] | None = None
    extension: dict[str, Any] | None = None


class Flow(BaseModel):
    """End-to-end identity lifecycle orchestration. Standard FlowTypes have fixed protocol
sequences; non-standard graphs use flow_type custom with a versioned extension envelope."""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    flow_type: FlowType
    flow_category: Literal["ISSUANCE", "VERIFICATION", "RENEWAL", "REVOCATION", "COMBINED"]
    resolved_steps: list[str]
    trust_profile_id: str | None = None
    credential_template_id: str | None = None
    application_template_id: str | None = None
    presentation_policy_id: str | None = None
    delivery_destination_profile_id: str | None = None
    deployment_profile_ids: list[str] | None = None
    approval_strategy: ApprovalStrategy
    hooks: dict[str, Any] | None = None
    trigger: dict[str, Any] | None = None
    extension: FlowExtension | None = None
    status: Literal["DRAFT", "ACTIVE", "PAUSED", "ARCHIVED"]
    version: int
    created_at: datetime
    updated_at: datetime


class HolderCredentialInventory(BaseModel):
    """Privacy-filtered response from GET /v1/issued-credentials/mine. Credential material,
claims, hashes, signing references, and opaque subject identifiers are prohibited."""

    items: list[dict[str, Any]]
    total: int
    limit: int
    offset: int


class IssuanceRequest(BaseModel):
    """Public request to create a credential issuance. Custody and issuer-profile selectors are
intentionally absent."""

    organization_id: str
    credential_template_id: str | None = None
    issuer_did: str | None = None
    subject_did: str | None = None
    holder_did: str | None = None
    authorized_client: dict[str, Any] | None = None
    application_id: str | None = None
    claims: dict[str, Any] | None = None
    credential_subject: dict[str, Any] | None = None
    credential_document: dict[str, Any] | None = None


class IssuanceResponse(BaseModel):
    """Public result of initiating credential issuance. The offer URI is the wallet handoff;
the underlying pre-authorized code is never returned as a separate management API field."""

    id: str
    organization_id: str
    credential_template_id: str
    status: Literal["pending", "authorized", "signing", "issued", "failed", "expired", "revoked"]
    credential_offer_uri: str
    credential_offer_uris: dict[str, Any]
    credential_offer_labels: dict[str, Any]
    expires_at: datetime


class IssuanceTransaction(BaseModel):
    """Public management projection of a tenant-scoped credential issuance transaction. OAuth
tokens, pre-authorized codes, custody selectors, signing-service identifiers, keys, and
raw credential payloads are excluded."""

    id: str
    organization_id: str
    credential_template_id: str
    applicant_id: str | None = None
    application_id: str | None = None
    subject_did: str | None = None
    status: Literal["pending", "authorized", "signing", "issued", "failed", "expired", "revoked"]
    created_at: datetime
    expires_at: datetime | None = None
    issued_at: datetime | None = None
    revoked_at: datetime | None = None
    revocation_reason: str | None = None


class IssuedCredentialLifecycleRequest(BaseModel):
    """Reason supplied for a tenant-bound issued-credential lifecycle transition."""

    reason: str | None = None


class IssuedCredential(BaseModel):
    """Lifecycle record for an issued credential. Stores metadata without raw credential data
(only a SHA-256 hash for integrity). Links FlowExecution to credential status, status
list entries, and revocation history."""

    id: str
    organization_id: str
    credential_id: str
    credential_type: str
    credential_format: Literal["MDOC", "SD_JWT_VC", "VC_JWT", "JSON_LD"]
    flow_execution_id: str
    credential_template_id: str
    application_id: str | None = None
    revocation_profile_id: str | None = None
    renewed_from_credential_id: str | None = None
    renewed_to_credential_id: str | None = None
    renewable: bool | None = None
    renewal_eligible_at: datetime | None = None
    can_renew: bool | None = None
    subject_id: str
    issuer_did: str | None = None
    subject_claims_hash: str | None = None
    issued_at: datetime
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    status: Literal["ACTIVE", "SUSPENDED", "REVOKED", "EXPIRED"]
    status_list_entries: list[dict[str, Any]]
    credential_hash: str | None = None
    revoked_at: datetime | None = None
    revocation_reason: str | None = None
    revoked_by: str | None = None
    created_at: datetime
    updated_at: datetime | None = None


class IssuerEntityCreateRequest(BaseModel):
    """Create an organization-scoped issuer trust-registry record. Global/system issuers are
managed outside this public operation."""

    organization_id: str
    issuer_id: str
    issuer_type: Literal["ORGANIZATION", "GOVERNMENT", "DEVICE"] | None = None
    display_name: str
    description: str | None = None
    compliance_status: Literal["ACCREDITED", "COMPLIANT", "SUSPENDED"] | None = None
    accreditation_body: str | None = None
    accreditations: list[str] | None = None
    accreditation_date: datetime | None = None
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    trust_anchor_id: str | None = None
    metadata: dict[str, Any] | None = None


class IssuerEntityUpdateRequest(BaseModel):
    """Partially update an organization-scoped issuer trust-registry record. organization_id
binds the mutation to its tenant."""

    organization_id: str
    display_name: str | None = None
    description: str | None = None
    issuer_type: Literal["ORGANIZATION", "GOVERNMENT", "DEVICE"] | None = None
    compliance_status: Literal["ACCREDITED", "COMPLIANT", "SUSPENDED", "REVOKED"] | None = None
    accreditation_body: str | None = None
    accreditations: list[str] | None = None
    accreditation_date: datetime | None = None
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    trust_anchor_id: str | None = None
    metadata: dict[str, Any] | None = None
    revocation_reason: str | None = None


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
    is_system_issuer: bool
    compliance_status: Literal["ACCREDITED", "COMPLIANT", "SUSPENDED", "REVOKED"]
    accreditation_body: str | None = None
    accreditations: list[str]
    accreditation_date: datetime | None = None
    valid_from: datetime
    valid_until: datetime | None = None
    trust_anchor_id: str | None = None
    revoked_at: datetime | None = None
    revocation_reason: str | None = None
    revoked_by: str | None = None
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime


class IssuerIdentityCertificateRequest(BaseModel):
    """Attach a public X.509 certificate chain to exactly one DID-selected issuer identity. The
leaf public key must match the DID identity's managed key."""

    organization_id: str
    issuer_did: str
    key_purpose: Literal["vc_jwt_issuer", "mdoc_dsc", "x509_doc_signer", "holder_binding", "presentation_signing", "oid4vp_request_signing", "vdsnc_signing", "csca", "jwks_signing", "lti_tool_signing"]
    credential_format: CredentialFormat
    algorithm: Literal["ES256", "ES384", "RS256", "EdDSA"]
    cert_pem: str
    cert_chain_pem: str | None = None


class IssuerIdentityCreateRequest(BaseModel):
    """Provision or adopt a tenant-scoped issuer DID using implementation-managed custody. The
implementation selects the signing service and key; callers cannot provide custody
coordinates."""

    organization_id: str
    issuer_did: str
    key_purpose: Literal["vc_jwt_issuer", "mdoc_dsc", "x509_doc_signer", "holder_binding", "presentation_signing", "oid4vp_request_signing", "vdsnc_signing", "csca", "jwks_signing", "lti_tool_signing"]
    credential_format: CredentialFormat
    algorithm: Literal["ES256", "ES384", "RS256", "EdDSA"]
    key_attestation_policy: KeyAttestationPolicy | None = None


class IssuerIdentityCreateResponse(BaseModel):
    """Provider-neutral result of ensuring a DID issuer identity."""

    identity: IssuerIdentity
    created: bool


class IssuerIdentityDeleteResponse(BaseModel):
    """Provider-neutral result of retiring a DID issuer identity."""

    deleted: IssuerIdentity


class IssuerIdentityListResponse(BaseModel):
    """Public issuer identities available in the authenticated organization scope."""

    identities: list[IssuerIdentity]


class IssuerIdentityOperationRequest(BaseModel):
    """Select exactly one tenant issuer identity for a lifecycle operation without exposing its
private issuer profile or custody binding."""

    organization_id: str
    issuer_did: str
    key_purpose: Literal["vc_jwt_issuer", "mdoc_dsc", "x509_doc_signer", "holder_binding", "presentation_signing", "oid4vp_request_signing", "vdsnc_signing", "csca", "jwks_signing", "lti_tool_signing"]
    credential_format: CredentialFormat
    algorithm: Literal["ES256", "ES384", "RS256", "EdDSA"]


class IssuerIdentityResolutionResponse(BaseModel):
    """Public material resolved for exactly one DID identity tuple. The response never exposes
or accepts a verification-method, profile, service, key-reference, provider, or KMS
selector."""

    identity: IssuerIdentity
    public_jwk: dict[str, Any]


class IssuerIdentity(BaseModel):
    """A tenant-scoped public DID projection that callers may select for issuance or signed
verification. Custody coordinates and internal issuer-profile IDs are never part of this
resource."""

    issuer_did: str
    key_purpose: Literal["vc_jwt_issuer", "mdoc_dsc", "x509_doc_signer", "holder_binding", "presentation_signing", "oid4vp_request_signing", "vdsnc_signing", "csca", "jwks_signing", "lti_tool_signing"]
    credential_format: CredentialFormat
    algorithm: Literal["ES256", "ES384", "RS256", "EdDSA"]
    status: Literal["active"]


class KeyAttestationPolicy(BaseModel):
    """Provider-neutral trust policy for holder-key attestations presented during issuance. It
contains public trust material and validation requirements, never issuer custody
coordinates."""

    mode: Literal["disabled", "optional", "required"]
    trusted_root_certificates_pem: list[str] | None = None
    allowed_algorithms: list[str] | None = None
    required_key_storage: list[str] | None = None
    required_user_authentication: list[str] | None = None
    max_age_seconds: int | None = None
    require_nonce: bool | None = None
    status_validation: Literal["disabled", "if_present", "required"] | None = None
    status_list_allowed_origins: list[str] | None = None
    status_list_trusted_root_certificates_pem: list[str] | None = None
    status_list_allowed_algorithms: list[str] | None = None
    status_list_max_age_seconds: int | None = None
    status_list_allow_private_hosts: bool | None = None
    status_list_tls_ca_certificates_pem: list[str] | None = None


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
    supported_versions: list[str]
    implementation_classes: list[str]
    issuance_endpoint: str | None = None
    openid_credential_issuer: str | None = None
    presentation_endpoint: str | None = None
    token_endpoint: str | None = None
    authorization_endpoint: str | None = None
    supported_credential_formats: list[str] | None = None
    supported_compliance_profiles: list[str] | None = None
    active_compliance_profiles: list[ActiveComplianceProfile]
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


class OID4VCINonceResponse(BaseModel):
    """Response from the OID4VCI 1.0 Final Nonce Endpoint. The HTTP response must also include
Cache-Control: no-store."""

    c_nonce: str


class OrganizationCreateRequest(BaseModel):
    """Create an Organization through the public API. Discovery and admission settings are
explicit and persisted."""

    name: str
    display_name: str
    description: str | None = None
    org_type: Literal["enterprise", "startup", "individual", "government", "education", "healthcare", "financial", "other"] | None = None
    contact_email: str | None = None
    visibility: Literal["PUBLIC", "PRIVATE"] | None = None
    join_mechanism: Literal["open", "code", "invite", "domain"] | None = None
    requires_approval: bool | None = None


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


class OrganizationUpdateRequest(BaseModel):
    """Partially update an Organization through the public API. organization_id is required to
bind the mutation to its tenant."""

    organization_id: str
    name: str | None = None
    display_name: str | None = None
    description: str | None = None
    org_type: Literal["enterprise", "startup", "individual", "government", "education", "healthcare", "financial", "other"] | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    website: str | None = None
    visibility: Literal["PUBLIC", "PRIVATE"] | None = None
    join_mechanism: Literal["open", "code", "invite", "domain"] | None = None
    requires_approval: bool | None = None


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
    status: Literal["active", "suspended", "pending"]
    org_type: Literal["enterprise", "startup", "individual", "government", "education", "healthcare", "financial", "other"]
    join_mechanism: Literal["open", "code", "invite", "domain"]
    requires_approval: bool
    is_discoverable: bool
    contact_email: str | None = None
    contact_phone: str | None = None
    website: str | None = None
    membership: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime | None = None


class PhysicalDocumentJob(BaseModel):
    """Auditable production state for one physical ICAO eMRTD document. Sensitive data groups,
biometrics, signing keys, and connector secrets are referenced but never embedded."""

    id: str
    organization_id: str
    flow_execution_id: str
    application_id: str
    credential_template_id: str
    delivery_destination_profile_id: str
    document_type: Literal["TD1", "TD2", "TD3"]
    country_code: str | None = None
    secure_artifact_reference: str | None = None
    bureau_job_id: str | None = None
    tracking_number: str | None = None
    status: Literal["DRAFT", "DATA_GENERATED", "SOD_SIGNED", "SUBMITTED", "IN_PRODUCTION", "QUALITY_CHECK", "READY_FOR_ACTIVATION", "ACTIVE", "FAILED", "CANCELLED"]
    quality_result: dict[str, Any] | None = None
    error_code: str | None = None
    error_message: str | None = None
    submitted_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime | None = None


class PolicySet(BaseModel):
    """A named collection of Cedar policies that governs authorization decisions within the MIP
platform. PolicySets are referenced by ApplicationTemplate (approval_policy_set_id),
TrustProfile, ComplianceProfile, and the API gateway. Each PolicySet is evaluated using
deny-by-default semantics: at least one permit must match and zero forbid policies may
match."""

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


class PresentationPolicyCreateRequest(BaseModel):
    """Create a tenant-scoped Presentation Policy through the public API"""

    organization_id: str
    name: str
    description: str | None = None
    purpose: str | None = None
    display_metadata: dict[str, Any] | None = None
    required_claims: list[dict[str, Any]] | None = None
    accepted_credential_types: list[str] | None = None
    trust_profile_id: str | None = None
    credential_requirements: list[dict[str, Any]] | None = None
    alternative_requirements: list[dict[str, Any]] | None = None
    compliance_profile_id: str | None = None
    prefer_predicates: bool | None = None
    fallback_policy: Literal["REQUIRE_PREDICATE", "ACCEPT_RAW", "DENY"] | None = None
    supported_circuits: list[str] | None = None
    credential_ranking_strategy: Literal["FRESHEST_FIRST", "HIGHEST_TRUST_FIRST", "CUSTOM"] | None = None
    credential_ranking_weights: dict[str, Any] | None = None
    holder_binding: dict[str, Any] | None = None
    issuer_constraints: dict[str, Any] | None = None
    freshness: dict[str, Any] | None = None


class PresentationPolicyUpdateRequest(BaseModel):
    """Partially update a draft Presentation Policy through an explicit tenant scope"""

    organization_id: str
    name: str | None = None
    description: str | None = None
    purpose: str | None = None
    display_metadata: dict[str, Any] | None = None
    required_claims: list[dict[str, Any]] | None = None
    accepted_credential_types: list[str] | None = None
    trust_profile_id: str | None = None
    credential_requirements: list[dict[str, Any]] | None = None
    alternative_requirements: list[dict[str, Any]] | None = None
    compliance_profile_id: str | None = None
    prefer_predicates: bool | None = None
    fallback_policy: Literal["REQUIRE_PREDICATE", "ACCEPT_RAW", "DENY"] | None = None
    supported_circuits: list[str] | None = None
    credential_ranking_strategy: Literal["FRESHEST_FIRST", "HIGHEST_TRUST_FIRST", "CUSTOM"] | None = None
    credential_ranking_weights: dict[str, Any] | None = None
    holder_binding: dict[str, Any] | None = None
    issuer_constraints: dict[str, Any] | None = None
    freshness: dict[str, Any] | None = None


class PresentationPolicy(BaseModel):
    """Minimum disclosure requirements, predicates, and holder binding for credential
verification"""

    id: str
    organization_id: str
    name: str
    status: Literal["draft", "active", "suspended", "archived"]
    description: str | None = None
    purpose: str | None = None
    required_claims: list[dict[str, Any]]
    accepted_credential_types: list[str]
    display_metadata: dict[str, Any] | None = None
    credential_requirements: list[dict[str, Any]] | None = None
    alternative_requirements: list[dict[str, Any]] | None = None
    compliance_profile_id: str | None = None
    trust_profile_id: str | None = None
    holder_binding: dict[str, Any]
    freshness: dict[str, Any] | None = None
    prefer_predicates: bool
    supported_circuits: list[str]
    fallback_policy: Literal["REQUIRE_PREDICATE", "ACCEPT_RAW", "DENY"] | None = None
    issuer_constraints: dict[str, Any] | None = None
    credential_ranking_strategy: Literal["FRESHEST_FIRST", "HIGHEST_TRUST_FIRST", "CUSTOM"]
    credential_ranking_weights: dict[str, Any] | None = None
    version: int
    created_at: datetime
    updated_at: datetime


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
    status: Literal["DRAFT", "ACTIVE", "SUSPENDED"]
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


class TrustProfileIssuerCreateRequest(BaseModel):
    """Creates a trust relationship between an existing TrustProfile and IssuerEntity. Issuer
identity and lifecycle fields belong to IssuerEntity and are not accepted here."""

    issuer_id: str
    trust_level: int | None = None
    relationship_status: Literal["TRUSTED", "DENIED", "UNDER_REVIEW"] | None = None
    cascade_revocation_policy: Literal["AUTO_CASCADE", "MANUAL", "NOTIFY_ONLY"] | None = None
    metadata: dict[str, Any] | None = None


class TrustProfileIssuerUpdateRequest(BaseModel):
    """Updates trust-relationship policy only. IssuerEntity identity and lifecycle fields are
updated through the IssuerEntity API."""

    trust_level: int | None = None
    relationship_status: Literal["TRUSTED", "DENIED", "UNDER_REVIEW"] | None = None
    cascade_revocation_policy: Literal["AUTO_CASCADE", "MANUAL", "NOTIFY_ONLY"] | None = None
    metadata: dict[str, Any] | None = None


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


class TrustProfileRegistrySyncResult(BaseModel):
    """Atomic result of refreshing every configured Marty Trust Registry Sync v1 source for one
organization-owned Trust Profile."""

    trust_profile_id: str
    sources: list[dict[str, Any]]
    synchronized_at: datetime


class TrustProfile(BaseModel):
    """Cryptographic trust configuration for credential issuance and verification. Used by both
issuance flows (which issuer keys are trusted) and verification flows (which credential
issuers/roots are accepted). For org-specific framework overrides, see
OrganizationTrustProfile."""

    id: str
    organization_id: str
    name: str
    description: str | None = None
    status: TrustProfileStatus
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
    compatible_compliance_codes: list[str] | None = None
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


class VerificationCategorySummary(BaseModel):
    """Reducer-derived summary for one verification check category"""

    category: VerificationCheckCategory
    outcome: Literal["PASSED", "FAILED", "INDETERMINATE", "NOT_APPLICABLE"]
    required_check_count: int
    passed_required_count: int
    failed_required_count: int
    unresolved_required_count: int


class VerificationCheckResult(BaseModel):
    """Privacy-minimized evidence outcome for one verification check"""

    check_id: str
    category: VerificationCheckCategory
    required: bool
    outcome: VerificationCheckOutcome
    code: str
    component_id: str
    evaluated_at: datetime
    evidence_refs: list[str]


class VerificationComponentVersion(BaseModel):
    """Exact software or adapter artifact that produced verification evidence"""

    component_id: str
    version: str
    artifact_digest: str
    adapter_id: str | None = None
    adapter_version: str | None = None


class VerificationDecisionContext(BaseModel):
    """Tenant and transaction scope in which verification was authorized"""

    mode: Literal["ONLINE", "OFFLINE"]
    verifier_id: str
    organization_id: str | None = None
    transaction_id: str | None = None
    audience: str | None = None
    offline_profile_id: str | None = None


class VerificationDecisionResult(BaseModel):
    """Canonical, privacy-minimized verification decision and complete required-check evidence"""

    schema_version: str
    verification_id: str
    context: VerificationDecisionContext
    processing_status: VerificationProcessingStatus
    decision: VerificationDecision
    decision_code: Literal["ALL_REQUIRED_CHECKS_PASSED", "REQUIRED_CHECK_FAILED", "REQUIRED_CHECK_UNRESOLVED", "PROCESSING_NOT_COMPLETED"]
    valid: bool
    evaluated_at: datetime
    input_digest: str
    evidence_digest: str
    policy: VerificationProfileReference
    trust_profile: VerificationProfileReference
    reducer: VerificationReducerReference
    components: list[VerificationComponentVersion]
    checks: list[VerificationCheckResult]
    category_summaries: list[VerificationCategorySummary]


class VerificationFlowStartRequest(BaseModel):
    """Public request to start an OID4VP or SIOPv2 flow using a DID-resolved verifier profile."""

    presentation_policy_id: str | None = None
    organization_id: str
    issuer_did: str
    response_type: Literal["vp_token", "id_token"] | None = None
    trust_profile_id: str | None = None
    deployment_profile_id: str | None = None
    external_reference: str | None = None
    callback_url: str | None = None
    expiry_minutes: int | None = None
    oid4vp_profile: Literal["standard", "haip"] | None = None
    request_transport: Literal["request_uri", "request_object", "url_query"] | None = None
    request_uri_method: Literal["get", "post"] | None = None


class VerificationFlowStartResponse(BaseModel):
    """Public response for a newly started verification flow. Internal flow-definition routing
is intentionally absent."""

    instance_id: str
    request_uri: str
    qr_code_data: str
    presentation_policy_id: str
    nonce: str
    expires_at: datetime
    status: str


class VerificationProfileReference(BaseModel):
    """Versioned policy or trust profile used by a verification decision"""

    id: str
    version: str
    content_digest: str


class VerificationReducerReference(BaseModel):
    """Pure reducer contract that derived the verification decision"""

    reducer_id: str
    version: str


class VerificationResultResponse(BaseModel):
    """Public result projection for an authorized verification Flow execution."""

    instance_id: str
    status: FlowInstanceStatus
    result: str | None = None
    decision: str | None = None
    decision_reason: str | None = None
    verified_claims: dict[str, Any]
    evaluation_timestamp: datetime | None = None


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
    credential_format: Literal["MDOC", "MSO_MDOC", "SD_JWT_VC", "VC_JWT", "JSON_LD"]
    issuance_protocol: Literal["OID4VCI_PRE_AUTH", "OID4VCI_AUTH_CODE", "DIRECT"]
    compliance_profile_code: str | None = None
    wallet_apps: list[str] | None = None
    merge_strategy: Literal["APPEND", "REPLACE"] | None = None
    specifications: list[str] | None = None
    supported_platforms: list[str] | None = None
    deep_link_pattern: str | None = None
    format_variant: str | None = None
    deep_link_scheme: str | None = None
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
ActiveComplianceProfile.model_rebuild()
ApiKey.model_rebuild()
ApplicantApplication.model_rebuild()
ApplicationTemplate.model_rebuild()
BiometricEnrollment.model_rebuild()
CascadeRevocationOperation.model_rebuild()
ClaimBlocker.model_rebuild()
ComplianceProfile.model_rebuild()
CredentialRenewalOfferResponse.model_rebuild()
CredentialTemplate.model_rebuild()
DeliveryDestinationProfile.model_rebuild()
DeploymentProfile.model_rebuild()
DeviceRegistration.model_rebuild()
DidcommDeliverRequest.model_rebuild()
DidcommDeliveryResponse.model_rebuild()
EvidenceFact.model_rebuild()
FlowCreateRequest.model_rebuild()
FlowExecutionStartRequest.model_rebuild()
FlowExecution.model_rebuild()
FlowExtension.model_rebuild()
FlowUpdateRequest.model_rebuild()
Flow.model_rebuild()
HolderCredentialInventory.model_rebuild()
IssuanceRequest.model_rebuild()
IssuanceResponse.model_rebuild()
IssuanceTransaction.model_rebuild()
IssuedCredentialLifecycleRequest.model_rebuild()
IssuedCredential.model_rebuild()
IssuerEntityCreateRequest.model_rebuild()
IssuerEntityUpdateRequest.model_rebuild()
IssuerEntity.model_rebuild()
IssuerIdentityCertificateRequest.model_rebuild()
IssuerIdentityCreateRequest.model_rebuild()
IssuerIdentityCreateResponse.model_rebuild()
IssuerIdentityDeleteResponse.model_rebuild()
IssuerIdentityListResponse.model_rebuild()
IssuerIdentityOperationRequest.model_rebuild()
IssuerIdentityResolutionResponse.model_rebuild()
IssuerIdentity.model_rebuild()
KeyAttestationPolicy.model_rebuild()
Lane.model_rebuild()
MipConfigurationDiscoveryDocument.model_rebuild()
NotificationPayload.model_rebuild()
NotificationTarget.model_rebuild()
OID4VCINonceResponse.model_rebuild()
OrganizationCreateRequest.model_rebuild()
OrganizationTrustProfile.model_rebuild()
OrganizationUpdateRequest.model_rebuild()
Organization.model_rebuild()
PhysicalDocumentJob.model_rebuild()
PolicySet.model_rebuild()
PresentationPolicyCreateRequest.model_rebuild()
PresentationPolicyUpdateRequest.model_rebuild()
PresentationPolicy.model_rebuild()
ReviewerLock.model_rebuild()
RevocationBatch.model_rebuild()
RevocationProfile.model_rebuild()
MipScimRoleGroupExtension.model_rebuild()
MipScimUserExtension.model_rebuild()
Subscription.model_rebuild()
TrustFramework.model_rebuild()
TrustProfileIssuerCreateRequest.model_rebuild()
TrustProfileIssuerUpdateRequest.model_rebuild()
TrustProfileIssuer.model_rebuild()
TrustProfileRegistrySyncResult.model_rebuild()
TrustProfile.model_rebuild()
TrustRegistrySync.model_rebuild()
VerificationCategorySummary.model_rebuild()
VerificationCheckResult.model_rebuild()
VerificationComponentVersion.model_rebuild()
VerificationDecisionContext.model_rebuild()
VerificationDecisionResult.model_rebuild()
VerificationFlowStartRequest.model_rebuild()
VerificationFlowStartResponse.model_rebuild()
VerificationProfileReference.model_rebuild()
VerificationReducerReference.model_rebuild()
VerificationResultResponse.model_rebuild()
VerificationSession.model_rebuild()
VettingCheck.model_rebuild()
WalletProfile.model_rebuild()
Webhook.model_rebuild()
