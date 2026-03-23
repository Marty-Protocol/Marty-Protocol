# Credential Format Mapping

The MIP protocol defines **canonical format identifiers** (`CredentialFormat` enum) used in all protocol entities. When credentials traverse OID4VCI/OID4VP wire protocols, different format strings are used. This document specifies the normative mapping.

## Canonical Identifiers

| Protocol Value | Description |
|---|---|
| `MDOC` | ISO/IEC 18013-5 mDoc (CBOR-encoded mobile document) |
| `SD_JWT_VC` | IETF Selective Disclosure JWT Verifiable Credential |
| `VC_JWT` | W3C VC Data Model + JWT |
| `JSON_LD` | W3C VC with Linked Data Proof |
| `ZK_MDOC` | Zero-knowledge mDoc (experimental) |

## Wire Format Mapping

Implementations MUST use the canonical protocol identifiers in all MIP API requests and responses. When interacting with external systems (OID4VCI issuers, OID4VP verifiers), implementations MUST map to/from wire-format strings.

| Protocol | OID4VCI Wire Format | Legacy Aliases |
|---|---|---|
| `MDOC` | `mso_mdoc` | `mdoc` |
| `SD_JWT_VC` | `dc+sd-jwt` | `vc+sd-jwt`, `spruce-vc+sd-jwt`, `sd_jwt_vc`, `sd-jwt` |
| `VC_JWT` | `jwt_vc_json` | `jwt_vc`, `jwt_vc_json-ld` |
| `JSON_LD` | `ldp_vc` | — |
| `ZK_MDOC` | `zk_mdoc` | `zk-mdoc`, `zkp_mdoc` |

## Normalisation Rules

1. Wire format strings from external sources SHOULD be normalised to canonical identifiers at the system boundary (adapter/gateway layer).
2. The `wire_format_mapping` and `wire_format_aliases` sections in `enums/credential-formats.json` are the machine-readable source of truth for this mapping.
3. Normalisation MUST be case-insensitive.
4. Unknown wire strings SHOULD be rejected with a `400 Bad Request` error that lists the accepted values.

## Implementation Example

```python
from mip_types.enums import CredentialFormat

# Mapping from OID4VCI wire strings to protocol identifiers
WIRE_TO_PROTOCOL = {
    "mso_mdoc": CredentialFormat.MDOC,
    "mdoc": CredentialFormat.MDOC,
    "dc+sd-jwt": CredentialFormat.SD_JWT_VC,
    "vc+sd-jwt": CredentialFormat.SD_JWT_VC,
    "sd_jwt_vc": CredentialFormat.SD_JWT_VC,
    "jwt_vc_json": CredentialFormat.VC_JWT,
    "jwt_vc": CredentialFormat.VC_JWT,
    "ldp_vc": CredentialFormat.JSON_LD,
    "zk_mdoc": CredentialFormat.ZK_MDOC,
}

def normalise_format(wire: str) -> CredentialFormat:
    key = wire.lower().strip()
    if key not in WIRE_TO_PROTOCOL:
        raise ValueError(f"Unknown credential format: {wire!r}")
    return WIRE_TO_PROTOCOL[key]
```
