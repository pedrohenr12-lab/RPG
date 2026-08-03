from __future__ import annotations

"""Dados espaciais, ecológicos e sociais da Região 3 — Arkanor."""

from typing import Any


ARKANOR_BIOMES: dict[str, dict[str, Any]] = {
    "planicies_ferteis": {
        "name": "Planícies Férteis",
        "region": "arkanor",
        "speed_kmh": 3.1,
        "temperature_delta": 0,
        "ambience": [
            "Campos de grão alcançam o horizonte, interrompidos por sebes, canais e árvores usadas como marcos de propriedade.",
            "O vento percorre a grama em faixas largas; cada mudança de cor pode ser animal, trabalhador ou apenas relevo.",
            "Espantalhos trazem placas em alfabetos diferentes, sinais de que nem todos os campos pertencem ao mesmo povo.",
            "Rodas de carroça deixam sulcos paralelos, mas algumas estradas terminam em porteiras vigiadas.",
            "O solo escuro retém umidade sob a superfície; acima dele, poeira fina cobre botas e folhas baixas.",
            "Torres de grão e fumaças rurais aparecem longe. A visibilidade facilita orientação e também torna viajantes visíveis.",
        ],
        "weather": [
            "vento constante", "céu claro e frio", "chuva sazonal", "calor moderado",
            "nuvens baixas", "poeira depois da passagem de carroças",
        ],
        "routes": {
            "norte": ["Seguir os canais de irrigação ao norte", "Acompanhar a estrada dos celeiros ao norte", "Avançar contra o vento rumo ao norte"],
            "sul": ["Cruzar campos já colhidos para o sul", "Seguir marcos de pedra ao sul", "Acompanhar carroças rumo ao sul"],
            "leste": ["Manter o Rio Aurenta à distância e seguir leste", "Contornar propriedades rumo a leste", "Seguir a sombra das torres para leste"],
            "oeste": ["Acompanhar uma sebe antiga para oeste", "Seguir terrenos de pousio a oeste", "Procurar colinas no horizonte oeste"],
        },
        "flora": [
            ("Trigo-Dourado de Arkanor", "espigas altas refletem luz sem esconder que o cultivo pertence a alguém", True, False),
            ("Grama-Alta das Planícies", "faixas não cultivadas abrigam insetos, lebres e ninhos", True, False),
            ("Arbusto-de-Fruto-Solar", "bagas maduras crescem junto a uma cerca marcada", True, False),
            ("Flor-do-Aurenta", "pétalas douradas indicam solo úmido perto de um canal", False, False),
            ("Girassol-Simétrico", "flores acompanham o sol em ângulos quase idênticos", False, False),
            ("Raiz-de-Cálcio", "folhas baixas escondem uma raiz medicinal profunda", False, False),
        ],
        "fauna": [
            ("Cavalo-de-Arkanor", "pacific", 1, "um pequeno grupo pasta usando arreios quebrados, talvez separado de alguma caravana"),
            ("Boi-das-Planícies", "territorial", 2, "um animal de trabalho sem condutor protege a passagem entre duas cercas"),
            ("Lebre-Dourada", "pacific", 0, "orelhas surgem acima do trigo antes que o corpo atravesse a trilha"),
            ("Águia-Real de Arkanor", "predator", 3, "uma sombra larga repete círculos sobre animais pequenos"),
            ("Raposa-das-Planícies", "neutral", 1, "uma caçadora observa os canais antes de procurar roedores"),
            ("Cervo-Comum", "pacific", 1, "um rebanho usa faixas de terra entre propriedades"),
            ("Falcão-do-Vento", "neutral", 2, "a ave carrega uma correia de treinamento sem dono à vista"),
            ("Leão-de-Campo", "predator", 5, "a grama dobra contra o vento sob o peso de um felino que não mostra a cabeça"),
            ("Titã-das-Planícies", "legendary", 7, "ao longe, algo alto demais desloca aves e faz a terra vibrar em intervalos longos"),
        ],
        "landmarks": [
            ("Campos Dourados", "Cultivos de proprietários diferentes formam um mosaico visível somente de terreno alto."),
            ("Estrada Real do Meio", "Pedras compactadas suportam comboios, patrulhas e cobradores de pedágio."),
            ("Celeiro das Doze Portas", "Um armazém monumental recebe grãos de comunidades que não usam a mesma moeda."),
            ("Marco da Terra Afundada", "Uma pedra antiga registra nomes de famílias humanas que chegaram pelo mar."),
            ("Canal de Botanium", "Água de irrigação percorre divisões calculadas e vigiadas."),
        ],
        "hazards": [
            ("Incêndio de Colheita", "Fumaça baixa corre mais rápido que uma pessoa entre fileiras secas."),
            ("Touro sem Condutor", "Um animal assustado bloqueia a única abertura da cerca."),
            ("Carroça Desgovernada", "Uma roda quebrada lança carga e madeira pela estrada inclinada."),
            ("Patrulha Desconfiada", "Guardas confundem falta de documentos com intenção criminosa."),
        ],
    },
    "colinas_suaves": {
        "name": "Colinas Suaves",
        "region": "arkanor",
        "speed_kmh": 2.5,
        "temperature_delta": -1,
        "ambience": [
            "Morros sucessivos escondem estradas, casas e rebanhos até o último trecho da subida.",
            "Muros baixos de pedra separam vinhedos, pastos e bosques sem formar uma linha reta.",
            "O vento traz cheiro de uva, lenha e chuva antes de revelar qualquer construção.",
            "Tocas profundas transformam encostas firmes em terreno que pode ceder sob peso concentrado.",
            "Rochas circulares aparecem entre carvalhos; algumas são marcos, outras pertencem a ruínas mais antigas.",
            "Sinos de propriedades rurais viajam entre vales, mas a origem muda a cada elevação.",
        ],
        "weather": ["garoa de colina", "vento oeste", "sol entre nuvens", "névoa nos vales", "noite fria", "chuva curta"],
        "routes": {
            "norte": ["Usar cristas baixas rumo ao norte", "Seguir vinhedos para o norte", "Acompanhar marcos circulares ao norte"],
            "sul": ["Descer entre muros de pedra para o sul", "Seguir o vale mais aberto ao sul", "Contornar bosques rumo ao sul"],
            "leste": ["Atravessar pomares em direção a leste", "Seguir o som de água a leste", "Usar uma estrada de carga rumo a leste"],
            "oeste": ["Subir pelas rochas para oeste", "Seguir carvalhos espaçados a oeste", "Acompanhar rastros de rebanho rumo a oeste"],
        },
        "flora": [
            ("Carvalho-Suave", "galhos largos protegem o solo do vento", False, False),
            ("Arbusto-de-Fruto-Doce", "frutos escuros crescem entre pedras de uma divisão rural", True, False),
            ("Musgo-de-Colina", "círculos verdes cobrem a face norte das rochas", False, False),
            ("Flor-de-Pedra Circular", "pétalas rígidas ocupam uma fenda com Orbitium", False, False),
            ("Erva-de-Fonte", "folhas aromáticas indicam água próxima", False, False),
            ("Vinhas-de-Colina", "fileiras cultivadas seguem curvas de nível", True, False),
            ("Grama-Curta de Vale", "pastos naturais conservam marcas de cascos", True, False),
        ],
        "fauna": [
            ("Javali-Comum", "territorial", 3, "um grupo revira solo junto a um muro e fecha a passagem"),
            ("Texugo-de-Arkanor", "territorial", 2, "terra fresca marca uma rede de tocas ocupadas"),
            ("Lebre-de-Morro", "pacific", 0, "uma lebre usa os muros como cobertura entre corridas"),
            ("Falcão-Circular", "predator", 2, "a ave repete a mesma curva sobre uma formação rochosa"),
            ("Cobra-de-Colina", "neutral", 1, "uma serpente sem veneno absorve calor na trilha"),
            ("Urso-das-Colinas", "territorial", 4, "marcas de garras e frutas esmagadas indicam um animal próximo"),
            ("Predador-Espiral", "mystic", 5, "rastros circulam o acampamento sem jamais cruzar a própria linha"),
        ],
        "landmarks": [
            ("Círculo de Orbitium", "Rochas formam uma medida perfeita que nenhum proprietário admite ter construído."),
            ("Vinhedos das Colinas", "Propriedades antigas usam variedades, contratos e tradições diferentes."),
            ("Tocas de Arkanor", "Galerias naturais e artificiais se confundem sob as encostas."),
            ("Mosteiro da Balança Vazia", "Copistas registram pesos e dívidas, mas não aceitam previsões como pagamento."),
            ("Estrada dos Sete Muros", "Cada trecho pertenceu a uma família, guilda ou exército diferente."),
        ],
        "hazards": [
            ("Encosta Oca", "O som sob seus passos revela galerias incapazes de sustentar mais peso."),
            ("Javalis Acuados", "Filhotes ficam entre você e adultos que já perceberam sua presença."),
            ("Pedágio Falso", "Homens armados usam selos antigos para cobrar uma estrada que não controlam."),
            ("Névoa de Vale", "A próxima colina desaparece e todos os sinos parecem vir da mesma direção."),
        ],
    },
    "vales_verdes": {
        "name": "Vales Verdes",
        "region": "arkanor",
        "speed_kmh": 2.0,
        "temperature_delta": 0,
        "ambience": [
            "O Rio Aurenta ocupa o fundo do vale e transforma margens, ilhas e portos conforme a estação.",
            "Salgueiros escondem barcos pequenos; cordas e marcas de nível revelam uso humano frequente.",
            "Água de cascatas permanece suspensa no ar como névoa e mantém rochas cobertas de musgo.",
            "Canais navegáveis aproximam cidades, mas penhascos e curvas isolam trechos por quilômetros.",
            "Pássaros mergulham onde peixes se concentram; redes abandonadas indicam correnteza perigosa.",
            "Pontes, balsas e barcos oferecem caminhos diferentes, cada um com dono, horário e preço.",
        ],
        "weather": ["névoa de rio", "chuva no vale", "sol úmido", "vento de cascata", "céu encoberto", "noite amena"],
        "routes": {
            "norte": ["Subir o Aurenta rumo ao norte", "Usar a margem alta para o norte", "Seguir salgueiros marcados ao norte"],
            "sul": ["Descer com a corrente para o sul", "Seguir caminhos de pescadores ao sul", "Acompanhar barcos rumo ao sul"],
            "leste": ["Cruzar uma ponte de serviço para leste", "Seguir cascatas rumo a leste", "Contornar a margem para leste"],
            "oeste": ["Subir uma trilha fluvial a oeste", "Acompanhar canais de moinho a oeste", "Procurar terreno alto rumo a oeste"],
        },
        "flora": [
            ("Salgueiro-do-Aurenta", "galhos flexíveis quase tocam a corrente", False, False),
            ("Lírio-d'Água Verde", "folhas largas criam abrigo para peixes pequenos", False, False),
            ("Musgo-de-Cascata", "colônias densas conservam água em pedras verticais", False, False),
            ("Samambaia-de-Vale", "folhas longas ocupam margens protegidas", False, False),
            ("Flor-de-Água-Pura", "uma flor rara cresce onde Aquanium se concentra", False, False),
            ("Vinhas-de-Rio", "frutos pequenos sobem por salgueiros e pilares", True, False),
            ("Grama-de-Margem", "raízes estabilizam a curva externa do rio", True, False),
        ],
        "fauna": [
            ("Lontra-do-Aurenta", "pacific", 1, "uma família quebra conchas numa pedra de uso repetido"),
            ("Peixe-Prateado", "pacific", 0, "cardumes refletem luz sob uma ponte"),
            ("Garça-Verde", "neutral", 1, "a ave permanece imóvel junto a águas rasas"),
            ("Sapo-de-Vale", "pacific", 0, "cantos diferentes marcam margens e profundidades"),
            ("Cobra-d'Água", "neutral", 1, "uma serpente corta a superfície sem se aproximar"),
            ("Martim-Pescador", "neutral", 1, "uma ave colorida repete mergulhos perto de uma corredeira"),
            ("Libélula-Circular", "mystic", 1, "o inseto nunca completa a volta no mesmo ponto"),
            ("Lontra-Predadora", "predator", 3, "uma forma maior expulsa as lontras comuns de uma enseada"),
            ("Guardião-das-Águas", "legendary", 7, "a corrente sobe contra a gravidade ao redor de uma silhueta submersa"),
        ],
        "landmarks": [
            ("Porto do Aurenta", "Guindastes, balsas e mercados conectam vales e regiões distantes."),
            ("Cascatas Verdes", "Quedas sucessivas alimentam musgos, moinhos e canais de distribuição."),
            ("Nascente Pura", "Curandeiros e comunidades disputam proteção sem concordar sobre propriedade."),
            ("Ponte dos Sete Arcos", "Arcos de épocas diferentes sustentam uma mesma travessia comercial."),
            ("Ilha dos Barqueiros", "Casas flutuantes mudam de posição conforme tarifas e correnteza."),
        ],
        "hazards": [
            ("Cheia Súbita", "Galhos, barris e água turva ocupam a margem em poucos minutos."),
            ("Rede Submersa", "Cordas abandonadas prendem pernas e remos sob a superfície."),
            ("Balsa sem Cabo", "Uma plataforma carregada perde o controle no trecho mais rápido."),
            ("Cobradores do Rio", "Homens armados exigem documento que pescadores locais dizem não existir."),
        ],
    },
}


