"""MIP-owned tests for the public Organization resource and operations."""

import copy
import json

import pytest
from jsonschema import ValidationError

from .helpers import REPO_ROOT, validate_instance


RESOURCE_SCHEMA = REPO_ROOT / "schemas" / "organization.json"
CREATE_SCHEMA = REPO_ROOT / "schemas" / "organization-create-request.json"
UPDATE_SCHEMA = REPO_ROOT / "schemas" / "organization-update-request.json"


def _organization() -> dict:
    return {
        "id": "20000000-0000-4000-8000-000000000001",
        "name": "example-issuer",
        "display_name": "Example Issuer",
        "description": "Example tenant",
        "join_code": None,
        "visibility": "PUBLIC",
        "owner_id": "owner-subject",
        "status": "active",
        "org_type": "enterprise",
        "join_mechanism": "open",
        "requires_approval": True,
        "is_discoverable": True,
        "contact_email": "operator@example.com",
        "contact_phone": None,
        "website": "https://example.com",
        "membership": {
            "roles": [
                {
                    "id": "role-owner",
                    "name": "owner",
                    "display_name": "Owner",
                }
            ],
            "status": "active",
            "permissions": ["organization:edit"],
            "has_org_console_access": True,
            "is_owner": True,
            "joined_at": "2026-07-31T00:00:00Z",
        },
        "created_at": "2026-07-31T00:00:00Z",
        "updated_at": "2026-07-31T00:00:00Z",
    }


def test_organization_resource_carries_discovery_and_admission_semantics() -> None:
    validate_instance(RESOURCE_SCHEMA, _organization())


def test_private_organization_cannot_claim_discoverability() -> None:
    organization = _organization()
    organization["visibility"] = "PRIVATE"
    with pytest.raises(ValidationError):
        validate_instance(RESOURCE_SCHEMA, organization)


def test_resource_rejects_internal_and_custody_fields() -> None:
    for field in (
        "issuer_profile_id",
        "signing_service_id",
        "key_reference",
        "kms_provider",
        "settings",
        "plan",
    ):
        organization = copy.deepcopy(_organization())
        organization[field] = "private-selector"
        with pytest.raises(ValidationError):
            validate_instance(RESOURCE_SCHEMA, organization)


def test_schema_declares_exact_public_resource_fields() -> None:
    schema = json.loads(RESOURCE_SCHEMA.read_text(encoding="utf-8"))
    assert set(schema["properties"]) == set(_organization())


def test_create_operation_is_strict_and_persists_public_join_semantics() -> None:
    validate_instance(
        CREATE_SCHEMA,
        {
            "name": "example-issuer",
            "display_name": "Example Issuer",
            "description": "Example tenant",
            "org_type": "healthcare",
            "contact_email": "operator@example.com",
            "visibility": "PUBLIC",
            "join_mechanism": "open",
            "requires_approval": True,
        },
    )


def test_open_create_requires_public_visibility() -> None:
    with pytest.raises(ValidationError):
        validate_instance(
            CREATE_SCHEMA,
            {
                "name": "example-issuer",
                "display_name": "Example Issuer",
                "visibility": "PRIVATE",
                "join_mechanism": "open",
            },
        )


def test_create_rejects_unknown_and_internal_fields() -> None:
    for field in ("jurisdiction", "membership_mode", "issuer_profile_id"):
        request = {
            "name": "example-issuer",
            "display_name": "Example Issuer",
            field: "must-not-pass",
        }
        with pytest.raises(ValidationError):
            validate_instance(CREATE_SCHEMA, request)


def test_update_is_tenant_bound_partial_and_strict() -> None:
    validate_instance(
        UPDATE_SCHEMA,
        {
            "organization_id": "20000000-0000-4000-8000-000000000001",
            "display_name": "Updated Example Issuer",
            "contact_email": None,
        },
    )

    for request in (
        {"display_name": "Missing tenant"},
        {"organization_id": "20000000-0000-4000-8000-000000000001"},
        {
            "organization_id": "20000000-0000-4000-8000-000000000001",
            "settings": {"private": True},
        },
    ):
        with pytest.raises(ValidationError):
            validate_instance(UPDATE_SCHEMA, request)
