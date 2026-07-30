// MIP Protocol Models — generated from marty-protocol/schemas/*.json
// Protocol version: 0.3.1
// DO NOT EDIT — regenerate with: python scripts/codegen.py typescript

import {
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
  TrustSourceType,
  ValidationAlgorithm,
  ZkCircuitSystem,
} from './enums';

/** Deployment discovery projection of an active Compliance Profile and the discoverable API surface it requires. */
export interface ActiveComplianceProfile {
  compliance_code: string;
  credential_format?: CredentialFormat;
  issuance_protocol?: IssuanceProtocol;
  api_surface: Record<string, unknown>[];
}

/** API key for authenticating programmatic access to the Marty gateway. Keys are either ORGANIZATION-scoped (full org access within their scopes) or DEPLOYMENT-scoped (restricted to a single deployment profile). The raw key value is only returned on creation; subsequent reads show a masked representation. Managed via /v1/api-keys. */
export interface ApiKey {
  id: string;
  organization_id: string;
  name: string;
  description?: string;
  key_prefix: string;
  scope_type: 'ORGANIZATION' | 'DEPLOYMENT';
  deployment_profile_id?: string | null;
  scopes: ApiKeyScope[];
  enabled: boolean;
  expires_at?: string | null;
  last_used_at?: string | null;
  created_at: string;
  updated_at?: string;
}

/** A holder-owned credential application created from an active ApplicationTemplate. Identity, credential policy, checks, and issuer data are server-derived. */
export interface ApplicantApplication {
  id: string;
  applicant_id: string;
  organization_id: string;
  reference_number?: string | null;
  application_template_id: string;
  credential_template_id: string;
  form_data: Record<string, unknown>;
  integration_context: Record<string, unknown>;
  status: 'DRAFT' | 'SUBMITTED' | 'UNDER_REVIEW' | 'PENDING_INFORMATION' | 'APPROVED' | 'REJECTED' | 'WITHDRAWN' | 'OFFERED' | 'CREDENTIALED' | 'SUSPENDED';
  claim_state: 'NOT_READY' | 'BLOCKED' | 'OFFER_READY' | 'CLAIMED' | 'EXPIRED';
  claim_blocker?: ClaimBlocker | null;
  credential_display_name?: string | null;
  credential_offer_uri?: string | null;
  credential_offer_uris?: Record<string, unknown>;
  credential_offer_labels?: Record<string, unknown>;
  offer_expires_at?: string | null;
  submitted_at?: string | null;
  reviewed_at?: string | null;
  issued_at?: string | null;
  created_at: string;
  updated_at: string;
}

/** MIP 0.3 user-facing credential application workflow with canonical form fields, evidence, checks, approval policy, and lifecycle state */
export interface ApplicationTemplate {
  id: string;
  organization_id: string;
  name: string;
  description?: string;
  credential_template_id?: string | null;
  form_fields?: Record<string, unknown>[];
  evidence_requirements?: Record<string, unknown>[];
  claim_collection_rules?: Record<string, unknown>[];
  required_checks?: Record<string, unknown>[];
  approval_strategy: 'AUTO' | 'MANUAL' | 'RULES_BASED' | 'EXTERNAL';
  approval_policy_set_id?: string | null;
  application_validity_days?: number;
  notification_config?: Record<string, unknown>;
  ui_config?: Record<string, unknown>;
  status: 'DRAFT' | 'ACTIVE' | 'DEPRECATED';
  created_at: string;
  updated_at?: string;
}

/** A record of a biometric enrollment event for an applicant. Stores only the modality, hash of the biometric template, and metadata. Raw biometric data MUST NOT be stored in this record and MUST NOT be transmitted via the MIP API. */
export interface BiometricEnrollment {
  id: string;
  applicant_id: string;
  organization_id: string;
  modality: 'FACE' | 'FINGERPRINT' | 'IRIS' | 'VOICE' | 'PALM_VEIN' | 'SIGNATURE';
  template_hash: string;
  hash_algorithm: 'SHA-256' | 'SHA-384' | 'SHA-512';
  provider?: string | null;
  capture_device?: string | null;
  quality_score?: number | null;
  liveness_verified?: boolean;
  status: 'ENROLLED' | 'REVOKED' | 'SUPERSEDED';
  revoked_at?: string | null;
  revocation_reason?: string | null;
  created_at: string;
}

