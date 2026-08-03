"""Núcleo persistente compartilhado por todas as regiões de Eudora."""

from .actions import ActionRequest, ActionResult, ActionResolver
from .clock import GameClock
from .events import EventScheduler, ScheduledEvent
from .quests import QuestEngine
from .relationships import RelationshipEngine
from .runtime import PersistentCore
from .world import WorldState

__all__ = [
    "ActionRequest", "ActionResult", "ActionResolver", "EventScheduler",
    "GameClock", "PersistentCore", "QuestEngine", "RelationshipEngine",
    "ScheduledEvent", "WorldState",
]
