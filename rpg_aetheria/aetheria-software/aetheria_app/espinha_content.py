from __future__ import annotations

"""Dados espaciais, ecológicos, sociais e econômicos da Região 6 — Espinha do Mundo."""

from typing import Any


def _routes(noun: str) -> dict[str, list[str]]:
    return {
        "norte": [f"Seguir {noun} rumo ao norte", "Subir com o vento lateral para o norte", "Testar apoios antes de avançar ao norte"],
        "sul": [f"Acompanhar {noun} rumo ao sul", "Descer em zigue-zague para o sul", "Manter a parede à direita e seguir ao sul"],
        "leste": [f"Cruzar {noun} rumo a leste", "Contornar a escarpa pelo leste", "Seguir marcas de carga para leste"],
        "oeste": [f"Procurar continuidade em {noun} a oeste", "Avançar preso à linha de segurança para oeste", "Seguir o eco mais aberto a oeste"],
    }


ESPINHA_BIOMES: dict[str, dict[str, Any]] = {
    "cordilheira_monumental": {
        "name": "Cordilheira Monumental", "region": "espinha_do_mundo", "speed_kmh": 0.85, "temperature_delta": -16,
        "ambience": [
            "Picos atravessam as nuvens e retiram do horizonte qualquer escala familiar. O ar rarefeito obriga cada inspiração a participar da caminhada.",
            "Vento acima de cem quilômetros por hora varre neve solta e empurra o corpo para a borda; avançar exige três apoios antes de mover o quarto.",
            "Cristais de Luminite e Fractium emergem da rocha nua. A luz não aquece, mas revela rachaduras que continuam abrindo sob a neve.",
            "A gravidade mais fraca permite agulhas de pedra altas demais para parecerem estáveis, embora quedas continuem fatais.",
            "Líquen-de-Pico colore a face protegida das pedras. Onde ele termina de repente, gelo recente cobriu o paredão.",
            "Durante horas não há voz, fumaça ou construção: somente altitude, vento e o ruído distante de placas de gelo se acomodando.",
        ],
        "weather": ["vento de cume", "nevasca horizontal", "céu mineralmente claro", "nuvens abaixo da trilha", "geada seca", "silêncio antes da rajada"],
        "routes": _routes("uma aresta de rocha"),
        "flora": [
            ("Líquen-de-Pico", "crosta comestível apenas depois de fervida, usada para reconhecer faces abrigadas", True, False),
            ("Musgo-de-Gelo de Altitude", "almofadas densas armazenam água entre cristais", True, False),
            ("Flor-de-Neve Eterna", "pétalas translúcidas fecham antes de tempestades", False, False),
            ("Fungo-de-Pressium", "colônias minerais crescem em fendas de pressão e podem causar vertigem", False, True),
            ("Arbusto-Anão de Montanha", "galhos baixos fornecem fibra e combustível raro", True, False),
        ],
        "fauna": [
            ("Águia-das-Nuvens", "neutral", 2, "uma ave enorme usa correntes ascendentes sem bater as asas"),
            ("Cabra-das-Presas", "territorial", 3, "cascos encontram apoios invisíveis e chifres defendem a única passagem"),
            ("Urso-de-Montanha", "predator", 7, "um urso faminto fareja provisões através da neve"),
            ("Lobo-de-Altitude", "predator", 6, "uma alcateia economiza oxigênio e espera o viajante cansar"),
            ("Marmota-de-Rocha", "pacific", 0, "o alarme agudo precede deslocamentos de neve e predadores"),
            ("Dragão-de-Pedra Ancião", "legendary", 10, "uma crista inteira inspira sob gelo antigo"),
            ("Guardião de Pressium", "mystic", 8, "placas minerais redistribuem peso e fecham rotas instáveis"),
            ("Espírito-do-Vento", "mystic", 6, "uma voz muda de direção sem mudar de distância"),
        ],
        "landmarks": [
            ("Cume das Sete Pressões", "Sete agulhas de Pressium sustentam pontes e instrumentos meteorológicos."),
            ("Geleira do Martelo", "O gelo guarda ferramentas, corpos e uma estrada de outra era."),
            ("Ponte das Nuvens", "Cabos unem paredes separadas por uma garganta cujo fundo não aparece."),
            ("Coluna do Primeiro Pulso", "A pedra vibra no mesmo intervalo do coração de quem dorme perto."),
            ("Ninho dos Ventos", "Plataformas Luminari e Drakari acompanham migrações acima das nuvens."),
        ],
        "hazards": [
            ("Hipóxia", "Dor de cabeça, confusão e fraqueza surgem antes que a pessoa perceba a própria lentidão."),
            ("Cornija de Neve", "Uma extensão branca parece chão firme, mas projeta-se sobre o vazio."),
            ("Queda de Pedra", "O primeiro fragmento pequeno anuncia uma parede inteira em movimento."),
            ("Rajada de Pressium", "Vento e vibração mineral alteram equilíbrio e direção ao mesmo tempo."),
        ],
    },
    "vales_profundos": {
        "name": "Vales Profundos", "region": "espinha_do_mundo", "speed_kmh": 1.25, "temperature_delta": -7,
        "ambience": [
            "Paredes abruptas escondem o sol durante grande parte do dia. A sombra conserva gelo mesmo quando o ar acima aquece.",
            "Ecos de Resonum devolvem passos com intervalos incorretos; um som repetido pode vir de outra garganta ou de outra hora.",
            "A vegetação cabe em terraços estreitos: samambaias, musgo e arbustos de cobre disputam toda faixa onde a água não congela.",
            "Uma trilha que parece próxima pode exigir horas de descida e subida. Distância horizontal quase nunca mede o esforço real.",
            "Corvos-de-Eco repetem ferramentas, nomes e alarmes ouvidos nas vilas, confundindo comunicação e aviso.",
            "Pequenos rebanhos descem para água ao entardecer. A presença deles não elimina serpentes entre as pedras aquecidas.",
        ],
        "weather": ["sombra permanente", "vento canalizado", "neblina no fundo", "chuva fria localizada", "degelo distante", "eco de trovão"],
        "routes": _routes("um terraço estreito"),
        "flora": [
            ("Musgo-de-Sombra", "tapetes escuros revelam água lenta", True, False),
            ("Samambaia-de-Vale", "folhas resistentes ocupam terraços úmidos", True, False),
            ("Flor-de-Cristal", "flores rígidas refratam a pouca luz", False, False),
            ("Líquen-de-Eco", "colônias vibram quando vozes ou quedas se aproximam", False, False),
            ("Arbusto-de-Cobre", "raízes acumulam cobre e tornam a seiva imprópria sem tratamento", False, True),
        ],
        "fauna": [
            ("Cervo-de-Vale", "pacific", 0, "um cervo leve cruza terraços antes de beber"),
            ("Raposa-de-Montanha", "neutral", 2, "uma raposa segue cozinhas e acampamentos sem se aproximar"),
            ("Águia-de-Vale", "neutral", 2, "a ave usa a garganta como corredor de caça"),
            ("Serpente-de-Rocha", "predator", 5, "escamas minerais desaparecem entre pedras mornas"),
            ("Corvo-de-Eco", "mystic", 3, "a ave repete um pedido de socorro que pode ter semanas"),
            ("Eco-Vivo dos Vales", "mystic", 7, "uma resposta sem corpo aprende a voz de quem insiste"),
            ("Guardião de Vynium", "legendary", 9, "uma forma mineral protege a distribuição de peso do vale"),
            ("Sombra-dos-Vales", "predator", 7, "algo usa a noite precoce para acompanhar grupos feridos"),
        ],
        "landmarks": [
            ("Vale do Martelo", "Terraços agrícolas e forjas baixas dividem calor, água e trabalho."),
            ("Garganta das Vozes", "Resonum conserva discussões antigas em camadas de eco."),
            ("Mosteiro da Carga", "Ethari e Aureli medem como montanhas transferem peso."),
            ("Cemitério das Cordas", "Equipamentos rompidos registram expedições que não retornaram."),
            ("Portão de Pedra", "Uma estrada oriental alcança as terras áridas de Stonevale."),
        ],
        "hazards": [
            ("Cheia de Degelo", "Água de uma geleira distante ocupa o leito seco sem chuva local."),
            ("Eco Falso", "Um alarme repetido conduz na direção oposta à fonte atual."),
            ("Terraço Solto", "Raízes mantêm uma camada de solo que pode partir sob peso concentrado."),
            ("Sombra Fria", "A temperatura cai horas antes do pôr do sol e congela roupa molhada."),
        ],
    },
    "cavernas_gigantes": {
        "name": "Cavernas Gigantes", "region": "espinha_do_mundo", "speed_kmh": 0.95, "temperature_delta": -3,
        "ambience": [
            "A escuridão permanece completa entre colônias luminosas. Sem uma referência, teto, chão e distância parecem trocar de lugar.",
            "Cristais de Luminite iluminam galerias inteiras sem fonte externa; Harmonix transforma goteiras em acordes lentos.",
            "O ar úmido e parado conserva cerca de cinco graus, mas bolsões pobres em oxigênio apagam chama antes de causar tontura.",
            "Pilares naturais seriam montanhas na superfície. Pontes Ferrari e Aureli ocupam apenas uma fração do vazio.",
            "Fungos, musgos e Raízes-Cegas formam ecossistemas que nunca receberam luz solar. Colher demais altera alimento e ventilação.",
            "Batidas de mineração viajam por quilômetros. Uma sequência fora do turno pode ser pedido de ajuda, aviso estrutural ou imitação.",
        ],
        "weather": ["ar imóvel", "névoa mineral", "corrente de galeria", "goteira de degelo", "calor de forja", "silêncio de câmara selada"],
        "routes": _routes("uma galeria marcada"),
        "flora": [
            ("Fungo-Luminoso", "colônias azuis fornecem luz e alimento quando cultivadas", True, False),
            ("Musgo-de-Caverna", "tapetes úmidos filtram água de goteira", True, False),
            ("Flor-de-Luminite", "estruturas minerais abrem em ciclos de vibração", False, False),
            ("Líquen-de-Harmonix", "o líquen muda de cor conforme a frequência da rocha", False, False),
            ("Raiz-Cega", "raízes profundas ligam bolsões de água e podem ser tóxicas cruas", True, True),
        ],
        "fauna": [
            ("Morcego-Gigante de Caverna", "territorial", 5, "asas deslocam ar antes que o animal atravesse a luz"),
            ("Salamandra-Cega", "neutral", 1, "a pele pálida denuncia água sem contaminação recente"),
            ("Aranha-de-Cristal", "predator", 6, "fios transparentes cruzam a galeria na altura do peito"),
            ("Peixe-Cego", "pacific", 0, "cardumes percebem vibração em lagos subterrâneos"),
            ("Rato-de-Caverna", "neutral", 2, "roedores evitam bolsões de ar ruim e galerias ocupadas"),
            ("Guardião de Luminite", "legendary", 9, "um corpo de luz mineral protege a colônia que ventila a câmara"),
            ("Eco-Ancião", "mystic", 7, "uma consciência incompleta habita frequências de Harmonix"),
            ("Sombra-Vorath", "mystic", 8, "uma silhueta lembra a guerra, mas pode ser pessoa, defesa ou deformação"),
            ("Dragão-de-Caverna", "legendary", 10, "escamas fundidas à coluna convertem calor e movimento em estabilidade"),
        ],
        "landmarks": [
            ("Forja que Não Deveria Existir", "Uma fábrica antiga alimenta ventilação e também desperta o Meridiano."),
            ("Lago Harmônico", "Ondas repetem padrões mesmo quando nenhuma pedra toca a água."),
            ("Refúgio Velado", "Famílias Vorath, Aureli e Ferrari ocultaram uma cidade colaborativa por séculos."),
            ("Berço do Meridiano", "Arquivos físicos registram causas, ordens e omissões da Grande Fractura."),
            ("Coluna do Dragão", "Correntes de Pressium ligam uma criatura antiga ao teto de várias cidades."),
        ],
        "hazards": [
            ("Bolsa sem Oxigênio", "A chama diminui antes que pensamentos e movimentos fiquem lentos."),
            ("Ponte de Cristal", "A transparência oculta trincas e a profundidade abaixo."),
            ("Desabamento em Cadeia", "Uma extração distante muda a carga desta galeria."),
            ("Esporo Luminoso", "Luz intensa acompanha dormência e febre quando a colônia é perturbada."),
        ],
    },
}


