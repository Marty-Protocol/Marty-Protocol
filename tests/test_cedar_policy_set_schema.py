"""Cedar schema coverage for PolicySet governance and approval duties."""

from __future__ import annotations

import json

import pytest

from .helpers import REPO_ROOT

cedarpy = pytest.importorskip("cedarpy")


def _schema() -> str:
    return (REPO_ROOT / "cedar" / "mip.cedarschema").read_text()


def _assert_valid(policy_text: str) -> None:
    result = cedarpy.validate_policies(policy_text, _schema())
    errors = [str(error) for error in (getattr(result, "errors", []) or [])]
    assert errors == []


def test_policy_set_entity_and_lifecycle_actions_validate() -> None:
    _assert_valid(
        """
        @id("policy-set-lifecycle")
        permit (
            principal is MIP::User,
            action in [
                MIP::Action::"policy_sets:read",
                MIP::Action::"policy_sets:update",
                MIP::Action::"policy_sets:delete",
                MIP::Action::"policy_sets:activate",
                MIP::Action::"policy_sets:archive",
                MIP::Action::"policy_sets:validate"
            ],
            resource is MIP::PolicySet
        )
        when {
            resource.status != "ARCHIVED"
        };
        """
    )


def test_policy_set_create_action_validates_against_organization_resource() -> None:
    _assert_valid(
        """
        @id("policy-set-create")
        permit (
            principal is MIP::User,
            action == MIP::Action::"policy_sets:create",
            resource is MIP::Organization
        );
        """
    )


def test_approval_policy_can_deny_self_approval() -> None:
    policy_text = """
    @id("deny-self-approval")
    forbid (
        principal is MIP::User,
        action == MIP::Action::"applications:approve",
        resource is MIP::Application
    )
    when {
        principal has user_id &&
        (
            (resource has submitted_by && principal.user_id == resource.submitted_by) ||
            (resource has created_by && principal.user_id == resource.created_by)
        )
    };

    @id("allow-low-risk-reviewer")
    permit (
        principal is MIP::User,
        action == MIP::Action::"applications:approve",
        resource is MIP::Application
    )
    when {
        context.risk_score < 20 &&
        context.document_verification_passed &&
        context.biometric_match_score >= 80 &&
        context.evidence_count >= 1
    };
    """
    _assert_valid(policy_text)

    context = {
        "risk_score": 0,
        "document_verification_passed": True,
        "biometric_match_score": 100,
        "evidence_count": 1,
        "applicant_country": "US",
    }
    entities = [
        {
            "uid": {"type": "MIP::User", "id": "submitter"},
            "attrs": {"email": "submitter@example.com", "status": "ACTIVE", "user_id": "user-1"},
            "parents": [{"type": "MIP::Organization", "id": "org-1"}],
        },
        {
            "uid": {"type": "MIP::User", "id": "reviewer"},
            "attrs": {"email": "reviewer@example.com", "status": "ACTIVE", "user_id": "user-2"},
            "parents": [{"type": "MIP::Organization", "id": "org-1"}],
        },
        {
            "uid": {"type": "MIP::Organization", "id": "org-1"},
            "attrs": {},
            "parents": [],
        },
        {
            "uid": {"type": "MIP::Application", "id": "app-1"},
            "attrs": {"risk_score": 0, "status": "PENDING", "submitted_by": "user-1"},
            "parents": [{"type": "MIP::Organization", "id": "org-1"}],
        },
    ]

    self_result = cedarpy.is_authorized(
        {
            "principal": 'MIP::User::"submitter"',
            "action": 'MIP::Action::"applications:approve"',
            "resource": 'MIP::Application::"app-1"',
            "context": context,
        },
        policy_text,
        json.dumps(entities),
        _schema(),
    )
    reviewer_result = cedarpy.is_authorized(
        {
            "principal": 'MIP::User::"reviewer"',
            "action": 'MIP::Action::"applications:approve"',
            "resource": 'MIP::Application::"app-1"',
            "context": context,
        },
        policy_text,
        json.dumps(entities),
        _schema(),
    )

    assert self_result.allowed is False
    assert reviewer_result.allowed is True


def test_approval_policy_can_deny_application_creator_approval() -> None:
    policy_text = """
    @id("deny-self-approval")
    forbid (
        principal is MIP::User,
        action == MIP::Action::"applications:approve",
        resource is MIP::Application
    )
    when {
        principal has user_id &&
        (
            (resource has submitted_by && principal.user_id == resource.submitted_by) ||
            (resource has created_by && principal.user_id == resource.created_by)
        )
    };

    @id("allow-low-risk-reviewer")
    permit (
        principal is MIP::User,
        action == MIP::Action::"applications:approve",
        resource is MIP::Application
    )
    when {
        context.risk_score < 20 &&
        context.document_verification_passed &&
        context.biometric_match_score >= 80 &&
        context.evidence_count >= 1
    };
    """
    _assert_valid(policy_text)

    result = cedarpy.is_authorized(
        {
            "principal": 'MIP::User::"creator"',
            "action": 'MIP::Action::"applications:approve"',
            "resource": 'MIP::Application::"app-1"',
            "context": {
                "risk_score": 0,
                "document_verification_passed": True,
                "biometric_match_score": 100,
                "evidence_count": 1,
                "applicant_country": "US",
            },
        },
        policy_text,
        json.dumps(
            [
                {
                    "uid": {"type": "MIP::User", "id": "creator"},
                    "attrs": {"email": "creator@example.com", "status": "ACTIVE", "user_id": "user-1"},
                    "parents": [{"type": "MIP::Organization", "id": "org-1"}],
                },
                {
                    "uid": {"type": "MIP::Organization", "id": "org-1"},
                    "attrs": {},
                    "parents": [],
                },
                {
                    "uid": {"type": "MIP::Application", "id": "app-1"},
                    "attrs": {"risk_score": 0, "status": "PENDING", "created_by": "user-1"},
                    "parents": [{"type": "MIP::Organization", "id": "org-1"}],
                },
            ]
        ),
        _schema(),
    )

    assert result.allowed is False
