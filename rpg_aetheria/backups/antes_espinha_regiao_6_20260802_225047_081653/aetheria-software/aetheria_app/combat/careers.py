from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any, Iterable


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = "".join(char for char in normalized if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "_", ascii_text.casefold()).strip("_")


@dataclass(frozen=True)
class SkillNode:
    slug: str
    name: str
    description: str
    tier: int
    cost: int
    branch: str
    prerequisites: tuple[str, ...] = ()
    effects: tuple[dict[str, Any], ...] = ()


@dataclass(frozen=True)
class CareerDefinition:
    slug: str
    name: str
    category: str
    role: str
    resource: str
    description: str
    branches: dict[str, tuple[SkillNode, ...]]
    innate_name: str
    innate_description: str
    stat_modifiers: dict[str, int] = field(default_factory=dict)
    proficiencies: tuple[str, ...] = ()
    starting_gear: tuple[str, ...] = ()

    @property
    def nodes(self) -> tuple[SkillNode, ...]:
        return tuple(node for nodes in self.branches.values() for node in nodes)


# Cada mecânica possui um efeito realmente consumido pelo motor. Os valores por
# nível são pequenos de propósito: escolhas de árvore somam, mas não apagam o
# valor de posição, equipamento, terreno ou sorte.
MECHANICS: dict[str, tuple[str, str, tuple[int, ...]]] = {
    "ofensiva": ("bonus_attack", "aumenta a precisão e a pressão ofensiva", (1, 1, 2, 2, 3)),
    "potencia": ("bonus_damage", "aumenta o dano depois da mitigação", (1, 1, 2, 2, 3)),
    "defesa": ("bonus_defense", "melhora bloqueio, aparo e resistência", (1, 1, 2, 2, 3)),
    "mobilidade": ("bonus_evasion", "melhora esquiva e reposicionamento", (1, 1, 2, 2, 3)),
    "critico": ("bonus_critical", "amplia a margem de acerto crítico", (1, 1, 2, 2, 3)),
    "controle": ("bonus_control", "fortalece empurrões e condições", (2, 3, 4, 5, 7)),
    "arcano": ("bonus_magic", "fortalece magia e canalização", (1, 1, 2, 2, 3)),
    "eficiencia_mana": ("mana_efficiency", "reduz o custo de feitiços", (1, 1, 1, 2, 2)),
    "cura": ("bonus_healing", "fortalece cura, barreiras e estabilização", (1, 2, 3, 4, 6)),
    "invocacao": ("summon_power", "fortalece aliados invocados", (1, 1, 2, 2, 3)),
    "sobrevivencia": ("survival_bonus", "melhora testes e recuperação no ermo", (1, 1, 2, 2, 3)),
    "furtividade": ("stealth_bonus", "melhora ocultação, emboscada e fuga", (1, 1, 2, 2, 3)),
    "social": ("social_bonus", "melhora influência, trégua e rendição", (1, 1, 2, 2, 3)),
    "coleta": ("gather_bonus", "aumenta rendimento e descoberta de recursos", (1, 1, 2, 2, 3)),
    "oficio": ("craft_bonus", "eleva qualidade, reparo e durabilidade", (1, 1, 2, 2, 3)),
    "alquimia": ("alchemy_bonus", "eleva potência e segurança de preparados", (1, 1, 2, 2, 3)),
    "comercio": ("trade_bonus", "melhora preço, oferta e leitura de mercado", (1, 1, 2, 2, 3)),
    "conhecimento": ("lore_bonus", "melhora estudo, identificação e rituais", (1, 1, 2, 2, 3)),
    "exploracao": ("exploration_bonus", "melhora navegação e revela rotas", (1, 1, 2, 2, 3)),
    "lideranca": ("leadership_bonus", "fortalece moral e companheiros", (1, 1, 2, 2, 3)),
}

TIER_LABELS = ("Fundamento", "Técnica", "Domínio", "Assinatura", "Ápice")
TIER_COSTS = (1, 1, 2, 2, 3)


