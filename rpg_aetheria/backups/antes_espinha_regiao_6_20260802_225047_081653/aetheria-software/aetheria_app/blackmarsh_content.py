from __future__ import annotations

"""Dados espaciais, ecológicos, sociais e econômicos da Região 5 — Blackmarsh."""

from typing import Any


BLACKMARSH_BIOMES: dict[str, dict[str, Any]] = {
    "pantanos_vastos": {
        "name": "Pântanos Vastos", "region": "blackmarsh", "speed_kmh": 1.35, "temperature_delta": 7,
        "ambience": [
            "Água marrom-preta cobre a base das árvores e esconde a profundidade. Cada passo precisa encontrar apoio antes de receber o peso do corpo.",
            "Chuva morna fecha o horizonte e transforma sons próximos em distâncias enganosas; insetos retomam o coro assim que você para.",
            "Raízes submersas formam corredores que não aparecem em mapas. Bolhas isoladas podem indicar decomposição, nascente ou respiração.",
            "Luzes azuis, verdes e violetas surgem entre troncos. Algumas pertencem a insetos; outras mantêm posição contra vento e corrente.",
            "O cheiro doce dos Lírios-de-Pântano atravessa lama e folhas apodrecidas, forte o bastante para esconder sinais de toxina.",
            "O solo guarda peças da Batalha das Fendas: metal oxidado, pedra vitrificada e círculos onde o musgo se recusa a crescer.",
        ],
        "weather": ["chuva constante", "calor úmido", "névoa baixa", "trovoada distante", "garoa quente", "noite abafada"],
        "routes": {
            "norte": ["Testar raízes firmes rumo ao norte", "Seguir marcas Aquari para o norte", "Acompanhar água mais clara ao norte"],
            "sul": ["Avançar entre juncos para o sul", "Seguir o fluxo lento ao sul", "Contornar poças fundas rumo ao sul"],
            "leste": ["Usar ilhas de musgo rumo a leste", "Seguir as luzes sem alcançá-las a leste", "Acompanhar raízes retorcidas para leste"],
            "oeste": ["Procurar terreno elevado a oeste", "Seguir aves sombrias para oeste", "Manter a corrente à direita e ir a oeste"],
        },
        "flora": [
            ("Musgo-Negro", "tapetes esponjosos absorvem água, matéria orgânica e objetos pequenos", False, False),
            ("Lírio-de-Pântano", "flores pálidas exalam perfume adocicado capaz de mascarar perigo", False, True),
            ("Raiz-Retorcida Sombria", "raízes aéreas e submersas formam passagens instáveis", False, False),
            ("Alga-Pura de Aquanium", "a alga cresce somente onde a água pode ser tratada com segurança", True, False),
            ("Flor-de-Fogo-Fátuo", "pétalas iridescentes abrem perto das luzes móveis", False, False),
            ("Samambaia-de-Lama", "folhas pesadas indicam trechos de lodo menos ácido", False, False),
            ("Cogumelo-de-Sombra", "variedades quase idênticas podem ser medicinais, tóxicas ou alucinógenas", False, True),
        ],
        "fauna": [
            ("Crocodilo-Negro", "predator", 6, "olhos imóveis permanecem acima da água enquanto o corpo desaparece no lodo"),
            ("Serpente-d'Água Gigante", "predator", 6, "um corpo de até seis metros deixa ondas onde não há vento"),
            ("Garça-Sombria", "neutral", 1, "uma ave alta caça em silêncio e evita áreas contaminadas"),
            ("Sapo-Gigante de Blackmarsh", "territorial", 4, "a pele tóxica de um anfíbio do tamanho de um cão bloqueia uma raiz seca"),
            ("Peixe-Luminoso", "neutral", 1, "luzes azuis sob a superfície atraem presas e predadores"),
            ("Inseto-Fogo-Fátuo", "mystic", 3, "um enxame organiza luzes numa rota que muda quando observado"),
            ("Rato-d'Água Negro", "neutral", 2, "roedores deixam tocas semi-submersas ao sentir uma alteração na água"),
            ("Vulto-das-Fendas", "mystic", 6, "uma sombra se move sem corresponder a corpo ou fonte de luz"),
            ("Ninfa-Negra", "legendary", 7, "uma figura aquática decide entre guiar, testar ou afogar quem entra em sua corrente"),
            ("Guardião da Fenda Selada", "legendary", 10, "uma entidade antiga reage a sangue, Resonum e ordens da Vigília do Limiar"),
        ],
        "landmarks": [
            ("Fenda Selada", "O campo central da antiga batalha permanece coberto por selos, água e estruturas que pulsam em ritmos diferentes."),
            ("Luzes de Blackmarsh", "Fogo-fátuo forma caminhos belos; somente alguns terminam em terreno firme."),
            ("Corredor das Raízes Negras", "Raízes densas criam um labirinto usado por predadores e navegadores clandestinos."),
            ("Hospital da Água Alta", "Uma plataforma de quarentena recebe febris sem perguntar origem, mas registra cada visitante."),
            ("Memorial sem Nomes", "Placas vazias lembram mortos que nunca receberam registro legal."),
        ],
        "hazards": [
            ("Água Potável Falsa", "Uma poça clara contém parasitas invisíveis e não apresenta o cheiro comum de decomposição."),
            ("Lodo de Sucção", "A superfície segura o pé enquanto a água sobe e o apoio ao redor se desfaz."),
            ("Enxame Tóxico", "Insetos respondem ao calor corporal e ocupam qualquer abertura da roupa."),
            ("Febre de Duas Margens", "Um animal debilitado deixa secreções junto à única passagem seca."),
        ],
    },
    "mangues_gigantes": {
        "name": "Mangues Gigantes", "region": "blackmarsh", "speed_kmh": 1.6, "temperature_delta": 5,
        "ambience": [
            "Raízes aéreas do tamanho de torres dividem a maré em corredores. O caminho de agora estará submerso em poucas horas.",
            "Sal, madeira úmida e algas ocupam o ar. Marcas de barco aparecem muito acima da água atual e anunciam a força da próxima maré.",
            "Sinos de concha presos às raízes funcionam como avisos de corrente, não decoração. Cada comunidade usa um ritmo diferente.",
            "Cavernas costeiras devolvem o som da água em frequências de Resonum; algumas respostas surgem quando o mar está imóvel.",
            "Ninhos ocupam raízes altas, enquanto caranguejos disputam lama e restos deixados pela maré.",
            "Passarelas de madeira terminam no vazio porque canais, vilas flutuantes e ancoradouros mudaram desde a última estação.",
        ],
        "weather": ["maré crescente", "tempestade costeira", "vento salgado", "chuva lateral", "calmaria abafada", "maré vazante"],
        "routes": {
            "norte": ["Subir por raízes marcadas ao norte", "Seguir a maré vazante para o norte", "Acompanhar passarelas rumo ao norte"],
            "sul": ["Usar canais abrigados ao sul", "Contornar raízes gigantes para o sul", "Seguir barcos de fundo raso ao sul"],
            "leste": ["Acompanhar a costa para leste", "Seguir sinos de corrente a leste", "Cruzar lama firme rumo a leste"],
            "oeste": ["Procurar a salina a oeste", "Seguir o cheiro do mar para oeste", "Acompanhar raízes cortadas rumo a oeste"],
        },
        "flora": [
            ("Mangue-Gigante", "raízes aéreas formam plataformas, túneis e paredes vivas", False, False),
            ("Alga-Salobra", "colônias comestíveis crescem onde água doce encontra maré", True, False),
            ("Flor-de-Maré", "pétalas rosadas abrem somente durante a maré baixa", False, False),
            ("Musgo-de-Raiz", "uma camada escorregadia cobre os apoios mais usados", False, False),
            ("Samambaia-Costeira", "folhas resistentes ao sal abrigam ovos e pequenos crustáceos", False, False),
            ("Planta-de-Sal", "folhas cristalizadas acumulam sal e minerais de cada inundação", True, False),
        ],
        "fauna": [
            ("Caranguejo-Gigante de Mangue", "territorial", 4, "uma colônia fecha as pinças ao redor de uma área de alimentação"),
            ("Crocodilo-Costeiro", "predator", 5, "um predador menor e agressivo acompanha um canal estreito"),
            ("Ave-de-Mangue", "neutral", 1, "aves transportam fibras e revelam onde raízes continuam secas"),
            ("Serpente-de-Raiz", "predator", 4, "escamas imitam casca e escondem veneno paralisante"),
            ("Peixe-Salobra", "pacific", 0, "cardumes atravessam a mudança de salinidade com a maré"),
            ("Morcego-de-Caverna", "neutral", 2, "chamados anômalos desenham cavidades antes que a água as cubra"),
            ("Eco-das-Raízes", "mystic", 5, "vozes antigas usam o labirinto para oferecer direções incompatíveis"),
            ("Guardião de Harmonix", "legendary", 9, "raízes vivas assumem forma para proteger maré, reprodução e ciclos de sal"),
        ],
        "landmarks": [
            ("Labirinto de Mangue", "Corredores de raízes mudam com maré, erosão e crescimento."),
            ("Cavernas da Maré", "Resonum transforma água corrente em vozes e alarmes antigos."),
            ("Salina de Raízes", "Plantas cristalizadas sustentam comércio e registram contaminação."),
            ("Farol de Conchas", "Um farol sem chama usa som para orientar barcos durante chuva e névoa."),
            ("Cemitério de Cascos", "Embarcações de épocas diferentes permanecem presas no alto das raízes."),
        ],
        "hazards": [
            ("Maré de Retorno", "A água ocupa o corredor antes que a rota de volta permaneça acessível."),
            ("Raiz Coberta", "Musgo escorregadio oculta uma queda para lama e conchas cortantes."),
            ("Tempestade Costeira", "Vento, água e madeira solta transformam abrigo alto em alvo."),
            ("Caverna Enchendo", "O Resonum mascara a velocidade real com que a maré entra."),
        ],
    },
    "ilhas_vegetacao_flutuante": {
        "name": "Ilhas de Vegetação Flutuante", "region": "blackmarsh", "speed_kmh": 1.15, "temperature_delta": 6,
        "ambience": [
            "O chão de turfa desce alguns centímetros sob cada passo e continua oscilando depois que você para.",
            "Ilhas cobertas de vegetação deslocam-se devagar entre canais escuros. Distâncias mudam enquanto você observa.",
            "Vinhas-de-Turfa unem placas de solo; cortar uma para obter fibra pode alterar a estabilidade de toda a margem.",
            "Flores mudam de cor com umidade e pressão. Padrões de Patterium tornam bonitas justamente as espécies mais tóxicas.",
            "Aves migrantes seguem ilhas específicas, não pontos do horizonte. Mapas locais registram data, vento e corrente junto de cada linha.",
            "Sob a turfa, algo grande toca raízes e carapaças sem romper a superfície. O movimento pode ser animal, corrente ou parte do próprio circuito.",
        ],
        "weather": ["chuva torrencial", "pressão baixa", "calor úmido", "vento contrário à corrente", "névoa violeta", "calmaria antes da chuva"],
        "routes": {
            "norte": ["Saltar por placas mais espessas ao norte", "Seguir aves migrantes para o norte", "Acompanhar uma ilha lenta rumo ao norte"],
            "sul": ["Testar vinhas de conexão ao sul", "Usar um canal estreito para o sul", "Seguir flores de menor umidade ao sul"],
            "leste": ["Acompanhar o movimento da turfa a leste", "Cruzar por raízes flutuantes a leste", "Seguir marcas temporárias rumo a leste"],
            "oeste": ["Procurar água aberta a oeste", "Seguir estacas datadas para oeste", "Usar uma ilha alongada rumo a oeste"],
        },
        "flora": [
            ("Musgo-Flutuante", "camadas espessas formam a base instável das ilhas", False, False),
            ("Planta-Venenosa de Patterium", "folhas simétricas contêm toxina concentrada", False, True),
            ("Flor-de-Ilha", "pétalas mudam de cor conforme umidade e pressão", False, False),
            ("Samambaia-Flutuante", "raízes largas distribuem peso e estabilizam a turfa", False, False),
            ("Cogumelo-Migrante", "colônias aparecem e desaparecem conforme a ilha muda de posição", False, True),
            ("Vinhas-de-Turfa", "fibras vivas mantêm placas de vegetação conectadas", False, False),
        ],
        "fauna": [
            ("Rã-Flutuante", "territorial", 3, "um anfíbio colorido e tóxico salta entre placas próximas"),
            ("Inseto-de-Patterium", "mystic", 3, "um enxame voa em padrões geométricos e protege ovos sob folhas"),
            ("Serpente-Flutuante", "predator", 5, "uma serpente cruza água e turfa sem produzir ondas regulares"),
            ("Ave-Migrante", "neutral", 1, "a ave acompanha a mesma ilha por meses"),
            ("Caramujo-Gigante", "territorial", 4, "uma concha resistente sustenta parte de uma margem"),
            ("Espírito-das-Ilhas", "mystic", 6, "uma presença altera corrente e posição para separar ou reunir caminhos"),
            ("Sombra-Flutuante", "predator", 7, "algo sob a ilha segue calor e vibração através das raízes"),
            ("Guardião de Orbitium", "legendary", 10, "vegetação, água e energia orbital protegem o equilíbrio móvel"),
        ],
        "landmarks": [
            ("Ilhas Migrantes", "Massas de turfa carregam casas, fauna e histórias para novas coordenadas."),
            ("Mar de Turfa", "Água profunda separa centenas de ilhas frágeis e rotas sazonais."),
            ("Núcleo de Orbitium", "Uma anomalia parece coordenar movimento contra vento e corrente."),
            ("Ilha do Terceiro Círculo", "Durante três noites, a ilha repete a mesma órbita e completa parte do Limiar."),
            ("Vila entre Respirações", "Telhados e vozes aparecem em intervalos como se a comunidade ocupasse duas margens do mundo."),
        ],
        "hazards": [
            ("Ruptura de Turfa", "A placa abre lentamente e transforma chão em duas ilhas separadas."),
            ("Flor de Contato", "Pólen tóxico adere à pele molhada antes de provocar dormência."),
            ("Deslocamento Noturno", "O acampamento amanhece quilômetros longe da rota calculada."),
            ("Pressão do Limiar", "Ouvidos, visão e equilíbrio respondem a uma mudança que o céu não explica."),
        ],
    },
}


