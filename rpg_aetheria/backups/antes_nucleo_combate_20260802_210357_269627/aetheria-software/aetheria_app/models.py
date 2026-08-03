from __future__ import annotations

import random
from dataclasses import asdict, dataclass, field, fields
from typing import Any

from .content import REGIONS


@dataclass
class PlayerSession:
    name: str
    race_slug: str
    race_name: str
    region_slug: str
    scene_id: str
    life_max: int
    attack: int
    defense: int
    mana_max: int
    speed: int
    critical: float
    character_id: int | None = None
    life: int = 0
    mana: int = 0
    energy: int = 100
    hunger: int = 15
    thirst: int = 15
    temperature: int = 0
    day: int = 1
    hour: int = 8
    minute: int = 0
    awake_minutes: int = 0
    travel_minutes_today: int = 0
    distance_traveled_km: float = 0.0
    xp: int = 0
    biome_slug: str = "nascimento"
    position_x: float = 0.0
    position_y: float = 0.0
    exploration_step: int = 0
    exploration: dict = field(default_factory=dict)
    schema_version: int = 3
    core_state: dict[str, Any] = field(default_factory=dict)
    flags: set[str] = field(default_factory=set)
    inventory: list[str] = field(default_factory=list)
    reputation: dict[str, int] = field(default_factory=lambda: {
        "stonhelm": 50, "brumafiorde": 50, "renaquieta": 50,
        "pedravela": 50, "patrulha_do_norte": 50, "companheiros": 50,
        "sylvarin": 50, "brumavale": 50, "lethariel": 50,
        "vale_eldor": 50, "conselhos_do_dossel": 50,
        "estradas_livres": 50, "confluencia": 50,
        "regencia_arkanor": 50, "conclave_meridiano": 50,
        "universidade_aberta": 50, "assembleia_da_rua": 50,
        "casa_das_medidas": 50, "coro_de_navegadores": 50,
        "calendario_das_safras": 50, "vigias_da_fronteira": 50,
        "guildas_douradas": 50, "campos_livres": 50,
    })
    attributes: dict[str, int] = field(default_factory=lambda: {
        "sobrevivencia": 0, "percepcao": 0, "forca": 0,
        "agilidade": 0, "vontade": 0, "social": 0, "furtividade": 0,
    })

    def __post_init__(self) -> None:
        if self.life <= 0:
            self.life = self.life_max
        if self.mana <= 0:
            self.mana = self.mana_max

    @property
    def region_name(self) -> str:
        return REGIONS[self.region_slug][0]

    def roll_d20(self) -> tuple[int, str]:
        value = random.randint(1, 20)
        label = "falha crítica" if value == 1 else "sucesso crítico" if value == 20 else "resultado comum"
        return value, label

    def advance_time(self, hours: int = 1) -> None:
        self.advance_minutes(max(0, int(hours)) * 60)

    def advance_minutes(self, minutes: int, *, traveling: bool = False) -> None:
        minutes = max(0, int(minutes))
        old_day = self.day
        total = self.hour * 60 + self.minute + minutes
        self.day += total // (24 * 60)
        within_day = total % (24 * 60)
        self.hour, self.minute = divmod(within_day, 60)
        self.awake_minutes += minutes
        if self.day != old_day:
            self.travel_minutes_today = 0
        if traveling:
            self.travel_minutes_today += minutes

    @property
    def day_phase(self) -> str:
        if 0 <= self.hour < 5:
            return "Madrugada"
        if self.hour < 8:
            return "Amanhecer"
        if self.hour < 12:
            return "Manhã"
        if self.hour < 17:
            return "Tarde"
        if self.hour < 19:
            return "Entardecer"
        return "Noite"

    @property
    def clock_label(self) -> str:
        return f"Dia {self.day} — {self.hour:02d}:{self.minute:02d} ({self.day_phase})"

    def complete_rest(self, minutes: int) -> None:
        self.advance_minutes(minutes)
        if minutes >= 360:
            self.awake_minutes = 0
            self.travel_minutes_today = 0

    def change_need(self, name: str, amount: int) -> None:
        field_name = {
            "energia": "energy", "fome": "hunger", "sede": "thirst",
        }.get(name, name)
        if field_name not in {"energy", "hunger", "thirst"}:
            raise ValueError(f"Necessidade desconhecida: {name}")
        current = int(getattr(self, field_name))
        setattr(self, field_name, max(0, min(100, current + int(amount))))

    def travel(self, direction: str) -> dict:
        roll = random.randint(1, 20)
        self.advance_minutes(60, traveling=True)
        self.energy = max(0, self.energy - random.randint(4, 8))
        self.hunger = min(100, self.hunger + random.randint(2, 5))
        self.thirst = min(100, self.thirst + random.randint(3, 6))
        if self.region_slug == "frostreach":
            self.temperature = max(-100, self.temperature - random.randint(3, 7))
        elif self.region_slug in {"stonevale", "blackmarsh"}:
            self.temperature = min(100, self.temperature + random.randint(2, 6))

        if roll <= 4:
            event = "Você encontra rastros recentes. Algo grande passou por aqui e talvez ainda esteja perto."
        elif roll <= 8:
            event = "O terreno força uma passagem lenta. Cada passo exige atenção e custa mais energia."
        elif roll <= 13:
            event = "A caminhada é longa e silenciosa. O mundo muda pouco, mas novos sons surgem adiante."
        elif roll <= 17:
            event = "Você encontra sinais úteis: água, abrigo parcial ou marcas de uma trilha antiga."
        else:
            event = "Uma descoberta incomum interrompe a marcha. Este lugar será registrado no diário."
            self.flags.add(f"descoberta_{self.region_slug}_{self.day}_{self.hour}")
        return {"roll": roll, "event": event, "direction": direction}

    def to_dict(self) -> dict:
        data = asdict(self)
        data["flags"] = sorted(self.flags)
        return data

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "PlayerSession":
        """Restaura saves atuais e antigos sem exigir uma migração manual."""
        data = dict(raw or {})
        aliases = {
            "vida": "life", "vida_max": "life_max", "ataque": "attack",
            "defesa": "defense", "mana_maxima": "mana_max",
            "velocidade": "speed", "chance_critico": "critical",
            "energia": "energy", "fome": "hunger", "sede": "thirst",
            "temperatura": "temperature", "dia": "day", "hora": "hour",
            "minuto": "minute", "inventario": "inventory",
        }
        for old, new in aliases.items():
            if old in data and new not in data:
                data[new] = data[old]
        allowed = {item.name for item in fields(cls)}
        cleaned = {key: value for key, value in data.items() if key in allowed}
        cleaned["flags"] = set(cleaned.get("flags") or ())
        cleaned["inventory"] = list(cleaned.get("inventory") or ())
        cleaned["exploration"] = dict(cleaned.get("exploration") or {})
        cleaned["core_state"] = dict(cleaned.get("core_state") or {})
        cleaned["reputation"] = dict(cleaned.get("reputation") or {})
        cleaned["attributes"] = dict(cleaned.get("attributes") or {})
        return cls(**cleaned)