ESPINHA_SETTLEMENTS: list[dict[str, Any]] = [
    {"id":"dhor_karun","name":"Dhor-Karun","type":"capital fortaleza","population":156000,"x":-260.0,"y":320.0,"radius_km":38.0,"scene_id":"r6_dhor_karun_portao_das_cargas","description":"Capital Aureli escavada em sete níveis, onde conselhos de mineração, ventilação e carga governam a montanha."},
    {"id":"cume_vyn","name":"Cume Vyn","type":"fortaleza de altitude","population":28000,"x":-820.0,"y":2240.0,"radius_km":18.0,"scene_id":"r6_cume_vyn_eclusa_do_ar","description":"Fortaleza acima das nuvens, dedicada a Pressium, meteorologia e resgate de altitude."},
    {"id":"ponte_nuvens","name":"Ponte das Nuvens","type":"cidade suspensa","population":19000,"x":760.0,"y":1900.0,"radius_km":16.0,"scene_id":"r6_ponte_nuvens_casa_dos_cabos","description":"Cidade construída em cabos, plataformas e paredes opostas de uma garganta monumental."},
    {"id":"vale_martelo","name":"Vale do Martelo","type":"cidade de vale","population":52000,"x":1120.0,"y":420.0,"radius_km":25.0,"scene_id":"r6_vale_martelo_terracos_de_degelo","description":"Terraços agrícolas, moinhos e forjas compartilham uma vazão curta e um inverno longo."},
    {"id":"ninho_alto","name":"Ninho Alto","type":"vila aérea","population":7800,"x":-1880.0,"y":1520.0,"radius_km":11.0,"scene_id":"r6_ninho_alto_plataforma_dos_ventos","description":"Vila Luminari e Drakari que observa migrações, tempestades e rotas acima das nuvens."},
    {"id":"forja_profunda","name":"Forja Profunda","type":"cidade industrial subterrânea","population":61000,"x":-620.0,"y":-1120.0,"radius_km":27.0,"scene_id":"r6_forja_profunda_elevador_termico","description":"Centro Ferrari e Aureli de fundição, ventilação e máquinas antigas alimentadas por calor subterrâneo."},
    {"id":"luminaria_baixa","name":"Luminária Baixa","type":"cidade de cavernas","population":34000,"x":720.0,"y":-1720.0,"radius_km":21.0,"scene_id":"r6_luminaria_baixa_jardim_de_fungos","description":"Cidade iluminada por fungos e Luminite, cercada por fazendas subterrâneas e regras rígidas de coleta."},
    {"id":"lago_harmonico","name":"Lago Harmônico","type":"porto subterrâneo","population":17000,"x":1760.0,"y":-980.0,"radius_km":16.0,"scene_id":"r6_lago_harmonico_cais_sem_vento","description":"Porto Aquari e Ninfari num lago cujas ondas e ecos regulam navegação e medicina."},
    {"id":"vigilia_branca","name":"Vigília Branca","type":"posto de fronteira","population":4200,"x":-1800.0,"y":2920.0,"radius_km":9.0,"scene_id":"r6_vigilia_branca_marco_da_neve","description":"Posto do passo setentrional que liga a Espinha às Presas de Gelo de Frostreach."},
    {"id":"portao_de_pedra","name":"Portão de Pedra","type":"posto de fronteira","population":6600,"x":2920.0,"y":-1180.0,"radius_km":10.0,"scene_id":"r6_portao_de_pedra_arco_oriental","description":"Entreposto oriental de caravanas, água e ferramentas na rota física para Stonevale."},
    {"id":"refugio_velado","name":"Refúgio Velado","type":"cidade oculta","population":11500,"x":-1960.0,"y":-2140.0,"radius_km":14.0,"scene_id":"r6_refugio_velado_porta_sem_brasao","description":"Cidade Vorath, Aureli e Ferrari ocultada depois da guerra, sustentada por colaboração e silêncio."},
]


