"""Smoke tests for Canvas approval PolicySet examples."""

from __future__ import annotations

import os
import sys

import pytest

from .helpers import REPO_ROOT

pytest.importorskip("cedarpy")

_MARTY_COMMON_PACKAGES = REPO_ROOT.parent / "marty-ui" / "packages"
if os.path.isdir(_MARTY_COMMON_PACKAGES) and str(_MARTY_COMMON_PACKAGES) not in sys.path:
    sys.path.insert(0, str(_MARTY_COMMON_PACKAGES))

from marty_common import CedarEngine  # noqa: E402


_POLICY_PATH = REPO_ROOT / "cedar" / "policies" / "canvas_approval_examples.cedar"


def _engine() -> CedarEngine:
    return CedarEngine.with_approval_policy_text(_POLICY_PATH.read_text())


def _entities() -> list[dict]:
    return [
        {
            "uid": {"type": "MIP::ServiceAccount", "id": "canvas-evidence-policy"},
            "attrs": {"service_name": "canvas-evidence-policy"},
            "parents": [{"type": "MIP::Organization", "id": "org-1"}],
        },
        {
            "uid": {"type": "MIP::Organization", "id": "org-1"},
            "attrs": {},
            "parents": [],
        },
        {
            "uid": {"type": "MIP::Application", "id": "app-1"},
            "attrs": {"risk_score": 0, "status": "pending"},
            "parents": [{"type": "MIP::Organization", "id": "org-1"}],
        },
    ]


def _context(fact_type: str, **overrides) -> dict:
    context = {
        "risk_score": 0,
        "document_verification_passed": True,
        "biometric_match_score": 100,
        "evidence_count": 1,
        "applicant_country": "US",
        "evidence_provider": "canvas",
        "evidence_fact_type": fact_type,
        "evidence_verification_status": "VERIFIED",
        "evidence_scope_matched": True,
        "verified_evidence_count": 1,
        "required_evidence_count": 1,
        "satisfied_requirement_count": 1,
        "all_required_evidence_satisfied": True,
        "auto_issue_eligible": True,
    }
    context.update(overrides)
    return context


def _decide(context: dict):
    return _engine().is_authorized(
        principal='MIP::ServiceAccount::"canvas-evidence-policy"',
        action='MIP::Action::"applications:approve"',
        resource='MIP::Application::"app-1"',
        context=context,
        entities=_entities(),
    )


@pytest.mark.parametrize(
    "fact_type",
    [
        "canvas.course_completion",
        "canvas.assignment_completion",
        "canvas.assignment_score",
        "canvas.quiz_completion",
        "canvas.quiz_score",
        "canvas.module_completion",
        "canvas.manual_instructor_approval",
    ],
)
def test_canvas_policy_examples_permit_verified_satisfied_fact_type(fact_type: str) -> None:
    decision = _decide(_context(fact_type))

    assert decision.allowed is True
    assert decision.errors == []


def test_canvas_policy_examples_deny_unverified_evidence() -> None:
    decision = _decide(
        _context(
            "canvas.course_completion",
            evidence_verification_status="UNVERIFIED",
        )
    )

    assert decision.allowed is False


def test_canvas_policy_examples_deny_wrong_scope() -> None:
    decision = _decide(
        _context(
            "canvas.assignment_score",
            evidence_scope_matched=False,
        )
    )

    assert decision.allowed is False


def test_canvas_policy_examples_deny_unsatisfied_requirement() -> None:
    decision = _decide(
        _context(
            "canvas.quiz_score",
            satisfied_requirement_count=0,
            all_required_evidence_satisfied=False,
        )
    )

    assert decision.allowed is False
