# Open Badges 2 temporary compatibility window

Open Badges 3 is the current and default Marty protocol profile. Open Badges
2 remains available only as `OB2_COMPATIBILITY` while existing deployments
complete their migration.

- Do not create new OB2-only integrations, algorithms, aliases, or dependency
  exceptions.
- Continue testing existing OB2 issuance and verification behavior during the
  migration window.
- Review remaining use on 2026-09-01.
- Target removal on 2026-10-01, before MIP 1.0, unless a separately reviewed
  extension is recorded.
- Migrate callers to `OB3_JWT` or `OB3_JSONLD`.

The implementation retirement work is tracked in
[`ElevenID/marty-core#96`](https://github.com/ElevenID/marty-core/issues/96).
This exception does not establish a general legacy-compatibility policy.