ESPINHA_NPCS: list[dict[str, Any]] = [
    {"id":"mara_viga_clara","name":"Mara Viga-Clara","race":"Ferrari","role":"engenheira estrutural e possível companheira","home":"forja_profunda","faction":"oficina_da_carga_viva","x":-600.0,"y":-1100.0,"description":"uma Ferrari escuta tensões em pilares e procura libertar o dragão sem condenar cidades","values":["segurança","liberdade","prova"],"red_lines":["sacrificar trabalhador","manter escravidão por conveniência"]},
    {"id":"tarek_sem_ceu","name":"Tarek Sem-Céu","race":"Vorath","role":"cartógrafo do refúgio e possível companheiro","home":"refugio_velado","faction":"assembleia_do_refugio","x":-1940.0,"y":-2120.0,"description":"um jovem Vorath deseja reconhecimento público sem entregar famílias à vingança","values":["povo","verdade","autonomia"],"red_lines":["expor criança","apagar colaboração antiga"]},
    {"id":"dhoram_ferro_vivo","name":"Dhoram Ferro-Vivo","race":"Aureli","role":"Primeiro Mestre das Cargas","home":"dhor_karun","faction":"conselho_das_sete_cargas","x":-240.0,"y":340.0,"description":"um ancião Aureli sabe que a prosperidade depende de decisões enterradas","values":["continuidade","tradição","responsabilidade"],"red_lines":["colapso deliberado","destruir arquivo"]},
    {"id":"lia_passo_curto","name":"Lia Passo-Curto","race":"Humana","role":"mensageira de montanha","home":"vigilia_branca","faction":"correio_dos_passos","x":-1780.0,"y":2900.0,"description":"uma humana mede distância por abrigos e nunca promete chegada antes do clima","values":["entrega","honestidade","retorno"],"red_lines":["abandonar parceiro","falsificar rota"]},
    {"id":"silven_raiz_na_pedra","name":"Silven Raiz-na-Pedra","race":"Sylvani","role":"agricultor de terraços","home":"vale_martelo","faction":"comuna_do_degelo","x":1100.0,"y":440.0,"description":"um Sylvani mantém raízes vivas em paredes que recebem poucas horas de sol","values":["cultivo","água","continuidade"],"red_lines":["envenenar degelo","queimar terraço"]},
    {"id":"nami_onda_funda","name":"Nami Onda-Funda","race":"Aquari","role":"pilota do lago subterrâneo","home":"lago_harmonico","faction":"barqueiros_sem_vento","x":1780.0,"y":-960.0,"description":"uma Aquari navega por vibrações e correntes invisíveis","values":["tripulação","água limpa","resgate"],"red_lines":["afundar refugiado","contaminar lago"]},
    {"id":"sael_sol_na_neve","name":"Sael Sol-na-Neve","race":"Solari","role":"meteorologista de cume","home":"cume_vyn","faction":"observatorio_das_sete_pressoes","x":-800.0,"y":2260.0,"description":"uma Solari lê halos e cristais de gelo para prever vento","values":["método","alerta","clareza"],"red_lines":["reter previsão","simular resgate"]},
    {"id":"ivel_geada_lenta","name":"Ivel Geada-Lenta","race":"Glacari","role":"guia de aclimatação","home":"cume_vyn","faction":"casa_do_ar_lento","x":-840.0,"y":2220.0,"description":"um Glacari ensina o corpo a aceitar altitude sem transformar resistência em orgulho","values":["paciência","cuidado","ritmo"],"red_lines":["forçar aclimatação","abandonar hipóxico"]},
    {"id":"pali_asa_de_corda","name":"Pali Asa-de-Corda","race":"Luminari","role":"vigia de correntes aéreas","home":"ninho_alto","faction":"ninho_dos_ventos","x":-1860.0,"y":1540.0,"description":"uma Luminari plana entre plataformas e registra aves migratórias","values":["beleza","precisão","liberdade"],"red_lines":["cortar asa","enjaular migração"]},
    {"id":"garr_martelo_calmo","name":"Garr Martelo-Calmo","race":"Kragari","role":"chefe de resgate","home":"ponte_nuvens","faction":"brigada_das_cordas","x":780.0,"y":1880.0,"description":"um Kragari usa força para estabilizar cabos e nunca atravessa uma vítima sem ancoragem","values":["equipe","honra","proteção"],"red_lines":["duelo na ponte","abandonar caído"]},
    {"id":"zikka_pulso_fino","name":"Zikka Pulso-Fino","race":"Ziraki","role":"mecânica de ventilação","home":"forja_profunda","faction":"oficina_dos_foles","x":-640.0,"y":-1140.0,"description":"uma Ziraki constrói sensores simples para galerias onde instrumentos antigos mentem","values":["reparo","autoria","acesso"],"red_lines":["selar saída","roubar projeto"]},
    {"id":"nira_lago_escuro","name":"Nira Lago-Escuro","race":"Ninfari","role":"curadora subterrânea","home":"lago_harmonico","faction":"casa_das_aguas_fundas","x":1740.0,"y":-1000.0,"description":"uma Ninfari trata pulmões de mineiros e mapeia toxinas pela água","values":["cura","consentimento","pesquisa"],"red_lines":["teste forçado","negar tratamento"]},
    {"id":"umbra_sete_lampadas","name":"Umbra Sete-Lâmpadas","race":"Umbrari","role":"exploradora de galerias","home":"luminaria_baixa","faction":"vigias_da_escuridao","x":700.0,"y":-1700.0,"description":"uma Umbrari diferencia ausência de luz, emboscada e ar parado","values":["silêncio","orientação","retorno"],"red_lines":["apagar marca","deixar desaparecido"]},
    {"id":"kaar_escama_termica","name":"Kaar Escama-Térmica","race":"Drakari","role":"mediador com dragões","home":"ninho_alto","faction":"guardas_da_coluna","x":-1900.0,"y":1500.0,"description":"um Drakari percebe calor sob pedra e rejeita tratar dragões como máquinas","values":["dignidade","dever","memória"],"red_lines":["torturar dragão","quebrar juramento"]},
    {"id":"ethra_frequencia_baixa","name":"Ethra Frequência-Baixa","race":"Ethari","role":"pesquisadora de Harmonix","home":"luminaria_baixa","faction":"arquivo_do_meridiano","x":740.0,"y":-1740.0,"description":"uma Ethari ouve padrões simétricos que antecedem tremores","values":["conhecimento","harmonia","publicidade"],"red_lines":["falsificar dado","ocultar risco público"]},
    {"id":"toru_pe_de_rocha","name":"Toru Pé-de-Rocha","race":"Voraki","role":"cartógrafa sísmica","home":"portao_de_pedra","faction":"mapas_da_carga","x":2900.0,"y":-1160.0,"description":"uma Voraki sente vibração e prova que mineração recente rompeu amortecedores antigos","values":["território","evidência","reparação"],"red_lines":["culpar povo sem prova","minerar amortecedor"]},
    {"id":"orik_sem_turno","name":"Orik Sem-Turno","race":"Aureli","role":"representante dos mineiros","home":"dhor_karun","faction":"liga_dos_turnos","x":-280.0,"y":300.0,"description":"um Aureli organiza trabalhadores cuja segurança é tratada como custo","values":["trabalho","verdade","solidariedade"],"red_lines":["turno forçado","silenciar acidente"]},
]


