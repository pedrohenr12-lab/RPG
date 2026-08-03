from __future__ import annotations

import random
from dataclasses import asdict, dataclass, field
from typing import Any

from ..models import PlayerSession
from .clock import GameClock
from .world import WorldState


DEGREES = ("critical_failure", "failure", "success", "critical_success")


@dataclass
class ActionRequest:
    action_id: str
    label: str
    attribute: str | None = None
    difficulty: int | None = None
    duration_minutes: int = 0
    energy_delta: int = 0
    hunger_delta: int = 0
    thirst_delta: int = 0
    modifiers: list[dict[str, Any]] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionResult:
    action_id: str
    degree: str
    automatic: bool
    die: int | None
    bonus: int
    modifier: int
    total: int | None
    difficulty: int | None
    duration_minutes: int
    reasons: list[str]

    @property
    def success(self) -> bool:
        return self.degree in {"success", "critical_success"}

    @property
    def label(self) -> str:
        return {
            "critical_failure": "Falha crítica",
            "failure": "Falha",
            "success": "Sucesso",
            "critical_success": "Sucesso crítico",
        }[self.degree]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ActionResolver:
    """Resolve apenas incerteza interessante; ações sem dificuldade são automáticas."""

    def __init__(
        self,
        session: PlayerSession,
        clock: GameClock,
        world: WorldState,
        rng: random.Random | None = None,
    ) -> None:
        self.session = session
        self.clock = clock
        self.world = world
        self.rng = rng or random.Random()

    @staticmethod
    def _step(degree: str, amount: int) -> str:
        index = max(0, min(len(DEGREES) - 1, DEGREES.index(degree) + amount))
        return DEGREES[index]

    def resolve(self, request: ActionRequest) -> ActionResult:
        bonus = int(self.session.attributes.get(request.attribute or "", 0))
        modifier = 0
        reasons: list[str] = []
        for entry in request.modifiers:
            value = int(entry.get("value") or 0)
            modifier += value
            if value:
                reasons.append(f"{entry.get('reason', 'circunstância')}: {value:+d}")

        die: int | None = None
        total: int | None = None
        automatic = request.difficulty is None
        if automatic:
            degree = "success"
        else:
            die = self.rng.randint(1, 20)
            total = die + bonus + modifier
            difference = total - int(request.difficulty)
            if difference >= 10:
                degree = "critical_success"
            elif difference >= 0:
                degree = "success"
            elif difference <= -10:
                degree = "critical_failure"
            else:
                degree = "failure"
            if die == 20:
                degree = self._step(degree, 1)
                reasons.append("20 natural melhora o grau do resultado")
            elif die == 1:
                degree = self._step(degree, -1)
                reasons.append("1 natural piora o grau do resultado")

        self.clock.advance(request.duration_minutes)
        if request.energy_delta:
            self.session.change_need("energy", request.energy_delta)
        if request.hunger_delta:
            self.session.change_need("hunger", request.hunger_delta)
        if request.thirst_delta:
            self.session.change_need("thirst", request.thirst_delta)

        result = ActionResult(
            action_id=request.action_id,
            degree=degree,
            automatic=automatic,
            die=die,
            bonus=bonus,
            modifier=modifier,
            total=total,
            difficulty=request.difficulty,
            duration_minutes=max(0, int(request.duration_minutes)),
            reasons=reasons,
        )
        self.world.append_history(
            "action_resolved",
            action=request.action_id,
            label=request.label,
            attribute=request.attribute,
            result=result.to_dict(),
            context=request.context,
        )
        return result

    @staticmethod
    def format_result(result: ActionResult, attribute_label: str = "teste") -> str:
        if result.automatic:
            return f"{result.label}: a ação não exigiu teste. Tempo: {result.duration_minutes} min."
        modifier = f" {result.modifier:+d}" if result.modifier else ""
        reasons = f" ({'; '.join(result.reasons)})" if result.reasons else ""
        return (
            f"D20: {result.die} + {result.bonus}{modifier} = {result.total}, "
            f"dificuldade {result.difficulty}. {result.label} em {attribute_label}.{reasons}"
        )