BLACKMARSH_SETTLEMENTS: list[dict[str, Any]] = [
    {"id":"nhar_delta","name":"Nhar-Delta","type":"capital de confluência","population":142000,"x":-240.0,"y":1180.0,"radius_km":38.0,"scene_id":"r5_nhar_delta_cais_da_confluencia","description":"Capital de plataformas, canais e assembleias por bacia; sede da Confluência e dos Vigias do Limiar."},
    {"id":"porto_lodoalto","name":"Porto Lodoalto","type":"cidade portuária","population":65000,"x":-1520.0,"y":980.0,"radius_km":28.0,"scene_id":"r5_porto_lodoalto_doca_alta","description":"Porto Aquari construído acima da maré máxima, centro de barcos rasos, pescado e navegação costeira."},
    {"id":"sete_aguas","name":"Confluência das Sete Águas","type":"cidade de canais","population":42000,"x":420.0,"y":1960.0,"radius_km":24.0,"scene_id":"r5_sete_aguas_ponte_das_bacias","description":"Cidade onde sete bacias elegem vozes e disputam quarentena, abastecimento e passagem."},
    {"id":"raiz_catedral","name":"Raiz-Catedral","type":"cidade de mangue","population":28000,"x":-2100.0,"y":-120.0,"radius_km":20.0,"scene_id":"r5_raiz_catedral_portico_vivo","description":"Cidade dentro de raízes gigantes, mantida por podas, pontes e pactos com o Guardião de Harmonix."},
    {"id":"mare_oca","name":"Maré Oca","type":"cidade de cavernas","population":19000,"x":-1180.0,"y":-860.0,"radius_km":17.0,"scene_id":"r5_mare_oca_entrada_da_caverna","description":"Cidade costeira que usa cavernas de Resonum, abrindo e fechando bairros conforme a maré."},
    {"id":"varzea_errante","name":"Várzea Errante","type":"cidade flutuante","population":21000,"x":1260.0,"y":420.0,"radius_km":18.0,"scene_id":"r5_varzea_errante_ancoradouro_movel","description":"Cidade distribuída por ilhas conectadas, cuja posição muda e torna endereço uma combinação de data, corrente e vizinhança."},
    {"id":"farol_sal","name":"Farol de Sal","type":"vila de navegação","population":12000,"x":-2600.0,"y":-980.0,"radius_km":13.0,"scene_id":"r5_farol_sal_torre_de_conchas","description":"Vila costeira que orienta barcos com sons de concha, salinas e sinais luminosos controlados."},
    {"id":"ponte_turfa","name":"Ponte-Turfa","type":"vila flutuante","population":8000,"x":2080.0,"y":1120.0,"radius_km":11.0,"scene_id":"r5_ponte_turfa_passarela_flexivel","description":"Vila de passarelas flexíveis, mecânicos Ziraki e cultivadores que estabilizam ilhas sem imobilizá-las."},
    {"id":"lago_cego","name":"Lago Cego","type":"comunidade de cura","population":6200,"x":860.0,"y":-1040.0,"radius_km":10.0,"scene_id":"r5_lago_cego_plataforma_de_quarentena","description":"Comunidade médica e botânica junto a água opaca, dedicada à Febre de Duas Margens."},
    {"id":"vigilia_norte","name":"Vigília do Norte","type":"posto de fronteira","population":3400,"x":520.0,"y":2920.0,"radius_km":9.0,"scene_id":"r5_vigilia_norte_marco_das_chuvas","description":"Posto entre os vales de Stonevale e as primeiras águas profundas de Blackmarsh."},
    {"id":"porto_cinzento","name":"Porto Cinzento","type":"posto fluvial","population":4800,"x":-2900.0,"y":1880.0,"radius_km":10.0,"scene_id":"r5_porto_cinzento_cais_de_fronteira","description":"Entreposto ocidental conectado às rotas de Arkanor, ocupado por fiscais, barqueiros e resgatadores clandestinos."},
]


