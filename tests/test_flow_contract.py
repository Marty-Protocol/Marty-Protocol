"""Cross-file invariants for the MIP 0.4.0 Flow contract."""

import json

import pytest

from .helpers import REPO_ROOT, validate_instance


FLOW_TYPES_PATH = REPO_ROOT / "enums" / "flow-types.json"
FLOW_SCHEMA_PATH = REPO_ROOT / "schemas" / "flow.json"


def _manifest() -> dict:
    return json.loads(FLOW_TYPES_PATH.read_text())


def _validate_extension_graph(extension: dict) -> None:
    step_ids = [step["step_id"] for step in extension["steps"]]
    if len(step_ids) != len(set(step_ids)):
        raise ValueError("FlowExtension step_id values must be unique")
    if extension["entry_step_id"] not in step_ids:
        raise ValueError("FlowExtension entry_step_id must reference a step")

    adjacency = {step_id: [] for step_id in step_ids}
    for transition in extension["transitions"]:
        source = transition["from_step_id"]
        target = transition["to_step_id"]
        if source not in adjacency or target not in adjacency:
            raise ValueError("FlowExtension transition must reference declared steps")
        adjacency[source].append(target)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(step_id: str) -> None:
        if step_id in visiting:
            raise ValueError("FlowExtension graph must be acyclic")
        if step_id in visited:
            return
        visiting.add(step_id)
        for target in adjacency[step_id]:
            visit(target)
        visiting.remove(step_id)
        visited.add(step_id)

    for step_id in step_ids:
        visit(step_id)


def test_standard_flow_types_have_one_manifest_definition() -> None:
    manifest = _manifest()
    all_values = set(manifest["enum"])
    standard_values = set(manifest["$defs"]["standard_values"]["enum"])
    descriptions = manifest["$defs"]["values"]
    sequences = manifest["$defs"]["step_sequences"]

    assert all_values == standard_values | {"custom"}
    assert set(descriptions) == all_values
    assert set(sequences) == standard_values
    assert all(sequences[flow_type] for flow_type in standard_values)
    assert descriptions["custom"]["category"] == "DERIVED"


def test_flow_schema_references_canonical_flow_type_manifest() -> None:
    schema = json.loads(FLOW_SCHEMA_PATH.read_text())
    assert schema["properties"]["flow_type"]["$ref"] == "../enums/flow-types.json"
    assert "enabled" not in schema["properties"]


def test_physical_flow_declares_complete_normative_sequence() -> None:
    sequence = _manifest()["$defs"]["step_sequences"]["physical_document_issuance"]
    assert sequence == [
        "accept_application",
        "validate_evidence",
        "approval_decision",
        "generate_data_groups",
        "sign_sod",
        "submit_to_personalization",
        "track_production",
        "quality_verify",
        "activate_credential",
    ]


def test_standard_flow_rejects_extension_envelope() -> None:
    flow = json.loads((REPO_ROOT / "conformance" / "valid" / "flow-custom.json").read_text())
    flow["flow_type"] = "oid4vci_pre_authorized"
    with pytest.raises(Exception):
        validate_instance(FLOW_SCHEMA_PATH, flow)


@pytest.mark.parametrize(
    "mutator, message",
    [
        (lambda extension: extension["steps"].append(dict(extension["steps"][0])), "unique"),
        (lambda extension: extension.update(entry_step_id="missing"), "entry_step_id"),
        (
            lambda extension: extension["transitions"].append(
                {"from_step_id": "issue", "to_step_id": "policy_gate", "outcome": "SUCCESS"}
            ),
            "acyclic",
        ),
    ],
)
def test_custom_extension_graph_semantics(mutator, message: str) -> None:
    flow = json.loads((REPO_ROOT / "conformance" / "valid" / "flow-custom.json").read_text())
    mutator(flow["extension"])
    with pytest.raises(ValueError, match=message):
        _validate_extension_graph(flow["extension"])


def test_valid_custom_extension_graph_semantics() -> None:
    flow = json.loads((REPO_ROOT / "conformance" / "valid" / "flow-custom.json").read_text())
    _validate_extension_graph(flow["extension"])
