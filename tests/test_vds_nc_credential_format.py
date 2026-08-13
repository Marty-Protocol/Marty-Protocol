"""VDS-NC is a first-class protocol credential format."""

import json

from .helpers import REPO_ROOT, SCHEMAS_DIR, validate_instance


ENUM_PATH = REPO_ROOT / "enums" / "credential-formats.json"


def test_vds_nc_has_canonical_wire_mapping_and_metadata():
    credential_formats = json.loads(ENUM_PATH.read_text(encoding="utf-8"))

    assert "VDS_NC" in credential_formats["enum"]
    definitions = credential_formats["$defs"]
    assert definitions["wire_format_mapping"]["VDS_NC"] == "vds_nc"
    assert definitions["wire_format_aliases"]["VDS_NC"] == ["vds-nc", "VDS-NC"]
    assert definitions["values"]["VDS_NC"]["standards"] == ["ICAO Doc 9303 Part 13"]


def test_active_compliance_profile_accepts_vds_nc():
    validate_instance(
        SCHEMAS_DIR / "active-compliance-profile.json",
        {
            "compliance_code": "ICAO_VDS_NC",
            "credential_format": "VDS_NC",
            "api_surface": [],
        },
    )


def test_generated_bindings_expose_vds_nc():
    generated = {
        "python": REPO_ROOT / "reference" / "python" / "mip_types" / "enums.py",
        "rust": REPO_ROOT / "reference" / "rust" / "src" / "enums.rs",
        "typescript": REPO_ROOT / "reference" / "typescript" / "src" / "enums.ts",
    }
    expected = {
        "python": 'VDS_NC = "VDS_NC"',
        "rust": 'serde(rename = "VDS_NC")',
        "typescript": "VDS_NC = 'VDS_NC'",
    }

    for language, path in generated.items():
        assert expected[language] in path.read_text(encoding="utf-8")