ESPINHA_ROADS: list[dict[str, Any]] = [
    {"id":"estrada_das_sete_cargas","a":(-260.0,320.0),"b":(1120.0,420.0),"width_km":24.0},
    {"id":"trilha_do_cume","a":(-260.0,320.0),"b":(-820.0,2240.0),"width_km":18.0},
    {"id":"cabos_das_nuvens","a":(-820.0,2240.0),"b":(760.0,1900.0),"width_km":13.0},
    {"id":"rota_do_ninho","a":(-820.0,2240.0),"b":(-1880.0,1520.0),"width_km":12.0},
    {"id":"elevador_da_forja","a":(-260.0,320.0),"b":(-620.0,-1120.0),"width_km":22.0},
    {"id":"galeria_luminosa","a":(-620.0,-1120.0),"b":(720.0,-1720.0),"width_km":19.0},
    {"id":"canal_harmonico","a":(720.0,-1720.0),"b":(1760.0,-980.0),"width_km":16.0},
    {"id":"caminho_da_vigilia","a":(-820.0,2240.0),"b":(-1800.0,2920.0),"width_km":14.0},
    {"id":"estrada_oriental","a":(1120.0,420.0),"b":(2920.0,-1180.0),"width_km":20.0},
    {"id":"galeria_velada","a":(-620.0,-1120.0),"b":(-1960.0,-2140.0),"width_km":10.0},
]


