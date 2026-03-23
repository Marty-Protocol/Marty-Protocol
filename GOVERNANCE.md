# Governance

This document describes how the Marty Identity Protocol (MIP) specification is maintained, how decisions are made, and how contributors can take on greater responsibility.

---

## Roles

### Contributor

Anyone who opens an issue, submits a pull request, or participates in discussion. No special requirements; see [CONTRIBUTING.md](CONTRIBUTING.md) for how to get started.

### Reviewer

A contributor who regularly provides substantive review on pull requests. Reviewers are recognized informally; maintainers may invite frequent reviewers to become maintainers.

### Maintainer

Maintainers are responsible for:

- Reviewing and merging pull requests
- Triaging issues
- Releasing new versions per [VERSIONING.md](VERSIONING.md)
- Maintaining the conformance test suite
- Representing the project in external standards discussions

Maintainers are listed in [CODEOWNERS](.github/CODEOWNERS) and the repository's GitHub team.

**Becoming a maintainer:** Open a GitHub issue titled "Maintainer nomination: {name}" with a summary of the candidate's contributions. Existing maintainers vote by emoji reaction (+1 / -1) over a 7-day window. A simple majority of responding maintainers approves the nomination.

**Stepping down:** Maintainers who are inactive for 6+ months may be moved to emeritus status by a majority vote. Emeritus maintainers retain commit history attribution and may return to active status at any time.

---

## Decision Making

### Routine Changes (PATCH / editorial)

Changes that do not modify normative behavior — documentation fixes, conformance fixture additions, typo corrections — may be merged by any maintainer with at least one approving review from another maintainer.

### Minor Changes (MINOR — new optional fields, new enum values, new compliance profiles)

Require:

1. An issue open for at least **5 business days** with no unresolved objections from maintainers.
2. At least **two maintainer approvals** on the pull request.
3. Updated CHANGELOG.md entry.

### Breaking Changes (MAJOR — field removal, new required fields, normative semantics changes)

Require:

1. An issue open for at least **14 calendar days**.
2. A written proposal covering: the change, rationale, migration path, and impact on existing conformant implementations.
3. **All active maintainers** given opportunity to review (minimum 14-day review window).
4. At least **two-thirds of responding maintainers** approve.
5. A migration guide entry in [docs/migration-guide.md](docs/migration-guide.md).
6. Updated conformance fixtures demonstrating the change.

### Disputes

If a PR receives a blocking objection, it must not be merged until the objection is resolved or withdrawn. If consensus cannot be reached within 21 days, the matter is escalated to a synchronous maintainer meeting. The meeting outcome (majority decision) is documented as a comment on the PR and is binding.

---

## Spec Versioning

Version increments follow the rules in [VERSIONING.md](VERSIONING.md). Maintainers cut releases by:

1. Updating `**Version:**` in `SPECIFICATION.md` and `**Status:**` as appropriate.
2. Updating `CHANGELOG.md` — move `[Unreleased]` entries to the new version heading.
3. Tagging the commit: `git tag -s v{major}.{minor}.{patch} -m "MIP v{major}.{minor}.{patch}"`.
4. Publishing a GitHub Release with the CHANGELOG section as release notes.

---

## Specification Status Lifecycle

| Status | Meaning |
|--------|---------|
| `Draft` | Active development; breaking changes expected |
| `Candidate` | Feature-complete; implementation feedback period (minimum 60 days) |
| `Stable` | Ratified; breaking changes require a new major version |
| `Deprecated` | Superseded; no further updates |

---

## Project Charter

MIP is a vendor-neutral open standard. No single organization controls the specification. The project does not require a corporate contributor license agreement (CLA) — contributions are made under the Apache 2.0 license via the Developer Certificate of Origin (DCO).

Decisions are made in the open on GitHub. There are no private steering committee votes or closed mailing lists.
