from __future__ import annotations

"""Dados espaciais, ecológicos, sociais e econômicos da Região 4 — Stonevale."""

from typing import Any


STONEVALE_BIOMES: dict[str, dict[str, Any]] = {
    "platos_aridos": {
        "name": "Platôs Áridos",
        "region": "stonevale",
        "speed_kmh": 2.6,
        "temperature_delta": 9,
        "ambience": [
            "Lajes nuas se prolongam por dezenas de quilômetros; sob o sol, veios de Silicyn transformam o chão numa superfície clara demais para encarar por muito tempo.",
            "O vento atravessa colunas de pedra e produz notas baixas. Algumas respondem antes que a rajada chegue, como se o relevo antecipasse o próprio som.",
            "Fendas estreitas guardam sombra, raízes e fezes secas de pequenos animais. Fora delas, calor e distância dominam tudo que os olhos alcançam.",
            "Formações de Patterium repetem o mesmo ângulo em escalas diferentes; à distância parecem ruínas, mas não há porta, fumaça ou movimento humano.",
            "Cristais quebrados estalam durante a dilatação da rocha. O ruído viaja pelo platô e pode ser confundido com passos de algo muito maior.",
            "A gravidade mais fraca permite arcos naturais altos e delgados, embora a superfície esfarelada ainda possa ceder sob uma bota mal apoiada.",
        ],
        "weather": ["sol branco e vento seco", "poeira de cristal", "calor imóvel", "nuvens altas sem chuva", "vento de leste", "noite rapidamente fria"],
        "routes": {
            "norte": ["Seguir as sombras curtas rumo ao norte", "Acompanhar uma fileira de pedras de rota ao norte", "Avançar entre arcos naturais para o norte"],
            "sul": ["Procurar fendas com vegetação ao sul", "Descer por lajes inclinadas ao sul", "Seguir o brilho de uma salina ao sul"],
            "leste": ["Cruzar o campo de Silicyn para leste", "Acompanhar o eco mais grave rumo a leste", "Contornar colunas fraturadas a leste"],
            "oeste": ["Seguir marcas de caravana para oeste", "Manter o sol às costas e avançar a oeste", "Procurar o posto de fronteira no horizonte oeste"],
        },
        "flora": [
            ("Cacto-de-Cristal", "placas translúcidas armazenam água protegida por espinhos minerais", True, False),
            ("Arbusto-de-Pedra", "galhos cinzentos se confundem com fragmentos de rocha", False, False),
            ("Flor-do-Deserto", "pétalas abrem somente nas horas menos quentes", False, False),
            ("Líquen-de-Quartzo", "colônias pálidas marcam a face sombreada das pedras", False, False),
            ("Grama-de-Fenda", "folhas duras denunciam umidade retida sob a laje", True, False),
            ("Raiz-de-Pressium", "uma raiz medicinal cresce onde a pedra sofre compressão", False, False),
        ],
        "fauna": [
            ("Lagarto-de-Cristal", "neutral", 1, "um réptil translúcido regula a temperatura alternando sombra e pedra quente"),
            ("Águia-do-Platô", "predator", 3, "uma ave larga acompanha sombras de roedores sem se aproximar de você"),
            ("Serpente-de-Areia", "predator", 4, "um sulco recente termina sob cascalho; o veneno provoca febre e desidratação"),
            ("Rato-de-Pedra", "pacific", 0, "um pequeno mamífero transporta sementes para uma fenda protegida"),
            ("Escorpião-de-Quartzo", "territorial", 3, "pinças cristalinas ocupam a única sombra próxima"),
            ("Espectro-de-Pedra", "mystic", 5, "uma silhueta imita seus movimentos com um atraso que diminui a cada gesto"),
            ("Guardião de Silicyn", "legendary", 8, "placas minerais se elevam como um corpo quando vibrações atingem certa frequência"),
        ],
        "landmarks": [
            ("Planalto de Cristal", "Uma extensão de Silicyn refrata o céu em faixas que confundem distância e inclinação."),
            ("Salina das Luas", "Poças rasas deixam círculos de sal usados por caravanas para medir estação e rota."),
            ("Ninho da Águia do Platô", "Um arco de pedra abriga penas, ossos e objetos trazidos de lugares muito distantes."),
            ("Relógio de Patterium", "Colunas projetam sombras regulares, mas uma delas marca alguns minutos antes das demais."),
            ("Acampamento sem Pegadas", "Tendas rasgadas e recipientes secos permanecem montados; nenhuma trilha chega ou parte dali."),
        ],
        "hazards": [
            ("Insolação de Reflexo", "A luz devolvida pelo chão aquece rosto e olhos mesmo quando o vento parece fresco."),
            ("Fenda sob Crosta", "Uma camada fina cobre um vazio profundo o bastante para prender uma perna ou derrubar uma carga."),
            ("Tempestade de Cristal", "Partículas duras avançam rente ao chão e transformam pele exposta em ferida."),
            ("Miragem de Rota", "Marcos parecem se duplicar e conduzem viajantes para longe dos poços conhecidos."),
        ],
    },
    "canions_profundos": {
        "name": "Cânions Profundos",
        "region": "stonevale",
        "speed_kmh": 1.7,
        "temperature_delta": 5,
        "ambience": [
            "Paredes descem por centenas de metros, alternando faixas de Fractium escuro e rocha vermelha. O fundo permanece invisível atrás de névoa mineral.",
            "O eco chega por caminhos diferentes: primeiro uma sílaba clara, depois versões deformadas que parecem responder a perguntas ainda não feitas.",
            "Vinhas agarradas à parede marcam antigos pontos de escalada. Algumas cordas vegetais estão cortadas de dentro para fora.",
            "Uma queda d'água distante espalha névoa em arco-íris. Entre você e ela existem abismos, pontes frágeis e horas de descida.",
            "A temperatura muda a cada trecho de sombra; pedra que queimava a mão ao meio-dia pode congelar água depois do anoitecer.",
            "Morcegos-de-Eco abandonam uma fenda em ondas organizadas, desviando de algo que continua oculto no interior.",
        ],
        "weather": ["calor preso entre paredes", "vento ascendente", "névoa de cachoeira", "poeira ressonante", "sombra gelada", "trovoada distante"],
        "routes": {
            "norte": ["Acompanhar uma borda estável ao norte", "Subir por degraus Ferrari rumo ao norte", "Seguir as vinhas de parede para o norte"],
            "sul": ["Descer por um leito seco ao sul", "Procurar a ponte mais baixa ao sul", "Acompanhar a água rumo ao sul"],
            "leste": ["Cruzar uma cornija estreita a leste", "Seguir o eco de ferramentas para leste", "Contornar a garganta pelo leste"],
            "oeste": ["Subir pela face sombreada a oeste", "Seguir marcas Kragari para oeste", "Procurar a saída mais larga a oeste"],
        },
        "flora": [
            ("Samambaia-de-Fenda", "folhas surgem onde um fio de água atravessa a parede", False, False),
            ("Flor-de-Cachoeira", "pétalas aderem à rocha dentro da névoa constante", False, False),
            ("Musgo-de-Eco", "o musgo vibra e muda de cor quando recebe som", False, False),
            ("Vinhas-de-Parede", "caules fibrosos suportam peso apenas quando hidratados", False, False),
            ("Árvore-de-Cânion", "raízes atravessam estratos e formam uma pequena plataforma", True, False),
            ("Fungo-de-Resonum", "lamelas reproduzem vozes próximas e podem desorientar", False, True),
        ],
        "fauna": [
            ("Águia-de-Cânion", "predator", 3, "a ave usa correntes ascendentes para patrulhar ninhos na parede"),
            ("Cabra-das-Paredes", "pacific", 1, "cascos estreitos encontram apoio onde uma pessoa vê apenas rocha lisa"),
            ("Serpente-de-Fenda", "territorial", 4, "escamas escuras fecham a passagem para uma área aquecida"),
            ("Morcego-de-Eco", "neutral", 1, "chamados curtos desenham a garganta no escuro"),
            ("Lagarto-de-Parede", "neutral", 2, "dedos largos mantêm o animal numa superfície quase vertical"),
            ("Eco-Vivo", "mystic", 6, "uma voz sem corpo testa diferentes respostas para o mesmo perigo"),
            ("Dragão-de-Pedra Menor", "legendary", 8, "uma crista rochosa abre os olhos e bloqueia a ponte natural"),
            ("Guardião do Cânion Proibido", "legendary", 10, "corpos minerais repetem a postura de um exército morto ao redor de um único comando"),
        ],
        "landmarks": [
            ("Cânion Proibido", "Marcos de vários clãs repetem a mesma proibição em línguas e épocas diferentes."),
            ("Ponte das Vinhas", "Raízes trançadas ligam paredes separadas por um abismo que devolve vozes antigas."),
            ("Caverna dos Ecos", "Cada som retorna primeiro correto e depois alterado por uma intenção difícil de explicar."),
            ("Escadaria Ferrari", "Degraus escavados seguem uma tensão estrutural segura, desde que ninguém remova os grampos."),
            ("Campo dos Cem Capacetes", "Armaduras vazias estão posicionadas como soldados olhando para a garganta."),
        ],
        "hazards": [
            ("Queda de Cornija", "Pedra aquecida se desprende sem aviso e leva o apoio mais próximo."),
            ("Eco Desorientador", "Sua própria voz volta de uma direção impossível e apaga referências de percurso."),
            ("Cheia de Garganta", "Chuva ocorrida muitos quilômetros acima envia água e detritos pelo leito seco."),
            ("Frio de Fundo", "A sombra profunda derruba a temperatura antes que o corpo se adapte."),
        ],
    },
    "vales_ferteis_isolados": {
        "name": "Vales Férteis Isolados",
        "region": "stonevale",
        "speed_kmh": 2.2,
        "temperature_delta": 1,
        "ambience": [
            "Depois de quilômetros de pedra, árvores e água parecem excessivamente verdes. Canais pequenos dividem o vale conforme acordos marcados em placas públicas.",
            "Palmeiras protegem hortas, enquanto lagos de Aquanium devolvem reflexos que não correspondem exatamente às nuvens acima.",
            "O som de uma cascata ocupa o vale inteiro. Chegar à água, porém, exige contornar plantações, santuários e áreas de reprodução animal.",
            "Vinhas-de-Jade cobrem muros baixos e conduzem insetos luminosos entre flores abertas apenas na sombra.",
            "Casas aparecem em terraços distantes, mas horas de trilha e direitos de passagem separam você de qualquer porta.",
            "Uma miragem de Luminite duplica o bosque junto ao lago. A cópia não produz vento, cheiro nem pássaros.",
        ],
        "weather": ["ar morno e úmido", "chuva curta de vale", "névoa de cascata", "sol filtrado", "vento vindo do platô", "noite amena"],
        "routes": {
            "norte": ["Subir os terraços irrigados ao norte", "Seguir a margem alta para o norte", "Acompanhar canais antigos rumo ao norte"],
            "sul": ["Descer em direção às palmeiras ao sul", "Seguir a corrente para o sul", "Contornar o lago pelo sul"],
            "leste": ["Acompanhar Vinhas-de-Jade a leste", "Seguir o som da cascata para leste", "Usar uma trilha de cultivo rumo a leste"],
            "oeste": ["Procurar a saída do vale a oeste", "Seguir marcos de poço para oeste", "Subir pela sombra das árvores rumo a oeste"],
        },
        "flora": [
            ("Palmeira-de-Oásis", "frutos e sombra pertencem a uma comunidade que registra cada colheita", True, False),
            ("Lírio-d'Água Cristalino", "folhas transparentes protegem ovos de peixes", False, False),
            ("Musgo-de-Cascata", "tapetes espessos filtram sedimentos sem esterilizar a água", False, False),
            ("Árvore-de-Vida do Vale", "raízes unem canais e estabilizam encostas cultivadas", True, False),
            ("Flor-de-Miragem", "pétalas de Luminite criam duplicatas ópticas ao entardecer", False, False),
            ("Vinhas-de-Jade", "frutos duros armazenam minerais e umidade", True, False),
            ("Erva-dos-Sete-Poços", "folhas amargas reduzem febre quando preparadas corretamente", False, False),
        ],
        "fauna": [
            ("Cervo-de-Oásis", "pacific", 1, "um rebanho bebe somente depois que aves verificam a margem"),
            ("Peixe-Cristalino", "pacific", 0, "cardumes se tornam visíveis apenas quando mudam de direção"),
            ("Garça-Branca", "neutral", 1, "a ave caça em canais que pertencem a famílias diferentes"),
            ("Lontra-de-Vale", "territorial", 2, "uma família protege uma toca escavada sob raízes"),
            ("Borboleta-de-Luminite", "mystic", 1, "asas projetam uma segunda sombra alguns instantes antes do voo"),
            ("Ninfa-do-Oásis", "mystic", 5, "uma figura aquática observa quem retira água sem anunciar intenção"),
            ("Guardião de Jade", "legendary", 7, "raízes, pedra e água assumem forma quando um canal é ameaçado"),
            ("Fênix-de-Pedra", "legendary", 9, "fragmentos incandescentes reconstroem uma ave sobre uma antiga fogueira ritual"),
        ],
        "landmarks": [
            ("Oásis Esmeralda", "Poços, hortas e moradias dependem de uma assembleia que mede água, trabalho e estação."),
            ("Cascata da Vida", "Água atravessa Botanium e alimenta canais de três comunidades rivais."),
            ("Nascente de Jade", "Uma fonte mineral muda de vazão quando vozes entram em ressonância perto dela."),
            ("Jardim dos Espelhos", "Flores de Luminite multiplicam caminhos que somente cheiro e vento distinguem."),
            ("Terraço dos Acordos", "Pedras gravadas registram séculos de divisão de água e correções públicas."),
        ],
        "hazards": [
            ("Canal Rompido", "Água abre uma passagem nova e ameaça hortas antes que a comunidade consiga reagir."),
            ("Miragem de Luminite", "Uma cópia perfeita de sombra e água não possui temperatura nem profundidade."),
            ("Disputa de Poço", "Dois grupos armados chegam com registros incompatíveis de propriedade."),
            ("Predador na Margem", "A água está acessível, mas rastros frescos circundam o único ponto de descida."),
        ],
    },
}


