//! MIP Protocol Models — generated from marty-protocol/schemas/*.json
//! Protocol version: 0.5.0
//! DO NOT EDIT — regenerate with: python scripts/codegen.py rust

use serde::{Deserialize, Serialize};

use crate::enums::*;

/// Deployment discovery projection of an active Compliance Profile and the discoverable API
/// surface it requires.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ActiveComplianceProfile {
    pub compliance_code: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_format: Option<CredentialFormat>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuance_protocol: Option<IssuanceProtocol>,
    pub api_surface: Vec<serde_json::Value>,
}

/// API key for authenticating programmatic access to the Marty gateway. Keys are either
/// ORGANIZATION-scoped (full org access within their scopes) or DEPLOYMENT-scoped
/// (restricted to a single deployment profile). The raw key value is only returned on
/// creation; subsequent reads show a masked representation. Managed via /v1/api-keys.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ApiKey {
    pub id: String,
    pub organization_id: String,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    pub key_prefix: String,
    pub scope_type: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub deployment_profile_id: Option<String>,
    pub scopes: Vec<ApiKeyScope>,
    pub enabled: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expires_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub last_used_at: Option<String>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// A holder-owned credential application created from an active ApplicationTemplate.
/// Identity, credential policy, checks, and issuer data are server-derived.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ApplicantApplication {
    pub id: String,
    pub applicant_id: String,
    pub organization_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub reference_number: Option<String>,
    pub application_template_id: String,
    pub credential_template_id: String,
    pub form_data: serde_json::Value,
    pub integration_context: serde_json::Value,
    pub status: String,
    pub claim_state: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub claim_blocker: Option<ClaimBlocker>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_display_name: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_offer_uri: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_offer_uris: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_offer_labels: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offer_expires_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub submitted_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub reviewed_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issued_at: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

/// MIP 0.3 user-facing credential application workflow with canonical form fields,
/// evidence, checks, approval policy, and lifecycle state
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ApplicationTemplate {
    pub id: String,
    pub organization_id: String,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_template_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub form_fields: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub evidence_requirements: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub claim_collection_rules: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub required_checks: Option<Vec<serde_json::Value>>,
    pub approval_strategy: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub approval_policy_set_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub application_validity_days: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub notification_config: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub ui_config: Option<serde_json::Value>,
    pub status: String,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// A record of a biometric enrollment event for an applicant. Stores only the modality,
/// hash of the biometric template, and metadata. Raw biometric data MUST NOT be stored in
/// this record and MUST NOT be transmitted via the MIP API.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BiometricEnrollment {
    pub id: String,
    pub applicant_id: String,
    pub organization_id: String,
    pub modality: String,
    pub template_hash: String,
    pub hash_algorithm: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub provider: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub capture_device: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub quality_score: Option<f64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub liveness_verified: Option<bool>,
    pub status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revoked_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_reason: Option<String>,
    pub created_at: String,
}

/// Tracks the cascade from a trust anchor or issuer revocation to dependent credentials.
/// Provides circuit-breaker protection (pauses when affected_credential_count >=
/// circuit_breaker_threshold), rollback support, and manual confirmation for high-impact
/// operations.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CascadeRevocationOperation {
    pub id: String,
    pub organization_id: String,
    pub operation_type: String,
    pub trigger_entity_type: String,
    pub trigger_entity_id: String,
    pub status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub affected_credential_count: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub affected_credential_ids: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub requires_confirmation: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub confirmed_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub confirmed_by: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub max_cascade_depth: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub current_depth: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub circuit_breaker_threshold: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub circuit_breaker_triggered: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub can_rollback: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub rollback_snapshot: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub rolled_back_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub rolled_back_by: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error_message: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub metadata: Option<serde_json::Value>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// A privacy-safe, recoverable reason that an approved application cannot yet produce a
/// credential offer.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ClaimBlocker {
    pub code: String,
    pub owner: ClaimBlockerOwner,
    pub message: String,
}