BLACKMARSH_NPCS: list[dict[str, Any]] = [
    {"id":"neris_mare_cega","name":"Neris Maré-Cega","race":"Ninfari","role":"navegadora clandestina e possível companheira","home":"varzea_errante","faction":"rede_da_mare_cega","x":1260.0,"y":440.0,"description":"uma Ninfari memoriza ilhas pela pressão da água e esconde pessoas destinadas ao sacrifício","values":["liberdade","resgate","responsabilidade"],"red_lines":["entregar refugiado","possuir parceiro"]},
    {"id":"seris_vael","name":"Seris Vael","race":"Ethari","role":"emissária Vorath e possível companheira","home":"lago_cego","faction":"coro_do_retorno","x":880.0,"y":-1020.0,"description":"uma figura quase Ethari escuta vozes do outro lado do Limiar sem fingir neutralidade","values":["libertação","verdade","autonomia"],"red_lines":["usar Vorath como combustível","ocultar decisão existencial"]},
    {"id":"maeva_nhar","name":"Maeva Nhar","race":"Umbrari","role":"Primeira Guardiã do Limiar","home":"nhar_delta","faction":"vigias_do_limiar","x":-220.0,"y":1200.0,"description":"uma Umbrari conhece o custo biológico do selo e acredita que revelar tudo pode matar mais pessoas","values":["continuidade","selo","dever"],"red_lines":["abrir sem evacuar","destruir registros do selo"]},
    {"id":"tomas_agua_alta","name":"Tomás Água-Alta","race":"Humana","role":"médico de quarentena","home":"lago_cego","faction":"casa_das_duas_margens","x":840.0,"y":-1060.0,"description":"um médico humano separa sintoma de origem racial enquanto a fila cresce sob chuva","values":["cura","prova","acesso"],"red_lines":["experimento forçado","abandono de febril"]},
    {"id":"silea_raiz_clara","name":"Silea Raiz-Clara","race":"Sylvani","role":"botânica de mangue","home":"raiz_catedral","faction":"jardineiros_da_mare","x":-2080.0,"y":-100.0,"description":"uma Sylvani poda raízes sem romper os corredores usados por peixes e moradores","values":["ciclo","cultivo","consentimento ecológico"],"red_lines":["cortar raiz-mãe","envenenar canal"]},
    {"id":"brann_pedra_boiando","name":"Brann Pedra-Boiando","race":"Aureli","role":"construtor de fundações","home":"ponte_turfa","faction":"mestres_da_turfa","x":2060.0,"y":1140.0,"description":"um Aureli calcula peso em solo flutuante e admite que tradição de pedra precisa mudar","values":["estrutura","aprendizado","trabalho"],"red_lines":["sobrecarregar ilha","ocultar falha"]},
    {"id":"suri_tres_correntes","name":"Suri Três-Correntes","race":"Aquari","role":"capitã de navegação","home":"porto_lodoalto","faction":"coro_de_navegadores","x":-1500.0,"y":1000.0,"description":"uma Aquari lê maré, chuva e humor da tripulação antes de aceitar carga","values":["tripulação","fluxo livre","acordo"],"red_lines":["contaminar água","abandonar passageiro"]},
    {"id":"amina_chuva_branca","name":"Amina Chuva-Branca","race":"Solari","role":"meteorologista tropical","home":"sete_aguas","faction":"observatorio_das_chuvas","x":400.0,"y":1980.0,"description":"uma Solari mede o céu através de reflexos porque a chuva raramente permite olhar para cima","values":["previsão honesta","evacuação","método"],"red_lines":["falsificar tempestade","reter alerta"]},
    {"id":"ivel_gelo_morno","name":"Ivel Gelo-Morno","race":"Glacari","role":"especialista em febres","home":"lago_cego","faction":"casa_das_duas_margens","x":900.0,"y":-1060.0,"description":"um Glacari usa metabolismo lento para acompanhar pacientes por noites inteiras","values":["cuidado","isolamento proporcional","paciência"],"red_lines":["quarentena racial","negar antídoto"]},
    {"id":"pali_luz_baixa","name":"Pali Luz-Baixa","race":"Luminari","role":"pesquisadora de fogo-fátuo","home":"nhar_delta","faction":"arquivo_das_luzes","x":-260.0,"y":1160.0,"description":"uma Luminari distingue inseto, reflexo e anomalia sem tocar nas luzes","values":["curiosidade","beleza","segurança"],"red_lines":["atrair criança ao pântano","enjaular enxame"]},
    {"id":"garr_lama_firme","name":"Garr Lama-Firme","race":"Kragari","role":"chefe de resgate","home":"sete_aguas","faction":"brigada_das_bacias","x":440.0,"y":1940.0,"description":"um Kragari usa força para retirar pessoas do lodo e autoridade para impedir curiosos de entrar","values":["proteção","equipe","honra"],"red_lines":["abandonar soterrado","violência por medo"]},
    {"id":"zikka_sete_rebites","name":"Zikka Sete-Rebites","race":"Ziraki","role":"mecânica de barcos","home":"ponte_turfa","faction":"irmandade_sete_parafusos","x":2100.0,"y":1100.0,"description":"uma Ziraki transforma sucata em lemes, filtros e pontes que aceitam movimento","values":["invenção","autoria","reparo"],"red_lines":["roubar projeto","culpar aprendiz"]},
    {"id":"dorra_raiz_de_ferro","name":"Dorra Raiz-de-Ferro","race":"Ferrari","role":"engenheira de plataformas","home":"raiz_catedral","faction":"mestres_da_turfa","x":-2120.0,"y":-140.0,"description":"uma Ferrari escuta pilares e raízes antes de autorizar mais peso","values":["manutenção","segurança","responsabilidade"],"red_lines":["ignorar vibração","construir sobre ninho"]},
    {"id":"kaar_mare_quente","name":"Kaar Maré-Quente","race":"Drakari","role":"guardião reformista","home":"nhar_delta","faction":"vigias_do_limiar_reformistas","x":-200.0,"y":1220.0,"description":"um Drakari percebe a febre em prisioneiros e questiona ordens que chama de proteção","values":["dever","reforma","vida"],"red_lines":["sacrifício secreto","execução sem julgamento"]},
    {"id":"toru_turfa_funda","name":"Toru Turfa-Funda","race":"Voraki","role":"cartógrafa de ilhas","home":"varzea_errante","faction":"mapas_temporarios","x":1240.0,"y":400.0,"description":"uma Voraki sente ilhas se separando antes que a água abra uma linha visível","values":["território móvel","precisão","acesso"],"red_lines":["mapa falso","cortar ilha habitada"]},
    {"id":"elion_sal_calmo","name":"Elion Sal-Calmo","race":"Humana","role":"mercador de antídotos","home":"farol_sal","faction":"mercado_da_mare","x":-2580.0,"y":-960.0,"description":"um humano mantém preços públicos e uma reserva cuja distribuição depende da Confluência","values":["estoque","comércio","continuidade"],"red_lines":["antídoto falso","monopólio durante surto"]},
    {"id":"asha_vael","name":"Asha Vael","race":"Vorath","role":"sobrevivente entre margens","home":"vila_entre_respiracoes","faction":"alianca_antiga","x":1840.0,"y":-620.0,"description":"uma sobrevivente da guerra aparece em intervalos, lembrando ter ajudado a fechar o Limiar","values":["testemunho","povo","escolha"],"red_lines":["reescrever aliança","usar sua vida como chave"]},
]


