from __future__ import annotations

import random
import re
import unicodedata
from typing import Any

from ..models import PlayerSession
from .actions import ActionRequest, ActionResolver, ActionResult
from .clock import GameClock
from .events import EventScheduler, ScheduledEvent
from .quests import QuestEngine
from .relationships import RelationshipEngine
from .world import WorldState


CORE_SCHEMA_VERSION = 3
TOVIN_QUEST = "frostreach_o_barco_que_voltou_sozinho"
ELDORWOOD_ROOT_QUEST = "eldorwood_as_folhas_pronunciam_nomes"
TERMINAL_QUEST_STATUSES = {
    "completed", "failed", "expired", "resolved_by_world", "transformed",
}


def _slug(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    plain = "".join(char for char in normalized if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "_", plain.casefold()).strip("_")


class PersistentCore:
    """Fachada única usada pela interface, exploração e futuras regiões."""

    def __init__(
        self,
        session: PlayerSession,
        quest_definitions: dict[str, dict[str, Any]] | None = None,
        rng: random.Random | None = None,
    ) -> None:
        self.session = session
        self.state = session.core_state
        self.state.setdefault("schema_version", CORE_SCHEMA_VERSION)
        self.state.setdefault("decisions", [])
        self.state.setdefault("notifications", [])
        self.state.setdefault("visited_scenes", {})
        self.clock = GameClock(session)
        self.world = WorldState(self.state, self.clock)
        self.scheduler = EventScheduler(self.state, self.clock, self.world)
        self.quests = QuestEngine(
            self.state, self.clock, self.world, quest_definitions or {},
        )
        self.relationships = RelationshipEngine(self.state, self.clock, self.world)
        self.actions = ActionResolver(session, self.clock, self.world, rng=rng)
        self._migrate()

    def _migrate(self) -> None:
        previous = int(self.state.get("schema_version") or 1)
        if previous < CORE_SCHEMA_VERSION or not self.world.has("system.core_v2_initialized"):
            migrated = self.world.migrate_flags(self.session.flags)
            self.world.set(
                "system.core_v2_initialized", True, category="system",
                source="migration", visibility="system",
                description=f"Núcleo v2 inicializado; {migrated} flags anteriores migradas.",
            )
            self.state["schema_version"] = CORE_SCHEMA_VERSION
        self.session.schema_version = CORE_SCHEMA_VERSION

    def notify(self, title: str, text: str, *, kind: str = "world") -> None:
        now = self.clock.now
        self.state["notifications"].append({
            "title": title,
            "text": text,
            "kind": kind,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute,
            "absolute_minute": now.absolute_minute,
        })
        if len(self.state["notifications"]) > 100:
            del self.state["notifications"][:-100]

    def drain_notifications(self) -> list[dict[str, Any]]:
        result = list(self.state.get("notifications") or [])
        self.state["notifications"] = []
        return result

    def enter_scene(self, scene_id: str) -> list[dict[str, Any]]:
        visits = self.state["visited_scenes"]
        visits[scene_id] = int(visits.get(scene_id, 0)) + 1
        first_visit = visits[scene_id] == 1
        self.world.append_history(
            "scene_entered", scene_id=scene_id, visit=visits[scene_id],
        )
        if first_visit:
            self.world.set(
                f"scene.visited.{scene_id}", True, category="scene",
                source=scene_id, visibility="system",
            )
        self._tovin_scene_hook(scene_id, first_visit)
        self._eldorwood_scene_hook(scene_id, first_visit)
        self.process_due_events()
        return self.drain_notifications()

    def record_choice(
        self,
        *,
        scene_id: str,
        option_text: str,
        destination: str | None,
        result: ActionResult | None = None,
        result_key: str | None = None,
    ) -> list[dict[str, Any]]:
        now = self.clock.now
        decision = {
            "scene_id": scene_id,
            "option": option_text,
            "option_slug": _slug(option_text),
            "destination": destination,
            "result_key": result_key,
            "result": result.to_dict() if result else None,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute,
            "absolute_minute": now.absolute_minute,
        }
        self.state["decisions"].append(decision)
        if len(self.state["decisions"]) > 1000:
            del self.state["decisions"][:-1000]
        self.world.set(
            f"decision.{scene_id}.{decision['option_slug']}",
            {"destination": destination, "result": result_key},
            category="decision", source=scene_id, visibility="system",
            description=option_text,
        )
        self.world.append_history("choice_made", **decision)
        self._tovin_choice_hook(scene_id, option_text, destination, result_key)
        self._eldorwood_choice_hook(scene_id, destination)
        self.process_due_events()
        return self.drain_notifications()

    def resolve_scene_test(
        self,
        *,
        scene_id: str,
        option_text: str,
        attribute: str,
        difficulty: int,
        duration_minutes: int = 0,
    ) -> ActionResult:
        modifiers: list[dict[str, Any]] = []
        if scene_id == "fr1_c09_sombra_no_fiorde" and self.world.get("frostreach.tovin.tide_rose", False):
            modifiers.append({
                "value": -2,
                "reason": "maré alta e placas instáveis",
            })
        return self.actions.resolve(ActionRequest(
            action_id=f"scene:{scene_id}:{_slug(option_text)}",
            label=option_text,
            attribute=attribute,
            difficulty=difficulty,
            duration_minutes=duration_minutes,
            modifiers=modifiers,
            context={"scene_id": scene_id},
        ))

    def process_due_events(self) -> list[ScheduledEvent]:
        events = self.scheduler.process_due()
        for event in events:
            self._handle_resolved_event(event)
            self.notify(event.title, event.description, kind="event")
        self.scheduler.prune()
        return events

    def _handle_resolved_event(self, event: ScheduledEvent) -> None:
        if event.event_type == "tovin_tide_rises":
            quest = self.quests.get(TOVIN_QUEST)
            if quest and quest.get("status") not in TERMINAL_QUEST_STATUSES:
                self.quests.objective(
                    TOVIN_QUEST, "tide_window", status="failed", progress=0,
                    source=event.event_id,
                )
        elif event.event_type == "tovin_village_search":
            quest = self.quests.get(TOVIN_QUEST)
            if quest and quest.get("status") not in TERMINAL_QUEST_STATUSES:
                self.world.set(
                    "frostreach.tovin.fate", "rescued_injured",
                    category="npc", source=event.event_id,
                    description="A busca organizada pela vila encontrou Tovin com vida e ferido.",
                )
                self.quests.objective(TOVIN_QUEST, "locate_tovin", source=event.event_id)
                self.quests.objective(TOVIN_QUEST, "determine_tovin_fate", source=event.event_id)
                self.quests.set_stage(TOVIN_QUEST, "aftermath", source=event.event_id)
                self.quests.set_status(
                    TOVIN_QUEST, "completed", outcome="search_organized",
                    source=event.event_id,
                )
        elif event.event_type == "tovin_world_resolution":
            quest = self.quests.get(TOVIN_QUEST)
            involved = self.world.get("frostreach.tovin.player_involved", False)
            if quest and quest.get("status") not in TERMINAL_QUEST_STATUSES and not involved:
                self.world.set(
                    "frostreach.tovin.fate", "resolved_without_player",
                    category="npc", source=event.event_id,
                    description="Os moradores continuaram a busca sem o personagem.",
                )
                self.quests.set_status(
                    TOVIN_QUEST, "resolved_by_world",
                    outcome="resolved_without_player", source=event.event_id,
                )
        elif event.event_type == "eldorwood_root_world_step":
            quest = self.quests.get(ELDORWOOD_ROOT_QUEST)
            involved = self.world.get("eldorwood.raiz_ancora.player_involved", False)
            if quest and quest.get("status") not in TERMINAL_QUEST_STATUSES and not involved:
                self.world.set(
                    "eldorwood.raiz_ancora.world_progress",
                    "council_quarantine",
                    category="quest",
                    source=event.event_id,
                    description=(
                        "Sem a participação do personagem, o conselho isolou parte da rede e "
                        "as famílias organizaram uma investigação paralela."
                    ),
                )
                self.quests.set_status(
                    ELDORWOOD_ROOT_QUEST,
                    "transformed",
                    outcome="investigation_led_by_council",
                    source=event.event_id,
                )

    def _eldorwood_scene_hook(self, scene_id: str, first_visit: bool) -> None:
        if not first_visit or scene_id != "r2_q01_folhas_pronunciam":
            return
        self.world.set(
            "eldorwood.raiz_ancora.player_involved",
            False,
            category="quest",
            source=scene_id,
            visibility="system",
        )
        self.quests.discover(ELDORWOOD_ROOT_QUEST, rumor=True, source=scene_id)
        self.quests.set_stage(ELDORWOOD_ROOT_QUEST, "q01", source=scene_id)
        self.scheduler.schedule(
            "eldorwood_root_world_step",
            in_minutes=3 * 24 * 60,
            title="A investigação da Raiz-Âncora avançou",
            description=(
                "Três dias se passaram. O conselho, as famílias e os guardiões tomaram "
                "decisões sobre as vozes sem esperar pelo personagem."
            ),
            unique_key="eldorwood_root_world_step",
            condition={"fact": "eldorwood.raiz_ancora.player_involved", "not_equals": True},
        )
        self.notify(
            "Novo rumor — As folhas pronunciam nomes",
            "A investigação é opcional, mas continuará avançando no calendário se você partir.",
            kind="quest",
        )

    def _eldorwood_choice_hook(self, scene_id: str, destination: str | None) -> None:
        if scene_id != "r2_q01_folhas_pronunciam":
            return
        if destination and destination.startswith("r2_q"):
            self.world.set(
                "eldorwood.raiz_ancora.player_involved",
                True,
                category="quest",
                source=scene_id,
                visibility="world",
            )
            self.quests.activate(ELDORWOOD_ROOT_QUEST, stage="q01", source=scene_id)

    def _tovin_scene_hook(self, scene_id: str, first_visit: bool) -> None:
        if not first_visit:
            return
        if scene_id == "fr1_c07_redes_aquari":
            self.world.set(
                "frostreach.tovin.player_involved", False,
                category="quest", source=scene_id, visibility="system",
            )
            if self.quests.discover(TOVIN_QUEST, rumor=True, source=scene_id):
                self.quests.set_stage(TOVIN_QUEST, "rumor", source=scene_id)
                self.quests.objective(TOVIN_QUEST, "learn_disappearance", source=scene_id)
                self.notify(
                    "Novo rumor — O barco que voltou sozinho",
                    "Um pescador chamado Tovin não voltou. Isso existe no mundo mesmo que você decida não se envolver.",
                    kind="quest",
                )
                self.scheduler.schedule(
                    "tovin_world_resolution", in_minutes=12 * 60,
                    title="A busca por Tovin continuou",
                    description="Doze horas se passaram; os moradores tomaram suas próprias decisões sobre o desaparecimento.",
                    unique_key="tovin_world_resolution",
                    condition={"fact": "frostreach.tovin.player_involved", "not_equals": True},
                )
        elif scene_id == "fr1_c08_barco_de_tovin":
            self.quests.discover(TOVIN_QUEST, source=scene_id)
            self.quests.activate(TOVIN_QUEST, stage="boat", source=scene_id)
            self.quests.objective(TOVIN_QUEST, "inspect_boat", source=scene_id)
            self.world.set(
                "frostreach.tovin.player_involved", True,
                category="quest", source=scene_id, visibility="world",
            )
            self.world.set(
                "frostreach.tovin.fate", "missing",
                category="npc", source=scene_id,
                description="O barco voltou, mas Tovin continua desaparecido.",
            )
            self.scheduler.schedule(
                "tovin_tide_rises", in_minutes=55,
                title="A maré do fiorde subiu",
                description="A água cobre parte das marcas e pressiona as placas. Seguir a trilha agora é mais difícil.",
                unique_key="tovin_tide_rises",
                condition={"fact": "frostreach.tovin.fate", "not_equals": "rescued"},
                effects=[{
                    "type": "set_fact", "key": "frostreach.tovin.tide_rose",
                    "value": True, "category": "environment",
                    "description": "A janela de maré baixa terminou.",
                }],
            )
            self.notify(
                "Missão iniciada — O barco que voltou sozinho",
                "O barco, as marcas e a maré foram registrados. As pistas continuarão mudando com o tempo.",
                kind="quest",
            )
        elif scene_id == "fr1_c09_sombra_no_fiorde":
            self.quests.discover(TOVIN_QUEST, source=scene_id)
            self.quests.activate(TOVIN_QUEST, stage="search", source=scene_id)
            self.quests.objective(TOVIN_QUEST, "locate_tovin", source=scene_id)
            self.world.set(
                "frostreach.tovin.player_involved", True,
                category="quest", source=scene_id, visibility="world",
            )
            self.world.set(
                "frostreach.tovin.fate", "located_in_danger",
                category="npc", source=scene_id,
            )
            self.notify(
                "Pista confirmada",
                "Tovin está vivo no fiorde. Encontrá-lo não encerra a situação: ainda é preciso decidir como responder à serpente.",
                kind="quest",
            )
        elif scene_id == "fr1_c10_colheita_de_alga":
            quest = self.quests.get(TOVIN_QUEST)
            if quest and quest.get("status") == "active":
                self.world.set(
                    "frostreach.tovin.antidote_available", True,
                    category="knowledge", source=scene_id,
                    description="A Alga-de-Gelo pode retardar o veneno de frio.",
                )
                self.quests.objective(TOVIN_QUEST, "prepare_treatment", source=scene_id)

    def _tovin_choice_hook(
        self,
        scene_id: str,
        option_text: str,
        destination: str | None,
        result_key: str | None,
    ) -> None:
        option = _slug(option_text)
        if scene_id == "fr1_c08_barco_de_tovin":
            self.quests.objective(TOVIN_QUEST, "choose_search_method", source=scene_id)
            if "seguir_as_botas" in option:
                self.quests.set_stage(TOVIN_QUEST, "search", source=scene_id)
                self.world.set(
                    "frostreach.tovin.search_method", "follow_boots",
                    category="decision", source=scene_id,
                )
            elif "antidoto" in option:
                self.world.set(
                    "frostreach.tovin.search_method", "study_scales",
                    category="decision", source=scene_id,
                )
                if result_key in {"success", "critical_success"}:
                    self.world.set(
                        "frostreach.tovin.antidote_known", True,
                        category="knowledge", source=scene_id,
                    )
            elif "organizar_uma_busca" in option:
                self.world.set(
                    "frostreach.tovin.search_method", "village_search",
                    category="decision", source=scene_id,
                )
                self.scheduler.schedule(
                    "tovin_village_search", in_minutes=3 * 60,
                    title="A busca da vila retornou",
                    description="As equipes organizadas no fiorde regressaram com notícias de Tovin.",
                    unique_key="tovin_village_search",
                    condition={"fact": "frostreach.tovin.fate", "not_equals": "rescued"},
                )
                self.notify(
                    "Busca organizada",
                    "Os moradores agora procurarão Tovin por conta própria. O resultado chegará mesmo que você siga outro caminho.",
                    kind="quest",
                )
        elif scene_id == "fr1_c09_sombra_no_fiorde":
            self.quests.objective(TOVIN_QUEST, "respond_to_serpent", source=scene_id)
            if "distrair" in option:
                outcome = "rescued_injured"
            elif "correr_pelas_placas" in option:
                outcome = "rescued" if result_key in {"success", "critical_success"} else "rescued_injured"
            else:
                outcome = "rescued"
            self.world.set(
                "frostreach.tovin.fate", outcome,
                category="npc", source=scene_id,
                description="A decisão diante da serpente determinou o destino imediato dos pescadores.",
            )
            self.scheduler.cancel(unique_key="tovin_village_search")
            self.quests.objective(TOVIN_QUEST, "determine_tovin_fate", source=scene_id)
            self.quests.set_stage(TOVIN_QUEST, "aftermath", source=scene_id)
            self.quests.set_status(
                TOVIN_QUEST, "completed", outcome=outcome, source=scene_id,
            )
            description = (
                "Tovin foi retirado com vida, mas precisa de tratamento."
                if outcome == "rescued_injured"
                else "Tovin e a pescadora alcançaram terreno firme com vida."
            )
            self.notify(
                "Missão atualizada — Tovin encontrado",
                description + " A vila e os envolvidos lembrarão como isso aconteceu.",
                kind="quest",
            )

    def journal_snapshot(self) -> dict[str, Any]:
        return {
            "quests": self.quests.journal(),
            "relationships": self.relationships.all_known(),
            "facts": [
                {"key": key, **value}
                for key, value in sorted(
                    self.world.facts.items(),
                    key=lambda item: int(item[1].get("absolute_minute") or 0),
                    reverse=True,
                )
                if value.get("visibility") != "system"
            ],
            "events": [event.to_dict() for event in self.scheduler.pending()],
            "history": list(reversed(self.world.history[-100:])),
        }