ARKANOR_SETTLEMENTS: list[dict[str, Any]] = [
    {"id":"cidade_arkanor","name":"Cidade de Arkanor","type":"capital","population":420000,"x":0.0,"y":1180.0,"radius_km":42.0,"scene_id":"r3_arkanor_portao_sul","description":"Capital do Pacto Dourado, dividida entre palácio, assembleia mercantil, universidades, tribunais, guildas e bairros de muitas raças."},
    {"id":"porto_aurenta","name":"Porto do Aurenta","type":"cidade fluvial","population":112000,"x":1120.0,"y":720.0,"radius_km":30.0,"scene_id":"r3_porto_aurenta_cais","description":"Cidade de cais, armazéns, estaleiros e pontes onde o rio transforma informação em mercadoria."},
    {"id":"alvacampo","name":"Alvacampo","type":"cidade agrícola","population":68000,"x":-920.0,"y":1680.0,"radius_km":25.0,"scene_id":"r3_alvacampo_portao","description":"Centro de grãos e trabalho rural, rico em celeiros e marcado por dívidas de terra."},
    {"id":"sete_arcos","name":"Sete Arcos","type":"cidade-ponte","population":31000,"x":720.0,"y":1450.0,"radius_km":19.0,"scene_id":"r3_sete_arcos_ponte","description":"Entreposto erguido ao redor de pontes de épocas diferentes e pedágios concorrentes."},
    {"id":"vinhedos_orbel","name":"Vinhedos de Orbel","type":"vila de colina","population":9400,"x":-1340.0,"y":540.0,"radius_km":12.0,"scene_id":"r3_orbel_estrada","description":"Vila de produtores, arrendatários e adegas onde safras antigas sustentam poder político."},
    {"id":"campos_dourados","name":"Campos Dourados","type":"vila agrícola","population":7600,"x":-340.0,"y":2050.0,"radius_km":10.0,"scene_id":"r3_campos_dourados_marco","description":"Comunidade cercada por grandes propriedades, canais de irrigação e trabalhadores sazonais."},
    {"id":"salgueiral","name":"Salgueiral","type":"vila ribeirinha","population":5200,"x":1450.0,"y":-180.0,"radius_km":9.0,"scene_id":"r3_salgueiral_trapiche","description":"Vila de pesca, cestos e pequenas balsas protegida por salgueiros antigos."},
    {"id":"nascente_serena","name":"Nascente Serena","type":"comunidade de cura","population":1800,"x":820.0,"y":-960.0,"radius_km":7.0,"scene_id":"r3_nascente_serena_entrada","description":"Comunidade multirracial que cuida de uma fonte de Aquanium e resiste à privatização da água."},
    {"id":"mercado_horizonte","name":"Mercado do Horizonte","type":"cidade de estrada","population":24000,"x":-280.0,"y":2600.0,"radius_km":16.0,"scene_id":"r3_mercado_horizonte_portico","description":"Último grande mercado ao norte, abastecendo caravanas entre Arkanor e Eldorwood."},
    {"id":"vigilia_verde","name":"Vigília Verde","type":"posto de fronteira","population":2100,"x":430.0,"y":2940.0,"radius_km":8.0,"scene_id":"r3_vigilia_verde_cancela","description":"Posto aberto junto à fronteira úmida de Eldorwood, ocupado por guardas, boticários e guias."},
    {"id":"balanca_baixa","name":"Balança Baixa","type":"bairro extramuros","population":17000,"x":90.0,"y":1070.0,"radius_km":13.0,"scene_id":"r3_balanca_baixa_praca","description":"Bairro de refugiados, diaristas e ofícios não reconhecidos pelas guildas da capital."},
]


