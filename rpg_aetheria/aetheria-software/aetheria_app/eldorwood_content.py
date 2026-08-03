from __future__ import annotations

"""Conteúdo regional de Eldorwood usado pelo explorador persistente.

As coordenadas representam quilômetros dentro de um recorte continental. A região é
grande o bastante para que um nascimento perto da fronteira alcance Frostreach em
dias, enquanto um nascimento profundo exija semanas ou meses de marcha.
"""

from typing import Any


ELDORWOOD_BIOMES: dict[str, dict[str, Any]] = {
    "floresta_densa_antiga": {
        "name": "Floresta Densa Antiga",
        "region": "eldorwood",
        "speed_kmh": 1.7,
        "temperature_delta": -1,
        "ambience": [
            "O dossel fecha o céu em camadas; gotas antigas caem muito depois de a chuva terminar.",
            "Raízes largas erguem o solo como costelas, obrigando cada passo a escolher um apoio diferente.",
            "Musgo-Luminoso desenha manchas verde-azuladas em troncos altos demais para serem medidos de baixo.",
            "O cheiro de casca molhada, fungos e terra fria muda sempre que o vento encontra uma abertura.",
            "Galhos rangem em sequências longas. Algumas parecem resposta; outras são apenas madeira sob tensão.",
            "A penumbra conserva rastros: cascos, folhas viradas, pelos presos e marcas de ferramentas antigas.",
        ],
        "weather": [
            "neblina entre os troncos", "chuva fina sob o dossel", "ar frio e imóvel",
            "vento alto nas copas", "garoa de folhas largas", "claridade verde filtrada",
        ],
        "routes": {
            "norte": [
                "Seguir raízes que sobem para o norte", "Acompanhar marcas de cervídeo ao norte",
                "Procurar uma abertura no dossel ao norte",
            ],
            "sul": [
                "Descer com a água escura para o sul", "Seguir terreno mais úmido ao sul",
                "Acompanhar fungos luminosos rumo ao sul",
            ],
            "leste": [
                "Contornar as Árvores-Anciãs para leste", "Seguir o canto grave das corujas a leste",
                "Avançar entre samambaias para leste",
            ],
            "oeste": [
                "Seguir uma antiga trilha Sylvani a oeste", "Buscar terreno firme a oeste",
                "Acompanhar marcas de carroça apagadas a oeste",
            ],
        },
        "flora": [
            ("Árvore-Anciã de Eldor", "um tronco de largura monumental sustenta jardins inteiros sobre os galhos", False, False),
            ("Musgo-Luminoso", "colônias verde-azuladas guardam umidade e luz sob as raízes", False, False),
            ("Samambaia-Espiral", "folhas repetem o mesmo desenho em escalas menores", False, False),
            ("Erva-da-Neblina", "folhas quase transparentes crescem num tronco caído", False, False),
            ("Cogumelo-Sombra", "chapéus semelhantes escondem variedades nutritivas e tóxicas", True, True),
            ("Lírio-da-Penumbra", "uma flor branca abre onde quase nenhuma luz alcança o solo", False, False),
            ("Raiz-de-Vida", "uma raiz superficial pulsa lentamente depois da chuva", False, False),
        ],
        "fauna": [
            ("Cervídeo-de-Eldor", "pacific", 1, "chifres semelhantes a galhos passam silenciosos entre samambaias"),
            ("Lobo-Sombrio", "predator", 3, "dois olhos acompanham sua posição enquanto um segundo animal tenta contornar o vento"),
            ("Coruja-das-Brumas", "neutral", 1, "uma ave de olhos amarelos espera você olhar antes de mudar de galho"),
            ("Raposa-de-Musgo", "neutral", 1, "pelagem verde-cinzenta some sempre que o animal para"),
            ("Aranha-Teia-Verde", "territorial", 2, "fios quase invisíveis fecham a passagem entre dois troncos"),
            ("Sapo-de-Folha", "neutral", 1, "uma folha respira e revela olhos protegidos por membranas"),
            ("Espírito-das-Árvores", "mystic", 4, "névoa, folhas e luz formam uma presença que observa sem rosto"),
            ("Cervo-Luminoso", "mystic", 2, "pontos de luz percorrem a galhada sem iluminar o chão"),
            ("Tigre-de-Sombra", "predator", 5, "um felino grande utiliza a penumbra como se ela fosse cobertura sólida"),
        ],
        "landmarks": [
            ("Círculo das Árvores-Anciãs", "Troncos colossais cercam uma depressão onde o som chega abafado."),
            ("Clareira da Penumbra", "Lírios brancos ocupam uma abertura que nunca recebe sol direto."),
            ("Santuário das Duas Folhas", "Uma construção Sylvani viva une dois troncos sem pregos ou cortes."),
            ("Ponte Engolida", "Pedras de uma estrada medieval desaparecem sob raízes mais recentes."),
            ("Arquivo de Casca", "Placas finas cobertas de escrita vegetal pendem protegidas da chuva."),
            ("Poço sem Reflexo", "Água escura devolve o dossel, mas não mostra quem se inclina sobre ela."),
        ],
        "hazards": [
            ("Queda de Galho Ancião", "A madeira estala acima; o objeto que cai tem o tamanho de uma torre pequena."),
            ("Campo de Esporos", "Uma nuvem dourada sai de fungos esmagados por algo que passou antes."),
            ("Solo de Raiz Oca", "A camada de folhas esconde uma rede vazia incapaz de sustentar peso."),
            ("Teia Verde", "Fios paralisantes atravessam o caminho na altura do peito."),
        ],
    },
    "pantanos_rios": {
        "name": "Pântanos e Rios",
        "region": "eldorwood",
        "speed_kmh": 1.1,
        "temperature_delta": 0,
        "ambience": [
            "A água marrom reflete apenas a neblina; raízes submersas transformam cada linha reta em labirinto.",
            "Ilhas de musgo giram devagar em torno de vórtices que não acompanham o vento.",
            "Insetos luminosos acendem e apagam em ritmos diferentes, escondendo distâncias reais.",
            "O chão alterna lama, água e turfa flutuante sem mudança visível de cor.",
            "Garças imóveis vigiam canais onde bolhas grandes demais sobem entre os juncos.",
            "Chuva, folhas e animais pequenos criam tantos círculos na água que um movimento intencional quase se perde.",
        ],
        "weather": [
            "neblina baixa", "chuva morna e contínua", "vento de rio", "calor úmido",
            "garoa fria", "céu cinza refletido na água",
        ],
        "routes": {
            "norte": [
                "Seguir o canal de água clara ao norte", "Acompanhar raízes mais altas para o norte",
                "Avançar contra a corrente ao norte",
            ],
            "sul": [
                "Descer o rio para o sul", "Cruzar ilhas de turfa rumo ao sul",
                "Seguir garças em direção ao sul",
            ],
            "leste": [
                "Contornar o mangue fluvial para leste", "Acompanhar fogo-fátuos a distância para leste",
                "Procurar uma margem firme a leste",
            ],
            "oeste": [
                "Seguir juncos cortados a oeste", "Atravessar um canal raso para oeste",
                "Acompanhar sinais de barco rumo a oeste",
            ],
        },
        "flora": [
            ("Musgo-de-Água", "tapetes flutuantes absorvem chuva e escondem a profundidade", False, False),
            ("Lírio-d'Água de Eldor", "flores grandes guardam gotas luminosas entre as pétalas", False, False),
            ("Raiz-Retorcida", "raízes aéreas formam um corredor sobre água lodosa", False, False),
            ("Alga-Pura", "filamentos claros indicam água rica em Aquanium", True, False),
            ("Samambaia-Pântano", "folhas longas dobram sem quebrar durante a chuva", False, False),
            ("Flor-de-Fogo-Fátuo", "pétalas iridescentes sustentam um enxame luminoso", False, False),
            ("Junco-Espiral", "hastes crescem em anéis concêntricos junto à margem", False, False),
        ],
        "fauna": [
            ("Crocodilo-de-Pântano", "predator", 5, "um tronco escuro muda de posição contra a corrente"),
            ("Garça-das-Brumas", "neutral", 1, "uma ave alta mede a água antes de lançar o bico"),
            ("Peixe-Luminoso", "pacific", 0, "luzes azuis atravessam a água sob folhas largas"),
            ("Sapo-Gigante de Eldor", "territorial", 3, "um anfíbio do tamanho de um cão infla o corpo sobre uma ilha"),
            ("Serpente-d'Água", "predator", 3, "uma linha rápida corta a superfície e desaparece sob raízes"),
            ("Inseto-Fogo-Fátuo", "mystic", 2, "o enxame desenha círculos que parecem indicar uma direção"),
            ("Lontra-de-Neblina", "pacific", 1, "uma família organiza pedras e conchas diante da toca"),
            ("Aquaphant", "territorial", 4, "um herbívoro enorme abre caminho carregando plantas nas costas"),
            ("Guardião das Águas", "legendary", 5, "a corrente sobe em forma viva ao redor de um núcleo luminoso"),
        ],
        "landmarks": [
            ("Ilhas do Fogo-Fátuo", "Turfa, flores e raízes formam ilhas que trocam lentamente de posição."),
            ("Fonte de Aquanium", "Água cristalina ocupa um círculo perfeito no meio do pântano."),
            ("Labirinto de Raízes", "Corredores submersos cruzam-se em níveis diferentes."),
            ("Ponte dos Barqueiros", "Uma ponte medieval sobre pilares móveis acompanha a cheia do rio."),
            ("Templo da Confluência", "Aquari e Ninfari mantêm plataformas sobre três rios que se encontram."),
            ("Torre Afundada", "O último andar de uma torre de pedra emerge da água escura."),
        ],
        "hazards": [
            ("Turfa Instável", "A ilha flutuante separa-se da margem quando recebe seu peso."),
            ("Vórtice de Circulium", "Folhas giram sobre uma corrente que puxa para baixo."),
            ("Água Contaminada", "Peixes evitam um canal de odor doce e cor uniforme."),
            ("Enxame Defensivo", "Fogo-fátuos concentram luz e calor ao redor de um ninho."),
        ],
    },
    "colinas_arborizadas": {
        "name": "Colinas Arborizadas",
        "region": "eldorwood",
        "speed_kmh": 2.6,
        "temperature_delta": -1,
        "ambience": [
            "Bosques separados revelam um horizonte raro em Eldorwood; torres e fumaças podem ser vistas a muitos quilômetros.",
            "Grama alta cobre encostas suaves, interrompida por carvalhos e muros de pedra cobertos de musgo.",
            "Estradas medievais acompanham as elevações, evitando vales onde a neblina permanece até a tarde.",
            "Fazendas aparecem em clareiras amplas, mas quilômetros de colina vazia separam uma propriedade da outra.",
            "Formações de Patterium repetem ângulos de muralhas construídas muito depois delas.",
            "O vento traz sinos de rebanho, rodas de carroça ou apenas o som das folhas, dependendo da direção.",
        ],
        "weather": [
            "vento frio de colina", "céu aberto entre nuvens", "chuva passageira",
            "neblina nos vales", "sol pálido", "garoa levada pelo vento",
        ],
        "routes": {
            "norte": [
                "Seguir a estrada de cumeeira ao norte", "Acompanhar muros antigos rumo ao norte",
                "Avançar por clareiras em direção ao norte",
            ],
            "sul": [
                "Descer pelos campos para o sul", "Seguir carroças em direção ao sul",
                "Acompanhar um riacho de colina ao sul",
            ],
            "leste": [
                "Cruzar bosques dispersos a leste", "Seguir torres distantes para leste",
                "Acompanhar a estrada comercial a leste",
            ],
            "oeste": [
                "Subir a encosta arborizada a oeste", "Seguir cercas de pedra para oeste",
                "Procurar passagem entre fazendas a oeste",
            ],
        },
        "flora": [
            ("Carvalho-de-Colina", "uma copa larga protege o cruzamento de duas trilhas", False, False),
            ("Arbusto-de-Fruto-Vermelho", "bagas maduras atraem aves e pequenos mamíferos", True, False),
            ("Grama-Alta de Clareira", "ondas na vegetação denunciam o vento e movimentos escondidos", True, False),
            ("Flor-de-Pedra", "pétalas rígidas ocupam uma fenda de Patterium", False, False),
            ("Musgo-de-Morro", "círculos verdes cobrem pedras de uma muralha abandonada", False, False),
            ("Erva-de-Vento", "hastes flexíveis liberam aroma calmante quando dobradas", False, False),
        ],
        "fauna": [
            ("Cervo-das-Colinas", "pacific", 1, "um rebanho observa a estrada antes de cruzar"),
            ("Javali-de-Eldor", "territorial", 3, "um adulto protege filhotes escondidos na grama"),
            ("Águia-de-Colina", "predator", 2, "uma ave desce sobre alguma presa fora de sua visão"),
            ("Raposa-Vermelha", "neutral", 1, "uma caçadora solitária acompanha muros de pedra"),
            ("Lebre-de-Clareira", "pacific", 0, "orelhas aparecem acima da grama e somem juntas"),
            ("Falcão-de-Patterium", "neutral", 2, "o voo permanece estável mesmo sob vento lateral"),
            ("Texugo-das-Colinas", "territorial", 2, "terra recém-removida marca uma toca extensa"),
            ("Urso-das-Colinas", "predator", 4, "um corpo pesado procura frutos perto da estrada"),
            ("Cervo-Astral", "legendary", 5, "uma galhada translúcida reflete constelações invisíveis durante o dia"),
        ],
        "landmarks": [
            ("Círculo de Patterium", "Pedras simétricas cercam uma depressão coberta de Flor-de-Pedra."),
            ("Torre do Caminho Velho", "Uma torre medieval abandonada ainda domina três vales."),
            ("Pomar sem Dono", "Árvores frutíferas crescem dentro de muros rompidos por raízes."),
            ("Campo dos Sete Menires", "Pedras antigas marcam direções que não correspondem às estradas."),
            ("Mosteiro da Chuva", "Telhados íngremes recolhem água para viajantes e aldeias."),
            ("Marco da Fronteira Antiga", "Brasões apagados indicam que o limite político mudou muitas vezes."),
        ],
        "hazards": [
            ("Deslizamento de Encosta", "Terra saturada começa a mover árvores e pedras para o vale."),
            ("Ponte de Madeira Podre", "Tábuas escondem fungos que consumiram o interior das vigas."),
            ("Ninho Territorial", "Ovos grandes ocupam uma formação rochosa junto à trilha."),
            ("Caçadores em Disputa", "Armadilhas de dois grupos sobrepõem-se sem qualquer sinal claro de posse."),
        ],
    },
}