/// Abstraction of credential format complexity behind compliance-oriented identifiers
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ComplianceProfile {
    pub id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub organization_id: Option<String>,
    pub compliance_code: String,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub version: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub specification_reference: Option<String>,
    pub credential_format: CredentialFormat,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuance_protocol: Option<IssuanceProtocol>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_artifact_requirements: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub verification_policy_set_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_profile_constraints: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub api_surface: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub discoverable: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub required_claims: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub optional_claims: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub required_namespaces: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub optional_namespaces: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub required_contexts: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub supported_proof_types: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub supported_algorithms: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub key_requirements: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_methods: Option<Vec<RevocationMechanism>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_required: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub allow_skip_revocation: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_source_types: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub holder_binding_required: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub selective_disclosure_required: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub immutable: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub oid4vci_features: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub oid4vp_features: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub pex_requirements: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub physical_production: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub pki_hierarchy: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub vetting_requirements: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub conformance_tests: Option<Vec<serde_json::Value>>,
    pub status: String,
    pub is_system: bool,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// Public wallet handoff produced for an eligible issued-credential renewal.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CredentialRenewalOfferResponse {
    pub source_credential_id: String,
    pub transaction_id: String,
    pub credential_offer_uri: String,
    pub credential_offer_uris: serde_json::Value,
    pub credential_offer_labels: serde_json::Value,
    pub expires_at: String,
}

/// Public issuance configuration combining claims, compliance, issuer DID, and validity
/// rules. Custody and signing-profile metadata are resolved internally from the
/// organization and issuer DID.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CredentialTemplate {
    pub id: String,
    pub organization_id: String,
    pub name: String,
    pub credential_type: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    pub compliance_profile_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub vct: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub doctype: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_payload_format: Option<CredentialFormat>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub application_template_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_profile_id: Option<String>,
    pub claims: Vec<serde_json::Value>,
    pub validity_rules: serde_json::Value,
    pub issuer_did: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub privacy_posture: Option<serde_json::Value>,
    pub status: String,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// A delivery destination describes where an issued credential can be delivered, opened,
/// imported, or mirrored. Unlike WalletProfile, it can represent holder wallets, learner-
/// owned backpacks, organization-managed mirrors such as Canvas Credentials, or custom
/// delivery channels.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeliveryDestinationProfile {
    pub id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub organization_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub is_system: Option<bool>,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    pub provider: String,
    pub mode: String,
    pub setup_actor: String,
    pub delivery_target: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub wallet_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_format: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuance_protocol: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub compliance_profile_code: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub connector_type: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub connector_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub requires_consent: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub claim_projection_policy: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub setup_requirements: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub capabilities: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub docs_url: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub is_enabled: Option<bool>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// Runtime configuration for a physical or logical identity verification endpoint. Packages
/// trust, policies, issuance capability, network mode, user experience, and device grouping
/// via Lanes.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeploymentProfile {
    pub id: String,
    pub organization_id: String,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    pub trust_profile_id: String,
    pub presentation_policy_ids: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_template_ids: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub default_policy_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub site_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub enabled_flow_ids: Option<Vec<String>>,
    pub network_mode: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub key_access_mode: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub environment_config: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub update_channel: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub update_policy: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offline_cache_ttl_hours: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub operator_biometric_authentication_required: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub biometric_required: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub audit_all_events: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub lanes: Option<Vec<Lane>>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// User device record for push notification delivery and challenge-response authentication
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeviceRegistration {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub id: Option<String>,
    pub user_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub organization_id: Option<String>,
    pub device_id: String,
    pub platform: String,
    pub fcm_token: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub app_version: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub os_version: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub device_model: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub preferences: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub public_key_der: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub public_key_kid: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub key_version: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub key_valid_from: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub key_valid_until: Option<String>,
    pub is_active: bool,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub last_seen_at: Option<String>,
}

/// Tenant-scoped request to deliver an already-authorized issuance transaction over
/// encrypted DIDComm v2
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DidcommDeliverRequest {
    pub organization_id: String,
    pub transaction_id: String,
    pub holder_did: String,
}

/// Result of encrypted DIDComm v2 credential delivery
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DidcommDeliveryResponse {
    pub transaction_id: String,
    pub credential_id: String,
    pub holder_did: String,
    pub service_endpoint: String,
    pub didcomm_message_id: String,
    pub status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<String>,
}

/// Immutable normalized fact derived from verified evidence. Provider adapters create
/// EvidenceFacts from receipts so approval policy can evaluate facts without parsing
/// provider payloads.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EvidenceFact {
    pub id: String,
    pub organization_id: String,
    pub application_id: String,
    pub subject_id: String,
    pub provider: String,
    pub fact_type: String,
    pub scope: serde_json::Value,
    pub assertion: serde_json::Value,
    pub verification: serde_json::Value,
    pub source: serde_json::Value,
    pub created_at: String,
}