ARKANOR_NPCS: list[dict[str, Any]] = [
    {"id":"liora_sen","name":"Liora Sen","race":"Humana","role":"pesquisadora do Manuscrito","home":"cidade_arkanor","faction":"universidade_aberta","x":20.0,"y":1200.0,"description":"uma pesquisadora humana protege anotações com o corpo quando agentes do Conclave atravessam a praça","values":["prova","acesso público","consentimento"],"red_lines":["teste humano forçado","destruir registro"]},
    {"id":"astreon_vale","name":"Astreon Vale","race":"Ethari","role":"estrategista do Conclave","home":"cidade_arkanor","faction":"conclave_meridiano","x":-20.0,"y":1220.0,"description":"um Ethari translúcido mede distâncias entre pessoas antes de oferecer uma conversa privada","values":["previsão","estabilidade","conhecimento"],"red_lines":["desperdício de dados","violência sem cálculo"]},
    {"id":"odelia_arkan","name":"Odelia Arkan","race":"Humana","role":"regente do Pacto Dourado","home":"cidade_arkanor","faction":"regencia_arkanor","x":0.0,"y":1260.0,"description":"a regente escuta três assessores enquanto lê uma petição que nenhum deles mencionou","values":["paz","comércio","continuidade"],"red_lines":["guerra civil","ameaça ao abastecimento"]},
    {"id":"sorel_folha_livre","name":"Sorel Folha-Livre","race":"Sylvani","role":"advogado de migrantes","home":"balanca_baixa","faction":"assembleia_da_rua","x":100.0,"y":1080.0,"description":"um Sylvani organiza contratos por tipo de abuso, não por espécie de papel","values":["acolhimento","autonomia","lei pública"],"red_lines":["trabalho escravo","deportação coletiva"]},
    {"id":"bren_ferro_claro","name":"Bren Ferro-Claro","race":"Aureli","role":"inspetora de pesos","home":"sete_arcos","faction":"casa_das_medidas","x":710.0,"y":1450.0,"description":"uma Aureli recalibra uma balança antes de acusar um comerciante","values":["precisão","trabalho","reparação"],"red_lines":["fraude de alimento","suborno técnico"]},
    {"id":"nami_tres_correntes","name":"Nami Três-Correntes","race":"Aquari","role":"capitã fluvial","home":"porto_aurenta","faction":"coro_de_navegadores","x":1100.0,"y":700.0,"description":"uma Aquari calcula corrente, carga e humor da tripulação antes de aceitar passageiros","values":["fluxo livre","tripulação","acordo"],"red_lines":["contaminar rio","abandonar marinheiro"]},
    {"id":"ihra_sol_baixo","name":"Ihra Sol-Baixo","race":"Solari","role":"astrônoma agrícola","home":"campos_dourados","faction":"calendario_das_safras","x":-350.0,"y":2040.0,"description":"uma Solari compara sombras dos girassóis com datas riscadas num bastão","values":["ciclo","previsão honesta","alimento"],"red_lines":["falsificar clima","queimar safra"]},
    {"id":"iven_neve_mansa","name":"Iven Neve-Mansa","race":"Glacari","role":"médico itinerante","home":"vigilia_verde","faction":"vigias_da_fronteira","x":440.0,"y":2920.0,"description":"o médico Glacari reconhece viajantes vindos de Eldorwood pela umidade nas roupas","values":["cuidado","travessia livre","prudência"],"red_lines":["abandonar exposto","fechar fronteira por raça"]},
    {"id":"piri_luz_de_bolso","name":"Piri Luz-de-Bolso","race":"Luminari","role":"mensageira judicial","home":"cidade_arkanor","faction":"correio_dos_tribunais","x":40.0,"y":1160.0,"description":"uma Luminari carrega intimações, cartas de amor e recursos legais em bolsas separadas","values":["entrega","beleza","palavra dada"],"red_lines":["interceptar carta","enjaular mensageiro"]},
    {"id":"grom_ceifa_justa","name":"Grom Ceifa-Justa","race":"Kragari","role":"organizador de trabalhadores","home":"alvacampo","faction":"liga_dos_ceifadores","x":-900.0,"y":1660.0,"description":"um Kragari distribui água antes de iniciar uma reunião sobre pagamento","values":["honra","salário","proteção"],"red_lines":["reter comida","agredir trabalhador"]},
    {"id":"zizi_roda_torta","name":"Zizi Roda-Torta","race":"Ziraki","role":"mecânica de carroças","home":"mercado_horizonte","faction":"oficios_livres","x":-260.0,"y":2590.0,"description":"uma Ziraki diagnostica uma roda pelo som e cobra apenas depois de mostrar a rachadura","values":["invenção","troca justa","autoria"],"red_lines":["roubar projeto","culpar aprendiz"]},
    {"id":"mera_salgueiro","name":"Mera Salgueiro","race":"Ninfari","role":"guardiã de margem","home":"salgueiral","faction":"confluencia","x":1440.0,"y":-160.0,"description":"uma Ninfari mede erosão com os pés na água e marcas no tronco","values":["água","comunidade","memória"],"red_lines":["privatizar nascente","destruir berçário"]},
    {"id":"vesh_tinta_escura","name":"Vesh Tinta-Escura","race":"Umbrari","role":"investigador independente","home":"balanca_baixa","faction":"arquivo_da_lanterna","x":70.0,"y":1090.0,"description":"um Umbrari lê contratos à sombra e destaca cláusulas que ninguém pretendia explicar","values":["segredo responsável","prova","sobrevivência"],"red_lines":["expor fonte","fabricar confissão"]},
    {"id":"doma_sete_arcos","name":"Doma Sete-Arcos","race":"Ferrari","role":"engenheira de pontes","home":"sete_arcos","faction":"mestres_de_ponte","x":730.0,"y":1470.0,"description":"uma Ferrari testa vibrações enquanto carroças continuam atravessando","values":["segurança","responsabilidade","manutenção"],"red_lines":["ocultar rachadura","sobrecarregar ponte"]},
    {"id":"kaar_escama_cobre","name":"Kaar Escama-de-Cobre","race":"Drakari","role":"guarda de testemunhas","home":"cidade_arkanor","faction":"tribunal_do_pacto","x":10.0,"y":1140.0,"description":"um Drakari mantém a mão perto da arma e o corpo entre a testemunha e a multidão","values":["dever","proteção","testemunho"],"red_lines":["ameaçar criança","executar sem julgamento"]},
    {"id":"tavar_solo_aberto","name":"Tavar Solo-Aberto","race":"Voraki","role":"agrimensor rural","home":"vinhedos_orbel","faction":"cartografos_da_aurora","x":-1320.0,"y":560.0,"description":"um Voraki sente estacas enterradas e encontra limites movidos durante a noite","values":["território","precisão","acesso"],"red_lines":["roubar terra","apagar marco"]},
    {"id":"eloa_pedra_do_ceu","name":"Eloa Pedra-do-Céu","race":"Ethari","role":"curadora da Nascente","home":"nascente_serena","faction":"circulo_da_agua_clara","x":800.0,"y":-940.0,"description":"uma Ethari compara pulsações da água com a respiração de pacientes","values":["cura","harmonia","consentimento"],"red_lines":["vender água sagrada","experimentar sem permissão"]},
]


