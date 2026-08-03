from __future__ import annotations

from copy import deepcopy
from typing import Any

from .clock import GameClock
from .world import WorldState


QUEST_STATUSES = {
    "unknown", "rumored", "discovered", "active", "paused", "blocked",
    "transformed", "completed", "partial", "failed", "abandoned", "expired",
    "resolved_by_world",
}


class QuestEngine:
    """Máquina de estados de missão; definições são dados, progresso pertence ao save."""

    def __init__(
        self,
        state: dict[str, Any],
        clock: GameClock,
        world: WorldState,
        definitions: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        self.state = state
        self.clock = clock
        self.world = world
        self.definitions = definitions or {}
        self.quests: dict[str, dict[str, Any]] = state.setdefault("quests", {})

    def definition(self, quest_id: str) -> dict[str, Any]:
        return self.definitions.get(quest_id, {"id": quest_id, "title": quest_id, "stages": []})

    def get(self, quest_id: str) -> dict[str, Any] | None:
        quest = self.quests.get(quest_id)
        return deepcopy(quest) if quest else None

    def ensure(self, quest_id: str) -> dict[str, Any]:
        if quest_id not in self.quests:
            definition = self.definition(quest_id)
            self.quests[quest_id] = {
                "quest_id": quest_id,
                "title": definition.get("title", quest_id),
                "category": definition.get("category", "side"),
                "status": "unknown",
                "stage": None,
                "outcome": None,
                "objectives": {},
                "discovered_absolute_minute": None,
                "started_absolute_minute": None,
                "updated_absolute_minute": self.clock.absolute_minute,
                "completed_absolute_minute": None,
            }
        return self.quests[quest_id]

    def set_status(
        self,
        quest_id: str,
        status: str,
        *,
        outcome: str | None = None,
        source: str = "system",
    ) -> bool:
        if status not in QUEST_STATUSES:
            raise ValueError(f"Estado de missão desconhecido: {status}")
        quest = self.ensure(quest_id)
        previous = quest["status"]
        if previous == status and (outcome is None or quest.get("outcome") == outcome):
            return False
        quest["status"] = status
        quest["updated_absolute_minute"] = self.clock.absolute_minute
        if status in {"rumored", "discovered"} and quest["discovered_absolute_minute"] is None:
            quest["discovered_absolute_minute"] = self.clock.absolute_minute
        if status == "active" and quest["started_absolute_minute"] is None:
            quest["started_absolute_minute"] = self.clock.absolute_minute
        if status in {"completed", "partial", "failed", "expired", "resolved_by_world"}:
            quest["completed_absolute_minute"] = self.clock.absolute_minute
        if outcome is not None:
            quest["outcome"] = outcome
        self.world.append_history(
            "quest_status_changed", quest_id=quest_id, previous=previous,
            status=status, outcome=outcome, source=source,
        )
        return True

    def discover(self, quest_id: str, *, rumor: bool = False, source: str = "scene") -> bool:
        quest = self.ensure(quest_id)
        if quest["status"] != "unknown":
            return False
        return self.set_status(quest_id, "rumored" if rumor else "discovered", source=source)

    def activate(self, quest_id: str, *, stage: str | None = None, source: str = "scene") -> bool:
        quest = self.ensure(quest_id)
        changed = self.set_status(quest_id, "active", source=source)
        if stage:
            changed = self.set_stage(quest_id, stage, source=source) or changed
        return changed

    def set_stage(self, quest_id: str, stage: str, *, source: str = "system") -> bool:
        quest = self.ensure(quest_id)
        if quest.get("stage") == stage:
            return False
        previous = quest.get("stage")
        quest["stage"] = stage
        quest["updated_absolute_minute"] = self.clock.absolute_minute
        self.world.append_history(
            "quest_stage_changed", quest_id=quest_id, previous=previous,
            stage=stage, source=source,
        )
        return True

    def objective(
        self,
        quest_id: str,
        objective_id: str,
        *,
        status: str = "completed",
        progress: int | float = 1,
        source: str = "system",
    ) -> bool:
        quest = self.ensure(quest_id)
        previous = quest["objectives"].get(objective_id)
        current = {
            "status": status,
            "progress": progress,
            "updated_absolute_minute": self.clock.absolute_minute,
        }
        if previous and previous.get("status") == status and previous.get("progress") == progress:
            return False
        quest["objectives"][objective_id] = current
        quest["updated_absolute_minute"] = self.clock.absolute_minute
        self.world.append_history(
            "quest_objective_changed", quest_id=quest_id,
            objective_id=objective_id, status=status, progress=progress, source=source,
        )
        return True

    def active(self) -> list[dict[str, Any]]:
        visible = {
            "rumored", "discovered", "active", "paused", "blocked", "partial",
        }
        return [deepcopy(item) for item in self.quests.values() if item.get("status") in visible]

    def finished(self) -> list[dict[str, Any]]:
        visible = {"completed", "failed", "expired", "resolved_by_world", "transformed"}
        return [deepcopy(item) for item in self.quests.values() if item.get("status") in visible]

    def journal(self) -> list[dict[str, Any]]:
        return sorted(
            (deepcopy(item) for item in self.quests.values() if item.get("status") != "unknown"),
            key=lambda item: int(item.get("updated_absolute_minute") or 0),
            reverse=True,
        )