/// Create a tenant-scoped orchestration definition through the public API.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FlowCreateRequest {
    pub organization_id: String,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    pub flow_type: FlowType,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_template_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub application_template_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub presentation_policy_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub delivery_destination_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub deployment_profile_ids: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub approval_strategy: Option<ApprovalStrategy>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub hooks: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trigger: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub extension: Option<serde_json::Value>,
}

/// Start an authorized Flow execution in an explicitly selected organization.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FlowExecutionStartRequest {
    pub organization_id: String,
    pub flow_definition_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub subject_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub subject_type: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub external_reference: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub initial_context: Option<serde_json::Value>,
}

/// Public, tenant-scoped projection of a single Flow execution. Internal custody selectors,
/// bearer credentials, pre-authorized codes, and service state are never part of this
/// representation.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FlowExecution {
    pub id: String,
    pub flow_id: Option<String>,
    pub flow_type: Option<FlowType>,
    pub organization_id: String,
    pub status: FlowInstanceStatus,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub current_step: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub current_step_index: Option<i64>,
    pub step_results: serde_json::Value,
    pub context_data: serde_json::Value,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issued_credential_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub started_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub completed_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expires_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error_code: Option<String>,
    pub metadata: serde_json::Value,
    pub state_history: Vec<serde_json::Value>,
    pub created_at: String,
    pub updated_at: String,
}

/// Versioned non-standard orchestration envelope. A custom Flow uses this object so it
/// cannot claim the conformance semantics of a standard FlowType.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FlowExtension {
    pub extension_uri: String,
    pub extension_version: String,
    pub extends_flow_type: serde_json::Value,
    pub entry_step_id: String,
    pub steps: Vec<serde_json::Value>,
    pub transitions: Vec<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub config: Option<serde_json::Value>,
}

/// Patch a tenant-scoped Flow. The service validates the complete merged definition before
/// persisting it.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FlowUpdateRequest {
    pub organization_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub name: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub flow_type: Option<FlowType>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_template_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub application_template_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub presentation_policy_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub delivery_destination_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub deployment_profile_ids: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub approval_strategy: Option<ApprovalStrategy>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub hooks: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trigger: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub extension: Option<serde_json::Value>,
}

/// End-to-end identity lifecycle orchestration. Standard FlowTypes have fixed protocol
/// sequences; non-standard graphs use flow_type custom with a versioned extension envelope.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Flow {
    pub id: String,
    pub organization_id: String,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    pub flow_type: FlowType,
    pub flow_category: String,
    pub resolved_steps: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_template_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub application_template_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub presentation_policy_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub delivery_destination_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub deployment_profile_ids: Option<Vec<String>>,
    pub approval_strategy: ApprovalStrategy,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub hooks: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trigger: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub extension: Option<FlowExtension>,
    pub status: String,
    pub version: i64,
    pub created_at: String,
    pub updated_at: String,
}

/// Privacy-filtered response from GET /v1/issued-credentials/mine. Credential material,
/// claims, hashes, signing references, and opaque subject identifiers are prohibited.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HolderCredentialInventory {
    pub items: Vec<serde_json::Value>,
    pub total: i64,
    pub limit: i64,
    pub offset: i64,
}

/// Public request to create a credential issuance. Custody and issuer-profile selectors are
/// intentionally absent.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuanceRequest {
    pub organization_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_template_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_did: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub subject_did: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub holder_did: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub authorized_client: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub application_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub claims: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_subject: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_document: Option<serde_json::Value>,
}

/// Public result of initiating credential issuance. The offer URI is the wallet handoff;
/// the underlying pre-authorized code is never returned as a separate management API field.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuanceResponse {
    pub id: String,
    pub organization_id: String,
    pub credential_template_id: String,
    pub status: String,
    pub credential_offer_uri: String,
    pub credential_offer_uris: serde_json::Value,
    pub credential_offer_labels: serde_json::Value,
    pub expires_at: String,
}

/// Public management projection of a tenant-scoped credential issuance transaction. OAuth
/// tokens, pre-authorized codes, custody selectors, signing-service identifiers, keys, and
/// raw credential payloads are excluded.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuanceTransaction {
    pub id: String,
    pub organization_id: String,
    pub credential_template_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub applicant_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub application_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub subject_did: Option<String>,
    pub status: String,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expires_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issued_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revoked_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_reason: Option<String>,
}

/// Reason supplied for a tenant-bound issued-credential lifecycle transition.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuedCredentialLifecycleRequest {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub reason: Option<String>,
}

