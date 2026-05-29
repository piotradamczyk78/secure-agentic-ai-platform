from dataclasses import dataclass
from enum import StrEnum

from secure_agentic_ai.domain.actors import Actor, ActorType


class ActionType(StrEnum):
    READ_CONTEXT = "context.read"
    CREATE_CONTENT = "content.create"
    WRITE_FILE = "file.write"
    SEND_NOTIFICATION = "notification.send"
    RUN_COMMAND = "command.run"
    RESOLVE_SECRET = "secret.resolve"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PolicyDecision(StrEnum):
    ALLOW = "allow"
    REQUIRE_APPROVAL = "require_approval"
    DENY = "deny"


@dataclass(frozen=True)
class Action:
    action_type: ActionType
    risk_level: RiskLevel
    description: str


@dataclass(frozen=True)
class PolicyEvaluation:
    decision: PolicyDecision
    reason: str


def evaluate_policy(actor: Actor, action: Action) -> PolicyEvaluation:
    if actor.actor_type is ActorType.AGENT and action.action_type is ActionType.RESOLVE_SECRET:
        return PolicyEvaluation(
            decision=PolicyDecision.DENY,
            reason="Agents cannot resolve secrets directly",
        )

    if actor.actor_type is ActorType.AGENT and action.risk_level is RiskLevel.HIGH:
        return PolicyEvaluation(
            decision=PolicyDecision.REQUIRE_APPROVAL,
            reason="High-risk agent actions require human approval",
        )

    if actor.actor_type is ActorType.AGENT and action.action_type is ActionType.RUN_COMMAND:
        return PolicyEvaluation(
            decision=PolicyDecision.REQUIRE_APPROVAL,
            reason="Agent command execution requires human approval",
        )

    return PolicyEvaluation(
        decision=PolicyDecision.ALLOW,
        reason="Action is allowed by the baseline domain policy",
    )