/** Tracks the cascade from a trust anchor or issuer revocation to dependent credentials. Provides circuit-breaker protection (pauses when affected_credential_count >= circuit_breaker_threshold), rollback support, and manual confirmation for high-impact operations. */
export interface CascadeRevocationOperation {
  id: string;
  organization_id: string;
  operation_type: 'ISSUER_REVOCATION' | 'ANCHOR_REVOCATION';
  trigger_entity_type: 'ISSUER' | 'TRUST_ANCHOR';
  trigger_entity_id: string;
  status: 'PENDING_CONFIRMATION' | 'IN_PROGRESS' | 'COMPLETED' | 'ROLLED_BACK' | 'FAILED';
  affected_credential_count?: number;
  affected_credential_ids?: string[];
  requires_confirmation?: boolean;
  confirmed_at?: string | null;
  confirmed_by?: string | null;
  max_cascade_depth?: number;
  current_depth?: number;
  circuit_breaker_threshold?: number;
  circuit_breaker_triggered?: boolean;
  can_rollback?: boolean;
  rollback_snapshot?: Record<string, unknown>;
  rolled_back_at?: string | null;
  rolled_back_by?: string | null;
  error_message?: string | null;
  metadata?: Record<string, unknown>;
  created_at: string;
  updated_at?: string;
}

/** A privacy-safe, recoverable reason that an approved application cannot yet produce a credential offer. */
export interface ClaimBlocker {
  code: string;
  owner: ClaimBlockerOwner;
  message: string;
}

/** Abstraction of credential format complexity behind compliance-oriented identifiers */
export interface ComplianceProfile {
  id: string;
  organization_id?: string | null;
  compliance_code: 'ICAO_DTC' | 'ICAO_MRZ' | 'ICAO_PASSPORT' | 'AAMVA_MDL' | 'EUDI_PID' | 'EUDI_MDL' | 'OB3_JWT' | 'OB3_JSONLD' | 'SD_JWT_VC' | 'ENTERPRISE_VC' | 'OID4VC' | 'PEX' | 'CUSTOM';
  name: string;
  description?: string;
  version?: string;
  specification_reference?: string;
  credential_format: CredentialFormat;
  issuance_protocol?: IssuanceProtocol;
  issuer_artifact_requirements?: Record<string, unknown>;
  verification_policy_set_id?: string | null;
  trust_profile_constraints?: Record<string, unknown>;
  api_surface?: Record<string, unknown>[];
  discoverable?: boolean;
  required_claims?: Record<string, unknown>[];
  optional_claims?: Record<string, unknown>[];
  required_namespaces?: string[];
  optional_namespaces?: string[];
  required_contexts?: string[];
  supported_proof_types?: string[];
  supported_algorithms?: string[];
  key_requirements?: Record<string, unknown>;
  revocation_methods?: RevocationMechanism[];
  revocation_required?: boolean;
  allow_skip_revocation?: boolean;
  trust_source_types?: string[];
  holder_binding_required?: boolean;
  selective_disclosure_required?: boolean;
  immutable?: boolean;
  oid4vci_features?: Record<string, unknown>;
  oid4vp_features?: Record<string, unknown>;
  pex_requirements?: Record<string, unknown>;
  physical_production?: Record<string, unknown>;
  pki_hierarchy?: Record<string, unknown>;
  vetting_requirements?: Record<string, unknown>;
  conformance_tests?: Record<string, unknown>[];
  status: 'DRAFT' | 'ACTIVE' | 'SUSPENDED' | 'DEPRECATED';
  is_system: boolean;
  created_at: string;
  updated_at?: string;
}

/** Public issuance configuration combining claims, compliance, issuer DID, and validity rules. Custody and signing-profile metadata are resolved internally from the organization and issuer DID. */
export interface CredentialTemplate {
  id: string;
  organization_id: string;
  name: string;
  credential_type: string;
  description?: string;
  compliance_profile_id: string;
  vct?: string | null;
  doctype?: string | null;
  credential_payload_format?: CredentialFormat;
  application_template_id?: string | null;
  trust_profile_id?: string | null;
  revocation_profile_id?: string | null;
  claims: Record<string, unknown>[];
  validity_rules: Record<string, unknown>;
  issuer_did?: string;
  privacy_posture?: Record<string, unknown>;
  status: 'DRAFT' | 'ACTIVE' | 'DEPRECATED';
  created_at: string;
  updated_at?: string;
}