BLACKMARSH_ROADS: list[dict[str, Any]] = [
    {"id":"canal_da_confluencia","a":(-240.0,1180.0),"b":(420.0,1960.0),"width_km":28.0},
    {"id":"rota_de_lodoalto","a":(-1520.0,980.0),"b":(-240.0,1180.0),"width_km":25.0},
    {"id":"canal_da_raiz","a":(-1520.0,980.0),"b":(-2100.0,-120.0),"width_km":20.0},
    {"id":"rota_da_mare_oca","a":(-2100.0,-120.0),"b":(-1180.0,-860.0),"width_km":18.0},
    {"id":"rota_do_farol","a":(-1180.0,-860.0),"b":(-2600.0,-980.0),"width_km":17.0},
    {"id":"canal_errante","a":(-240.0,1180.0),"b":(1260.0,420.0),"width_km":24.0},
    {"id":"ponte_das_ilhas","a":(1260.0,420.0),"b":(2080.0,1120.0),"width_km":16.0},
    {"id":"rota_do_lago_cego","a":(1260.0,420.0),"b":(860.0,-1040.0),"width_km":19.0},
    {"id":"caminho_da_vigilia","a":(420.0,1960.0),"b":(520.0,2920.0),"width_km":18.0},
    {"id":"rota_do_porto_cinzento","a":(-1520.0,980.0),"b":(-2900.0,1880.0),"width_km":20.0},
]