def _branch_nodes(career_slug: str, career_name: str, branch_name: str, mechanic: str) -> tuple[SkillNode, ...]:
    effect_key, explanation, values = MECHANICS[mechanic]
    branch_slug = slugify(branch_name)
    nodes: list[SkillNode] = []
    previous = ""
    for index, (label, cost, value) in enumerate(zip(TIER_LABELS, TIER_COSTS, values), start=1):
        node_slug = f"{career_slug}.{branch_slug}.{index}"
        effects: list[dict[str, Any]] = [{"type": effect_key, "value": value}]
        if index == 3:
            effects.append({"type": "unlock_action", "value": f"tecnica_{career_slug}_{branch_slug}"})
        if index == 5:
            effects.append({"type": "capstone", "value": f"apice_{career_slug}_{branch_slug}"})
        nodes.append(SkillNode(
            slug=node_slug,
            name=f"{label} — {branch_name}",
            description=(
                f"{career_name}: {explanation}. Grau {index}; no terceiro grau libera uma técnica ativa "
                "e no quinto consolida o ápice deste caminho."
            ),
            tier=index,
            cost=cost,
            branch=branch_name,
            prerequisites=(previous,) if previous else (),
            effects=tuple(effects),
        ))
        previous = node_slug
    return tuple(nodes)