ARKANOR_ROADS: list[dict[str, Any]] = [
    {"id":"estrada_real_norte","a":(0.0,1180.0),"b":(430.0,2940.0),"width_km":28.0},
    {"id":"rota_dos_celeiros","a":(-920.0,1680.0),"b":(0.0,1180.0),"width_km":22.0},
    {"id":"rota_do_horizonte","a":(-920.0,1680.0),"b":(-280.0,2600.0),"width_km":18.0},
    {"id":"estrada_dos_vinhedos","a":(-1340.0,540.0),"b":(0.0,1180.0),"width_km":16.0},
    {"id":"rota_dos_sete_arcos","a":(0.0,1180.0),"b":(720.0,1450.0),"width_km":20.0},
    {"id":"rota_fluvial_aurenta","a":(720.0,1450.0),"b":(1120.0,720.0),"width_km":26.0},
    {"id":"aurenta_sul","a":(1120.0,720.0),"b":(820.0,-960.0),"width_km":24.0},
    {"id":"estrada_de_salgueiral","a":(1120.0,720.0),"b":(1450.0,-180.0),"width_km":15.0},
]


ARKANOR_REGION_MAPS: dict[str, dict[str, Any]] = {
    "arkanor": {
        "name": "Arkanor",
        "spawns": {
            "planicies_ferteis": [(-620.0, 1880.0), (260.0, 2140.0), (-1060.0, 1320.0)],
            "colinas_suaves": [(-1580.0, 380.0), (-980.0, 820.0), (-420.0, -260.0)],
            "vales_verdes": [(1260.0, 420.0), (940.0, -720.0), (1580.0, -420.0)],
        },
        "borders": [
            {
                "id":"arkanor_eldorwood","axis":"y","limit":3000.0,"operator":">=",
                "x_min":-1100.0,"x_max":1600.0,"direction":"norte",
                "target_region":"eldorwood","target_biome":"pantanos_rios","target_position":(430.0,-1540.0),
                "name":"Fronteira dos Campos Úmidos",
                "description":"Canais agrícolas tornam-se cursos naturais, o trigo cede a juncos e raízes, e a névoa de Eldorwood ocupa o horizonte norte.",
            }
        ],
    }
}


