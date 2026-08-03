-- Região 3 — Arkanor: mapa espacial, rotas, fronteira e NPCs persistentes.
-- Idempotente: pode ser executado novamente sem apagar personagens ou saves.
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
('cidade_arkanor','arkanor','planicies_ferteis','Cidade de Arkanor','capital',420000,0.0,1180.0,42.0,'r3_arkanor_portao_sul','Capital do Pacto Dourado, dividida entre palácio, assembleia mercantil, universidades, tribunais, guildas e bairros de muitas raças.'),
('porto_aurenta','arkanor','vales_verdes','Porto do Aurenta','cidade fluvial',112000,1120.0,720.0,30.0,'r3_porto_aurenta_cais','Cidade de cais, armazéns, estaleiros e pontes onde o rio transforma informação em mercadoria.'),
('alvacampo','arkanor','planicies_ferteis','Alvacampo','cidade agrícola',68000,-920.0,1680.0,25.0,'r3_alvacampo_portao','Centro de grãos e trabalho rural, rico em celeiros e marcado por dívidas de terra.'),
('sete_arcos','arkanor','vales_verdes','Sete Arcos','cidade-ponte',31000,720.0,1450.0,19.0,'r3_sete_arcos_ponte','Entreposto erguido ao redor de pontes de épocas diferentes e pedágios concorrentes.'),
('vinhedos_orbel','arkanor','colinas_suaves','Vinhedos de Orbel','vila de colina',9400,-1340.0,540.0,12.0,'r3_orbel_estrada','Vila de produtores, arrendatários e adegas onde safras antigas sustentam poder político.'),
('campos_dourados','arkanor','planicies_ferteis','Campos Dourados','vila agrícola',7600,-340.0,2050.0,10.0,'r3_campos_dourados_marco','Comunidade cercada por grandes propriedades, canais de irrigação e trabalhadores sazonais.'),
('salgueiral','arkanor','vales_verdes','Salgueiral','vila ribeirinha',5200,1450.0,-180.0,9.0,'r3_salgueiral_trapiche','Vila de pesca, cestos e pequenas balsas protegida por salgueiros antigos.'),
('nascente_serena','arkanor','vales_verdes','Nascente Serena','comunidade de cura',1800,820.0,-960.0,7.0,'r3_nascente_serena_entrada','Comunidade multirracial que cuida de uma fonte de Aquanium e resiste à privatização da água.'),
('mercado_horizonte','arkanor','planicies_ferteis','Mercado do Horizonte','cidade de estrada',24000,-280.0,2600.0,16.0,'r3_mercado_horizonte_portico','Último grande mercado ao norte, abastecendo caravanas entre Arkanor e Eldorwood.'),
('vigilia_verde','arkanor','planicies_ferteis','Vigília Verde','posto de fronteira',2100,430.0,2940.0,8.0,'r3_vigilia_verde_cancela','Posto aberto junto à fronteira úmida de Eldorwood, ocupado por guardas, boticários e guias.'),
('balanca_baixa','arkanor','planicies_ferteis','Balança Baixa','bairro extramuros',17000,90.0,1070.0,13.0,'r3_balanca_baixa_praca','Bairro de refugiados, diaristas e ofícios não reconhecidos pelas guildas da capital.')
ON DUPLICATE KEY UPDATE
region_slug=VALUES(region_slug),biome_slug=VALUES(biome_slug),name=VALUES(name),settlement_type=VALUES(settlement_type),population_estimate=VALUES(population_estimate),x_km=VALUES(x_km),y_km=VALUES(y_km),radius_km=VALUES(radius_km),entry_scene_key=VALUES(entry_scene_key),description=VALUES(description);


INSERT INTO regional_routes
(route_key,region_slug,route_type,a_x_km,a_y_km,b_x_km,b_y_km,influence_width_km,description)
VALUES
('estrada_real_norte','arkanor','road',0.0,1180.0,430.0,2940.0,28.0,'Liga a capital à Vigília Verde e aos mercados da fronteira.'),
('rota_dos_celeiros','arkanor','road',-920.0,1680.0,0.0,1180.0,22.0,'Transporta grão entre Alvacampo e a Cidade de Arkanor.'),
('rota_do_horizonte','arkanor','road',-920.0,1680.0,-280.0,2600.0,18.0,'Conecta Alvacampo ao Mercado do Horizonte.'),
('estrada_dos_vinhedos','arkanor','road',-1340.0,540.0,0.0,1180.0,16.0,'Liga Orbel à capital por colinas cultivadas.'),
('rota_dos_sete_arcos','arkanor','road',0.0,1180.0,720.0,1450.0,20.0,'Conecta a capital à travessia de Sete Arcos.'),
('rota_fluvial_aurenta','arkanor','river_road',720.0,1450.0,1120.0,720.0,26.0,'Trecho navegável entre Sete Arcos e o Porto do Aurenta.'),
('aurenta_sul','arkanor','river_road',1120.0,720.0,820.0,-960.0,24.0,'Curso meridional do Aurenta até Nascente Serena.'),
('estrada_de_salgueiral','arkanor','road',1120.0,720.0,1450.0,-180.0,15.0,'Rota ribeirinha do porto até Salgueiral.')
ON DUPLICATE KEY UPDATE
region_slug=VALUES(region_slug),route_type=VALUES(route_type),a_x_km=VALUES(a_x_km),a_y_km=VALUES(a_y_km),b_x_km=VALUES(b_x_km),b_y_km=VALUES(b_y_km),influence_width_km=VALUES(influence_width_km),description=VALUES(description);


