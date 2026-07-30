"""Public issuer selection is DID-only; custody remains implementation-private."""

import json

import pytest
from jsonschema import ValidationError

from .helpers import REPO_ROOT, validate_instance


SCHEMA = REPO_ROOT / "schemas" / "credential-template.json"
FORBIDDEN_PUBLIC_FIELDS = {
    "issuer_profile_id",
    "issuer_key_id",
    "issuer_algorithm",
    "key_access_mode",
    "issuer_certificate_chain_pem",
    "issuer_identity",
    "remote_key_binding",
    "remote_signing_config",
    "signing_service_id",
    "signing_key_reference",
    "kms_provider",
    "provider",
    "key_name",
    "key_version",
    "transit_mount",
    "auto_generate_artifacts",
}


def _property_names(value: object) -> set[str]:
    if isinstance(value, dict):
        result = set(value.get("properties", {}))
        for child in value.values():
            result.update(_property_names(child))
        return result
    if isinstance(value, list):
        result: set[str] = set()
        for child in value:
            result.update(_property_names(child))
        return result
    return set()


def _active_template() -> dict[str, object]:
    return {
        "id": "ct-did-only",
        "organization_id": "org-conformance",
        "name": "DID-only Credential Template",
        "credential_type": "ConformanceTestCredential",
        "compliance_profile_id": "cp-enterprise-vc",
        "credential_payload_format": "SD_JWT_VC",
        "vct": "ConformanceTestCredential",
        "issuer_did": "did:web:issuer.example.com",
        "validity_rules": {"ttl_seconds": 3600},
        "claims": [{"name": "test_claim", "type": "STRING", "required": True}],
        "status": "ACTIVE",
        "created_at": "2026-01-01T00:00:00Z",
    }


def test_public_credential_template_exposes_no_custody_selector() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    leaked = FORBIDDEN_PUBLIC_FIELDS & _property_names(schema)
    assert leaked == set()


def test_active_template_requires_only_public_issuer_did() -> None:
    validate_instance(SCHEMA, _active_template())


@pytest.mark.parametrize("field", sorted(FORBIDDEN_PUBLIC_FIELDS))
def test_public_template_rejects_every_private_custody_field(field: str) -> None:
    document = _active_template()
    document[field] = "private-selector"
    with pytest.raises(ValidationError):
        validate_instance(SCHEMA, document)


def test_active_template_without_issuer_did_fails_closed() -> None:
    document = _active_template()
    document.pop("issuer_did")
    with pytest.raises(ValidationError, match="issuer_did"):
        validate_instance(SCHEMA, document)