/** A delivery destination describes where an issued credential can be delivered, opened, imported, or mirrored. Unlike WalletProfile, it can represent holder wallets, learner-owned backpacks, organization-managed mirrors such as Canvas Credentials, or custom delivery channels. */
export interface DeliveryDestinationProfile {
  id: string;
  organization_id?: string | null;
  is_system?: boolean;
  name: string;
  description?: string | null;
  provider: 'elevenid_wallet' | 'oid4vci_wallet' | 'didcomm_v2' | 'canvas_credentials' | 'canvas_credentials_backpack' | 'open_badges_backpack' | 'physical_personalization_bureau' | 'custom';
  mode: 'holder_wallet' | 'learner_backpack' | 'organization_mirror' | 'direct_delivery' | 'physical_production';
  setup_actor: 'learner' | 'org_admin' | 'system';
  delivery_target: 'wallet' | 'didcomm_v2' | 'canvas_credentials' | 'external_api' | 'webhook' | 'physical_document';
  wallet_profile_id?: string | null;
  credential_format?: 'MDOC' | 'SD_JWT_VC' | 'VC_JWT' | 'JSON_LD' | 'ICAO_EMRTD' | 'None';
  issuance_protocol?: 'OID4VCI_PRE_AUTH' | 'OID4VCI_AUTH_CODE' | 'DIRECT' | 'PHYSICAL_DOCUMENT' | 'None';
  compliance_profile_code?: string | null;
  connector_type?: string | null;
  connector_id?: string | null;
  requires_consent?: boolean;
  claim_projection_policy?: Record<string, unknown>;
  setup_requirements?: string[];
  capabilities?: Record<string, unknown>;
  docs_url?: string | null;
  is_enabled?: boolean;
  created_at: string;
  updated_at?: string | null;
}

/** Runtime configuration for a physical or logical identity verification endpoint. Packages trust, policies, issuance capability, network mode, user experience, and device grouping via Lanes. */
export interface DeploymentProfile {
  id: string;
  organization_id: string;
  name: string;
  description?: string;
  trust_profile_id: string;
  presentation_policy_ids: string[];
  credential_template_ids?: string[];
  default_policy_id?: string | null;
  site_id?: string | null;
  enabled_flow_ids?: string[];
  network_mode: 'ONLINE' | 'OFFLINE' | 'HYBRID';
  key_access_mode?: 'KEY_VAULT' | 'HSM' | 'DEVICE_KEYSTORE';
  environment_config?: Record<string, unknown>;
  update_channel?: 'stable' | 'beta' | 'pinned';
  update_policy?: Record<string, unknown>;
  offline_cache_ttl_hours?: number;
  operator_biometric_authentication_required?: boolean;
  biometric_required?: boolean;
  audit_all_events?: boolean;
  lanes?: Lane[];
  created_at: string;
  updated_at?: string;
}

/** User device record for push notification delivery and challenge-response authentication */
export interface DeviceRegistration {
  id?: string;
  user_id: string;
  organization_id?: string | null;
  device_id: string;
  platform: 'ios' | 'android' | 'web';
  fcm_token: string;
  app_version?: string;
  os_version?: string;
  device_model?: string;
  preferences?: Record<string, unknown>;
  public_key_der?: string;
  public_key_kid?: string;
  key_valid_from?: string;
  key_valid_until?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  last_seen_at?: string;
}

/** Immutable normalized fact derived from verified evidence. Provider adapters create EvidenceFacts from receipts so approval policy can evaluate facts without parsing provider payloads. */
export interface EvidenceFact {
  id: string;
  organization_id: string;
  application_id: string;
  subject_id: string;
  provider: string;
  fact_type: string;
  scope: Record<string, unknown>;
  assertion: Record<string, unknown>;
  verification: Record<string, unknown>;
  source: Record<string, unknown>;
  created_at: string;
}

/** Runtime state of a single flow instance. Tracks current step, step results, context data, and lifecycle transitions. Created when a flow is initiated; updated as steps complete. */
export interface FlowExecution {
  id: string;
  flow_id: string;
  flow_type: FlowType;
  organization_id: string;
  status: FlowInstanceStatus;
  current_step?: string | null;
  current_step_index?: number;
  step_results?: Record<string, unknown>;
  context_data?: Record<string, unknown>;
  issued_credential_id?: string | null;
  started_at?: string | null;
  completed_at?: string | null;
  expires_at?: string | null;
  error_code?: string | null;
  metadata?: Record<string, unknown>;
  created_at: string;
  updated_at?: string;
}