BLACKMARSH_MARKETS: dict[str, dict[str, Any]] = {
    "nhar_delta":{"currency":"coroas","water_index":1.15,"stock":[("filtro de Aquanium",12,5),("capa de chuva",8,3),("mapa temporário",10,4)]},
    "porto_lodoalto":{"currency":"coroas","water_index":1.05,"stock":[("peixe salobro",4,2),("remo curto",9,4),("rede de mangue",11,5)]},
    "sete_aguas":{"currency":"coroas","water_index":0.95,"stock":[("odre tratado",5,2),("antídoto comum",13,6),("sino de corrente",7,3)]},
    "raiz_catedral":{"currency":"coroas","water_index":1.10,"stock":[("fibra de mangue",6,3),("gancho de raiz",10,4),("alga salobra",3,1)]},
    "mare_oca":{"currency":"coroas","water_index":1.20,"stock":[("lanterna de caverna",10,4),("tampão de Resonum",8,3),("sal medicinal",6,2)]},
    "varzea_errante":{"currency":"coroas","water_index":1.25,"stock":[("estaca datada",6,2),("poncho de turfa",9,4),("mapa temporário",12,5)]},
    "farol_sal":{"currency":"coroas","water_index":1.15,"stock":[("sal de raiz",4,2),("sinal de concha",8,3),("antídoto comum",14,6)]},
    "ponte_turfa":{"currency":"coroas","water_index":1.30,"stock":[("tábua flexível",9,4),("kit de rebites",13,6),("corda de vinha",7,3)]},
    "lago_cego":{"currency":"coroas","water_index":0.85,"stock":[("antídoto de febre",16,7),("máscara de esporos",10,4),("água tratada",4,2)]},
    "vigilia_norte":{"currency":"coroas","water_index":1.20,"stock":[("capa de chuva",9,4),("mapa de fronteira",8,3),("ração selada",6,3)]},
    "porto_cinzento":{"currency":"coroas","water_index":1.25,"stock":[("passagem fluvial",10,4),("odre tratado",6,2),("caixa impermeável",12,5)]},
}


