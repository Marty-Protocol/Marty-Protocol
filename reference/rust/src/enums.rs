//! MIP Protocol Enums — generated from marty-protocol/enums/*.json
//! Generated: 2026-03-14
//! DO NOT EDIT — regenerate with: python scripts/codegen.py rust

use serde::{Deserialize, Serialize};

/// Formal permission scope strings for MIP API keys. Scopes follow the pattern '{resource}:{action}'. Organization-scoped keys may hold any of these scopes. Deployment-scoped keys are restricted to a subset appropriate for a single deployment profile.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ApiKeyScope {
    #[serde(rename = "credentials:issue")]
    CredentialsIssue,
    #[serde(rename = "credentials:revoke")]
    CredentialsRevoke,
    #[serde(rename = "credentials:read")]
    CredentialsRead,
    #[serde(rename = "flows:read")]
    FlowsRead,
    #[serde(rename = "flows:write")]
    FlowsWrite,
    #[serde(rename = "flows:execute")]
    FlowsExecute,
    #[serde(rename = "applications:read")]
    ApplicationsRead,
    #[serde(rename = "applications:write")]
    ApplicationsWrite,
    #[serde(rename = "applications:approve")]
    ApplicationsApprove,
    #[serde(rename = "trust:read")]
    TrustRead,
    #[serde(rename = "trust:write")]
    TrustWrite,
    #[serde(rename = "trust:admin")]
    TrustAdmin,
    #[serde(rename = "compliance:read")]
    ComplianceRead,
    #[serde(rename = "compliance:write")]
    ComplianceWrite,
    #[serde(rename = "templates:read")]
    TemplatesRead,
    #[serde(rename = "templates:write")]
    TemplatesWrite,
    #[serde(rename = "wallet:read")]
    WalletRead,
    #[serde(rename = "wallet:write")]
    WalletWrite,
    #[serde(rename = "keys:read")]
    KeysRead,
    #[serde(rename = "keys:write")]
    KeysWrite,
    #[serde(rename = "users:read")]
    UsersRead,
    #[serde(rename = "users:invite")]
    UsersInvite,
    #[serde(rename = "roles:read")]
    RolesRead,
    #[serde(rename = "roles:write")]
    RolesWrite,
    #[serde(rename = "audit:read")]
    AuditRead,
    #[serde(rename = "webhooks:read")]
    WebhooksRead,
    #[serde(rename = "webhooks:write")]
    WebhooksWrite,
    #[serde(rename = "notifications:send")]
    NotificationsSend,
    #[serde(rename = "notifications:read")]
    NotificationsRead,
    #[serde(rename = "deployment:read")]
    DeploymentRead,
    #[serde(rename = "deployment:write")]
    DeploymentWrite,
    #[serde(rename = "admin:full")]
    AdminFull,
}

/// How credential applications are reviewed and approved
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ApprovalStrategy {
    #[serde(rename = "AUTO")]
    Auto,
    #[serde(rename = "MANUAL")]
    Manual,
    #[serde(rename = "RULES_BASED")]
    RulesBased,
    #[serde(rename = "EXTERNAL")]
    External,
}

/// Notification delivery channel types
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ChannelType {
    #[serde(rename = "FCM")]
    Fcm,
    #[serde(rename = "SSE")]
    Sse,
    #[serde(rename = "WEBHOOK")]
    Webhook,
    #[serde(rename = "EMAIL")]
    Email,
    #[serde(rename = "SMS")]
    Sms,
}

/// Recognized compliance frameworks and identity standards for credential format abstraction
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ComplianceCode {
    #[serde(rename = "ICAO_DTC")]
    IcaoDtc,
    #[serde(rename = "ICAO_MRZ")]
    IcaoMrz,
    #[serde(rename = "AAMVA_MDL")]
    AamvaMdl,
    #[serde(rename = "EUDI_PID")]
    EudiPid,
    #[serde(rename = "EUDI_MDL")]
    EudiMdl,
    #[serde(rename = "OB3_JWT")]
    Ob3Jwt,
    #[serde(rename = "OB3_JSONLD")]
    Ob3Jsonld,
    #[serde(rename = "OB2_COMPATIBILITY")]
    Ob2Compatibility,
    #[serde(rename = "SD_JWT_VC")]
    SdJwtVc,
    #[serde(rename = "ENTERPRISE_VC")]
    EnterpriseVc,
    #[serde(rename = "OID4VC")]
    Oid4vc,
    #[serde(rename = "PEX")]
    Pex,
    #[serde(rename = "CUSTOM")]
    Custom,
}