STONEVALE_SETTLEMENTS: list[dict[str, Any]] = [
    {"id":"solkar","name":"Solkar","type":"capital solar","population":185000,"x":-180.0,"y":1120.0,"radius_km":38.0,"scene_id":"r4_solkar_portico_das_sombras","description":"Capital em terraços de pedra clara, sede da Mesa dos Poços, de observatórios Solari e de mercados que negociam água antes de qualquer metal."},
    {"id":"karsthal","name":"Karsthal","type":"fortaleza de cânion","population":62000,"x":1280.0,"y":1080.0,"radius_km":27.0,"scene_id":"r4_karsthal_portao_suspenso","description":"Fortaleza Kragari erguida sobre pontes, elevadores e muralhas que controlam a entrada do Cânion Proibido."},
    {"id":"ferraria_baixa","name":"Ferrária Baixa","type":"cidade mineira","population":31000,"x":1880.0,"y":420.0,"radius_km":21.0,"scene_id":"r4_ferraria_baixa_elevador","description":"Cidade Ferrari encaixada na rocha, especializada em grampos, bombas d'água, ferramentas de escalada e leitura estrutural."},
    {"id":"poco_sete_vozes","name":"Poço das Sete Vozes","type":"cidade-oásis","population":26000,"x":480.0,"y":-920.0,"radius_km":19.0,"scene_id":"r4_sete_vozes_praca_dagua","description":"Cidade multirracial construída ao redor de sete poços cujas vazões e ecos nunca coincidem."},
    {"id":"miralume","name":"Miralume","type":"cidade de estudos","population":18000,"x":1320.0,"y":-1120.0,"radius_km":16.0,"scene_id":"r4_miralume_jardim_dos_espelhos","description":"Centro de botânica, óptica e cura junto a flores de Luminite e canais protegidos por Ninfari."},
    {"id":"passo_kragar","name":"Passo Kragar","type":"forte de caravanas","population":12000,"x":720.0,"y":1860.0,"radius_km":14.0,"scene_id":"r4_passo_kragar_patio","description":"Entreposto Kragari onde caravanas contratam guardas e transformam duelos em contratos públicos de responsabilidade."},
    {"id":"cristalia","name":"Cristália","type":"cidade de extração","population":15000,"x":-980.0,"y":2020.0,"radius_km":14.0,"scene_id":"r4_cristalia_arco_mineral","description":"Cidade de mineiros Aureli, Ferrari e Voraki que limita a retirada de Silicyn para impedir o colapso dos platôs."},
    {"id":"ponte_alta","name":"Ponte Alta","type":"vila suspensa","population":8000,"x":2060.0,"y":1480.0,"radius_km":11.0,"scene_id":"r4_ponte_alta_catraca","description":"Vila distribuída pelos dois lados de uma garganta, dependente de cabos, guinchos e uma ponte viva de raízes."},
    {"id":"jardim_jade","name":"Jardim de Jade","type":"comunidade agrícola","population":5000,"x":-420.0,"y":-1180.0,"radius_km":10.0,"scene_id":"r4_jardim_jade_canal_comum","description":"Comunidade de hortas e canais que reconhece água como responsabilidade coletiva e não como propriedade absoluta."},
    {"id":"salina_luas","name":"Salina das Luas","type":"cidade de caravana","population":11000,"x":-1680.0,"y":620.0,"radius_km":13.0,"scene_id":"r4_salina_luas_balanca","description":"Mercado de sal, couro, montarias e informação onde preços mudam com poços fechados e tempestades previstas."},
    {"id":"vigilia_rubra","name":"Vigília Rubra","type":"posto de fronteira","population":3000,"x":-2880.0,"y":380.0,"radius_km":9.0,"scene_id":"r4_vigilia_rubra_marco","description":"Posto aberto entre os campos de Arkanor e os primeiros platôs, usado por guias, fiscais, refugiados e contrabandistas."},
]