/// Lifecycle record for an issued credential. Stores metadata without raw credential data
/// (only a SHA-256 hash for integrity). Links FlowExecution to credential status, status
/// list entries, and revocation history.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuedCredential {
    pub id: String,
    pub organization_id: String,
    pub credential_id: String,
    pub credential_type: String,
    pub credential_format: String,
    pub flow_execution_id: String,
    pub credential_template_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub application_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub renewed_from_credential_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub renewed_to_credential_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub renewable: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub renewal_eligible_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub can_renew: Option<bool>,
    pub subject_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_did: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub subject_claims_hash: Option<String>,
    pub issued_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub valid_from: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub valid_until: Option<String>,
    pub status: String,
    pub status_list_entries: Vec<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_hash: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revoked_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_reason: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revoked_by: Option<String>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// Create an organization-scoped issuer trust-registry record. Global/system issuers are
/// managed outside this public operation.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuerEntityCreateRequest {
    pub organization_id: String,
    pub issuer_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_type: Option<String>,
    pub display_name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub compliance_status: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub accreditation_body: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub accreditations: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub accreditation_date: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub valid_from: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub valid_until: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_anchor_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub metadata: Option<serde_json::Value>,
}

/// Partially update an organization-scoped issuer trust-registry record. organization_id
/// binds the mutation to its tenant.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuerEntityUpdateRequest {
    pub organization_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub display_name: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_type: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub compliance_status: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub accreditation_body: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub accreditations: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub accreditation_date: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub valid_from: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub valid_until: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_anchor_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub metadata: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_reason: Option<String>,
}

/// An organisation or authority that issues credentials. Separate from Trust Anchors
/// (cryptographic roots). An issuer may be backed by one or more trust anchors. Supports
/// full lifecycle: accreditation, suspension, and revocation.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuerEntity {
    pub id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub organization_id: Option<String>,
    pub issuer_id: String,
    pub issuer_type: String,
    pub display_name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    pub is_system_issuer: bool,
    pub compliance_status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub accreditation_body: Option<String>,
    pub accreditations: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub accreditation_date: Option<String>,
    pub valid_from: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub valid_until: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_anchor_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revoked_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_reason: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revoked_by: Option<String>,
    pub metadata: serde_json::Value,
    pub created_at: String,
    pub updated_at: String,
}

/// Attach a public X.509 certificate chain to exactly one DID-selected issuer identity. The
/// leaf public key must match the DID identity's managed key.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuerIdentityCertificateRequest {
    pub organization_id: String,
    pub issuer_did: String,
    pub key_purpose: String,
    pub credential_format: CredentialFormat,
    pub algorithm: String,
    pub cert_pem: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cert_chain_pem: Option<String>,
}

/// Provision or adopt a tenant-scoped issuer DID using implementation-managed custody. The
/// implementation selects the signing service and key; callers cannot provide custody
/// coordinates.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuerIdentityCreateRequest {
    pub organization_id: String,
    pub issuer_did: String,
    pub key_purpose: String,
    pub credential_format: CredentialFormat,
    pub algorithm: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub key_attestation_policy: Option<KeyAttestationPolicy>,
}

/// Provider-neutral result of ensuring a DID issuer identity.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuerIdentityCreateResponse {
    pub identity: IssuerIdentity,
    pub created: bool,
}

/// Provider-neutral result of retiring a DID issuer identity.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuerIdentityDeleteResponse {
    pub deleted: IssuerIdentity,
}

/// Public issuer identities available in the authenticated organization scope.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuerIdentityListResponse {
    pub identities: Vec<IssuerIdentity>,
}

/// Select exactly one tenant issuer identity for a lifecycle operation without exposing its
/// private issuer profile or custody binding.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuerIdentityOperationRequest {
    pub organization_id: String,
    pub issuer_did: String,
    pub key_purpose: String,
    pub credential_format: CredentialFormat,
    pub algorithm: String,
}

/// Public material resolved for exactly one DID identity tuple. The response never exposes
/// or accepts a verification-method, profile, service, key-reference, provider, or KMS
/// selector.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuerIdentityResolutionResponse {
    pub identity: IssuerIdentity,
    pub public_jwk: serde_json::Value,
}

/// A tenant-scoped public DID projection that callers may select for issuance or signed
/// verification. Custody coordinates and internal issuer-profile IDs are never part of this
/// resource.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuerIdentity {
    pub issuer_did: String,
    pub key_purpose: String,
    pub credential_format: CredentialFormat,
    pub algorithm: String,
    pub status: String,
}

