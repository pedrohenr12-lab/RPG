from __future__ import annotations

import random
from dataclasses import asdict, dataclass, field

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
    xp: int = 0
    flags: set[str] = field(default_factory=set)
    inventory: list[str] = field(default_factory=list)
    reputation: dict[str, int] = field(default_factory=lambda: {
        "stonhelm": 50, "brumafiorde": 50, "renaquieta": 50,
        "pedravela": 50, "patrulha_do_norte": 50, "companheiros": 50,
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

    def travel(self, direction: str) -> dict:
        roll = random.randint(1, 20)
        self.hour += 1
        if self.hour >= 24:
            self.day += self.hour // 24
            self.hour %= 24
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

