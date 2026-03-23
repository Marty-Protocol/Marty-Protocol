# Compliance Profile — Design Notes

**Version:** 0.1.0

---

## Key Design Decisions

### Compliance As the User-Facing Dimension

Operators understand "AAMVA mDL" or "EUDI PID" but don't necessarily understand "SD-JWT-VC with ISO 23220-3 namespace encoding." Compliance Profiles hide the technical format from the user-facing configuration surface. Only compliance + specification engineers need to understand the format dimension.

### System Profiles Are Immutable

System profiles encode legally or technically normative requirements. An implementation of AAMVA_MDL that allows modification of the format or artifact requirements is non-conformant. Immutability is enforced by `is_system: true` plus a server-side guard on update/delete.

### Why is_system Is Explicit

Rather than detecting system profiles by the absence of `organization_id`, we use an explicit `is_system` flag. This prevents edge cases where a custom profile is mistakenly treated as mutable because it was created without an org ID.

### Custom Profiles for Non-Standard Frameworks

Organizations with proprietary credential schemes (e.g., internal access badges not matching any public standard) can create custom compliance profiles with `compliance_code: CUSTOM`. These behave identically to system profiles in terms of how Credential Templates reference them, but they are organization-scoped.

### Immutability After Reference

Once an ACTIVE Credential Template references a Compliance Profile, that profile MUST NOT change. This is analogous to how library versioning works: once you publish a dependency, consumers depend on that exact behavior. Profile updates require creating a new profile version and migrating templates.