STONEVALE_NPCS: list[dict[str, Any]] = [
    {"id":"rakh_toruun","name":"Rakh Toruun","race":"Kragari","role":"guarda de caravana e possível companheiro","home":"passo_kragar","faction":"guardas_do_passo","x":720.0,"y":1860.0,"description":"um Kragari enorme distribui água aos animais antes de beber; o duelo que o tornou famoso foi combinado para evitar uma guerra","values":["proteção","honra como responsabilidade","verdade útil"],"red_lines":["crueldade gratuita","abandonar dependente"]},
    {"id":"samira_sete_sombras","name":"Samira Sete-Sombras","race":"Solari","role":"astrônoma e mediadora da Mesa","home":"solkar","faction":"mesa_dos_pocos","x":-160.0,"y":1140.0,"description":"uma Solari compara o tamanho de sete sombras antes de aceitar que dois mapas descrevem o mesmo poço","values":["observação","água pública","dúvida honesta"],"red_lines":["falsificar medição","punir sede"]},
    {"id":"maara_veyl","name":"Maara Veyl","race":"Humana","role":"mercadora de água e contratos","home":"salina_luas","faction":"liga_das_caravanas","x":-1660.0,"y":640.0,"description":"uma humana recalcula o preço de cada odre quando uma rota fecha, mas mantém uma cota gratuita para quem chegaria morto ao próximo poço","values":["continuidade","lucro sustentável","palavra dada"],"red_lines":["envenenar poço","roubar caravana"]},
    {"id":"telar_folha_palida","name":"Telar Folha-Pálida","race":"Sylvani","role":"cultivador de sombra","home":"jardim_jade","faction":"circulo_dos_canais","x":-400.0,"y":-1160.0,"description":"um Sylvani de pele pálida orienta folhas para reduzir a evaporação de um canal comum","values":["cultivo","cooperação","paciência"],"red_lines":["queimar horta","privatizar chuva"]},
    {"id":"orun_veio_seco","name":"Orun Veio-Seco","race":"Aureli","role":"mestre de extração","home":"cristalia","faction":"guilda_do_silicyn","x":-960.0,"y":2040.0,"description":"um Aureli marca a pedra que não deve ser cortada, mesmo sendo a mais valiosa do turno","values":["estrutura","trabalho","legado"],"red_lines":["mineração cega","fraude de segurança"]},
    {"id":"neris_sete_pocos","name":"Neris Sete-Poços","race":"Aquari","role":"hidróloga itinerante","home":"poco_sete_vozes","faction":"circulo_dos_canais","x":500.0,"y":-900.0,"description":"uma Aquari prova gotas de sete recipientes e identifica a origem pela concentração mineral","values":["fluxo","acesso","cuidado"],"red_lines":["contaminar água","negar socorro"]},
    {"id":"ivena_branca","name":"Ivena Branca","race":"Glacari","role":"médica do calor","home":"vigilia_rubra","faction":"casa_da_sombra","x":-2860.0,"y":400.0,"description":"uma Glacari observa pele, fala e coordenação para diagnosticar insolação antes que o viajante perceba","values":["cuidado","preparo","acolhimento"],"red_lines":["deixar febril ao sol","cobrar por emergência"]},
    {"id":"lume_dois","name":"Lume-Dois","race":"Luminari","role":"cartógrafa de miragens","home":"miralume","faction":"observatorio_das_reflexoes","x":1300.0,"y":-1100.0,"description":"uma Luminari mede uma miragem pelo ponto em que sua própria sombra deixa de acompanhá-la","values":["curiosidade","beleza verificável","autoria"],"red_lines":["cegar animal","roubar mapa"]},
    {"id":"zik_corda_curta","name":"Zik Corda-Curta","race":"Ziraki","role":"mecânico de guinchos","home":"ponte_alta","faction":"mestres_da_ponte","x":2040.0,"y":1480.0,"description":"um Ziraki escuta a tensão dos cabos com uma peça de metal entre os dentes","values":["invenção","manutenção","troca justa"],"red_lines":["ocultar desgaste","culpar aprendiz"]},
    {"id":"nhalis_azul","name":"Nhalis Azul","race":"Ninfari","role":"guardiã da Nascente de Jade","home":"miralume","faction":"guardioes_da_nascente","x":1340.0,"y":-1140.0,"description":"uma Ninfari permanece dentro do canal para sentir mudanças de vazão causadas por vozes distantes","values":["água","memória","consentimento"],"red_lines":["aprisionar ninfa","secar berçário"]},
    {"id":"sombra_de_sal","name":"Sombra-de-Sal","race":"Umbrari","role":"investigadora de desvios","home":"salina_luas","faction":"arquivo_dos_odres","x":-1700.0,"y":600.0,"description":"uma Umbrari segue o rastro úmido de um odre numa praça seca e encontra uma dívida escondida","values":["prova","sigilo responsável","sobrevivência"],"red_lines":["fabricar culpado","expor fonte"]},
    {"id":"ferra_viga_rubra","name":"Ferra Viga-Rubra","race":"Ferrari","role":"engenheira do cânion","home":"ferraria_baixa","faction":"mestres_da_ponte","x":1860.0,"y":440.0,"description":"uma Ferrari testa grampos estruturais enquanto trabalhadores ainda descem pelo elevador","values":["segurança","reparo","responsabilidade"],"red_lines":["ignorar fissura","sobrecarregar cabo"]},
    {"id":"dravos_bronze","name":"Dravos Bronze","race":"Drakari","role":"capitão de Karsthal","home":"karsthal","faction":"vigias_do_canion","x":1300.0,"y":1100.0,"description":"um Drakari percebe calor por trás da rocha e manda retirar a patrulha antes do primeiro desabamento","values":["dever","proteção","disciplina"],"red_lines":["executar rendido","abandonar posto civil"]},
    {"id":"erian_vespera","name":"Erian Véspera","race":"Ethari","role":"estudiosa dos Ecos","home":"solkar","faction":"arquivo_das_vozes","x":-200.0,"y":1100.0,"description":"uma Ethari deixa um gravador de Resonum responder primeiro, para não contaminar o Eco com expectativa","values":["identidade","registro","consentimento"],"red_lines":["apagar testemunho","ocupar corpo"]},
    {"id":"torv_fenda_clara","name":"Torv Fenda-Clara","race":"Voraki","role":"batedor subterrâneo","home":"ferraria_baixa","faction":"cartografos_da_fenda","x":1900.0,"y":400.0,"description":"um Voraki encontra galerias ocultas pela vibração de gotas muito abaixo do piso","values":["território","orientação","autonomia"],"red_lines":["selar vivo","invadir ninho"]},
    {"id":"cora_pedra_mansa","name":"Cora Pedra-Mansa","race":"Humana","role":"juíza itinerante da água","home":"poco_sete_vozes","faction":"mesa_dos_pocos","x":460.0,"y":-940.0,"description":"uma juíza humana escuta agricultores, caravaneiros e animais de carga antes de dividir uma vazão insuficiente","values":["processo público","proporção","reparação"],"red_lines":["suborno","punição coletiva"]},
    {"id":"kharos_do_eco","name":"Kharos do Eco","race":"Eco","role":"cópia ressonante de um general morto","home":"canion_proibido","faction":"exercito_dos_ecos","x":2440.0,"y":820.0,"description":"uma voz militar alterna entre corpos e paredes, convencida de que a batalha de novecentos anos atrás ainda ocorre","values":["continuidade","soldados","vitória"],"red_lines":["apagar memória","declarar seus mortos irreais"]},
]


