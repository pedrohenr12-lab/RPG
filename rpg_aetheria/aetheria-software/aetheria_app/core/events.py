from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from typing import Any

from .clock import GameClock
from .world import WorldState


@dataclass
class ScheduledEvent:
    event_id: str
    event_type: str
    due_absolute_minute: int
    title: str
    description: str
    payload: dict[str, Any] = field(default_factory=dict)
    condition: dict[str, Any] = field(default_factory=dict)
    effects: list[dict[str, Any]] = field(default_factory=list)
    status: str = "scheduled"
    created_absolute_minute: int = 0
    resolved_absolute_minute: int | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "ScheduledEvent":
        allowed = cls.__dataclass_fields__
        return cls(**{key: value for key, value in raw.items() if key in allowed})

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EventScheduler:
    """Agenda consequências que continuam avançando sem depender da cena aberta."""

    def __init__(self, state: dict[str, Any], clock: GameClock, world: WorldState):
        self.state = state
        self.clock = clock
        self.world = world
        self.events: list[dict[str, Any]] = state.setdefault("scheduled_events", [])

    def schedule(
        self,
        event_type: str,
        *,
        in_minutes: int,
        title: str,
        description: str,
        payload: dict[str, Any] | None = None,
        condition: dict[str, Any] | None = None,
        effects: list[dict[str, Any]] | None = None,
        unique_key: str | None = None,
    ) -> str:
        unique_key = unique_key or ""
        if unique_key:
            for raw in self.events:
                if raw.get("status") == "scheduled" and raw.get("payload", {}).get("unique_key") == unique_key:
                    return str(raw["event_id"])
        event_id = f"evt_{uuid.uuid4().hex[:16]}"
        event_payload = dict(payload or {})
        if unique_key:
            event_payload["unique_key"] = unique_key
        event = ScheduledEvent(
            event_id=event_id,
            event_type=event_type,
            due_absolute_minute=self.clock.absolute_minute + max(0, int(in_minutes)),
            title=title,
            description=description,
            payload=event_payload,
            condition=dict(condition or {}),
            effects=list(effects or []),
            created_absolute_minute=self.clock.absolute_minute,
        )
        self.events.append(event.to_dict())
        self.world.append_history(
            "event_scheduled", event_id=event_id, scheduled_type=event_type,
            due_absolute_minute=event.due_absolute_minute, title=title,
        )
        return event_id

    def cancel(self, *, event_id: str | None = None, unique_key: str | None = None) -> int:
        cancelled = 0
        for raw in self.events:
            matches = event_id and raw.get("event_id") == event_id
            matches = matches or (unique_key and raw.get("payload", {}).get("unique_key") == unique_key)
            if matches and raw.get("status") == "scheduled":
                raw["status"] = "cancelled"
                raw["resolved_absolute_minute"] = self.clock.absolute_minute
                cancelled += 1
        return cancelled

    def pending(self) -> list[ScheduledEvent]:
        return sorted(
            (ScheduledEvent.from_dict(raw) for raw in self.events if raw.get("status") == "scheduled"),
            key=lambda item: item.due_absolute_minute,
        )

    def process_due(self) -> list[ScheduledEvent]:
        resolved: list[ScheduledEvent] = []
        for raw in self.events:
            if raw.get("status") != "scheduled":
                continue
            event = ScheduledEvent.from_dict(raw)
            if event.due_absolute_minute > self.clock.absolute_minute:
                continue
            if event.condition and not self.world.check(event.condition):
                raw["status"] = "skipped"
                raw["resolved_absolute_minute"] = self.clock.absolute_minute
                self.world.append_history(
                    "event_skipped", event_id=event.event_id, scheduled_type=event.event_type,
                )
                continue
            for effect in event.effects:
                self._apply_effect(effect, event)
            raw["status"] = "resolved"
            raw["resolved_absolute_minute"] = self.clock.absolute_minute
            event.status = "resolved"
            event.resolved_absolute_minute = self.clock.absolute_minute
            resolved.append(event)
            self.world.append_history(
                "event_resolved", event_id=event.event_id,
                scheduled_type=event.event_type, title=event.title,
            )
        return resolved

    def _apply_effect(self, effect: dict[str, Any], event: ScheduledEvent) -> None:
        kind = effect.get("type")
        if kind == "set_fact":
            self.world.set(
                str(effect["key"]), effect.get("value"),
                category=str(effect.get("category") or "event"),
                source=event.event_id,
                certainty=str(effect.get("certainty") or "confirmed"),
                visibility=str(effect.get("visibility") or "character"),
                description=str(effect.get("description") or event.description),
            )
        elif kind == "increment_fact":
            self.world.increment(
                str(effect["key"]), effect.get("amount", 1), source=event.event_id,
            )

    def prune(self, keep_resolved: int = 300) -> None:
        active = [raw for raw in self.events if raw.get("status") == "scheduled"]
        finished = [raw for raw in self.events if raw.get("status") != "scheduled"]
        finished.sort(key=lambda raw: int(raw.get("resolved_absolute_minute") or 0))
        self.events[:] = finished[-keep_resolved:] + active
