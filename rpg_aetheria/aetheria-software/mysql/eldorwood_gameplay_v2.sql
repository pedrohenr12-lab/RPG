-- Eldorwood: mapa espacial, assentamentos, rotas e NPCs persistentes.
-- Idempotente: pode ser executado várias vezes sem apagar saves ou conteúdo.
USE aetheria_rpg;

CREATE TABLE IF NOT EXISTS regional_settlements (
    settlement_key VARCHAR(120) PRIMARY KEY,
    region_slug VARCHAR(80) NOT NULL,
    biome_slug VARCHAR(80) NULL,
    name VARCHAR(160) NOT NULL,
    settlement_type VARCHAR(80) NOT NULL,
    population_estimate INT NOT NULL DEFAULT 0,
    x_km DECIMAL(10,2) NOT NULL,
    y_km DECIMAL(10,2) NOT NULL,
    radius_km DECIMAL(8,2) NOT NULL DEFAULT 1,
    entry_scene_key VARCHAR(160) NOT NULL,
    description TEXT NOT NULL,
    INDEX idx_settlement_region_position (region_slug, x_km, y_km)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS regional_routes (
    route_key VARCHAR(120) PRIMARY KEY,
    region_slug VARCHAR(80) NOT NULL,
    route_type VARCHAR(60) NOT NULL DEFAULT 'road',
    a_x_km DECIMAL(10,2) NOT NULL,
    a_y_km DECIMAL(10,2) NOT NULL,
    b_x_km DECIMAL(10,2) NOT NULL,
    b_y_km DECIMAL(10,2) NOT NULL,
    influence_width_km DECIMAL(8,2) NOT NULL,
    description TEXT NULL,
    INDEX idx_route_region (region_slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS region_borders_v2 (
    border_key VARCHAR(120) PRIMARY KEY,
    source_region_slug VARCHAR(80) NOT NULL,
    target_region_slug VARCHAR(80) NOT NULL,
    direction_key VARCHAR(20) NOT NULL,
    axis_key CHAR(1) NOT NULL,
    coordinate_limit_km DECIMAL(10,2) NOT NULL,
    corridor_min_km DECIMAL(10,2) NOT NULL,
    corridor_max_km DECIMAL(10,2) NOT NULL,
    target_biome_slug VARCHAR(80) NOT NULL,
    target_x_km DECIMAL(10,2) NOT NULL,
    target_y_km DECIMAL(10,2) NOT NULL,
    description TEXT NOT NULL,
    INDEX idx_border_source (source_region_slug, direction_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS npc_definitions_v2 (
    npc_key VARCHAR(120) PRIMARY KEY,
    name VARCHAR(160) NOT NULL,
    race_name VARCHAR(120) NOT NULL,
    role_name VARCHAR(160) NOT NULL,
    home_settlement_key VARCHAR(120) NULL,
    faction_key VARCHAR(120) NULL,
    x_km DECIMAL(10,2) NOT NULL,
    y_km DECIMAL(10,2) NOT NULL,
    description TEXT NOT NULL,
    values_json JSON NOT NULL,
    red_lines_json JSON NOT NULL,
    INDEX idx_npc_home (home_settlement_key),
    INDEX idx_npc_position (x_km, y_km)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO regional_settlements
(settlement_key,region_slug,biome_slug,name,settlement_type,population_estimate,x_km,y_km,radius_km,entry_scene_key,description)
VALUES
('sylvarin','eldorwood','floresta_densa_antiga','Sylvarin','capital florestal',180000,0,1780,34,'r2_sylvarin_portoes','Capital construída no solo, nos troncos e nas copas; conselho, guildas, mercados e bairros multirraciais disputam o uso da floresta.'),
('brumavale','eldorwood','pantanos_rios','Brumavale','cidade fluvial',96000,920,760,28,'r2_brumavale_cais','Cidade de canais, cais sobre raízes e rodas d\'água; Aquari, Ninfari, humanos e Ziraki governam margens interdependentes.'),
('lethariel','eldorwood','floresta_densa_antiga','Lethariel','cidade do dossel',74000,-1120,2140,25,'r2_lethariel_passarela','Cidade Sylvani vertical ligada por passarelas vivas, arquivos de casca e santuários que guardam memórias antigas.'),
('ponte_circulium','eldorwood','floresta_densa_antiga','Ponte de Circulium','cidade-ponte',18000,610,1240,16,'r2_ponte_circulium','Entreposto construído ao redor de uma ponte mineral cujos arcos distribuem carga em padrões circulares.'),
('vale_eldor','eldorwood','floresta_densa_antiga','Vale Eldor','vila agrícola',6200,150,1430,12,'r2_vale_eldor_praca','Vila de hortas, boticários e criadores que abastece Sylvarin sem deixar de negociar autonomia.'),
('brejo_lume','eldorwood','pantanos_rios','Brejo-Lume','aldeia aquática',2100,1510,-880,9,'r2_brejo_lume_ancoradouro','Aldeia Ninfari e Aquari erguida em ilhas de raiz, próxima a berçários naturais e águas luminosas.'),
('folha_baixa','eldorwood','floresta_densa_antiga','Folha Baixa','aldeia de coletores',980,-390,810,7,'r2_folha_baixa_entrada','Povoado de coletores e boticários onde plantas medicinais, venenos e informação percorrem as mesmas mesas.'),
('miralva','eldorwood','colinas_arborizadas','Miralva','cidade fortificada',26000,-1430,2620,15,'r2_miralva_portao','Cidade de colina, observatório e fortificações que protege estradas do norte sem controlar toda a fronteira.'),
('passagem_cervo','eldorwood','colinas_arborizadas','Passagem do Cervo','pouso de estrada',640,-710,2360,6,'r2_passagem_cervo','Pouso de caravanas onde animais, contratos e notícias recebem tanta atenção quanto viajantes.'),
('raiz_serena','eldorwood','floresta_densa_antiga','Raiz Serena','comunidade contemplativa',430,430,2020,5,'r2_raiz_serena','Pequena comunidade reunida em torno de uma raiz silenciosa, visitada por curadores e estudiosos.'),
('portao_nevoa','eldorwood','colinas_arborizadas','Portão da Névoa','posto de fronteira',1200,180,2920,8,'r2_portao_nevoa','Último posto antes da tundra de Frostreach; abriga vigias, médicos e viajantes sem exigir uma missão para cruzar.')
ON DUPLICATE KEY UPDATE
region_slug=VALUES(region_slug),biome_slug=VALUES(biome_slug),name=VALUES(name),settlement_type=VALUES(settlement_type),
population_estimate=VALUES(population_estimate),x_km=VALUES(x_km),y_km=VALUES(y_km),radius_km=VALUES(radius_km),
entry_scene_key=VALUES(entry_scene_key),description=VALUES(description);

INSERT INTO regional_routes
(route_key,region_slug,route_type,a_x_km,a_y_km,b_x_km,b_y_km,influence_width_km,description)
VALUES
('estrada_do_dossel','eldorwood','road',0,1780,-1430,2620,24,'Liga Sylvarin a Miralva por terreno alto e trechos sob o dossel.'),
('rota_das_duas_margens','eldorwood','river_road',920,760,610,1240,20,'Conecta Brumavale à Ponte de Circulium por água e margens consolidadas.'),
('caminho_de_eldor','eldorwood','road',610,1240,0,1780,18,'Estrada de abastecimento entre a Ponte de Circulium e Sylvarin.'),
('estrada_da_fronteira','eldorwood','road',-1430,2620,180,2920,22,'Rota de Miralva ao Portão da Névoa e à fronteira de Frostreach.'),
('rota_dos_boticarios','eldorwood','trail',-390,810,150,1430,12,'Trilha de coletores entre Folha Baixa e Vale Eldor.'),
('rota_do_brejo','eldorwood','river_road',920,760,1510,-880,16,'Canais e passadiços de Brumavale até Brejo-Lume.'),
('trilha_de_lethariel','eldorwood','trail',0,1780,-1120,2140,10,'Passagens controladas pelo dossel entre Sylvarin e Lethariel.')
ON DUPLICATE KEY UPDATE
region_slug=VALUES(region_slug),route_type=VALUES(route_type),a_x_km=VALUES(a_x_km),a_y_km=VALUES(a_y_km),
b_x_km=VALUES(b_x_km),b_y_km=VALUES(b_y_km),influence_width_km=VALUES(influence_width_km),description=VALUES(description);

INSERT INTO region_borders_v2
(border_key,source_region_slug,target_region_slug,direction_key,axis_key,coordinate_limit_km,corridor_min_km,corridor_max_km,target_biome_slug,target_x_km,target_y_km,description)
VALUES
('eldorwood_frostreach','eldorwood','frostreach','norte','y',3000,-900,1250,'planalto_central_frostreach',450,-2920,'As colinas perdem árvores e cedem à tundra; a travessia conserva tempo, necessidades, itens e relações.'),
('frostreach_eldorwood','frostreach','eldorwood','sul','y',-3000,-900,1250,'colinas_arborizadas',450,2960,'A tundra cede a bosques úmidos; a mesma fronteira pode ser cruzada no sentido inverso.')
ON DUPLICATE KEY UPDATE
source_region_slug=VALUES(source_region_slug),target_region_slug=VALUES(target_region_slug),direction_key=VALUES(direction_key),
axis_key=VALUES(axis_key),coordinate_limit_km=VALUES(coordinate_limit_km),corridor_min_km=VALUES(corridor_min_km),
corridor_max_km=VALUES(corridor_max_km),target_biome_slug=VALUES(target_biome_slug),target_x_km=VALUES(target_x_km),
target_y_km=VALUES(target_y_km),description=VALUES(description);

INSERT INTO npc_definitions_v2
(npc_key,name,race_name,role_name,home_settlement_key,faction_key,x_km,y_km,description,values_json,red_lines_json)
VALUES
('sael_ithyr','Sael Ithyr','Sylvani','guardião de memórias','lethariel','conselhos_do_dossel',-1080,2100,'Escuta raízes antes de responder e protege a autonomia de quem se conecta à rede.',JSON_ARRAY('autonomia','memória','cuidado'),JSON_ARRAY('queimar árvore viva','forçar assimilação')),
('maelis_venn','Maelis Venn','Umbrari','boticária e informante','folha_baixa','arquivo_da_lanterna',-410,830,'Separa remédios, venenos e informações com a mesma cautela.',JSON_ARRAY('conhecimento','discrição','sobrevivência'),JSON_ARRAY('expor fonte vulnerável','desperdiçar antídoto')),
('mara_avel','Mara Avel','Humana','curandeira','vale_eldor','boticarios_folha_velada',150,1430,'Avalia primeiro a respiração e só depois pergunta o nome.',JSON_ARRAY('cuidado','honestidade','aprendizado'),JSON_ARRAY('vender remédio falso','abandonar doente')),
('orun_duas_margens','Orun das Duas Margens','Aquari','diplomata fluvial','brumavale','coro_de_navegadores',900,780,'Representa margens interdependentes de Brumavale.',JSON_ARRAY('fluxo','reciprocidade','acordo'),JSON_ARRAY('envenenar rio','aprisionar navegante')),
('tili_sete_sinos','Tili Sete-Sinos','Luminari','mensageira','sylvarin','estradas_livres',30,1760,'Transporta mensagens por rotas aéreas curtas e estradas longas.',JSON_ARRAY('liberdade','curiosidade','palavra dada'),JSON_ARRAY('reter correspondência','enjaular ser alado')),
('brohm_pedra_mansa','Brohm Pedra-Mansa','Ferrari','mestre de pontes','ponte_circulium','mestres_de_ponte',620,1240,'Testa pilares pelo som e recusa inaugurar obra insegura.',JSON_ARRAY('obra segura','responsabilidade','paciência'),JSON_ARRAY('sabotar ponte ocupada','falsificar inspeção')),
('ysra_miralva','Ysra de Miralva','Humana','capitã da guarda','miralva','guarda_de_miralva',-1420,2600,'Protege a cidade e exige provas antes de condenar.',JSON_ARRAY('ordem','proteção','prova'),JSON_ARRAY('ferir civil','subornar guarda')),
('velen_raiz_clara','Velen Raiz-Clara','Sylvani','conselheiro urbano','sylvarin','conselhos_do_dossel',0,1800,'Negocia interesses de raças, guildas e guardiões.',JSON_ARRAY('equilíbrio','continuidade','consenso'),JSON_ARRAY('incêndio','decisão secreta sobre a floresta')),
('zori_trinca_folha','Zori Trinca-Folha','Ziraki','mecânica de rodas d\'água','brumavale','oficios_livres',940,750,'Constrói mecanismos e protege o crédito de aprendizes.',JSON_ARRAY('invenção','troca justa','humor'),JSON_ARRAY('roubar projeto de aprendiz','culpar trabalhador')),
('rheva_mare_baixa','Rheva Maré-Baixa','Ninfari','guardiã de fonte','brejo_lume','confluencia',1490,-850,'Observa algas e berçários antes de autorizar qualquer obra fluvial.',JSON_ARRAY('água','comunidade','verdade'),JSON_ARRAY('contaminar fonte','vender água sagrada')),
('garran_casco_cinza','Garran Casco-Cinza','Kragari','caravaneiro','passagem_cervo','estradas_livres',-680,2340,'Trata animais feridos com mais delicadeza do que sua voz sugere.',JSON_ARRAY('dever','franqueza','proteção'),JSON_ARRAY('abandonar animal','quebrar contrato')),
('essen_luz_de_chuva','Essen Luz-de-Chuva','Ethari','astrônoma','miralva','observatorio_de_miralva',-1450,2650,'Compara padrões da chuva com observações celestes.',JSON_ARRAY('evidência','harmonia','partilha'),JSON_ARRAY('destruir registro','fabricar presságio')),
('kora_solo_quieto','Kora Solo-Quieto','Voraki','agrimensora','portao_nevoa','cartografos_da_aurora',160,2900,'Detecta vibrações de carroças e mede fronteiras sem fechá-las.',JSON_ARRAY('território','precisão','memória'),JSON_ARRAY('apagar marco','minerar sem medir')),
('aelar_duas_copas','Aelar Duas-Copas','Drakari','cavaleiro do conselho','lethariel','guardioes_dos_seis_selos',-1100,2170,'Guarda selos antigos e percebe calor sob raízes.',JSON_ARRAY('dever','proteção','disciplina'),JSON_ARRAY('abrir selo desconhecido','ameaçar criança')),
('hela_fruto_vermelho','Hela Fruto-Vermelho','Solari','dona de estalagem','passagem_cervo','estradas_livres',-700,2360,'Administra comida, abrigo e informações da estrada.',JSON_ARRAY('hospitalidade','clareza','trabalho'),JSON_ARRAY('envenenar hóspede','negar pagamento')),
('dori_folha_de_ferro','Dori Folha-de-Ferro','Aureli','ferreira','sylvarin','oficios_livres',20,1740,'Forja ferramentas destinadas a cortar somente madeira morta.',JSON_ARRAY('qualidade','limite','legado'),JSON_ARRAY('cortar Árvore-Anciã','vender arma defeituosa')),
('iven_neve_mansa','Iven Neve-Mansa','Glacari','médico de fronteira','portao_nevoa','vigias_da_fronteira',210,2940,'Cuida de viajantes expostos e compara a umidade de Eldorwood com o gelo do norte.',JSON_ARRAY('prudência','cuidado','travessia livre'),JSON_ARRAY('abandonar viajante exposto','fechar a fronteira por origem'))
ON DUPLICATE KEY UPDATE
name=VALUES(name),race_name=VALUES(race_name),role_name=VALUES(role_name),home_settlement_key=VALUES(home_settlement_key),
faction_key=VALUES(faction_key),x_km=VALUES(x_km),y_km=VALUES(y_km),description=VALUES(description),
values_json=VALUES(values_json),red_lines_json=VALUES(red_lines_json);

SELECT
    (SELECT COUNT(*) FROM regional_settlements WHERE region_slug='eldorwood') AS assentamentos,
    (SELECT COUNT(*) FROM regional_routes WHERE region_slug='eldorwood') AS rotas,
    (SELECT COUNT(*) FROM npc_definitions_v2 WHERE home_settlement_key IN
        (SELECT settlement_key FROM regional_settlements WHERE region_slug='eldorwood')) AS npcs,
    (SELECT COUNT(*) FROM region_borders_v2 WHERE source_region_slug IN ('eldorwood','frostreach')) AS fronteiras;
