import json

import pytest
from jsonschema import ValidationError

from .helpers import SCHEMAS_DIR, validate_instance


def test_holder_binding_policy_requires_control_profile_and_freshness() -> None:
    policy = json.loads(
        (SCHEMAS_DIR.parent / "conformance" / "valid" / "presentation-policy.json").read_text()
    )
    policy["holder_binding"] = {
        "required": True,
        "binding_methods": ["CREDENTIAL_KEY"],
        "proof_profiles": ["SD_JWT_KEY_BINDING"],
        "proof_freshness": {
            "challenge_required": True,
            "audience_binding_required": True,
            "replay_detection_required": True,
        },
    }

    validate_instance(SCHEMAS_DIR / "presentation-policy.json", policy)


@pytest.mark.parametrize("obsolete_field", ["nonce_required", "NONCE"])
def test_draft_era_nonce_binding_is_rejected(obsolete_field: str) -> None:
    policy = json.loads(
        (SCHEMAS_DIR.parent / "conformance" / "valid" / "presentation-policy.json").read_text()
    )
    policy["holder_binding"] = {
        "required": True,
        "binding_methods": ["CREDENTIAL_KEY"],
        "proof_profiles": ["SD_JWT_KEY_BINDING"],
        "proof_freshness": {
            "challenge_required": True,
            "audience_binding_required": True,
            "replay_detection_required": True,
        },
    }
    if obsolete_field == "nonce_required":
        policy["holder_binding"][obsolete_field] = True
    else:
        policy["holder_binding"]["binding_methods"] = [obsolete_field]

    with pytest.raises(ValidationError):
        validate_instance(SCHEMAS_DIR / "presentation-policy.json", policy)


def test_oid4vci_nonce_messages() -> None:
    validate_instance(SCHEMAS_DIR / "oid4vci-nonce-request.json", {})
    validate_instance(
        SCHEMAS_DIR / "oid4vci-nonce-response.json",
        {"c_nonce": "a-cryptographically-random-nonce"},
    )


def test_nonce_request_rejects_body_fields() -> None:
    with pytest.raises(ValidationError):
        validate_instance(
            SCHEMAS_DIR / "oid4vci-nonce-request.json",
            {"access_token": "must-not-be-sent"},
        )


def test_deployment_profile_accepts_only_one_biometric_field() -> None:
    profile = json.loads(
        (SCHEMAS_DIR.parent / "conformance" / "valid" / "deployment-profile.json").read_text()
    )
    profile["operator_biometric_authentication_required"] = True
    validate_instance(SCHEMAS_DIR / "deployment-profile.json", profile)

    profile["biometric_required"] = True
    with pytest.raises(ValidationError):
        validate_instance(SCHEMAS_DIR / "deployment-profile.json", profile)