# 24 classes de batalha + 16 profissões = 40 caminhos. Nenhuma raça é impedida
# de aprender um caminho; mestres, cultura, reputação e tempo de treino podem
# influenciar o acesso dentro da narrativa.
CAREER_SPECS = (
    # slug, nome, categoria, função, recurso, descrição, inata, descrição da inata,
    # modificadores, proficiências, equipamento, três (ramo, mecânica)
    ("guerreiro", "Guerreiro", "battle", "linha de frente", "vigor", "Combatente adaptável que lê ritmo, alcance e abertura.", "Segundo Fôlego", "Uma vez por combate, recupera vigor e ganha Guarda.", {"attack": 2, "life_max": 3}, ("espadas", "machados", "escudos"), ("Espada Curta de Ferro", "Escudo de Madeira"), (("Mestre de Armas", "ofensiva"), ("Muralha Móvel", "defesa"), ("Comando de Campo", "lideranca"))),
    ("guardiao", "Guardião", "battle", "tanque", "vigor", "Protege aliados e domina gargalos.", "Interposição", "Pode receber parte do ataque destinado a um aliado próximo.", {"defense": 3, "life_max": 4}, ("escudos", "peitorais", "macas"), ("Maça de Ferro", "Escudo Reforçado"), (("Bastião", "defesa"), ("Provocação", "controle"), ("Juramento de Guarda", "lideranca"))),
    ("berserker", "Berserker", "battle", "dano sustentado", "fúria", "Transforma ferimentos e risco em pressão ofensiva.", "Fúria Crescente", "Recebe dano bônus quando a vida cai, sem perder o controle automaticamente.", {"attack": 3, "defense": -1, "life_max": 3}, ("machados", "martelos", "armadura_media"), ("Machado de Batalha",), (("Fúria", "potencia"), ("Dor Convertida", "defesa"), ("Ruptura", "controle"))),
    ("duelista", "Duelista", "battle", "precisão", "ímpeto", "Especialista em um oponente, aparos e contra-ataques.", "Marca do Duelo", "Marca um adversário e melhora aparo contra ele.", {"attack": 2, "speed": 2}, ("espadas", "adagas", "armadura_leve"), ("Rapieira da Vigia",), (("Esgrima", "critico"), ("Contratempo", "defesa"), ("Passo Medido", "mobilidade"))),
    ("lanceiro", "Lanceiro", "battle", "alcance", "vigor", "Mantém inimigos fora da distância ideal e interrompe avanços.", "Recepção", "Ataca como reação quando um inimigo entra em alcance.", {"attack": 2, "defense": 1}, ("lancas", "escudos", "armadura_media"), ("Lança de Caça",), (("Linha de Ponta", "ofensiva"), ("Muralha de Lanças", "controle"), ("Caçador de Gigantes", "potencia"))),
    ("cavaleiro", "Cavaleiro", "battle", "choque e proteção", "ímpeto", "Combina armadura, investida e dever para controlar a batalha.", "Investida", "Converte deslocamento em impacto e ameaça.", {"defense": 2, "life_max": 2}, ("lancas", "espadas", "armadura_pesada"), ("Espada Longa de Aço", "Escudo Reforçado"), (("Investida", "potencia"), ("Cavalaria", "mobilidade"), ("Código de Honra", "lideranca"))),
    ("patrulheiro", "Patrulheiro", "battle", "exploração armada", "foco", "Mistura rastreamento, armas e adaptação ao bioma.", "Inimigo Estudado", "Observar revela resistência e comportamento do alvo.", {"speed": 2, "attack": 1}, ("arcos", "espadas", "sobrevivencia"), ("Arco Curto de Teixo", "Faca de Osso"), (("Trilhas", "exploracao"), ("Predador Estudado", "ofensiva"), ("Guarda do Ermo", "sobrevivencia"))),
    ("cacador", "Caçador", "battle", "emboscada", "foco", "Prepara terreno, escolhe a presa e conserva recursos.", "Preparar Armadilha", "Cria uma zona que causa dano e Imobiliza.", {"attack": 1, "critical": 2}, ("arcos", "bestas", "armadilhas"), ("Arco Curto de Teixo", "Armadilha de Caça"), (("Armadilhas", "controle"), ("Tiro Vital", "critico"), ("Leitura de Rastros", "sobrevivencia"))),
    ("arqueiro", "Arqueiro", "battle", "dano à distância", "foco", "Domina linha de visão, cobertura, munição e distância.", "Tiro Preparado", "Troca tempo por precisão e perfuração.", {"attack": 2, "critical": 1}, ("arcos", "bestas", "armadura_leve"), ("Arco Longo de Freixo",), (("Precisão", "ofensiva"), ("Chuva de Projéteis", "potencia"), ("Olho do Vento", "mobilidade"))),
    ("ladino", "Ladino", "battle", "oportunismo", "astúcia", "Usa posição, truques e ferramentas para criar vantagem.", "Ataque Oportuno", "Causa dano adicional contra alvo Exposto ou distraído.", {"speed": 3, "critical": 1}, ("adagas", "bestas", "ferramentas"), ("Adaga de Ferro", "Besta de Mão"), (("Truques", "controle"), ("Golpe Oportuno", "critico"), ("Saída Limpa", "furtividade"))),
    ("assassino", "Assassino", "battle", "explosão furtiva", "sombra", "Converte preparação e informação em uma janela letal.", "Sentença", "Marca um alvo; o primeiro ataque oculto recebe grande bônus.", {"attack": 2, "critical": 3}, ("adagas", "venenos", "furtividade"), ("Punhal Umbra",), (("Lâmina Oculta", "critico"), ("Toxicologia", "alquimia"), ("Desaparecer", "furtividade"))),
    ("monge", "Monge", "battle", "mobilidade e controle", "disciplina", "Luta sem depender de equipamento pesado e encadeia movimentos.", "Fluxo Interior", "Recupera disciplina ao alternar ataque, defesa e movimento.", {"speed": 3, "defense": 1}, ("desarmado", "cajados_comuns", "armadura_leve"), ("Bastão de Caminhante",), (("Formas", "ofensiva"), ("Corpo Sereno", "defesa"), ("Passo sem Peso", "mobilidade"))),
    ("mago", "Mago", "battle", "magia versátil", "mana", "Estuda padrões do Aether e prepara repertórios variados.", "Grimório Vivo", "Pode trocar uma magia preparada fora de combate.", {"mana_max": 6, "attack": 1}, ("cajados_arcanos", "grimorios", "armadura_arcana"), ("Cajado das Brasas",), (("Evocação", "arcano"), ("Abjuração", "defesa"), ("Metamagia", "eficiencia_mana"))),
    ("feiticeiro", "Feiticeiro", "battle", "magia espontânea", "mana", "Canaliza magia inata com grande intensidade e risco.", "Sobrecarga", "Amplifica um feitiço ao custo de instabilidade.", {"mana_max": 5, "critical": 2}, ("cajados_arcanos", "catalisadores"), ("Cajado Condutor Vazio",), (("Sangue Arcano", "arcano"), ("Sobrecarga", "potencia"), ("Controle Instintivo", "eficiencia_mana"))),
    ("elementalista", "Elementalista", "battle", "fraquezas elementais", "mana", "Alterna fogo, gelo, tempestade e terra conforme o alvo.", "Sintonização", "Troca o elemento dominante e revela resistências atingidas.", {"mana_max": 4, "attack": 2}, ("cajados_arcanos", "catalisadores"), ("Cajado da Geada Profunda",), (("Chama e Geada", "arcano"), ("Terra e Tempestade", "controle"), ("Convergência", "potencia"))),
    ("artifice_arcano", "Artífice Arcano", "battle", "artefatos", "carga", "Combina engenharia, catalisadores e artefatos instáveis.", "Calibrar Artefato", "Recupera carga e reduz instabilidade fora de perigo imediato.", {"defense": 1, "mana_max": 3}, ("catalisadores", "bestas", "ferramentas"), ("Besta de Mão", "Fragmento Inerte de Aether"), (("Engenharia Aetérica", "oficio"), ("Descarga", "arcano"), ("Contenção", "defesa"))),
    ("clerigo", "Clérigo", "battle", "cura e apoio", "fé", "Sustenta aliados, repele corrupção e negocia rendições.", "Prece de Estabilização", "Impede que um aliado caído piore até receber cuidado.", {"mana_max": 4, "defense": 1}, ("macas", "escudos", "simbolos_sagrados"), ("Maça de Ferro", "Símbolo de Peregrino"), (("Vida", "cura"), ("Proteção", "defesa"), ("Revelação", "conhecimento"))),
    ("paladino", "Paladino", "battle", "defesa sagrada", "convicção", "Une juramento, presença e golpes contra ameaças escolhidas.", "Desafio Solene", "Marca um inimigo e protege quem ele tentar atacar.", {"attack": 1, "defense": 2, "life_max": 2}, ("espadas", "escudos", "armadura_pesada"), ("Espada Longa de Aço", "Escudo Reforçado"), (("Juramento", "lideranca"), ("Luz Punitiva", "potencia"), ("Misericórdia", "cura"))),
    ("druida", "Druida", "battle", "natureza e transformação", "seiva", "Usa o bioma, formas animais e ciclos vivos.", "Forma Adaptativa", "Assume um aspecto breve adequado ao terreno atual.", {"mana_max": 3, "speed": 1}, ("cajados_comuns", "catalisadores_naturais"), ("Cajado das Raízes",), (("Formas Selvagens", "mobilidade"), ("Círculo Verde", "cura"), ("Ira do Bioma", "controle"))),
    ("xama", "Xamã", "battle", "espíritos e totens", "ressonância", "Negocia com ecos, planta totens e altera o campo.", "Totem de Vigília", "Cria uma zona que revela ocultos e fortalece vontade.", {"mana_max": 4, "defense": 1}, ("cajados_arcanos", "totens"), ("Cajado de Ressonum",), (("Totens", "controle"), ("Ancestrais", "invocacao"), ("Ressonância", "arcano"))),
    ("necromante", "Necromante", "battle", "dreno e servos", "essência", "Manipula restos, memória e custo vital sem negar consequências.", "Colher Eco", "Recupera essência quando uma criatura cai perto.", {"mana_max": 5, "life_max": -2}, ("cajados_arcanos", "rituais"), ("Cajado das Sombras Umbra",), (("Dreno", "cura"), ("Servos", "invocacao"), ("Mortificação", "controle"))),
    ("invocador", "Invocador", "battle", "aliados conjurados", "vínculo", "Divide ações e risco com entidades vinculadas.", "Manifestar Vínculo", "Chama um companheiro temporário com função escolhida.", {"mana_max": 5}, ("cajados_arcanos", "selos"), ("Cajado do Orbe Celeste",), (("Pactos", "invocacao"), ("Comando", "lideranca"), ("Portais", "arcano"))),
    ("bardo_guerra", "Bardo de Guerra", "battle", "apoio e influência", "inspiração", "Usa ritmo, história e presença para mudar moral e iniciativa.", "Compasso de Batalha", "Concede precisão a um aliado ou abala a moral inimiga.", {"speed": 1, "critical": 1}, ("espadas", "instrumentos", "armadura_leve"), ("Sabre de Arkanor", "Alaúde de Viagem"), (("Canções", "lideranca"), ("Sátira", "social"), ("Ritmo Marcial", "ofensiva"))),
    ("anciao", "Ancião", "battle", "sabedoria e previsão", "lucidez", "Vence pela leitura de padrões, preparo e intervenção precisa.", "Antever", "Uma vez por rodada, transforma uma falha crítica próxima em falha comum.", {"mana_max": 3, "defense": 1}, ("cajados_comuns", "rituais", "conhecimento"), ("Cajado de Carvalho",), (("Memória Longa", "conhecimento"), ("Presciência", "defesa"), ("Conselho", "lideranca"))),

    ("ferreiro", "Ferreiro", "profession", "forja", "ofício", "Forja lâminas, ferramentas e ferragens sob condições reais.", "Têmpera", "Repara metal e concede durabilidade temporária.", {"forca": 1}, ("forja", "martelos"), ("Martelo de Ferreiro",), (("Metalurgia", "oficio"), ("Têmpera", "defesa"), ("Lâminas", "potencia"))),
    ("armeiro", "Armeiro", "profession", "armaduras", "ofício", "Projeta proteção sem ignorar peso, mobilidade e manutenção.", "Ajuste de Placas", "Melhora a mitigação de uma armadura até o próximo reparo.", {"defesa": 1}, ("armaduras", "escudos"), ("Kit de Reparo",), (("Placas", "defesa"), ("Escudos", "controle"), ("Mobilidade", "mobilidade"))),
    ("alquimista", "Alquimista", "profession", "preparados", "reagentes", "Cria poções, bombas, solventes e antídotos.", "Análise de Reagente", "Identifica risco e propriedade de uma amostra.", {"percepcao": 1}, ("pocoes", "bombas"), ("Estojo Alquímico",), (("Poções", "alquimia"), ("Bombas", "potencia"), ("Antídotos", "cura"))),
    ("herbalista", "Herbalista", "profession", "flora", "amostras", "Reconhece, cultiva e coleta flora sem destruir a fonte.", "Coleta Sustentável", "Colhe uma segunda amostra quando o ambiente permite.", {"sobrevivencia": 1}, ("flora", "coleta"), ("Foice de Herbalista",), (("Identificação", "conhecimento"), ("Cultivo", "coleta"), ("Preparos", "alquimia"))),
    ("curandeiro", "Curandeiro", "profession", "medicina", "suprimentos", "Trata trauma, doença, veneno e recuperação prolongada.", "Triagem", "Revela a lesão mais urgente e estabiliza o paciente.", {"vontade": 1}, ("medicina", "ervas"), ("Bolsa de Curandeiro",), (("Trauma", "cura"), ("Doenças", "conhecimento"), ("Recuperação", "sobrevivencia"))),
    ("cozinheiro", "Cozinheiro", "profession", "alimentação", "ingredientes", "Transforma recursos locais em comida segura e benefícios duradouros.", "Refeição de Marcha", "Reduz fome e fadiga do grupo com provisões simples.", {"sobrevivencia": 1}, ("cozinha", "provisoes"), ("Panela de Campanha",), (("Nutrição", "sobrevivencia"), ("Sabores", "social"), ("Conservação", "oficio"))),
    ("cacador_coletor", "Caçador-Coletor", "profession", "subsistência", "recursos", "Obtém alimento e materiais respeitando risco e território.", "Aproveitamento", "Extrai material adicional de caça ou coleta bem-sucedida.", {"sobrevivencia": 1}, ("caca", "coleta"), ("Faca de Osso",), (("Caça", "sobrevivencia"), ("Coleta", "coleta"), ("Rastros", "exploracao"))),
    ("pescador", "Pescador", "profession", "águas", "iscas", "Lê corrente, gelo, maré e comportamento aquático.", "Leitura da Água", "Prevê uma mudança perigosa na água próxima.", {"percepcao": 1}, ("pesca", "barcos"), ("Kit de Pesca",), (("Redes", "coleta"), ("Navegação", "exploracao"), ("Iscas", "conhecimento"))),
    ("minerador", "Minerador", "profession", "mineração", "vigor", "Encontra veios, sustenta túneis e extrai sem provocar colapso.", "Ouvido da Rocha", "Detecta vazio, instabilidade e veio próximo.", {"forca": 1}, ("mineracao", "picaretas"), ("Picareta de Mineração",), (("Prospecção", "exploracao"), ("Extração", "coleta"), ("Segurança", "defesa"))),
    ("lenhador", "Lenhador", "profession", "madeira", "vigor", "Abate, maneja e prepara madeira para campo e construção.", "Corte Direcionado", "Derruba ou remove madeira sem atingir a área errada.", {"forca": 1}, ("machados", "madeira"), ("Machadinha de Lenhador",), (("Manejo", "coleta"), ("Carpintaria", "oficio"), ("Trilhas", "exploracao"))),
    ("engenheiro", "Engenheiro", "profession", "mecanismos", "peças", "Projeta máquinas, armadilhas, pontes e reparos de campo.", "Improviso Estrutural", "Cria uma solução temporária com materiais inadequados.", {"percepcao": 1}, ("engenharia", "armadilhas"), ("Estojo de Ferramentas",), (("Mecanismos", "oficio"), ("Fortificações", "defesa"), ("Autômatos", "invocacao"))),
    ("encantador", "Encantador", "profession", "encantamento", "catalisadores", "Inscreve efeitos estáveis em equipamento e artefatos.", "Inscrição Menor", "Aplica um efeito limitado até a próxima manutenção.", {"vontade": 1}, ("runas", "catalisadores"), ("Cinzel Rúnico",), (("Runas", "arcano"), ("Vínculos", "oficio"), ("Estabilização", "eficiencia_mana"))),
    ("cartografo", "Cartógrafo", "profession", "mapas", "referências", "Mede distância, registra descobertas e conecta rotas reais.", "Triangulação", "Reduz incerteza de posição usando três referências.", {"percepcao": 1}, ("mapas", "navegacao"), ("Estojo de Cartografia",), (("Levantamento", "exploracao"), ("Rotas", "sobrevivencia"), ("Atlas", "conhecimento"))),
    ("mercador", "Mercador", "profession", "economia", "capital", "Lê oferta, risco, reputação e logística entre regiões.", "Avaliação", "Revela qualidade, procura local e faixa justa de preço.", {"social": 1}, ("comercio", "logistica"), ("Balança Portátil",), (("Negociação", "comercio"), ("Caravanas", "lideranca"), ("Mercados", "conhecimento"))),
    ("diplomata", "Diplomata", "profession", "relações", "influência", "Constrói acordos, mede tensões e preserva saídas não violentas.", "Ouvir Interesses", "Revela uma necessidade e uma linha vermelha do interlocutor.", {"social": 2}, ("etiqueta", "idiomas"), ("Selo de Mensageiro",), (("Tratados", "social"), ("Mediação", "lideranca"), ("Culturas", "conhecimento"))),
    ("escriba", "Escriba", "profession", "registros", "tinta", "Preserva conhecimento, decifra línguas e cria cópias confiáveis.", "Memória Escrita", "Registra uma pista sem perda de certeza ao longo do tempo.", {"percepcao": 1}, ("escrita", "idiomas", "arquivos"), ("Estojo de Escrita",), (("Línguas", "conhecimento"), ("Arquivos", "exploracao"), ("Selos", "oficio"))),
)


