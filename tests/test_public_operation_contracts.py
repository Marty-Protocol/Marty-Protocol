"""MIP public operations expose identities, never custody selectors."""

import copy
import json

import pytest
from jsonschema import ValidationError

from .helpers import REPO_ROOT, validate_instance


ISSUANCE = REPO_ROOT / "schemas" / "issuance-request.json"
VERIFY_REQUEST = REPO_ROOT / "schemas" / "verification-flow-start-request.json"
VERIFY_RESPONSE = REPO_ROOT / "schemas" / "verification-flow-start-response.json"

FORBIDDEN_CUSTODY_FIELDS = {
    "issuer_profile_id",
    "issuer_key_id",
    "issuer_algorithm",
    "key_access_mode",
    "verification_method_id",
    "signing_service_id",
    "signing_key_reference",
    "key_reference",
    "kms_provider",
    "provider",
    "key_name",
    "key_version",
    "transit_mount",
}


def _properties(schema_path) -> set[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return set(schema["properties"])


def _issuance() -> dict:
    return {
        "organization_id": "org-conformance",
        "issuer_did": "did:web:issuer.example.com",
        "subject_did": "did:key:z6MkSubject",
        "claims": {"given_name": "Ada"},
    }


def _verification() -> dict:
    return {
        "organization_id": "org-conformance",
        "issuer_did": "did:web:verifier.example.com",
        "presentation_policy_id": "policy-conformance",
        "response_type": "vp_token",
        "request_transport": "request_uri",
        "request_uri_method": "post",
    }


def test_public_operation_schemas_expose_no_custody_selector() -> None:
    for schema_path in (ISSUANCE, VERIFY_REQUEST, VERIFY_RESPONSE):
        assert _properties(schema_path).isdisjoint(FORBIDDEN_CUSTODY_FIELDS)


def test_direct_issuance_uses_only_organization_and_issuer_did() -> None:
    validate_instance(ISSUANCE, _issuance())


def test_template_issuance_may_derive_issuer_did_from_template() -> None:
    request = _issuance()
    request.pop("issuer_did")
    request["credential_template_id"] = "template-conformance"
    validate_instance(ISSUANCE, request)


def test_issuance_without_template_or_issuer_did_fails_closed() -> None:
    request = _issuance()
    request.pop("issuer_did")
    with pytest.raises(ValidationError):
        validate_instance(ISSUANCE, request)


def test_null_template_and_issuer_did_do_not_select_an_identity() -> None:
    request = _issuance()
    request["issuer_did"] = None
    request["credential_template_id"] = None
    with pytest.raises(ValidationError):
        validate_instance(ISSUANCE, request)


@pytest.mark.parametrize("field", sorted(FORBIDDEN_CUSTODY_FIELDS))
def test_issuance_rejects_private_selector_at_root_or_in_claims(field: str) -> None:
    root = _issuance()
    root[field] = "private-selector"
    with pytest.raises(ValidationError):
        validate_instance(ISSUANCE, root)

    nested = _issuance()
    nested["claims"][field] = "private-selector"
    with pytest.raises(ValidationError):
        validate_instance(ISSUANCE, nested)


def test_public_authorized_client_rejects_private_jwk_material() -> None:
    request = _issuance()
    request["authorized_client"] = {
        "client_id": "wallet-client",
        "jwks": {
            "keys": [
                {
                    "kty": "EC",
                    "crv": "P-256",
                    "kid": "wallet-key",
                    "x": "A" * 43,
                    "y": "B" * 43,
                    "d": "private",
                }
            ]
        },
    }
    with pytest.raises(ValidationError):
        validate_instance(ISSUANCE, request)


def test_public_authorized_client_accepts_omitted_or_null_optional_metadata() -> None:
    request = _issuance()
    request["authorized_client"] = {
        "client_id": "wallet-client",
        "jwks": {
            "keys": [
                {
                    "kty": "EC",
                    "crv": "P-256",
                    "kid": "wallet-key",
                    "x": "A" * 43,
                    "y": "B" * 43,
                    "alg": None,
                    "use": None,
                }
            ]
        },
    }
    validate_instance(ISSUANCE, request)


def test_vcdm_document_requires_verifiable_credential_type() -> None:
    request = _issuance()
    request.pop("claims")
    request["credential_document"] = {
        "@context": ["https://www.w3.org/ns/credentials/v2"],
        "type": "NotAVerifiableCredential",
        "credentialSubject": {"id": "did:example:holder"},
    }
    with pytest.raises(ValidationError):
        validate_instance(ISSUANCE, request)


def test_signed_oid4vp_request_is_did_only() -> None:
    validate_instance(VERIFY_REQUEST, _verification())


def test_siop_request_is_did_only_without_presentation_policy() -> None:
    request = _verification()
    request.pop("presentation_policy_id")
    request.update(
        {
            "response_type": "id_token",
            "request_transport": "request_object",
            "request_uri_method": "get",
        }
    )
    validate_instance(VERIFY_REQUEST, request)


@pytest.mark.parametrize("field", sorted(FORBIDDEN_CUSTODY_FIELDS))
def test_verification_rejects_private_custody_selector(field: str) -> None:
    request = _verification()
    request[field] = "private-selector"
    with pytest.raises(ValidationError):
        validate_instance(VERIFY_REQUEST, request)


@pytest.mark.parametrize(
    ("updates", "removed"),
    [
        ({"request_transport": "url_query", "oid4vp_profile": "haip"}, ()),
        ({"request_transport": "url_query", "response_type": "id_token"}, ()),
        ({"request_transport": "request_object", "request_uri_method": "post"}, ()),
        ({"response_type": "vp_token"}, ("presentation_policy_id",)),
    ],
)
def test_invalid_verification_transport_combinations_fail_closed(
    updates: dict, removed: tuple[str, ...]
) -> None:
    request = copy.deepcopy(_verification())
    request.update(updates)
    for field in removed:
        request.pop(field)
    with pytest.raises(ValidationError):
        validate_instance(VERIFY_REQUEST, request)


def test_verification_response_does_not_leak_internal_flow_definition() -> None:
    response = {
        "instance_id": "flow-instance",
        "request_uri": "openid4vp://authorize?request_uri=https%3A%2F%2Fexample.test",
        "qr_code_data": "openid4vp://authorize?request_uri=https%3A%2F%2Fexample.test",
        "presentation_policy_id": "policy-conformance",
        "nonce": "a-high-entropy-nonce-value",
        "expires_at": "2026-07-30T20:00:00Z",
        "status": "AWAITING_WALLET",
    }
    validate_instance(VERIFY_RESPONSE, response)

    response["flow_definition_id"] = "internal-routing-id"
    with pytest.raises(ValidationError):
        validate_instance(VERIFY_RESPONSE, response)
