from __future__ import annotations

import math
import random
import re
import unicodedata
from dataclasses import dataclass
from typing import Any

from .models import PlayerSession
from .combat.careers import SkillTreeService
from .eldorwood_content import (
    ELDORWOOD_BIOMES,
    ELDORWOOD_NPCS,
    ELDORWOOD_PHASE_DETAILS,
    ELDORWOOD_QUIET_TRAVEL,
    ELDORWOOD_ROADS,
    ELDORWOOD_SETTLEMENTS,
    REGION_MAPS,
)
from .arkanor_content import (
    ARKANOR_BIOMES,
    ARKANOR_NPCS,
    ARKANOR_PHASE_DETAILS,
    ARKANOR_QUIET_TRAVEL,
    ARKANOR_REGION_MAPS,
    ARKANOR_ROADS,
    ARKANOR_SETTLEMENTS,
    ELDORWOOD_ARKANOR_BORDER,
)
from .stonevale_content import (
    ARKANOR_STONEVALE_BORDER,
    STONEVALE_BIOMES,
    STONEVALE_NPCS,
    STONEVALE_PHASE_DETAILS,
    STONEVALE_QUIET_TRAVEL,
    STONEVALE_REGION_MAPS,
    STONEVALE_ROADS,
    STONEVALE_SETTLEMENTS,
)


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

# As regiões compartilham o motor; clima, ecologia e geografia são dados.
BIOMES.update(ELDORWOOD_BIOMES)
BIOMES.update(ARKANOR_BIOMES)
BIOMES.update(STONEVALE_BIOMES)

REGION_MAPS.update(ARKANOR_REGION_MAPS)
REGION_MAPS.update(STONEVALE_REGION_MAPS)
if not any(
    border.get("id") == ELDORWOOD_ARKANOR_BORDER["id"]
    for border in REGION_MAPS["eldorwood"]["borders"]
):
    REGION_MAPS["eldorwood"]["borders"].append(ELDORWOOD_ARKANOR_BORDER)
if not any(
    border.get("id") == ARKANOR_STONEVALE_BORDER["id"]
    for border in REGION_MAPS["arkanor"]["borders"]
):
    REGION_MAPS["arkanor"]["borders"].append(ARKANOR_STONEVALE_BORDER)


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

FROSTREACH_NPCS = [
    {"id": _slug(name), "name": name, "description": description, "faction": "frostreach"}
    for name, description in NPCS
]
FROSTREACH_SETTLEMENTS = [
    {"id": _slug(name), "name": name, "description": description}
    for name, description in SETTLEMENTS
]
REGION_NPCS = {
    "frostreach": FROSTREACH_NPCS,
    "eldorwood": ELDORWOOD_NPCS,
    "arkanor": ARKANOR_NPCS,
    "stonevale": STONEVALE_NPCS,
}
REGION_SETTLEMENTS = {
    "frostreach": FROSTREACH_SETTLEMENTS,
    "eldorwood": ELDORWOOD_SETTLEMENTS,
    "arkanor": ARKANOR_SETTLEMENTS,
    "stonevale": STONEVALE_SETTLEMENTS,
}
REGION_ROADS = {
    "eldorwood": ELDORWOOD_ROADS,
    "arkanor": ARKANOR_ROADS,
    "stonevale": STONEVALE_ROADS,
}

DAY_PHASE_DETAILS = {
    "Madrugada": (
        "A aurora oferece claridade irregular, mas as depressões do terreno continuam negras.",
        "O frio se acumula perto do solo; respirar pelo tecido poupa calor e abafa o som dos passos.",
        "As estrelas ainda servem de referência, embora nuvens rápidas escondam partes do céu.",
    ),
    "Amanhecer": (
        "A primeira luz separa camadas de relevo que durante a noite pareciam uma única parede.",
        "Cristais recentes devolvem tons azulados; rastros da madrugada ainda conservam bordas nítidas.",
        "A temperatura permanece baixa, mas a direção das sombras volta a servir como referência.",
    ),
    "Manhã": (
        "A visibilidade alcança o horizonte, revelando quanto chão ainda existe entre dois pontos reconhecíveis.",
        "A luz branca elimina parte das sombras, sem reduzir o vento que atravessa a roupa.",
        "Pequenos animais aproveitam a claridade longe de você e desaparecem antes de qualquer aproximação.",
    ),
    "Tarde": (
        "A luz incide de lado e dá profundidade às marcas no gelo; algumas são recentes, muitas não.",
        "A camada superficial amolece onde a pedra guarda calor, tornando cada apoio menos previsível.",
        "Nuvens começam a engrossar sobre o horizonte, ainda sem sinal claro de tempestade.",
    ),
    "Entardecer": (
        "As sombras se alongam depressa, transformando pequenas elevações em obstáculos difíceis de medir.",
        "A perda de luz torna abrigo e direção mais importantes do que velocidade.",
        "O vento esfria enquanto a última faixa clara permanece presa ao horizonte.",
    ),
    "Noite": (
        "Fora do alcance da aurora, o terreno existe primeiro como som e somente depois como forma.",
        "Qualquer luz seria visível de muito longe; permanecer escuro preserva anonimato e cobra orientação.",
        "A neve devolve uma claridade fraca, suficiente para andar devagar, insuficiente para confiar no relevo.",
    ),
}