BLACKMARSH_REGION_MAPS: dict[str, dict[str, Any]] = {
    "blackmarsh": {
        "name":"Blackmarsh",
        "spawns": {
            "pantanos_vastos":[(-320.0,2180.0),(520.0,1560.0),(-860.0,1380.0)],
            "mangues_gigantes":[(-2180.0,1760.0),(-1640.0,460.0),(-2580.0,-320.0)],
            "ilhas_vegetacao_flutuante":[(1120.0,1160.0),(2020.0,220.0),(820.0,-1260.0)],
        },
        "borders": [
            {"id":"blackmarsh_stonevale","axis":"y","limit":3000.0,"operator":">=","x_min":-800.0,"x_max":2200.0,"direction":"norte","target_region":"stonevale","target_biome":"vales_ferteis_isolados","target_position":(520.0,-1760.0),"name":"Fronteira das Chuvas Quentes","description":"A água negra se divide em canais de vale, a chuva perde força e as primeiras pedras de Stonevale surgem ao norte."},
            {"id":"blackmarsh_arkanor","axis":"x","limit":-3000.0,"operator":"<=","x_min":-10000.0,"x_max":10000.0,"y_min":1100.0,"y_max":2700.0,"direction":"oeste","target_region":"arkanor","target_biome":"vales_verdes","target_position":(1760.0,-1180.0),"name":"Fronteira do Rio Cinzento","description":"Mangue e pântano cedem a margens firmes, pontes e canais medidos do extremo sul de Arkanor."},
        ],
    }
}