ESPINHA_MARKETS: dict[str, dict[str, Any]] = {
    "dhor_karun":{"currency":"coroas","water_index":1.05,"stock":[("capacete de mina",12,5),("rações de líquen",6,3),("mapa de cargas",11,5)]},
    "cume_vyn":{"currency":"coroas","water_index":1.30,"stock":[("máscara de altitude",16,7),("grampos de Pressium",14,6),("manta de cume",12,5)]},
    "ponte_nuvens":{"currency":"coroas","water_index":1.25,"stock":[("corda trançada",10,4),("mosquetão Ferrari",15,7),("sinalizador de vento",8,3)]},
    "vale_martelo":{"currency":"coroas","water_index":0.90,"stock":[("pão de raiz",4,2),("odre de degelo",5,2),("martelo de viagem",9,4)]},
    "ninho_alto":{"currency":"coroas","water_index":1.35,"stock":[("capa de planagem",13,6),("luneta de névoa",17,8),("ração de altitude",7,3)]},
    "forja_profunda":{"currency":"coroas","water_index":1.10,"stock":[("picareta balanceada",15,7),("filtro de fuligem",9,4),("lanterna térmica",13,6)]},
    "luminaria_baixa":{"currency":"coroas","water_index":0.95,"stock":[("fungo luminoso",5,2),("máscara de esporos",10,4),("frasco de Luminite",14,6)]},
    "lago_harmonico":{"currency":"coroas","water_index":0.80,"stock":[("água mineral tratada",4,2),("remo de caverna",9,4),("tampão de Harmonix",8,3)]},
    "vigilia_branca":{"currency":"coroas","water_index":1.40,"stock":[("manta Glacari",14,6),("chá de aclimatação",8,3),("mapa de Frostreach",10,4)]},
    "portao_de_pedra":{"currency":"coroas","water_index":1.25,"stock":[("odre grande",8,3),("ração de Stonevale",7,3),("sapato de rocha",11,5)]},
    "refugio_velado":{"currency":"coroas","water_index":1.15,"stock":[("filtro Vorath",12,5),("tinta sem brilho",7,3),("chave de galeria",15,7)]},
}