ELDORWOOD_SETTLEMENTS: list[dict[str, Any]] = [
    {
        "id": "sylvarin", "name": "Sylvarin", "type": "capital florestal", "population": 180_000,
        "x": 0.0, "y": 1780.0, "radius_km": 34.0, "scene_id": "r2_sylvarin_portoes",
        "description": "pontes, torres de madeira viva, muralhas de pedra úmida e bairros inteiros ocupam árvores e solo em níveis diferentes",
    },
    {
        "id": "brumavale", "name": "Brumavale", "type": "grande cidade fluvial", "population": 96_000,
        "x": 920.0, "y": 760.0, "radius_km": 28.0, "scene_id": "r2_brumavale_cais",
        "description": "muralhas cinzentas, telhados íngremes, canais, rodas d'água e mercados cobertos acompanham as duas margens",
    },
    {
        "id": "lethariel", "name": "Lethariel", "type": "cidade Sylvani do dossel", "population": 74_000,
        "x": -1120.0, "y": 2140.0, "radius_km": 25.0, "scene_id": "r2_lethariel_passarela",
        "description": "plataformas vivas, jardins suspensos e santuários de memória ligam Árvores-Anciãs sem tocar o chão",
    },
    {
        "id": "ponte_circulium", "name": "Ponte de Circulium", "type": "cidade-ponte", "population": 21_000,
        "x": 610.0, "y": 1240.0, "radius_km": 16.0, "scene_id": "r2_ponte_circulium",
        "description": "arcos móveis, pedágios, hospedarias e oficinas controlam a travessia de um rio largo",
    },
    {
        "id": "vale_eldor", "name": "Vale Eldor", "type": "vila murada", "population": 8_400,
        "x": 150.0, "y": 1430.0, "radius_km": 12.0, "scene_id": "r2_vale_eldor_praca",
        "description": "casas de madeira escura cercam uma Árvore-Anciã e um pequeno mercado protegido por paliçada",
    },
    {
        "id": "brejo_lume", "name": "Brejo-Lume", "type": "vila de plataformas", "population": 2_200,
        "x": 1510.0, "y": -880.0, "radius_km": 9.0, "scene_id": "r2_brejo_lume_ancoradouro",
        "description": "plataformas, barcos rasos e jardins flutuantes formam ruas que mudam com o nível da água",
    },
    {
        "id": "folha_baixa", "name": "Folha Baixa", "type": "aldeia de coletores", "population": 980,
        "x": -390.0, "y": 810.0, "radius_km": 7.0, "scene_id": "r2_folha_baixa_entrada",
        "description": "secadores de ervas e casas entre raízes abrigam boticários, lenhadores e famílias Sylvani",
    },
    {
        "id": "miralva", "name": "Miralva", "type": "cidade de colina", "population": 13_500,
        "x": -1430.0, "y": 2620.0, "radius_km": 15.0, "scene_id": "r2_miralva_portao",
        "description": "muralhas baixas, moinhos e pomares cercam um castelo de pedra clara sobre a colina",
    },
    {
        "id": "passagem_cervo", "name": "Passagem do Cervo", "type": "aldeia de estrada", "population": 690,
        "x": -710.0, "y": 2360.0, "radius_km": 6.0, "scene_id": "r2_passagem_cervo",
        "description": "estábulos, uma estalagem e um posto de vigia marcam a rota mais segura entre bosques",
    },
    {
        "id": "raiz_serena", "name": "Raiz Serena", "type": "comunidade Sylvani", "population": 360,
        "x": 430.0, "y": 2020.0, "radius_km": 5.0, "scene_id": "r2_raiz_serena",
        "description": "habitações discretas cercam jardins medicinais e um arquivo vivo de casca e seiva",
    },
    {
        "id": "portao_nevoa", "name": "Portão da Névoa", "type": "posto de fronteira", "population": 520,
        "x": 180.0, "y": 2920.0, "radius_km": 8.0, "scene_id": "r2_portao_nevoa",
        "description": "uma fortificação de pedra e madeira controla a última estrada antes das terras frias de Frostreach",
    },
]


