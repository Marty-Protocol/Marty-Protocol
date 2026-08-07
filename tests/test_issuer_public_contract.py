"""Issuer trust records and public signing identities stay distinct."""

import copy

import pytest
from jsonschema import ValidationError

from .helpers import REPO_ROOT, validate_instance


ISSUER_ENTITY = REPO_ROOT / "schemas" / "issuer-entity.json"
ISSUER_ENTITY_CREATE = REPO_ROOT / "schemas" / "issuer-entity-create-request.json"
ISSUER_ENTITY_UPDATE = REPO_ROOT / "schemas" / "issuer-entity-update-request.json"
ISSUER_IDENTITY = REPO_ROOT / "schemas" / "issuer-identity.json"
ISSUER_IDENTITY_LIST = REPO_ROOT / "schemas" / "issuer-identity-list-response.json"
ISSUER_IDENTITY_CREATE = REPO_ROOT / "schemas" / "issuer-identity-create-request.json"
ISSUER_IDENTITY_OPERATION = REPO_ROOT / "schemas" / "issuer-identity-operation-request.json"
ISSUER_IDENTITY_CERTIFICATE = REPO_ROOT / "schemas" / "issuer-identity-certificate-request.json"
ISSUER_IDENTITY_CREATE_RESPONSE = REPO_ROOT / "schemas" / "issuer-identity-create-response.json"
ISSUER_IDENTITY_DELETE_RESPONSE = REPO_ROOT / "schemas" / "issuer-identity-delete-response.json"

FORBIDDEN_CUSTODY_FIELDS = {
    "issuer_algorithm",
    "issuer_profile_id",
    "issuer_key_id",
    "key_access_mode",
    "key_binding",
    "key_management",
    "verification_method_id",
    "signing_service_id",
    "signing_key_reference",
    "key_reference",
    "kms_arn",
    "kms_provider",
    "kms_region",
    "managed_key_id",
    "provider",
    "service_id",
    "signing_agent_auth",
    "signing_agent_url",
    "key_name",
    "key_version",
    "transit_mount",
}


def _entity() -> dict:
    return {
        "id": "10000000-0000-4000-8000-000000000001",
        "organization_id": "20000000-0000-4000-8000-000000000001",
        "issuer_id": "did:web:issuer.example",
        "issuer_type": "ORGANIZATION",
        "display_name": "Example Issuer",
        "description": "Tenant trust-registry entry",
        "is_system_issuer": False,
        "compliance_status": "COMPLIANT",
        "accreditation_body": None,
        "accreditation_date": None,
        "valid_from": "2026-08-01T00:00:00Z",
        "valid_until": None,
        "trust_anchor_id": None,
        "revoked_at": None,
        "revocation_reason": None,
        "revoked_by": None,
        "metadata": {"jurisdiction": "US", "labels": ["education"]},
        "created_at": "2026-08-01T00:00:00Z",
        "updated_at": "2026-08-01T00:00:00Z",
    }


def _create() -> dict:
    return {
        "organization_id": "20000000-0000-4000-8000-000000000001",
        "issuer_id": "did:web:issuer.example",
        "issuer_type": "ORGANIZATION",
        "display_name": "Example Issuer",
        "metadata": {"jurisdiction": "US"},
    }


def _identity() -> dict:
    return {
        "issuer_did": "did:web:issuer.example",
        "key_purpose": "vc_jwt_issuer",
        "credential_format": "SD_JWT_VC",
        "algorithm": "ES256",
        "status": "active",
    }


def _identity_operation() -> dict:
    return {
        "organization_id": "org-conformance",
        "issuer_did": "did:web:issuer.example",
        "key_purpose": "vc_jwt_issuer",
        "credential_format": "SD_JWT_VC",
        "algorithm": "ES256",
    }


def test_issuer_entity_resource_and_operations_validate() -> None:
    validate_instance(ISSUER_ENTITY, _entity())
    validate_instance(ISSUER_ENTITY_CREATE, _create())
    validate_instance(
        ISSUER_ENTITY_UPDATE,
        {
            "organization_id": "20000000-0000-4000-8000-000000000001",
            "display_name": "Updated Issuer",
        },
    )


def test_public_create_cannot_claim_global_or_system_issuer_authority() -> None:
    for field, value in (
        ("is_system_issuer", True),
        ("revoked_by", "operator-subject"),
    ):
        request = _create()
        request[field] = value
        with pytest.raises(ValidationError):
            validate_instance(ISSUER_ENTITY_CREATE, request)

    missing_scope = _create()
    missing_scope.pop("organization_id")
    with pytest.raises(ValidationError):
        validate_instance(ISSUER_ENTITY_CREATE, missing_scope)


@pytest.mark.parametrize("field", sorted(FORBIDDEN_CUSTODY_FIELDS))
def test_entity_metadata_rejects_custody_selectors_at_every_depth(field: str) -> None:
    for schema, document in (
        (ISSUER_ENTITY, _entity()),
        (ISSUER_ENTITY_CREATE, _create()),
    ):
        nested = copy.deepcopy(document)
        nested["metadata"] = {"public": {"nested": [{field: "private"}]}}
        with pytest.raises(ValidationError):
            validate_instance(schema, nested)


