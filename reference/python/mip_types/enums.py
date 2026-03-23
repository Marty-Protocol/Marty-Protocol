"""MIP Protocol Enums — generated from marty-protocol/enums/*.json
Generated: 2026-03-15
DO NOT EDIT — regenerate with: python scripts/codegen.py python
"""
from enum import Enum


class ApiKeyScope(str, Enum):
    """Formal permission scope strings for MIP API keys. Scopes follow the pattern '{resource}:{action}'. Organization-scoped keys may hold any of these scopes. Deployment-scoped keys are restricted to a subset appropriate for a single deployment profile."""

    CREDENTIALS_ISSUE = "credentials:issue"
    CREDENTIALS_REVOKE = "credentials:revoke"
    CREDENTIALS_READ = "credentials:read"
    FLOWS_READ = "flows:read"
    FLOWS_WRITE = "flows:write"
    FLOWS_EXECUTE = "flows:execute"
    APPLICATIONS_READ = "applications:read"
    APPLICATIONS_WRITE = "applications:write"
    APPLICATIONS_APPROVE = "applications:approve"
    TRUST_READ = "trust:read"
    TRUST_WRITE = "trust:write"
    TRUST_ADMIN = "trust:admin"
    COMPLIANCE_READ = "compliance:read"
    COMPLIANCE_WRITE = "compliance:write"
    TEMPLATES_READ = "templates:read"
    TEMPLATES_WRITE = "templates:write"
    WALLET_READ = "wallet:read"
    WALLET_WRITE = "wallet:write"
    KEYS_READ = "keys:read"
    KEYS_WRITE = "keys:write"
    USERS_READ = "users:read"
    USERS_INVITE = "users:invite"
    ROLES_READ = "roles:read"
    ROLES_WRITE = "roles:write"
    AUDIT_READ = "audit:read"
    WEBHOOKS_READ = "webhooks:read"
    WEBHOOKS_WRITE = "webhooks:write"
    NOTIFICATIONS_SEND = "notifications:send"
    NOTIFICATIONS_READ = "notifications:read"
    DEPLOYMENT_READ = "deployment:read"
    DEPLOYMENT_WRITE = "deployment:write"
    ADMIN_FULL = "admin:full"


class ApprovalStrategy(str, Enum):
    """How credential applications are reviewed and approved"""

    AUTO = "AUTO"
    MANUAL = "MANUAL"
    RULES_BASED = "RULES_BASED"
    EXTERNAL = "EXTERNAL"


class ChannelType(str, Enum):
    """Notification delivery channel types"""

    FCM = "FCM"
    SSE = "SSE"
    WEBHOOK = "WEBHOOK"
    EMAIL = "EMAIL"
    SMS = "SMS"


class ComplianceCode(str, Enum):
    """Recognized compliance frameworks and identity standards for credential format abstraction"""

    ICAO_DTC = "ICAO_DTC"
    ICAO_MRZ = "ICAO_MRZ"
    AAMVA_MDL = "AAMVA_MDL"
    EUDI_PID = "EUDI_PID"
    EUDI_MDL = "EUDI_MDL"
    OB3_JWT = "OB3_JWT"
    OB3_JSONLD = "OB3_JSONLD"
    OB2_COMPATIBILITY = "OB2_COMPATIBILITY"
    SD_JWT_VC = "SD_JWT_VC"
    ENTERPRISE_VC = "ENTERPRISE_VC"
    OID4VC = "OID4VC"
    PEX = "PEX"
    CUSTOM = "CUSTOM"


class CredentialFormat(str, Enum):
    """Technical encoding formats for verifiable credentials"""

    MDOC = "MDOC"
    SD_JWT_VC = "SD_JWT_VC"
    VC_JWT = "VC_JWT"
    JSON_LD = "JSON_LD"
    ZK_MDOC = "ZK_MDOC"


class CredentialRankingStrategy(str, Enum):
    """When a wallet holds multiple credentials that satisfy a PresentationPolicy, this strategy determines which is preferred. Used in PresentationPolicy.credential_ranking_strategy."""

    FRESHEST_FIRST = "FRESHEST_FIRST"
    HIGHEST_TRUST_FIRST = "HIGHEST_TRUST_FIRST"
    CUSTOM = "CUSTOM"


class DevicePlatform(str, Enum):
    """Supported device platforms for Device Registration"""

    IOS = "ios"
    ANDROID = "android"
    WEB = "web"


class FallbackPolicy(str, Enum):
    """Behavior when ZK circuit is unavailable for a predicate requirement"""

    REQUIRE_PREDICATE = "REQUIRE_PREDICATE"
    ACCEPT_RAW = "ACCEPT_RAW"
    DENY = "DENY"