ELDORWOOD_NPCS: list[dict[str, Any]] = [
    {
        "id": "sael_ithyr", "name": "Sael Ithyr", "race": "Sylvani", "role": "guardião de memórias",
        "home": "lethariel", "faction": "conselhos_do_dossel", "x": -1080.0, "y": 2100.0,
        "description": "um Sylvani de fala precisa interrompe a coleta para escutar uma raiz antes de responder",
        "values": ["autonomia", "memória", "cuidado"], "red_lines": ["queimar árvore viva", "forçar assimilação"],
    },
    {
        "id": "maelis_venn", "name": "Maelis Venn", "race": "Umbrari", "role": "boticária e informante",
        "home": "folha_baixa", "faction": "arquivo_da_lanterna", "x": -410.0, "y": 830.0,
        "description": "uma Umbrari separa folhas medicinais e venenosas em caixas visualmente idênticas",
        "values": ["conhecimento", "discrição", "sobrevivência"], "red_lines": ["expor fonte vulnerável", "desperdiçar antídoto"],
    },
    {
        "id": "mara_avel", "name": "Mara Avel", "race": "Humana", "role": "curandeira",
        "home": "vale_eldor", "faction": "boticarios_folha_velada", "x": 150.0, "y": 1430.0,
        "description": "uma humana de mangas manchadas por ervas avalia sua respiração antes de perguntar seu nome",
        "values": ["cuidado", "honestidade", "aprendizado"], "red_lines": ["vender remédio falso", "abandonar doente"],
    },
    {
        "id": "orun_duas_margens", "name": "Orun das Duas Margens", "race": "Aquari", "role": "diplomata fluvial",
        "home": "brumavale", "faction": "coro_de_navegadores", "x": 900.0, "y": 780.0,
        "description": "um Aquari compara o movimento dos barcos antes de decidir de qual margem falar",
        "values": ["fluxo", "reciprocidade", "acordo"], "red_lines": ["envenenar rio", "aprisionar navegante"],
    },
    {
        "id": "tili_sete_sinos", "name": "Tili Sete-Sinos", "race": "Luminari", "role": "mensageira",
        "home": "sylvarin", "faction": "estradas_livres", "x": 30.0, "y": 1760.0,
        "description": "uma Luminari carrega sinos abafados e mede correntes de ar entre as árvores",
        "values": ["liberdade", "curiosidade", "palavra dada"], "red_lines": ["reter correspondência", "enjaular ser alado"],
    },
    {
        "id": "brohm_pedra_mansa", "name": "Brohm Pedra-Mansa", "race": "Ferrari", "role": "mestre de pontes",
        "home": "ponte_circulium", "faction": "mestres_de_ponte", "x": 620.0, "y": 1240.0,
        "description": "um Ferrari largo e grisalho testa pilares pelo som com os nós dos dedos",
        "values": ["obra segura", "responsabilidade", "paciência"], "red_lines": ["sabotar ponte ocupada", "falsificar inspeção"],
    },
    {
        "id": "ysra_miralva", "name": "Ysra de Miralva", "race": "Humana", "role": "capitã da guarda",
        "home": "miralva", "faction": "guarda_de_miralva", "x": -1420.0, "y": 2600.0,
        "description": "uma capitã humana observa botas, mãos e direção de chegada antes de oferecer saudação",
        "values": ["ordem", "proteção", "prova"], "red_lines": ["ferir civil", "subornar guarda"],
    },
    {
        "id": "velen_raiz_clara", "name": "Velen Raiz-Clara", "race": "Sylvani", "role": "conselheiro urbano",
        "home": "sylvarin", "faction": "conselhos_do_dossel", "x": 0.0, "y": 1800.0,
        "description": "um conselheiro Sylvani ouve assessores de três raças enquanto alimenta pássaros no parapeito",
        "values": ["equilíbrio", "continuidade", "consenso"], "red_lines": ["incêndio", "decisão secreta sobre a floresta"],
    },
    {
        "id": "zori_trinca_folha", "name": "Zori Trinca-Folha", "race": "Ziraki", "role": "mecânica de rodas d'água",
        "home": "brumavale", "faction": "oficios_livres", "x": 940.0, "y": 750.0,
        "description": "uma Ziraki pendurada numa roda parada pede uma ferramenta antes de perguntar quem você é",
        "values": ["invenção", "troca justa", "humor"], "red_lines": ["roubar projeto de aprendiz", "culpar trabalhador"],
    },
    {
        "id": "rheva_mare_baixa", "name": "Rheva Maré-Baixa", "race": "Ninfari", "role": "guardiã de fonte",
        "home": "brejo_lume", "faction": "confluencia", "x": 1490.0, "y": -850.0,
        "description": "uma Ninfari mantém metade do corpo na água enquanto examina a cor das algas",
        "values": ["água", "comunidade", "verdade"], "red_lines": ["contaminar fonte", "vender água sagrada"],
    },
    {
        "id": "garran_casco_cinza", "name": "Garran Casco-Cinza", "race": "Kragari", "role": "caravaneiro",
        "home": "passagem_cervo", "faction": "estradas_livres", "x": -680.0, "y": 2340.0,
        "description": "um Kragari ajusta a carga de uma mula ferida com mais delicadeza do que sua voz sugere",
        "values": ["dever", "franqueza", "proteção"], "red_lines": ["abandonar animal", "quebrar contrato"],
    },
    {
        "id": "essen_luz_de_chuva", "name": "Essen Luz-de-Chuva", "race": "Ethari", "role": "astrônoma",
        "home": "miralva", "faction": "observatorio_de_miralva", "x": -1450.0, "y": 2650.0,
        "description": "uma Ethari translúcida compara gotas numa placa escura como se fossem constelações",
        "values": ["evidência", "harmonia", "partilha"], "red_lines": ["destruir registro", "fabricar presságio"],
    },
    {
        "id": "kora_solo_quieto", "name": "Kora Solo-Quieto", "race": "Voraki", "role": "agrimensora",
        "home": "portao_nevoa", "faction": "cartografos_da_aurora", "x": 160.0, "y": 2900.0,
        "description": "uma Voraki toca a estrada e descreve carroças que passaram horas antes",
        "values": ["território", "precisão", "memória"], "red_lines": ["apagar marco", "minerar sem medir"],
    },
    {
        "id": "aelar_duas_copas", "name": "Aelar Duas-Copas", "race": "Drakari", "role": "cavaleiro do conselho",
        "home": "lethariel", "faction": "guardioes_dos_seis_selos", "x": -1100.0, "y": 2170.0,
        "description": "um Drakari de escamas bronze mantém a lança baixa e a atenção no calor sob as raízes",
        "values": ["dever", "proteção", "disciplina"], "red_lines": ["abrir selo desconhecido", "ameaçar criança"],
    },
    {
        "id": "hela_fruto_vermelho", "name": "Hela Fruto-Vermelho", "race": "Solari", "role": "dona de estalagem",
        "home": "passagem_cervo", "faction": "estradas_livres", "x": -700.0, "y": 2360.0,
        "description": "uma Solari de voz clara conta porções e cobertores antes de abrir espaço à mesa",
        "values": ["hospitalidade", "clareza", "trabalho"], "red_lines": ["envenenar hóspede", "negar pagamento"],
    },
    {
        "id": "dori_folha_de_ferro", "name": "Dori Folha-de-Ferro", "race": "Aureli", "role": "ferreira",
        "home": "sylvarin", "faction": "oficios_livres", "x": 20.0, "y": 1740.0,
        "description": "uma Aureli testa a flexibilidade de lâminas destinadas a cortar somente madeira morta",
        "values": ["qualidade", "limite", "legado"], "red_lines": ["cortar Árvore-Anciã", "vender arma defeituosa"],
    },
    {
        "id": "iven_neve_mansa", "name": "Iven Neve-Mansa", "race": "Glacari", "role": "médico de fronteira",
        "home": "portao_nevoa", "faction": "vigias_da_fronteira", "x": 210.0, "y": 2940.0,
        "description": "um Glacari de movimentos lentos compara a umidade das folhas com o gelo trazido do norte",
        "values": ["prudência", "cuidado", "travessia livre"], "red_lines": ["abandonar viajante exposto", "fechar a fronteira por origem"],
    },
]


