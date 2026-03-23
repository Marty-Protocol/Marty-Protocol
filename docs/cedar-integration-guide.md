# Cedar Integration Guide for MIP Implementors

This guide explains how to integrate [Cedar](https://www.cedarpolicy.com/) policy evaluation into a MIP-compatible implementation. Cedar is the authorization engine underlying the `PolicySet` entity (§16 of the specification).

---

## Overview

MIP uses Cedar for three authorization domains:

| Domain | `policy_type` | Applied where |
|--------|--------------|---------------|
| **Access Control** | `ACCESS_CONTROL` | Gateway / API layer: who can read/write which MIP entities |
| **Credential Verification** | `CREDENTIAL_VERIFICATION` | Verification flow: whether a credential passes trust rules |
| **Approval Rules** | `APPROVAL_RULES` | Application approval flow: whether an application can be auto-approved |

Cedar provides deny-by-default, statically analyzable policies. The MIP Cedar schema (`cedar/mip.cedarschema`) defines the entity types and actions that all three domains share.

---

## Prerequisites

```bash
pip install "cedarpy>=4.8.0"
```

`cedarpy` wraps the official Rust `cedar-policy` crate via PyO3. No sidecar or external service is required — evaluation runs in-process in ~100µs.

For Rust implementations, use the [`cedar-policy`](https://crates.io/crates/cedar-policy) crate directly.

---

## CedarEngine

A minimal evaluation engine for MIP:

```python
"""Cedar policy evaluation engine for MIP."""
import cedarpy
from pathlib import Path
from typing import Any
from dataclasses import dataclass, field

@dataclass
class AuthzDecision:
    allowed: bool
    decision: str
    reasons: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

class CedarEngine:
    """Wraps cedarpy with MIP schema, policy loading, and entity construction."""

    def __init__(self, schema_path: str | Path | None = None):
        self._schema: str | None = None
        self._policies: str = ""

        if schema_path:
            self._schema = Path(schema_path).read_text()

    def load_policies(self, cedar_text: str) -> None:
        """Load Cedar policy text. Validates against schema if loaded."""
        if self._schema:
            result = cedarpy.validate_policies(cedar_text, self._schema)
            if not result.validation_passed:
                errors = [e.error for e in result.errors]
                raise ValueError(f"Cedar policy validation failed: {errors}")
        self._policies = cedar_text

    def is_authorized(
        self,
        principal: str,
        action: str,
        resource: str,
        context: dict[str, Any] | None = None,
        entities: list[dict] | None = None,
    ) -> AuthzDecision:
        """Evaluate a Cedar authorization request."""
        request: dict[str, Any] = {
            "principal": principal,
            "action": action,
            "resource": resource,
        }
        if context:
            request["context"] = context

        result = cedarpy.is_authorized(
            request=request,
            policies=self._policies,
            entities=entities or [],
            schema=self._schema,
        )
        return AuthzDecision(
            allowed=result.allowed,
            decision=result.decision.name,
            reasons=list(result.diagnostics.reasons),
            errors=[str(e) for e in result.diagnostics.errors],
        )
```

Load the MIP Cedar schema on startup:

```python
engine = CedarEngine(schema_path="cedar/mip.cedarschema")
```

---

## Entity Model

MIP entities map to Cedar entity types as follows:

| MIP concept | Cedar entity type |
|-------------|------------------|
| User / human actor | `MIP::User` |
| API key | `MIP::ApiKey` |
| Organization | `MIP::Organization` |
| RBAC role | `MIP::Role` |
| TrustProfile | `MIP::TrustProfile` |
| CredentialTemplate | `MIP::CredentialTemplate` |
| DeploymentProfile | `MIP::DeploymentProfile` |
| Flow / FlowExecution | `MIP::Flow` |
| Application | `MIP::Application` |
| PolicySet | `MIP::PolicySet` |

### Entity builder helpers

```python
def build_user_entity(user_id: str, org_id: str, role: str, status: str = "ACTIVE", email: str = "") -> dict:
    parents = [{"type": "MIP::Organization", "id": org_id}]
    if role:
        parents.append({"type": "MIP::Role", "id": f"{org_id}:{role}"})
    return {
        "uid": {"type": "MIP::User", "id": user_id},
        "attrs": {"status": status, "email": email},
        "parents": parents,
    }

def build_apikey_entity(key_id: str, org_id: str, scope: str, enabled: bool, deployment_id: str | None = None) -> dict:
    parents = [{"type": "MIP::Organization", "id": org_id}]
    if deployment_id:
        parents.append({"type": "MIP::DeploymentProfile", "id": deployment_id})
    return {
        "uid": {"type": "MIP::ApiKey", "id": key_id},
        "attrs": {"scope": scope, "enabled": enabled},
        "parents": parents,
    }

def build_org_entity(org_id: str, status: str = "ACTIVE") -> dict:
    return {
        "uid": {"type": "MIP::Organization", "id": org_id},
        "attrs": {"status": status},
        "parents": [],
    }

def build_role_entity(org_id: str, role_name: str) -> dict:
    return {
        "uid": {"type": "MIP::Role", "id": f"{org_id}:{role_name}"},
        "attrs": {"role_name": role_name},
        "parents": [{"type": "MIP::Organization", "id": org_id}],
    }

def build_resource_entity(resource_type: str, resource_id: str, org_id: str) -> dict:
    """Build any MIP resource entity (CredentialTemplate, TrustProfile, etc.)."""
    return {
        "uid": {"type": f"MIP::{resource_type}", "id": resource_id},
        "attrs": {},
        "parents": [{"type": "MIP::Organization", "id": org_id}],
    }
```

---

## Action Model

MIP actions follow a `resource-domain:verb` convention. Map your API routes to Cedar actions:

| API operation | Cedar action |
|---------------|-------------|
| Read trust profiles / presentation policies / revocation profiles | `MIP::Action::"trust:read"` |
| Write trust profiles / presentation policies / revocation profiles | `MIP::Action::"trust:write"` |
| Admin-delete trust entities | `MIP::Action::"trust:admin"` |
| Read credential templates | `MIP::Action::"templates:read"` |
| Write credential templates | `MIP::Action::"templates:write"` |
| Read flow definitions / executions | `MIP::Action::"flows:read"` |
| Write flow definitions | `MIP::Action::"flows:write"` |
| Start a flow execution | `MIP::Action::"flows:execute"` |
| Issue a credential | `MIP::Action::"credentials:issue"` |
| Verify a credential | `MIP::Action::"credentials:verify"` |
| Read applications | `MIP::Action::"applications:read"` |
| Write / submit applications | `MIP::Action::"applications:write"` |
| Approve an application | `MIP::Action::"applications:approve"` |
| Read API keys | `MIP::Action::"keys:read"` |
| Write API keys | `MIP::Action::"keys:write"` |
| Read org members | `MIP::Action::"users:read"` |
| Invite org members | `MIP::Action::"users:invite"` |
| Read RBAC roles | `MIP::Action::"roles:read"` |
| Write RBAC roles | `MIP::Action::"roles:write"` |
| Read audit events | `MIP::Action::"audit:read"` |
| Read / write notifications | `MIP::Action::"notifications:read"` / `"notifications:send"` |

---

## Gateway Integration Pattern

For an HTTP gateway, evaluate Cedar before forwarding requests to downstream services. Example ASGI middleware:

```python
class CedarAuthMiddleware:
    """ASGI middleware: evaluates Cedar for every org-scoped request."""

    def __init__(self, app, engine: CedarEngine, route_action_map: dict):
        self.app = app
        self.engine = engine
        self.route_action_map = route_action_map

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope, receive, send)

        # Skip public / health routes
        if not requires_authorization(request.url.path):
            return await self.app(scope, receive, send)

        # Auth context must be set by a preceding authentication middleware
        user = request.state.user
        resource_type, action_name = self.route_action_map.get(
            (request.url.path, request.method), (None, None)
        )
        if not resource_type:
            # Unknown route — deny by default
            return await send_403(send, "unknown_route")

        entities = [
            build_user_entity(user.id, user.org_id, user.role, user.status),
            build_org_entity(user.org_id),
            build_role_entity(user.org_id, user.role),
            build_resource_entity(resource_type, request.path_params.get("id", "*"), user.org_id),
        ]

        decision = self.engine.is_authorized(
            principal=f'MIP::User::"{user.id}"',
            action=f'MIP::Action::"{action_name}"',
            resource=f'MIP::{resource_type}::"{request.path_params.get("id", "*")}"',
            context={
                "ip_address": request.client.host,
                "timestamp": int(time.time()),
                "mfa_authenticated": getattr(request.state, "mfa_verified", False),
            },
            entities=entities,
        )

        if not decision.allowed:
            return await send_403(send, f"Cedar denied: {decision.reasons}")

        request.state.cedar_decision = decision
        return await self.app(scope, receive, send)
```

---

## Wiring to Verification and Approval Flows

### Credential Verification Flow

After completing standard trust chain validation (§5.7.3), evaluate the `CREDENTIAL_VERIFICATION` PolicySet referenced by the TrustProfile:

```python
if trust_profile.verification_policy_set_id:
    policy_set = await load_policy_set(trust_profile.verification_policy_set_id)
    engine.load_policies(policy_set.cedar_text)

    decision = engine.is_authorized(
        principal=f'MIP::User::"{verifier_id}"',
        action='MIP::Action::"credentials:verify"',
        resource=f'MIP::Credential::"{credential_id}"',
        context={
            "credential_format": credential.format,
            "compliance_code": credential.compliance_code,
            "issuer_trust_level": issuer_trust_score,
            "is_revoked": credential.is_revoked,
            "is_expired": credential.is_expired,
            "holder_binding_present": holder_binding_verified,
            "algorithm": credential.algorithm,
            "credential_age_seconds": credential_age_seconds,
        },
        entities=entities,
    )

    if not decision.allowed:
        return VerificationResult(status="REJECTED", reasons=decision.reasons)
```

### Application Approval Flow

When `ApplicationTemplate.approval_strategy == "EXTERNAL"` and an `approval_policy_set_id` is set:

```python
if application_template.approval_policy_set_id:
    policy_set = await load_policy_set(application_template.approval_policy_set_id)
    engine.load_policies(policy_set.cedar_text)

    decision = engine.is_authorized(
        principal=f'MIP::ApiKey::"{api_key_id}"',
        action='MIP::Action::"applications:approve"',
        resource=f'MIP::Application::"{application_id}"',
        context={
            "risk_score": application.risk_score,
            "document_verification_passed": application.doc_verified,
            "biometric_match_score": application.biometric_score,
            "evidence_count": len(application.evidence),
            "applicant_country": application.country,
        },
        entities=entities,
    )
```

---

## PolicySet Storage

Implementations must persist and serve PolicySet documents. Minimum required API surface (from §16):

```
GET    /v1/policy-sets              List PolicySets for org
POST   /v1/policy-sets              Create (validates Cedar text against MIP schema)
GET    /v1/policy-sets/{id}         Get PolicySet
PATCH  /v1/policy-sets/{id}         Update (validates before saving)
DELETE /v1/policy-sets/{id}         Delete (if DRAFT status)
POST   /v1/policy-sets/{id}/activate    DRAFT → ACTIVE
POST   /v1/policy-sets/{id}/archive     ACTIVE → ARCHIVED
POST   /v1/policy-sets/{id}/validate    Dry-run: validate Cedar text, return errors
```

Always validate Cedar text against `cedar/mip.cedarschema` before persisting:

```python
result = cedarpy.validate_policies(cedar_text, mip_schema)
if not result.validation_passed:
    raise ValueError([e.error for e in result.errors])
```

Policy caching (if applicable) should be invalidated on any PolicySet create, update, activate, or archive operation.

---

## Configuration

Implementations should support a mode flag to ease migration:

```env
CEDAR_MODE=shadow    # shadow: run Cedar alongside legacy auth; log disagreements
CEDAR_MODE=enforce   # enforce: Cedar is the sole authorization engine
CEDAR_MODE=legacy    # legacy: Cedar disabled; fall back to non-Cedar auth
```

`enforce` is the required mode for a conformant implementation. `shadow` and `legacy` are provided for migration purposes only.

---

## Testing

1. **Unit tests** — Test `CedarEngine` with the MIP schema against each policy domain.
2. **Conformance tests** — All MIP conformance fixtures in `conformance/` must validate with Cedar policies active.
3. **Permit/deny tests** — For each policy in `cedar/policies/`, write test cases asserting expected permit and deny outcomes.
4. **Policy validation tests** — Verify that malformed Cedar text is rejected before persistence.
5. **Performance** — `cedarpy` evaluation targets <1ms p99 under concurrent load; test with your expected request rate.

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `cedarpy` (Python) | ≥4.8.0 | Cedar evaluation (PyO3 wrapper around Rust `cedar-policy`) |
| `cedar-policy` (Rust) | ≥4.0.0 | Cedar evaluation for Rust implementations |

No additional infrastructure is required. Cedar evaluation is in-process.

---

## Reference Policies

See `cedar/policies/` for the reference Cedar policies shipped with MIP:

- `api_access.cedar` — Default RBAC for MIP entity access (owner / admin / member / viewer)
- `credential_verification.cedar` — Example verification trust rules
- `approval_rules.cedar` — Example auto-approval patterns

All reference policies are normative examples. See `cedar/mip.cedarschema` for the full entity/action schema.