INSERT INTO region_borders_v2
(border_key,source_region_slug,target_region_slug,direction_key,axis_key,coordinate_limit_km,corridor_min_km,corridor_max_km,target_biome_slug,target_x_km,target_y_km,description)
VALUES
('arkanor_eldorwood','arkanor','eldorwood','norte','y',3000.0,-1100.0,1600.0,'pantanos_rios',430.0,-1540.0,'Canais agrícolas tornam-se cursos naturais, o trigo cede a juncos e raízes, e a névoa de Eldorwood ocupa o horizonte norte.'),
('eldorwood_arkanor','eldorwood','arkanor','sul','y',-1600.0,-1100.0,1600.0,'planicies_ferteis',430.0,2960.0,'A água se divide em canais medidos, árvores antigas cedem a plantações e marcos de propriedade anunciam Arkanor sem muralha ou portal.')
ON DUPLICATE KEY UPDATE
source_region_slug=VALUES(source_region_slug),target_region_slug=VALUES(target_region_slug),direction_key=VALUES(direction_key),axis_key=VALUES(axis_key),coordinate_limit_km=VALUES(coordinate_limit_km),corridor_min_km=VALUES(corridor_min_km),corridor_max_km=VALUES(corridor_max_km),target_biome_slug=VALUES(target_biome_slug),target_x_km=VALUES(target_x_km),target_y_km=VALUES(target_y_km),description=VALUES(description);