ELDORWOOD_ROADS: list[dict[str, Any]] = [
    {"id": "estrada_do_dossel", "a": (0.0, 1780.0), "b": (-1430.0, 2620.0), "width_km": 24.0},
    {"id": "rota_das_duas_margens", "a": (920.0, 760.0), "b": (610.0, 1240.0), "width_km": 20.0},
    {"id": "caminho_de_eldor", "a": (610.0, 1240.0), "b": (0.0, 1780.0), "width_km": 18.0},
    {"id": "estrada_da_fronteira", "a": (-1430.0, 2620.0), "b": (180.0, 2920.0), "width_km": 22.0},
    {"id": "rota_dos_boticarios", "a": (-390.0, 810.0), "b": (150.0, 1430.0), "width_km": 12.0},
    {"id": "rota_do_brejo", "a": (920.0, 760.0), "b": (1510.0, -880.0), "width_km": 16.0},
    {"id": "trilha_de_lethariel", "a": (0.0, 1780.0), "b": (-1120.0, 2140.0), "width_km": 10.0},
]


REGION_MAPS: dict[str, dict[str, Any]] = {
    "eldorwood": {
        "name": "Eldorwood",
        "spawns": {
            "floresta_densa_antiga": [(-240.0, 1500.0), (380.0, 1620.0), (-760.0, 1880.0)],
            "pantanos_rios": [(1320.0, -1220.0), (1760.0, -420.0), (1080.0, 260.0)],
            "colinas_arborizadas": [(-1280.0, 2700.0), (320.0, 2780.0), (-420.0, 2460.0)],
        },
        "borders": [
            {
                "id": "eldorwood_frostreach", "axis": "y", "limit": 3000.0, "operator": ">=",
                "x_min": -900.0, "x_max": 1250.0, "direction": "norte",
                "target_region": "frostreach", "target_biome": "planalto_central_frostreach",
                "target_position": (450.0, -2920.0),
                "name": "Fronteira Nebulosa de Frostreach",
                "description": "As últimas colinas perdem árvores. Tundra, vento e placas de neve ocupam o norte; atrás de você, a umidade de Eldorwood ainda cobre as folhas.",
            },
        ],
    },
    "frostreach": {
        "name": "Frostreach",
        "borders": [
            {
                "id": "frostreach_eldorwood", "axis": "y", "limit": -3000.0, "operator": "<=",
                "x_min": -900.0, "x_max": 1250.0, "direction": "sul",
                "target_region": "eldorwood", "target_biome": "colinas_arborizadas",
                "target_position": (450.0, 2960.0),
                "name": "Fronteira das Colinas Úmidas",
                "description": "A tundra cede a bosques, muros cobertos de musgo e uma neblina que carrega cheiro de terra viva. Eldorwood começa sem portal ou corte artificial.",
            },
        ],
    },
}