/// Provider-neutral trust policy for holder-key attestations presented during issuance. It
/// contains public trust material and validation requirements, never issuer custody
/// coordinates.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KeyAttestationPolicy {
    pub mode: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trusted_root_certificates_pem: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub allowed_algorithms: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub required_key_storage: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub required_user_authentication: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub max_age_seconds: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub require_nonce: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub status_validation: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub status_list_allowed_origins: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub status_list_trusted_root_certificates_pem: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub status_list_allowed_algorithms: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub status_list_max_age_seconds: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub status_list_allow_private_hosts: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub status_list_tls_ca_certificates_pem: Option<Vec<String>>,
}

/// Logical device grouping within a Deployment Profile
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Lane {
    pub id: String,
    pub name: String,
    pub deployment_profile_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub default_policy_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub device_ids: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub metadata: Option<serde_json::Value>,
}

/// Schema for the /.well-known/mip-configuration endpoint response. This document describes
/// the capabilities, endpoints, and supported profiles of a MIP implementation. Analogous
/// to OpenID Connect Discovery (RFC 8414) but scoped to MIP-specific capabilities.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MipConfigurationDiscoveryDocument {
    pub mip_version: String,
    pub issuer: String,
    pub mip_configuration_endpoint: String,
    pub supported_versions: Vec<String>,
    pub implementation_classes: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuance_endpoint: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub openid_credential_issuer: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub presentation_endpoint: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub token_endpoint: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub authorization_endpoint: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub supported_credential_formats: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub supported_compliance_profiles: Option<Vec<String>>,
    pub active_compliance_profiles: Vec<ActiveComplianceProfile>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub supported_flow_types: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub supported_signing_algorithms: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub proximity_supported: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub proximity_engagement_methods: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub scim_endpoint: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_endpoint: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub jwks_uri: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub org_endpoints: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub service_documentation: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub policy_uri: Option<String>,
}

/// Message content and routing metadata for multi-channel identity event notification
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NotificationPayload {
    pub id: String,
    pub title: String,
    pub body: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub data: Option<serde_json::Value>,
    pub event_type: String,
    pub priority: String,
    pub target: NotificationTarget,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub ttl_seconds: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub collapse_key: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub correlation_id: Option<String>,
    pub created_at: String,
}

/// Multi-channel message delivery targeting configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NotificationTarget {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub organization_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub user_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub device_tokens: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub webhook_endpoints: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub email_addresses: Option<Vec<String>>,
    pub channels: Vec<String>,
}

/// Response from the OID4VCI 1.0 Final Nonce Endpoint. The HTTP response must also include
/// Cache-Control: no-store.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OID4VCINonceResponse {
    pub c_nonce: String,
}

/// Create an Organization through the public API. Discovery and admission settings are
/// explicit and persisted.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OrganizationCreateRequest {
    pub name: String,
    pub display_name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub org_type: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub contact_email: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub visibility: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub join_mechanism: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub requires_approval: Option<bool>,
}

/// Organisation-specific overlay of a TrustFramework. Separates shared framework
/// definitions from per-org policy overrides, issuer allow/deny lists, and jurisdiction
/// filters.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OrganizationTrustProfile {
    pub id: String,
    pub organization_id: String,
    pub framework_id: String,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub display_name: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub enabled: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub use_case_tags: Option<Vec<String>>,
    pub compliance_status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub auto_generated: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_policy: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub time_policy: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub allowed_algorithms: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub allowed_formats: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub allowed_issuers: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub denied_issuers: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub jurisdiction_filter: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub metadata: Option<serde_json::Value>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// Partially update an Organization through the public API. organization_id is required to
/// bind the mutation to its tenant.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OrganizationUpdateRequest {
    pub organization_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub name: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub display_name: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub org_type: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub contact_email: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub contact_phone: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub website: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub visibility: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub join_mechanism: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub requires_approval: Option<bool>,
}

/// The primary multi-tenant boundary in MIP. All configuration resources are scoped to an
/// organization.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Organization {
    pub id: String,
    pub name: String,
    pub display_name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub join_code: Option<String>,
    pub visibility: String,
    pub owner_id: String,
    pub status: String,
    pub org_type: String,
    pub join_mechanism: String,
    pub requires_approval: bool,
    pub is_discoverable: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub contact_email: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub contact_phone: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub website: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub membership: Option<serde_json::Value>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// Auditable production state for one physical ICAO eMRTD document. Sensitive data groups,