ELDORWOOD_ARKANOR_BORDER = {
    "id":"eldorwood_arkanor","axis":"y","limit":-1600.0,"operator":"<=",
    "x_min":-1100.0,"x_max":1600.0,"direction":"sul",
    "target_region":"arkanor","target_biome":"planicies_ferteis","target_position":(430.0,2960.0),
    "name":"Fronteira dos Primeiros Campos",
    "description":"A água se divide em canais medidos, árvores antigas cedem a plantações e marcos de propriedade anunciam Arkanor sem muralha ou portal.",
}


ARKANOR_PHASE_DETAILS = {
    "Madrugada": ("Estradas permanecem vazias, mas fornos rurais e guardas já trabalham.", "Névoa ocupa vales e canais enquanto campos abertos recebem primeiro a luz.", "Animais noturnos deixam plantações antes da chegada dos trabalhadores."),
    "Amanhecer": ("Carroças partem antes dos mercados e tornam as rotas principais mais visíveis.", "Sinos de propriedades marcam horários diferentes para trabalho e oração.", "A luz revela poeira, pegadas e limites de terra que a noite escondia."),
    "Manhã": ("Estradas próximas a cidades acumulam mercadores, patrulhas, aprendizes e diaristas.", "Nos trechos distantes, vento e cultivo ainda dominam horas inteiras.", "Barcos aproveitam corrente e pontes começam a cobrar pedágio."),
    "Tarde": ("O calor aumenta sobre campos abertos e trabalhadores procuram água e sombra.", "Tribunais, mercados e guildas recebem as últimas demandas do dia.", "Tempestades curtas podem interromper colheita, estrada e navegação."),
    "Entardecer": ("Portões calculam quem entra antes do fechamento e estalagens aumentam preços.", "Rebanhos retornam, carroças procuram pátios e patrulhas trocam turno.", "Luzes de cidades parecem próximas muito antes de a estrada alcançá-las."),
    "Noite": ("Estradas perdem movimento regular e ganham contrabandistas, vigias e animais.", "Bairros e portos continuam ativos, mas regras mudam depois do toque de recolher.", "Fora de cidades, o céu aberto ajuda orientação e expõe qualquer fogueira."),
}


ARKANOR_QUIET_TRAVEL = (
    "O trecho contém apenas cultivo, vento e trabalho distante; ninguém abandona a rotina por sua passagem.",
    "Você cruza marcas antigas de carroça e pegadas recentes, mas não alcança seus autores.",
    "Uma torre permanece no horizonte durante horas, crescendo devagar demais para parecer chegada.",
    "Animais pequenos usam sebes e canais; nenhum deles exige uma decisão imediata.",
    "A estrada continua sem encontro. Distância, sede e posição do sol são os acontecimentos do período.",
    "Você vê casas longe da rota e decide não invadir propriedades apenas para confirmar que estão ocupadas.",
    "Sinais de civilização permanecem presentes sem produzir conversa, missão ou conflito.",
    "O vale oferece água, plantas comuns e vozes distantes, mas nada raro acontece neste trecho.",
)
