from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import StrEnum

from secure_agentic_ai.domain.actors import Actor
from secure_agentic_ai.domain.policies import Action


class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    FAILED = "failed"


_ALLOWED_TRANSITIONS: dict[ApprovalStatus, frozenset[ApprovalStatus]] = {
    ApprovalStatus.PENDING: frozenset(
        {
            ApprovalStatus.APPROVED,
            ApprovalStatus.REJECTED,
        }
    ),
    ApprovalStatus.APPROVED: frozenset(
        {
            ApprovalStatus.EXECUTED,
            ApprovalStatus.FAILED,
        }
    ),
    ApprovalStatus.REJECTED: frozenset(),
    ApprovalStatus.EXECUTED: frozenset(),
    ApprovalStatus.FAILED: frozenset(),
}


class InvalidApprovalTransitionError(Exception):
    """Raised when an approval request cannot move to the requested status."""


@dataclass(frozen=True)
class ApprovalRequest:
    request_id: str
    action: Action
    requested_by: Actor
    status: ApprovalStatus = ApprovalStatus.PENDING
    requested_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    decided_at: datetime | None = None

    def transition_to(self, new_status: ApprovalStatus) -> "ApprovalRequest":
        if new_status not in _ALLOWED_TRANSITIONS[self.status]:
            raise InvalidApprovalTransitionError(f"Invalid status transition from {self.status} to {new_status}")

        return replace(
            self,
            status=new_status,
            decided_at=datetime.now(UTC),
        )

    def approve(self) -> "ApprovalRequest":
        return self.transition_to(ApprovalStatus.APPROVED)

    def reject(self) -> "ApprovalRequest":
        return self.transition_to(ApprovalStatus.REJECTED)

    def mark_executed(self) -> "ApprovalRequest":
        return self.transition_to(ApprovalStatus.EXECUTED)

    def mark_failed(self) -> "ApprovalRequest":
        return self.transition_to(ApprovalStatus.FAILED)
