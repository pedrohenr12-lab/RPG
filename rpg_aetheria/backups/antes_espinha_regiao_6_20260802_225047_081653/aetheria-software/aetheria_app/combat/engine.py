from __future__ import annotations

import math
import random
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any

from .careers import BATTLE_CLASSES, SkillTreeService


@dataclass
class StatusEffect:
    slug: str
    name: str
    duration: int
    potency: int = 1
    stacks: int = 1
    source: str = ""

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "StatusEffect":
        return cls(**{key: raw[key] for key in ("slug", "name", "duration", "potency", "stacks", "source") if key in raw})


@dataclass
class Combatant:
    identifier: str
    name: str
    side: str
    life: int
    life_max: int
    mana: int = 0
    mana_max: int = 0
    stamina: int = 100
    stamina_max: int = 100
    attack: int = 4
    defense: int = 10
    armor: int = 0
    block: int = 0
    magic: int = 0
    speed: int = 4
    critical_margin: int = 0
    position: int = 0
    ai: str = "balanced"
    threat: int = 1
    morale: int = 100
    resistances: dict[str, int] = field(default_factory=dict)
    statuses: list[StatusEffect] = field(default_factory=list)
    proficiencies: list[str] = field(default_factory=list)
    weapon: dict[str, Any] = field(default_factory=dict)
    phase: int = 1
    phase_thresholds: list[float] = field(default_factory=list)
    surrendered: bool = False
    captured: bool = False

    @property
    def alive(self) -> bool:
        return self.life > 0 and not self.surrendered and not self.captured

    def has(self, slug: str) -> bool:
        return any(effect.slug == slug and effect.duration > 0 for effect in self.statuses)

    def status(self, slug: str) -> StatusEffect | None:
        return next((effect for effect in self.statuses if effect.slug == slug and effect.duration > 0), None)

    def add_status(self, effect: StatusEffect) -> None:
        existing = self.status(effect.slug)
        if existing:
            existing.duration = max(existing.duration, effect.duration)
            existing.stacks = min(5, existing.stacks + effect.stacks)
            existing.potency = max(existing.potency, effect.potency)
        else:
            self.statuses.append(effect)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Combatant":
        data = dict(raw)
        data["statuses"] = [StatusEffect.from_dict(item) for item in data.get("statuses") or []]
        return cls(**data)


@dataclass
class BattleState:
    combat_id: str
    region_slug: str
    terrain: str
    weather: str
    round_no: int
    action_points: int
    combatants: list[Combatant]
    log: list[str] = field(default_factory=list)
    outcome: str = "active"
    nonlethal: bool = False
    artifact_charge: int = 0
    artifact_instability: int = 0
    event: dict[str, Any] = field(default_factory=dict)

    @property
    def active(self) -> bool:
        return self.outcome == "active"

    @property
    def player(self) -> Combatant:
        return next(item for item in self.combatants if item.side == "player")

    @property
    def enemies(self) -> list[Combatant]:
        return [item for item in self.combatants if item.side == "enemy" and item.alive]

    @property
    def allies(self) -> list[Combatant]:
        return [item for item in self.combatants if item.side == "ally" and item.alive]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "BattleState":
        data = dict(raw)
        data["combatants"] = [Combatant.from_dict(item) for item in data.get("combatants") or []]
        return cls(**data)


STATUS_NAMES = {
    "bleeding": "Sangramento",
    "burning": "Em chamas",
    "poisoned": "Envenenado",
    "chilled": "Resfriado",
    "frozen": "Congelado",
    "stunned": "Atordoado",
    "prone": "Caído",
    "guarded": "Em guarda",
    "dodging": "Esquiva preparada",
    "exposed": "Exposto",
    "silenced": "Silenciado",
    "rooted": "Imobilizado",
    "frightened": "Amedrontado",
    "marked": "Marcado",
    "regeneration": "Regeneração",
    "barrier": "Barreira",
    "counterspell": "Contrafeitiço preparado",
}


SPELLS: dict[str, dict[str, Any]] = {
    "faisca_ignea": {"name": "Faísca Ígnea", "cost": 3, "ap": 2, "damage": (5, 9), "type": "fire", "range": 3, "status": "burning", "chance": 35},
    "agulha_geada": {"name": "Agulha de Geada", "cost": 3, "ap": 2, "damage": (4, 8), "type": "frost", "range": 3, "status": "chilled", "chance": 55},
    "arco_tempestade": {"name": "Arco de Tempestade", "cost": 5, "ap": 2, "damage": (6, 11), "type": "storm", "range": 3, "status": "stunned", "chance": 20},
    "prisao_raizes": {"name": "Prisão de Raízes", "cost": 4, "ap": 2, "damage": (2, 5), "type": "earth", "range": 2, "status": "rooted", "chance": 70},
    "lanca_sombria": {"name": "Lança Sombria", "cost": 5, "ap": 2, "damage": (7, 12), "type": "shadow", "range": 3, "status": "frightened", "chance": 30},
    "pulso_aether": {"name": "Pulso de Aether", "cost": 6, "ap": 3, "damage": (8, 14), "type": "aether", "range": 3, "status": "exposed", "chance": 40},
    "luz_reparadora": {"name": "Luz Reparadora", "cost": 5, "ap": 2, "healing": (6, 11), "type": "sacred", "range": 2},
    "barreira_harmonica": {"name": "Barreira Harmônica", "cost": 4, "ap": 2, "healing": (0, 0), "type": "aether", "range": 0, "status": "barrier", "chance": 100},
}


CLASS_SPELLS = {
    "mago": ("faisca_ignea", "agulha_geada", "barreira_harmonica", "pulso_aether"),
    "feiticeiro": ("faisca_ignea", "arco_tempestade", "pulso_aether"),
    "elementalista": ("faisca_ignea", "agulha_geada", "arco_tempestade", "prisao_raizes"),
    "artifice_arcano": ("pulso_aether", "barreira_harmonica"),
    "clerigo": ("luz_reparadora", "barreira_harmonica"),
    "paladino": ("luz_reparadora",),
    "druida": ("prisao_raizes", "luz_reparadora", "agulha_geada"),
    "xama": ("arco_tempestade", "barreira_harmonica", "prisao_raizes"),
    "necromante": ("lanca_sombria", "pulso_aether"),
    "invocador": ("pulso_aether", "barreira_harmonica"),
    "anciao": ("barreira_harmonica", "agulha_geada"),
}


