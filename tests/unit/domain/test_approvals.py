import pytest

from secure_agentic_ai.domain.actors import Actor, ActorType
from secure_agentic_ai.domain.approvals import (
    ApprovalRequest,
    ApprovalStatus,
    InvalidApprovalTransitionError,
)
from secure_agentic_ai.domain.policies import Action, ActionType, RiskLevel


def test_approval_request_can_be_approved() -> None:
    request = ApprovalRequest(
        request_id="req-001",
        action=Action(
            action_type=ActionType.RUN_COMMAND,
            risk_level=RiskLevel.HIGH,
            description="Run local test command",
        ),
        requested_by=Actor(
            actor_id="agent-001",
            actor_type=ActorType.AGENT,
            display_name="Developer Agent",
        ),
    )

    approved_request = request.approve()

    assert request.status is ApprovalStatus.PENDING
    assert approved_request.status is ApprovalStatus.APPROVED
    assert approved_request.decided_at is not None


def test_approval_request_rejects_invalid_transition() -> None:
    request = ApprovalRequest(
        request_id="req-001",
        action=Action(
            action_type=ActionType.RUN_COMMAND,
            risk_level=RiskLevel.HIGH,
            description="Run local test command",
        ),
        requested_by=Actor(
            actor_id="agent-001",
            actor_type=ActorType.AGENT,
            display_name="Developer Agent",
        ),
    ).approve()

    with pytest.raises(InvalidApprovalTransitionError):
        request.reject()
