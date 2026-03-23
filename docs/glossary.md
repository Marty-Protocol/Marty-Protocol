# MIP Glossary

Definitions for terms used throughout the Marty Identity Protocol specification.

---

## A

**Accepted Algorithm**
An algorithm enumerated in a Trust Profile's `accepted_algorithms` field. Credentials signed with algorithms not in this list MUST be rejected.

**Age Attestation**
A cryptographic claim indicating that the holder meets an age threshold (e.g., `age_over_21: true`) without disclosing the holder's actual date of birth. Implemented via ISO 18013-5 age elements or SD-JWT-VC boolean claims with ZK predicates.

**Application Template**
A MIP protocol entity that defines the user-facing workflow for applying for a credential — fields, evidence requirements, UX metadata, and approval routing — independently of the cryptographic specification.

**Approval Strategy**
The method by which a credential issuance request is reviewed. One of `AUTO` (immediate), `MANUAL` (human reviewer), `RULES_BASED` (Cedar PolicySet evaluation), or `EXTERNAL` (delegated to an external system).

---

## C

**Cedar**
An open-source policy language created by Amazon for authorization decisions. MIP uses Cedar to express access control, credential verification trust, and approval rules via PolicySet entities. Cedar policies are deny-by-default, statically analyzable, and formally verifiable.

**Cedar Policy**
A single `permit` or `forbid` rule written in the Cedar language. A policy evaluates a principal, action, resource, and context to determine whether an operation is allowed or denied. Contained within a PolicySet.

**Claim**
A named attribute within a credential. In SD-JWT-VC, claims may be selectively disclosable. In mDoc, claims are organized into namespaces.

**Compliance Code**
A standardized identifier (`ICAO_DTC`, `AAMVA_MDL`, `EUDI_PID`, `EUDI_MDL`, `ENTERPRISE_VC`, etc.) that anchors a Credential Template or Compliance Profile to a specific identity standard.

**Compliance Profile**
A MIP protocol entity encoding the mandatory claim set, algorithm requirements, key requirements, and revocation constraints for a specific identity standard. System Compliance Profiles are immutable.

**Credential Template**
A MIP protocol entity that fully specifies how to issue a single credential type — its claim schema, cryptographic parameters, issuance protocol, compliance anchor, and lifecycle behavior.

**Credential Type**
A PascalCase string (e.g., `PreBoardingClearance`, `EmployeeAccessBadge`) that uniquely names a credential Schema within an organization.

---

## D

**Deployment Profile**
A MIP protocol entity that configures how and where credential verification occurs — network mode, device lanes, trust profile reference, and associated presentation policies.

**Derived Entity**
An entity whose state is computed from other stored entities at query time rather than being persisted independently. See: Wallet Profile.

**Device Registration**
A MIP protocol entity recording a mobile device's push notification token, platform, and optional cryptographic public key for challenge-response authentication.

---

## F

**Fallback Policy**
The action a verifier takes when a wallet cannot satisfy a predicate request. One of `REQUIRE_PREDICATE` (no fallback), `ACCEPT_RAW` (accept the raw claim value), or `DENY` (reject the presentation).

**FCM (Firebase Cloud Messaging)**
Google's push notification service. Used in MIP for delivering OID4VCI offer URIs to Android and iOS devices. Credential data MUST NOT be included in FCM payloads.

**Flow**
A MIP protocol entity that orchestrates a complete identity workflow by linking Credential Templates, Presentation Policies, and Deployment Profiles. Flow types: `ISSUANCE`, `VERIFICATION`, `COMBINED`.

**Freshness**
The temporal validity requirement for a presented credential. Defined in Presentation Policy as `max_age_seconds` and `require_not_revoked`.

---

## H

**Holder Binding**
Cryptographic proof that the credential presenter is the same entity to which the credential was issued. Implemented via device key proof or nonce-based challenge-response. Configurable per Presentation Policy.

**HYBRID (Network Mode)**
A Deployment Profile network mode where online connectivity is preferred but offline operation is tolerated up to `offline_tolerance_seconds`.

---

## I

**ICAO PKD (Public Key Directory)**
The International Civil Aviation Organization's central repository of Document Signing Certificates and Country Signing CA Certificates used to verify ICAO travel documents.

**Immutable**
A Compliance Profile state indicating it cannot be modified after being referenced by an active Credential Template. All system-defined Compliance Profiles are permanently immutable.

**Issuance Protocol**
The protocol used to deliver a credential to a wallet. One of `OID4VCI_PRE_AUTH` (pre-authorized code), `OID4VCI_AUTH_CODE` (authorization code), or `DIRECT`.

---

## J

**JWK Thumbprint**
An RFC 7638 SHA-256 digest of the canonical JSON representation of a JWK. Used in MIP as the `public_key_kid` for Device Registration public keys.

---

## K

**Key Mode**
The security environment for a credential signing key. One of `SOFTWARE` (in-process), `HSM` (Hardware Security Module), or `EXTERNAL` (externally-issued credential, key not held by this platform).

