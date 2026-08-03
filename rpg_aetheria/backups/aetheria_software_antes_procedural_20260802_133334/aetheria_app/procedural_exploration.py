from __future__ import annotations

import random
import re
import unicodedata
from dataclasses import dataclass
from typing import Any

from .models import PlayerSession


@dataclass
class ExplorationTurn:
    title: str
    narrative: str
    choices: list[dict[str, Any]]

    def as_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "narrative": self.narrative,
            "choices": self.choices,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExplorationTurn":
        return cls(
            str(data.get("title", "Exploração")),
            str(data.get("narrative", "")),
            list(data.get("choices") or []),
        )


def _slug(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    plain = "".join(char for char in normalized if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "_", plain.casefold()).strip("_")


BIOMES: dict[str, dict[str, Any]] = {
    "orla_costeira_gelo": {
        "name": "Orla Costeira do Gelo",
        "ambience": [
            "O mar trabalha sob placas azul-escuras; cada impacto chega pelos pés antes de alcançar os ouvidos.",
            "Sal, pedra molhada e neve ocupam o ar. A bruma apaga a linha entre água e céu.",
            "As falésias negras devolvem o grito das aves com alguns segundos de atraso.",
            "A maré respira por rachaduras no gelo, soltando névoa branca sobre as rochas.",
        ],
        "weather": ["bruma salgada", "neve horizontal", "vento de maré", "céu limpo e cortante"],
        "routes": {
            "norte": ["Testar o gelo rumo ao norte", "Seguir as placas mais espessas ao norte", "Acompanhar pegadas pela enseada ao norte"],
            "sul": ["Contornar a falésia pelo sul", "Descer pela costa em direção ao sul", "Seguir o recuo da maré ao sul"],
            "leste": ["Subir as pedras escuras a leste", "Deixar o mar e avançar para leste", "Seguir a fumaça distante a leste"],
            "oeste": ["Acompanhar os fiordes para oeste", "Cruzar a praia congelada a oeste", "Seguir o canto das aves a oeste"],
        },
        "flora": [
            ("Musgo-de-Fiorde", "camadas azul-prateadas crescem sobre a rocha e retêm um pouco de calor", False, False),
            ("Alga-de-Gelo", "teias verde-escuras se movem sob uma lâmina transparente de gelo", True, False),
            ("Líquen-de-Vento", "desenhos simétricos apontam para as áreas menos castigadas pelo vento", False, False),
            ("Flor-de-Maré", "pétalas brancas surgem numa faixa que a água logo voltará a cobrir", False, False),
            ("Cristal-Verde", "uma planta quase mineral pulsa dentro de uma fenda de basalto", False, False),
        ],
        "fauna": [
            ("Foca-de-Cristal", "pacific", 1, "escamas translúcidas refletem a aurora enquanto ela procura uma abertura na plataforma"),
            ("Urso-Costeiro de Frost", "predator", 4, "um predador fareja o vento entre você e a água"),
            ("Ave-Aurora", "pacific", 1, "penas azul-prateadas vibram em sincronia com a luz do céu"),
            ("Serpente-Marinha de Gelo", "predator", 5, "uma forma comprida acompanha seus passos sob o gelo"),
            ("Caranguejo-de-Pressium", "territorial", 2, "pinças duras raspam a pedra e bloqueiam uma poça salgada"),
            ("Baleia-de-Gelo", "mystic", 2, "um canto grave atravessa água, gelo e ossos antes de desaparecer no fiorde"),
        ],
        "landmarks": [
            ("Caverna da Maré", "Uma abertura respira névoa e exibe marcas da altura alcançada pela água."),
            ("Barco Preso no Gelo", "Um casco Northariano está inclinado entre duas placas, com cordas ainda tensionadas."),
            ("Farol de Basalto", "Uma torre sem chama domina a enseada; símbolos Aquari cobrem a porta."),
            ("Ossário da Falésia", "Ossos polidos pela água formam círculos que não parecem naturais."),
        ],
        "hazards": [
            ("Gelo de Maré", "Rachaduras novas se abrem a cada pressão da água sob seus pés."),
            ("Bruma Branca", "A visibilidade cai até suas próprias pegadas desaparecerem."),
            ("Desprendimento da Falésia", "Pedras e lâminas de gelo começam a cair da parede costeira."),
        ],
    },
    "planalto_central_frostreach": {
        "name": "Planalto Central",
        "ambience": [
            "A tundra parece imóvel, mas musgos baixos tremem antes de cada rajada.",
            "O horizonte é largo demais para oferecer escala; rastros se tornam a única medida de distância.",
            "Neve antiga cobre solo compacto, e manchas escuras denunciam vegetação resistente.",
            "O silêncio se rompe por cascos distantes e pelo estalo seco do gelo no solo.",
        ],
        "weather": ["vento de tundra", "neve fina", "aurora pálida", "nuvens baixas"],
        "routes": {
            "norte": ["Seguir rastros de rena ao norte", "Avançar contra o vento para o norte", "Buscar terreno elevado ao norte"],
            "sul": ["Descer pelo vale raso ao sul", "Acompanhar os corvos para o sul", "Seguir marcas de trenó ao sul"],
            "leste": ["Cruzar o musgo congelado a leste", "Seguir uma linha de pedras a leste", "Investigar fumaça tênue a leste"],
            "oeste": ["Acompanhar a depressão do terreno a oeste", "Marchar para a luz baixa a oeste", "Seguir pegadas isoladas a oeste"],
        },
        "flora": [
            ("Musgo-Congelado", "tapetes geométricos isolam pequenas bolsas de solo", False, False),
            ("Grama-de-Gelo", "folhas rígidas sobrevivem dentro de uma cavidade protegida", True, False),
            ("Flor-do-Vento Polar", "uma flor abre as pétalas justamente durante a rajada mais forte", False, False),
            ("Líquen-de-Fenda", "veios avermelhados ocupam uma cicatriz antiga no terreno", False, False),
            ("Arbusto-Anão de Ferro", "raízes escuras atravessam um solo que parecia pedra", False, False),
        ],
        "fauna": [
            ("Lobo-de-Gelo", "predator", 4, "olhos amarelos surgem e desaparecem atrás das ondulações da tundra"),
            ("Rena-das-Planícies", "pacific", 1, "chifres perfeitamente simétricos se movem acima de uma manada"),
            ("Lebre-de-Neve", "pacific", 0, "orelhas rompem a camuflagem branca por um único instante"),
            ("Raposa-Ártica", "predator", 2, "uma caçadora solitária circula contra o vento para sentir seu cheiro"),
            ("Mamute-das-Presas", "territorial", 3, "um gigante coberto de gelo protege um filhote no centro da manada"),
            ("Corvo-de-Gelo", "neutral", 1, "a ave observa suas mãos e depois olha deliberadamente para o horizonte"),
        ],
        "landmarks": [
            ("Menir Vorath", "Uma pedra negra corta a tundra; nenhuma neve permanece sobre sua superfície."),
            ("Acampamento Abandonado", "Peles endurecidas e uma fogueira fria indicam uma partida apressada."),
            ("Trilha de Trenó", "Sulcos paralelos seguem além do horizonte, alguns recentes e outros muito antigos."),
            ("Círculo de Renas", "Cascos comprimiram a neve num padrão que converge para um símbolo central."),
        ],
        "hazards": [
            ("Tempestade Branca", "O horizonte desaparece e o vento tenta arrancar o ar de seus pulmões."),
            ("Lago Oculto", "O som sob a neve muda: existe água corrente sob uma camada fina."),
            ("Campo de Fractium", "Agulhas minerais vibram quando você se move, atraindo descargas da aurora."),
        ],
    },
    "presas_de_gelo": {
        "name": "Presas de Gelo",
        "ambience": [
            "Picos atravessam as nuvens, e a gravidade mais fraca torna cada abismo ainda mais profundo.",
            "O glaciar geme como madeira sob tensão. Luz azul sobe de fendas sem fundo visível.",
            "O ar é seco e fino; cada som percorre a rocha por uma distância enganosa.",
            "Cristais nas paredes repetem a aurora em círculos cada vez menores.",
        ],
        "weather": ["vento de altitude", "granizo de gelo", "céu violeta", "neve de caverna"],
        "routes": {
            "norte": ["Subir pela garganta ao norte", "Seguir cristais azuis ao norte", "Escalar em direção ao norte"],
            "sul": ["Descer pela moraina ao sul", "Buscar o vale profundo ao sul", "Acompanhar água de degelo ao sul"],
            "leste": ["Entrar na fenda a leste", "Contornar o pico pelo leste", "Seguir marcas de ferramentas a leste"],
            "oeste": ["Cruzar a ponte de gelo a oeste", "Acompanhar a parede para oeste", "Seguir o eco de metal a oeste"],
        },
        "flora": [
            ("Líquen-de-Pico", "fractais escuros sobrevivem numa parede quase vertical", False, False),
            ("Musgo-de-Caverna", "um brilho azul constante acompanha a umidade da rocha", False, False),
            ("Flor-de-Gelo Eterna", "pétalas translúcidas permanecem abertas dentro do glaciar", False, False),
            ("Fungo-Luminoso", "corpos azulados marcam uma passagem que desce para a escuridão", True, False),
        ],
        "fauna": [
            ("Urso-Glacial das Presas", "predator", 5, "um corpo enorme bloqueia a entrada de uma caverna marcada por garras"),
            ("Águia-das-Nuvens", "predator", 3, "uma sombra circular passa sobre você antes de a ave surgir entre as nuvens"),
            ("Cabra-das-Presas", "territorial", 2, "cascos encontram apoio onde a parede parece lisa"),
            ("Dragão-de-Gelo Menor", "legendary", 5, "escamas de Luminite acendem uma a uma no fundo da fenda"),
            ("Aranha-de-Gelo", "predator", 4, "fios congelados fecham a passagem e tremem sem vento"),
            ("Yeti-das-Presas", "legendary", 5, "pegadas quase humanas terminam diante de uma parede de gelo intacta"),
        ],
        "landmarks": [
            ("Caverna de Luminite", "Veios azuis iluminam degraus talhados por uma civilização desconhecida."),
            ("Ponte dos Aureli", "Uma ponte metálica atravessa o abismo sem qualquer pilar visível."),
            ("Santuário Glacari", "Fitas brancas e sinos sem badalo cercam uma porta escavada no gelo."),
            ("Observatório Quebrado", "Anéis de bronze apontam para uma aurora que não ocupa mais aquela posição."),
        ],
        "hazards": [
            ("Avalanche", "Uma linha branca se desprende acima e cresce depressa demais."),
            ("Ponte de Gelo", "O arco transparente vibra sobre um abismo coberto por névoa."),
            ("Fenda de Pressium", "A rocha comprime e libera o ar em pulsos capazes de derrubar uma pessoa."),
        ],
    },
}


NPCS = [
    ("Sigrid Vento-Curto", "uma rastreadora Northariana mede você pela forma como pisa na neve"),
    ("Ilyra da Neve Serena", "uma curandeira Glacari recolhe líquen sem danificar o centro da colônia"),
    ("Brokk Ferrofrio", "um mineiro Aureli tenta libertar um trenó preso entre pedras"),
    ("Nym Auralume", "uma cartógrafa Luminari compara a aurora com círculos desenhados em couro"),
    ("Tovin das Marés", "um pescador Aquari verifica redes sob uma placa de gelo rachada"),
    ("Varka Pedra-Oca", "uma exploradora Voraki encosta a mão no solo para sentir vibrações"),
]

SETTLEMENTS = [
    ("Brumafiorde", "fumaça baixa, barcos presos no gelo e vozes em Aquari e Northariano"),
    ("Renaquieta", "tendas reforçadas cercam um rebanho protegido do vento"),
    ("Pedravela", "luzes Aureli e Ferrari brilham em janelas cortadas na montanha"),
    ("Stonhelm", "muralhas escuras reúnem viajantes de várias raças sob bandeiras congeladas"),
    ("Lúmen-Ninho", "passarelas de gelo e luz conectam abrigos Luminari acima de uma ravina"),
]


class ProceduralExploration:
    """Exploração com encontros persistentes e botões derivados do contexto atual."""

    def __init__(
        self,
        session: PlayerSession,
        catalog: list[dict[str, Any]] | None = None,
        rng: random.Random | None = None,
    ) -> None:
        self.session = session
        self.catalog = list(catalog or [])
        self.rng = rng or random.Random()
        self.state = session.exploration
        self.state.setdefault("recent_events", [])
        self.state.setdefault("discoveries", [])
        self.state.setdefault("weather", "vento constante")
        self.state.setdefault("encounter", None)
        self.state.setdefault("turn", None)
        self._set_initial_biome()

    def set_catalog(self, records: list[dict[str, Any]]) -> None:
        self.catalog = list(records or [])

    def set_biome_hint(self, hint: str | None) -> None:
        mapping = {
            "c": "orla_costeira_gelo",
            "orla": "orla_costeira_gelo",
            "orla_costeira_do_gelo": "orla_costeira_gelo",
            "p": "planalto_central_frostreach",
            "planalto": "planalto_central_frostreach",
            "planalto_central": "planalto_central_frostreach",
            "m": "presas_de_gelo",
            "presas": "presas_de_gelo",
            "montanha": "presas_de_gelo",
        }
        if hint in mapping:
            self._change_biome(mapping[hint], announce=False)

    def current_or_start(self, opening: str = "") -> ExplorationTurn:
        saved = self.state.get("turn")
        if isinstance(saved, dict) and saved.get("choices"):
            return ExplorationTurn.from_dict(saved)
        return self.start(opening)

    def start(self, opening: str = "") -> ExplorationTurn:
        self.state["encounter"] = None
        intro = opening.strip() or "Você interrompe a marcha para entender onde está."
        return self._idle_turn(intro)

    def choose(self, action_id: str) -> ExplorationTurn:
        if action_id.startswith("travel:"):
            return self._travel(action_id.split(":", 1)[1])
        if action_id.startswith("support:"):
            return self._support(action_id.split(":", 1)[1])
        if action_id.startswith("event:"):
            return self._resolve_event(action_id.split(":", 1)[1])
        if action_id == "continue":
            return self._idle_turn("Depois de lidar com o que encontrou, você volta a observar as rotas possíveis.")
        return self._idle_turn("A intenção não encontra uma ação possível; você reavalia o terreno.")

    def _set_initial_biome(self) -> None:
        existing = self.state.get("biome") or self.session.biome_slug
        if existing in BIOMES:
            biome = existing
        elif "fr1_nasceu_orla" in self.session.flags:
            biome = "orla_costeira_gelo"
            self.session.position_x = min(self.session.position_x, -4)
        elif "fr1_nasceu_presas" in self.session.flags:
            biome = "presas_de_gelo"
            self.session.position_y = max(self.session.position_y, 5)
        else:
            biome = "planalto_central_frostreach"
        self.state["biome"] = biome
        self.session.biome_slug = biome

    def _change_biome(self, biome: str, announce: bool = True) -> str:
        previous = self.state.get("biome")
        self.state["biome"] = biome
        self.session.biome_slug = biome
        if previous == biome or not announce:
            return ""
        name = BIOMES[biome]["name"]
        self._discover(f"bioma:{biome}")
        return f"\n\nDESCOBERTO — {name}. O diário passa a reconhecer este bioma."

    def _idle_turn(self, opening: str) -> ExplorationTurn:
        biome = BIOMES[self.state["biome"]]
        weather = self.state.get("weather", biome["weather"][0])
        ambience = self._different_choice(biome["ambience"], "last_ambience")
        urgency = self._urgency_text()
        narrative = (
            f"{opening}\n\n{ambience}\n\n"
            f"Condição atual: {weather}; Dia {self.session.day}, {self.session.hour:02d}:00. "
            f"Você está em {biome['name']}, posição aproximada "
            f"({self.session.position_x:+d}, {self.session.position_y:+d}).{urgency}"
        )
        choices: list[dict[str, Any]] = []
        directions = ["norte", "oeste", "leste", "sul"]
        for direction in directions:
            route = self._different_choice(biome["routes"][direction], f"route_{direction}")
            choices.append(self._choice(f"travel:{direction}", route))
        choices.extend(self._support_choices())
        return self._turn(f"Exploração — {biome['name']}", narrative, choices)

    def _support_choices(self) -> list[dict[str, Any]]:
        result = [self._choice("support:listen", "Parar e identificar os sons ao redor")]
        if self.session.thirst >= 35:
            result.append(self._choice("support:water", "Procurar gelo limpo e derreter água", "urgent"))
        elif self.session.hunger >= 35:
            result.append(self._choice("support:forage", "Procurar alimento sem abandonar a área", "urgent"))
        elif self.session.temperature <= -25:
            result.append(self._choice("support:shelter", "Buscar abrigo contra o frio", "urgent"))
        else:
            result.append(self._choice("support:survey", "Examinar os arredores antes de caminhar"))
        if self.session.energy <= 35:
            result.append(self._choice("support:rest", "Tentar descansar em segurança", "urgent"))
        return result

    def _travel(self, direction: str) -> ExplorationTurn:
        movement = {"norte": (0, 1), "sul": (0, -1), "leste": (1, 0), "oeste": (-1, 0)}
        dx, dy = movement.get(direction, (0, 0))
        self.session.position_x += dx
        self.session.position_y += dy
        self.session.exploration_step += 1
        hours = self.rng.choice((1, 1, 2, 2, 3))
        self.session.advance_time(hours)
        self.session.change_need("energy", -self.rng.randint(4, 8))
        self.session.change_need("hunger", self.rng.randint(2, 5))
        self.session.change_need("thirst", self.rng.randint(3, 6))
        self.session.temperature = max(-100, self.session.temperature - self.rng.randint(2, 6))
        biome_note = self._update_biome_from_position()
        biome = BIOMES[self.state["biome"]]
        if self.session.exploration_step % 2 == 0 or self.rng.random() < 0.35:
            self.state["weather"] = self.rng.choice(biome["weather"])
        survival_note = self._survival_consequences()
        encounter = self._generate_encounter(direction)
        self.state["encounter"] = encounter
        narrative = self._encounter_narrative(encounter, direction, hours)
        narrative += biome_note + survival_note
        return self._turn(
            f"{encounter['name']} — {biome['name']}",
            narrative,
            self._event_choices(encounter),
        )

    def _update_biome_from_position(self) -> str:
        x, y = self.session.position_x, self.session.position_y
        if y >= 4:
            biome = "presas_de_gelo"
        elif x <= -4:
            biome = "orla_costeira_gelo"
        else:
            biome = "planalto_central_frostreach"
        return self._change_biome(biome)

    def _generate_encounter(self, direction: str, forced_kind: str | None = None) -> dict[str, Any]:
        kind = forced_kind or self.rng.choices(
            ("fauna", "flora", "tracks", "npc", "landmark", "hazard", "settlement"),
            weights=(25, 18, 12, 12, 14, 13, 6),
            k=1,
        )[0]
        biome_key = self.state["biome"]
        biome = BIOMES[biome_key]
        if kind in {"fauna", "flora"}:
            entry = self._species_entry(kind, biome_key)
            event = {**entry, "kind": kind}
        elif kind == "tracks":
            animal = self._species_entry("fauna", biome_key)
            event = {
                "kind": "tracks",
                "name": f"Rastros de {animal['name']}",
                "slug": f"rastros_{animal['slug']}",
                "description": f"Marcas recentes sugerem {animal['description']}",
                "threat": animal.get("threat", 1),
                "target": animal,
            }
        elif kind == "npc":
            name, description = self._unseen_named(NPCS)
            event = {"kind": kind, "name": name, "slug": _slug(name), "description": description, "threat": 1}
        elif kind == "settlement":
            name, description = self._unseen_named(SETTLEMENTS)
            event = {"kind": kind, "name": name, "slug": _slug(name), "description": description, "threat": 1}
        else:
            source = biome["landmarks"] if kind == "landmark" else biome["hazards"]
            name, description = self._unseen_named(source)
            event = {
                "kind": kind,
                "name": name,
                "slug": _slug(name),
                "description": description,
                "threat": 2 if kind == "landmark" else self.rng.randint(3, 5),
            }
        event["direction"] = direction
        event["stage"] = "noticed"
        self._remember_event(event["slug"])
        return event

    def _species_entry(self, kind: str, biome_key: str) -> dict[str, Any]:
        kingdom = "fauna" if kind == "fauna" else None
        records = [
            row for row in self.catalog
            if self._catalog_biome(row.get("biome_slug")) == biome_key
            and ((kind == "fauna" and row.get("kingdom") == kingdom) or (kind == "flora" and row.get("kingdom") in {"flora", "fungi"}))
        ]
        recent = set(self.state.get("recent_events", []))
        unseen = [row for row in records if str(row.get("slug")) not in recent]
        if unseen:
            records = unseen
        if records:
            weights = []
            for row in records:
                weight = max(1, int(row.get("encounter_weight") or 1))
                if row.get("legendary"):
                    weight = max(1, weight // 8)
                weights.append(weight)
            row = self.rng.choices(records, weights=weights, k=1)[0]
            return {
                "name": row.get("name") or row.get("common_name") or "espécie desconhecida",
                "slug": row.get("slug") or _slug(str(row.get("name", "especie"))),
                "description": row.get("description") or "uma forma de vida desconhecida ocupa o caminho",
                "behavior": row.get("behavior", "neutral"),
                "threat": int(row.get("threat") or 0),
                "edible": bool(row.get("edible")),
                "poisonous": bool(row.get("poisonous")),
                "legendary": bool(row.get("legendary")),
            }
        fallback = BIOMES[biome_key][kind]
        item = self.rng.choice(fallback)
        if kind == "fauna":
            name, behavior, threat, description = item
            return {
                "name": name, "slug": _slug(name), "description": description,
                "behavior": behavior, "threat": threat, "edible": behavior == "pacific",
                "poisonous": "Serpente" in name or "Aranha" in name,
                "legendary": behavior == "legendary",
            }
        name, description, edible, poisonous = item
        return {
            "name": name, "slug": _slug(name), "description": description,
            "behavior": "pacific", "threat": 1 if poisonous else 0,
            "edible": edible, "poisonous": poisonous, "legendary": False,
        }

    @staticmethod
    def _catalog_biome(slug: Any) -> str:
        aliases = {
            "orla_costeira_do_gelo": "orla_costeira_gelo",
            "planalto_central": "planalto_central_frostreach",
        }
        value = str(slug or "")
        return aliases.get(value, value)

    def _encounter_narrative(self, event: dict[str, Any], direction: str, hours: int) -> str:
        biome = BIOMES[self.state["biome"]]
        weather = self.state.get("weather")
        discovery_key = f"{event['kind']}:{event['slug']}"
        first = discovery_key not in self.state["discoveries"]
        self._discover(discovery_key)
        discovery = f"DESCOBERTO — {event['name']}.\n\n" if first else ""
        danger = ""
        if event.get("legendary"):
            danger = " O que está diante de você corresponde apenas a relatos quase míticos."
        elif int(event.get("threat", 0)) >= 4:
            danger = " Seu corpo percebe o perigo antes de sua memória encontrar um nome para ele."
        return (
            f"Você avança para {direction} durante cerca de {hours} hora(s). Sob {weather}, "
            f"{biome['ambience'][self.session.exploration_step % len(biome['ambience'])].lower()}\n\n"
            f"{discovery}{event['description'].rstrip('.')}.{danger}\n\n"
            "O deslocamento foi interrompido. Enquanto esta situação estiver ativa, as escolhas abaixo pertencem a ela — não são comandos genéricos de caminhada."
        )

    def _event_choices(self, event: dict[str, Any]) -> list[dict[str, Any]]:
        kind = event["kind"]
        stage = event.get("stage", "noticed")
        hostile = event.get("behavior") in {"predator", "territorial", "legendary"} and int(event.get("threat", 0)) >= 3
        if kind == "fauna" and hostile:
            if stage == "wounded":
                return [
                    self._choice("event:fight", f"Atacar novamente {event['name']}", "danger"),
                    self._choice("event:flee", "Fugir usando o terreno", "urgent"),
                    self._choice("event:distract", "Lançar um item para criar uma abertura"),
                ]
            return [
                self._choice("event:observe", "Ler o comportamento antes de reagir"),
                self._choice("event:hide", "Sair da linha de visão sem correr"),
                self._choice("event:flee", "Recuar imediatamente", "urgent"),
                self._choice("event:fight", f"Enfrentar {event['name']}", "danger"),
            ]
        if kind == "fauna":
            if stage == "revealed":
                return [
                    self._choice("event:track", "Seguir o animal sem ser percebido"),
                    self._choice("event:approach", "Tentar uma aproximação lenta"),
                    self._choice("event:hunt", "Tentar caçar para obter alimento", "danger"),
                    self._choice("event:leave", "Deixar o animal seguir seu caminho"),
                ]
            return [
                self._choice("event:observe", "Observar hábitos e sinais corporais"),
                self._choice("event:approach", "Aproximar-se com cuidado"),
                self._choice("event:hunt", "Preparar uma tentativa de caça", "danger"),
                self._choice("event:leave", "Evitar interferir"),
            ]
        if kind == "flora":
            if stage == "revealed":
                return [
                    self._choice("event:harvest", f"Colher {event['name']} preservando a base"),
                    self._choice("event:use", "Testar uma pequena amostra", "danger"),
                    self._choice("event:mark", "Registrar o local e deixar intacto"),
                ]
            return [
                self._choice("event:study", "Estudar forma, cheiro e reação ao calor"),
                self._choice("event:harvest", "Colher sem conhecer suas propriedades", "danger"),
                self._choice("event:mark", "Marcar no diário e não tocar"),
                self._choice("event:leave", "Ignorar e continuar depois"),
            ]
        if kind == "tracks":
            if stage == "revealed":
                return [
                    self._choice("event:follow", "Seguir na distância correta"),
                    self._choice("event:ambush", "Preparar uma emboscada", "danger"),
                    self._choice("event:leave", "Abandonar os rastros"),
                ]
            return [
                self._choice("event:identify", "Identificar idade, direção e quantidade"),
                self._choice("event:follow", "Seguir imediatamente"),
                self._choice("event:ambush", "Preparar uma emboscada", "danger"),
                self._choice("event:leave", "Evitar o que produziu as marcas"),
            ]
        if kind == "npc":
            if stage == "revealed":
                return [
                    self._choice("event:talk", f"Conversar com {event['name']}"),
                    self._choice("event:help", "Oferecer ajuda na tarefa atual"),
                    self._choice("event:follow", "Seguir à distância sem se apresentar"),
                    self._choice("event:leave", "Partir sem contato"),
                ]
            return [
                self._choice("event:call", "Chamar mostrando as mãos vazias"),
                self._choice("event:observe", "Observar antes de revelar sua presença"),
                self._choice("event:help", "Aproximar-se oferecendo ajuda"),
                self._choice("event:leave", "Evitar o desconhecido"),
            ]
        if kind == "settlement":
            return [
                self._choice("event:enter", f"Entrar em {event['name']} abertamente"),
                self._choice("event:scout", "Observar guardas, saídas e costumes"),
                self._choice("event:work", "Procurar trabalho em troca de comida e abrigo"),
                self._choice("event:leave", "Contornar o povoado e permanecer só"),
            ]
        if kind == "landmark":
            return [
                self._choice("event:investigate", "Investigar marcas, entradas e mecanismos"),
                self._choice("event:map", "Mapear o local sem entrar"),
                self._choice("event:camp", "Usar o local como abrigo temporário"),
                self._choice("event:leave", "Não correr o risco agora"),
            ]
        return [
            self._choice("event:study", "Parar e entender o ritmo do perigo"),
            self._choice("event:cross", "Atravessar pelo caminho mais curto", "danger"),
            self._choice("event:detour", "Procurar uma rota mais longa e segura"),
            self._choice("event:wait", "Esperar as condições mudarem"),
        ]

    def _resolve_event(self, action: str) -> ExplorationTurn:
        event = self.state.get("encounter")
        if not isinstance(event, dict):
            return self._idle_turn("O encontro já não está presente; restam apenas sinais no terreno.")
        if action == "leave":
            self.session.advance_time(1)
            self.state["encounter"] = None
            return self._resolution_turn(
                "Escolha de não interferir",
                f"Você deixa {event['name']} para trás. Isso também é uma decisão: o encontro permanece sem sua interferência.",
            )
        if action == "distract" and not self.session.inventory:
            return self._turn(
                f"Sem recurso para distrair {event['name']}",
                "Seu inventário está vazio. Procurar algo agora exporia sua posição por tempo demais.",
                [
                    self._choice("event:fight", "Enfrentar", "danger"),
                    self._choice("event:flee", "Tentar fugir", "urgent"),
                    self._choice("event:hide", "Tentar desaparecer no terreno"),
                ],
            )
        attribute, difficulty = self._action_test(event, action)
        die = self.rng.randint(1, 20)
        bonus = int(self.session.attributes.get(attribute, 0))
        if action == "fight":
            bonus += max(0, self.session.attack // 3)
        total = die + bonus
        success = die == 20 or (die != 1 and total >= difficulty)
        self.session.advance_time(1)
        self.session.change_need("energy", -self.rng.randint(2, 6))
        roll_text = f"D20 {die} + {bonus} ({attribute}) = {total}; dificuldade {difficulty}."

        reveal_actions = {"observe", "study", "identify", "scout"}
        if action in reveal_actions:
            event["stage"] = "revealed"
            if success:
                self.session.xp += 2
                text = self._reveal_text(event, action)
            else:
                self.session.change_need("energy", -2)
                text = "A leitura fica incompleta, mas esperar altera a situação e elimina algumas possibilidades."
            return self._turn(
                f"{event['name']} — situação revelada",
                f"{roll_text} {'SUCESSO.' if success else 'FALHA.'}\n\n{text}",
                self._event_choices(event),
            )

        text = self._outcome_text(event, action, success)
        self._apply_outcome(event, action, success)
        still_active = (
            event["kind"] == "fauna"
            and event.get("behavior") in {"predator", "territorial", "legendary"}
            and action in {"fight", "flee", "hide"}
            and not success
            and self.session.life > 0
        )
        if still_active:
            event["stage"] = "wounded"
            return self._turn(
                f"Perigo ativo — {event['name']}",
                f"{roll_text} FALHA.\n\n{text}\n\nO encontro não terminou; fugir, lutar ou improvisar continuam sendo decisões diferentes.",
                self._event_choices(event),
            )
        self.state["encounter"] = None
        return self._resolution_turn(
            f"Consequência — {event['name']}",
            f"{roll_text} {'SUCESSO.' if success else 'FALHA.'}\n\n{text}",
        )

    def _action_test(self, event: dict[str, Any], action: str) -> tuple[str, int]:
        threat = int(event.get("threat", 1))
        table = {
            "observe": ("percepcao", 8 + threat), "study": ("percepcao", 9 + threat),
            "identify": ("sobrevivencia", 9 + threat), "scout": ("furtividade", 10 + threat),
            "hide": ("furtividade", 10 + threat), "flee": ("agilidade", 9 + threat),
            "fight": ("forca", 10 + threat * 2), "distract": ("agilidade", 9 + threat),
            "track": ("sobrevivencia", 10 + threat), "follow": ("furtividade", 10 + threat),
            "approach": ("vontade", 9 + threat), "hunt": ("sobrevivencia", 10 + threat * 2),
            "ambush": ("furtividade", 11 + threat), "harvest": ("sobrevivencia", 10 + threat),
            "use": ("vontade", 11 + threat), "mark": ("percepcao", 8),
            "call": ("social", 10), "talk": ("social", 10), "help": ("social", 11),
            "enter": ("social", 10), "work": ("social", 11),
            "investigate": ("percepcao", 11 + threat), "map": ("percepcao", 9),
            "camp": ("sobrevivencia", 10), "cross": ("agilidade", 11 + threat),
            "detour": ("sobrevivencia", 9 + threat), "wait": ("vontade", 9),
        }
        return table.get(action, ("sobrevivencia", 10 + threat))

    def _reveal_text(self, event: dict[str, Any], action: str) -> str:
        kind = event["kind"]
        if kind == "fauna":
            return f"Você distingue intenção, rota de fuga e sinais de tensão de {event['name']}. Agora pode escolher com mais informação."
        if kind == "flora":
            properties = []
            if event.get("edible"):
                properties.append("há sinais de que pode servir como alimento")
            if event.get("poisonous"):
                properties.append("cor e odor sugerem toxicidade")
            detail = "; ".join(properties) or "as propriedades ainda não são totalmente conhecidas"
            return f"A estrutura reage ao calor de sua mão sem contato direto; {detail}."
        if kind == "tracks":
            return f"As marcas são recentes. Você estima direção, ritmo e o risco de alcançar {event.get('target', {}).get('name', 'a criatura')}."
        if kind == "npc":
            return f"A postura de {event['name']} não é imediatamente hostil. Equipamento e gestos revelam hábitos locais que você ainda não compreende."
        if kind == "settlement":
            return f"Você identifica entradas, vigias e áreas de trabalho de {event['name']}; morar, negociar ou apenas atravessar seriam caminhos distintos."
        return f"O padrão de {event['name']} deixa de parecer aleatório. Há um intervalo seguro, mas ele será breve."

    def _outcome_text(self, event: dict[str, Any], action: str, success: bool) -> str:
        name = event["name"]
        if success:
            table = {
                "hide": f"Você rompe a linha de visão e {name} perde seu rastro.",
                "flee": f"O terreno escolhido impede que {name} acompanhe sua fuga.",
                "fight": f"Você sobrevive ao confronto e força {name} a recuar.",
                "distract": f"O item desviado compra segundos suficientes para escapar de {name}.",
                "track": f"Você acompanha {name} e aprende uma rota segura usada pela fauna.",
                "follow": f"Seguir sem ser percebido leva a uma trilha que não aparecia no horizonte.",
                "approach": f"Sua lentidão evita uma reação agressiva; a distância entre você e {name} diminui.",
                "hunt": f"A caça termina rápido e fornece alimento, mas deixa marcas no território.",
                "ambush": f"A posição escolhida funciona; você controla o primeiro instante do encontro.",
                "harvest": f"Você recolhe parte de {name} sem destruir a fonte.",
                "use": f"A pequena amostra produz um efeito compreensível antes de causar dano grave.",
                "mark": f"O local de {name} entra no diário com referências suficientes para ser reencontrado.",
                "call": f"{name} responde e espera que você se aproxime.",
                "talk": f"A conversa revela nomes locais, uma direção e uma pequena oportunidade.",
                "help": f"A ajuda é aceita; uma relação começa por uma tarefa concreta.",
                "enter": f"Você entra em {name} sem ser tratado imediatamente como ameaça.",
                "work": f"Uma tarefa simples rende comida, calor e os primeiros rumores de {name}.",
                "investigate": f"Você encontra uma marca, passagem ou mecanismo que altera o que sabia sobre {name}.",
                "map": f"Distâncias e pontos de referência de {name} ficam registrados.",
                "camp": f"O abrigo reduz a exposição e permite recuperar energia.",
                "cross": f"Você atravessa antes que o perigo alcance o ponto crítico.",
                "detour": f"A rota longa custa tempo, mas evita o centro do perigo.",
                "wait": f"A paciência revela o momento em que a ameaça enfraquece.",
            }
            return table.get(action, f"Sua decisão diante de {name} produz uma vantagem concreta.")
        table = {
            "hide": f"{name} percebe seu movimento e encurta a distância.",
            "flee": f"Você perde apoio durante a fuga; {name} continua perto.",
            "fight": f"O ataque não rompe a defesa de {name}; você recebe o impacto e precisa decidir novamente.",
            "distract": f"{name} ignora a distração e acompanha o movimento de sua mão.",
            "hunt": f"A presa escapa e o esforço consome reservas importantes.",
            "harvest": f"A tentativa danifica a amostra e expõe sua pele a uma substância desconhecida.",
            "use": f"Seu corpo reage mal à amostra; o efeito só se torna claro quando já começou.",
            "call": f"O chamado é interpretado com cautela; {name} mantém distância.",
            "help": f"Você não compreende a tarefa a tempo e piora a primeira impressão.",
            "enter": f"Os guardas de {name} barram sua passagem e memorizam seu rosto.",
            "work": f"Ninguém confia uma tarefa a alguém sem história ou referência.",
            "investigate": f"Uma armadilha antiga ou instabilidade escondida interrompe a busca.",
            "cross": "A travessia falha no pior trecho e cobra um preço físico.",
            "detour": "A rota alternativa se fecha e faz você perder tempo e energia.",
        }
        return table.get(action, f"A tentativa diante de {name} falha e altera suas condições.")

    def _apply_outcome(self, event: dict[str, Any], action: str, success: bool) -> None:
        if success:
            self.session.xp += 3 + int(event.get("threat", 0))
            if action in {"harvest", "hunt", "fight", "ambush"}:
                item = f"recurso: {event['name']}"
                self.session.inventory.append(item)
            if action == "use":
                if event.get("poisonous"):
                    self.session.life = max(0, self.session.life - 4)
                elif event.get("edible"):
                    self.session.change_need("hunger", -15)
                else:
                    self.session.temperature = min(100, self.session.temperature + 6)
            if action == "hunt":
                self.session.change_need("hunger", -22)
            if action == "camp":
                self.session.change_need("energy", 24)
                self.session.temperature = min(100, self.session.temperature + 12)
                self.session.advance_time(3)
            if action in {"talk", "help", "enter", "work"}:
                faction = _slug(event["name"])
                self.session.reputation[faction] = min(100, self.session.reputation.get(faction, 50) + (5 if action in {"help", "work"} else 2))
            if action == "distract" and self.session.inventory:
                self.session.inventory.pop()
            self.session.flags.add(f"procedural_{event['slug']}_{action}_sucesso")
            return
        self.session.change_need("energy", -5)
        threat = max(1, int(event.get("threat", 1)))
        if action in {"fight", "flee", "hide", "cross", "investigate", "ambush"}:
            damage = self.rng.randint(1, 3) + threat
            self.session.life = max(0, self.session.life - damage)
        if action == "use" or (action == "harvest" and event.get("poisonous")):
            self.session.life = max(0, self.session.life - self.rng.randint(2, 6))
        if action in {"enter", "work", "help"}:
            faction = _slug(event["name"])
            self.session.reputation[faction] = max(0, self.session.reputation.get(faction, 50) - 3)
        self.session.flags.add(f"procedural_{event['slug']}_{action}_falha")

    def _resolution_turn(self, title: str, narrative: str) -> ExplorationTurn:
        choices = [self._choice("continue", "Reavaliar as rotas e continuar a jornada")]
        if self.session.thirst >= 35:
            choices.append(self._choice("support:water", "Resolver a sede antes de partir", "urgent"))
        if self.session.life < self.session.life_max or self.session.energy <= 35:
            choices.append(self._choice("support:rest", "Tratar ferimentos e recuperar o fôlego", "urgent"))
        if self.session.temperature <= -25:
            choices.append(self._choice("support:shelter", "Procurar proteção contra o frio", "urgent"))
        return self._turn(title, narrative + self._urgency_text(), choices)

    def _support(self, action: str) -> ExplorationTurn:
        if action in {"listen", "survey", "forage"}:
            forced = {"listen": "tracks", "survey": self.rng.choice(("flora", "landmark")), "forage": self.rng.choice(("flora", "fauna"))}[action]
            self.session.advance_time(1)
            self.session.change_need("energy", -2)
            event = self._generate_encounter("arredores", forced)
            self.state["encounter"] = event
            self._discover(f"{event['kind']}:{event['slug']}")
            lead = {
                "listen": "Você fica imóvel até separar vento, gelo e um som produzido por movimento consciente.",
                "survey": "Você escolhe altura, luz e contraste antes de examinar o terreno por partes.",
                "forage": "Em vez de caminhar sem objetivo, você procura sinais de alimento e vida.",
            }[action]
            return self._turn(
                f"{event['name']} — encontrado nos arredores",
                f"{lead}\n\nDESCOBERTO — {event['name']}. {event['description'].rstrip('.') }.",
                self._event_choices(event),
            )
        die = self.rng.randint(1, 20)
        bonus = int(self.session.attributes.get("sobrevivencia", 0))
        difficulty = 10
        success = die == 20 or (die != 1 and die + bonus >= difficulty)
        self.session.advance_time(1 if action != "rest" else 3)
        if action == "water":
            if success:
                self.session.change_need("thirst", -30)
                text = "Você separa gelo limpo, derrete aos poucos e bebe sem reduzir ainda mais a temperatura do corpo."
            else:
                self.session.temperature = max(-100, self.session.temperature - 6)
                text = "O gelo escolhido contém sal ou sedimentos; o esforço piora sua exposição sem resolver a sede."
        elif action == "shelter":
            self.session.change_need("energy", -4)
            if success:
                self.session.temperature = min(100, self.session.temperature + 16)
                self.session.flags.add("abrigo_procedural_frostreach")
                text = "A forma do terreno corta o vento. Você reforça a proteção e cria um ponto temporariamente seguro."
            else:
                self.session.temperature = max(-100, self.session.temperature - 5)
                text = "A neve não sustenta a estrutura; parte do abrigo cede antes de protegê-lo."
        else:
            if success:
                self.session.change_need("energy", 28)
                self.session.change_need("hunger", 4)
                self.session.change_need("thirst", 5)
                text = "Você encontra uma posição defensável e dorme em intervalos curtos, atento aos sons."
            else:
                self.session.change_need("energy", 8)
                self.session.temperature = max(-100, self.session.temperature - 8)
                text = "O frio e os ruídos impedem descanso profundo; apenas parte do esforço é recuperada."
        return self._resolution_turn(
            "Sobrevivência em Frostreach",
            f"D20 {die} + {bonus} (sobrevivência) = {die + bonus}; dificuldade {difficulty}. "
            f"{'SUCESSO' if success else 'FALHA'}.\n\n{text}",
        )

    def _survival_consequences(self) -> str:
        notes = []
        if self.session.temperature <= -80:
            damage = self.rng.randint(2, 5)
            self.session.life = max(0, self.session.life - damage)
            notes.append(f"A exposição extrema causa {damage} de dano.")
        if self.session.thirst >= 85:
            self.session.life = max(0, self.session.life - 2)
            notes.append("A desidratação começa a causar dano.")
        if self.session.hunger >= 85:
            self.session.change_need("energy", -6)
            notes.append("A fome reduz ainda mais sua energia.")
        return ("\n\nCONSEQUÊNCIA DE SOBREVIVÊNCIA — " + " ".join(notes)) if notes else ""

    def _urgency_text(self) -> str:
        notes = []
        if self.session.life <= max(4, self.session.life_max // 4):
            notes.append("ferimentos graves")
        if self.session.energy <= 20:
            notes.append("exaustão")
        if self.session.hunger >= 70:
            notes.append("fome intensa")
        if self.session.thirst >= 70:
            notes.append("sede intensa")
        if self.session.temperature <= -60:
            notes.append("hipotermia provável")
        return f"\n\nURGENTE — {', '.join(notes)}." if notes else ""

    def _turn(self, title: str, narrative: str, choices: list[dict[str, Any]]) -> ExplorationTurn:
        turn = ExplorationTurn(title, narrative, choices)
        self.state["turn"] = turn.as_dict()
        return turn

    @staticmethod
    def _choice(action_id: str, text: str, tone: str = "normal") -> dict[str, Any]:
        return {"id": action_id, "text": text, "tone": tone}

    def _discover(self, key: str) -> None:
        if key not in self.state["discoveries"]:
            self.state["discoveries"].append(key)
        self.session.flags.add(f"descobriu_{_slug(key)}")

    def _remember_event(self, slug: str) -> None:
        recent = self.state["recent_events"]
        recent.append(slug)
        del recent[:-8]

    def _unseen_named(self, entries: list[tuple[str, str]]) -> tuple[str, str]:
        recent = set(self.state.get("recent_events", []))
        unseen = [entry for entry in entries if _slug(entry[0]) not in recent]
        return self.rng.choice(unseen or entries)

    def _different_choice(self, values: list[str], state_key: str) -> str:
        previous = self.state.get(state_key)
        candidates = [value for value in values if value != previous]
        selected = self.rng.choice(candidates or values)
        self.state[state_key] = selected
        return selected
