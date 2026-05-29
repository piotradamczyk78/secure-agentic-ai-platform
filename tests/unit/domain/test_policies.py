from secure_agentic_ai.domain.actors import Actor, ActorType
from secure_agentic_ai.domain.policies import (
    Action,
    ActionType,
    PolicyDecision,
    RiskLevel,
    evaluate_policy,
)


def test_low_risk_human_action_is_allowed() -> None:
    actor = Actor(
        actor_id="human-001",
        actor_type=ActorType.HUMAN,
        display_name="Developer",
    )
    action = Action(
        action_type=ActionType.CREATE_CONTENT,
        risk_level=RiskLevel.LOW,
        description="Create draft documentation",
    )

    evaluation = evaluate_policy(actor, action)

    assert evaluation.decision is PolicyDecision.ALLOW


def test_high_risk_agent_action_requires_approval() -> None:
    actor = Actor(
        actor_id="agent-001",
        actor_type=ActorType.AGENT,
        display_name="Developer Agent",
    )
    action = Action(
        action_type=ActionType.WRITE_FILE,
        risk_level=RiskLevel.HIGH,
        description="Write a generated file",
    )

    evaluation = evaluate_policy(actor, action)

    assert evaluation.decision is PolicyDecision.REQUIRE_APPROVAL


def test_agent_secret_resolution_is_denied() -> None:
    actor = Actor(
        actor_id="agent-001",
        actor_type=ActorType.AGENT,
        display_name="Developer Agent",
    )
    action = Action(
        action_type=ActionType.RESOLVE_SECRET,
        risk_level=RiskLevel.HIGH,
        description="Resolve provider token",
    )

    evaluation = evaluate_policy(actor, action)

    assert evaluation.decision is PolicyDecision.DENY