def test_revocation_is_server_attributed_and_requires_a_reason() -> None:
    request = {
        "organization_id": "20000000-0000-4000-8000-000000000001",
        "compliance_status": "REVOKED",
    }
    with pytest.raises(ValidationError):
        validate_instance(ISSUER_ENTITY_UPDATE, request)

    request["revocation_reason"] = "Accreditation withdrawn"
    validate_instance(ISSUER_ENTITY_UPDATE, request)

    request["revoked_by"] = "forged-operator"
    with pytest.raises(ValidationError):
        validate_instance(ISSUER_ENTITY_UPDATE, request)


def test_public_issuer_identity_contains_no_custody_coordinates() -> None:
    identity = _identity()
    validate_instance(ISSUER_IDENTITY, identity)
    validate_instance(ISSUER_IDENTITY_LIST, {"identities": [identity]})

    for field in FORBIDDEN_CUSTODY_FIELDS:
        private = dict(identity)
        private[field] = "private"
        with pytest.raises(ValidationError):
            validate_instance(ISSUER_IDENTITY, private)


def test_public_issuer_identity_lifecycle_is_did_first_and_provider_neutral() -> None:
    operation = _identity_operation()
    identity = _identity()
    validate_instance(ISSUER_IDENTITY_CREATE, operation)
    validate_instance(ISSUER_IDENTITY_OPERATION, operation)
    validate_instance(
        ISSUER_IDENTITY_CERTIFICATE,
        {**operation, "cert_pem": "-----BEGIN CERTIFICATE-----\nAA==\n-----END CERTIFICATE-----"},
    )
    validate_instance(
        ISSUER_IDENTITY_CREATE_RESPONSE,
        {"identity": identity, "created": True},
    )
    validate_instance(ISSUER_IDENTITY_DELETE_RESPONSE, {"deleted": identity})

    validate_instance(
        ISSUER_IDENTITY_CREATE,
        {
            **operation,
            "key_attestation_policy": {
                "mode": "required",
                "trusted_root_certificates_pem": ["public test root"],
                "allowed_algorithms": ["ES256"],
                "status_validation": "disabled",
            },
        },
    )


@pytest.mark.parametrize("field", sorted(FORBIDDEN_CUSTODY_FIELDS))
def test_public_issuer_identity_lifecycle_rejects_custody_selectors(field: str) -> None:
    for schema in (ISSUER_IDENTITY_CREATE, ISSUER_IDENTITY_OPERATION):
        request = _identity_operation()
        request[field] = "private"
        with pytest.raises(ValidationError):
            validate_instance(schema, request)


def test_public_issuer_identity_lifecycle_requires_complete_resolution_tuple() -> None:
    for field in (
        "organization_id",
        "issuer_did",
        "key_purpose",
        "credential_format",
        "algorithm",
    ):
        request = _identity_operation()
        request.pop(field)
        with pytest.raises(ValidationError):
            validate_instance(ISSUER_IDENTITY_OPERATION, request)


def test_issuer_identity_rejects_non_did_inactive_and_unknown_purpose() -> None:
    for updates in (
        {"issuer_did": "https://issuer.example"},
        {"status": "draft"},
        {"key_purpose": "arbitrary"},
        {"algorithm": "none"},
    ):
        identity = _identity()
        identity.update(updates)
        with pytest.raises(ValidationError):
            validate_instance(ISSUER_IDENTITY, identity)


def test_generated_bindings_keep_trust_entities_and_did_identities_distinct() -> None:
    python = (REPO_ROOT / "reference/python/mip_types/models.py").read_text(
        encoding="utf-8"
    )
    rust = (REPO_ROOT / "reference/rust/src/models.rs").read_text(encoding="utf-8")
    typescript = (REPO_ROOT / "reference/typescript/src/models.ts").read_text(
        encoding="utf-8"
    )

    assert "class IssuerEntityCreateRequest(BaseModel):" in python
    assert "class IssuerEntityUpdateRequest(BaseModel):" in python
    assert "class IssuerIdentity(BaseModel):" in python
    assert "class IssuerIdentityCreateRequest(BaseModel):" in python
    assert "class IssuerIdentityOperationRequest(BaseModel):" in python
    assert 'status: Literal["active"]' in python

    assert "pub struct IssuerEntityCreateRequest {" in rust
    assert "pub struct IssuerEntityUpdateRequest {" in rust
    assert "pub struct IssuerIdentity {" in rust
    assert "pub struct IssuerIdentityCreateRequest {" in rust
    assert "pub struct IssuerIdentityOperationRequest {" in rust
    assert "pub status: String," in rust

    assert "export interface IssuerEntityCreateRequest {" in typescript
    assert "export interface IssuerEntityUpdateRequest {" in typescript
    assert "export interface IssuerIdentity {" in typescript
    assert "export interface IssuerIdentityCreateRequest {" in typescript
    assert "export interface IssuerIdentityOperationRequest {" in typescript
    assert "status: 'active';" in typescript