/** Versioned non-standard orchestration envelope. A custom Flow uses this object so it cannot claim the conformance semantics of a standard FlowType. */
export interface FlowExtension {
  extension_uri: string;
  extension_version: string;
  extends_flow_type: FlowType;
  entry_step_id: string;
  steps: Record<string, unknown>[];
  transitions: Record<string, unknown>[];
  config?: Record<string, unknown>;
}

/** End-to-end identity lifecycle orchestration. Standard FlowTypes have fixed protocol sequences; non-standard graphs use flow_type custom with a versioned extension envelope. */
export interface Flow {
  id: string;
  organization_id: string;
  name: string;
  description?: string;
  flow_type: FlowType;
  flow_category?: 'ISSUANCE' | 'VERIFICATION' | 'RENEWAL' | 'REVOCATION' | 'COMBINED';
  trust_profile_id?: string | null;
  credential_template_id?: string | null;
  application_template_id?: string | null;
  presentation_policy_id?: string | null;
  delivery_destination_profile_id?: string | null;
  deployment_profile_ids?: string[];
  approval_strategy: ApprovalStrategy;
  hooks?: Record<string, unknown>;
  trigger?: Record<string, unknown>;
  extension?: FlowExtension;
  status: 'DRAFT' | 'ACTIVE' | 'PAUSED' | 'ARCHIVED';
  created_at: string;
  updated_at?: string;
}

/** Privacy-filtered response from GET /v1/issued-credentials/mine. Credential material, claims, hashes, signing references, and opaque subject identifiers are prohibited. */
export interface HolderCredentialInventory {
  items: Record<string, unknown>[];
  total: number;
  limit: number;
  offset: number;
}

/** Public request to create a credential issuance. Custody and issuer-profile selectors are intentionally absent. */
export interface IssuanceRequest {
  organization_id: string;
  credential_template_id?: string | null;
  issuer_did?: string | null;
  subject_did?: string | null;
  holder_did?: string | null;
  authorized_client?: Record<string, unknown> | null;
  application_id?: string | null;
  claims?: Record<string, unknown>;
  credential_subject?: Record<string, unknown> | null;
  credential_document?: Record<string, unknown> | null;
}

/** Record of a credential issuance event */
export interface IssuanceRecord {
  id: string;
  flow_id: string;
  flow_execution_id?: string | null;
  application_id?: string | null;
  credential_template_id: string;
  holder_id: string;
  credential_id?: string | null;
  credential_format?: 'MDOC' | 'SD_JWT_VC' | 'VC_JWT' | 'JSON_LD';
  offer_uri?: string | null;
  offer_expires_at?: string | null;
  status: 'PENDING' | 'OFFER_SENT' | 'CLAIMED' | 'EXPIRED' | 'FAILED' | 'REVOKED';
  revocation_index?: number | null;
  valid_from?: string | null;
  valid_until?: string | null;
  created_at: string;
  claimed_at?: string | null;
}

/** Lifecycle record for an issued credential. Stores metadata without raw credential data (only a SHA-256 hash for integrity). Links FlowExecution to credential status, status list entries, and revocation history. */
export interface IssuedCredential {
  id: string;
  organization_id: string;
  credential_id: string;
  credential_type: string;
  credential_format: 'MDOC' | 'SD_JWT_VC' | 'VC_JWT' | 'JSON_LD';
  flow_execution_id: string;
  credential_template_id: string;
  application_id?: string | null;
  revocation_profile_id?: string | null;
  renewed_from_credential_id?: string | null;
  renewed_to_credential_id?: string | null;
  renewable?: boolean;
  renewal_eligible_at?: string | null;
  can_renew?: boolean;
  subject_id: string;
  subject_claims_hash?: string | null;
  issued_at: string;
  valid_from?: string | null;
  valid_until?: string | null;
  status: 'ACTIVE' | 'SUSPENDED' | 'REVOKED' | 'EXPIRED';
  status_list_entries?: Record<string, unknown>[];
  credential_hash?: string | null;
  revoked_at?: string | null;
  revocation_reason?: string | null;
  revoked_by?: string | null;
  created_at: string;
  updated_at?: string;
}