class FlowInstanceStatus(str, Enum):
    """Lifecycle status of a FlowInstance. Aligned with §9.9.2 state machine. Terminal states: COMPLETED, FAILED, EXPIRED, CANCELLED."""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    AWAITING_WALLET = "AWAITING_WALLET"
    AWAITING_EVIDENCE = "AWAITING_EVIDENCE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class FlowType(str, Enum):
    """Protocol-aligned flow types. Each type maps to a fixed ordered step sequence. Issuance and verification flows are separate; application_approval_issuance is the multi-step application workflow."""

    OID4VCI_PRE_AUTHORIZED = "oid4vci_pre_authorized"
    OID4VCI_AUTHORIZATION_CODE = "oid4vci_authorization_code"
    MDL_ISSUANCE = "mdl_issuance"
    OID4VP_PRESENTATION = "oid4vp_presentation"
    MDL_PRESENTATION = "mdl_presentation"
    APPLICATION_APPROVAL_ISSUANCE = "application_approval_issuance"
    CREDENTIAL_RENEWAL = "credential_renewal"
    CREDENTIAL_REVOCATION = "credential_revocation"
    COMBINED = "combined"
    SIOPV2 = "siopv2"


class IssuanceProtocol(str, Enum):
    """Protocols used to deliver credentials from issuer to holder"""

    OID4VCI_PRE_AUTH = "OID4VCI_PRE_AUTH"
    OID4VCI_AUTH_CODE = "OID4VCI_AUTH_CODE"
    DIRECT = "DIRECT"


class NetworkMode(str, Enum):
    """Network connectivity requirements for a Deployment Profile"""

    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    HYBRID = "HYBRID"


class NotificationPriority(str, Enum):
    """Priority levels for notification delivery routing and FCM/APNs configuration"""

    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class PredicateType(str, Enum):
    """Types of zero-knowledge predicates supported in Presentation Policies"""

    RANGE_PROOF = "RANGE_PROOF"
    MEMBERSHIP = "MEMBERSHIP"
    EQUALITY = "EQUALITY"
    NON_MEMBERSHIP = "NON_MEMBERSHIP"
    INEQUALITY = "INEQUALITY"


class RevocationCheckMode(str, Enum):
    """Behaviour when performing a revocation check during credential verification. Used in TrustProfile.revocation_policy.check_mode and OrganizationTrustProfile.revocation_policy.check_mode."""

    HARD_FAIL = "HARD_FAIL"
    SOFT_FAIL = "SOFT_FAIL"
    SKIP = "SKIP"


class RevocationMechanism(str, Enum):
    """Supported cryptographic credential revocation mechanisms"""

    OCSP = "OCSP"
    CRL = "CRL"
    STATUS_LIST_2021 = "STATUS_LIST_2021"
    BITSTRING_STATUS_LIST = "BITSTRING_STATUS_LIST"
    TOKEN_STATUS_LIST = "TOKEN_STATUS_LIST"


class RevocationReason(str, Enum):
    """Standard reasons for revoking a credential or trust anchor. Aligned with RFC 5280 CRL reason codes and X.509 CRLReason extension."""

    UNSPECIFIED = "unspecified"
    KEY_COMPROMISE = "key_compromise"
    CA_COMPROMISE = "ca_compromise"
    AFFILIATION_CHANGED = "affiliation_changed"
    SUPERSEDED = "superseded"
    CESSATION_OF_OPERATION = "cessation_of_operation"
    CERTIFICATE_HOLD = "certificate_hold"
    PRIVILEGE_WITHDRAWN = "privilege_withdrawn"


class RevocationTimingMode(str, Enum):
    """Check-timing behavior for revocation during credential verification. Used in RevocationProfile.check_mode. Distinct from RevocationCheckMode (revocation-check-modes.json) which governs failure behavior in TrustProfile."""

    ALWAYS = "ALWAYS"
    CACHED = "CACHED"
    OFFLINE_GRACE = "OFFLINE_GRACE"
    DISABLED = "DISABLED"


class TrustSourceType(str, Enum):
    """Types of cryptographic trust material sources"""

    TRUST_LIST = "TRUST_LIST"
    PINNED_ISSUER = "PINNED_ISSUER"
    ROOT_CA = "ROOT_CA"
    PKD_URL = "PKD_URL"


class ValidationAlgorithm(str, Enum):
    """Accepted cryptographic signature algorithms for credential signing and verification"""

    ES256 = "ES256"
    ES384 = "ES384"
    ES512 = "ES512"
    PS256 = "PS256"
    PS384 = "PS384"
    PS512 = "PS512"
    EDDSA = "EdDSA"
    RS256 = "RS256"
    RS384 = "RS384"
    RS512 = "RS512"
    BBS_BLS12381_SHA256 = "BBS_BLS12381_SHA256"
    BBS_BLS12381_SHAKE256 = "BBS_BLS12381_SHAKE256"


class ZkCircuitSystem(str, Enum):
    """Registry of zero-knowledge circuit systems and their circuit identifiers accepted in PredicateSpec.supported_circuits. Each system defines a proof scheme, a circuit identification method, and the set of supported credential formats and predicate types."""

    LONGFELLOW_LIBZK_V1 = "longfellow-libzk-v1"

