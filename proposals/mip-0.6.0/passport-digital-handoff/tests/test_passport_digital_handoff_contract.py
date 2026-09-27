"""Cross-file boundaries for the proposed passport digital handoff contract."""

import copy
import hashlib
import json
import uuid

import pytest
from jsonschema import ValidationError

from .helpers import REPO_ROOT, validate_instance


def _fixture(name: str) -> dict:
    return json.loads((REPO_ROOT / "conformance" / "valid" / name).read_text())


def test_source_job_digest_vector_binds_organization_and_private_job_uuid() -> None:
    package = _fixture("passport-digital-handoff-private-manifest.json")
    prefix = b"MIP-PASSPORT-DIGITAL-HANDOFF-SOURCE-JOB-V1" + bytes([0])
    organization = package["organization_id"].encode("utf-8")
    private_job = uuid.UUID(package["source_job_id"])
    expected = hashlib.sha256(prefix + len(organization).to_bytes(4, "big") + organization + private_job.bytes).hexdigest()
    assert package["source_job_sha256"] == expected
    other_organization = b"another-org"
    assert hashlib.sha256(prefix + len(other_organization).to_bytes(4, "big") + other_organization + private_job.bytes).hexdigest() != expected


@pytest.mark.parametrize("missing", [
    "credential_template_id", "application_template_id", "delivery_destination_profile_id",
])
def test_digital_flow_requires_all_references(missing: str) -> None:
    for schema_name, fixture_name in [
        ("flow.json", "flow-passport-digital-handoff.json"),
        ("flow-create-request.json", "flow-create-request-passport-digital-handoff.json"),
    ]:
        flow = _fixture(fixture_name)
        del flow[missing]
        with pytest.raises(ValidationError):
            validate_instance(REPO_ROOT / "schemas" / schema_name, flow)


@pytest.mark.parametrize("changes", [
    {"provider": "physical_personalization_bureau"},
    {"mode": "physical_production"},
    {"delivery_target": "physical_document"},
    {"issuance_protocol": "PHYSICAL_DOCUMENT"},
    {"credential_format": "MDOC"},
    {"compliance_profile_code": "ICAO_PASSPORT"},
    {"connector_type": "personalization_bureau", "connector_id": "bureau-1"},
    {"is_system": True},
    {"organization_id": None},
])
def test_digital_destination_rejects_physical_or_unscoped_configuration(changes: dict) -> None:
    profile = _fixture("delivery-destination-profile-digital-handoff.json")
    profile.update(changes)
    with pytest.raises(ValidationError):
        validate_instance(REPO_ROOT / "schemas" / "delivery-destination-profile.json", profile)


