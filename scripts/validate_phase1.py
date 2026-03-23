#!/usr/bin/env python3
"""Quick Phase 1 validation: check that all Phase 1 schema changes are applied."""
import json, sys, pathlib

base = pathlib.Path(__file__).parent.parent

errors = []

def check(label, value, expected):
    if value != expected:
        errors.append(f"FAIL {label}: got {value!r}, expected {expected!r}")
    else:
        print(f"  OK  {label}")

# flow-statuses.json
fs = json.load((base / "enums/flow-statuses.json").open())
check("flow-statuses title", fs["title"], "FlowInstanceStatus")
check("flow-statuses enum[0]", fs["enum"][0], "PENDING")
check("flow-statuses len", len(fs["enum"]), 9)
check("flow-statuses terminal_states", "terminal_states" in fs["$defs"], True)

# flow-execution.json
fe = json.load((base / "schemas/flow-execution.json").open())
check("flow-execution required has flow_type", "flow_type" in fe["required"], True)
check("flow-execution required has organization_id", "organization_id" in fe["required"], True)
check("flow-execution status is $ref", "$ref" in fe["properties"]["status"], True)
check("flow-execution has flow_type prop", "flow_type" in fe["properties"], True)
check("flow-execution has expires_at", "expires_at" in fe["properties"], True)
check("flow-execution has error_code", "error_code" in fe["properties"], True)
check("flow-execution no old error", "error" not in fe["properties"], True)

# issued-credential.json
ic = json.load((base / "schemas/issued-credential.json").open())
check("issued-credential status ACTIVE", "ACTIVE" in ic["properties"]["status"]["enum"], True)
check("issued-credential status old lowercase", "active" not in ic["properties"]["status"]["enum"], True)
check("issued-credential has revocation_profile_id", "revocation_profile_id" in ic["properties"], True)

# revocation-profile.json
rp = json.load((base / "schemas/revocation-profile.json").open())
check("revocation-profile has updated_at", "updated_at" in rp["properties"], True)
check("revocation-profile check_mode is $ref", "$ref" in rp["properties"]["check_mode"], True)

# verification-session.json
vs = json.load((base / "schemas/verification-session.json").open())
check("verification-session has updated_at", "updated_at" in vs["properties"], True)
check("verification-session has error", "error" in vs["properties"], True)

# issuance.json
iss = json.load((base / "schemas/issuance.json").open())
check("issuance has flow_execution_id", "flow_execution_id" in iss["properties"], True)
check("issuance no old flow_instance_id", "flow_instance_id" not in iss["properties"], True)

# revocation-timing-modes.json (new file)
rtm = json.load((base / "enums/revocation-timing-modes.json").open())
check("revocation-timing-modes enum", sorted(rtm["enum"]), sorted(["ALWAYS", "CACHED", "OFFLINE_GRACE", "DISABLED"]))

print()
if errors:
    for e in errors: print(e)
    sys.exit(1)
else:
    print("All Phase 1 checks passed.")