DEFAULT_WEAPONS: dict[str, dict[str, Any]] = {
    "Ataque Desarmado": {"name": "Ataque Desarmado", "damage_min": 2, "damage_max": 5, "damage_type": "impact", "range": 1, "accuracy": 1, "armor_piercing": 0},
    "Espada Curta de Ferro": {"name": "Espada Curta de Ferro", "damage_min": 7, "damage_max": 12, "damage_type": "slash", "range": 1, "accuracy": 2, "armor_piercing": 1, "status": "bleeding", "status_chance": 18},
    "Espada Longa de Aço": {"name": "Espada Longa de Aço", "damage_min": 9, "damage_max": 15, "damage_type": "slash", "range": 1, "accuracy": 1, "armor_piercing": 2, "status": "bleeding", "status_chance": 20},
    "Machado de Batalha": {"name": "Machado de Batalha", "damage_min": 8, "damage_max": 13, "damage_type": "slash", "range": 1, "accuracy": 0, "armor_piercing": 3},
    "Maça de Ferro": {"name": "Maça de Ferro", "damage_min": 8, "damage_max": 13, "damage_type": "impact", "range": 1, "accuracy": 0, "armor_piercing": 4, "status": "stunned", "status_chance": 12},
    "Lança de Caça": {"name": "Lança de Caça", "damage_min": 8, "damage_max": 14, "damage_type": "piercing", "range": 2, "accuracy": 1, "armor_piercing": 2},
    "Adaga de Ferro": {"name": "Adaga de Ferro", "damage_min": 6, "damage_max": 11, "damage_type": "piercing", "range": 1, "accuracy": 3, "armor_piercing": 1, "critical": 2},
    "Punhal Umbra": {"name": "Punhal Umbra", "damage_min": 10, "damage_max": 17, "damage_type": "piercing", "range": 1, "accuracy": 3, "armor_piercing": 2, "critical": 3},
    "Arco Curto de Teixo": {"name": "Arco Curto de Teixo", "damage_min": 7, "damage_max": 12, "damage_type": "piercing", "range": 3, "accuracy": 2, "armor_piercing": 1},
    "Arco Longo de Freixo": {"name": "Arco Longo de Freixo", "damage_min": 7, "damage_max": 12, "damage_type": "piercing", "range": 3, "accuracy": 3, "armor_piercing": 1},
    "Besta de Mão": {"name": "Besta de Mão", "damage_min": 9, "damage_max": 14, "damage_type": "piercing", "range": 3, "accuracy": 1, "armor_piercing": 4},
    "Bastão de Caminhante": {"name": "Bastão de Caminhante", "damage_min": 5, "damage_max": 10, "damage_type": "impact", "range": 1, "accuracy": 2, "armor_piercing": 0},
}


def _normalized_damage_type(value: str | None) -> str:
    aliases = {"corte": "slash", "perfuracao": "piercing", "perfuração": "piercing", "impacto": "impact"}
    return aliases.get(str(value or "").casefold(), str(value or "impact").casefold())