ESPINHA_REGION_MAPS: dict[str, dict[str, Any]] = {
    "espinha_do_mundo": {
        "name":"Espinha do Mundo",
        "spawns": {
            "cordilheira_monumental":[(-1240.0,2320.0),(420.0,2480.0),(-2200.0,840.0)],
            "vales_profundos":[(920.0,720.0),(1860.0,260.0),(420.0,-360.0)],
            "cavernas_gigantes":[(-780.0,-1480.0),(840.0,-2140.0),(-2180.0,-1760.0)],
        },
        "borders": [
            {"id":"espinha_frostreach","axis":"y","limit":3000.0,"operator":">=","x_min":-2600.0,"x_max":-1300.0,"direction":"norte","target_region":"frostreach","target_biome":"presas_de_gelo","target_position":(-1800.0,-2960.0),"name":"Passo da Neve Vertical","description":"A cordilheira desce para geleiras abertas; marcos Glacari e Aureli anunciam Frostreach sem portão ou teleporte."},
            {"id":"espinha_stonevale","axis":"x","limit":3000.0,"operator":">=","y_min":-1900.0,"y_max":-650.0,"direction":"leste","target_region":"stonevale","target_biome":"platos_aridos","target_position":(-2960.0,-1180.0),"name":"Portão Oriental","description":"O vale se abre, a umidade desaparece e colunas minerais de Stonevale substituem os paredões da Espinha."},
        ],
    }
}


