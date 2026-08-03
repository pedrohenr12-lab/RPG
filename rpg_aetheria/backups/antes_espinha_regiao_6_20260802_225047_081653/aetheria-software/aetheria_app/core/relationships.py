from __future__ import annotations

from copy import deepcopy
from typing import Any

from .clock import GameClock
from .world import WorldState


RELATIONSHIP_AXES = {"trust", "respect", "warmth", "fear", "resentment"}


class RelationshipEngine:
    """Relações multidimensionais com memórias e autoria do NPC."""

    def __init__(self, state: dict[str, Any], clock: GameClock, world: WorldState):
        self.state = state
        self.clock = clock
        self.world = world
        self.relationships: dict[str, dict[str, Any]] = state.setdefault("relationships", {})

    def ensure(
        self,
        npc_id: str,
        *,
        name: str | None = None,
        faction: str | None = None,
        values: list[str] | None = None,
        red_lines: list[str] | None = None,
    ) -> dict[str, Any]:
        relation = self.relationships.setdefault(
            npc_id,
            {
                "npc_id": npc_id,
                "name": name or npc_id,
                "faction": faction,
                "trust": 0,
                "respect": 0,
                "warmth": 0,
                "fear": 0,
                "resentment": 0,
                "met": False,
                "status": "unknown",
                "values": list(values or []),
                "red_lines": list(red_lines or []),
                "memories": [],
                "last_interaction": None,
            },
        )
        if name:
            relation["name"] = name
        if faction:
            relation["faction"] = faction
        if values:
            relation["values"] = list(values)
        if red_lines:
            relation["red_lines"] = list(red_lines)
        return relation

    def meet(self, npc_id: str, **identity: Any) -> dict[str, Any]:
        relation = self.ensure(npc_id, **identity)
        if not relation["met"]:
            relation["met"] = True
            relation["status"] = "acquaintance"
            relation["last_interaction"] = self.clock.absolute_minute
            self.world.append_history("relationship_met", npc_id=npc_id, name=relation["name"])
        return deepcopy(relation)

    def change(
        self,
        npc_id: str,
        axis: str,
        amount: int,
        *,
        reason: str,
        source: str = "system",
        name: str | None = None,
        faction: str | None = None,
        values: list[str] | None = None,
        red_lines: list[str] | None = None,
    ) -> dict[str, Any]:
        if axis not in RELATIONSHIP_AXES:
            raise ValueError(f"Eixo de relação desconhecido: {axis}")
        relation = self.ensure(
            npc_id, name=name, faction=faction, values=values, red_lines=red_lines,
        )
        relation["met"] = True
        previous = int(relation.get(axis, 0))
        relation[axis] = max(-100, min(100, previous + int(amount)))
        relation["last_interaction"] = self.clock.absolute_minute
        self.remember(npc_id, reason, source=source, axis=axis, amount=int(amount))
        relation["status"] = self._status(relation)
        self.world.append_history(
            "relationship_changed",
            npc_id=npc_id,
            axis=axis,
            previous=previous,
            value=relation[axis],
            amount=int(amount),
            reason=reason,
            source=source,
            status=relation["status"],
        )
        return deepcopy(relation)

    def apply(
        self,
        npc_id: str,
        changes: dict[str, int],
        *,
        reason: str,
        source: str = "system",
        **identity: Any,
    ) -> dict[str, Any]:
        relation = self.ensure(npc_id, **identity)
        for axis, amount in changes.items():
            if axis not in RELATIONSHIP_AXES or not amount:
                continue
            relation = self.change(
                npc_id, axis, amount, reason=reason, source=source, **identity,
            )
        return deepcopy(relation)

    def remember(
        self,
        npc_id: str,
        text: str,
        *,
        source: str = "system",
        axis: str | None = None,
        amount: int = 0,
    ) -> None:
        relation = self.ensure(npc_id)
        relation["memories"].append(
            {
                "text": text,
                "source": source,
                "axis": axis,
                "amount": int(amount),
                "day": self.clock.now.day,
                "hour": self.clock.now.hour,
                "minute": self.clock.now.minute,
                "absolute_minute": self.clock.absolute_minute,
            }
        )
        if len(relation["memories"]) > 100:
            del relation["memories"][:-100]

    def get(self, npc_id: str) -> dict[str, Any] | None:
        relation = self.relationships.get(npc_id)
        return deepcopy(relation) if relation else None

    def all_known(self) -> list[dict[str, Any]]:
        return sorted(
            (deepcopy(item) for item in self.relationships.values() if item.get("met")),
            key=lambda item: int(item.get("last_interaction") or 0),
            reverse=True,
        )

    @staticmethod
    def _status(relation: dict[str, Any]) -> str:
        trust = int(relation.get("trust", 0))
        respect = int(relation.get("respect", 0))
        warmth = int(relation.get("warmth", 0))
        fear = int(relation.get("fear", 0))
        resentment = int(relation.get("resentment", 0))
        if resentment >= 60 and trust <= -35:
            return "enemy"
        if fear >= 65 and trust <= -15:
            return "afraid"
        if resentment >= 30 or trust <= -30:
            return "hostile"
        if trust >= 65 and respect >= 45 and warmth >= 45:
            return "devoted"
        if trust >= 40 and (respect >= 30 or warmth >= 35):
            return "trusted"
        if warmth >= 25 or trust >= 20 or respect >= 25:
            return "friendly"
        if trust <= -10 or resentment >= 15:
            return "wary"
        return "acquaintance"
