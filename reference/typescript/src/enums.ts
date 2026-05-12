// MIP Protocol Enums — generated from marty-protocol/enums/*.json
// Generated: 2026-05-11
// DO NOT EDIT — regenerate with: python scripts/codegen.py typescript

/** Formal permission scope strings for MIP API keys. Scopes follow the pattern '{resource}:{action}'. Organization-scoped keys may hold any of these scopes. Deployment-scoped keys are restricted to a subset appropriate for a single deployment profile. */
export enum ApiKeyScope {
  CREDENTIALS_ISSUE = 'credentials:issue',
  CREDENTIALS_REVOKE = 'credentials:revoke',
  CREDENTIALS_READ = 'credentials:read',
  FLOWS_READ = 'flows:read',
  FLOWS_WRITE = 'flows:write',
  FLOWS_EXECUTE = 'flows:execute',
  APPLICATIONS_READ = 'applications:read',
  APPLICATIONS_WRITE = 'applications:write',
  APPLICATIONS_APPROVE = 'applications:approve',
  TRUST_READ = 'trust:read',
  TRUST_WRITE = 'trust:write',
  TRUST_ADMIN = 'trust:admin',
  COMPLIANCE_READ = 'compliance:read',
  COMPLIANCE_WRITE = 'compliance:write',
  TEMPLATES_READ = 'templates:read',
  TEMPLATES_WRITE = 'templates:write',
  WALLET_READ = 'wallet:read',
  WALLET_WRITE = 'wallet:write',
  KEYS_READ = 'keys:read',
  KEYS_WRITE = 'keys:write',
  USERS_READ = 'users:read',
  USERS_INVITE = 'users:invite',
  ROLES_READ = 'roles:read',
  ROLES_WRITE = 'roles:write',
  AUDIT_READ = 'audit:read',
  WEBHOOKS_READ = 'webhooks:read',
  WEBHOOKS_WRITE = 'webhooks:write',
  NOTIFICATIONS_SEND = 'notifications:send',
  NOTIFICATIONS_READ = 'notifications:read',
  DEPLOYMENT_READ = 'deployment:read',
  DEPLOYMENT_WRITE = 'deployment:write',
  ADMIN_FULL = 'admin:full',
}

/** Lifecycle status of an Applicant. Terminal states: REJECTED, WITHDRAWN, CREDENTIALED, SUSPENDED. */
export enum ApplicantStatus {
  DRAFT = 'DRAFT',
  SUBMITTED = 'SUBMITTED',
  UNDER_REVIEW = 'UNDER_REVIEW',
  PENDING_INFORMATION = 'PENDING_INFORMATION',
  APPROVED = 'APPROVED',
  REJECTED = 'REJECTED',
  WITHDRAWN = 'WITHDRAWN',
  CREDENTIALED = 'CREDENTIALED',
  SUSPENDED = 'SUSPENDED',
}

/** How credential applications are reviewed and approved */
export enum ApprovalStrategy {
  AUTO = 'AUTO',
  MANUAL = 'MANUAL',
  RULES_BASED = 'RULES_BASED',
  EXTERNAL = 'EXTERNAL',
}

/** Notification delivery channel types */
export enum ChannelType {
  FCM = 'FCM',
  SSE = 'SSE',
  WEBHOOK = 'WEBHOOK',
  EMAIL = 'EMAIL',
  SMS = 'SMS',
}

/** Recognized compliance frameworks and identity standards for credential format abstraction */
export enum ComplianceCode {
  ICAO_DTC = 'ICAO_DTC',
  ICAO_MRZ = 'ICAO_MRZ',
  ICAO_PASSPORT = 'ICAO_PASSPORT',
  AAMVA_MDL = 'AAMVA_MDL',
  EUDI_PID = 'EUDI_PID',
  EUDI_MDL = 'EUDI_MDL',
  OB3_JWT = 'OB3_JWT',
  OB3_JSONLD = 'OB3_JSONLD',
  OB2_COMPATIBILITY = 'OB2_COMPATIBILITY',
  SD_JWT_VC = 'SD_JWT_VC',
  ENTERPRISE_VC = 'ENTERPRISE_VC',
  OID4VC = 'OID4VC',
  PEX = 'PEX',
  CUSTOM = 'CUSTOM',
}

/** Technical encoding formats for verifiable credentials */
export enum CredentialFormat {
  MDOC = 'MDOC',
  SD_JWT_VC = 'SD_JWT_VC',
  VC_JWT = 'VC_JWT',
  JSON_LD = 'JSON_LD',
  ZK_MDOC = 'ZK_MDOC',
}

/** When a wallet holds multiple credentials that satisfy a PresentationPolicy, this strategy determines which is preferred. Used in PresentationPolicy.credential_ranking_strategy. */
export enum CredentialRankingStrategy {
  FRESHEST_FIRST = 'FRESHEST_FIRST',
  HIGHEST_TRUST_FIRST = 'HIGHEST_TRUST_FIRST',
  CUSTOM = 'CUSTOM',
}

/** Supported device platforms for Device Registration */
export enum DevicePlatform {
  IOS = 'ios',
  ANDROID = 'android',
  WEB = 'web',
}

/** Behavior when ZK circuit is unavailable for a predicate requirement */
export enum FallbackPolicy {
  REQUIRE_PREDICATE = 'REQUIRE_PREDICATE',
  ACCEPT_RAW = 'ACCEPT_RAW',
  DENY = 'DENY',
}