STONEVALE_ROADS: list[dict[str, Any]] = [
    {"id":"rota_rubra","a":(-2880.0,380.0),"b":(-180.0,1120.0),"width_km":24.0},
    {"id":"rota_das_salinas","a":(-1680.0,620.0),"b":(-180.0,1120.0),"width_km":20.0},
    {"id":"estrada_do_silicyn","a":(-980.0,2020.0),"b":(-180.0,1120.0),"width_km":18.0},
    {"id":"rota_do_passo","a":(-180.0,1120.0),"b":(720.0,1860.0),"width_km":22.0},
    {"id":"ponte_de_karsthal","a":(-180.0,1120.0),"b":(1280.0,1080.0),"width_km":18.0},
    {"id":"rota_dos_guinchos","a":(1280.0,1080.0),"b":(2060.0,1480.0),"width_km":13.0},
    {"id":"descida_ferrari","a":(1280.0,1080.0),"b":(1880.0,420.0),"width_km":15.0},
    {"id":"caminho_dos_sete_pocos","a":(-180.0,1120.0),"b":(480.0,-920.0),"width_km":21.0},
    {"id":"rota_de_jade","a":(480.0,-920.0),"b":(-420.0,-1180.0),"width_km":14.0},
    {"id":"estrada_dos_espelhos","a":(480.0,-920.0),"b":(1320.0,-1120.0),"width_km":16.0},
]