/** An organisation or authority that issues credentials. Separate from Trust Anchors (cryptographic roots). An issuer may be backed by one or more trust anchors. Supports full lifecycle: accreditation, suspension, and revocation. */
export interface IssuerEntity {
  id: string;
  organization_id?: string | null;
  issuer_id: string;
  issuer_type: 'ORGANIZATION' | 'GOVERNMENT' | 'DEVICE';
  display_name: string;
  description?: string;
  is_system_issuer?: boolean;
  compliance_status: 'ACCREDITED' | 'COMPLIANT' | 'SUSPENDED' | 'REVOKED';
  accreditation_body?: string | null;
  accreditation_date?: string | null;
  valid_from: string;
  valid_until?: string | null;
  trust_anchor_id?: string | null;
  revoked_at?: string | null;
  revocation_reason?: string | null;
  revoked_by?: string | null;
  metadata?: Record<string, unknown>;
  created_at: string;
  updated_at?: string;
}

/** Logical device grouping within a Deployment Profile */
export interface Lane {
  id: string;
  name: string;
  deployment_profile_id: string;
  default_policy_id?: string | null;
  device_ids?: string[];
  metadata?: Record<string, unknown>;
}

/** Schema for the /.well-known/mip-configuration endpoint response. This document describes the capabilities, endpoints, and supported profiles of a MIP implementation. Analogous to OpenID Connect Discovery (RFC 8414) but scoped to MIP-specific capabilities. */
export interface MipConfigurationDiscoveryDocument {
  mip_version: string;
  issuer: string;
  mip_configuration_endpoint: string;
  supported_versions: string[];
  implementation_classes: string[];
  issuance_endpoint?: string;
  openid_credential_issuer?: string;
  presentation_endpoint?: string;
  token_endpoint?: string;
  authorization_endpoint?: string;
  supported_credential_formats?: string[];
  supported_compliance_profiles?: string[];
  active_compliance_profiles: ActiveComplianceProfile[];
  supported_flow_types?: string[];
  supported_signing_algorithms?: string[];
  proximity_supported?: boolean;
  proximity_engagement_methods?: string[];
  scim_endpoint?: string;
  revocation_endpoint?: string;
  jwks_uri?: string;
  org_endpoints?: Record<string, unknown>[];
  service_documentation?: string;
  policy_uri?: string;
}

/** Message content and routing metadata for multi-channel identity event notification */
export interface NotificationPayload {
  id: string;
  title: string;
  body: string;
  data?: Record<string, unknown>;
  event_type: string;
  priority: 'LOW' | 'NORMAL' | 'HIGH' | 'CRITICAL';
  target: NotificationTarget;
  ttl_seconds?: number;
  collapse_key?: string;
  correlation_id?: string;
  created_at: string;
}

/** Multi-channel message delivery targeting configuration */
export interface NotificationTarget {
  organization_id?: string;
  user_id?: string;
  device_tokens?: string[];
  webhook_endpoints?: string[];
  email_addresses?: string[];
  channels: string[];
}

/** Response from the OID4VCI 1.0 Final Nonce Endpoint. The HTTP response must also include Cache-Control: no-store. */
export interface OID4VCINonceResponse {
  c_nonce: string;
}

/** Organisation-specific overlay of a TrustFramework. Separates shared framework definitions from per-org policy overrides, issuer allow/deny lists, and jurisdiction filters. */
export interface OrganizationTrustProfile {
  id: string;
  organization_id: string;
  framework_id: string;
  name: string;
  display_name?: string;
  description?: string;
  enabled?: boolean;
  use_case_tags?: string[];
  compliance_status: 'COMPLIANT' | 'NEEDS_ATTENTION' | 'SETUP_REQUIRED';
  auto_generated?: boolean;
  revocation_policy?: Record<string, unknown> | null;
  time_policy?: Record<string, unknown> | null;
  allowed_algorithms?: string[] | null;
  allowed_formats?: string[] | null;
  allowed_issuers?: string[] | null;
  denied_issuers?: string[] | null;
  jurisdiction_filter?: string[] | null;
  metadata?: Record<string, unknown>;
  created_at: string;
  updated_at?: string;
}

/** The primary multi-tenant boundary in MIP. All configuration resources are scoped to an organization. */
export interface Organization {
  id: string;
  name: string;
  display_name: string;
  description?: string;
  join_code?: string | null;
  visibility: 'PUBLIC' | 'PRIVATE';
  owner_id: string;
  status: 'ACTIVE' | 'SUSPENDED' | 'DELETED';
  created_at: string;
  updated_at?: string | null;
}

