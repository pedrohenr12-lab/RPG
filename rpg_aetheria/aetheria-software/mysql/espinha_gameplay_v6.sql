-- Região 6: A Espinha do Mundo. Execute após schema.sql, seed_core.sql e seed_biologia.sql.
USE aetheria_rpg;
CREATE TABLE IF NOT EXISTS locations (id INT AUTO_INCREMENT PRIMARY KEY,slug VARCHAR(120) UNIQUE NOT NULL,region_id INT NOT NULL,biome_id INT NULL,name VARCHAR(160) NOT NULL,location_type VARCHAR(80) NOT NULL,danger_base TINYINT NOT NULL DEFAULT 1,description TEXT NOT NULL,FOREIGN KEY(region_id) REFERENCES regions(id),FOREIGN KEY(biome_id) REFERENCES biomes(id));
CREATE TABLE IF NOT EXISTS biome_elements (biome_id INT NOT NULL,atomic_number SMALLINT NOT NULL,PRIMARY KEY(biome_id,atomic_number),FOREIGN KEY(biome_id) REFERENCES biomes(id) ON DELETE CASCADE,FOREIGN KEY(atomic_number) REFERENCES elements(atomic_number));
INSERT INTO regions(slug,name,continent,climate,lore) VALUES ('espinha_do_mundo','A Espinha do Mundo','Eudora','Alpino extremo, −20°C a 18°C, ventos muito fortes e gravidade de 0,7G.','Território ancestral dos anões, marcado por fortalezas escavadas e possíveis refúgios Vorath nas profundezas.') ON DUPLICATE KEY UPDATE name=VALUES(name),climate=VALUES(climate),lore=VALUES(lore);
INSERT INTO biomes(region_id,slug,name,climate,danger_base) SELECT id,'cordilheira_monumental','Cordilheira Monumental','Picos com neve permanente, −25°C a −5°C e ventos acima de 100 km/h.',5 FROM regions WHERE slug='espinha_do_mundo' ON DUPLICATE KEY UPDATE region_id=VALUES(region_id),name=VALUES(name),climate=VALUES(climate),danger_base=VALUES(danger_base);
INSERT INTO biomes(region_id,slug,name,climate,danger_base) SELECT id,'vales_profundos','Vales Profundos entre Picos','Sombra persistente, microclima de −10°C a 8°C e cavernas profundas.',4 FROM regions WHERE slug='espinha_do_mundo' ON DUPLICATE KEY UPDATE region_id=VALUES(region_id),name=VALUES(name),climate=VALUES(climate),danger_base=VALUES(danger_base);
INSERT INTO biomes(region_id,slug,name,climate,danger_base) SELECT id,'cavernas_gigantes','Cavernas Gigantes','Escuridão total, umidade alta e temperatura estável de aproximadamente 5°C.',5 FROM regions WHERE slug='espinha_do_mundo' ON DUPLICATE KEY UPDATE region_id=VALUES(region_id),name=VALUES(name),climate=VALUES(climate),danger_base=VALUES(danger_base);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('fortaleza_abandonada',(SELECT id FROM regions WHERE slug='espinha_do_mundo'),(SELECT id FROM biomes WHERE slug='cordilheira_monumental'),'Fortaleza Anã Abandonada','fortaleza',5,'Ruínas escavadas na montanha, fechadas desde guerras antigas e protegidas por mecanismos desconhecidos.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('pico_dos_ventos',(SELECT id FROM regions WHERE slug='espinha_do_mundo'),(SELECT id FROM biomes WHERE slug='cordilheira_monumental'),'Pico dos Ventos','pico',5,'Pico que perfura as nuvens; o vento pode carregar vozes ou enlouquecer escaladores.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('camara_de_pressium',(SELECT id FROM regions WHERE slug='espinha_do_mundo'),(SELECT id FROM biomes WHERE slug='cordilheira_monumental'),'Câmara de Pressium','caverna mineral',5,'Fenda de rocha e metal de alta estabilidade, próxima a veios antigos.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('vale_das_sombras',(SELECT id FROM regions WHERE slug='espinha_do_mundo'),(SELECT id FROM biomes WHERE slug='vales_profundos'),'Vale das Sombras','vale',4,'Vale frio de pouca luz, onde cervos escuros e raposas percorrem caminhos estreitos.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('entrada_dos_ecos',(SELECT id FROM regions WHERE slug='espinha_do_mundo'),(SELECT id FROM biomes WHERE slug='vales_profundos'),'Entrada dos Ecos','caverna',4,'Boca de caverna onde Líquens-de-Eco reagem ao som e corvos imitam chamados.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('veio_de_vynium',(SELECT id FROM regions WHERE slug='espinha_do_mundo'),(SELECT id FROM biomes WHERE slug='vales_profundos'),'Veio de Vynium','veio mineral',5,'Veio natural comprimido entre paredes abruptas, guardado por rumores cristalinos.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('cidade_soterrada',(SELECT id FROM regions WHERE slug='espinha_do_mundo'),(SELECT id FROM biomes WHERE slug='cavernas_gigantes'),'Cidade Anã Soterrada','ruína subterrânea',5,'Estruturas antigas parcialmente engolidas por cristais e raízes cegas.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('camara_de_luminite',(SELECT id FROM regions WHERE slug='espinha_do_mundo'),(SELECT id FROM biomes WHERE slug='cavernas_gigantes'),'Câmara de Luminite','caverna cristalina',5,'Câmara iluminada sem chama por Luminite puro e fungos azuis.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('lago_sem_luz',(SELECT id FROM regions WHERE slug='espinha_do_mundo'),(SELECT id FROM biomes WHERE slug='cavernas_gigantes'),'Lago sem Luz','lago subterrâneo',5,'Lago de peixes cegos e salamandras, onde vibrações substituem visão.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,129 FROM biomes WHERE slug='cordilheira_monumental';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,119 FROM biomes WHERE slug='cordilheira_monumental';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,124 FROM biomes WHERE slug='cordilheira_monumental';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,127 FROM biomes WHERE slug='cordilheira_monumental';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,119 FROM biomes WHERE slug='vales_profundos';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,133 FROM biomes WHERE slug='vales_profundos';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,127 FROM biomes WHERE slug='cavernas_gigantes';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,143 FROM biomes WHERE slug='cavernas_gigantes';
INSERT INTO species(slug,common_name,scientific_name,kingdom,class_name,behavior,threat,description,edible,poisonous,legendary) VALUES
('espinha_flora_liquen_de_pico_da_espinha','Líquen-de-Pico da Espinha',NULL,'flora','Líquen alpino','pacific',0,'Vegetação de altitudes acima de cinco mil metros, em padrões fractais.',FALSE,FALSE,FALSE),
('espinha_flora_musgo_de_gelo_de_altitude','Musgo-de-Gelo de Altitude',NULL,'flora','Musgo alpino','pacific',0,'Tapete fino sobre rochas, extremamente resistente.',FALSE,FALSE,FALSE),
('espinha_flora_flor_de_neve_eterna','Flor-de-Neve Eterna',NULL,'flora','Flor alpina rara','mystic',1,'Flor raríssima de glaciares antigos, com pétalas cristalinas.',FALSE,FALSE,FALSE),
('espinha_flora_fungo_de_pressium','Fungo-de-Pressium',NULL,'flora','Fungo mineral','pacific',0,'Cresce em fendas protegidas, com textura metálica.',FALSE,FALSE,FALSE),
('espinha_flora_arbusto_anao_de_montanha','Arbusto-Anão de Montanha',NULL,'flora','Arbusto alpino','pacific',0,'Arbusto baixo e resistente, de raízes muito profundas.',FALSE,FALSE,FALSE),
('espinha_flora_musgo_de_sombra','Musgo-de-Sombra',NULL,'flora','Musgo de vale','pacific',0,'Musgo verde-escuro de pouca luz.',FALSE,FALSE,FALSE),
('espinha_flora_samambaia_de_vale_da_espinha','Samambaia-de-Vale da Espinha',NULL,'flora','Samambaia ribeirinha','pacific',0,'Folhas longas e delicadas que crescem perto de rios frios.',FALSE,FALSE,FALSE),
('espinha_flora_flor_de_cristal','Flor-de-Cristal',NULL,'flora','Flor mineral','mystic',1,'Cresce junto a veios de Vynium, com pétalas translúcidas.',FALSE,FALSE,FALSE),
('espinha_flora_liquen_de_eco','Líquen-de-Eco',NULL,'flora','Líquen ressonante','mystic',1,'Vibra levemente quando há som; cresce em entradas de cavernas.',FALSE,FALSE,FALSE),
('espinha_flora_arbusto_de_cobre','Arbusto-de-Cobre',NULL,'flora','Arbusto mineral','pacific',0,'Folhas de tom metálico e raízes que concentram minerais.',FALSE,FALSE,FALSE),
('espinha_flora_fungo_luminoso_da_espinha','Fungo-Luminoso da Espinha',NULL,'flora','Fungo de caverna','pacific',0,'Fonte principal de luz natural, em azul, verde e roxo.',FALSE,FALSE,FALSE),
('espinha_flora_musgo_de_caverna_da_espinha','Musgo-de-Caverna da Espinha',NULL,'flora','Musgo de caverna','pacific',0,'Cresce em paredes úmidas e tem textura macia.',FALSE,FALSE,FALSE),
('espinha_flora_flor_de_luminite','Flor-de-Luminite',NULL,'flora','Flor de caverna rara','mystic',1,'Só cresce perto de cristais de Luminite puro.',FALSE,FALSE,FALSE),
('espinha_flora_liquen_de_harmonix','Líquen-de-Harmonix',NULL,'flora','Líquen ressonante','mystic',1,'Emite sons baixos e constantes; cresce em colônias.',FALSE,FALSE,FALSE),
('espinha_flora_raiz_cega','Raiz-Cega',NULL,'flora','Flora subterrânea','pacific',0,'Planta sem folhas que absorve minerais e umidade.',FALSE,FALSE,FALSE),
('espinha_fauna_urso_de_montanha','Urso-de-Montanha',NULL,'fauna','Mamífero predador','predator',4,'Menor que o urso glacial de Frostreach, mas agressivo e territorial.',FALSE,FALSE,FALSE),
('espinha_fauna_lobo_de_altitude','Lobo-de-Altitude',NULL,'fauna','Mamífero predador','predator',3,'Pelagem cinza-clara; caça em pequenos grupos.',FALSE,FALSE,FALSE),
('espinha_fauna_marmota_de_rocha','Marmota-de-Rocha',NULL,'fauna','Roedor','pacific',0,'Vive em colônias e alerta outras marmotas com gritos agudos.',FALSE,FALSE,FALSE),
('espinha_fauna_dragao_de_pedra_anciao','Dragão-de-Pedra Ancião',NULL,'fauna','Criatura lendária','legendary',5,'Criatura colossal de pele de rocha viva, quase nunca observada.',FALSE,FALSE,TRUE),
('espinha_fauna_guardiao_de_pressium','Guardião de Pressium',NULL,'fauna','Entidade lendária','legendary',5,'Entidade de rocha e metal que protege fortalezas anãs abandonadas.',FALSE,FALSE,TRUE),
('espinha_fauna_espirito_do_vento','Espírito-do-Vento',NULL,'fauna','Entidade lendária','legendary',4,'Vozes que viajam no vento e podem guiar ou enlouquecer escaladores.',FALSE,FALSE,TRUE),
('espinha_fauna_cervo_de_vale','Cervo-de-Vale',NULL,'fauna','Mamífero herbívoro','pacific',1,'Pelagem escura; vive em pequenos grupos.',FALSE,FALSE,FALSE),
('espinha_fauna_raposa_de_montanha','Raposa-de-Montanha',NULL,'fauna','Mamífero predador','predator',1,'Caçadora solitária e inteligente.',FALSE,FALSE,FALSE),
('espinha_fauna_aguia_de_vale','Águia-de-Vale',NULL,'fauna','Ave de rapina','predator',2,'Menor que a Águia-das-Nuvens, porém muito ágil.',FALSE,FALSE,FALSE),
('espinha_fauna_serpente_de_rocha','Serpente-de-Rocha',NULL,'fauna','Réptil','predator',2,'Camuflada em fendas e rochas.',FALSE,FALSE,FALSE),
('espinha_fauna_corvo_de_eco','Corvo-de-Eco',NULL,'fauna','Ave','neutral',2,'Imita sons com precisão anômala graças ao Resonum.',FALSE,FALSE,FALSE),
('espinha_fauna_eco_vivo_dos_vales','Eco-Vivo dos Vales',NULL,'fauna','Entidade lendária','legendary',4,'Sons antigos presos nas paredes do vale.',FALSE,FALSE,TRUE),
('espinha_fauna_guardiao_de_vynium','Guardião de Vynium',NULL,'fauna','Entidade lendária','legendary',5,'Criatura cristalina que protege veios de metal raro.',FALSE,FALSE,TRUE),
('espinha_fauna_sombra_dos_vales','Sombra-dos-Vales',NULL,'fauna','Entidade lendária','legendary',5,'Presença de penumbra ligada a possíveis restos Vorath.',FALSE,FALSE,TRUE),
('espinha_fauna_morcego_gigante_de_caverna','Morcego-Gigante de Caverna',NULL,'fauna','Mamífero voador','neutral',2,'Enxames grandes que navegam por ecolocalização.',FALSE,FALSE,FALSE),
('espinha_fauna_salamandra_cega','Salamandra-Cega',NULL,'fauna','Anfíbio','pacific',1,'Vive em lagos subterrâneos, de pele pálida e sensível.',FALSE,FALSE,FALSE),
('espinha_fauna_aranha_de_cristal','Aranha-de-Cristal',NULL,'fauna','Aracnídeo','predator',3,'Teia brilha com Luminite e veneno paralisa.',FALSE,TRUE,FALSE),
('espinha_fauna_peixe_cego','Peixe-Cego',NULL,'fauna','Peixe','pacific',0,'Habita lagos escuros e responde a vibrações.',FALSE,FALSE,FALSE),
('espinha_fauna_rato_de_caverna','Rato-de-Caverna',NULL,'fauna','Roedor','neutral',0,'Adaptado à escuridão total e com excelente olfato.',FALSE,FALSE,FALSE),
('espinha_fauna_guardiao_de_luminite','Guardião de Luminite',NULL,'fauna','Entidade lendária','legendary',5,'Cristais vivos que protegem as câmaras profundas.',FALSE,FALSE,TRUE),
('espinha_fauna_eco_anciao','Eco-Ancião',NULL,'fauna','Entidade lendária','legendary',5,'Vozes de anões e Vorath presas nas paredes podem enlouquecer quem escuta demais.',FALSE,FALSE,TRUE),
('espinha_fauna_sombra_vorath','Sombra-Vorath',NULL,'fauna','Entidade lendária','legendary',5,'Possível resquício da invasão escondido nas profundezas absolutas.',FALSE,FALSE,TRUE),
('espinha_fauna_dragao_de_caverna','Dragão-de-Caverna',NULL,'fauna','Criatura lendária','legendary',5,'Lenda anã: um dragão de cristal dorme nas câmaras mais profundas.',FALSE,FALSE,TRUE)
ON DUPLICATE KEY UPDATE common_name=VALUES(common_name),class_name=VALUES(class_name),behavior=VALUES(behavior),threat=VALUES(threat),description=VALUES(description),edible=VALUES(edible),poisonous=VALUES(poisonous),legendary=VALUES(legendary);
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,3 FROM species s JOIN biomes b WHERE b.slug='cordilheira_monumental' AND s.slug IN ('espinha_flora_liquen_de_pico_da_espinha','espinha_flora_musgo_de_gelo_de_altitude','espinha_flora_flor_de_neve_eterna','espinha_flora_fungo_de_pressium','espinha_flora_arbusto_anao_de_montanha','espinha_fauna_urso_de_montanha','espinha_fauna_lobo_de_altitude','espinha_fauna_marmota_de_rocha','espinha_fauna_dragao_de_pedra_anciao','espinha_fauna_guardiao_de_pressium','espinha_fauna_espirito_do_vento');
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,6 FROM species s JOIN biomes b WHERE b.slug='vales_profundos' AND s.slug IN ('espinha_flora_musgo_de_sombra','espinha_flora_samambaia_de_vale_da_espinha','espinha_flora_flor_de_cristal','espinha_flora_liquen_de_eco','espinha_flora_arbusto_de_cobre','espinha_fauna_cervo_de_vale','espinha_fauna_raposa_de_montanha','espinha_fauna_aguia_de_vale','espinha_fauna_serpente_de_rocha','espinha_fauna_corvo_de_eco','espinha_fauna_eco_vivo_dos_vales','espinha_fauna_guardiao_de_vynium','espinha_fauna_sombra_dos_vales');
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,3 FROM species s JOIN biomes b WHERE b.slug='cavernas_gigantes' AND s.slug IN ('espinha_flora_fungo_luminoso_da_espinha','espinha_flora_musgo_de_caverna_da_espinha','espinha_flora_flor_de_luminite','espinha_flora_liquen_de_harmonix','espinha_flora_raiz_cega','espinha_fauna_morcego_gigante_de_caverna','espinha_fauna_salamandra_cega','espinha_fauna_aranha_de_cristal','espinha_fauna_peixe_cego','espinha_fauna_rato_de_caverna','espinha_fauna_guardiao_de_luminite','espinha_fauna_eco_anciao','espinha_fauna_sombra_vorath','espinha_fauna_dragao_de_caverna');
-- Espécies de altitude e caverna já catalogadas, ligadas sem duplicação.
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,2 FROM species s JOIN biomes b WHERE b.slug='cordilheira_monumental' AND s.slug IN ('frost_fauna_aguia_das_nuvens','frost_fauna_cabra_das_presas','frost_fauna_urso_glacial_das_presas','frost_fauna_lobo_de_gelo','mamifero_cabra_gigante','mamifero_ovelha_de_rocha','mamifero_gato_das_rochas','oviparo_dragao_de_rocha','lendario_colosso_de_pedra');
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,3 FROM species s JOIN biomes b WHERE b.slug='vales_profundos' AND s.slug IN ('frost_fauna_raposa_artica','frost_fauna_corvo_de_gelo','eldor_fauna_cervo_das_colinas','mamifero_tatu_fractal','mamifero_lobo_resonante','oviparo_coruja_clara','oviparo_corvo_inteligente','lendario_predador_sombrio');
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,2 FROM species s JOIN biomes b WHERE b.slug='cavernas_gigantes' AND s.slug IN ('frost_flora_fungo_luminoso','frost_flora_musgo_de_caverna','frost_fauna_aranha_de_gelo','oviparo_lagarto_predador','oviparo_serpente_resonante','oviparo_predador_abissal','lendario_serpente_de_vidro','lendario_entidade_celestyn');
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,124 FROM species WHERE slug='espinha_flora_liquen_de_pico_da_espinha';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='espinha_flora_musgo_de_gelo_de_altitude';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='espinha_flora_flor_de_neve_eterna';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,119 FROM species WHERE slug='espinha_flora_flor_de_neve_eterna';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,129 FROM species WHERE slug='espinha_flora_fungo_de_pressium';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,119 FROM species WHERE slug='espinha_flora_arbusto_anao_de_montanha';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='espinha_flora_samambaia_de_vale_da_espinha';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,119 FROM species WHERE slug='espinha_flora_flor_de_cristal';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,133 FROM species WHERE slug='espinha_flora_liquen_de_eco';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='espinha_flora_fungo_luminoso_da_espinha';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='espinha_flora_musgo_de_caverna_da_espinha';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='espinha_flora_flor_de_luminite';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,143 FROM species WHERE slug='espinha_flora_liquen_de_harmonix';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,129 FROM species WHERE slug='espinha_flora_raiz_cega';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='espinha_fauna_dragao_de_pedra_anciao';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,129 FROM species WHERE slug='espinha_fauna_guardiao_de_pressium';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,133 FROM species WHERE slug='espinha_fauna_espirito_do_vento';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,133 FROM species WHERE slug='espinha_fauna_corvo_de_eco';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,133 FROM species WHERE slug='espinha_fauna_eco_vivo_dos_vales';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,119 FROM species WHERE slug='espinha_fauna_guardiao_de_vynium';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,133 FROM species WHERE slug='espinha_fauna_morcego_gigante_de_caverna';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='espinha_fauna_salamandra_cega';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='espinha_fauna_aranha_de_cristal';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,133 FROM species WHERE slug='espinha_fauna_peixe_cego';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='espinha_fauna_guardiao_de_luminite';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,133 FROM species WHERE slug='espinha_fauna_eco_anciao';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='espinha_fauna_dragao_de_caverna';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='espinha_fauna_dragao_de_caverna';
INSERT IGNORE INTO resources(slug,name,resource_type,description,value_base) VALUES ('fungo_pressium','Fungo de Pressium','alchemy','Fungo mineral de textura metálica.',18),('flor_neve_eterna','Flor de Neve Eterna','alchemy','Flor cristalina rara de glaciar.',50),('flor_de_cristal','Flor de Cristal','alchemy','Flor translúcida que cresce perto de Vynium.',22),('liquen_de_eco','Líquen de Eco','alchemy','Líquen que reage a som.',14),('cobre_de_arbusto','Cobre de Arbusto','ore','Mineral concentrado em raízes de arbusto.',10),('fungo_luminoso_espinha','Fungo Luminoso da Espinha','herb','Fonte de luz natural e ingrediente de caverna.',11),('flor_luminite','Flor de Luminite','alchemy','Flor raríssima perto de cristais puros.',45),('seda_de_cristal','Seda de Cristal','hide','Seda brilhante de aranhas de caverna.',16),('peixe_cego','Peixe-Cego','food','Peixe de lago subterrâneo.',7);
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,2 FROM species s JOIN resources r WHERE s.slug='espinha_flora_fungo_de_pressium' AND r.slug='fungo_pressium';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,1 FROM species s JOIN resources r WHERE s.slug='espinha_flora_flor_de_neve_eterna' AND r.slug='flor_neve_eterna';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,2 FROM species s JOIN resources r WHERE s.slug='espinha_flora_flor_de_cristal' AND r.slug='flor_de_cristal';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,2 FROM species s JOIN resources r WHERE s.slug='espinha_flora_liquen_de_eco' AND r.slug='liquen_de_eco';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,2 FROM species s JOIN resources r WHERE s.slug='espinha_flora_arbusto_de_cobre' AND r.slug='cobre_de_arbusto';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,3 FROM species s JOIN resources r WHERE s.slug='espinha_flora_fungo_luminoso_da_espinha' AND r.slug='fungo_luminoso_espinha';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,1 FROM species s JOIN resources r WHERE s.slug='espinha_flora_flor_de_luminite' AND r.slug='flor_luminite';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,2 FROM species s JOIN resources r WHERE s.slug='espinha_fauna_aranha_de_cristal' AND r.slug='seda_de_cristal';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,3 FROM species s JOIN resources r WHERE s.slug='espinha_fauna_peixe_cego' AND r.slug='peixe_cego';
SELECT b.name AS bioma,COUNT(sb.species_id) AS especies_ligadas FROM biomes b LEFT JOIN species_biomes sb ON sb.biome_id=b.id WHERE b.slug IN ('cordilheira_monumental','vales_profundos','cavernas_gigantes') GROUP BY b.id,b.name ORDER BY b.name;



-- Camada jogável v6: assentamentos, rotas, fronteiras, NPCs e economia persistente.
CREATE TABLE IF NOT EXISTS regional_settlements (
    settlement_key VARCHAR(120) PRIMARY KEY, region_slug VARCHAR(80) NOT NULL,
    biome_slug VARCHAR(80) NULL, name VARCHAR(160) NOT NULL, settlement_type VARCHAR(80) NOT NULL,
    population_estimate INT NOT NULL DEFAULT 0, x_km DECIMAL(10,2) NOT NULL, y_km DECIMAL(10,2) NOT NULL,
    radius_km DECIMAL(8,2) NOT NULL DEFAULT 1, entry_scene_key VARCHAR(160) NOT NULL, description TEXT NOT NULL,
    INDEX idx_settlement_region_position (region_slug,x_km,y_km)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS regional_routes (
    route_key VARCHAR(120) PRIMARY KEY, region_slug VARCHAR(80) NOT NULL, route_type VARCHAR(60) NOT NULL DEFAULT 'road',
    a_x_km DECIMAL(10,2) NOT NULL, a_y_km DECIMAL(10,2) NOT NULL, b_x_km DECIMAL(10,2) NOT NULL,
    b_y_km DECIMAL(10,2) NOT NULL, influence_width_km DECIMAL(8,2) NOT NULL, description TEXT NULL,
    INDEX idx_route_region (region_slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS region_borders_v2 (
    border_key VARCHAR(120) PRIMARY KEY, source_region_slug VARCHAR(80) NOT NULL, target_region_slug VARCHAR(80) NOT NULL,
    direction_key VARCHAR(20) NOT NULL, axis_key CHAR(1) NOT NULL, coordinate_limit_km DECIMAL(10,2) NOT NULL,
    corridor_min_km DECIMAL(10,2) NOT NULL, corridor_max_km DECIMAL(10,2) NOT NULL,
    target_biome_slug VARCHAR(80) NOT NULL, target_x_km DECIMAL(10,2) NOT NULL, target_y_km DECIMAL(10,2) NOT NULL,
    description TEXT NOT NULL, INDEX idx_border_source (source_region_slug,direction_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS npc_definitions_v2 (
    npc_key VARCHAR(120) PRIMARY KEY, name VARCHAR(160) NOT NULL, race_name VARCHAR(120) NOT NULL,
    role_name VARCHAR(160) NOT NULL, home_settlement_key VARCHAR(120) NULL, faction_key VARCHAR(120) NULL,
    x_km DECIMAL(10,2) NOT NULL, y_km DECIMAL(10,2) NOT NULL, description TEXT NOT NULL,
    values_json JSON NOT NULL, red_lines_json JSON NOT NULL,
    INDEX idx_npc_home (home_settlement_key), INDEX idx_npc_position (x_km,y_km)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS regional_market_offers (
    settlement_key VARCHAR(120) NOT NULL, item_key VARCHAR(120) NOT NULL, item_name VARCHAR(160) NOT NULL,
    currency_key VARCHAR(40) NOT NULL DEFAULT 'coroas', buy_price INT NOT NULL, sell_price INT NOT NULL,
    water_index DECIMAL(6,2) NOT NULL DEFAULT 1.00, stock_state VARCHAR(40) NOT NULL DEFAULT 'available',
    PRIMARY KEY (settlement_key,item_key), INDEX idx_market_item (item_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO regional_settlements
(settlement_key,region_slug,biome_slug,name,settlement_type,population_estimate,x_km,y_km,radius_km,entry_scene_key,description) VALUES
('dhor_karun','espinha_do_mundo','vales_profundos','Dhor-Karun','capital fortaleza',156000,-260.0,320.0,38.0,'r6_dhor_karun_portao_das_cargas','Capital Aureli escavada em sete níveis, onde conselhos de mineração, ventilação e carga governam a montanha.'),
('cume_vyn','espinha_do_mundo','cordilheira_monumental','Cume Vyn','fortaleza de altitude',28000,-820.0,2240.0,18.0,'r6_cume_vyn_eclusa_do_ar','Fortaleza acima das nuvens, dedicada a Pressium, meteorologia e resgate de altitude.'),
('ponte_nuvens','espinha_do_mundo','cordilheira_monumental','Ponte das Nuvens','cidade suspensa',19000,760.0,1900.0,16.0,'r6_ponte_nuvens_casa_dos_cabos','Cidade construída em cabos, plataformas e paredes opostas de uma garganta monumental.'),
('vale_martelo','espinha_do_mundo','vales_profundos','Vale do Martelo','cidade de vale',52000,1120.0,420.0,25.0,'r6_vale_martelo_terracos_de_degelo','Terraços agrícolas, moinhos e forjas compartilham uma vazão curta e um inverno longo.'),
('ninho_alto','espinha_do_mundo','cordilheira_monumental','Ninho Alto','vila aérea',7800,-1880.0,1520.0,11.0,'r6_ninho_alto_plataforma_dos_ventos','Vila Luminari e Drakari que observa migrações, tempestades e rotas acima das nuvens.'),
('forja_profunda','espinha_do_mundo','cavernas_gigantes','Forja Profunda','cidade industrial subterrânea',61000,-620.0,-1120.0,27.0,'r6_forja_profunda_elevador_termico','Centro Ferrari e Aureli de fundição, ventilação e máquinas antigas alimentadas por calor subterrâneo.'),
('luminaria_baixa','espinha_do_mundo','cavernas_gigantes','Luminária Baixa','cidade de cavernas',34000,720.0,-1720.0,21.0,'r6_luminaria_baixa_jardim_de_fungos','Cidade iluminada por fungos e Luminite, cercada por fazendas subterrâneas e regras rígidas de coleta.'),
('lago_harmonico','espinha_do_mundo','cavernas_gigantes','Lago Harmônico','porto subterrâneo',17000,1760.0,-980.0,16.0,'r6_lago_harmonico_cais_sem_vento','Porto Aquari e Ninfari num lago cujas ondas e ecos regulam navegação e medicina.'),
('vigilia_branca','espinha_do_mundo','cordilheira_monumental','Vigília Branca','posto de fronteira',4200,-1800.0,2920.0,9.0,'r6_vigilia_branca_marco_da_neve','Posto do passo setentrional que liga a Espinha às Presas de Gelo de Frostreach.'),
('portao_de_pedra','espinha_do_mundo','vales_profundos','Portão de Pedra','posto de fronteira',6600,2920.0,-1180.0,10.0,'r6_portao_de_pedra_arco_oriental','Entreposto oriental de caravanas, água e ferramentas na rota física para Stonevale.'),
('refugio_velado','espinha_do_mundo','cavernas_gigantes','Refúgio Velado','cidade oculta',11500,-1960.0,-2140.0,14.0,'r6_refugio_velado_porta_sem_brasao','Cidade Vorath, Aureli e Ferrari ocultada depois da guerra, sustentada por colaboração e silêncio.')
ON DUPLICATE KEY UPDATE region_slug=VALUES(region_slug),biome_slug=VALUES(biome_slug),name=VALUES(name),settlement_type=VALUES(settlement_type),population_estimate=VALUES(population_estimate),x_km=VALUES(x_km),y_km=VALUES(y_km),radius_km=VALUES(radius_km),entry_scene_key=VALUES(entry_scene_key),description=VALUES(description);

INSERT INTO regional_routes
(route_key,region_slug,route_type,a_x_km,a_y_km,b_x_km,b_y_km,influence_width_km,description) VALUES
('estrada_das_sete_cargas','espinha_do_mundo','mountain',-260.0,320.0,1120.0,420.0,24.0,'Rota física da Espinha: estrada das sete cargas.'),
('trilha_do_cume','espinha_do_mundo','mountain',-260.0,320.0,-820.0,2240.0,18.0,'Rota física da Espinha: trilha do cume.'),
('cabos_das_nuvens','espinha_do_mundo','mountain',-820.0,2240.0,760.0,1900.0,13.0,'Rota física da Espinha: cabos das nuvens.'),
('rota_do_ninho','espinha_do_mundo','mountain',-820.0,2240.0,-1880.0,1520.0,12.0,'Rota física da Espinha: rota do ninho.'),
('elevador_da_forja','espinha_do_mundo','mountain',-260.0,320.0,-620.0,-1120.0,22.0,'Rota física da Espinha: elevador da forja.'),
('galeria_luminosa','espinha_do_mundo','mountain',-620.0,-1120.0,720.0,-1720.0,19.0,'Rota física da Espinha: galeria luminosa.'),
('canal_harmonico','espinha_do_mundo','mountain',720.0,-1720.0,1760.0,-980.0,16.0,'Rota física da Espinha: canal harmonico.'),
('caminho_da_vigilia','espinha_do_mundo','mountain',-820.0,2240.0,-1800.0,2920.0,14.0,'Rota física da Espinha: caminho da vigilia.'),
('estrada_oriental','espinha_do_mundo','mountain',1120.0,420.0,2920.0,-1180.0,20.0,'Rota física da Espinha: estrada oriental.'),
('galeria_velada','espinha_do_mundo','mountain',-620.0,-1120.0,-1960.0,-2140.0,10.0,'Rota física da Espinha: galeria velada.')
ON DUPLICATE KEY UPDATE region_slug=VALUES(region_slug),route_type=VALUES(route_type),a_x_km=VALUES(a_x_km),a_y_km=VALUES(a_y_km),b_x_km=VALUES(b_x_km),b_y_km=VALUES(b_y_km),influence_width_km=VALUES(influence_width_km),description=VALUES(description);

INSERT INTO region_borders_v2
(border_key,source_region_slug,target_region_slug,direction_key,axis_key,coordinate_limit_km,corridor_min_km,corridor_max_km,target_biome_slug,target_x_km,target_y_km,description) VALUES
('espinha_frostreach','espinha_do_mundo','frostreach','norte','y',3000,-2600,-1300,'presas_de_gelo',-1800,-2960,'O passo de altitude desce fisicamente para as geleiras de Frostreach.'),
('frostreach_espinha','frostreach','espinha_do_mundo','sul','y',-3000,-2600,-1300,'cordilheira_monumental',-1800,2960,'As geleiras tornam-se rampas de rocha da Espinha do Mundo.'),
('espinha_stonevale','espinha_do_mundo','stonevale','leste','x',3000,-1900,-650,'platos_aridos',-2960,-1180,'O vale abre e alcança os platôs áridos de Stonevale.'),
('stonevale_espinha','stonevale','espinha_do_mundo','oeste','x',-3000,-1900,-650,'vales_profundos',2960,-1180,'Os platôs entram fisicamente nos vales profundos da Espinha.')
ON DUPLICATE KEY UPDATE source_region_slug=VALUES(source_region_slug),target_region_slug=VALUES(target_region_slug),direction_key=VALUES(direction_key),axis_key=VALUES(axis_key),coordinate_limit_km=VALUES(coordinate_limit_km),corridor_min_km=VALUES(corridor_min_km),corridor_max_km=VALUES(corridor_max_km),target_biome_slug=VALUES(target_biome_slug),target_x_km=VALUES(target_x_km),target_y_km=VALUES(target_y_km),description=VALUES(description);

INSERT INTO npc_definitions_v2
(npc_key,name,race_name,role_name,home_settlement_key,faction_key,x_km,y_km,description,values_json,red_lines_json) VALUES
('mara_viga_clara','Mara Viga-Clara','Ferrari','engenheira estrutural e possível companheira','forja_profunda','oficina_da_carga_viva',-600.0,-1100.0,'uma Ferrari escuta tensões em pilares e procura libertar o dragão sem condenar cidades','["segurança", "liberdade", "prova"]','["sacrificar trabalhador", "manter escravidão por conveniência"]'),
('tarek_sem_ceu','Tarek Sem-Céu','Vorath','cartógrafo do refúgio e possível companheiro','refugio_velado','assembleia_do_refugio',-1940.0,-2120.0,'um jovem Vorath deseja reconhecimento público sem entregar famílias à vingança','["povo", "verdade", "autonomia"]','["expor criança", "apagar colaboração antiga"]'),
('dhoram_ferro_vivo','Dhoram Ferro-Vivo','Aureli','Primeiro Mestre das Cargas','dhor_karun','conselho_das_sete_cargas',-240.0,340.0,'um ancião Aureli sabe que a prosperidade depende de decisões enterradas','["continuidade", "tradição", "responsabilidade"]','["colapso deliberado", "destruir arquivo"]'),
('lia_passo_curto','Lia Passo-Curto','Humana','mensageira de montanha','vigilia_branca','correio_dos_passos',-1780.0,2900.0,'uma humana mede distância por abrigos e nunca promete chegada antes do clima','["entrega", "honestidade", "retorno"]','["abandonar parceiro", "falsificar rota"]'),
('silven_raiz_na_pedra','Silven Raiz-na-Pedra','Sylvani','agricultor de terraços','vale_martelo','comuna_do_degelo',1100.0,440.0,'um Sylvani mantém raízes vivas em paredes que recebem poucas horas de sol','["cultivo", "água", "continuidade"]','["envenenar degelo", "queimar terraço"]'),
('nami_onda_funda','Nami Onda-Funda','Aquari','pilota do lago subterrâneo','lago_harmonico','barqueiros_sem_vento',1780.0,-960.0,'uma Aquari navega por vibrações e correntes invisíveis','["tripulação", "água limpa", "resgate"]','["afundar refugiado", "contaminar lago"]'),
('sael_sol_na_neve','Sael Sol-na-Neve','Solari','meteorologista de cume','cume_vyn','observatorio_das_sete_pressoes',-800.0,2260.0,'uma Solari lê halos e cristais de gelo para prever vento','["método", "alerta", "clareza"]','["reter previsão", "simular resgate"]'),
('ivel_geada_lenta','Ivel Geada-Lenta','Glacari','guia de aclimatação','cume_vyn','casa_do_ar_lento',-840.0,2220.0,'um Glacari ensina o corpo a aceitar altitude sem transformar resistência em orgulho','["paciência", "cuidado", "ritmo"]','["forçar aclimatação", "abandonar hipóxico"]'),
('pali_asa_de_corda','Pali Asa-de-Corda','Luminari','vigia de correntes aéreas','ninho_alto','ninho_dos_ventos',-1860.0,1540.0,'uma Luminari plana entre plataformas e registra aves migratórias','["beleza", "precisão", "liberdade"]','["cortar asa", "enjaular migração"]'),
('garr_martelo_calmo','Garr Martelo-Calmo','Kragari','chefe de resgate','ponte_nuvens','brigada_das_cordas',780.0,1880.0,'um Kragari usa força para estabilizar cabos e nunca atravessa uma vítima sem ancoragem','["equipe", "honra", "proteção"]','["duelo na ponte", "abandonar caído"]'),
('zikka_pulso_fino','Zikka Pulso-Fino','Ziraki','mecânica de ventilação','forja_profunda','oficina_dos_foles',-640.0,-1140.0,'uma Ziraki constrói sensores simples para galerias onde instrumentos antigos mentem','["reparo", "autoria", "acesso"]','["selar saída", "roubar projeto"]'),
('nira_lago_escuro','Nira Lago-Escuro','Ninfari','curadora subterrânea','lago_harmonico','casa_das_aguas_fundas',1740.0,-1000.0,'uma Ninfari trata pulmões de mineiros e mapeia toxinas pela água','["cura", "consentimento", "pesquisa"]','["teste forçado", "negar tratamento"]'),
('umbra_sete_lampadas','Umbra Sete-Lâmpadas','Umbrari','exploradora de galerias','luminaria_baixa','vigias_da_escuridao',700.0,-1700.0,'uma Umbrari diferencia ausência de luz, emboscada e ar parado','["silêncio", "orientação", "retorno"]','["apagar marca", "deixar desaparecido"]'),
('kaar_escama_termica','Kaar Escama-Térmica','Drakari','mediador com dragões','ninho_alto','guardas_da_coluna',-1900.0,1500.0,'um Drakari percebe calor sob pedra e rejeita tratar dragões como máquinas','["dignidade", "dever", "memória"]','["torturar dragão", "quebrar juramento"]'),
('ethra_frequencia_baixa','Ethra Frequência-Baixa','Ethari','pesquisadora de Harmonix','luminaria_baixa','arquivo_do_meridiano',740.0,-1740.0,'uma Ethari ouve padrões simétricos que antecedem tremores','["conhecimento", "harmonia", "publicidade"]','["falsificar dado", "ocultar risco público"]'),
('toru_pe_de_rocha','Toru Pé-de-Rocha','Voraki','cartógrafa sísmica','portao_de_pedra','mapas_da_carga',2900.0,-1160.0,'uma Voraki sente vibração e prova que mineração recente rompeu amortecedores antigos','["território", "evidência", "reparação"]','["culpar povo sem prova", "minerar amortecedor"]'),
('orik_sem_turno','Orik Sem-Turno','Aureli','representante dos mineiros','dhor_karun','liga_dos_turnos',-280.0,300.0,'um Aureli organiza trabalhadores cuja segurança é tratada como custo','["trabalho", "verdade", "solidariedade"]','["turno forçado", "silenciar acidente"]')
ON DUPLICATE KEY UPDATE name=VALUES(name),race_name=VALUES(race_name),role_name=VALUES(role_name),home_settlement_key=VALUES(home_settlement_key),faction_key=VALUES(faction_key),x_km=VALUES(x_km),y_km=VALUES(y_km),description=VALUES(description),values_json=VALUES(values_json),red_lines_json=VALUES(red_lines_json);

INSERT INTO regional_market_offers
(settlement_key,item_key,item_name,currency_key,buy_price,sell_price,water_index,stock_state) VALUES
('dhor_karun','capacete_de_mina','capacete de mina','coroas',12,5,1.05,'available'),
('dhor_karun','racoes_de_liquen','rações de líquen','coroas',6,3,1.05,'available'),
('dhor_karun','mapa_de_cargas','mapa de cargas','coroas',11,5,1.05,'available'),
('cume_vyn','mascara_de_altitude','máscara de altitude','coroas',16,7,1.3,'available'),
('cume_vyn','grampos_de_pressium','grampos de Pressium','coroas',14,6,1.3,'available'),
('cume_vyn','manta_de_cume','manta de cume','coroas',12,5,1.3,'available'),
('ponte_nuvens','corda_trancada','corda trançada','coroas',10,4,1.25,'available'),
('ponte_nuvens','mosquetao_ferrari','mosquetão Ferrari','coroas',15,7,1.25,'available'),
('ponte_nuvens','sinalizador_de_vento','sinalizador de vento','coroas',8,3,1.25,'available'),
('vale_martelo','pao_de_raiz','pão de raiz','coroas',4,2,0.9,'available'),
('vale_martelo','odre_de_degelo','odre de degelo','coroas',5,2,0.9,'available'),
('vale_martelo','martelo_de_viagem','martelo de viagem','coroas',9,4,0.9,'available'),
('ninho_alto','capa_de_planagem','capa de planagem','coroas',13,6,1.35,'available'),
('ninho_alto','luneta_de_nevoa','luneta de névoa','coroas',17,8,1.35,'available'),
('ninho_alto','racao_de_altitude','ração de altitude','coroas',7,3,1.35,'available'),
('forja_profunda','picareta_balanceada','picareta balanceada','coroas',15,7,1.1,'available'),
('forja_profunda','filtro_de_fuligem','filtro de fuligem','coroas',9,4,1.1,'available'),
('forja_profunda','lanterna_termica','lanterna térmica','coroas',13,6,1.1,'available'),
('luminaria_baixa','fungo_luminoso','fungo luminoso','coroas',5,2,0.95,'available'),
('luminaria_baixa','mascara_de_esporos','máscara de esporos','coroas',10,4,0.95,'available'),
('luminaria_baixa','frasco_de_luminite','frasco de Luminite','coroas',14,6,0.95,'available'),
('lago_harmonico','agua_mineral_tratada','água mineral tratada','coroas',4,2,0.8,'available'),
('lago_harmonico','remo_de_caverna','remo de caverna','coroas',9,4,0.8,'available'),
('lago_harmonico','tampao_de_harmonix','tampão de Harmonix','coroas',8,3,0.8,'available'),
('vigilia_branca','manta_glacari','manta Glacari','coroas',14,6,1.4,'available'),
('vigilia_branca','cha_de_aclimatacao','chá de aclimatação','coroas',8,3,1.4,'available'),
('vigilia_branca','mapa_de_frostreach','mapa de Frostreach','coroas',10,4,1.4,'available'),
('portao_de_pedra','odre_grande','odre grande','coroas',8,3,1.25,'available'),
('portao_de_pedra','racao_de_stonevale','ração de Stonevale','coroas',7,3,1.25,'available'),
('portao_de_pedra','sapato_de_rocha','sapato de rocha','coroas',11,5,1.25,'available'),
('refugio_velado','filtro_vorath','filtro Vorath','coroas',12,5,1.15,'available'),
('refugio_velado','tinta_sem_brilho','tinta sem brilho','coroas',7,3,1.15,'available'),
('refugio_velado','chave_de_galeria','chave de galeria','coroas',15,7,1.15,'available')
ON DUPLICATE KEY UPDATE item_name=VALUES(item_name),currency_key=VALUES(currency_key),buy_price=VALUES(buy_price),sell_price=VALUES(sell_price),water_index=VALUES(water_index),stock_state=VALUES(stock_state);

SELECT
 (SELECT COUNT(*) FROM regional_settlements WHERE region_slug='espinha_do_mundo') AS assentamentos,
 (SELECT COUNT(*) FROM regional_routes WHERE region_slug='espinha_do_mundo') AS rotas,
 (SELECT COUNT(*) FROM npc_definitions_v2 WHERE home_settlement_key IN (SELECT settlement_key FROM regional_settlements WHERE region_slug='espinha_do_mundo')) AS npcs,
 (SELECT COUNT(*) FROM regional_market_offers WHERE settlement_key IN (SELECT settlement_key FROM regional_settlements WHERE region_slug='espinha_do_mundo')) AS ofertas,
 (SELECT COUNT(*) FROM region_borders_v2 WHERE border_key IN ('espinha_frostreach','frostreach_espinha','espinha_stonevale','stonevale_espinha')) AS fronteiras;