STONEVALE_MARKETS: dict[str, dict[str, Any]] = {
    "solkar": {"currency":"coroas","water_index":1.15,"stock":[("odre de água",5,2),("véu solar",8,3),("mapa dos poços",14,6)]},
    "karsthal": {"currency":"coroas","water_index":1.30,"stock":[("corda de cânion",10,4),("grampo Ferrari",12,5),("ração seca",5,2)]},
    "ferraria_baixa": {"currency":"coroas","water_index":1.35,"stock":[("picareta de Silicyn",18,8),("kit de escalada",22,10),("máscara de poeira",9,4)]},
    "poco_sete_vozes": {"currency":"coroas","water_index":0.80,"stock":[("odre de água",4,2),("erva dos sete poços",7,3),("fruta de oásis",3,1)]},
    "miralume": {"currency":"coroas","water_index":0.90,"stock":[("antídoto de miragem",12,5),("lente de Luminite",20,9),("erva medicinal",7,3)]},
    "passo_kragar": {"currency":"coroas","water_index":1.25,"stock":[("ração de caravana",6,3),("escudo de viagem",24,11),("corda de cânion",11,5)]},
    "cristalia": {"currency":"coroas","water_index":1.40,"stock":[("fragmento de Silicyn",15,7),("óculos de cristal",10,4),("cantimplora reforçada",12,5)]},
    "ponte_alta": {"currency":"coroas","water_index":1.20,"stock":[("grampo Ferrari",11,5),("luvas de escalada",13,6),("corda de cânion",9,4)]},
    "jardim_jade": {"currency":"coroas","water_index":0.65,"stock":[("fruta de oásis",2,1),("erva medicinal",6,3),("semente de jade",8,3)]},
    "salina_luas": {"currency":"coroas","water_index":1.10,"stock":[("sal lunar",4,2),("odre de água",5,2),("capa de poeira",9,4)]},
    "vigilia_rubra": {"currency":"coroas","water_index":1.20,"stock":[("odre de água",6,2),("mapa de fronteira",8,3),("ração seca",5,2)]},
}