/// biometrics, signing keys, and connector secrets are referenced but never embedded.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PhysicalDocumentJob {
    pub id: String,
    pub organization_id: String,
    pub flow_execution_id: String,
    pub application_id: String,
    pub credential_template_id: String,
    pub delivery_destination_profile_id: String,
    pub document_type: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub country_code: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub secure_artifact_reference: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub bureau_job_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub tracking_number: Option<String>,
    pub status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub quality_result: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error_code: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error_message: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub submitted_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub completed_at: Option<String>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// A named collection of Cedar policies that governs authorization decisions within the MIP
/// platform. PolicySets are referenced by ApplicationTemplate (approval_policy_set_id),
/// TrustProfile, ComplianceProfile, and the API gateway. Each PolicySet is evaluated using
/// deny-by-default semantics: at least one permit must match and zero forbid policies may
/// match.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PolicySet {
    pub id: String,
    pub organization_id: String,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    pub policy_type: String,
    pub cedar_policies: Vec<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cedar_schema_version: Option<String>,
    pub status: String,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// Create a tenant-scoped Presentation Policy through the public API
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PresentationPolicyCreateRequest {
    pub organization_id: String,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub purpose: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub display_metadata: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub required_claims: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub accepted_credential_types: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_requirements: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub alternative_requirements: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub compliance_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub prefer_predicates: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub fallback_policy: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub supported_circuits: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_ranking_strategy: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_ranking_weights: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub holder_binding: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_constraints: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub freshness: Option<serde_json::Value>,
}

/// Partially update a draft Presentation Policy through an explicit tenant scope
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PresentationPolicyUpdateRequest {
    pub organization_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub name: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub purpose: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub display_metadata: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub required_claims: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub accepted_credential_types: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_requirements: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub alternative_requirements: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub compliance_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub prefer_predicates: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub fallback_policy: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub supported_circuits: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_ranking_strategy: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_ranking_weights: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub holder_binding: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_constraints: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub freshness: Option<serde_json::Value>,
}

/// Minimum disclosure requirements, predicates, and holder binding for credential
/// verification
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PresentationPolicy {
    pub id: String,
    pub organization_id: String,
    pub name: String,
    pub status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub purpose: Option<String>,
    pub required_claims: Vec<serde_json::Value>,
    pub accepted_credential_types: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub display_metadata: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_requirements: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub alternative_requirements: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub compliance_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_profile_id: Option<String>,
    pub holder_binding: serde_json::Value,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub freshness: Option<serde_json::Value>,
    pub prefer_predicates: bool,
    pub supported_circuits: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub fallback_policy: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_constraints: Option<serde_json::Value>,
    pub credential_ranking_strategy: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_ranking_weights: Option<serde_json::Value>,
    pub version: i64,
    pub created_at: String,
    pub updated_at: String,
}

/// A time-bounded exclusive lock that prevents two reviewers from acting on the same
/// applicant simultaneously. A lock MUST be acquired before transitioning an applicant out
/// of SUBMITTED or UNDER_REVIEW. Locks expire automatically; the default TTL is 1800
/// seconds (30 minutes).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReviewerLock {
    pub id: String,
    pub applicant_id: String,
    pub organization_id: String,
    pub holder_user_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub ttl_seconds: Option<i64>,
    pub expires_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub released_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub status: Option<String>,
    pub created_at: String,
}