def _build_careers() -> dict[str, CareerDefinition]:
    careers: dict[str, CareerDefinition] = {}
    for spec in CAREER_SPECS:
        (
            slug, name, category, role, resource, description, innate_name,
            innate_description, modifiers, proficiencies, gear, branch_specs,
        ) = spec
        branches = {
            branch_name: _branch_nodes(slug, name, branch_name, mechanic)
            for branch_name, mechanic in branch_specs
        }
        careers[slug] = CareerDefinition(
            slug=slug, name=name, category=category, role=role, resource=resource,
            description=description, branches=branches, innate_name=innate_name,
            innate_description=innate_description, stat_modifiers=dict(modifiers),
            proficiencies=tuple(proficiencies), starting_gear=tuple(gear),
        )
    return careers


CAREERS = _build_careers()
BATTLE_CLASSES = {key: value for key, value in CAREERS.items() if value.category == "battle"}
PROFESSIONS = {key: value for key, value in CAREERS.items() if value.category == "profession"}


class SkillTreeService:
    """Compra, consulta e soma os efeitos das árvores sem depender da interface."""

    @staticmethod
    def career(slug: str) -> CareerDefinition:
        try:
            return CAREERS[slug]
        except KeyError as exc:
            raise ValueError(f"Carreira desconhecida: {slug}") from exc

    @staticmethod
    def node(slug: str) -> SkillNode:
        career_slug = slug.split(".", 1)[0]
        career = SkillTreeService.career(career_slug)
        found = next((node for node in career.nodes if node.slug == slug), None)
        if found is None:
            raise ValueError(f"Habilidade desconhecida: {slug}")
        return found

    @staticmethod
    def selected_careers(session: Any) -> tuple[CareerDefinition, ...]:
        slugs = (getattr(session, "battle_class_slug", "guerreiro"), getattr(session, "profession_slug", "cacador_coletor"))
        return tuple(CAREERS[slug] for slug in slugs if slug in CAREERS)

    @staticmethod
    def available_nodes(session: Any, career_slug: str) -> list[tuple[SkillNode, str]]:
        career = SkillTreeService.career(career_slug)
        selected = {item.slug for item in SkillTreeService.selected_careers(session)}
        unlocked = set(getattr(session, "unlocked_skills", ()) or ())
        points = int(getattr(session, "skill_points", 0))
        result = []
        for node in career.nodes:
            if career_slug not in selected:
                state = "carreira_não_selecionada"
            elif node.slug in unlocked:
                state = "aprendida"
            elif not set(node.prerequisites).issubset(unlocked):
                state = "requer_habilidade_anterior"
            elif points < node.cost:
                state = "pontos_insuficientes"
            else:
                state = "disponível"
            result.append((node, state))
        return result

    @staticmethod
    def purchase(session: Any, node_slug: str) -> SkillNode:
        node = SkillTreeService.node(node_slug)
        career_slug = node_slug.split(".", 1)[0]
        states = dict((entry.slug, state) for entry, state in SkillTreeService.available_nodes(session, career_slug))
        if states.get(node_slug) != "disponível":
            raise ValueError(f"Habilidade indisponível: {states.get(node_slug, 'desconhecida')}")
        session.skill_points = int(getattr(session, "skill_points", 0)) - node.cost
        unlocked = list(getattr(session, "unlocked_skills", ()) or ())
        unlocked.append(node.slug)
        session.unlocked_skills = unlocked
        return node

    @staticmethod
    def effects(session: Any) -> dict[str, int]:
        totals: dict[str, int] = {}
        for slug in set(getattr(session, "unlocked_skills", ()) or ()):
            try:
                node = SkillTreeService.node(slug)
            except ValueError:
                continue
            for effect in node.effects:
                if effect.get("type") in {"unlock_action", "capstone"}:
                    continue
                key = str(effect.get("type"))
                totals[key] = totals.get(key, 0) + int(effect.get("value") or 0)
        return totals

    @staticmethod
    def unlocked_actions(session: Any) -> set[str]:
        actions: set[str] = set()
        for slug in set(getattr(session, "unlocked_skills", ()) or ()):
            try:
                node = SkillTreeService.node(slug)
            except ValueError:
                continue
            actions.update(str(effect["value"]) for effect in node.effects if effect.get("type") == "unlock_action")
        return actions

    @staticmethod
    def grant_xp(session: Any, amount: int, *, profession: bool = False) -> int:
        field = "profession_xp" if profession else "class_xp"
        level_field = "profession_level" if profession else "class_level"
        current_xp = int(getattr(session, field, 0)) + max(0, int(amount))
        level = int(getattr(session, level_field, 1))
        gained = 0
        while level < 50 and current_xp >= 80 + level * 40:
            current_xp -= 80 + level * 40
            level += 1
            gained += 1
        setattr(session, field, current_xp)
        setattr(session, level_field, level)
        if gained:
            session.skill_points = int(getattr(session, "skill_points", 0)) + gained
            session.level = max(int(getattr(session, "level", 1)), level)
        return gained