/** Auditable production state for one physical ICAO eMRTD document. Sensitive data groups, biometrics, signing keys, and connector secrets are referenced but never embedded. */
export interface PhysicalDocumentJob {
  id: string;
  organization_id: string;
  flow_execution_id: string;
  application_id: string;
  credential_template_id: string;
  delivery_destination_profile_id: string;
  document_type: 'TD1' | 'TD2' | 'TD3';
  country_code?: string;
  secure_artifact_reference?: string | null;
  bureau_job_id?: string | null;
  tracking_number?: string | null;
  status: 'DRAFT' | 'DATA_GENERATED' | 'SOD_SIGNED' | 'SUBMITTED' | 'IN_PRODUCTION' | 'QUALITY_CHECK' | 'READY_FOR_ACTIVATION' | 'ACTIVE' | 'FAILED' | 'CANCELLED';
  quality_result?: Record<string, unknown> | null;
  error_code?: string | null;
  error_message?: string | null;
  submitted_at?: string | null;
  completed_at?: string | null;
  created_at: string;
  updated_at?: string | null;
}

/** A named collection of Cedar policies that governs authorization decisions within the MIP platform. PolicySets are referenced by ApplicationTemplate (approval_policy_set_id), TrustProfile, ComplianceProfile, and the API gateway. Each PolicySet is evaluated using deny-by-default semantics: at least one permit must match and zero forbid policies may match. */
export interface PolicySet {
  id: string;
  organization_id: string;
  name: string;
  description?: string;
  policy_type: 'ACCESS_CONTROL' | 'CREDENTIAL_VERIFICATION' | 'APPROVAL_RULES' | 'CUSTOM';
  cedar_policies: Record<string, unknown>[];
  cedar_schema_version?: string;
  status: 'DRAFT' | 'ACTIVE' | 'ARCHIVED';
  created_at: string;
  updated_at?: string;
}

/** Minimum disclosure requirements, predicates, and holder binding for credential verification */
export interface PresentationPolicy {
  id: string;
  organization_id: string;
  name: string;
  description?: string;
  purpose?: string;
  required_claims: Record<string, unknown>[];
  accepted_credential_types?: string[];
  trust_profile_id?: string | null;
  holder_binding?: Record<string, unknown>;
  freshness?: Record<string, unknown>;
  prefer_predicates?: boolean;
  supported_circuits?: string[];
  fallback_policy?: 'REQUIRE_PREDICATE' | 'ACCEPT_RAW' | 'DENY';
  issuer_constraints?: Record<string, unknown>;
  credential_ranking_strategy?: 'FRESHEST_FIRST' | 'HIGHEST_TRUST_FIRST' | 'CUSTOM';
  credential_ranking_weights?: Record<string, unknown>;
  created_at: string;
  updated_at?: string;
}

/** A time-bounded exclusive lock that prevents two reviewers from acting on the same applicant simultaneously. A lock MUST be acquired before transitioning an applicant out of SUBMITTED or UNDER_REVIEW. Locks expire automatically; the default TTL is 1800 seconds (30 minutes). */
export interface ReviewerLock {
  id: string;
  applicant_id: string;
  organization_id: string;
  holder_user_id: string;
  ttl_seconds?: number;
  expires_at: string;
  released_at?: string | null;
  status?: 'ACTIVE' | 'RELEASED' | 'EXPIRED';
  created_at: string;
}

/** Privacy-preserving batched revocation. Instead of publishing status list updates immediately (which enables timing-correlation attacks), the system batches revocations and publishes at configurable intervals. Interval options: 1h, 6h, 24h. */
export interface RevocationBatch {
  id: string;
  organization_id: string;
  credential_format: 'MDOC' | 'SD_JWT_VC' | 'VC_JWT' | 'JSON_LD';
  batch_interval: '1h' | '6h' | '24h';
  status: 'PENDING' | 'PUBLISHING' | 'PUBLISHED' | 'FAILED';
  pending_credential_ids?: string[];
  published_credential_count?: number;
  status_list_uri?: string | null;
  scheduled_publish_at?: string | null;
  published_at?: string | null;
  error_message?: string | null;
  created_at: string;
  updated_at?: string;
}

/** Format-agnostic revocation configuration for issuers and verifiers */
export interface RevocationProfile {
  id: string;
  organization_id: string;
  name: string;
  status: 'DRAFT' | 'ACTIVE' | 'SUSPENDED';
  revocation_mechanism: string[];
  mechanism_priority?: string[];
  check_mode: RevocationTimingMode;
  cache_ttl_seconds?: number;
  offline_grace_seconds?: number;
  issuer_config?: Record<string, unknown>;
  status_list_url?: string;
  created_at: string;
  updated_at?: string;
}

