# Root specification amendment for coordinated MIP 0.6.0 promotion

Apply these changes to the beta-only candidate specification when its candidate gate in `README.md` passes. Apply them to Section 9 of the public root specification only at the later coordinated 0.6.0 release gate:

- Add `passport_digital_handoff` to normative FlowType values and the derived ISSUANCE category. Require `credential_template_id`, `application_template_id`, and `delivery_destination_profile_id`.
- Freeze its distinct eight-step sequence: `accept_application -> validate_evidence -> approval_decision -> generate_data_groups -> sign_sod -> verify_digital_package -> seal_handoff_package -> handoff_ready`.
- Require the `ICAO_PASSPORT_DIGITAL_HANDOFF` compliance profile and a Marty-managed `digital_handoff` destination. Keep `physical_document_issuance` tied to `physical_production` and its existing nine-step sequence.
- Specify that the public result is only an opaque handoff reference plus digests of an encrypted private manifest and signed attestation. Protected receipts bind Marty IDs to the exact SOD digest; the ICAO SOD itself binds only data-group hashes and the document-signer signature.
- Except these two passport FlowTypes and explicit custom extensions from the mutual-exclusion rule for credential and application templates.
- Let a Credential Template reference a system Compliance Profile by its stable `cp-*`/`cpf-*` ID as well as an organization UUID profile, and validate the exact referenced format/protocol at Flow activation.
- In the beta candidate, advertise only its exact prerelease version and explicit digital-handoff capability in beta discovery. Update the public exact supported version and discovery contract as part of the coordinated 0.6.0 release, not in this proposal.