@pytest.mark.parametrize("changes", [
    {"status": "SHIPPED"},
    {"bureau_job_id": "bureau-1"},
    {"mrz_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
    {"secure_artifact_reference": "vault://private/path"},
    {"issuer_profile_bindings": {"csca": {}}},
    {"artifact_seal_flow_attestation_sha256": "abababababababababababababababababababababababababababababababab"},
])
def test_public_handoff_rejects_sensitive_or_physical_claims(changes: dict) -> None:
    package = _fixture("passport-digital-handoff-package.json")
    package.update(changes)
    with pytest.raises(ValidationError):
        validate_instance(REPO_ROOT / "schemas" / "passport-digital-handoff-package.json", package)


def test_digital_package_requires_both_dg1_and_dg2_hashes() -> None:
    package = _fixture("passport-digital-handoff-private-manifest.json")
    for field in ("data_group_sha256", "sod_data_group_sha256"):
        altered = copy.deepcopy(package)
        del altered[field]["DG2"]
        with pytest.raises(ValidationError):
            validate_instance(REPO_ROOT / "schemas" / "passport-digital-handoff-private-manifest.json", altered)


@pytest.mark.parametrize("field", [
    "application_template_id", "issuer_profile_bindings", "artifact_seal_flow_attestation_sha256",
])
def test_private_manifest_requires_trusted_identity_bindings(field: str) -> None:
    manifest = _fixture("passport-digital-handoff-private-manifest.json")
    del manifest[field]
    with pytest.raises(ValidationError):
        validate_instance(REPO_ROOT / "schemas" / "passport-digital-handoff-private-manifest.json", manifest)


@pytest.mark.parametrize("role", ["csca", "document_signer"])
def test_private_manifest_requires_registry_revision_and_custody_receipt(role: str) -> None:
    manifest = _fixture("passport-digital-handoff-private-manifest.json")
    for field in ("registry_revision", "custody_receipt_sha256"):
        altered = copy.deepcopy(manifest)
        del altered["issuer_profile_bindings"][role][field]
        with pytest.raises(ValidationError):
            validate_instance(REPO_ROOT / "schemas" / "passport-digital-handoff-private-manifest.json", altered)


def test_verification_and_signing_steps_have_no_hook_surface() -> None:
    manifest = json.loads((REPO_ROOT / "enums" / "flow-types.json").read_text())
    assert manifest["$defs"]["extensible_steps"]["passport_digital_handoff"] == ["approval_decision"]


def test_final_receipt_binds_completed_flow_to_private_package() -> None:
    private = _fixture("passport-digital-handoff-private-manifest.json")
    final = _fixture("passport-digital-handoff-final-flow-receipt.json")
    release = _fixture("passport-digital-handoff-release-attestation.json")
    public = _fixture("passport-digital-handoff-package.json")
    assert final["private_manifest_id"] == private["id"]
    for field in ("organization_id", "source_job_id", "flow_execution_id", "package_revision", "sod_sha256", "artifact_sha256"):
        assert final[field] == private[field]
    assert final["artifact_seal_flow_attestation_sha256"] == private["artifact_seal_flow_attestation_sha256"]
    assert final["completed_steps"] == json.loads((REPO_ROOT / "enums" / "flow-types.json").read_text())["$defs"]["step_sequences"]["passport_digital_handoff"]
    assert release["handoff_reference"] == public["handoff_reference"] == final["handoff_reference"]
    assert release["protected_manifest_sha256"] == public["protected_manifest_sha256"]
    assert release["artifact_seal_flow_attestation_sha256"] == final["artifact_seal_flow_attestation_sha256"]
    assert "final_flow_completion_receipt_sha256" in release
    assert "final_flow_completion_receipt_sha256" not in private


def test_proposed_template_profile_and_flow_references_resolve() -> None:
    flow = _fixture("flow-passport-digital-handoff.json")
    credential = _fixture("credential-template-passport-digital-handoff.json")
    application = _fixture("application-template-passport-digital-handoff.json")
    destination = _fixture("delivery-destination-profile-digital-handoff.json")
    profile = json.loads((REPO_ROOT / "compliance-profiles" / "icao" / "passport-digital-handoff.json").read_text())
    assert flow["credential_template_id"] == credential["id"] == application["credential_template_id"]
    assert flow["application_template_id"] == application["id"]
    assert flow["delivery_destination_profile_id"] == destination["id"]
    assert credential["compliance_profile_id"] == profile["id"]
    assert profile["issuance_protocol"] == destination["issuance_protocol"] == "DIGITAL_HANDOFF"
    assert {flow["organization_id"], credential["organization_id"], application["organization_id"], destination["organization_id"]} == {flow["organization_id"]}


def test_non_uuid_flow_and_org_references_remain_schema_valid() -> None:
    flow = _fixture("flow-passport-digital-handoff.json")
    private = _fixture("passport-digital-handoff-private-manifest.json")
    final = _fixture("passport-digital-handoff-final-flow-receipt.json")
    flow["id"] = final["flow_definition_id"] = "flow-definition-1"
    flow["organization_id"] = private["organization_id"] = final["organization_id"] = "org-conformance"
    private["flow_execution_id"] = final["flow_execution_id"] = "flow-execution-1"
    org_bytes = private["organization_id"].encode("utf-8")
    job_bytes = uuid.UUID(private["source_job_id"]).bytes
    private["source_job_sha256"] = hashlib.sha256(
        b"MIP-PASSPORT-DIGITAL-HANDOFF-SOURCE-JOB-V1\x00"
        + len(org_bytes).to_bytes(4, "big") + org_bytes + job_bytes
    ).hexdigest()
    validate_instance(REPO_ROOT / "schemas" / "flow.json", flow)
    validate_instance(REPO_ROOT / "schemas" / "passport-digital-handoff-private-manifest.json", private)
    validate_instance(REPO_ROOT / "schemas" / "passport-digital-handoff-final-flow-receipt.json", final)