/** Lifecycle status of a FlowInstance. Aligned with §9.9.2 state machine. Terminal states: COMPLETED, FAILED, EXPIRED, CANCELLED. */
export enum FlowInstanceStatus {
  PENDING = 'PENDING',
  IN_PROGRESS = 'IN_PROGRESS',
  AWAITING_APPROVAL = 'AWAITING_APPROVAL',
  AWAITING_WALLET = 'AWAITING_WALLET',
  AWAITING_EVIDENCE = 'AWAITING_EVIDENCE',
  COMPLETED = 'COMPLETED',
  FAILED = 'FAILED',
  EXPIRED = 'EXPIRED',
  CANCELLED = 'CANCELLED',
}

/** Protocol-aligned flow types. Each type maps to a fixed ordered step sequence. Issuance and verification flows are separate; application_approval_issuance is the multi-step application workflow. */
export enum FlowType {
  OID4VCI_PRE_AUTHORIZED = 'oid4vci_pre_authorized',
  OID4VCI_AUTHORIZATION_CODE = 'oid4vci_authorization_code',
  MDL_ISSUANCE = 'mdl_issuance',
  OID4VP_PRESENTATION = 'oid4vp_presentation',
  MDL_PRESENTATION = 'mdl_presentation',
  APPLICATION_APPROVAL_ISSUANCE = 'application_approval_issuance',
  CREDENTIAL_RENEWAL = 'credential_renewal',
  CREDENTIAL_REVOCATION = 'credential_revocation',
  PHYSICAL_DOCUMENT_ISSUANCE = 'physical_document_issuance',
  COMBINED = 'combined',
  SIOPV2 = 'siopv2',
}

/** Protocols used to deliver credentials from issuer to holder */
export enum IssuanceProtocol {
  OID4VCI_PRE_AUTH = 'OID4VCI_PRE_AUTH',
  OID4VCI_AUTH_CODE = 'OID4VCI_AUTH_CODE',
  DIRECT = 'DIRECT',
  PHYSICAL_DOCUMENT = 'PHYSICAL_DOCUMENT',
}

/** Network connectivity requirements for a Deployment Profile */
export enum NetworkMode {
  ONLINE = 'ONLINE',
  OFFLINE = 'OFFLINE',
  HYBRID = 'HYBRID',
}

/** Priority levels for notification delivery routing and FCM/APNs configuration */
export enum NotificationPriority {
  LOW = 'LOW',
  NORMAL = 'NORMAL',
  HIGH = 'HIGH',
  CRITICAL = 'CRITICAL',
}

/** Types of zero-knowledge predicates supported in Presentation Policies */
export enum PredicateType {
  RANGE_PROOF = 'RANGE_PROOF',
  MEMBERSHIP = 'MEMBERSHIP',
  EQUALITY = 'EQUALITY',
  NON_MEMBERSHIP = 'NON_MEMBERSHIP',
  INEQUALITY = 'INEQUALITY',
}

/** Behaviour when performing a revocation check during credential verification. Used in TrustProfile.revocation_policy.check_mode and OrganizationTrustProfile.revocation_policy.check_mode. */
export enum RevocationCheckMode {
  HARD_FAIL = 'HARD_FAIL',
  SOFT_FAIL = 'SOFT_FAIL',
  SKIP = 'SKIP',
}

/** Supported cryptographic credential revocation mechanisms */
export enum RevocationMechanism {
  OCSP = 'OCSP',
  CRL = 'CRL',
  STATUS_LIST_2021 = 'STATUS_LIST_2021',
  BITSTRING_STATUS_LIST = 'BITSTRING_STATUS_LIST',
  TOKEN_STATUS_LIST = 'TOKEN_STATUS_LIST',
}

/** Standard reasons for revoking a credential or trust anchor. Aligned with RFC 5280 CRL reason codes and X.509 CRLReason extension. */
export enum RevocationReason {
  UNSPECIFIED = 'unspecified',
  KEY_COMPROMISE = 'key_compromise',
  CA_COMPROMISE = 'ca_compromise',
  AFFILIATION_CHANGED = 'affiliation_changed',
  SUPERSEDED = 'superseded',
  CESSATION_OF_OPERATION = 'cessation_of_operation',
  CERTIFICATE_HOLD = 'certificate_hold',
  PRIVILEGE_WITHDRAWN = 'privilege_withdrawn',
}

/** Check-timing behavior for revocation during credential verification. Used in RevocationProfile.check_mode. Distinct from RevocationCheckMode (revocation-check-modes.json) which governs failure behavior in TrustProfile. */
export enum RevocationTimingMode {
  ALWAYS = 'ALWAYS',
  CACHED = 'CACHED',
  OFFLINE_GRACE = 'OFFLINE_GRACE',
  DISABLED = 'DISABLED',
}

/** Types of cryptographic trust material sources */
export enum TrustSourceType {
  TRUST_LIST = 'TRUST_LIST',
  PINNED_ISSUER = 'PINNED_ISSUER',
  ROOT_CA = 'ROOT_CA',
  PKD_URL = 'PKD_URL',
}

/** Accepted cryptographic signature algorithms for credential signing and verification */
export enum ValidationAlgorithm {
  ES256 = 'ES256',
  ES384 = 'ES384',
  ES512 = 'ES512',
  PS256 = 'PS256',
  PS384 = 'PS384',
  PS512 = 'PS512',
  EDDSA = 'EdDSA',
  RS256 = 'RS256',
  RS384 = 'RS384',
  RS512 = 'RS512',
  BBS_BLS12381_SHA256 = 'BBS_BLS12381_SHA256',
  BBS_BLS12381_SHAKE256 = 'BBS_BLS12381_SHAKE256',
}

/** Registry of zero-knowledge circuit systems and their circuit identifiers accepted in PredicateSpec.supported_circuits. Each system defines a proof scheme, a circuit identification method, and the set of supported credential formats and predicate types. */
export enum ZkCircuitSystem {
  LONGFELLOW_LIBZK_V1 = 'longfellow-libzk-v1',
}

