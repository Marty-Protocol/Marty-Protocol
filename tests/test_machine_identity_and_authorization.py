"""Machine identity, binding, attestation, and decision-receipt invariants."""

from __future__ import annotations

import json

import pytest
from jsonschema import ValidationError

from .helpers import REPO_ROOT, SCHEMAS_DIR, validate_instance
from .test_flow_contract import _validate_extension_graph


def _valid(name: str) -> dict:
    return json.loads((REPO_ROOT / "conformance" / "valid" / name).read_text())


def test_managed_machine_contracts_validate() -> None:
    validate_instance(SCHEMAS_DIR / "machine-identity.json", _valid("machine-identity.json"))
    validate_instance(
        SCHEMAS_DIR / "machine-authentication-policy.json",
        _valid("machine-authentication-policy.json"),
    )
    validate_instance(
        SCHEMAS_DIR / "authorization-decision-receipt.json",
        _valid("authorization-decision-receipt.json"),
    )


def test_machine_authentication_flow_is_a_presentation_extension() -> None:
    flow = _valid("flow-machine-authentication.json")
    validate_instance(SCHEMAS_DIR / "flow.json", flow)
    _validate_extension_graph(flow["extension"])

    assert flow["flow_type"] == "custom"
    assert flow["extension"]["extends_flow_type"] == "oid4vp_presentation"
    assert "machine_authentication_policy_id" in flow["extension"]["config"]


def test_machine_key_receipt_requires_key_thumbprint() -> None:
    receipt = _valid("authorization-decision-receipt.json")
    del receipt["binding"]["principal_key_thumbprint"]

    with pytest.raises(ValidationError):
        validate_instance(SCHEMAS_DIR / "authorization-decision-receipt.json", receipt)


@pytest.mark.parametrize(
    "mutation",
    [
        pytest.param(
            lambda receipt: receipt["binding"].update(replay_checked=False),
            id="replay-not-checked",
        ),
        pytest.param(
            lambda receipt: receipt["binding"].update(identity_key_bound=False),
            id="machine-key-not-bound",
        ),
        pytest.param(lambda receipt: receipt.pop("expires_at"), id="missing-expiry"),
    ],
)
def test_machine_key_receipt_security_controls_cannot_be_weakened(mutation) -> None:
    receipt = _valid("authorization-decision-receipt.json")
    mutation(receipt)

    with pytest.raises(ValidationError):
        validate_instance(SCHEMAS_DIR / "authorization-decision-receipt.json", receipt)


def test_attestation_only_trust_profile_does_not_require_credential_format() -> None:
    profile = _valid("trust-profile-machine-attestation.json")
    assert "supported_formats" not in profile
    validate_instance(SCHEMAS_DIR / "trust-profile.json", profile)


def test_attestation_trust_profile_requires_assertion_format() -> None:
    profile = _valid("trust-profile-machine-attestation.json")
    del profile["trusted_assertion_formats"]

    with pytest.raises(ValidationError):
        validate_instance(SCHEMAS_DIR / "trust-profile.json", profile)


def test_legacy_credential_trust_profile_still_requires_supported_formats() -> None:
    profile = _valid("trust-profile-machine-attestation.json")
    profile.pop("trust_purposes")
    profile.pop("trusted_assertion_formats")

    with pytest.raises(ValidationError):
        validate_instance(SCHEMAS_DIR / "trust-profile.json", profile)


def test_active_machine_has_exactly_one_active_identity_key() -> None:
    machine = _valid("machine-identity.json")
    duplicate = dict(machine["identity_keys"][0])
    duplicate["key_id"] = "urn:example:key:duplicate-active"
    duplicate["thumbprint"] = "sha256:ABCDEFGHIJKLMNOPQRSTUVWXYZabcde_1234567890"
    machine["identity_keys"].append(duplicate)

    with pytest.raises(ValidationError):
        validate_instance(SCHEMAS_DIR / "machine-identity.json", machine)

    machine["identity_keys"] = [
        {**machine["identity_keys"][0], "status": "ROTATING"}
    ]
    with pytest.raises(ValidationError):
        validate_instance(SCHEMAS_DIR / "machine-identity.json", machine)


@pytest.mark.parametrize(
    "control",
    ["challenge_required", "audience_binding_required", "replay_detection_required"],
)
def test_machine_authentication_freshness_controls_are_mandatory(control: str) -> None:
    policy = _valid("machine-authentication-policy.json")
    policy["machine_binding"]["proof_freshness"][control] = False

    with pytest.raises(ValidationError):
        validate_instance(SCHEMAS_DIR / "machine-authentication-policy.json", policy)


def test_holder_and_machine_binding_evidence_are_distinct() -> None:
    session = {
        "id": "29999999-9999-4999-8999-999999999999",
        "flow_id": "3aaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
        "presentation_policy_id": "4bbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
        "status": "PASSED",
        "result": {
            "passed": True,
            "holder_binding_evidence": {"required": True, "validated": True},
            "machine_binding_evidence": {
                "required": True,
                "validated": True,
                "machine_identity_id": "a1111111-1111-4111-8111-111111111111",
                "binding_method": "MACHINE_KEY",
                "proof_profile": "SIGNED_CHALLENGE",
            },
        },
        "created_at": "2026-07-28T00:00:00Z",
    }

    with pytest.raises(ValidationError):
        validate_instance(SCHEMAS_DIR / "verification-session.json", session)


def test_holder_binding_contract_does_not_gain_machine_key() -> None:
    presentation_schema = json.loads((SCHEMAS_DIR / "presentation-policy.json").read_text())
    binding_methods = presentation_schema["properties"]["holder_binding"]["properties"][
        "binding_methods"
    ]["items"]["enum"]

    assert "MACHINE_KEY" not in binding_methods