/// Privacy-preserving batched revocation. Instead of publishing status list updates
/// immediately (which enables timing-correlation attacks), the system batches revocations
/// and publishes at configurable intervals. Interval options: 1h, 6h, 24h.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RevocationBatch {
    pub id: String,
    pub organization_id: String,
    pub credential_format: String,
    pub batch_interval: String,
    pub status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub pending_credential_ids: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub published_credential_count: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub status_list_uri: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub scheduled_publish_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub published_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error_message: Option<String>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// Format-agnostic revocation configuration for issuers and verifiers
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RevocationProfile {
    pub id: String,
    pub organization_id: String,
    pub name: String,
    pub status: String,
    pub revocation_mechanism: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub mechanism_priority: Option<Vec<String>>,
    pub check_mode: RevocationTimingMode,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cache_ttl_seconds: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offline_grace_seconds: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_config: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub status_list_url: Option<String>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// MIP extension attributes for SCIM 2.0 Group resources representing roles. Schema URI:
/// urn:mip:scim:schemas:extension:Organization:2.0:Role
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MipScimRoleGroupExtension {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub permissions: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub policy_set_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub is_system_role: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
}

/// MIP extension attributes for SCIM 2.0 User resources. Schema URI:
/// urn:mip:scim:schemas:extension:Organization:2.0:User
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MipScimUserExtension {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub role_ids: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub is_owner: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub joined_at: Option<String>,
}

/// Event subscription that routes identity lifecycle events to a configured delivery target
/// (webhook, email, or SSE channel). Managed via /v1/subscriptions.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Subscription {
    pub id: String,
    pub organization_id: String,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    pub event_types: Vec<String>,
    pub delivery: serde_json::Value,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub filter: Option<serde_json::Value>,
    pub enabled: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub retry_policy: Option<serde_json::Value>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// System-managed trust framework definition for ICAO, AAMVA, EUDI, or custom identity
/// ecosystems. Immutable at the system level; organisations reference frameworks via
/// OrganizationTrustProfile.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrustFramework {
    pub id: String,
    pub code: String,
    pub display_name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub pkd_endpoints: Option<serde_json::Value>,
    pub default_algorithms: Vec<String>,
    pub default_formats: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub validation_ruleset: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub sync_config: Option<serde_json::Value>,
    pub is_system: bool,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// Creates a trust relationship between an existing TrustProfile and IssuerEntity. Issuer
/// identity and lifecycle fields belong to IssuerEntity and are not accepted here.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrustProfileIssuerCreateRequest {
    pub issuer_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_level: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub relationship_status: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cascade_revocation_policy: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub metadata: Option<serde_json::Value>,
}

/// Updates trust-relationship policy only. IssuerEntity identity and lifecycle fields are
/// updated through the IssuerEntity API.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrustProfileIssuerUpdateRequest {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_level: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub relationship_status: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cascade_revocation_policy: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub metadata: Option<serde_json::Value>,
}

/// Join entity between TrustProfile and IssuerEntity with trust scoring and cascade
/// revocation policy. trust_level is a 0–100 score; future versions will auto-adjust based
/// on issuer history (failed validations, revocation events, compliance lapses).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrustProfileIssuer {
    pub id: String,
    pub trust_profile_id: String,
    pub issuer_id: String,
    pub trust_level: i64,
    pub relationship_status: String,
    pub cascade_revocation_policy: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub metadata: Option<serde_json::Value>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// Atomic result of refreshing every configured Marty Trust Registry Sync v1 source for one
/// organization-owned Trust Profile.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrustProfileRegistrySyncResult {
    pub trust_profile_id: String,
    pub sources: Vec<serde_json::Value>,
    pub synchronized_at: String,
}

/// Cryptographic trust configuration for credential issuance and verification. Used by both
/// issuance flows (which issuer keys are trusted) and verification flows (which credential
/// issuers/roots are accepted). For org-specific framework overrides, see
/// OrganizationTrustProfile.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrustProfile {
    pub id: String,
    pub organization_id: String,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    pub status: TrustProfileStatus,
    pub profile_type: String,
    pub trust_sources: Vec<serde_json::Value>,
    pub allowed_algorithms: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_policy: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_services: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub time_policy: Option<serde_json::Value>,
    pub supported_formats: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub allowed_issuers: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub denied_issuers: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub system_issuer_overrides: Option<serde_json::Value>,
    pub compliance_status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub verification_policy_set_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub compatible_compliance_codes: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub auto_generated: Option<bool>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// Delta-sync resource for mobile wallet trust registry updates. Provides CSCA/DSC anchor
/// data from the /v1/trust-registry endpoints so wallets can sync incrementally rather than
/// downloading the full trust store on every launch.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrustRegistrySync {
    pub sync_token: String,
    pub sequence: i64,
    pub entries: Vec<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub has_more: Option<bool>,
    pub generated_at: String,
}

/// Reducer-derived summary for one verification check category
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VerificationCategorySummary {
    pub category: VerificationCheckCategory,
    pub outcome: String,
    pub required_check_count: i64,
    pub passed_required_count: i64,
    pub failed_required_count: i64,
    pub unresolved_required_count: i64,
}

/// Privacy-minimized evidence outcome for one verification check
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VerificationCheckResult {
    pub check_id: String,
    pub category: VerificationCheckCategory,
    pub required: bool,
    pub outcome: VerificationCheckOutcome,
    pub code: String,
    pub component_id: String,
    pub evaluated_at: String,
    pub evidence_refs: Vec<String>,
}

/// Exact software or adapter artifact that produced verification evidence
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VerificationComponentVersion {
    pub component_id: String,
    pub version: String,
    pub artifact_digest: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub adapter_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub adapter_version: Option<String>,
}