STONEVALE_BLACKMARSH_BORDER = {"id":"stonevale_blackmarsh","axis":"y","limit":-1800.0,"operator":"<=","x_min":-800.0,"x_max":2200.0,"direction":"sul","target_region":"blackmarsh","target_biome":"pantanos_vastos","target_position":(520.0,2960.0),"name":"Fronteira das Primeiras Águas","description":"Os vales ficam mais úmidos, o terreno perde firmeza e chuvas quentes anunciam Blackmarsh sem muralha."}

ARKANOR_BLACKMARSH_BORDER = {"id":"arkanor_blackmarsh","axis":"y","limit":-1300.0,"operator":"<=","x_min":600.0,"x_max":1800.0,"direction":"sul","target_region":"blackmarsh","target_biome":"mangues_gigantes","target_position":(-2860.0,1880.0),"name":"Fronteira dos Canais Escuros","description":"O Aurenta se divide, salgueiros cedem a mangues e a estrada termina em embarcadouros de Blackmarsh."}


BLACKMARSH_PHASE_DETAILS = {
    "Madrugada":("Fogo-fátuo e olhos animais parecem usar a mesma luz.","A água conserva calor enquanto o ar esfria pouco.","Barcos clandestinos aproveitam névoa e maré antes do amanhecer."),
    "Amanhecer":("A primeira claridade revela bolhas, rastros e profundidades escondidas.","Aves deixam raízes altas e indicam áreas sem predadores imediatos.","Mercados medem chuva, maré e casos de febre antes de abrir."),
    "Manhã":("Calor e umidade sobem enquanto a chuva alterna intensidade.","Rotas movimentadas recebem barcos; trechos selvagens permanecem vazios por horas.","Flores abrem e insetos tornam algumas passagens quase impraticáveis."),
    "Tarde":("Trovoadas reduzem visibilidade e elevam canais em poucos minutos.","A roupa molhada impede o corpo de resfriar apesar do vento.","Ilhas flutuantes mudam posição e invalidam referências da manhã."),
    "Entardecer":("Maré, chuva e deslocamento de turfa redesenham rotas usadas durante o dia.","Luzes coloridas surgem antes que a escuridão esconda suas origens.","Vilas recolhem passarelas e registram quem ainda não retornou."),
    "Noite":("Predadores usam água e raízes sem produzir sinais fáceis de separar.","Qualquer luz atrai insetos e anuncia posição a grandes distâncias.","O Limiar parece mais próximo quando vozes atravessam canais sem barco ou corpo."),
}


BLACKMARSH_QUIET_TRAVEL = (
    "O trecho contém apenas chuva, água, raízes e o trabalho de testar cada apoio.",
    "Você encontra rastros, fezes e pele trocada, mas nenhum animal permanece ao alcance da vista.",
    "Uma ilha muda de posição durante horas sem revelar criatura, morador ou ruína.",
    "A vegetação comum ocupa todo o caminho; reconhecer espécies não torna a coleta automaticamente segura.",
    "Nenhuma conversa ou batalha interrompe a marcha. Umidade e distância são os acontecimentos do período.",
    "Sinais de barco aparecem sem tripulação: uma estaca datada, corda molhada e marca recente de remo.",
    "Aves cruzam acima e peixes perturbam a água abaixo, longe demais para exigir decisão.",
    "Por quilômetros, Blackmarsh permanece ecossistema em vez de palco: viva, extensa e indiferente à pressa do viajante.",
)

