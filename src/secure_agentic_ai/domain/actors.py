from dataclasses import dataclass
from enum import StrEnum


class ActorType(StrEnum):
    HUMAN = "human"
    AGENT = "agent"


@dataclass(frozen=True)
class Actor:
    actor_id: str
    actor_type: ActorType
    display_name: str
