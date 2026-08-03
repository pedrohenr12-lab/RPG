from __future__ import annotations

from copy import deepcopy
from typing import Any

from .clock import GameClock


class WorldState:
    """Fatos tipados e histórico semântico da campanha."""

    def __init__(self, state: dict[str, Any], clock: GameClock):
        self.state = state
        self.clock = clock
        self.facts: dict[str, dict[str, Any]] = state.setdefault("facts", {})
        self.history: list[dict[str, Any]] = state.setdefault("history", [])

    def has(self, key: str) -> bool:
        return key in self.facts

    def get(self, key: str, default: Any = None) -> Any:
        record = self.facts.get(key)
        return default if record is None else record.get("value", default)

    def record(self, key: str) -> dict[str, Any] | None:
        item = self.facts.get(key)
        return deepcopy(item) if item is not None else None

    def set(
        self,
        key: str,
        value: Any,
        *,
        category: str = "world",
        source: str = "system",
        certainty: str = "confirmed",
        visibility: str = "character",
        description: str = "",
    ) -> bool:
        previous = self.facts.get(key)
        if previous and previous.get("value") == value:
            return False
        now = self.clock.now
        self.facts[key] = {
            "value": value,
            "category": category,
            "source": source,
            "certainty": certainty,
            "visibility": visibility,
            "description": description,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute,
            "absolute_minute": now.absolute_minute,
        }
        self.append_history(
            "fact_changed",
            key=key,
            value=value,
            previous=None if previous is None else previous.get("value"),
            source=source,
            description=description,
        )
        return True

    def remove(self, key: str, *, source: str = "system") -> bool:
        if key not in self.facts:
            return False
        previous = self.facts.pop(key)
        self.append_history(
            "fact_removed", key=key, previous=previous.get("value"), source=source,
        )
        return True

    def increment(
        self,
        key: str,
        amount: int | float = 1,
        *,
        category: str = "counter",
        source: str = "system",
    ) -> int | float:
        value = self.get(key, 0)
        if not isinstance(value, (int, float)):
            raise TypeError(f"O fato {key!r} não é numérico.")
        result = value + amount
        self.set(key, result, category=category, source=source)
        return result

    def append_history(self, event_type: str, **payload: Any) -> dict[str, Any]:
        now = self.clock.now
        event = {
            "type": event_type,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute,
            "absolute_minute": now.absolute_minute,
            **payload,
        }
        self.history.append(event)
        # A campanha pode ser longa. O log completo fica no MySQL; o save guarda uma janela útil.
        if len(self.history) > 2000:
            del self.history[: len(self.history) - 2000]
        return event

    def check(self, condition: dict[str, Any] | None) -> bool:
        if not condition:
            return True
        if "all" in condition:
            return all(self.check(item) for item in condition.get("all") or [])
        if "any" in condition:
            return any(self.check(item) for item in condition.get("any") or [])
        if "not" in condition:
            return not self.check(condition.get("not"))
        key = str(condition.get("fact") or "")
        if not key:
            return True
        exists = self.has(key)
        if "exists" in condition and exists != bool(condition["exists"]):
            return False
        if not exists:
            return False
        current = self.get(key)
        if "equals" in condition and current != condition["equals"]:
            return False
        if "not_equals" in condition and current == condition["not_equals"]:
            return False
        if "minimum" in condition and current < condition["minimum"]:
            return False
        if "maximum" in condition and current > condition["maximum"]:
            return False
        return True

    def migrate_flags(self, flags: set[str]) -> int:
        migrated = 0
        for flag in sorted(flags):
            key = f"legacy.flag.{flag}"
            if key not in self.facts:
                self.set(
                    key, True, category="legacy", source="save_v1",
                    visibility="system", description="Flag migrada de um save anterior.",
                )
                migrated += 1
        return migrated
