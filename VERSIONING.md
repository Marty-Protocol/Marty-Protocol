# Versioning Policy

The Marty Identity Protocol uses [Semantic Versioning](https://semver.org/), applied to specification changes.

**Current Version:** 0.1.0

---

## Version Format

```
MAJOR.MINOR.PATCH
```

---

## Change Classification

### MAJOR version bump (breaking change)

Changes that are **not backward-compatible** and require implementors to update:

- Removing a previously required field from a schema
- Adding a new required field to an existing entity
- Renaming a field or entity that appears in normative text
- Changing the semantic meaning of an existing field
- Removing a previously stable endpoint or resource
- Removing an enum value from a closed vocabulary
- Changing validation rules in a way that rejects previously valid documents

**Example:** `0.x.x` → `1.0.0`

---

### MINOR version bump (backward-compatible addition)

Changes that **add new capability** without breaking existing valid documents:

- Adding a new optional field to an entity
- Adding a new entity or abstraction
- Adding a new enum value to a closed vocabulary
- Adding a new compliance profile
- Clarifying normative text without changing validation behavior
- Adding new examples or conformance fixtures
- Adding a new reference implementation

**Example:** `0.1.x` → `0.2.0`

---

### PATCH version bump (non-normative fix)

Changes that **correct errors** without altering semantic behavior:

- Fixing typographical errors in normative text
- Correcting JSON Schema constraints that misrepresented the spec
- Updating examples to match existing normative text
- Fixing documentation links or formatting
- Updating non-normative descriptions

**Example:** `0.1.0` → `0.1.1`

---

## Pre-1.0 Policy

While the protocol is at `0.x.x`, MINOR versions may contain breaking changes. This gives the specification room to evolve based on implementation feedback before committing to a stable API surface.

Breaking changes in `0.x.x` will be:
- Clearly documented in CHANGELOG.md
- Labeled with `[BREAKING]` in the changelog entry
- Accompanied by a migration note when feasible

---

## Stability Markers

Sections of the specification may carry an explicit stability marker:

| Marker | Meaning |
|--------|---------|
| **Stable** | Will not change without a MAJOR version bump |
| **Draft** | May change in MINOR versions; production use at your own risk |
| **Experimental** | May change without notice; do not deploy to production |
| **Deprecated** | Will be removed in the next MAJOR version |

---

## Publication

Each version is tagged in the repository:

```
git tag v0.1.0
git push origin v0.1.0
```

Release notes are published in CHANGELOG.md. Conformance test suites are versioned alongside the specification.