ELDORWOOD_PHASE_DETAILS = {
    "Madrugada": (
        "Musgos fornecem a única luz constante; água pinga em frequências que escondem passos distantes.",
        "A neblina se concentra perto do chão e reduz troncos enormes a silhuetas próximas.",
        "Animais noturnos encerram a caça enquanto os primeiros pássaros ainda permanecem quietos.",
    ),
    "Amanhecer": (
        "A claridade chega primeiro às copas e demora a alcançar o caminho sob seus pés.",
        "Teias e folhas molhadas refletem luz suficiente para revelar passagens antes invisíveis.",
        "Fumaças de moradias podem ser vistas entre árvores, mas a distância continua difícil de medir.",
    ),
    "Manhã": (
        "Estradas e trilhas ganham movimento perto de cidades; longe delas, a floresta continua quase vazia.",
        "O ar permanece frio e úmido, carregado pelo cheiro de casca, água e trabalho distante.",
        "Insetos, aves e pequenos mamíferos ocupam o espaço sem transformar cada encontro em ameaça.",
    ),
    "Tarde": (
        "A luz lateral atravessa algumas clareiras e revela poeira, pólen e esporos suspensos.",
        "Carroças procuram terreno firme antes da chuva; trilhas secundárias ficam silenciosas.",
        "O calor moderado aumenta o cheiro das plantas e facilita perceber água contaminada.",
    ),
    "Entardecer": (
        "A penumbra chega cedo sob o dossel. Moradores procuram abrigo antes de perder referências.",
        "Corujas começam a chamar enquanto viajantes calculam a distância até portas e pontes.",
        "Luzes de cidades grandes aparecem em níveis diferentes entre troncos e colinas.",
    ),
    "Noite": (
        "Musgos, peixes e fogo-fátuos formam pontos de luz que não obedecem às estradas.",
        "Predadores usam o som da chuva e das folhas para esconder aproximações.",
        "Dentro de muralhas há mercados noturnos e vigias; fora delas, a distância volta a ser escura.",
    ),
}


ELDORWOOD_QUIET_TRAVEL = (
    "O trecho contém apenas árvores, fungos, folhas e água. Nenhuma presença altera o caminho por sua causa.",
    "Você encontra fezes e pelos de animais, mas todos os sinais têm horas ou dias e não exigem perseguição.",
    "Durante quase todo o período, caminhar significa contornar raízes e manter uma referência entre troncos semelhantes.",
    "Uma construção surge no horizonte e desaparece atrás do relevo; ainda está a muitos quilômetros.",
    "Pássaros mudam de árvore sem alarme. A floresta percebe você, mas não reage como se fosse uma invasão.",
    "Há vegetação suficiente para estudar por horas, porém nada raro ou urgente aparece neste trecho.",
    "A trilha mantém marcas de uso antigo e nenhum viajante recente. Distância, não perigo, domina a marcha.",
    "A chuva ocupa parte do caminho. Você ajusta roupa, apoios e direção sem que um encontro interrompa o tempo.",
)
