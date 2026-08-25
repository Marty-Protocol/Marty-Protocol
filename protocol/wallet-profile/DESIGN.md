# Wallet Profile - Design Notes

**Version:** 0.4.0

## Requirements Are Derived; Product Support Is Evidenced

Credential format, issuance protocol, and compliance profile determine what a wallet must implement. They do not determine which commercial product actually implements that combination for a given issuer, jurisdiction, platform, and date.

The derivation function therefore returns a requirements profile. Named wallet applications and platforms appear only when a versioned system record or organization override carries authoritative documentation and interoperability evidence.

## Why the Registry Exists

Wallet products and government enrollment programs change faster than protocol entities. The registry stores deployment-specific evidence and routing metadata without changing the meaning of the underlying credential profile.

An empty named-wallet result means "not verified," not "unsupported." This avoids both false promises and false negatives.

## Compliance Codes Narrow Requirements

The optional `compliance_profile_code` narrows the required document type, claims, trust framework, and protocol profile. It MUST NOT be used as a shortcut to label a wallet "certified." Certification or program approval is separate evidence.

## Platform and Route Boundaries

Platform support is reported only when covered by evidence. OID4VCI offer URIs, wallet-specific deep links, Digital Credentials API routes, and ISO/IEC 18013-5 device engagement are distinct mechanisms and must remain distinct in the registry.
