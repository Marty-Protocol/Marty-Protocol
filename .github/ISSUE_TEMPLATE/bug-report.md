---
name: Bug Report
about: Report an error in a schema, conformance fixture, or reference implementation
labels: bug
---

## What is wrong?

<!-- Describe the problem clearly. -->

## Location

- [ ] JSON Schema (`schemas/` or `enums/`)
- [ ] Conformance fixture (`conformance/`)
- [ ] Reference implementation (`reference/`)
- [ ] Example (`examples/`)
- [ ] Tooling / scripts

**File:** <!-- e.g., schemas/trust-profile.json -->

## Expected behavior

<!-- What should happen? -->

## Actual behavior

<!-- What happens instead? Include error messages or validator output if applicable. -->

## Reproduction steps

```
# e.g., python -m pytest tests/test_conformance.py::test_valid_fixtures[trust-profile-minimal.json] -v
```

## Environment

- OS:
- Python / Node / Rust version:
- jsonschema / ajv / serde version (if relevant):
