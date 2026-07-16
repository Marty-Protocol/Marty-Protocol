# Versioning Policy

The Marty Identity Protocol uses semantic version identifiers for coordinated
specification and implementation releases.

**Current and only supported version:** `0.3.1`

## Pre-1.0 Releases

MIP is pre-1.0. Any release may contain breaking changes, including removal of
routes, fields, enum values, generated types, and conformance fixtures. A
release supports only its exact declared version unless its specification says
otherwise.

MIP 0.3.1 does not negotiate a highest common version, retain deprecated
request aliases, or support mixed-version deployments. Implementations must:

1. Build protocol, generated bindings, services, clients, and fixtures from one
   release manifest.
2. Advertise the exact version in `X-MIP-Version`.
3. Fail readiness when a required component advertises another MIP version.
4. Apply breaking migrations and deploy all components atomically.
5. Restore the complete prior release and pre-migration database on rollback.

## Change Classification

- **MAJOR:** post-1.0 incompatible protocol changes.
- **MINOR:** pre-1.0 capability or contract releases, which may be breaking.
- **PATCH:** corrections and coordinated contract hardening; before 1.0 these
  may also reject previously accepted invalid or noncanonical inputs.

Every breaking release must identify removed contracts in `CHANGELOG.md`,
provide a one-way migration where stored data changes, update conformance
fixtures, regenerate all bindings, and publish release-gate evidence.

## Publication

Tag the exact release and publish generated artifacts from that tag:

```sh
git tag v0.3.1
git push origin v0.3.1
```

Code generation drift and conformance failures block publication.