def apply_starting_careers(session: Any, battle_slug: str, profession_slug: str) -> None:
    battle = BATTLE_CLASSES.get(battle_slug) or BATTLE_CLASSES["guerreiro"]
    profession = PROFESSIONS.get(profession_slug) or PROFESSIONS["cacador_coletor"]
    session.battle_class_slug = battle.slug
    session.battle_class_name = battle.name
    session.profession_slug = profession.slug
    session.profession_name = profession.name
    session.skill_points = max(3, int(getattr(session, "skill_points", 0)))
    for career in (battle, profession):
        for key, value in career.stat_modifiers.items():
            if key in {"forca", "defesa", "percepcao", "sobrevivencia", "social", "vontade"}:
                session.attributes[key] = int(session.attributes.get(key, 0)) + int(value)
                continue
            if key == "critical":
                session.critical += float(value) / 100.0
                continue
            if hasattr(session, key):
                setattr(session, key, int(getattr(session, key)) + int(value))
    session.life = session.life_max
    session.mana = session.mana_max
    for item in (*battle.starting_gear, *profession.starting_gear):
        if item and item not in session.inventory:
            session.inventory.append(item)
    session.equipment.setdefault("weapon", battle.starting_gear[0] if battle.starting_gear else "Ataque Desarmado")
    if battle.slug == "artifice_arcano":
        if "Fragmento Inerte de Aether" not in session.equipped_artifacts:
            session.equipped_artifacts.append("Fragmento Inerte de Aether")
        session.artifact_state.update({"charge": 3, "instability": 0})


def iter_mysql_rows() -> Iterable[tuple]:
    for career in CAREERS.values():
        yield (
            career.slug, career.name, career.category, career.role, career.resource,
            career.description, career.innate_name, career.innate_description,
        )


def iter_skill_mysql_rows() -> Iterable[tuple]:
    import json
    for career in CAREERS.values():
        for node in career.nodes:
            yield (
                node.slug, career.slug, node.branch, node.name, node.description,
                node.tier, node.cost, json.dumps(node.prerequisites, ensure_ascii=False),
                json.dumps(node.effects, ensure_ascii=False),
            )