/// Technical encoding formats for verifiable credentials
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum CredentialFormat {
    #[serde(rename = "MDOC")]
    Mdoc,
    #[serde(rename = "SD_JWT_VC")]
    SdJwtVc,
    #[serde(rename = "VC_JWT")]
    VcJwt,
    #[serde(rename = "JSON_LD")]
    JsonLd,
    #[serde(rename = "ZK_MDOC")]
    ZkMdoc,
}

/// When a wallet holds multiple credentials that satisfy a PresentationPolicy, this strategy determines which is preferred. Used in PresentationPolicy.credential_ranking_strategy.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum CredentialRankingStrategy {
    #[serde(rename = "FRESHEST_FIRST")]
    FreshestFirst,
    #[serde(rename = "HIGHEST_TRUST_FIRST")]
    HighestTrustFirst,
    #[serde(rename = "CUSTOM")]
    Custom,
}

/// Supported device platforms for Device Registration
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum DevicePlatform {
    #[serde(rename = "ios")]
    Ios,
    #[serde(rename = "android")]
    Android,
    #[serde(rename = "web")]
    Web,
}

/// Behavior when ZK circuit is unavailable for a predicate requirement
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum FallbackPolicy {
    #[serde(rename = "REQUIRE_PREDICATE")]
    RequirePredicate,
    #[serde(rename = "ACCEPT_RAW")]
    AcceptRaw,
    #[serde(rename = "DENY")]
    Deny,
}

/// Lifecycle status of a FlowInstance. Aligned with §9.9.2 state machine. Terminal states: COMPLETED, FAILED, EXPIRED, CANCELLED.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum FlowInstanceStatus {
    #[serde(rename = "PENDING")]
    Pending,
    #[serde(rename = "IN_PROGRESS")]
    InProgress,
    #[serde(rename = "AWAITING_APPROVAL")]
    AwaitingApproval,
    #[serde(rename = "AWAITING_WALLET")]
    AwaitingWallet,
    #[serde(rename = "AWAITING_EVIDENCE")]
    AwaitingEvidence,
    #[serde(rename = "COMPLETED")]
    Completed,
    #[serde(rename = "FAILED")]
    Failed,
    #[serde(rename = "EXPIRED")]
    Expired,
    #[serde(rename = "CANCELLED")]
    Cancelled,
}

/// Protocol-aligned flow types. Each type maps to a fixed ordered step sequence. Issuance and verification flows are separate; application_approval_issuance is the multi-step application workflow.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum FlowType {
    #[serde(rename = "oid4vci_pre_authorized")]
    Oid4vciPreAuthorized,
    #[serde(rename = "oid4vci_authorization_code")]
    Oid4vciAuthorizationCode,
    #[serde(rename = "mdl_issuance")]
    MdlIssuance,
    #[serde(rename = "oid4vp_presentation")]
    Oid4vpPresentation,
    #[serde(rename = "mdl_presentation")]
    MdlPresentation,
    #[serde(rename = "application_approval_issuance")]
    ApplicationApprovalIssuance,
    #[serde(rename = "credential_renewal")]
    CredentialRenewal,
    #[serde(rename = "credential_revocation")]
    CredentialRevocation,
    #[serde(rename = "combined")]
    Combined,
    #[serde(rename = "siopv2")]
    Siopv2,
}

/// Protocols used to deliver credentials from issuer to holder
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum IssuanceProtocol {
    #[serde(rename = "OID4VCI_PRE_AUTH")]
    Oid4vciPreAuth,
    #[serde(rename = "OID4VCI_AUTH_CODE")]
    Oid4vciAuthCode,
    #[serde(rename = "DIRECT")]
    Direct,
}

/// Network connectivity requirements for a Deployment Profile
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum NetworkMode {
    #[serde(rename = "ONLINE")]
    Online,
    #[serde(rename = "OFFLINE")]
    Offline,
    #[serde(rename = "HYBRID")]
    Hybrid,
}

/// Priority levels for notification delivery routing and FCM/APNs configuration
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum NotificationPriority {
    #[serde(rename = "LOW")]
    Low,
    #[serde(rename = "NORMAL")]
    Normal,
    #[serde(rename = "HIGH")]
    High,
    #[serde(rename = "CRITICAL")]
    Critical,
}