/** MIP extension attributes for SCIM 2.0 Group resources representing roles. Schema URI: urn:mip:scim:schemas:extension:Organization:2.0:Role */
export interface MipScimRoleGroupExtension {
  permissions?: string[];
  policy_set_id?: string | null;
  is_system_role?: boolean;
  description?: string;
}

/** MIP extension attributes for SCIM 2.0 User resources. Schema URI: urn:mip:scim:schemas:extension:Organization:2.0:User */
export interface MipScimUserExtension {
  role_ids?: string[];
  is_owner?: boolean;
  joined_at?: string | null;
}

/** Event subscription that routes identity lifecycle events to a configured delivery target (webhook, email, or SSE channel). Managed via /v1/subscriptions. */
export interface Subscription {
  id: string;
  organization_id: string;
  name: string;
  description?: string;
  event_types: string[];
  delivery: Record<string, unknown>;
  filter?: Record<string, unknown>;
  enabled: boolean;
  retry_policy?: Record<string, unknown>;
  created_at: string;
  updated_at?: string;
}

/** System-managed trust framework definition for ICAO, AAMVA, EUDI, or custom identity ecosystems. Immutable at the system level; organisations reference frameworks via OrganizationTrustProfile. */
export interface TrustFramework {
  id: string;
  code: string;
  display_name: string;
  description?: string;
  pkd_endpoints?: Record<string, unknown>;
  default_algorithms: string[];
  default_formats: string[];
  validation_ruleset?: Record<string, unknown>;
  sync_config?: Record<string, unknown>;
  is_system: boolean;
  created_at: string;
  updated_at?: string;
}

/** Join entity between TrustProfile and IssuerEntity with trust scoring and cascade revocation policy. trust_level is a 0–100 score; future versions will auto-adjust based on issuer history (failed validations, revocation events, compliance lapses). */
export interface TrustProfileIssuer {
  id: string;
  trust_profile_id: string;
  issuer_id: string;
  trust_level: number;
  relationship_status: 'TRUSTED' | 'DENIED' | 'UNDER_REVIEW';
  cascade_revocation_policy: 'AUTO_CASCADE' | 'MANUAL' | 'NOTIFY_ONLY';
  metadata?: Record<string, unknown>;
  created_at: string;
  updated_at?: string;
}

/** Cryptographic trust configuration for credential issuance and verification. Used by both issuance flows (which issuer keys are trusted) and verification flows (which credential issuers/roots are accepted). For org-specific framework overrides, see OrganizationTrustProfile. */
export interface TrustProfile {
  id: string;
  organization_id: string;
  name: string;
  description?: string;
  profile_type: 'ICAO' | 'AAMVA' | 'EUDI' | 'CUSTOM';
  trust_sources: Record<string, unknown>[];
  allowed_algorithms: string[];
  revocation_policy?: Record<string, unknown>;
  revocation_services?: Record<string, unknown>;
  time_policy?: Record<string, unknown>;
  supported_formats: string[];
  allowed_issuers?: string[] | null;
  denied_issuers?: string[] | null;
  system_issuer_overrides?: Record<string, unknown>;
  compliance_status: 'COMPLIANT' | 'NEEDS_ATTENTION' | 'SETUP_REQUIRED';
  revocation_profile_id?: string | null;
  verification_policy_set_id?: string | null;
  compatible_compliance_codes?: string[];
  auto_generated?: boolean;
  created_at: string;
  updated_at?: string;
}

/** Delta-sync resource for mobile wallet trust registry updates. Provides CSCA/DSC anchor data from the /v1/trust-registry endpoints so wallets can sync incrementally rather than downloading the full trust store on every launch. */
export interface TrustRegistrySync {
  sync_token: string;
  sequence: number;
  entries: Record<string, unknown>[];
  has_more?: boolean;
  generated_at: string;
}

/** Public request to start an OID4VP or SIOPv2 flow using a DID-resolved verifier profile. */
export interface VerificationFlowStartRequest {
  presentation_policy_id?: string | null;
  organization_id: string;
  issuer_did: string;
  response_type?: 'vp_token' | 'id_token';
  trust_profile_id?: string | null;
  deployment_profile_id?: string | null;
  external_reference?: string | null;
  callback_url?: string | null;
  expiry_minutes?: number;
  oid4vp_profile?: 'standard' | 'haip';
  request_transport?: 'request_uri' | 'request_object' | 'url_query';
  request_uri_method?: 'get' | 'post';
}