def adapt_item_rows(rows: list[dict[str, Any]] | None) -> dict[str, dict[str, Any]]:
    result = dict(DEFAULT_WEAPONS)
    for row in rows or []:
        name = str(row.get("name") or "").strip()
        if not name:
            continue
        range_m = int(row.get("range_m") or 0)
        abstract_range = 3 if range_m >= 20 else 2 if range_m >= 4 else 1
        effect = str(row.get("effect_key") or "")
        status = {
            "sangramento": "bleeding", "atordoamento": "stunned",
            "congelamento": "chilled", "veneno": "poisoned",
        }.get(effect)
        result[name] = {
            "name": name,
            "damage_min": int(row.get("damage_min") or 2),
            "damage_max": int(row.get("damage_max") or 5),
            "damage_type": _normalized_damage_type(row.get("damage_type")),
            "range": abstract_range,
            "accuracy": max(0, int(row.get("tier") or 1) - 1),
            "armor_piercing": int((row.get("effect_value") or 0) // 10) if effect == "perfura_armadura" else 0,
            "status": status,
            "status_chance": int(row.get("effect_value") or 0) if status else 0,
            "magic_power": int(row.get("magic_power") or 0),
            "block": int(row.get("block_value") or 0),
            "defense": int(row.get("defense") or 0),
            "category": row.get("category_slug"),
        }
    return result


class CombatEngine:
    """Motor determinístico sob RNG injetável; a interface apenas envia ações."""

    MAX_ACTION_POINTS = 3

    def __init__(self, session: Any, state: BattleState, *, rng: random.Random | None = None, item_rows: list[dict] | None = None):
        self.session = session
        self.state = state
        self.rng = rng or random.Random()
        self.items = adapt_item_rows(item_rows)

    @classmethod
    def start(cls, session: Any, event: dict[str, Any], *, rng: random.Random | None = None, item_rows: list[dict] | None = None) -> "CombatEngine":
        rng = rng or random.Random()
        items = adapt_item_rows(item_rows)
        effects = SkillTreeService.effects(session)
        weapon_name = str((getattr(session, "equipment", {}) or {}).get("weapon") or "Ataque Desarmado")
        weapon = dict(items.get(weapon_name) or DEFAULT_WEAPONS["Ataque Desarmado"])
        armor_from_equipment = sum(
            int((items.get(str(name)) or {}).get("defense") or 0)
            for slot, name in (getattr(session, "equipment", {}) or {}).items()
            if slot != "weapon"
        )
        player = Combatant(
            identifier="player", name=session.name, side="player",
            life=int(session.life), life_max=int(session.life_max),
            mana=int(session.mana), mana_max=int(session.mana_max),
            stamina=max(10, int(session.energy)), stamina_max=100,
            attack=int(session.attack) + effects.get("bonus_attack", 0),
            defense=10 + int(session.defense) + effects.get("bonus_defense", 0),
            armor=max(0, int(session.defense) // 2 + armor_from_equipment),
            block=int(weapon.get("block") or 0),
            magic=max(1, int(session.mana_max) // 3) + effects.get("bonus_magic", 0),
            speed=int(session.speed), critical_margin=max(0, round(float(session.critical) * 20)) + effects.get("bonus_critical", 0),
            position=0, proficiencies=list((BATTLE_CLASSES.get(getattr(session, "battle_class_slug", "")) or BATTLE_CLASSES["guerreiro"]).proficiencies),
            weapon=weapon,
        )
        enemy_count = 1
        if int(event.get("threat", 1)) <= 2 and event.get("group_size"):
            enemy_count = max(1, min(4, int(event["group_size"])))
        enemies = [cls._enemy_from_event(event, index, enemy_count, rng) for index in range(enemy_count)]
        allies = [cls._ally_from_record(item, session, items) for item in (getattr(session, "companions", []) or []) if item.get("active", True)]
        state = BattleState(
            combat_id=uuid.uuid4().hex, region_slug=session.region_slug,
            terrain=str((getattr(session, "exploration", {}) or {}).get("biome") or session.biome_slug),
            weather=str((getattr(session, "exploration", {}) or {}).get("weather") or "estável"),
            round_no=1, action_points=cls.MAX_ACTION_POINTS,
            combatants=[player, *allies, *enemies], event=dict(event),
            artifact_charge=int((getattr(session, "artifact_state", {}) or {}).get("charge", 0)),
            artifact_instability=int((getattr(session, "artifact_state", {}) or {}).get("instability", 0)),
        )
        state.log.extend((
            f"COMBATE INICIADO — {event.get('name', 'ameaça desconhecida')}.",
            f"Terreno: {state.terrain}; clima: {state.weather}. Distâncias, cobertura e condições permanecem entre ações.",
            "Você possui 3 pontos de ação por rodada. Atacar sem observar ou se posicionar é possível, mas tem custo.",
        ))
        engine = cls(session, state, rng=rng, item_rows=item_rows)
        engine._initiative_opening()
        engine.sync_session()
        return engine

    @classmethod
    def resume(cls, session: Any, *, rng: random.Random | None = None, item_rows: list[dict] | None = None) -> "CombatEngine" | None:
        raw = getattr(session, "combat_state", None)
        if not isinstance(raw, dict) or raw.get("outcome") != "active":
            return None
        return cls(session, BattleState.from_dict(raw), rng=rng, item_rows=item_rows)

    @staticmethod
    def _enemy_from_event(event: dict[str, Any], index: int, count: int, rng: random.Random) -> Combatant:
        threat = max(1, min(8, int(event.get("threat") or 1)))
        legendary = bool(event.get("legendary")) or event.get("behavior") == "legendary"
        scale = 1.65 if legendary else 1.0
        life = round((10 + threat * 8) * scale)
        name = str(event.get("name") or "Criatura desconhecida")
        if count > 1:
            name += f" {index + 1}"
        resistances: dict[str, int] = {}
        lowered = name.casefold()
        if any(word in lowered for word in ("gelo", "geada", "neve")):
            resistances.update({"frost": 45, "fire": -20})
        if any(word in lowered for word in ("serpente", "aranha", "venen")):
            resistances["poison"] = 55
        if any(word in lowered for word in ("pedra", "titã", "carapaça")):
            resistances.update({"slash": 25, "impact": -10})
        thresholds = [0.65, 0.30] if legendary else []
        return Combatant(
            identifier=f"enemy_{index + 1}", name=name, side="enemy",
            life=life, life_max=life, stamina=70 + threat * 5, stamina_max=70 + threat * 5,
            attack=3 + threat * 2, defense=9 + threat, armor=max(0, threat - 1),
            magic=threat if legendary else max(0, threat - 3), speed=3 + threat,
            position=2 if event.get("behavior") == "predator" else 3,
            ai="boss" if legendary else str(event.get("behavior") or "balanced"),
            threat=threat, morale=120 if legendary else 65 + threat * 5,
            resistances=resistances, phase_thresholds=thresholds,
            weapon={"name": "armas naturais", "damage_min": 2 + threat, "damage_max": 5 + threat * 2, "damage_type": "slash", "range": 1, "accuracy": 1, "armor_piercing": max(0, threat - 3), "status": "bleeding", "status_chance": 12 + threat * 3},
        )

    @staticmethod
    def _ally_from_record(record: dict[str, Any], session: Any, items: dict[str, dict[str, Any]]) -> Combatant:
        level = max(1, int(record.get("level") or 1))
        weapon_name = str(record.get("weapon") or "Ataque Desarmado")
        life_max = int(record.get("life_max") or 14 + level * 3)
        return Combatant(
            identifier=str(record.get("id") or f"ally_{level}"), name=str(record.get("name") or "Companheiro"), side="ally",
            life=min(life_max, int(record.get("life") or life_max)), life_max=life_max,
            mana=int(record.get("mana") or 0), mana_max=int(record.get("mana_max") or 0),
            attack=4 + level, defense=10 + level, armor=max(0, level // 2), speed=4 + level,
            position=int(record.get("position") or 0), ai=str(record.get("role") or "balanced"),
            weapon=dict(items.get(weapon_name) or DEFAULT_WEAPONS["Ataque Desarmado"]),
        )

    def _initiative_opening(self) -> None:
        player_roll = self.rng.randint(1, 20) + self.state.player.speed
        enemy_roll = max(self.rng.randint(1, 20) + enemy.speed for enemy in self.state.enemies)
        self.state.log.append(f"Iniciativa: {self.state.player.name} {player_roll}; oposição {enemy_roll}.")
        if enemy_roll > player_roll + 5:
            self.state.log.append("A ameaça toma o primeiro instante antes que você complete a postura.")
            self._enemy_phase(opening=True)

    def target(self) -> Combatant | None:
        return self.state.enemies[0] if self.state.enemies else None

    def available_actions(self) -> list[dict[str, Any]]:
        if not self.state.active:
            return []
        player = self.state.player
        if player.has("stunned") or player.has("frozen"):
            return [{"id": "end_turn", "name": "Tentar recuperar o controle", "description": "Encerra a rodada e reduz condições incapacitantes.", "tone": "urgent"}]
        target = self.target()
        if target is None:
            return []
        distance = abs(player.position - target.position)
        weapon_range = int(player.weapon.get("range") or 1)
        actions: list[dict[str, Any]] = []
        if distance <= weapon_range:
            actions.extend((
                {"id": "quick_attack", "name": "Ataque rápido — 1 PA", "description": "Menos dano; preserva ações para defesa ou movimento."},
                {"id": "attack", "name": f"Atacar com {player.weapon.get('name', 'arma')} — 2 PA", "description": "Ataque equilibrado com efeito do equipamento."},
                {"id": "heavy_attack", "name": "Ataque pesado — 3 PA", "description": "Mais dano e perfuração; fica Exposto se falhar.", "tone": "danger"},
            ))
            if target.life <= max(1, round(target.life_max * 0.30)):
                actions.append({"id": "subdue", "name": "Subjugar sem matar — 2 PA", "description": "Tenta capturar ou incapacitar o alvo enfraquecido."})
        else:
            actions.append({"id": "approach", "name": "Avançar uma faixa — 1 PA", "description": "Encurta a distância; pode provocar reação."})
        if player.position < 3:
            actions.append({"id": "retreat", "name": "Recuar uma faixa — 1 PA", "description": "Abre distância e procura cobertura."})
        actions.extend((
            {"id": "guard", "name": "Preparar guarda — 1 PA", "description": "Aumenta defesa e bloqueia parte do próximo impacto."},
            {"id": "dodge", "name": "Preparar esquiva — 1 PA", "description": "Aumenta evasão; forte contra um ataque, fraca contra área."},
            {"id": "recover", "name": "Recobrar fôlego — 1 PA", "description": "Recupera vigor; não restaura vida."},
        ))
        career_slug = getattr(self.session, "battle_class_slug", "guerreiro")
        career = BATTLE_CLASSES.get(career_slug, BATTLE_CLASSES["guerreiro"])
        if self.state.action_points >= 2:
            actions.append({"id": "class_ability", "name": f"{career.innate_name} — 2 PA", "description": career.innate_description})
        for unlocked_action in sorted(SkillTreeService.unlocked_actions(self.session)):
            node = self._node_for_unlocked_action(unlocked_action)
            if node:
                actions.append({
                    "id": f"skill:{unlocked_action}",
                    "name": f"{node.name} — 2 PA",
                    "description": node.description,
                })
        efficiency = SkillTreeService.effects(self.session).get("mana_efficiency", 0)
        for spell_slug in CLASS_SPELLS.get(career_slug, ()):
            spell = SPELLS[spell_slug]
            cost = max(1, int(spell["cost"]) - efficiency)
            if player.mana >= cost and distance <= int(spell.get("range") or 0):
                actions.append({"id": f"spell:{spell_slug}", "name": f"{spell['name']} — {spell['ap']} PA / {cost} mana", "description": self._spell_description(spell)})
        if getattr(self.session, "equipped_artifacts", None) and self.state.artifact_charge > 0:
            actions.append({"id": "artifact", "name": "Ativar artefato — 2 PA", "description": "Efeito poderoso; aumenta instabilidade.", "tone": "urgent"})
        actions.extend((
            {"id": "influence", "name": "Exigir rendição — 2 PA", "description": "Usa vantagem, moral e presença; nem toda criatura entende palavras."},
            {"id": "flee", "name": "Tentar fugir — 2 PA", "description": "Compara mobilidade, distância e terreno.", "tone": "urgent"},
            {"id": "surrender", "name": "Render-se — 3 PA", "description": "Termina a luta sem garantir misericórdia.", "tone": "danger"},
            {"id": "end_turn", "name": "Encerrar rodada", "description": "Guarda ações restantes como cautela limitada."},
        ))
        return [action for action in actions if self._action_cost(action["id"]) <= self.state.action_points]

    @staticmethod
    def _spell_description(spell: dict[str, Any]) -> str:
        if spell.get("healing"):
            return f"Recupera {spell['healing'][0]}–{spell['healing'][1]} de vida ou cria proteção."
        extra = f"; pode causar {STATUS_NAMES.get(spell.get('status'), spell.get('status'))}" if spell.get("status") else ""
        return f"Dano {spell['damage'][0]}–{spell['damage'][1]} de {spell['type']}{extra}."

    def perform(self, action_id: str) -> list[str]:
        if not self.state.active:
            return ["O combate já terminou."]
        before = len(self.state.log)
        valid_actions = {str(action["id"]) for action in self.available_actions()}
        if action_id not in valid_actions:
            self.state.log.append("Essa ação não está disponível na posição, condição ou repertório atual.")
            return self.state.log[before:]
        cost = self._action_cost(action_id)
        if cost > self.state.action_points:
            self.state.log.append("Não há pontos de ação suficientes.")
            return self.state.log[before:]
        self.state.action_points -= cost
        if action_id in {"quick_attack", "attack", "heavy_attack", "subdue"}:
            self._weapon_action(action_id)
        elif action_id in {"approach", "retreat"}:
            self._move(action_id)
        elif action_id == "guard":
            self.state.player.add_status(StatusEffect("guarded", STATUS_NAMES["guarded"], 1, potency=max(2, self.state.player.block)))
            self.state.log.append("Você firma a postura e prepara bloqueio ou aparo contra o próximo impacto.")
        elif action_id == "dodge":
            self.state.player.add_status(StatusEffect("dodging", STATUS_NAMES["dodging"], 1, potency=4))
            self.state.log.append("Você mantém o peso leve e reserva espaço para uma esquiva.")
        elif action_id == "recover":
            recovered = min(18, self.state.player.stamina_max - self.state.player.stamina)
            self.state.player.stamina += recovered
            self.state.log.append(f"Você regula a respiração e recupera {recovered} de vigor.")
        elif action_id == "class_ability":
            self._class_ability()
        elif action_id.startswith("skill:"):
            self._skill_action(action_id.split(":", 1)[1])
        elif action_id.startswith("spell:"):
            self._cast(action_id.split(":", 1)[1])
        elif action_id == "artifact":
            self._artifact()
        elif action_id == "influence":
            self._influence()
        elif action_id == "flee":
            self._flee()
        elif action_id == "surrender":
            self.state.outcome = "surrendered"
            self.state.log.append("Você baixa a arma e se rende. O combate termina; a consequência dependerá de quem aceitou sua rendição.")
        elif action_id == "end_turn":
            self.state.log.append("Você abre mão das ações restantes e observa a resposta inimiga.")
            self.state.action_points = 0
        else:
            self.state.log.append(f"Ação desconhecida: {action_id}.")

        self._check_outcome()
        if self.state.active and self.state.action_points <= 0:
            self._end_player_round()
        self.sync_session()
        return self.state.log[before:]

    @staticmethod
    def _action_cost(action_id: str) -> int:
        if action_id == "quick_attack" or action_id in {"approach", "retreat", "guard", "dodge", "recover"}:
            return 1
        if action_id.startswith("spell:"):
            return int(SPELLS.get(action_id.split(":", 1)[1], {}).get("ap") or 2)
        if action_id in {"attack", "subdue", "class_ability", "artifact", "influence", "flee"} or action_id.startswith("skill:"):
            return 2
        if action_id in {"heavy_attack", "surrender"}:
            return 3
        return 0

    def _weapon_action(self, action_id: str) -> None:
        player, target = self.state.player, self.target()
        if target is None:
            return
        distance = abs(player.position - target.position)
        if distance > int(player.weapon.get("range") or 1):
            self.state.log.append("O alvo está fora do alcance da arma.")
            return
        multipliers = {"quick_attack": 0.65, "attack": 1.0, "heavy_attack": 1.45, "subdue": 0.55}
        accuracy = int(player.weapon.get("accuracy") or 0) + (2 if action_id == "quick_attack" else -2 if action_id == "heavy_attack" else 0)
        degree, roll, total, difficulty = self._check(player, target, accuracy)
        if degree in {"failure", "critical_failure"}:
            self.state.log.append(f"{player.name}: D20 {roll} + bônus = {total} contra {difficulty} — {self._degree_name(degree)}. O golpe não encontra abertura.")
            if action_id == "heavy_attack":
                player.add_status(StatusEffect("exposed", STATUS_NAMES["exposed"], 1, potency=2))
            return
        low = int(player.weapon.get("damage_min") or 2)
        high = max(low, int(player.weapon.get("damage_max") or 5))
        raw = max(1, round(self.rng.randint(low, high) * multipliers[action_id]))
        raw += SkillTreeService.effects(self.session).get("bonus_damage", 0)
        damage = self._deal_damage(player, target, raw, str(player.weapon.get("damage_type") or "impact"), degree, int(player.weapon.get("armor_piercing") or 0), nonlethal=action_id == "subdue")
        self.state.log.append(f"{player.name}: D20 {roll} + bônus = {total} contra {difficulty} — {self._degree_name(degree)}; {damage} de dano em {target.name}.")
        if action_id == "subdue" and target.life <= max(1, round(target.life_max * 0.12)):
            target.life = max(1, target.life)
            target.captured = True
            self.state.nonlethal = True
            self.state.log.append(f"{target.name} é incapacitado sem um golpe fatal.")
        elif player.weapon.get("status") and self.rng.randint(1, 100) <= int(player.weapon.get("status_chance") or 0):
            self._apply_status(target, str(player.weapon["status"]), 2, max(1, damage // 5), player.name)

    def _move(self, action_id: str) -> None:
        player = self.state.player
        target = self.target()
        if target is None:
            return
        old_distance = abs(player.position - target.position)
        if action_id == "approach":
            player.position = min(3, player.position + 1)
            self.state.log.append("Você avança uma faixa, usando irregularidades do terreno como referência.")
            if old_distance == 1 and target.weapon.get("range", 1) >= 2:
                self.state.log.append(f"{target.name} ameaça a passagem com alcance superior.")
        else:
            player.position = max(0, player.position - 1)
            self.state.log.append("Você recua uma faixa sem abandonar completamente a postura.")

    def _class_ability(self) -> None:
        player = self.state.player
        target = self.target()
        slug = getattr(self.session, "battle_class_slug", "guerreiro")
        career = BATTLE_CLASSES.get(slug, BATTLE_CLASSES["guerreiro"])
        if player.stamina < 12 and slug not in CLASS_SPELLS:
            self.state.log.append(f"Falta vigor para usar {career.innate_name}.")
            return
        player.stamina = max(0, player.stamina - (0 if slug in CLASS_SPELLS else 12))
        defensive = {"guerreiro", "guardiao", "cavaleiro", "clerigo", "paladino", "anciao"}
        mobile = {"duelista", "patrulheiro", "ladino", "monge", "arqueiro"}
        controlling = {"lanceiro", "cacador", "druida", "xama", "bardo_guerra"}
        if slug in defensive:
            player.add_status(StatusEffect("guarded", STATUS_NAMES["guarded"], 2, potency=4, source=career.name))
            heal = min(player.life_max - player.life, 3 + max(0, player.defense // 4))
            player.life += heal
            self.state.log.append(f"{career.innate_name}: você recupera {heal} de vida e assume Guarda por duas rodadas.")
        elif slug in mobile:
            player.add_status(StatusEffect("dodging", STATUS_NAMES["dodging"], 2, potency=5, source=career.name))
            if target:
                target.add_status(StatusEffect("marked", STATUS_NAMES["marked"], 2, potency=2, source=career.name))
            self.state.log.append(f"{career.innate_name}: movimento e leitura deixam o alvo Marcado.")
        elif slug in controlling and target:
            self._apply_status(target, "rooted", 1, 2, career.name)
            target.morale -= 10
            self.state.log.append(f"{career.innate_name}: o campo muda e reduz a liberdade de {target.name}.")
        elif slug in {"necromante", "invocador"} and target:
            damage = self._deal_damage(player, target, 5 + player.magic, "shadow" if slug == "necromante" else "aether", "success", 1)
            player.life = min(player.life_max, player.life + max(1, damage // 3))
            self.state.log.append(f"{career.innate_name}: {damage} de dano e parte da energia retorna ao vínculo.")
        else:
            player.mana = min(player.mana_max, player.mana + 4)
            player.add_status(StatusEffect("barrier", STATUS_NAMES["barrier"], 2, potency=3, source=career.name))
            self.state.log.append(f"{career.innate_name}: a canalização recupera mana e forma uma barreira breve.")

    def _node_for_unlocked_action(self, action_slug: str):
        for career in SkillTreeService.selected_careers(self.session):
            for node in career.nodes:
                if any(effect.get("type") == "unlock_action" and effect.get("value") == action_slug for effect in node.effects):
                    return node
        return None

    def _skill_action(self, action_slug: str) -> None:
        node = self._node_for_unlocked_action(action_slug)
        if node is None:
            self.state.log.append("A técnica não pertence aos caminhos atualmente treinados.")
            return
        player, target = self.state.player, self.target()
        mechanical = next((effect for effect in node.effects if effect.get("type") not in {"unlock_action", "capstone"}), {})
        kind = str(mechanical.get("type") or "")
        value = max(1, int(mechanical.get("value") or 1))
        defensive = {"bonus_defense", "bonus_evasion", "bonus_healing", "survival_bonus"}
        social = {"social_bonus", "leadership_bonus", "trade_bonus"}
        utility = {"gather_bonus", "craft_bonus", "alchemy_bonus", "lore_bonus", "exploration_bonus", "stealth_bonus"}
        if kind in defensive:
            healing = min(player.life_max - player.life, 2 + value * 2)
            player.life += healing
            player.add_status(StatusEffect("guarded", STATUS_NAMES["guarded"], 2, potency=2 + value, source=node.name))
            self.state.log.append(f"{node.name}: recupera {healing} de vida e fortalece a defesa.")
            return
        if target is None:
            return
        if kind in social:
            target.morale -= 12 + value * 4
            target.add_status(StatusEffect("frightened", STATUS_NAMES["frightened"], 2, potency=value, source=node.name))
            self.state.log.append(f"{node.name}: a moral de {target.name} cai e sua intenção vacila.")
            return
        if kind in utility:
            target.add_status(StatusEffect("marked", STATUS_NAMES["marked"], 3, potency=1 + value, source=node.name))
            player.add_status(StatusEffect("dodging", STATUS_NAMES["dodging"], 1, potency=2 + value, source=node.name))
            self.state.log.append(f"{node.name}: informação e preparo deixam {target.name} Marcado.")
            return
        damage_type = "aether" if kind in {"bonus_magic", "mana_efficiency", "summon_power"} else "impact"
        degree, roll, total, difficulty = self._check(player, target, value)
        if degree in {"failure", "critical_failure"}:
            self.state.log.append(f"{node.name}: D20 {roll} + bônus = {total} contra {difficulty} — {self._degree_name(degree)}.")
            return
        damage = self._deal_damage(player, target, 4 + player.attack // 2 + value * 2, damage_type, degree, value)
        if kind == "bonus_control":
            self._apply_status(target, "stunned", 1, value, node.name)
        self.state.log.append(f"{node.name}: {damage} de dano e aplicação da técnica aprendida.")

    def _cast(self, spell_slug: str) -> None:
        spell = SPELLS.get(spell_slug)
        if not spell:
            self.state.log.append("O padrão mágico não existe no repertório atual.")
            return
        player = self.state.player
        efficiency = SkillTreeService.effects(self.session).get("mana_efficiency", 0)
        cost = max(1, int(spell["cost"]) - efficiency)
        if player.mana < cost:
            self.state.log.append("Mana insuficiente; o padrão se desfaz antes de ganhar forma.")
            return
        player.mana -= cost
        if spell.get("healing"):
            if spell_slug == "barreira_harmonica":
                self._apply_status(player, "barrier", 2, 4 + player.magic // 2, player.name)
                self.state.log.append(f"{spell['name']} forma uma barreira ao redor de {player.name}.")
            else:
                low, high = spell["healing"]
                healing = self.rng.randint(low, high) + player.magic + SkillTreeService.effects(self.session).get("bonus_healing", 0)
                actual = min(healing, player.life_max - player.life)
                player.life += actual
                self.state.log.append(f"{spell['name']} recupera {actual} de vida.")
            return
        target = self.target()
        if target is None:
            return
        degree, roll, total, difficulty = self._check(player, target, player.magic)
        if degree in {"failure", "critical_failure"}:
            self.state.log.append(f"{spell['name']}: D20 {roll} + canalização = {total} contra {difficulty} — {self._degree_name(degree)}.")
            return
        low, high = spell["damage"]
        raw = self.rng.randint(low, high) + player.magic + SkillTreeService.effects(self.session).get("bonus_magic", 0)
        damage = self._deal_damage(player, target, raw, str(spell["type"]), degree, max(0, player.magic // 4))
        self.state.log.append(f"{spell['name']}: {self._degree_name(degree)}; {damage} de dano {spell['type']} em {target.name}.")
        if spell.get("status") and self.rng.randint(1, 100) <= int(spell.get("chance") or 0):
            self._apply_status(target, str(spell["status"]), 2, max(1, player.magic // 3), player.name)

    def _artifact(self) -> None:
        player, target = self.state.player, self.target()
        if target is None or self.state.artifact_charge <= 0:
            self.state.log.append("O artefato não possui carga utilizável.")
            return
        self.state.artifact_charge -= 1
        self.state.artifact_instability += 12
        raw = 10 + player.magic + self.rng.randint(1, 10)
        damage = self._deal_damage(player, target, raw, "aether", "success", 5)
        self.state.log.append(f"O artefato descarrega {damage} de dano de Aether e alcança {self.state.artifact_instability}% de instabilidade.")
        if self.rng.randint(1, 100) <= self.state.artifact_instability:
            backlash = self.rng.randint(2, 8)
            player.life = max(0, player.life - backlash)
            self.state.log.append(f"RETORNO INSTÁVEL — a descarga causa {backlash} de dano em você.")

    def _influence(self) -> None:
        target = self.target()
        if target is None:
            return
        social = int(getattr(self.session, "attributes", {}).get("social", 0)) + SkillTreeService.effects(self.session).get("social_bonus", 0)
        advantage = round((1 - target.life / max(1, target.life_max)) * 8)
        roll = self.rng.randint(1, 20)
        total = roll + social + advantage
        difficulty = 12 + target.threat + (8 if target.ai in {"predator", "legendary", "boss"} else 0)
        if roll == 20 or (roll != 1 and total >= difficulty):
            target.morale -= 45 + social * 2
            self.state.log.append(f"Influência: D20 {roll} + presença e vantagem = {total} contra {difficulty}. A vontade de {target.name} cede.")
            if target.morale <= 20:
                target.surrendered = True
        else:
            target.morale -= 5
            self.state.log.append(f"Influência: D20 {roll} + presença e vantagem = {total} contra {difficulty}. A ameaça não aceita os termos.")

    def _flee(self) -> None:
        player, target = self.state.player, self.target()
        if target is None:
            return
        distance = abs(player.position - target.position)
        terrain_bonus = 2 if any(word in self.state.terrain for word in ("floresta", "colina", "pântano")) else 0
        roll = self.rng.randint(1, 20) + player.speed + distance * 2 + terrain_bonus
        opposition = 10 + target.speed + target.threat
        if roll >= opposition:
            self.state.outcome = "escaped"
            self.state.log.append(f"Fuga: {roll} contra {opposition}. Você rompe o contato e não espera para confirmar se foi seguido.")
        else:
            self.state.log.append(f"Fuga: {roll} contra {opposition}. {target.name} fecha a rota escolhida.")
            player.add_status(StatusEffect("exposed", STATUS_NAMES["exposed"], 1, potency=2))

    def _end_player_round(self) -> None:
        for ally in self.state.allies:
            self._ally_turn(ally)
        self._enemy_phase()
        self._tick_statuses(self.state.player, "end")
        self._check_outcome()
        if self.state.active:
            self.state.round_no += 1
            self.state.action_points = self.MAX_ACTION_POINTS
            self._tick_statuses(self.state.player, "start")
            self.state.log.append(f"— RODADA {self.state.round_no} — 3 pontos de ação disponíveis.")

    def _ally_turn(self, ally: Combatant) -> None:
        target = self.target()
        if target is None:
            return
        if ally.ai in {"healer", "curandeiro", "clerigo"} and self.state.player.life < self.state.player.life_max * 0.55:
            healed = min(5 + ally.magic, self.state.player.life_max - self.state.player.life)
            self.state.player.life += healed
            self.state.log.append(f"{ally.name} estabiliza você e recupera {healed} de vida.")
            return
        if abs(ally.position - target.position) > int(ally.weapon.get("range") or 1):
            ally.position = min(3, ally.position + 1)
            self.state.log.append(f"{ally.name} avança para apoiar a linha.")
            return
        degree, _, _, _ = self._check(ally, target, int(ally.weapon.get("accuracy") or 0))
        if degree in {"success", "critical_success"}:
            damage = self._deal_damage(ally, target, self.rng.randint(int(ally.weapon.get("damage_min") or 2), int(ally.weapon.get("damage_max") or 5)), str(ally.weapon.get("damage_type") or "impact"), degree, int(ally.weapon.get("armor_piercing") or 0))
            self.state.log.append(f"{ally.name} atinge {target.name} e causa {damage} de dano.")
        else:
            self.state.log.append(f"{ally.name} ataca, mas {target.name} conserva a abertura fechada.")

    def _enemy_phase(self, opening: bool = False) -> None:
        for enemy in list(self.state.enemies):
            if not self.state.player.alive:
                break
            self._tick_statuses(enemy, "start")
            if not enemy.alive:
                continue
            if enemy.has("stunned") or enemy.has("frozen"):
                self.state.log.append(f"{enemy.name} perde a ação por {STATUS_NAMES['stunned'] if enemy.has('stunned') else STATUS_NAMES['frozen']}.")
                self._tick_statuses(enemy, "end")
                continue
            self._boss_phase(enemy)
            distance = abs(enemy.position - self.state.player.position)
            if enemy.ai in {"territorial", "neutral"} and enemy.life < enemy.life_max * 0.35 and enemy.morale < 55:
                enemy.surrendered = True
                self.state.log.append(f"{enemy.name} rompe o confronto e abandona o território imediato.")
                continue
            if distance > int(enemy.weapon.get("range") or 1) and not enemy.has("rooted"):
                enemy.position = max(0, enemy.position - 1)
                self.state.log.append(f"{enemy.name} encurta a distância.")
                distance = abs(enemy.position - self.state.player.position)
            if distance <= int(enemy.weapon.get("range") or 1):
                self._enemy_attack(enemy, opening=opening)
                if enemy.ai == "boss" and enemy.phase >= 3 and self.state.player.alive:
                    self._enemy_attack(enemy, opening=False, secondary=True)
            else:
                enemy.add_status(StatusEffect("guarded", STATUS_NAMES["guarded"], 1, potency=2))
                self.state.log.append(f"{enemy.name} não alcança você e protege a aproximação.")
            self._tick_statuses(enemy, "end")

    def _enemy_attack(self, enemy: Combatant, *, opening: bool = False, secondary: bool = False) -> None:
        player = self.state.player
        accuracy = int(enemy.weapon.get("accuracy") or 0) + (2 if opening else -2 if secondary else 0)
        degree, roll, total, difficulty = self._check(enemy, player, accuracy)
        if degree in {"failure", "critical_failure"}:
            self.state.log.append(f"{enemy.name}: D20 {roll} + bônus = {total} contra {difficulty} — {self._degree_name(degree)}.")
            return
        low = int(enemy.weapon.get("damage_min") or 2)
        high = int(enemy.weapon.get("damage_max") or 5)
        damage = self._deal_damage(enemy, player, self.rng.randint(low, high), str(enemy.weapon.get("damage_type") or "slash"), degree, int(enemy.weapon.get("armor_piercing") or 0))
        self.state.log.append(f"{enemy.name}: {self._degree_name(degree)}; {damage} de dano em {player.name}.")
        if enemy.weapon.get("status") and self.rng.randint(1, 100) <= int(enemy.weapon.get("status_chance") or 0):
            self._apply_status(player, str(enemy.weapon["status"]), 2, max(1, enemy.threat // 2), enemy.name)

    def _check(self, actor: Combatant, target: Combatant, situational: int = 0) -> tuple[str, int, int, int]:
        roll = self.rng.randint(1, 20)
        penalties = 2 * (actor.status("frightened").stacks if actor.status("frightened") else 0)
        total = roll + actor.attack + situational - penalties
        difficulty = target.defense
        if target.has("dodging"):
            difficulty += target.status("dodging").potency
        if target.has("guarded"):
            difficulty += 2
        if target.has("exposed"):
            difficulty -= target.status("exposed").potency
        if target.has("marked"):
            difficulty -= target.status("marked").potency
        margin = total - difficulty
        critical_threshold = 10 - max(0, actor.critical_margin)
        if roll == 20 or margin >= critical_threshold:
            degree = "critical_success"
        elif roll == 1 or margin <= -10:
            degree = "critical_failure"
        elif margin >= 0:
            degree = "success"
        else:
            degree = "failure"
        return degree, roll, total, difficulty

    def _deal_damage(self, actor: Combatant, target: Combatant, raw: int, damage_type: str, degree: str, armor_piercing: int, *, nonlethal: bool = False) -> int:
        if degree == "critical_success":
            raw = math.ceil(raw * 1.6)
        barrier = target.status("barrier")
        if barrier:
            absorbed = min(raw, barrier.potency * barrier.stacks)
            raw -= absorbed
            barrier.potency = max(0, barrier.potency - absorbed)
            self.state.log.append(f"A barreira de {target.name} absorve {absorbed}.")
            if barrier.potency <= 0:
                barrier.duration = 0
        mitigation = max(0, target.armor - armor_piercing)
        guarded = target.status("guarded")
        if guarded:
            mitigation += guarded.potency
            guarded.duration = 0
        resistance = int(target.resistances.get(damage_type, 0))
        after_armor = max(0, raw - mitigation)
        damage = max(0, round(after_armor * (100 - resistance) / 100))
        if raw > 0 and damage <= 0:
            damage = 1
        if nonlethal:
            target.life = max(1, target.life - damage)
        else:
            target.life = max(0, target.life - damage)
        target.morale -= max(2, damage)
        return damage

    def _apply_status(self, target: Combatant, slug: str, duration: int, potency: int, source: str) -> None:
        target.add_status(StatusEffect(slug, STATUS_NAMES.get(slug, slug.title()), duration, potency=potency, source=source))
        self.state.log.append(f"{target.name} recebe {STATUS_NAMES.get(slug, slug)} por {duration} rodada(s).")

    def _tick_statuses(self, combatant: Combatant, timing: str) -> None:
        for effect in list(combatant.statuses):
            if effect.duration <= 0:
                continue
            if timing == "start":
                if effect.slug in {"bleeding", "burning", "poisoned"}:
                    damage_type = {"bleeding": "piercing", "burning": "fire", "poisoned": "poison"}[effect.slug]
                    damage = max(1, round(effect.potency * effect.stacks * (100 - combatant.resistances.get(damage_type, 0)) / 100))
                    combatant.life = max(0, combatant.life - damage)
                    self.state.log.append(f"{effect.name} causa {damage} de dano em {combatant.name}.")
                elif effect.slug == "regeneration":
                    healing = min(effect.potency * effect.stacks, combatant.life_max - combatant.life)
                    combatant.life += healing
                    self.state.log.append(f"Regeneração recupera {healing} de vida de {combatant.name}.")
            elif timing == "end":
                effect.duration -= 1
        combatant.statuses = [effect for effect in combatant.statuses if effect.duration > 0]

    def _boss_phase(self, enemy: Combatant) -> None:
        ratio = enemy.life / max(1, enemy.life_max)
        target_phase = 1 + sum(1 for threshold in enemy.phase_thresholds if ratio <= threshold)
        if target_phase <= enemy.phase:
            return
        enemy.phase = target_phase
        enemy.attack += 2
        enemy.speed += 1
        enemy.armor = max(0, enemy.armor - 1)
        enemy.add_status(StatusEffect("barrier", STATUS_NAMES["barrier"], 2, potency=2 + target_phase, source=enemy.name))
        self.state.log.append(f"FASE {target_phase} — {enemy.name} muda comportamento: mais rápido e agressivo, porém com a defesa física aberta.")

    def _check_outcome(self) -> None:
        player = self.state.player
        if player.life <= 0:
            self.state.outcome = "defeat"
            self.state.log.append("Você não consegue permanecer consciente. O combate termina em derrota.")
            return
        if not self.state.enemies:
            enemies = [item for item in self.state.combatants if item.side == "enemy"]
            if any(item.captured for item in enemies):
                self.state.outcome = "captured_enemy"
            elif any(item.surrendered for item in enemies):
                self.state.outcome = "enemy_fled"
            else:
                self.state.outcome = "victory"
            self.state.log.append(f"COMBATE ENCERRADO — {self.outcome_label(self.state.outcome)}.")

    def sync_session(self) -> None:
        player = self.state.player
        self.session.life = max(0, min(self.session.life_max, player.life))
        self.session.mana = max(0, min(self.session.mana_max, player.mana))
        self.session.energy = max(0, min(100, player.stamina))
        self.session.combat_state = self.state.to_dict()
        self.session.artifact_state = {
            **dict(getattr(self.session, "artifact_state", {}) or {}),
            "charge": self.state.artifact_charge,
            "instability": self.state.artifact_instability,
        }
        if not self.state.active and not self.state.event.get("rewards_applied"):
            self.state.event["rewards_applied"] = True
            if self.state.outcome in {"victory", "captured_enemy", "enemy_fled"}:
                reward = sum(item.threat * 12 for item in self.state.combatants if item.side == "enemy")
                self.session.xp += reward
                SkillTreeService.grant_xp(self.session, reward)
                self.session.flags.add(f"combate_{self.state.event.get('slug', 'desconhecido')}_{self.state.outcome}")
            self.session.combat_history.append({
                "id": self.state.combat_id, "outcome": self.state.outcome,
                "enemy": self.state.event.get("name"), "rounds": self.state.round_no,
                "region": self.state.region_slug,
            })
            self.session.combat_state = self.state.to_dict()

    def summary(self) -> str:
        player = self.state.player
        target = self.target()
        rows = [
            f"RODADA {self.state.round_no} | PA {self.state.action_points}/3 | Distância abstrata: {abs(player.position - target.position) if target else 0}",
            f"{player.name}: vida {player.life}/{player.life_max}, mana {player.mana}/{player.mana_max}, vigor {player.stamina}/{player.stamina_max}",
        ]
        for enemy in [item for item in self.state.combatants if item.side == "enemy"]:
            conditions = ", ".join(effect.name for effect in enemy.statuses) or "nenhuma condição"
            status = "capturado" if enemy.captured else "recuou/rendeu-se" if enemy.surrendered else f"vida {enemy.life}/{enemy.life_max}"
            rows.append(f"{enemy.name}: {status}; fase {enemy.phase}; {conditions}.")
        player_conditions = ", ".join(effect.name for effect in player.statuses) or "nenhuma"
        rows.append(f"Condições do personagem: {player_conditions}.")
        rows.append("\n".join(self.state.log[-10:]))
        return "\n\n".join(rows)

    @staticmethod
    def _degree_name(degree: str) -> str:
        return {
            "critical_success": "SUCESSO CRÍTICO", "success": "SUCESSO",
            "failure": "FALHA", "critical_failure": "FALHA CRÍTICA",
        }.get(degree, degree)

    @staticmethod
    def outcome_label(outcome: str) -> str:
        return {
            "victory": "vitória", "captured_enemy": "alvo subjugado",
            "enemy_fled": "ameaça afastada", "escaped": "fuga bem-sucedida",
            "surrendered": "rendição", "defeat": "derrota",
        }.get(outcome, outcome)