INSERT INTO npc_definitions_v2
(npc_key,name,race_name,role_name,home_settlement_key,faction_key,x_km,y_km,description,values_json,red_lines_json)
VALUES
('liora_sen','Liora Sen','Humana','pesquisadora do Manuscrito','cidade_arkanor','universidade_aberta',20.0,1200.0,'uma pesquisadora humana protege anotações com o corpo quando agentes do Conclave atravessam a praça',CAST('["prova", "acesso público", "consentimento"]' AS JSON),CAST('["teste humano forçado", "destruir registro"]' AS JSON)),
('astreon_vale','Astreon Vale','Ethari','estrategista do Conclave','cidade_arkanor','conclave_meridiano',-20.0,1220.0,'um Ethari translúcido mede distâncias entre pessoas antes de oferecer uma conversa privada',CAST('["previsão", "estabilidade", "conhecimento"]' AS JSON),CAST('["desperdício de dados", "violência sem cálculo"]' AS JSON)),
('odelia_arkan','Odelia Arkan','Humana','regente do Pacto Dourado','cidade_arkanor','regencia_arkanor',0.0,1260.0,'a regente escuta três assessores enquanto lê uma petição que nenhum deles mencionou',CAST('["paz", "comércio", "continuidade"]' AS JSON),CAST('["guerra civil", "ameaça ao abastecimento"]' AS JSON)),
('sorel_folha_livre','Sorel Folha-Livre','Sylvani','advogado de migrantes','balanca_baixa','assembleia_da_rua',100.0,1080.0,'um Sylvani organiza contratos por tipo de abuso, não por espécie de papel',CAST('["acolhimento", "autonomia", "lei pública"]' AS JSON),CAST('["trabalho escravo", "deportação coletiva"]' AS JSON)),
('bren_ferro_claro','Bren Ferro-Claro','Aureli','inspetora de pesos','sete_arcos','casa_das_medidas',710.0,1450.0,'uma Aureli recalibra uma balança antes de acusar um comerciante',CAST('["precisão", "trabalho", "reparação"]' AS JSON),CAST('["fraude de alimento", "suborno técnico"]' AS JSON)),
('nami_tres_correntes','Nami Três-Correntes','Aquari','capitã fluvial','porto_aurenta','coro_de_navegadores',1100.0,700.0,'uma Aquari calcula corrente, carga e humor da tripulação antes de aceitar passageiros',CAST('["fluxo livre", "tripulação", "acordo"]' AS JSON),CAST('["contaminar rio", "abandonar marinheiro"]' AS JSON)),
('ihra_sol_baixo','Ihra Sol-Baixo','Solari','astrônoma agrícola','campos_dourados','calendario_das_safras',-350.0,2040.0,'uma Solari compara sombras dos girassóis com datas riscadas num bastão',CAST('["ciclo", "previsão honesta", "alimento"]' AS JSON),CAST('["falsificar clima", "queimar safra"]' AS JSON)),
('iven_neve_mansa','Iven Neve-Mansa','Glacari','médico itinerante','vigilia_verde','vigias_da_fronteira',440.0,2920.0,'o médico Glacari reconhece viajantes vindos de Eldorwood pela umidade nas roupas',CAST('["cuidado", "travessia livre", "prudência"]' AS JSON),CAST('["abandonar exposto", "fechar fronteira por raça"]' AS JSON)),
('piri_luz_de_bolso','Piri Luz-de-Bolso','Luminari','mensageira judicial','cidade_arkanor','correio_dos_tribunais',40.0,1160.0,'uma Luminari carrega intimações, cartas de amor e recursos legais em bolsas separadas',CAST('["entrega", "beleza", "palavra dada"]' AS JSON),CAST('["interceptar carta", "enjaular mensageiro"]' AS JSON)),
('grom_ceifa_justa','Grom Ceifa-Justa','Kragari','organizador de trabalhadores','alvacampo','liga_dos_ceifadores',-900.0,1660.0,'um Kragari distribui água antes de iniciar uma reunião sobre pagamento',CAST('["honra", "salário", "proteção"]' AS JSON),CAST('["reter comida", "agredir trabalhador"]' AS JSON)),
('zizi_roda_torta','Zizi Roda-Torta','Ziraki','mecânica de carroças','mercado_horizonte','oficios_livres',-260.0,2590.0,'uma Ziraki diagnostica uma roda pelo som e cobra apenas depois de mostrar a rachadura',CAST('["invenção", "troca justa", "autoria"]' AS JSON),CAST('["roubar projeto", "culpar aprendiz"]' AS JSON)),
('mera_salgueiro','Mera Salgueiro','Ninfari','guardiã de margem','salgueiral','confluencia',1440.0,-160.0,'uma Ninfari mede erosão com os pés na água e marcas no tronco',CAST('["água", "comunidade", "memória"]' AS JSON),CAST('["privatizar nascente", "destruir berçário"]' AS JSON)),
('vesh_tinta_escura','Vesh Tinta-Escura','Umbrari','investigador independente','balanca_baixa','arquivo_da_lanterna',70.0,1090.0,'um Umbrari lê contratos à sombra e destaca cláusulas que ninguém pretendia explicar',CAST('["segredo responsável", "prova", "sobrevivência"]' AS JSON),CAST('["expor fonte", "fabricar confissão"]' AS JSON)),
('doma_sete_arcos','Doma Sete-Arcos','Ferrari','engenheira de pontes','sete_arcos','mestres_de_ponte',730.0,1470.0,'uma Ferrari testa vibrações enquanto carroças continuam atravessando',CAST('["segurança", "responsabilidade", "manutenção"]' AS JSON),CAST('["ocultar rachadura", "sobrecarregar ponte"]' AS JSON)),
('kaar_escama_cobre','Kaar Escama-de-Cobre','Drakari','guarda de testemunhas','cidade_arkanor','tribunal_do_pacto',10.0,1140.0,'um Drakari mantém a mão perto da arma e o corpo entre a testemunha e a multidão',CAST('["dever", "proteção", "testemunho"]' AS JSON),CAST('["ameaçar criança", "executar sem julgamento"]' AS JSON)),
('tavar_solo_aberto','Tavar Solo-Aberto','Voraki','agrimensor rural','vinhedos_orbel','cartografos_da_aurora',-1320.0,560.0,'um Voraki sente estacas enterradas e encontra limites movidos durante a noite',CAST('["território", "precisão", "acesso"]' AS JSON),CAST('["roubar terra", "apagar marco"]' AS JSON)),
('eloa_pedra_do_ceu','Eloa Pedra-do-Céu','Ethari','curadora da Nascente','nascente_serena','circulo_da_agua_clara',800.0,-940.0,'uma Ethari compara pulsações da água com a respiração de pacientes',CAST('["cura", "harmonia", "consentimento"]' AS JSON),CAST('["vender água sagrada", "experimentar sem permissão"]' AS JSON))
ON DUPLICATE KEY UPDATE
name=VALUES(name),race_name=VALUES(race_name),role_name=VALUES(role_name),home_settlement_key=VALUES(home_settlement_key),faction_key=VALUES(faction_key),x_km=VALUES(x_km),y_km=VALUES(y_km),description=VALUES(description),values_json=VALUES(values_json),red_lines_json=VALUES(red_lines_json);


SELECT
 (SELECT COUNT(*) FROM regional_settlements WHERE region_slug='arkanor') AS assentamentos,
 (SELECT COUNT(*) FROM regional_routes WHERE region_slug='arkanor') AS rotas,
 (SELECT COUNT(*) FROM npc_definitions_v2 WHERE home_settlement_key IN (SELECT settlement_key FROM regional_settlements WHERE region_slug='arkanor')) AS npcs,
 (SELECT COUNT(*) FROM region_borders_v2 WHERE border_key IN ('arkanor_eldorwood','eldorwood_arkanor')) AS fronteiras;
