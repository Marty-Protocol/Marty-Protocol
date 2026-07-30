"""MIP-owned tests for the public Presentation Policy resource contract."""

import copy
import json

import pytest
from jsonschema import ValidationError

from .helpers import REPO_ROOT, validate_instance


SCHEMA = REPO_ROOT / "schemas" / "presentation-policy.json"
CREATE_SCHEMA = (
    REPO_ROOT / "schemas" / "presentation-policy-create-request.json"
)
UPDATE_SCHEMA = (
    REPO_ROOT / "schemas" / "presentation-policy-update-request.json"
)


def _policy() -> dict:
    return {
        "id": "policy-conformance",
        "organization_id": "org-conformance",
        "name": "Employee verification",
        "status": "draft",
        "description": "Verify a current employee credential.",
        "purpose": "Workforce access",
        "required_claims": [
            {
                "claim_name": "employee_id",
                "credential_type": "EmployeeCredential",
            }
        ],
        "accepted_credential_types": ["EmployeeCredential"],
        "display_metadata": {
            "title": "Employee verification",
            "description": "Present an employee credential.",
            "purpose": "employment_verification",
            "purpose_description": "Workforce access",
            "verifier_name": "Example verifier",
            "verifier_logo_url": None,
            "privacy_policy_url": None,
            "terms_of_service_url": None,
        },
        "credential_requirements": [
            {
                "credential_template_id": "template-employee",
                "display_name": "Employee credential",
                "description": None,
                "required": True,
                "credential_payload_format": "SD_JWT_VC",
                "requested_claims": [
                    {
                        "claim_name": "employee_id",
                        "display_name": "Employee ID",
                        "description": None,
                        "required": True,
                        "selective_disclosure": True,
                        "accept_derived": True,
                        "predicate_spec": None,
                        "constraints": [],
                    }
                ],
                "trust_profile_id": "trust-workforce",
                "max_age_seconds": 86400,
                "require_fresh_issuance": False,
            }
        ],
        "alternative_requirements": [],
        "compliance_profile_id": "compliance-workforce",
        "trust_profile_id": "trust-workforce",
        "holder_binding": {
            "required": True,
            "binding_methods": ["CREDENTIAL_KEY"],
            "proof_profiles": ["SD_JWT_KEY_BINDING"],
            "proof_freshness": {
                "challenge_required": True,
                "audience_binding_required": True,
                "replay_detection_required": True,
            },
        },
        "freshness": {
            "max_age_seconds": 86400,
            "require_not_revoked": True,
            "revocation_grace_seconds": 0,
        },
        "prefer_predicates": False,
        "supported_circuits": [],
        "fallback_policy": "ACCEPT_RAW",
        "issuer_constraints": {
            "min_trust_level": 80,
            "required_compliance_statuses": ["COMPLIANT"],
            "required_accreditations": [],
        },
        "credential_ranking_strategy": "FRESHEST_FIRST",
        "credential_ranking_weights": None,
        "version": 1,
        "created_at": "2026-07-30T00:00:00Z",
        "updated_at": "2026-07-30T00:00:00Z",
    }


def test_template_bound_presentation_policy_is_a_public_protocol_resource() -> None:
    validate_instance(SCHEMA, _policy())


def test_policy_can_express_alternative_template_requirements() -> None:
    policy = _policy()
    requirement = policy["credential_requirements"][0]
    policy["required_claims"] = []
    policy["credential_requirements"] = []
    policy["alternative_requirements"] = [
        {
            "name": "Employee identity",
            "description": "Accept either supported employee credential.",
            "credential_requirements": [requirement],
            "min_satisfied": 1,
        }
    ]
    validate_instance(SCHEMA, policy)


def test_policy_without_any_requirement_fails_closed() -> None:
    policy = _policy()
    policy["required_claims"] = []
    policy["credential_requirements"] = []
    policy["alternative_requirements"] = []
    with pytest.raises(ValidationError):
        validate_instance(SCHEMA, policy)


@pytest.mark.parametrize(
    "field",
    [
        "issuer_profile_id",
        "signing_service_id",
        "key_reference",
        "kms_provider",
    ],
)
def test_policy_rejects_custody_and_internal_routing_fields(field: str) -> None:
    policy = copy.deepcopy(_policy())
    policy[field] = "private-selector"
    with pytest.raises(ValidationError):
        validate_instance(SCHEMA, policy)


def test_schema_declares_exact_public_resource_fields() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert set(schema["properties"]) == set(_policy())


def _create_request() -> dict:
    policy = _policy()
    for field in (
        "id",
        "status",
        "version",
        "created_at",
        "updated_at",
    ):
        policy.pop(field)
    return policy


def test_create_request_preserves_template_bound_public_semantics() -> None:
    validate_instance(CREATE_SCHEMA, _create_request())


def test_create_request_rejects_unknown_and_custody_fields() -> None:
    for field in ("unmodeled_field", "issuer_profile_id", "kms_provider"):
        request = _create_request()
        request[field] = "must-not-pass"
        with pytest.raises(ValidationError):
            validate_instance(CREATE_SCHEMA, request)


def test_create_request_requires_at_least_one_requirement_form() -> None:
    request = _create_request()
    request["required_claims"] = []
    request["credential_requirements"] = []
    request["alternative_requirements"] = []
    with pytest.raises(ValidationError):
        validate_instance(CREATE_SCHEMA, request)


def test_update_request_is_tenant_scoped_and_partial() -> None:
    validate_instance(
        UPDATE_SCHEMA,
        {
            "organization_id": "org-conformance",
            "name": "Updated policy",
            "credential_requirements": _create_request()[
                "credential_requirements"
            ],
        },
    )


def test_update_request_rejects_missing_tenant_or_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        validate_instance(UPDATE_SCHEMA, {"name": "No tenant"})

    with pytest.raises(ValidationError):
        validate_instance(
            UPDATE_SCHEMA,
            {
                "organization_id": "org-conformance",
                "signing_service_id": "private-selector",
            },
        )
