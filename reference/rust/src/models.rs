//! MIP Protocol Models — generated from marty-protocol/schemas/*.json
//! Generated: 2026-05-11
//! DO NOT EDIT — regenerate with: python scripts/codegen.py rust

use serde::{Deserialize, Serialize};

use crate::enums::*;

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

/// A person or entity that has applied for a credential through an application-approval
/// flow. Applicants are a first-class entity with a lifecycle that terminates in credential
/// issuance, rejection, or withdrawal.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Applicant {
    pub id: String,
    pub organization_id: String,
    pub flow_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_template_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub user_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub external_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub given_name: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub family_name: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub email: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub phone: Option<String>,
    pub status: ApplicantStatus,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub reviewer_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub reviewer_lock_expires_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub submitted_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub reviewed_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub approved_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credentialed_at: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub rejection_reason: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub rejection_code: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub application_data: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub vetting_checks: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issued_credential_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub metadata: Option<serde_json::Value>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// User-facing credential application workflow with form fields, evidence, and approval
/// config
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ApplicationTemplate {
    pub id: String,
    pub organization_id: String,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub form_fields: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub evidence_requirements: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub claim_collection_rules: Option<Vec<serde_json::Value>>,
    pub approval_strategy: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub approval_rules: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub approval_policy_set_id: Option<String>,
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
    pub credential_format: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuance_protocol: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_artifact_requirements: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub default_verification_rules: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub verification_policy_set_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_profile_constraints: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub api_surface: Option<Vec<serde_json::Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub discoverable: Option<bool>,
    pub is_system: bool,
    pub created_at: String,
}

/// Master issuance configuration combining schema, compliance profile, and cryptographic
/// materials
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
    pub credential_payload_format: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub application_template_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_profile_id: Option<String>,
    pub claims: Vec<serde_json::Value>,
    pub validity_rules: serde_json::Value,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_key_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_algorithm: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub key_access_mode: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_certificate_chain_pem: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_did: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_identity: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub remote_signing_config: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub auto_generate_artifacts: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub privacy_posture: Option<serde_json::Value>,
    pub status: String,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// Runtime configuration for a physical or logical identity verification endpoint. Packages
/// trust, policies, issuance capability, network mode, UX, and device grouping via Lanes.
/// Compatibility extensions may additionally expose rollout and operational fields.
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
    #[serde(skip_serializing_if = "Option::is_none")]
    pub default_presentation_policy_id: Option<String>,
    pub network_mode: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub key_access_mode: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub environment_config: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub ux_config: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub update_channel: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub update_policy: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offline_cache_ttl_hours: Option<i64>,
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

/// Runtime state of a single flow instance. Tracks current step, step results, context
/// data, and lifecycle transitions. Created when a flow is initiated; updated as steps
/// complete.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FlowExecution {
    pub id: String,
    pub flow_id: String,
    pub flow_type: FlowType,
    pub organization_id: String,
    pub status: FlowInstanceStatus,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub current_step: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub current_step_index: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub step_results: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub context_data: Option<serde_json::Value>,
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
    #[serde(skip_serializing_if = "Option::is_none")]
    pub metadata: Option<serde_json::Value>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// End-to-end identity lifecycle orchestration. Each flow_type maps to a fixed protocol
/// step sequence defined by OID4VCI, OID4VP, mDL ISO 18013-5, or application-approval
/// workflows.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Flow {
    pub id: String,
    pub organization_id: String,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    pub flow_type: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub flow_category: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_template_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub application_template_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub presentation_policy_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub deployment_profile_ids: Option<Vec<String>>,
    pub approval_strategy: ApprovalStrategy,
    pub enabled: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub hooks: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trigger: Option<serde_json::Value>,
    pub status: String,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// Record of a credential issuance event
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuanceRecord {
    pub id: String,
    pub flow_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub flow_execution_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub application_id: Option<String>,
    pub credential_template_id: String,
    pub holder_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_format: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offer_uri: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offer_expires_at: Option<String>,
    pub status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_index: Option<i64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub valid_from: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub valid_until: Option<String>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub claimed_at: Option<String>,
}

/// Lifecycle record for an issued credential. Stores metadata without raw credential data
/// (only a SHA-256 hash for integrity). Links FlowExecution to credential status, status
/// list entries, and revocation history.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IssuedCredential {
    pub id: String,
    pub credential_id: String,
    pub credential_type: String,
    pub credential_format: String,
    pub flow_execution_id: String,
    pub credential_template_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub application_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revocation_profile_id: Option<String>,
    pub subject_id: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub subject_claims_hash: Option<String>,
    pub issued_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub valid_from: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub valid_until: Option<String>,
    pub status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub status_list_entries: Option<Vec<serde_json::Value>>,
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
    #[serde(skip_serializing_if = "Option::is_none")]
    pub is_system_issuer: Option<bool>,
    pub compliance_status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub accreditation_body: Option<String>,
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
    #[serde(skip_serializing_if = "Option::is_none")]
    pub metadata: Option<serde_json::Value>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
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
    #[serde(skip_serializing_if = "Option::is_none")]
    pub supported_versions: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub implementation_classes: Option<Vec<String>>,
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
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
}

/// A named collection of Cedar policies that governs authorization decisions within the MIP
/// platform. PolicySets are referenced by ApplicationTemplate (approval_rules),
/// TrustProfile (issuer trust), ComplianceProfile (verification rules), and the API gateway
/// (access control). Each PolicySet contains one or more Cedar policy statements evaluated
/// using deny-by-default semantics: at least one permit must match and zero forbid policies
/// may match for the request to be authorized.
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

/// Minimum disclosure requirements, predicates, and holder binding for credential
/// verification
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PresentationPolicy {
    pub id: String,
    pub organization_id: String,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub purpose: Option<String>,
    pub required_claims: Vec<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub accepted_credential_types: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_profile_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub holder_binding: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub freshness: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub prefer_predicates: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub supported_circuits: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub fallback_policy: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub issuer_constraints: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_ranking_strategy: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub credential_ranking_weights: Option<serde_json::Value>,
    pub created_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub updated_at: Option<String>,
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

/// Join entity between TrustProfile and IssuerEntity with trust scoring and cascade
/// revocation policy. trust_level is a 0â€“100 score; future versions will auto-adjust
/// based on issuer history (failed validations, revocation events, compliance lapses).
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

/// Wallet compatibility record for a credential format Ã— protocol Ã— compliance
/// combination. The canonical wallet profile set is auto-derived from CredentialTemplate
/// configuration via the derivation key (credential_format, issuance_protocol,
/// compliance_profile_code). Organizations MAY store override entries at /v1/wallet-
/// registry to extend or customise the derived profile for their specific deployment. GET
/// /v1/wallet-registry returns merged results: derived profiles supplemented (or
/// overridden) by stored entries.
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