class ProceduralExploration:
    """Exploração com encontros persistentes e botões derivados do contexto atual."""

    def __init__(
        self,
        session: PlayerSession,
        catalog: list[dict[str, Any]] | None = None,
        rng: random.Random | None = None,
        relationships: Any | None = None,
    ) -> None:
        self.session = session
        self.catalog = list(catalog or [])
        self.rng = rng or random.Random()
        self.relationships = relationships
        self.state = session.exploration
        self.state.setdefault("recent_events", [])
        self.state.setdefault("discoveries", [])
        self.state.setdefault("weather", "")
        self.state.setdefault("encounter", None)
        self.state.setdefault("turn", None)
        self.state.setdefault("journey", None)
        self.state.setdefault("events_today", 0)
        self.state.setdefault("events_day", session.day)
        self.state.setdefault("quiet_blocks", 0)
        self.state.setdefault("pending_scene", None)
        self.state.setdefault("border", None)
        self.state.setdefault("coordinates_by_region", {})
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
            "f": "floresta_densa_antiga",
            "floresta": "floresta_densa_antiga",
            "floresta_densa_antiga": "floresta_densa_antiga",
            "r": "pantanos_rios",
            "pantano": "pantanos_rios",
            "pantanos_rios": "pantanos_rios",
            "h": "colinas_arborizadas",
            "colinas": "colinas_arborizadas",
            "colinas_arborizadas": "colinas_arborizadas",
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
        if action_id.startswith("long:"):
            return self._long_travel(action_id.split(":", 1)[1])
        if action_id.startswith("border:"):
            return self._resolve_border(action_id.split(":", 1)[1])
        if action_id.startswith("journey:"):
            return self._progress_journey(action_id.split(":", 1)[1])
        if action_id.startswith("travel:"):
            return self._travel(action_id.split(":", 1)[1])
        if action_id.startswith("support:"):
            return self._support(action_id.split(":", 1)[1])
        if action_id.startswith("event:"):
            return self._resolve_event(action_id.split(":", 1)[1])
        if action_id == "continue":
            return self._idle_turn("Depois de lidar com o que encontrou, você volta a observar as rotas possíveis.")
        return self._idle_turn("A intenção não encontra uma ação possível; você reavalia o terreno.")

    def queue_story_journey(
        self,
        destination: str,
        transition: str,
        goal: str,
        journey: dict[str, Any] | None = None,
    ) -> ExplorationTurn:
        journey = dict(journey or {})
        distance = max(0.2, float(journey.get("distancia_km", 2.0)))
        minimum = max(10, int(journey.get("minutos_minimos", round(distance * 35))))
        self.state["journey"] = {
            "destination": destination,
            "transition": transition,
            "goal": goal,
            "distance_total_km": distance,
            "distance_remaining_km": distance,
            "minimum_total_minutes": minimum,
            "minimum_remaining_minutes": minimum,
            "terrain": journey.get("terreno", self.state.get("biome")),
            "direction": journey.get("direcao"),
            "near_civilization": bool(journey.get("perto_civilizacao", False)),
            "ready": False,
        }
        self.state["encounter"] = None
        return self._idle_turn(
            f"Você assume um objetivo, mas ele não acontece no mesmo instante: {goal}. "
            f"A estimativa inicial é de aproximadamente {distance:.1f} km, sujeita ao terreno e ao clima."
        )

    def claim_story_destination(self) -> tuple[str, str] | None:
        pending = self.state.get("pending_scene")
        if isinstance(pending, dict) and pending.get("destination"):
            result = (str(pending["destination"]), str(pending.get("transition", "")))
            self.state["pending_scene"] = None
            self.state["turn"] = None
            return result
        journey = self.state.get("journey")
        if not isinstance(journey, dict) or not journey.get("ready"):
            return None
        result = (str(journey["destination"]), str(journey.get("transition", "")))
        self.state["journey"] = None
        self.state["turn"] = None
        return result

    def current_encounter(self) -> dict[str, Any] | None:
        encounter = self.state.get("encounter")
        return dict(encounter) if isinstance(encounter, dict) else None

    def resolve_combat(self, outcome: str) -> ExplorationTurn:
        """Devolve o resultado persistente da luta para a exploração que a originou."""
        event = self.state.get("encounter")
        if not isinstance(event, dict):
            return self._idle_turn("A luta terminou, mas os sinais de sua origem já se confundem com o terreno.")
        name = str(event.get("name") or "a ameaça")
        threat = max(1, int(event.get("threat") or 1))
        self.state["encounter"] = None
        self.state["turn"] = None
        if outcome in {"victory", "captured_enemy", "enemy_fled"}:
            if event.get("kind") == "fauna":
                resource = f"recurso: {name}"
                if resource not in self.session.inventory:
                    self.session.inventory.append(resource)
            if outcome == "captured_enemy":
                detail = f"Você mantém {name} vivo e sob controle. Libertar, estudar, tratar ou entregar a criatura continuarão sendo decisões separadas."
            elif outcome == "enemy_fled":
                detail = f"{name} abandona o confronto. Isso não significa que deixou o território nem que esquecerá o encontro."
            else:
                detail = f"Você vence {name}. Ferimentos, recursos gastos, ruído e rastros permanecem; a vitória não restaura suas reservas automaticamente."
            return self._resolution_turn(f"Depois do combate — {name}", detail)
        if outcome == "escaped":
            self.session.change_need("energy", -max(2, threat))
            return self._resolution_turn(
                f"Contato rompido — {name}",
                "Você foge sem confirmar a distância final. A rota imediata muda, e retornar cedo pode reativar a ameaça.",
            )
        if outcome == "surrendered":
            if event.get("behavior") in {"predator", "legendary"}:
                self.session.life = max(1, self.session.life - threat * 2)
                lost = self.session.inventory.pop() if self.session.inventory else "nenhum item"
                detail = (
                    f"{name} não compreende rendição como um acordo. Você sobrevive abandonando {lost} e sofre novos ferimentos "
                    "antes de romper o contato."
                )
            elif event.get("behavior") == "territorial":
                detail = f"A postura baixa reduz a ameaça percebida. {name} permite o recuo, mas mantém o território."
            else:
                self.session.flags.add(f"capturado_por_{event.get('slug', 'desconhecido')}")
                detail = "Sua rendição é aceita. Equipamento, liberdade e destino agora dependem de uma consequência narrativa persistente."
            return self._resolution_turn(f"Rendição diante de {name}", detail)
        return self._resolution_turn(
            f"Derrota — {name}",
            "Você perde a consciência. Esta jornada não pode continuar sem uma consequência de resgate, captura ou morte definida pelo encontro.",
        )

    def _set_initial_biome(self) -> None:
        existing = self.state.get("biome") or self.session.biome_slug
        if existing in BIOMES:
            biome = existing
        elif self.session.region_slug == "eldorwood":
            biome = "floresta_densa_antiga"
        elif self.session.region_slug == "arkanor":
            biome = "planicies_ferteis"
        elif self.session.region_slug == "stonevale":
            biome = "platos_aridos"
        elif "fr1_nasceu_orla" in self.session.flags:
            biome = "orla_costeira_gelo"
            self.session.position_x = min(float(self.session.position_x), -1500.0)
        elif "fr1_nasceu_presas" in self.session.flags:
            biome = "presas_de_gelo"
            self.session.position_y = max(float(self.session.position_y), 1500.0)
        else:
            biome = "planalto_central_frostreach"
        self.state["biome"] = biome
        self.session.biome_slug = biome
        if not self.state.get("weather"):
            self.state["weather"] = BIOMES[biome]["weather"][0]
        coordinates = self.state["coordinates_by_region"]
        coordinates.setdefault(
            self.session.region_slug,
            {"x": float(self.session.position_x), "y": float(self.session.position_y)},
        )

    def _change_biome(self, biome: str, announce: bool = True) -> str:
        previous = self.state.get("biome")
        self.state["biome"] = biome
        self.session.biome_slug = biome
        if previous == biome or not announce:
            return ""
        self.state["weather"] = BIOMES[biome]["weather"][0]
        name = BIOMES[biome]["name"]
        self._discover(f"bioma:{biome}")
        return f"\n\nDESCOBERTO — {name}. O diário passa a reconhecer este bioma."

    def _idle_turn(self, opening: str) -> ExplorationTurn:
        biome = BIOMES[self.state["biome"]]
        weather = self.state.get("weather", biome["weather"][0])
        ambience = self._different_choice(biome["ambience"], "last_ambience")
        urgency = self._urgency_text()
        journey = self.state.get("journey")
        objective = ""
        if isinstance(journey, dict):
            objective = (
                f"\n\nObjetivo ativo: {journey['goal']}. "
                f"Distância estimada restante: {journey['distance_remaining_km']:.1f} km; "
                f"tempo mínimo restante: {journey['minimum_remaining_minutes']} minutos."
            )
        narrative = (
            f"{opening}\n\n{ambience}\n\n"
            f"Condição atual: {weather}; {self.session.clock_label}. "
            f"Você está em {biome['name']}, posição aproximada "
            f"({float(self.session.position_x):+.1f} km, {float(self.session.position_y):+.1f} km)."
            f"{objective}{urgency}"
        )
        choices: list[dict[str, Any]] = []
        exhausted = self.session.awake_minutes >= 20 * 60 or self.session.energy <= 2
        if isinstance(journey, dict) and journey.get("ready"):
            choices.append(self._choice("journey:arrive", f"Alcançar o objetivo: {journey['goal']}"))
        elif isinstance(journey, dict) and not exhausted:
            choices.extend((
                self._choice("journey:careful", f"Seguir o objetivo com cautela — {journey['goal']} (30 min)"),
                self._choice("journey:normal", f"Avançar normalmente no objetivo — {journey['goal']} (1 h)"),
                self._choice("journey:fast", f"Forçar o passo no objetivo — {journey['goal']} (1 h)", "urgent"),
            ))
        if not exhausted:
            directions = ["norte", "oeste", "leste", "sul"]
            for direction in directions:
                route = self._different_choice(biome["routes"][direction], f"route_{direction}")
                choices.append(self._choice(f"travel:{direction}", route + " — exploração livre (30 min)"))
            choices.append(
                self._choice(
                    "support:long_travel",
                    "Planejar uma marcha de longa distância — escolher direção e viajar até 8 h",
                )
            )
        else:
            narrative += (
                "\n\nSeu corpo já não sustenta outra marcha segura. Você ainda decide onde e como parar, "
                "mas precisa dormir antes de voltar a percorrer distância."
            )
        choices.extend(self._support_choices())
        return self._turn(f"Exploração — {biome['name']}", narrative, choices)

    def _support_choices(self) -> list[dict[str, Any]]:
        result = [self._choice("support:listen", "Parar e identificar os sons ao redor (10 min)")]
        if self.session.thirst >= 35:
            water_text = (
                "Procurar água segura e verificar sinais de contaminação (30 min)"
                if self.session.region_slug == "eldorwood"
                else "Procurar uma fenda úmida, cacto ou marco de poço (45 min)"
                if self.session.region_slug == "stonevale"
                else "Procurar gelo limpo e derreter água (30 min)"
            )
            result.append(self._choice("support:water", water_text, "urgent"))
        elif self.session.hunger >= 35:
            result.append(self._choice("support:forage", "Procurar alimento sem abandonar a área (1 h)", "urgent"))
        elif self.session.temperature <= -25:
            result.append(self._choice("support:shelter", "Buscar abrigo contra o frio (45 min)", "urgent"))
        else:
            result.append(self._choice("support:survey", "Examinar os arredores sem avançar (20 min)"))
        if (
            self.session.day_phase in {"Entardecer", "Noite", "Madrugada"}
            or self.session.awake_minutes >= 18 * 60
            or self.session.energy <= 10
        ):
            result.append(self._choice("support:sleep", "Preparar-se para dormir por pelo menos oito horas", "urgent"))
        if self.session.energy <= 35:
            result.append(self._choice("support:rest", "Descansar por duas horas", "urgent"))
        return result

    def _travel(self, direction: str) -> ExplorationTurn:
        movement = {"norte": (0, 1), "sul": (0, -1), "leste": (1, 0), "oeste": (-1, 0)}
        dx, dy = movement.get(direction, (0, 0))
        minutes = 30
        distance = self._movement_speed_kmh() * (minutes / 60)
        self.session.position_x = float(self.session.position_x) + dx * distance
        self.session.position_y = float(self.session.position_y) + dy * distance
        self._store_current_coordinates()
        self.session.exploration_step += 1
        march_note = self._apply_movement_cost(minutes, distance, "normal")
        biome_note = self._update_biome_from_position()
        border_note = self._check_border(direction)
        if border_note:
            return border_note
        biome = BIOMES[self.state["biome"]]
        if self.session.exploration_step % 4 == 0 or self.rng.random() < 0.15:
            self.state["weather"] = self.rng.choice(biome["weather"])
        survival_note = self._survival_consequences()
        encounter = self._roll_interruption(
            0.075, direction, near_civilization=self._near_civilization(),
        )
        if encounter:
            self.state["encounter"] = encounter
            narrative = self._encounter_narrative(encounter, direction, minutes)
            narrative += biome_note + march_note + survival_note
            return self._turn(
                f"{encounter['name']} — {biome['name']}",
                narrative,
                self._event_choices(encounter),
            )
        self.state["quiet_blocks"] += 1
        quiet = self._quiet_travel_text(direction, minutes, distance)
        return self._idle_turn(quiet + biome_note + march_note + survival_note)

    def _long_travel(self, direction: str) -> ExplorationTurn:
        if self.session.awake_minutes >= 12 * 60 or self.session.energy <= 25:
            return self._idle_turn(
                "Uma marcha de dia inteiro exige descanso e reservas. Seu estado atual permite apenas deslocamentos curtos."
            )
        movement = {"norte": (0, 1), "sul": (0, -1), "leste": (1, 0), "oeste": (-1, 0)}
        if direction not in movement:
            return self._idle_turn("A direção escolhida não forma uma rota de longa distância.")
        dx, dy = movement[direction]
        minutes = 8 * 60
        distance = self._movement_speed_kmh() * 8 * 0.88
        self.session.position_x = float(self.session.position_x) + dx * distance
        self.session.position_y = float(self.session.position_y) + dy * distance
        self._store_current_coordinates()
        self.session.exploration_step += 8
        march_note = self._apply_movement_cost(minutes, distance, "long")
        biome_note = self._update_biome_from_position()
        border_turn = self._check_border(direction)
        if border_turn:
            return border_turn
        biome = BIOMES[self.state["biome"]]
        if self.rng.random() < 0.45:
            self.state["weather"] = self.rng.choice(biome["weather"])
        survival_note = self._survival_consequences()
        encounter = self._roll_interruption(
            0.26, direction, near_civilization=self._near_civilization(),
        )
        if encounter:
            self.state["encounter"] = encounter
            narrative = self._encounter_narrative(encounter, direction, minutes)
            narrative += (
                f"\n\nA interrupção ocorre dentro de uma marcha planejada de oito horas. "
                f"Antes dela, você percorreu aproximadamente {distance:.1f} km."
                + biome_note + march_note + survival_note
            )
            return self._turn(
                f"{encounter['name']} — marcha longa",
                narrative,
                self._event_choices(encounter),
            )
        self.state["quiet_blocks"] += 1
        quiet = self._quiet_travel_text(direction, minutes, distance)
        return self._idle_turn(
            "MARCHA DE LONGA DISTÂNCIA — você reservou o dia para avançar, fez pausas curtas e não tentou transformar cada quilômetro em um acontecimento.\n\n"
            + quiet + biome_note + march_note + survival_note
        )

    def _store_current_coordinates(self) -> None:
        self.state["coordinates_by_region"][self.session.region_slug] = {
            "x": round(float(self.session.position_x), 3),
            "y": round(float(self.session.position_y), 3),
        }

    def _check_border(self, direction: str) -> ExplorationTurn | None:
        region = REGION_MAPS.get(self.session.region_slug, {})
        x = float(self.session.position_x)
        y = float(self.session.position_y)
        for border in region.get("borders", []):
            if border.get("direction") != direction:
                continue
            if not float(border.get("x_min", -math.inf)) <= x <= float(border.get("x_max", math.inf)):
                continue
            if not float(border.get("y_min", -math.inf)) <= y <= float(border.get("y_max", math.inf)):
                continue
            coordinate = x if border.get("axis") == "x" else y
            limit = float(border["limit"])
            reached = coordinate >= limit if border.get("operator") == ">=" else coordinate <= limit
            if not reached:
                continue
            self.state["border"] = dict(border)
            self._discover(f"fronteira:{border['id']}")
            return self._turn(
                str(border["name"]),
                str(border["description"])
                + "\n\nDESCOBERTO — fronteira regional. O relógio, o inventário, as relações e as consequências continuarão os mesmos se você atravessar.",
                [
                    self._choice("border:cross", f"Entrar em {REGION_MAPS[border['target_region']]['name']}"),
                    self._choice("border:stay", f"Permanecer em {REGION_MAPS[self.session.region_slug]['name']} e observar a fronteira"),
                    self._choice("border:return", "Retornar alguns quilômetros pela rota conhecida"),
                ],
            )
        return None

    def _resolve_border(self, action: str) -> ExplorationTurn:
        border = self.state.get("border")
        if not isinstance(border, dict):
            return self._idle_turn("Nenhuma fronteira está ativa diante de você.")
        if action == "cross":
            previous_region = self.session.region_slug
            self._store_current_coordinates()
            self.session.region_slug = str(border["target_region"])
            self.session.biome_slug = str(border["target_biome"])
            self.state["biome"] = self.session.biome_slug
            target_x, target_y = border["target_position"]
            self.session.position_x = float(target_x)
            self.session.position_y = float(target_y)
            self.state["weather"] = BIOMES[self.session.biome_slug]["weather"][0]
            self.state["border"] = None
            self.state["encounter"] = None
            self.state["turn"] = None
            self._store_current_coordinates()
            self.session.flags.add(f"atravessou_{border['id']}")
            self.session.flags.add(f"visitou_regiao_{self.session.region_slug}")
            return self._idle_turn(
                f"Você cruza de {REGION_MAPS[previous_region]['name']} para {REGION_MAPS[self.session.region_slug]['name']} por decisão própria. "
                "Não houve teleporte nem reinício: marcas da viagem, cansaço e vínculos atravessaram com você."
            )
        if action == "return":
            step = 4.0
            if border.get("direction") == "norte":
                self.session.position_y = float(self.session.position_y) - step
            elif border.get("direction") == "sul":
                self.session.position_y = float(self.session.position_y) + step
            elif border.get("direction") == "leste":
                self.session.position_x = float(self.session.position_x) - step
            else:
                self.session.position_x = float(self.session.position_x) + step
            self._store_current_coordinates()
        self.state["border"] = None
        return self._idle_turn(
            "Você permanece deste lado. A fronteira continua disponível e não exige uma missão para ser atravessada."
        )

    @staticmethod
    def _point_segment_distance(
        point: tuple[float, float], start: tuple[float, float], end: tuple[float, float],
    ) -> float:
        px, py = point
        ax, ay = start
        bx, by = end
        dx, dy = bx - ax, by - ay
        if dx == 0 and dy == 0:
            return math.hypot(px - ax, py - ay)
        ratio = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
        return math.hypot(px - (ax + ratio * dx), py - (ay + ratio * dy))

    def _nearest_settlement(self) -> tuple[dict[str, Any] | None, float]:
        settlements = REGION_SETTLEMENTS.get(self.session.region_slug, [])
        if not settlements or self.session.region_slug not in REGION_ROADS:
            return None, math.inf
        x, y = float(self.session.position_x), float(self.session.position_y)
        settlement = min(
            settlements,
            key=lambda item: math.hypot(x - float(item["x"]), y - float(item["y"])),
        )
        distance = math.hypot(x - float(settlement["x"]), y - float(settlement["y"]))
        return settlement, distance

    def _near_civilization(self) -> bool:
        roads = REGION_ROADS.get(self.session.region_slug)
        if roads is None:
            return False
        settlement, distance = self._nearest_settlement()
        if settlement and distance <= float(settlement.get("radius_km", 5)) * 2.5:
            return True
        point = (float(self.session.position_x), float(self.session.position_y))
        return any(
            self._point_segment_distance(point, tuple(road["a"]), tuple(road["b"]))
            <= float(road["width_km"])
            for road in roads
        )

    def _progress_journey(self, pace: str) -> ExplorationTurn:
        journey = self.state.get("journey")
        if not isinstance(journey, dict):
            return self._idle_turn("Você não possui um objetivo de viagem ativo.")
        if pace == "arrive":
            if not journey.get("ready"):
                return self._idle_turn("O objetivo ainda não foi alcançado; faltam distância e tempo de procura.")
            return self._turn(
                "Objetivo alcançado",
                f"Você está no ponto onde o objetivo pode continuar: {journey['goal']}. "
                "Entrar na cena é uma escolha; ainda é possível permanecer nos arredores.",
                [
                    self._choice(f"scene:{journey['destination']}", f"Continuar: {journey['goal']}"),
                    self._choice("continue", "Permanecer nos arredores antes de continuar"),
                ],
            )

        if self.session.awake_minutes >= 20 * 60 or self.session.energy <= 2:
            return self._idle_turn(
                "Você tenta retomar o objetivo, mas perde coordenação antes de completar o primeiro trecho. "
                "Prosseguir agora exigiria ignorar um limite físico, não apenas aceitar um risco."
            )

        settings = {
            "careful": (30, 0.62, 0.11),
            "normal": (60, 1.00, 0.075),
            "fast": (60, 1.45, 0.055),
        }
        minutes, multiplier, event_chance = settings.get(pace, settings["normal"])
        distance = self._movement_speed_kmh() * (minutes / 60) * multiplier
        remaining_distance = float(journey["distance_remaining_km"])
        traveled = min(distance, remaining_distance)
        journey["distance_remaining_km"] = max(0.0, remaining_distance - traveled)
        journey["minimum_remaining_minutes"] = max(0, int(journey["minimum_remaining_minutes"]) - minutes)
        direction = str(journey.get("direction") or "")
        if direction:
            self._move_coordinates(direction, traveled)
        self.session.exploration_step += 1
        march_note = self._apply_movement_cost(minutes, traveled, pace)
        biome_note = self._update_biome_from_position() if direction else ""
        border_turn = self._check_border(direction) if direction else None
        if border_turn:
            return border_turn
        survival_note = self._survival_consequences()

        if journey["distance_remaining_km"] <= 0.01 and journey["minimum_remaining_minutes"] <= 0:
            journey["ready"] = True
            return self._idle_turn(
                f"Depois de {minutes} minutos, referências do objetivo finalmente coincidem com o terreno. "
                f"Você percorreu {traveled:.1f} km neste trecho.{march_note}{survival_note}"
            )

        encounter = self._roll_interruption(
            event_chance,
            "a rota do objetivo",
            near_civilization=bool(journey.get("near_civilization")),
            fast=pace == "fast",
        )
        if encounter:
            self.state["encounter"] = encounter
            narrative = self._encounter_narrative(encounter, "a rota do objetivo", minutes)
            return self._turn(
                f"{encounter['name']} — interrupção da viagem",
                narrative + march_note + survival_note,
                self._event_choices(encounter),
            )
        self.state["quiet_blocks"] += 1
        quiet = self._quiet_travel_text(direction or "a rota do objetivo", minutes, traveled)
        return self._idle_turn(quiet + biome_note + march_note + survival_note)

    def _move_coordinates(self, direction: str, distance: float) -> None:
        movement = {"norte": (0, 1), "sul": (0, -1), "leste": (1, 0), "oeste": (-1, 0)}
        dx, dy = movement.get(direction, (0, 0))
        self.session.position_x = float(self.session.position_x) + dx * float(distance)
        self.session.position_y = float(self.session.position_y) + dy * float(distance)
        self._store_current_coordinates()

    def _movement_speed_kmh(self) -> float:
        biome = BIOMES.get(self.state.get("biome"), {})
        if "speed_kmh" in biome:
            return float(biome["speed_kmh"])
        return {
            "orla_costeira_gelo": 1.8,
            "planalto_central_frostreach": 2.4,
            "presas_de_gelo": 1.2,
        }.get(self.state.get("biome"), 1.8)

    def _apply_movement_cost(self, minutes: int, distance: float, pace: str) -> str:
        self.session.advance_minutes(minutes, traveling=True)
        self.session.distance_traveled_km = round(self.session.distance_traveled_km + distance, 2)
        energy_per_hour = {"careful": 3.0, "normal": 5.0, "fast": 8.0, "long": 4.5}.get(pace, 5.0)
        energy_cost = max(2, math.ceil((minutes / 60) * energy_per_hour))
        self.session.change_need("energy", -energy_cost)
        self.session.change_need("hunger", max(1, minutes // 60))
        self.session.change_need("thirst", max(1, minutes // 45))
        biome = BIOMES.get(self.state.get("biome"), {})
        temperature_delta = int(biome.get("temperature_delta", -1))
        exposure_blocks = max(1, math.ceil(minutes / 120))
        if self.session.day_phase in {"Noite", "Madrugada"} and temperature_delta < 0:
            temperature_delta -= 1
        if pace == "fast" and temperature_delta < 0:
            temperature_delta += 1
        self.session.temperature = max(
            -100,
            min(100, self.session.temperature + temperature_delta * exposure_blocks),
        )
        if self.session.travel_minutes_today > 8 * 60:
            self.session.flags.add("marcha_forcada")
            extra_hours = max(1, (self.session.travel_minutes_today - 8 * 60 + 59) // 60)
            difficulty = 10 + extra_hours
            die = self.rng.randint(1, 20)
            success = die == 20 or (die != 1 and die >= difficulty)
            if success:
                self.session.change_need("energy", -3)
                return (
                    f"\n\nMARCHA FORÇADA — D20 {die} contra dificuldade {difficulty}: sucesso. "
                    "Você mantém o passo, mas o esforço consome energia adicional."
                )
            self.session.change_need("energy", -8)
            if extra_hours >= 4:
                self.session.life = max(0, self.session.life - 1)
            return (
                f"\n\nMARCHA FORÇADA — D20 {die} contra dificuldade {difficulty}: falha. "
                "Frio, fadiga e perda de coordenação cobram energia"
                + (" e 1 ponto de vida." if extra_hours >= 4 else ".")
            )
        return ""

    def _roll_interruption(
        self,
        chance: float,
        direction: str,
        *,
        near_civilization: bool,
        fast: bool = False,
    ) -> dict[str, Any] | None:
        if self.state.get("events_day") != self.session.day:
            self.state["events_day"] = self.session.day
            self.state["events_today"] = 0
        if int(self.state.get("events_today", 0)) >= 2:
            return None
        if self.session.day_phase in {"Noite", "Madrugada"}:
            chance *= 1.25
        if self.rng.random() >= chance:
            return None
        if near_civilization:
            settlement, settlement_distance = self._nearest_settlement()
            settlement_is_near = bool(
                settlement
                and settlement_distance <= float(settlement.get("radius_km", 5)) * 2.5
            )
            kinds = ["fauna", "flora", "tracks", "landmark", "hazard", "npc"]
            weights = [18, 14, 13, 10, 14 if fast else 8, 20]
            if settlement_is_near:
                kinds.append("settlement")
                weights.append(17)
        else:
            kinds = ("fauna", "flora", "tracks", "landmark", "hazard")
            weights = (31, 25, 21, 13, 20 if fast else 10)
        kind = self.rng.choices(kinds, weights=weights, k=1)[0]
        self.state["events_today"] = int(self.state.get("events_today", 0)) + 1
        self.state["quiet_blocks"] = 0
        return self._generate_encounter(direction, kind)

    def _quiet_travel_text(self, direction: str, minutes: int, distance: float) -> str:
        biome = BIOMES[self.state["biome"]]
        frost_quiet = (
            "Nenhuma presença reage à sua passagem. Apenas a vegetação baixa muda de direção sob o vento.",
            "Você encontra rastros antigos demais para seguir. Neve nova já arredondou todas as bordas.",
            "Uma ave cruza o horizonte muito longe; ela nunca altera o voo por sua causa.",
            "O trecho contém apenas gelo, pedra e colônias comuns de líquen. Nada exige uma decisão imediata.",
            "Há sinais de fauna — pelos, fezes congeladas e marcas dispersas — mas nenhum animal permanece perto.",
            "O vento ocupa quase todo o período. Caminhar e conservar calor são os únicos acontecimentos.",
            "Você para duas vezes para conferir a direção. O horizonte continua vazio de fumaça ou construções.",
            "Pequenas formas de vida permanecem sob a neve, visíveis apenas por alterações no relevo.",
        )
        quiet_by_region = {
            "eldorwood": ELDORWOOD_QUIET_TRAVEL,
            "arkanor": ARKANOR_QUIET_TRAVEL,
            "stonevale": STONEVALE_QUIET_TRAVEL,
        }
        quiet = quiet_by_region.get(self.session.region_slug, frost_quiet)
        detail = quiet[(self.session.exploration_step + self.state["quiet_blocks"]) % len(quiet)]
        phase_by_region = {
            "eldorwood": ELDORWOOD_PHASE_DETAILS,
            "arkanor": ARKANOR_PHASE_DETAILS,
            "stonevale": STONEVALE_PHASE_DETAILS,
        }
        phase_table = phase_by_region.get(self.session.region_slug, DAY_PHASE_DETAILS)
        phase_details = phase_table[self.session.day_phase]
        phase_detail = phase_details[(self.session.exploration_step + self.session.day) % len(phase_details)]
        if distance < 0.05:
            opening = (
                f"Durante {minutes} minutos, você procura referências nos arredores do objetivo, "
                "sem acrescentar distância à marcha. "
            )
        else:
            opening = (
                f"Você percorre cerca de {distance:.1f} km em direção a {direction} "
                f"durante {minutes} minutos. "
            )
        return (
            opening + detail + "\n\n" + phase_detail + "\n\n"
            + biome["ambience"][self.session.exploration_step % len(biome["ambience"])]
        )

    def _update_biome_from_position(self) -> str:
        x, y = float(self.session.position_x), float(self.session.position_y)
        if self.session.region_slug == "eldorwood":
            if y < 600 or (x > 1250 and y < 1450):
                biome = "pantanos_rios"
            elif y >= 2350 or (x <= -1250 and y >= 1650):
                biome = "colinas_arborizadas"
            else:
                biome = "floresta_densa_antiga"
        elif self.session.region_slug == "arkanor":
            if x >= 650 and y < 1700:
                biome = "vales_verdes"
            elif x <= -650 or y < 300:
                biome = "colinas_suaves"
            else:
                biome = "planicies_ferteis"
        elif self.session.region_slug == "stonevale":
            if y <= -350:
                biome = "vales_ferteis_isolados"
            elif x >= 650:
                biome = "canions_profundos"
            else:
                biome = "platos_aridos"
        elif self.session.region_slug == "frostreach":
            if y >= 1500:
                biome = "presas_de_gelo"
            elif x <= -1500:
                biome = "orla_costeira_gelo"
            else:
                biome = "planalto_central_frostreach"
        else:
            return ""
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
            npc = self._select_npc()
            event = {
                "kind": kind,
                "name": npc["name"],
                "slug": str(npc.get("id") or _slug(npc["name"])),
                "npc_id": str(npc.get("id") or _slug(npc["name"])),
                "description": npc["description"],
                "threat": 1,
                "race": npc.get("race"),
                "role": npc.get("role"),
                "faction": npc.get("faction"),
                "values": list(npc.get("values") or []),
                "red_lines": list(npc.get("red_lines") or []),
            }
        elif kind == "settlement":
            settlement, distance = self._nearest_settlement()
            if settlement is None:
                candidates = REGION_SETTLEMENTS.get(self.session.region_slug, FROSTREACH_SETTLEMENTS)
                settlement = self.rng.choice(candidates)
                distance = 0.0
            event = {
                "kind": kind,
                "name": settlement["name"],
                "slug": str(settlement.get("id") or _slug(settlement["name"])),
                "description": settlement["description"],
                "threat": 1,
                "settlement_id": settlement.get("id"),
                "scene_id": settlement.get("scene_id"),
                "population": settlement.get("population"),
                "settlement_type": settlement.get("type"),
                "distance_km": round(float(distance), 1),
            }
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

    def _select_npc(self) -> dict[str, Any]:
        candidates = list(REGION_NPCS.get(self.session.region_slug, FROSTREACH_NPCS))
        if self.session.region_slug in REGION_ROADS:
            x, y = float(self.session.position_x), float(self.session.position_y)
            nearby = [
                npc for npc in candidates
                if math.hypot(x - float(npc.get("x", x)), y - float(npc.get("y", y))) <= 180.0
            ]
            traveler_factions = {
                "estradas_livres", "arquivo_da_lanterna", "cartografos_da_aurora",
                "correio_dos_tribunais", "coro_de_navegadores", "vigias_da_fronteira",
            }
            travelers = [npc for npc in candidates if npc.get("faction") in traveler_factions]
            candidates = nearby or travelers or candidates
        recent = set(self.state.get("recent_events", []))
        unseen = [npc for npc in candidates if str(npc.get("id")) not in recent]
        return self.rng.choice(unseen or candidates)

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
            "vales_fertis_isolados": "vales_ferteis_isolados",
        }
        value = str(slug or "")
        return aliases.get(value, value)

    def _encounter_narrative(self, event: dict[str, Any], direction: str, minutes: int) -> str:
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
            f"Você avança por {direction} durante {minutes} minutos. Sob {weather}, "
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
            self.session.advance_minutes(10)
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
        tree_effects = SkillTreeService.effects(self.session)
        action_bonuses = {
            "observe": ("lore_bonus", "exploration_bonus"),
            "study": ("lore_bonus",), "identify": ("lore_bonus", "survival_bonus"),
            "scout": ("exploration_bonus", "stealth_bonus"),
            "hide": ("stealth_bonus",), "flee": ("bonus_evasion", "survival_bonus"),
            "track": ("survival_bonus", "exploration_bonus"),
            "follow": ("stealth_bonus", "exploration_bonus"),
            "hunt": ("gather_bonus", "survival_bonus"),
            "harvest": ("gather_bonus", "alchemy_bonus"),
            "use": ("alchemy_bonus", "lore_bonus"),
            "call": ("social_bonus",), "talk": ("social_bonus", "lore_bonus"),
            "help": ("social_bonus", "craft_bonus"), "enter": ("social_bonus",),
            "work": ("craft_bonus", "trade_bonus"),
            "investigate": ("lore_bonus", "exploration_bonus"),
            "map": ("exploration_bonus", "lore_bonus"),
            "camp": ("survival_bonus", "craft_bonus"),
        }
        bonus += sum(tree_effects.get(key, 0) for key in action_bonuses.get(action, ()))
        if action == "fight":
            bonus += max(0, self.session.attack // 3)
        total = die + bonus
        success = die == 20 or (die != 1 and total >= difficulty)
        durations = {
            "observe": 10, "study": 20, "identify": 10, "scout": 20,
            "hide": 5, "flee": 10, "fight": 5, "distract": 5,
            "track": 30, "follow": 30, "approach": 15, "hunt": 60,
            "ambush": 30, "harvest": 30, "use": 10, "mark": 10,
            "call": 5, "talk": 20, "help": 45, "enter": 15,
            "work": 120, "investigate": 30, "map": 30, "camp": 120,
            "cross": 20, "detour": 60, "wait": 60,
        }
        self.session.advance_minutes(durations.get(action, 15))
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
        if event.get("kind") == "npc":
            text += self._relationship_summary(str(event.get("npc_id") or event.get("slug")))
        if (
            success
            and event.get("kind") == "settlement"
            and action == "enter"
            and event.get("scene_id")
        ):
            self.state["encounter"] = None
            self.state["pending_scene"] = {
                "destination": str(event["scene_id"]),
                "transition": (
                    f"Depois da aproximação e dos controles de entrada, você alcança {event['name']}. "
                    "O lugar possui rotina, pessoas e espaços próprios; entrar não encerra a liberdade de partir."
                ),
            }
            return self._turn(
                f"Entrada disponível — {event['name']}",
                f"{roll_text} SUCESSO.\n\n{text}\n\nA cidade ou vila agora pode ser acessada como um local persistente.",
                [
                    self._choice(f"scene:{event['scene_id']}", f"Entrar em {event['name']}"),
                    self._choice("continue", "Permanecer fora das construções por enquanto"),
                ],
            )
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
            profession_actions = {
                "harvest", "hunt", "track", "follow", "identify", "study",
                "work", "help", "map", "investigate", "camp", "scout",
            }
            if action in profession_actions:
                SkillTreeService.grant_xp(
                    self.session,
                    4 + int(event.get("threat", 0)),
                    profession=True,
                )
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
            if action in {"talk", "help", "enter", "work"}:
                faction = _slug(event["name"])
                self.session.reputation[faction] = min(100, self.session.reputation.get(faction, 50) + (5 if action in {"help", "work"} else 2))
            if event.get("kind") == "npc" and action in {"call", "talk", "help", "approach"}:
                self._apply_npc_relationship(event, action, True)
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
        if event.get("kind") == "npc" and action in {"call", "talk", "help", "approach", "follow"}:
            self._apply_npc_relationship(event, action, False)
        self.session.flags.add(f"procedural_{event['slug']}_{action}_falha")

    def _apply_npc_relationship(self, event: dict[str, Any], action: str, success: bool) -> None:
        if self.relationships is None:
            return
        identity = {
            "name": event.get("name"),
            "faction": event.get("faction"),
            "values": list(event.get("values") or []),
            "red_lines": list(event.get("red_lines") or []),
        }
        npc_id = str(event.get("npc_id") or event.get("slug"))
        self.relationships.meet(npc_id, **identity)
        if success:
            changes = {
                "call": {"trust": 2},
                "talk": {"trust": 4, "warmth": 2},
                "help": {"trust": 8, "respect": 7, "warmth": 3},
                "approach": {"trust": 2},
            }.get(action, {})
            reason = f"O primeiro contato por meio de '{action}' terminou de forma favorável."
        else:
            changes = {
                "call": {"trust": -2},
                "talk": {"trust": -3, "resentment": 2},
                "help": {"trust": -4, "respect": -3, "resentment": 4},
                "approach": {"fear": 3, "trust": -2},
                "follow": {"trust": -8, "resentment": 7, "fear": 3},
            }.get(action, {})
            reason = f"O contato por meio de '{action}' criou cautela ou ressentimento."
        self.relationships.apply(
            npc_id,
            changes,
            reason=reason,
            source="procedural_exploration",
            **identity,
        )

    def _relationship_summary(self, npc_id: str) -> str:
        if self.relationships is None:
            return ""
        record = self.relationships.get(npc_id)
        if not record:
            return ""
        labels = {
            "acquaintance": "conhecido",
            "wary": "cauteloso",
            "hostile": "hostil",
            "enemy": "inimigo",
            "afraid": "amedrontado",
            "friendly": "amistoso",
            "trusted": "confiança consolidada",
            "devoted": "vínculo profundo",
        }
        status = labels.get(str(record.get("status")), str(record.get("status") or "desconhecido"))
        return (
            f"\n\nRELAÇÃO — {record.get('name', npc_id)}: {status}. "
            f"Confiança {int(record.get('trust', 0)):+d}; respeito {int(record.get('respect', 0)):+d}; "
            f"proximidade {int(record.get('warmth', 0)):+d}; medo {int(record.get('fear', 0)):+d}; "
            f"ressentimento {int(record.get('resentment', 0)):+d}."
        )

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
        if action == "long_travel":
            biome = BIOMES[self.state["biome"]]
            return self._turn(
                "Planejar marcha de longa distância",
                "Você deixa de procurar acontecimentos a cada poucos metros e escolhe uma direção para dedicar até oito horas à viagem. "
                "O tempo, a distância, o clima e uma possível interrupção serão resolvidos como parte da marcha; não haverá salto instantâneo.",
                [
                    self._choice(f"long:{direction}", biome["routes"][direction][0] + " — marcha de até 8 h")
                    for direction in ("norte", "oeste", "leste", "sul")
                ] + [self._choice("continue", "Cancelar o plano e continuar nos arredores")],
            )
        if action in {"listen", "survey", "forage"}:
            durations = {"listen": 10, "survey": 20, "forage": 60}
            chances = {"listen": 0.16, "survey": 0.24, "forage": 0.42}
            minutes = durations[action]
            self.session.advance_minutes(minutes)
            self.session.change_need("energy", -1 if action != "forage" else -3)
            lead = {
                "listen": "Você fica imóvel até separar vento, gelo e os ruídos do próprio corpo.",
                "survey": "Você escolhe altura, luz e contraste antes de examinar o terreno por partes.",
                "forage": "Em vez de caminhar sem objetivo, você procura sinais de alimento e vida.",
            }[action]
            if self.state.get("events_day") != self.session.day:
                self.state["events_day"] = self.session.day
                self.state["events_today"] = 0
            can_find = int(self.state.get("events_today", 0)) < 2 and self.rng.random() < chances[action]
            if can_find:
                forced = {
                    "listen": self.rng.choice(("tracks", "fauna")),
                    "survey": self.rng.choice(("flora", "landmark", "tracks")),
                    "forage": self.rng.choice(("flora", "flora", "fauna")),
                }[action]
                event = self._generate_encounter("os arredores", forced)
                self.state["events_today"] = int(self.state.get("events_today", 0)) + 1
                self.state["encounter"] = event
                self._discover(f"{event['kind']}:{event['slug']}")
                return self._turn(
                    f"{event['name']} — encontrado nos arredores",
                    f"{lead}\n\nDESCOBERTO — {event['name']}. {event['description'].rstrip('.') }.",
                    self._event_choices(event),
                )
            quiet = {
                "listen": "Durante dez minutos, nenhum som mantém ritmo suficiente para indicar aproximação. O silêncio é informação: nada parece estar seguindo você.",
                "survey": "A inspeção revela apenas relevo comum, vegetação dispersa e marcas antigas. Você melhora sua referência de direção, mas não encontra um ponto especial.",
                "forage": "Uma hora de procura encontra vida demais para chamar o lugar de vazio, porém nada que você reconheça como alimento seguro. O tempo gasto não produz um recurso.",
            }[action]
            return self._idle_turn(f"{lead}\n\n{quiet}")

        if action == "sleep":
            current = self.session.hour * 60 + self.session.minute
            until_six = (24 * 60 - current + 6 * 60) % (24 * 60)
            sleep_minutes = max(8 * 60, until_six)
            shelter_flag = f"abrigo_procedural_{self.session.region_slug}"
            sheltered = shelter_flag in self.session.flags
            self.session.complete_rest(sleep_minutes)
            if sheltered:
                self.session.change_need("energy", 55)
                self.session.temperature = min(100, self.session.temperature + 12)
                text = "O abrigo reduz vento, umidade e exposição. Você dorme em períodos longos e acorda quando a luz começa a retornar."
            else:
                self.session.change_need("energy", 30)
                exposure = 7 if self.session.region_slug == "eldorwood" else 12
                self.session.temperature = max(-100, self.session.temperature - exposure)
                text = "Sem abrigo adequado, frio, umidade e ruídos interrompem o sono. Ainda assim, várias horas passam e um novo período do dia começa."
            self.session.change_need("hunger", 10)
            self.session.change_need("thirst", 12)
            return self._resolution_turn(
                "A noite passa",
                f"Você descansa por {sleep_minutes // 60} h {sleep_minutes % 60:02d} min.\n\n{text}\n\n{self.session.clock_label}.",
            )

        die = self.rng.randint(1, 20)
        bonus = int(self.session.attributes.get("sobrevivencia", 0))
        difficulty = 10
        success = die == 20 or (die != 1 and die + bonus >= difficulty)
        durations = {"water": 30, "shelter": 45, "rest": 120}
        self.session.advance_minutes(durations.get(action, 30))
        if action == "water":
            if success:
                self.session.change_need("thirst", -30)
                text = (
                    "Você verifica corrente, algas e rastros acima da fonte antes de beber e armazenar água."
                    if self.session.region_slug == "eldorwood"
                    else "Você separa gelo limpo, derrete aos poucos e bebe sem reduzir ainda mais a temperatura do corpo."
                )
            else:
                if self.session.region_slug == "eldorwood":
                    self.session.life = max(0, self.session.life - 2)
                    text = "Odor e cor parecem normais, mas a água contém matéria orgânica demais. A sede não é resolvida e a amostra causa mal-estar."
                else:
                    self.session.temperature = max(-100, self.session.temperature - 6)
                    text = "O gelo escolhido contém sal ou sedimentos; o esforço piora sua exposição sem resolver a sede."
        elif action == "shelter":
            self.session.change_need("energy", -4)
            if success:
                self.session.temperature = min(100, self.session.temperature + 16)
                self.session.flags.add(f"abrigo_procedural_{self.session.region_slug}")
                text = "A forma do terreno corta o vento. Você reforça a proteção e cria um ponto temporariamente seguro."
            else:
                self.session.temperature = max(-100, self.session.temperature - 5)
                text = "A neve não sustenta a estrutura; parte do abrigo cede antes de protegê-lo."
        else:
            if success:
                self.session.change_need("energy", 20)
                self.session.change_need("hunger", 3)
                self.session.change_need("thirst", 4)
                text = "Você encontra uma posição defensável e repousa por duas horas em intervalos curtos, atento aos sons."
            else:
                self.session.change_need("energy", 8)
                self.session.temperature = max(-100, self.session.temperature - 8)
                text = "O frio e os ruídos consomem as duas horas; apenas parte do esforço é recuperada."
        return self._resolution_turn(
            f"Sobrevivência em {self.session.region_name}",
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