**Key Version**
An integer counter on a Device Registration that increments on each key rotation event. Used to order rotations and detect replay attacks.

---

## L

**Lane**
An operational subdivision of a Deployment Profile representing a physical or logical channel (e.g., a specific gate, checkout lane, or device group) with its own device list and policy reference.

---

## M

**mDoc**
The ISO 18013-5 mobile Document format. A CBOR-encoded credential used for mDL, DTC, and other standards-based physical-identity credentials.

**MIP (Marty Identity Protocol)**
This protocol — the full set of entity definitions, API surface, validation rules, and governance rules defined in this repository.

---

## N

**Namespace**
In mDoc credentials, a string identifier (e.g., `org.iso.18013.5.1`) that groups a set of related claims. Different namespaces within a single mDoc document may be issued by different authorities.

**Notification Target**
A MIP protocol entity recording user delivery channel preferences — FCM device IDs, SSE subscriptions, webhook endpoints, email addresses, and phone numbers.

---

## O

**OID4VCI (OpenID for Verifiable Credential Issuance)**
The IETF/OpenID Foundation protocol specification for credential issuance. MIP supports the `pre-authorized_code` and `authorization_code` grant flows.

**OID4VP (OpenID for Verifiable Presentations)**
The IETF/OpenID Foundation protocol specification for credential presentation and verification. Used on the verifier side to request and receive credentials from wallets.

**Offer URI**
An OID4VCI deep link URI (`openid-credential-offer://...`) that a wallet opens to initiate a pre-authorized code exchange. The only credential-adjacent data permitted in notification payloads.

---

## P

**Policy Set**
A MIP protocol entity that stores one or more Cedar authorization policies. PolicySets are typed (`ACCESS_CONTROL`, `CREDENTIAL_VERIFICATION`, `APPROVAL_RULES`, `CUSTOM`) and referenced by Trust Profiles, Compliance Profiles, Application Templates, and SCIM Roles. Cedar policies within a PolicySet are evaluated with deny-by-default semantics.

**Policy Type**
The authorization domain of a PolicySet. One of `ACCESS_CONTROL` (API authorization), `CREDENTIAL_VERIFICATION` (trust evaluation rules), `APPROVAL_RULES` (application approval decisions), or `CUSTOM` (organization-defined).

**Predicate**
A privacy-preserving constraint on a claim value that allows verification of a property (e.g., `age >= 21`) without disclosing the underlying value (e.g., date of birth). MIP predicate types: `RANGE_PROOF`, `EQUALITY`, `INEQUALITY`, `MEMBERSHIP`, `NON_MEMBERSHIP`.

**Presentation Policy**
A MIP protocol entity defining the minimum set of claims a verifier requires from a holder, including predicate preferences, holder binding requirements, and freshness constraints.

---

## R

**Revocation Profile**
A MIP protocol entity that specifies the revocation method, check mode, cache TTL, and offline tolerance for a credential type. Configured independently for issuer and verifier.

**Revocation Grace**
The maximum time a cached revocation status is trusted in the absence of connectivity. Defined as `offline_grace_seconds` in the Revocation Profile verifier config.

---

## S

**SD-JWT-VC**
Selective Disclosure JWT Verifiable Credential — IETF draft `draft-ietf-oauth-sd-jwt-vc`. A JWT-based credential format supporting selective disclosure of individual claims.

**Selective Disclosure**
A cryptographic mechanism allowing a holder to reveal only chosen claims from a credential without invalidating the issuer's signature over undisclosed claims.

**SSE (Server-Sent Events)**
An HTTP/1.1 push mechanism for delivering real-time messages from server to browser. Used in MIP for web wallet credential delivery as an alternative to FCM.

**Stability Tier**
A classification of protocol entities by their expected rate of change and governance requirements. See `VERSIONING.md` for full stability tier definitions.

---

## T

**Trust Profile**
A MIP protocol entity that specifies what cryptographic trust roots are accepted, which credential formats and algorithms are valid, and how revocation must be checked.

**Trust Source**
An element within a Trust Profile that defines a single trust anchor — one of `TRUST_LIST` (URL), `PINNED_ISSUER` (DID), `ROOT_CA` (certificate), or `PKD_URL` (ICAO PKD).

---

## V

**Validator**
The strictness level for credential validation in a Trust Profile. `COMPLIANT` (strict, all rules enforced), `NEEDS_ATTENTION` (warnings only), `SETUP_REQUIRED` (not yet fully configured).

---

## W

**Wallet**
A software application that stores, manages, and presents verifiable credentials on behalf of a holder. Wallets may be mobile apps, web applications, or hardware devices.

**Wallet Profile**
A MIP derived entity (not stored) describing the credential formats, issuance protocols, and compliance codes a specific wallet application supports. Derived at query time from the `(credential_format, issuance_protocol, compliance_code)` combination.

**Webhook**
An HTTPS endpoint to which MIP delivers notification payloads via HTTP POST. Signed with HMAC-SHA256 using a pre-shared secret for authenticity verification.