/// Types of zero-knowledge predicates supported in Presentation Policies
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum PredicateType {
    #[serde(rename = "RANGE_PROOF")]
    RangeProof,
    #[serde(rename = "MEMBERSHIP")]
    Membership,
    #[serde(rename = "EQUALITY")]
    Equality,
    #[serde(rename = "NON_MEMBERSHIP")]
    NonMembership,
    #[serde(rename = "INEQUALITY")]
    Inequality,
}

/// Behaviour when performing a revocation check during credential verification. Used in TrustProfile.revocation_policy.check_mode and OrganizationTrustProfile.revocation_policy.check_mode.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum RevocationCheckMode {
    #[serde(rename = "HARD_FAIL")]
    HardFail,
    #[serde(rename = "SOFT_FAIL")]
    SoftFail,
    #[serde(rename = "SKIP")]
    Skip,
}

/// Supported cryptographic credential revocation mechanisms
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum RevocationMechanism {
    #[serde(rename = "OCSP")]
    Ocsp,
    #[serde(rename = "CRL")]
    Crl,
    #[serde(rename = "STATUS_LIST_2021")]
    StatusList2021,
    #[serde(rename = "BITSTRING_STATUS_LIST")]
    BitstringStatusList,
    #[serde(rename = "TOKEN_STATUS_LIST")]
    TokenStatusList,
}

/// Standard reasons for revoking a credential or trust anchor. Aligned with RFC 5280 CRL reason codes and X.509 CRLReason extension.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum RevocationReason {
    #[serde(rename = "unspecified")]
    Unspecified,
    #[serde(rename = "key_compromise")]
    KeyCompromise,
    #[serde(rename = "ca_compromise")]
    CaCompromise,
    #[serde(rename = "affiliation_changed")]
    AffiliationChanged,
    #[serde(rename = "superseded")]
    Superseded,
    #[serde(rename = "cessation_of_operation")]
    CessationOfOperation,
    #[serde(rename = "certificate_hold")]
    CertificateHold,
    #[serde(rename = "privilege_withdrawn")]
    PrivilegeWithdrawn,
}

/// Check-timing behavior for revocation during credential verification. Used in RevocationProfile.check_mode. Distinct from RevocationCheckMode (revocation-check-modes.json) which governs failure behavior in TrustProfile.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum RevocationTimingMode {
    #[serde(rename = "ALWAYS")]
    Always,
    #[serde(rename = "CACHED")]
    Cached,
    #[serde(rename = "OFFLINE_GRACE")]
    OfflineGrace,
    #[serde(rename = "DISABLED")]
    Disabled,
}

/// Types of cryptographic trust material sources
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum TrustSourceType {
    #[serde(rename = "TRUST_LIST")]
    TrustList,
    #[serde(rename = "PINNED_ISSUER")]
    PinnedIssuer,
    #[serde(rename = "ROOT_CA")]
    RootCa,
    #[serde(rename = "PKD_URL")]
    PkdUrl,
}

/// Accepted cryptographic signature algorithms for credential signing and verification
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ValidationAlgorithm {
    #[serde(rename = "ES256")]
    Es256,
    #[serde(rename = "ES384")]
    Es384,
    #[serde(rename = "ES512")]
    Es512,
    #[serde(rename = "PS256")]
    Ps256,
    #[serde(rename = "PS384")]
    Ps384,
    #[serde(rename = "PS512")]
    Ps512,
    #[serde(rename = "EdDSA")]
    Eddsa,
    #[serde(rename = "RS256")]
    Rs256,
    #[serde(rename = "RS384")]
    Rs384,
    #[serde(rename = "RS512")]
    Rs512,
    #[serde(rename = "BBS_BLS12381_SHA256")]
    BbsBls12381Sha256,
    #[serde(rename = "BBS_BLS12381_SHAKE256")]
    BbsBls12381Shake256,
}

/// Registry of zero-knowledge circuit systems and their circuit identifiers accepted in PredicateSpec.supported_circuits. Each system defines a proof scheme, a circuit identification method, and the set of supported credential formats and predicate types.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ZkCircuitSystem {
    #[serde(rename = "longfellow-libzk-v1")]
    LongfellowLibzkV1,
}