/** Public response for a newly started verification flow. Internal flow-definition routing is intentionally absent. */
export interface VerificationFlowStartResponse {
  instance_id: string;
  request_uri: string;
  qr_code_data: string;
  presentation_policy_id: string;
  nonce: string;
  expires_at: string;
  status: string;
}

/** A single presentation-request/response cycle instance */
export interface VerificationSession {
  id: string;
  flow_id: string;
  flow_instance_id?: string;
  presentation_policy_id: string;
  deployment_profile_id?: string | null;
  verifier_nonce?: string;
  holder_id?: string | null;
  status: 'PENDING' | 'AWAITING_PRESENTATION' | 'VERIFYING' | 'PASSED' | 'FAILED' | 'EXPIRED' | 'CANCELLED';
  result?: Record<string, unknown> | null;
  expires_at?: string;
  created_at: string;
  completed_at?: string | null;
  updated_at?: string | null;
  error?: string | null;
}

/** A discrete identity or document verification check performed as part of the applicant review process. Each check corresponds to a single automated or manual verification step. */
export interface VettingCheck {
  id: string;
  applicant_id: string;
  organization_id: string;
  check_type: 'DOCUMENT_AUTHENTICITY' | 'DOCUMENT_EXPIRY' | 'FACIAL_MATCH' | 'LIVENESS_DETECTION' | 'IDENTITY_DATABASE' | 'WATCHLIST_SCREENING' | 'ADDRESS_VERIFICATION' | 'EMAIL_VERIFICATION' | 'PHONE_VERIFICATION' | 'BACKGROUND_CHECK' | 'MANUAL_REVIEW' | 'CUSTOM';
  provider?: string | null;
  provider_reference_id?: string | null;
  status: 'PENDING' | 'IN_PROGRESS' | 'PASSED' | 'FAILED' | 'INCONCLUSIVE' | 'SKIPPED' | 'EXPIRED';
  score?: number | null;
  threshold?: number | null;
  failure_reason?: string | null;
  evidence_refs?: Record<string, unknown>[];
  performed_by?: string | null;
  started_at?: string | null;
  completed_at?: string | null;
  expires_at?: string | null;
  raw_result?: Record<string, unknown> | null;
  created_at: string;
  updated_at?: string;
}

/** Wallet compatibility record for a credential format × protocol × compliance combination. The canonical wallet profile set is auto-derived from CredentialTemplate configuration via the derivation key (credential_format, issuance_protocol, compliance_profile_code). Organizations MAY store override entries at /v1/wallet-registry to extend or customise the derived profile for their specific deployment. GET /v1/wallet-registry returns merged results: derived profiles supplemented (or overridden) by stored entries. */
export interface WalletProfile {
  id?: string;
  organization_id?: string | null;
  is_override?: boolean;
  override_precedence?: number;
  name: string;
  description?: string;
  credential_format: 'MDOC' | 'MSO_MDOC' | 'SD_JWT_VC' | 'VC_JWT' | 'JSON_LD';
  issuance_protocol: 'OID4VCI_PRE_AUTH' | 'OID4VCI_AUTH_CODE' | 'DIRECT';
  compliance_profile_code?: string | null;
  wallet_apps?: string[];
  merge_strategy?: 'APPEND' | 'REPLACE';
  specifications?: string[];
  supported_platforms?: string[];
  deep_link_pattern?: string;
  format_variant?: string;
  deep_link_scheme?: string;
  created_at: string;
  updated_at?: string;
}

/** A persistent webhook subscription that delivers signed HTTP POST callbacks to an operator-controlled endpoint when specified identity lifecycle events occur. Managed via /v1/organizations/{org_id}/webhooks. */
export interface Webhook {
  id: string;
  organization_id: string;
  name: string;
  description?: string;
  endpoint_url: string;
  events: string[];
  signing_secret?: string | null;
  signing_secret_masked?: string | null;
  enabled: boolean;
  api_version?: string;
  filter?: Record<string, unknown>;
  delivery_config?: Record<string, unknown>;
  status?: 'ACTIVE' | 'PAUSED' | 'DISABLED_PERMANENTLY';
  failure_count?: number;
  last_triggered_at?: string | null;
  last_success_at?: string | null;
  created_at: string;
  updated_at?: string;
}