FROSTREACH_ESPINHA_BORDER = {"id":"frostreach_espinha","axis":"y","limit":-3000.0,"operator":"<=","x_min":-2600.0,"x_max":-1300.0,"direction":"sul","target_region":"espinha_do_mundo","target_biome":"cordilheira_monumental","target_position":(-1800.0,2960.0),"name":"Passo da Neve Vertical","description":"Geleiras tornam-se rampas de rocha e picos da Espinha ocupam todo o horizonte ao sul."}

STONEVALE_ESPINHA_BORDER = {"id":"stonevale_espinha","axis":"x","limit":-3000.0,"operator":"<=","y_min":-1900.0,"y_max":-650.0,"direction":"oeste","target_region":"espinha_do_mundo","target_biome":"vales_profundos","target_position":(2960.0,-1180.0),"name":"Portão de Pedra","description":"Os platôs cedem a vales cada vez mais fundos até que a estrada entra fisicamente na Espinha do Mundo."}


ESPINHA_PHASE_DETAILS = {
    "Madrugada":("Cristais e fungos fornecem luz insuficiente para medir distâncias.","O frio de cume atinge o mínimo e o ar parado das cavernas acumula fumaça.","Turnos de forja e resgate trocam relatórios antes do amanhecer."),
    "Amanhecer":("Luz toca primeiro os picos e demora horas para alcançar vales profundos.","Gelo recente revela pegadas antes que o vento as apague.","Mercados verificam estradas, elevadores e galerias antes de abrir."),
    "Manhã":("Correntes ascendentes fortalecem e aves deixam paredes abrigadas.","Trilhas movimentadas recebem carga; áreas selvagens continuam vazias por longos períodos.","Degelo começa nas faces iluminadas e aumenta risco de pedra solta."),
    "Tarde":("Nuvens envolvem os cumes e retiram o horizonte.","Vales ainda recebem algumas horas de trabalho e comércio.","Forjas profundas elevam ventilação quando o turno atinge maior calor."),
    "Entardecer":("A sombra sobe pelas paredes e congela água deixada em recipientes rasos.","Pontes recolhem cabos secundários e contam viajantes atrasados.","Morcegos deixam cavernas enquanto rebanhos procuram abrigo."),
    "Noite":("O vento encobre movimento e voz nas cristas.","Ecos viajam por galerias muito além de sua origem.","O Pulso na Pedra parece acompanhar o coração de quem tenta dormir."),
}


ESPINHA_QUIET_TRAVEL = (
    "Durante horas, nenhuma criatura ou pessoa aparece; vento, inclinação e respiração são os únicos acontecimentos.",
    "Líquen, musgo e rastros antigos ocupam o caminho, mas nada oferece missão, conversa ou recompensa imediata.",
    "Você atravessa uma sucessão de cornijas sem encontrar construção, apenas provas de erosão e gelo.",
    "O vale permanece vazio. Um corvo distante e água sob o gelo confirmam vida fora de alcance.",
    "A galeria continua por quilômetros entre fungos luminosos; batidas de mineração chegam sem revelar trabalhadores.",
    "Fezes, pelos e marcas de casco indicam fauna, embora nenhum animal permaneça à vista.",
    "A caminhada exige pausas de aclimatação e verificação de equipamento, não uma nova aventura a cada minuto.",
    "A Espinha permanece território colossal em vez de corredor entre cenas: antiga, habitada em pontos e vazia na maior parte.",
)