STONEVALE_REGION_MAPS: dict[str, dict[str, Any]] = {
    "stonevale": {
        "name": "Stonevale",
        "spawns": {
            "platos_aridos": [(-1480.0, 840.0), (-760.0, 2280.0), (240.0, 2540.0)],
            "canions_profundos": [(760.0, 620.0), (1640.0, 1860.0), (2380.0, 260.0)],
            "vales_ferteis_isolados": [(-620.0, -980.0), (520.0, -1480.0), (1480.0, -920.0)],
        },
        "borders": [
            {
                "id":"stonevale_arkanor","axis":"x","limit":-3000.0,"operator":"<=",
                "x_min":-10000.0,"x_max":10000.0,"y_min":-600.0,"y_max":1650.0,"direction":"oeste",
                "target_region":"arkanor","target_biome":"vales_verdes","target_position":(1760.0,-420.0),
                "name":"Fronteira das Pedras Rubras",
                "description":"A rocha nua se fragmenta em colinas cobertas de pasto, canais e estradas medidas; Stonevale termina sem muralha onde começam as propriedades orientais de Arkanor.",
            }
        ],
    }
}


ARKANOR_STONEVALE_BORDER = {
    "id":"arkanor_stonevale","axis":"x","limit":1800.0,"operator":">=",
    "x_min":-10000.0,"x_max":10000.0,"y_min":-1200.0,"y_max":850.0,"direction":"leste",
    "target_region":"stonevale","target_biome":"platos_aridos","target_position":(-2960.0,380.0),
    "name":"Fronteira das Primeiras Lajes",
    "description":"Campos e salgueiros tornam-se raros, a estrada endurece sobre placas vermelhas e o ar seco anuncia Stonevale muito antes de qualquer posto.",
}


