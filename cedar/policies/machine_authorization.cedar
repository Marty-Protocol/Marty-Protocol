// Managed machine authorization
//
// The external action and resource identifiers are opaque to MIP. The domain
// system remains responsible for interpreting the decision and enforcing its
// own operation.

@id("permit-active-bound-attested-machine")
permit (
    principal is MIP::MachineIdentity,
    action == MIP::Action::"authorization_decisions:evaluate",
    resource is MIP::DeploymentProfile
)
when {
    principal.status == "ACTIVE" &&
    context.binding_method == "MACHINE_KEY" &&
    context.principal_key_thumbprint == principal.primary_key_thumbprint &&
    context.attestation_valid &&
    context.identity_key_bound
};

@id("deny-unbound-or-unattested-machine")
forbid (
    principal is MIP::MachineIdentity,
    action == MIP::Action::"authorization_decisions:evaluate",
    resource is MIP::DeploymentProfile
)
unless {
    principal.status == "ACTIVE" &&
    context.principal_key_thumbprint == principal.primary_key_thumbprint &&
    context.attestation_valid &&
    context.identity_key_bound
};