/// Tenant and transaction scope in which verification was authorized
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VerificationDecisionContext {
    pub mode: String,
    pub verifier_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub organization_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub transaction_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub audience: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offline_profile_id: Option<String>,
}

/// Canonical, privacy-minimized verification decision and complete required-check evidence
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VerificationDecisionResult {
    pub schema_version: String,
    pub verification_id: String,
    pub context: VerificationDecisionContext,
    pub processing_status: VerificationProcessingStatus,
    pub decision: VerificationDecision,
    pub decision_code: String,
    pub valid: bool,
    pub evaluated_at: String,
    pub input_digest: String,
    pub evidence_digest: String,
    pub policy: VerificationProfileReference,
    pub trust_profile: VerificationProfileReference,
    pub reducer: VerificationReducerReference,
    pub components: Vec<VerificationComponentVersion>,
    pub checks: Vec<VerificationCheckResult>,
    pub category_summaries: Vec<VerificationCategorySummary>,
}

/// Public request to start an OID4VP or SIOPv2 flow using a DID-resolved verifier profile.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VerificationFlowStartRequest {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub presentation_policy_id: Option<String>,
    pub organization_id: String,
    pub issuer_did: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub response_type: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub deployment_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub external_reference: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub callback_url: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expiry_minutes: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub oid4vp_profile: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub request_transport: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub request_uri_method: Option<String>,
}

/// Public response for a newly started verification flow. Internal flow-definition routing
/// is intentionally absent.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VerificationFlowStartResponse {
    pub instance_id: String,
    pub request_uri: String,
    pub qr_code_data: String,
    pub presentation_policy_id: String,
    pub nonce: String,
    pub expires_at: String,
    pub status: String,
}

/// Versioned policy or trust profile used by a verification decision
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VerificationProfileReference {
    pub id: String,
    pub version: String,
    pub content_digest: String,
}

/// Pure reducer contract that derived the verification decision
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VerificationReducerReference {
    pub reducer_id: String,
    pub version: String,
}

/// Public result projection for an authorized verification Flow execution.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VerificationResultResponse {
    pub instance_id: String,
    pub status: FlowInstanceStatus,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub result: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub decision: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub decision_reason: Option<String>,
    pub verified_claims: serde_json::Value,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub evaluation_timestamp: Option<String>,
}

/// A single presentation-request/response cycle instance
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VerificationSession {
    pub id: String,
    pub flow_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub flow_instance_id: Option<String>,
    pub presentation_policy_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub deployment_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub verifier_nonce: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub holder_id: Option<String>,
    pub status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub result: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expires_at: Option<String>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub completed_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<String>,
}

/// A discrete identity or document verification check performed as part of the applicant
/// review process. Each check corresponds to a single automated or manual verification
/// step.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VettingCheck {
    pub id: String,
    pub applicant_id: String,
    pub organization_id: String,
    pub check_type: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub provider: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub provider_reference_id: Option<String>,
    pub status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub score: Option<f64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub threshold: Option<f64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub failure_reason: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub evidence_refs: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub performed_by: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub started_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub completed_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expires_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub raw_result: Option<serde_json::Value>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// Wallet compatibility record for a credential format × protocol × compliance combination.
/// The canonical wallet profile set is auto-derived from CredentialTemplate configuration
/// via the derivation key (credential_format, issuance_protocol, compliance_profile_code).
/// Organizations MAY store override entries at /v1/wallet-registry to extend or customise
/// the derived profile for their specific deployment. GET /v1/wallet-registry returns
/// merged results: derived profiles supplemented (or overridden) by stored entries.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WalletProfile {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub organization_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub is_override: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub override_precedence: Option<i64>,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    pub credential_format: String,
    pub issuance_protocol: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub compliance_profile_code: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub wallet_apps: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub merge_strategy: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub specifications: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub supported_platforms: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub deep_link_pattern: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub format_variant: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub deep_link_scheme: Option<String>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// A persistent webhook subscription that delivers signed HTTP POST callbacks to an
/// operator-controlled endpoint when specified identity lifecycle events occur. Managed via
/// /v1/organizations/{org_id}/webhooks.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Webhook {
    pub id: String,
    pub organization_id: String,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    pub endpoint_url: String,
    pub events: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub signing_secret: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub signing_secret_masked: Option<String>,
    pub enabled: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub api_version: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub filter: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub delivery_config: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub status: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub failure_count: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub last_triggered_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub last_success_at: Option<String>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}
