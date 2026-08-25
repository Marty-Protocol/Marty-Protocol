"""Validate every bundled system Compliance Profile against the normative schema."""

import json

import pytest

from .helpers import REPO_ROOT, SCHEMAS_DIR, validate_instance


_profiles = sorted((REPO_ROOT / "compliance-profiles").rglob("*.json"))


@pytest.mark.parametrize(
    "profile_path",
    _profiles,
    ids=[str(path.relative_to(REPO_ROOT)) for path in _profiles],
)
def test_bundled_compliance_profile_passes_schema(profile_path):
    validate_instance(
        SCHEMAS_DIR / "compliance-profile.json",
        json.loads(profile_path.read_text(encoding="utf-8")),
    )


def test_icao_dtc_profile_does_not_claim_mdoc_or_oid4vci_conformance():
    profile = json.loads(
        (REPO_ROOT / "compliance-profiles" / "icao" / "dtc.json").read_text(
            encoding="utf-8"
        )
    )
    serialized = json.dumps(profile).lower()

    assert profile["credential_format"] == "ICAO_DTC"
    assert profile["status"] == "DRAFT"
    assert profile["discoverable"] is False
    assert "issuance_protocol" not in profile
    assert "api_surface" not in profile
    assert "required_namespaces" not in profile
    assert "doc 9303 part 13" not in serialized
    assert "com.icao.dtc" not in serialized


def test_icao_dtc_format_has_no_default_oid4vci_wire_mapping():
    formats = json.loads(
        (REPO_ROOT / "enums" / "credential-formats.json").read_text(
            encoding="utf-8"
        )
    )

    assert "ICAO_DTC" in formats["enum"]
    assert "ICAO_DTC" not in formats["$defs"]["wire_format_mapping"]
    assert "ICAO_EMRTD" not in formats["$defs"]["wire_format_mapping"]
    assert "ICAO_MRZ" not in formats["$defs"]["wire_format_mapping"]


def test_icao_mrz_profile_is_not_mdoc_or_cryptographic_authentication():
    profile = json.loads(
        (REPO_ROOT / "compliance-profiles" / "icao" / "mrz.json").read_text(
            encoding="utf-8"
        )
    )

    assert profile["credential_format"] == "ICAO_MRZ"
    assert profile["status"] == "DRAFT"
    assert profile["discoverable"] is False
    assert "supported_algorithms" not in profile
    assert "key_requirements" not in profile
    assert "revocation_methods" not in profile
    assert "trust_source_types" not in profile
    assert "cryptographic authenticity" in profile["description"]


def test_icao_passport_profile_uses_correct_biometric_data_groups():
    profile = json.loads(
        (REPO_ROOT / "compliance-profiles" / "icao" / "passport.json").read_text(
            encoding="utf-8"
        )
    )
    claims = {claim["name"]: claim for claim in profile["required_claims"]}
    eac_groups = profile["physical_production"]["access_control"]["eac"][
        "protected_data_groups"
    ]

    assert profile["credential_format"] == "ICAO_EMRTD"
    assert profile["status"] == "DRAFT"
    assert profile["discoverable"] is False
    assert "iris" in claims["data_group_4"]["description"].lower()
    assert "signature" in claims["data_group_7"]["description"].lower()
    assert eac_groups == ["DG3", "DG4"]
    assert "conformance_tests" not in profile


def test_aamva_mdl_profile_is_current_but_not_claimed_conformant():
    profile = json.loads(
        (REPO_ROOT / "compliance-profiles" / "aamva" / "mdl.json").read_text(
            encoding="utf-8"
        )
    )
    claims = {
        (claim["namespace"], claim["name"]): claim
        for claim in profile["required_claims"]
    }
    serialized = json.dumps(profile)

    assert profile["version"] == "1.6.0"
    assert profile["status"] == "DRAFT"
    assert profile["discoverable"] is False
    assert "issuance_protocol" not in profile
    assert "api_surface" not in profile
    assert "revocation_methods" not in profile
    assert "holder_binding_required" not in profile
    assert "ES512" in profile["supported_algorithms"]
    assert ("org.iso.18013.5.1", "resident_address") in claims
    assert ("org.iso.18013.5.1.aamva", "domestic_driving_privileges") in claims
    assert "org.aamva.16" not in serialized
    assert "real_id" not in serialized


def test_eudi_mdl_profile_remains_draft_until_current_mapping_is_tested():
    profile = json.loads(
        (REPO_ROOT / "compliance-profiles" / "eudi" / "mdl.json").read_text(
            encoding="utf-8"
        )
    )

    assert profile["status"] == "DRAFT"
    assert profile["discoverable"] is False
    assert "issuance_protocol" not in profile
    assert "api_surface" not in profile
    assert "conformance_tests" not in profile