STONEVALE_PHASE_DETAILS = {
    "Madrugada": ("A pedra perdeu o calor e o frio ocupa fendas e fundos de cânion.", "Estrelas Solari oferecem orientação precisa, mas qualquer fogueira fica visível de longe.", "Caravanas preparam animais antes do primeiro brilho para aproveitar as horas frescas."),
    "Amanhecer": ("A luz alcança bordas altas antes dos vales e revela caminhos em camadas.", "Flores de deserto se abrem por poucos minutos enquanto insetos deixam seus abrigos.", "Mercados de água recebem as primeiras medições de poços e cisternas."),
    "Manhã": ("A temperatura sobe depressa sobre as lajes e sombras encolhem a cada passo.", "Nas rotas, caravanas distribuem água em pausas marcadas; longe delas, o horizonte permanece vazio.", "Correntes ascendentes carregam aves acima dos cânions sem aproximá-las do chão."),
    "Tarde": ("O calor refletido pelo solo torna água, cobertura e ritmo decisões mais importantes que distância.", "Sombras de cânion oferecem alívio, mas também escondem predadores e quedas.", "Miragens de Luminite começam a duplicar vegetação e construções distantes."),
    "Entardecer": ("A pedra libera calor enquanto o ar esfria, produzindo vento entre platô e vale.", "Caravanas procuram círculos de acampamento e cidades fecham cotas públicas de água.", "Ecos se alongam com as sombras e algumas respostas deixam de coincidir com a voz original."),
    "Noite": ("O frio substitui o calor em poucas horas; caminhar exige luz discreta e roupa seca.", "Céu e estrelas revelam direção, enquanto o fundo dos cânions desaparece por completo.", "Fauna deixa fendas e canais; assentamentos mantêm vigias junto a poços e elevadores."),
}


STONEVALE_QUIET_TRAVEL = (
    "O trecho oferece apenas pedra, vento e distância. Nenhuma criatura altera a rota por sua presença.",
    "Você encontra fezes secas, pele trocada e marcas antigas, mas a fauna permanece longe durante toda a marcha.",
    "Uma coluna no horizonte cresce devagar por horas sem se transformar em cidade, pessoa ou ameaça.",
    "Vegetação baixa ocupa fendas dispersas; reconhecê-la não produz automaticamente alimento ou missão.",
    "O caminho continua vazio. Sede, apoio dos pés e posição do sol são os acontecimentos relevantes do período.",
    "Sinais de caravana aparecem sem seus autores: cinza fria, uma tira de couro e pedras recolocadas sobre a rota.",
    "Você escuta aves muito acima e água muito abaixo, mas não encontra acesso seguro a nenhuma das duas.",
    "Por quilômetros não há conversa, ruína extraordinária nem combate — apenas o trabalho de atravessar Stonevale vivo.",
)

