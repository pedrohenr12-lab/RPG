-- Região 4: Stonevale. Execute após schema.sql, seed_core.sql e seed_biologia.sql.
USE aetheria_rpg;
CREATE TABLE IF NOT EXISTS locations (id INT AUTO_INCREMENT PRIMARY KEY,slug VARCHAR(120) UNIQUE NOT NULL,region_id INT NOT NULL,biome_id INT NULL,name VARCHAR(160) NOT NULL,location_type VARCHAR(80) NOT NULL,danger_base TINYINT NOT NULL DEFAULT 1,description TEXT NOT NULL,FOREIGN KEY(region_id) REFERENCES regions(id),FOREIGN KEY(biome_id) REFERENCES biomes(id));
CREATE TABLE IF NOT EXISTS biome_elements (biome_id INT NOT NULL,atomic_number SMALLINT NOT NULL,PRIMARY KEY(biome_id,atomic_number),FOREIGN KEY(biome_id) REFERENCES biomes(id) ON DELETE CASCADE,FOREIGN KEY(atomic_number) REFERENCES elements(atomic_number));
INSERT INTO regions(slug,name,continent,climate,lore) VALUES ('stonevale','Stonevale','Eudora','Semiárido e quente, 15°C a 35°C, grande variação entre dia e noite e gravidade de 0,7G.','Alvo de ataques demoníacos na Guerra dos Vorath; seu cânion proibido permanece fechado e a região mistura desertos de pedra e oásis.') ON DUPLICATE KEY UPDATE name=VALUES(name),climate=VALUES(climate),lore=VALUES(lore);
INSERT INTO biomes(region_id,slug,name,climate,danger_base) SELECT id,'platos_aridos','Platôs Áridos','Rocha exposta, calor médio de 30°C, pouca chuva e noites frias.',4 FROM regions WHERE slug='stonevale' ON DUPLICATE KEY UPDATE region_id=VALUES(region_id),name=VALUES(name),climate=VALUES(climate),danger_base=VALUES(danger_base);
INSERT INTO biomes(region_id,slug,name,climate,danger_base) SELECT id,'canions_profundos','Cânions Profundos','Ravinas de até 1.200 metros, até 40°C de dia e −5°C à noite.',5 FROM regions WHERE slug='stonevale' ON DUPLICATE KEY UPDATE region_id=VALUES(region_id),name=VALUES(name),climate=VALUES(climate),danger_base=VALUES(danger_base);
INSERT INTO biomes(region_id,slug,name,climate,danger_base) SELECT id,'vales_fertis_isolados','Vales Férteis Isolados','Oásis protegidos, lagos e cachoeiras, 18°C a 28°C.',3 FROM regions WHERE slug='stonevale' ON DUPLICATE KEY UPDATE region_id=VALUES(region_id),name=VALUES(name),climate=VALUES(climate),danger_base=VALUES(danger_base);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('planalto_de_cristal',(SELECT id FROM regions WHERE slug='stonevale'),(SELECT id FROM biomes WHERE slug='platos_aridos'),'Planalto de Cristal','platô',4,'Formações geométricas de Silicyn, espinhos translúcidos e pouca água superficial.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('salina_das_luas',(SELECT id FROM regions WHERE slug='stonevale'),(SELECT id FROM biomes WHERE slug='platos_aridos'),'Salina das Luas','salina',4,'Depressão salgada onde Flores-do-Deserto abrem apenas à noite.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('ninho_da_aguia_do_plato',(SELECT id FROM regions WHERE slug='stonevale'),(SELECT id FROM biomes WHERE slug='platos_aridos'),'Ninho da Águia do Platô','falésia',4,'Paredes altas usadas por águias e observadas por lagartos de cristal.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('canion_proibido',(SELECT id FROM regions WHERE slug='stonevale'),(SELECT id FROM biomes WHERE slug='canions_profundos'),'Cânion Proibido','cânion amaldiçoado',5,'Área vedada desde os ataques demoníacos; ecos imitam vozes e algo antigo guarda a entrada.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('ponte_das_vinhas',(SELECT id FROM regions WHERE slug='stonevale'),(SELECT id FROM biomes WHERE slug='canions_profundos'),'Ponte das Vinhas','cânion',4,'Terraço estreito onde vinhas unem paredes acima de uma queda sazonal.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('caverna_dos_ecos',(SELECT id FROM regions WHERE slug='stonevale'),(SELECT id FROM biomes WHERE slug='canions_profundos'),'Caverna dos Ecos','caverna',5,'Morcegos e musgos de Resonum tornam qualquer som difícil de interpretar.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('oasis_esmeralda',(SELECT id FROM regions WHERE slug='stonevale'),(SELECT id FROM biomes WHERE slug='vales_fertis_isolados'),'Oásis Esmeralda','oásis',2,'Lago cristalino, palmeiras altas e Lírios-d’Água Cristalinos.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('cascata_da_vida',(SELECT id FROM regions WHERE slug='stonevale'),(SELECT id FROM biomes WHERE slug='vales_fertis_isolados'),'Cascata da Vida','cascata',3,'Queda d’água permanente sob uma Árvore-de-Vida do Vale.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('nascente_de_jade',(SELECT id FROM regions WHERE slug='stonevale'),(SELECT id FROM biomes WHERE slug='vales_fertis_isolados'),'Nascente de Jade','nascente',4,'Nascente protegida por vinhas verdes e histórias de um guardião mineral.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,126 FROM biomes WHERE slug='platos_aridos';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,132 FROM biomes WHERE slug='platos_aridos';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,124 FROM biomes WHERE slug='canions_profundos';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,133 FROM biomes WHERE slug='canions_profundos';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,120 FROM biomes WHERE slug='vales_fertis_isolados';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,121 FROM biomes WHERE slug='vales_fertis_isolados';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,127 FROM biomes WHERE slug='vales_fertis_isolados';
INSERT INTO species(slug,common_name,scientific_name,kingdom,class_name,behavior,threat,description,edible,poisonous,legendary) VALUES
('stonevale_flora_cacto_de_cristal','Cacto-de-Cristal',NULL,'flora','Flora desértica','pacific',0,'Cresce em geometrias perfeitas; espinhos translúcidos de Silicyn armazenam água por anos.',FALSE,FALSE,FALSE),
('stonevale_flora_arbusto_de_pedra','Arbusto-de-Pedra',NULL,'flora','Arbusto desértico','pacific',0,'Planta baixa de folhas cinzentas, camuflada nas rochas.',FALSE,FALSE,FALSE),
('stonevale_flora_flor_do_deserto','Flor-do-Deserto',NULL,'flora','Flor noturna','pacific',0,'Abre somente à noite; pétalas brancas brilham levemente sob a lua.',FALSE,FALSE,FALSE),
('stonevale_flora_liquen_de_quartzo','Líquen-de-Quartzo',NULL,'flora','Líquen mineral','pacific',0,'Cresce em círculos nas rochas, com coloração rosa e dourada.',FALSE,FALSE,FALSE),
('stonevale_flora_grama_de_fenda','Grama-de-Fenda',NULL,'flora','Gramínea de fenda','pacific',0,'Vegetação de rachaduras profundas, com raízes longas e fortes.',TRUE,FALSE,FALSE),
('stonevale_flora_samambaia_de_fenda','Samambaia-de-Fenda',NULL,'flora','Samambaia de cânion','pacific',0,'Folhas longas e elegantes nas fendas úmidas das paredes.',FALSE,FALSE,FALSE),
('stonevale_flora_flor_de_cachoeira','Flor-de-Cachoeira',NULL,'flora','Flor de cachoeira','pacific',0,'Aparece onde a água cai; pétalas azuis e brancas brilham com a umidade.',FALSE,FALSE,FALSE),
('stonevale_flora_musgo_de_eco','Musgo-de-Eco',NULL,'flora','Musgo ressonante','mystic',1,'Vibra levemente quando alguém fala perto, em locais de Resonum forte.',FALSE,FALSE,FALSE),
('stonevale_flora_vinhas_de_parede','Vinhas-de-Parede',NULL,'flora','Trepadeira','pacific',0,'Sobem centenas de metros e são usadas por escaladores experientes.',FALSE,FALSE,FALSE),
('stonevale_flora_arvore_de_canion','Árvore-de-Cânion',NULL,'flora','Árvore rara','pacific',0,'Cresce em terraços naturais; possui madeira extremamente dura.',FALSE,FALSE,FALSE),
('stonevale_flora_palmeira_de_oasis','Palmeira-de-Oásis',NULL,'flora','Árvore de oásis','pacific',0,'Alta e elegante, produz frutos doces e nutritivos.',TRUE,FALSE,FALSE),
('stonevale_flora_lirio_d_agua_cristalino','Lírio-d''Água Cristalino',NULL,'flora','Flor aquática','pacific',0,'Flutua nos lagos, com pétalas quase transparentes.',FALSE,FALSE,FALSE),
('stonevale_flora_musgo_de_cascata_de_stonevale','Musgo-de-Cascata de Stonevale',NULL,'flora','Musgo aquático','pacific',0,'Musgo de verde intenso que cresce sob quedas d’água.',FALSE,FALSE,FALSE),
('stonevale_flora_arvore_de_vida_do_vale','Árvore-de-Vida do Vale',NULL,'flora','Árvore sagrada','mystic',1,'Árvore sagrada de folhas douradas; descansar sob ela auxilia recuperação de ferimentos leves.',FALSE,FALSE,FALSE),
('stonevale_flora_flor_de_miragem','Flor-de-Miragem',NULL,'flora','Flor mística','mystic',2,'Surge em dias de calor e cria ilusões leves ao redor.',FALSE,FALSE,FALSE),
('stonevale_flora_vinhas_de_jade','Vinhas-de-Jade',NULL,'flora','Trepadeira mineral','pacific',0,'Folhas verde-esmeralda com traços de jade.',FALSE,FALSE,FALSE),
('stonevale_fauna_lagarto_de_cristal','Lagarto-de-Cristal',NULL,'fauna','Réptil','neutral',2,'Escamas translúcidas de Silicyn garantem camuflagem quase perfeita.',FALSE,FALSE,FALSE),
('stonevale_fauna_aguia_do_plato','Águia-do-Platô',NULL,'fauna','Ave de rapina','predator',3,'Predador aéreo dominante, de visão excepcional e ninhos em formações altas.',FALSE,FALSE,FALSE),
('stonevale_fauna_serpente_de_areia','Serpente-de-Areia',NULL,'fauna','Réptil','predator',4,'Move-se sob areia fina; veneno causa febre alta.',FALSE,TRUE,FALSE),
('stonevale_fauna_rato_de_pedra','Rato-de-Pedra',NULL,'fauna','Roedor','neutral',0,'Ágil, vive em colônias dentro de fendas.',FALSE,FALSE,FALSE),
('stonevale_fauna_escorpiao_de_quartzo','Escorpião-de-Quartzo',NULL,'fauna','Aracnídeo','predator',3,'Peçonhento, com carapaça brilhante.',FALSE,TRUE,FALSE),
('stonevale_fauna_espectro_de_pedra','Espectro-de-Pedra',NULL,'fauna','Entidade lendária','legendary',4,'Criatura semi-transparente vista apenas sob sol do meio-dia; possível eco de guerreiros da Guerra dos Vorath.',FALSE,FALSE,TRUE),
('stonevale_fauna_guardiao_de_silicyn','Guardião de Silicyn',NULL,'fauna','Entidade lendária','legendary',5,'Cristais vivos que protegem veios minerais importantes.',FALSE,FALSE,TRUE),
('stonevale_fauna_aguia_de_canion','Águia-de-Cânion',NULL,'fauna','Ave de rapina','predator',3,'Maior que a águia do platô, usa correntes de ar de cânions.',FALSE,FALSE,FALSE),
('stonevale_fauna_cabra_das_paredes','Cabra-das-Paredes',NULL,'fauna','Mamífero herbívoro','territorial',2,'Sobe superfícies quase verticais.',FALSE,FALSE,FALSE),
('stonevale_fauna_serpente_de_fenda','Serpente-de-Fenda',NULL,'fauna','Réptil','predator',3,'Pele camuflada com as rochas; vive em rachaduras profundas.',FALSE,FALSE,FALSE),
('stonevale_fauna_morcego_de_eco','Morcego-de-Eco',NULL,'fauna','Mamífero voador','neutral',1,'Emite sons com Resonum anômalo e navega no escuro.',FALSE,FALSE,FALSE),
('stonevale_fauna_lagarto_de_parede','Lagarto-de-Parede',NULL,'fauna','Réptil','neutral',1,'Corre em superfícies verticais com facilidade.',FALSE,FALSE,FALSE),
('stonevale_fauna_eco_vivo','Eco-Vivo',NULL,'fauna','Entidade lendária','legendary',4,'Som antigo preso nas paredes; pode imitar vozes de pessoas mortas.',FALSE,FALSE,TRUE),
('stonevale_fauna_dragao_de_pedra_menor','Dragão-de-Pedra Menor',NULL,'fauna','Criatura lendária','legendary',5,'Habitante raríssimo dos cânions profundos, de pele de rocha viva.',FALSE,FALSE,TRUE),
('stonevale_fauna_guardiao_do_canion_proibido','Guardião do Cânion Proibido',NULL,'fauna','Entidade lendária','legendary',5,'Entidade antiga que impede a entrada do cânion amaldiçoado.',FALSE,FALSE,TRUE),
('stonevale_fauna_cervo_de_oasis','Cervo-de-Oásis',NULL,'fauna','Mamífero herbívoro','pacific',1,'Pelagem dourada, dócil e muito bonito.',FALSE,FALSE,FALSE),
('stonevale_fauna_peixe_cristalino','Peixe-Cristalino',NULL,'fauna','Peixe','pacific',0,'Corpo quase transparente em lagos cristalinos.',FALSE,FALSE,FALSE),
('stonevale_fauna_garca_branca','Garça-Branca',NULL,'fauna','Ave aquática','neutral',1,'Nidifica perto das cachoeiras.',FALSE,FALSE,FALSE),
('stonevale_fauna_lontra_de_vale','Lontra-de-Vale',NULL,'fauna','Mamífero aquático','pacific',1,'Brincalhona e inteligente.',FALSE,FALSE,FALSE),
('stonevale_fauna_borboleta_de_luminite','Borboleta-de-Luminite',NULL,'fauna','Inseto','mystic',1,'Asas iridescentes brilham por Luminite.',FALSE,FALSE,FALSE),
('stonevale_fauna_ninfa_do_oasis','Ninfa-do-Oásis',NULL,'fauna','Entidade lendária','legendary',4,'Espírito da água que protege os vales e surge a quem respeita o lugar.',FALSE,FALSE,TRUE),
('stonevale_fauna_guardiao_de_jade','Guardião de Jade',NULL,'fauna','Entidade lendária','legendary',5,'Pedras preciosas vivas protegem as nascentes.',FALSE,FALSE,TRUE),
('stonevale_fauna_fenix_de_pedra','Fênix-de-Pedra',NULL,'fauna','Criatura lendária','legendary',5,'Dizem que nasce das chamas antigas da Guerra; aparece apenas após séculos.',FALSE,FALSE,TRUE)
ON DUPLICATE KEY UPDATE common_name=VALUES(common_name),class_name=VALUES(class_name),behavior=VALUES(behavior),threat=VALUES(threat),description=VALUES(description),edible=VALUES(edible),poisonous=VALUES(poisonous),legendary=VALUES(legendary);
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,6 FROM species s JOIN biomes b WHERE b.slug='platos_aridos' AND s.slug IN ('stonevale_flora_cacto_de_cristal','stonevale_flora_arbusto_de_pedra','stonevale_flora_flor_do_deserto','stonevale_flora_liquen_de_quartzo','stonevale_flora_grama_de_fenda','stonevale_fauna_lagarto_de_cristal','stonevale_fauna_aguia_do_plato','stonevale_fauna_serpente_de_areia','stonevale_fauna_rato_de_pedra','stonevale_fauna_escorpiao_de_quartzo','stonevale_fauna_espectro_de_pedra','stonevale_fauna_guardiao_de_silicyn');
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,3 FROM species s JOIN biomes b WHERE b.slug='canions_profundos' AND s.slug IN ('stonevale_flora_samambaia_de_fenda','stonevale_flora_flor_de_cachoeira','stonevale_flora_musgo_de_eco','stonevale_flora_vinhas_de_parede','stonevale_flora_arvore_de_canion','stonevale_fauna_aguia_de_canion','stonevale_fauna_cabra_das_paredes','stonevale_fauna_serpente_de_fenda','stonevale_fauna_morcego_de_eco','stonevale_fauna_lagarto_de_parede','stonevale_fauna_eco_vivo','stonevale_fauna_dragao_de_pedra_menor','stonevale_fauna_guardiao_do_canion_proibido');
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,6 FROM species s JOIN biomes b WHERE b.slug='vales_fertis_isolados' AND s.slug IN ('stonevale_flora_palmeira_de_oasis','stonevale_flora_lirio_d_agua_cristalino','stonevale_flora_musgo_de_cascata_de_stonevale','stonevale_flora_arvore_de_vida_do_vale','stonevale_flora_flor_de_miragem','stonevale_flora_vinhas_de_jade','stonevale_fauna_cervo_de_oasis','stonevale_fauna_peixe_cristalino','stonevale_fauna_garca_branca','stonevale_fauna_lontra_de_vale','stonevale_fauna_borboleta_de_luminite','stonevale_fauna_ninfa_do_oasis','stonevale_fauna_guardiao_de_jade','stonevale_fauna_fenix_de_pedra');
-- Espécies globais selecionadas para rocha, deserto, cânion e oásis.
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,3 FROM species s JOIN biomes b WHERE b.slug='platos_aridos' AND s.slug IN ('mamifero_gato_das_rochas','mamifero_predador_de_vortice','oviparo_lagarto_de_rocha','oviparo_serpente_de_fogo','oviparo_lagarto_colossal','oviparo_ave_de_vortice','oviparo_serpente_de_vortice','lendario_colosso_de_pedra','lendario_serpente_de_vidro');
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,3 FROM species s JOIN biomes b WHERE b.slug='canions_profundos' AND s.slug IN ('mamifero_cabra_gigante','mamifero_ovelha_de_rocha','mamifero_felino_escalador','oviparo_aguia_cacadora','oviparo_lagarto_de_emboscada','oviparo_ave_cortante','oviparo_dragao_de_rocha','lendario_dragao_orbital');
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,3 FROM species s JOIN biomes b WHERE b.slug='vales_fertis_isolados' AND s.slug IN ('mamifero_capivara_costeira','mamifero_lontra_predadora','mamifero_cervo_luminoso','oviparo_pato_d_agua','oviparo_garca_longa','oviparo_ra_das_aguas','oviparo_tartaruga_aquatica','lendario_fenix_bioluminescente','lendario_guardiao_das_aguas');
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='stonevale_flora_cacto_de_cristal';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='stonevale_flora_arbusto_de_pedra';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='stonevale_flora_flor_do_deserto';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,122 FROM species WHERE slug='stonevale_flora_liquen_de_quartzo';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='stonevale_flora_liquen_de_quartzo';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,121 FROM species WHERE slug='stonevale_flora_grama_de_fenda';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,121 FROM species WHERE slug='stonevale_flora_samambaia_de_fenda';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='stonevale_flora_flor_de_cachoeira';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='stonevale_flora_flor_de_cachoeira';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,133 FROM species WHERE slug='stonevale_flora_musgo_de_eco';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,121 FROM species WHERE slug='stonevale_flora_vinhas_de_parede';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='stonevale_flora_arvore_de_canion';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,121 FROM species WHERE slug='stonevale_flora_palmeira_de_oasis';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='stonevale_flora_palmeira_de_oasis';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='stonevale_flora_lirio_d_agua_cristalino';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='stonevale_flora_lirio_d_agua_cristalino';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='stonevale_flora_musgo_de_cascata_de_stonevale';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,121 FROM species WHERE slug='stonevale_flora_arvore_de_vida_do_vale';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='stonevale_flora_arvore_de_vida_do_vale';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='stonevale_flora_flor_de_miragem';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,148 FROM species WHERE slug='stonevale_flora_flor_de_miragem';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,121 FROM species WHERE slug='stonevale_flora_vinhas_de_jade';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='stonevale_flora_vinhas_de_jade';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='stonevale_fauna_lagarto_de_cristal';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='stonevale_fauna_escorpiao_de_quartzo';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='stonevale_fauna_espectro_de_pedra';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='stonevale_fauna_guardiao_de_silicyn';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,133 FROM species WHERE slug='stonevale_fauna_morcego_de_eco';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,133 FROM species WHERE slug='stonevale_fauna_eco_vivo';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='stonevale_fauna_dragao_de_pedra_menor';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,133 FROM species WHERE slug='stonevale_fauna_guardiao_do_canion_proibido';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='stonevale_fauna_cervo_de_oasis';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='stonevale_fauna_peixe_cristalino';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='stonevale_fauna_peixe_cristalino';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='stonevale_fauna_garca_branca';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='stonevale_fauna_lontra_de_vale';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='stonevale_fauna_borboleta_de_luminite';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='stonevale_fauna_ninfa_do_oasis';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='stonevale_fauna_guardiao_de_jade';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,128 FROM species WHERE slug='stonevale_fauna_fenix_de_pedra';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='stonevale_fauna_fenix_de_pedra';
INSERT IGNORE INTO resources(slug,name,resource_type,description,value_base) VALUES ('agua_de_cacto','Água de Cacto','food','Água retirada com cuidado de Cacto-de-Cristal.',10),('espinho_silicyn','Espinho de Silicyn','ore','Espinho cristalino; exige ferramenta segura.',18),('flor_do_deserto','Flor do Deserto','alchemy','Flor noturna de brilho lunar.',12),('musgo_de_eco','Musgo de Eco','alchemy','Musgo de Resonum que vibra com a voz.',16),('vinha_de_parede','Vinha de Parede','herb','Fibra de escalada, útil com técnica adequada.',9),('fruto_de_oasis','Fruto de Oásis','food','Fruto doce de palmeira.',8),('flor_de_miragem','Flor de Miragem','alchemy','Flor de ilusão leve; material delicado.',22),('peixe_cristalino','Peixe Cristalino','food','Peixe transparente de lago de oásis.',12);
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,2 FROM species s JOIN resources r WHERE s.slug='stonevale_flora_cacto_de_cristal' AND r.slug='agua_de_cacto';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,3 FROM species s JOIN resources r WHERE s.slug='stonevale_flora_cacto_de_cristal' AND r.slug='espinho_silicyn';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,2 FROM species s JOIN resources r WHERE s.slug='stonevale_flora_flor_do_deserto' AND r.slug='flor_do_deserto';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,2 FROM species s JOIN resources r WHERE s.slug='stonevale_flora_musgo_de_eco' AND r.slug='musgo_de_eco';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,3 FROM species s JOIN resources r WHERE s.slug='stonevale_flora_vinhas_de_parede' AND r.slug='vinha_de_parede';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,3 FROM species s JOIN resources r WHERE s.slug='stonevale_flora_palmeira_de_oasis' AND r.slug='fruto_de_oasis';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,1 FROM species s JOIN resources r WHERE s.slug='stonevale_flora_flor_de_miragem' AND r.slug='flor_de_miragem';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,3 FROM species s JOIN resources r WHERE s.slug='stonevale_fauna_peixe_cristalino' AND r.slug='peixe_cristalino';
SELECT b.name AS bioma,COUNT(sb.species_id) AS especies_ligadas FROM biomes b LEFT JOIN species_biomes sb ON sb.biome_id=b.id WHERE b.slug IN ('platos_aridos','canions_profundos','vales_fertis_isolados') GROUP BY b.id,b.name ORDER BY b.name;

-- Camada jogável v4: assentamentos, rotas, fronteiras, NPCs e economia persistente.
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
('solkar','stonevale','platos_aridos','Solkar','capital solar',185000,-180,1120,38,'r4_solkar_portico_das_sombras','Capital da Mesa dos Poços, dos observatórios Solari e do Arquivo das Vozes.'),
('karsthal','stonevale','canions_profundos','Karsthal','fortaleza de cânion',62000,1280,1080,27,'r4_karsthal_portao_suspenso','Fortaleza Kragari que controla pontes e a entrada do Cânion Proibido.'),
('ferraria_baixa','stonevale','canions_profundos','Ferrária Baixa','cidade mineira',31000,1880,420,21,'r4_ferraria_baixa_elevador','Cidade Ferrari de ferramentas, guinchos e leitura estrutural.'),
('poco_sete_vozes','stonevale','vales_fertis_isolados','Poço das Sete Vozes','cidade-oásis',26000,480,-920,19,'r4_sete_vozes_praca_dagua','Cidade multirracial ao redor de sete poços ressonantes.'),
('miralume','stonevale','vales_fertis_isolados','Miralume','cidade de estudos',18000,1320,-1120,16,'r4_miralume_jardim_dos_espelhos','Centro de botânica, óptica, cura e estudo de Luminite.'),
('passo_kragar','stonevale','platos_aridos','Passo Kragar','forte de caravanas',12000,720,1860,14,'r4_passo_kragar_patio','Entreposto Kragari de caravanas e contratos de proteção.'),
('cristalia','stonevale','platos_aridos','Cristália','cidade de extração',15000,-980,2020,14,'r4_cristalia_arco_mineral','Cidade que limita a retirada de Silicyn para preservar o platô.'),
('ponte_alta','stonevale','canions_profundos','Ponte Alta','vila suspensa',8000,2060,1480,11,'r4_ponte_alta_catraca','Vila dividida por uma garganta e ligada por cabos e raízes.'),
('jardim_jade','stonevale','vales_fertis_isolados','Jardim de Jade','comunidade agrícola',5000,-420,-1180,10,'r4_jardim_jade_canal_comum','Comunidade que trata água como responsabilidade coletiva.'),
('salina_luas','stonevale','platos_aridos','Salina das Luas','cidade de caravana',11000,-1680,620,13,'r4_salina_luas_balanca','Mercado de sal, couro, água, montarias e informação de rota.'),
('vigilia_rubra','stonevale','platos_aridos','Vigília Rubra','posto de fronteira',3000,-2880,380,9,'r4_vigilia_rubra_marco','Posto aberto entre Arkanor e os primeiros platôs de Stonevale.')
ON DUPLICATE KEY UPDATE region_slug=VALUES(region_slug),biome_slug=VALUES(biome_slug),name=VALUES(name),settlement_type=VALUES(settlement_type),population_estimate=VALUES(population_estimate),x_km=VALUES(x_km),y_km=VALUES(y_km),radius_km=VALUES(radius_km),entry_scene_key=VALUES(entry_scene_key),description=VALUES(description);

INSERT INTO regional_routes
(route_key,region_slug,route_type,a_x_km,a_y_km,b_x_km,b_y_km,influence_width_km,description) VALUES
('rota_rubra','stonevale','road',-2880,380,-180,1120,24,'Fronteira a Solkar.'),
('rota_das_salinas','stonevale','caravan',-1680,620,-180,1120,20,'Salina das Luas a Solkar.'),
('estrada_do_silicyn','stonevale','road',-980,2020,-180,1120,18,'Cristália a Solkar.'),
('rota_do_passo','stonevale','caravan',-180,1120,720,1860,22,'Solkar ao Passo Kragar.'),
('ponte_de_karsthal','stonevale','road',-180,1120,1280,1080,18,'Solkar a Karsthal.'),
('rota_dos_guinchos','stonevale','canyon',1280,1080,2060,1480,13,'Karsthal a Ponte Alta.'),
('descida_ferrari','stonevale','canyon',1280,1080,1880,420,15,'Karsthal a Ferrária Baixa.'),
('caminho_dos_sete_pocos','stonevale','road',-180,1120,480,-920,21,'Solkar ao Poço das Sete Vozes.'),
('rota_de_jade','stonevale','irrigation',480,-920,-420,-1180,14,'Poços ao Jardim de Jade.'),
('estrada_dos_espelhos','stonevale','road',480,-920,1320,-1120,16,'Poços a Miralume.')
ON DUPLICATE KEY UPDATE region_slug=VALUES(region_slug),route_type=VALUES(route_type),a_x_km=VALUES(a_x_km),a_y_km=VALUES(a_y_km),b_x_km=VALUES(b_x_km),b_y_km=VALUES(b_y_km),influence_width_km=VALUES(influence_width_km),description=VALUES(description);

INSERT INTO region_borders_v2
(border_key,source_region_slug,target_region_slug,direction_key,axis_key,coordinate_limit_km,corridor_min_km,corridor_max_km,target_biome_slug,target_x_km,target_y_km,description) VALUES
('arkanor_stonevale','arkanor','stonevale','leste','x',1800,-1200,850,'platos_aridos',-2960,380,'Campos cedem a placas vermelhas e ar seco.'),
('stonevale_arkanor','stonevale','arkanor','oeste','x',-3000,-600,1650,'vales_verdes',1760,-420,'A rocha nua cede a colinas, canais e propriedades de Arkanor.')
ON DUPLICATE KEY UPDATE source_region_slug=VALUES(source_region_slug),target_region_slug=VALUES(target_region_slug),direction_key=VALUES(direction_key),axis_key=VALUES(axis_key),coordinate_limit_km=VALUES(coordinate_limit_km),corridor_min_km=VALUES(corridor_min_km),corridor_max_km=VALUES(corridor_max_km),target_biome_slug=VALUES(target_biome_slug),target_x_km=VALUES(target_x_km),target_y_km=VALUES(target_y_km),description=VALUES(description);

INSERT INTO npc_definitions_v2
(npc_key,name,race_name,role_name,home_settlement_key,faction_key,x_km,y_km,description,values_json,red_lines_json) VALUES
('rakh_toruun','Rakh Toruun','Kragari','guarda de caravana e possível companheiro','passo_kragar','guardas_do_passo',720,1860,'Venceu um duelo combinado para impedir uma guerra.',JSON_ARRAY('proteção','honra como responsabilidade','verdade útil'),JSON_ARRAY('crueldade gratuita','abandonar dependente')),
('samira_sete_sombras','Samira Sete-Sombras','Solari','astrônoma e mediadora','solkar','mesa_dos_pocos',-160,1140,'Mede sombras, poços e incertezas antes de decidir.',JSON_ARRAY('observação','água pública','dúvida honesta'),JSON_ARRAY('falsificar medição','punir sede')),
('maara_veyl','Maara Veyl','Humana','mercadora de água','salina_luas','liga_das_caravanas',-1660,640,'Mantém comércio e uma cota de emergência.',JSON_ARRAY('continuidade','lucro sustentável'),JSON_ARRAY('envenenar poço','roubar caravana')),
('telar_folha_palida','Telar Folha-Pálida','Sylvani','cultivador de sombra','jardim_jade','circulo_dos_canais',-400,-1160,'Orienta folhas para reduzir evaporação.',JSON_ARRAY('cultivo','cooperação'),JSON_ARRAY('queimar horta','privatizar chuva')),
('orun_veio_seco','Orun Veio-Seco','Aureli','mestre de extração','cristalia','guilda_do_silicyn',-960,2040,'Marca a pedra que não deve ser cortada.',JSON_ARRAY('estrutura','trabalho'),JSON_ARRAY('mineração cega','fraude de segurança')),
('neris_sete_pocos','Neris Sete-Poços','Aquari','hidróloga itinerante','poco_sete_vozes','circulo_dos_canais',500,-900,'Identifica a origem da água pela concentração mineral.',JSON_ARRAY('fluxo','acesso','cuidado'),JSON_ARRAY('contaminar água','negar socorro')),
('ivena_branca','Ivena Branca','Glacari','médica do calor','vigilia_rubra','casa_da_sombra',-2860,400,'Diagnostica insolação antes do colapso.',JSON_ARRAY('cuidado','preparo'),JSON_ARRAY('deixar febril ao sol','cobrar por emergência')),
('lume_dois','Lume-Dois','Luminari','cartógrafa de miragens','miralume','observatorio_das_reflexoes',1300,-1100,'Mede miragens pela divergência das sombras.',JSON_ARRAY('curiosidade','beleza verificável'),JSON_ARRAY('cegar animal','roubar mapa')),
('zik_corda_curta','Zik Corda-Curta','Ziraki','mecânico de guinchos','ponte_alta','mestres_da_ponte',2040,1480,'Escuta a tensão dos cabos.',JSON_ARRAY('invenção','manutenção'),JSON_ARRAY('ocultar desgaste','culpar aprendiz')),
('nhalis_azul','Nhalis Azul','Ninfari','guardiã da Nascente','miralume','guardioes_da_nascente',1340,-1140,'Sente mudanças de vazão dentro do canal.',JSON_ARRAY('água','memória','consentimento'),JSON_ARRAY('aprisionar ninfa','secar berçário')),
('sombra_de_sal','Sombra-de-Sal','Umbrari','investigadora de desvios','salina_luas','arquivo_dos_odres',-1700,600,'Segue rastros de água e dívidas escondidas.',JSON_ARRAY('prova','sigilo responsável'),JSON_ARRAY('fabricar culpado','expor fonte')),
('ferra_viga_rubra','Ferra Viga-Rubra','Ferrari','engenheira do cânion','ferraria_baixa','mestres_da_ponte',1860,440,'Testa grampos e elevadores sob carga.',JSON_ARRAY('segurança','reparo'),JSON_ARRAY('ignorar fissura','sobrecarregar cabo')),
('dravos_bronze','Dravos Bronze','Drakari','capitão de Karsthal','karsthal','vigias_do_canion',1300,1100,'Percebe calor atrás da rocha e protege patrulhas.',JSON_ARRAY('dever','proteção'),JSON_ARRAY('executar rendido','abandonar civis')),
('erian_vespera','Erian Véspera','Ethari','estudiosa dos Ecos','solkar','arquivo_das_vozes',-200,1100,'Registra respostas sem contaminar o Eco.',JSON_ARRAY('identidade','registro','consentimento'),JSON_ARRAY('apagar testemunho','ocupar corpo')),
('torv_fenda_clara','Torv Fenda-Clara','Voraki','batedor subterrâneo','ferraria_baixa','cartografos_da_fenda',1900,400,'Encontra galerias por vibração.',JSON_ARRAY('território','orientação'),JSON_ARRAY('selar vivo','invadir ninho')),
('cora_pedra_mansa','Cora Pedra-Mansa','Humana','juíza itinerante','poco_sete_vozes','mesa_dos_pocos',460,-940,'Divide vazões por processo público.',JSON_ARRAY('proporção','reparação'),JSON_ARRAY('suborno','punição coletiva')),
('kharos_do_eco','Kharos do Eco','Eco','cópia ressonante de general morto','karsthal','exercito_dos_ecos',2440,820,'Acredita que a guerra de novecentos anos atrás ainda ocorre.',JSON_ARRAY('continuidade','soldados','vitória'),JSON_ARRAY('apagar memória','declarar mortos irreais'))
ON DUPLICATE KEY UPDATE name=VALUES(name),race_name=VALUES(race_name),role_name=VALUES(role_name),home_settlement_key=VALUES(home_settlement_key),faction_key=VALUES(faction_key),x_km=VALUES(x_km),y_km=VALUES(y_km),description=VALUES(description),values_json=VALUES(values_json),red_lines_json=VALUES(red_lines_json);

INSERT INTO regional_market_offers
(settlement_key,item_key,item_name,currency_key,buy_price,sell_price,water_index,stock_state) VALUES
('solkar','odre_agua','Odre de água','coroas',5,2,1.15,'available'),
('karsthal','corda_canion','Corda de cânion','coroas',10,4,1.30,'available'),
('ferraria_baixa','kit_escalada','Kit de escalada','coroas',22,10,1.35,'limited'),
('poco_sete_vozes','odre_agua','Odre de água','coroas',4,2,0.80,'available'),
('miralume','antidoto_miragem','Antídoto de miragem','coroas',12,5,0.90,'available'),
('passo_kragar','racao_caravana','Ração de caravana','coroas',6,3,1.25,'available'),
('cristalia','fragmento_silicyn','Fragmento de Silicyn','coroas',15,7,1.40,'limited'),
('ponte_alta','grampo_ferrari','Grampo Ferrari','coroas',11,5,1.20,'available'),
('jardim_jade','fruta_oasis','Fruta de oásis','coroas',2,1,0.65,'available'),
('salina_luas','sal_lunar','Sal lunar','coroas',4,2,1.10,'available'),
('vigilia_rubra','mapa_fronteira','Mapa de fronteira','coroas',8,3,1.20,'available')
ON DUPLICATE KEY UPDATE item_name=VALUES(item_name),currency_key=VALUES(currency_key),buy_price=VALUES(buy_price),sell_price=VALUES(sell_price),water_index=VALUES(water_index),stock_state=VALUES(stock_state);

SELECT
 (SELECT COUNT(*) FROM regional_settlements WHERE region_slug='stonevale') AS assentamentos,
 (SELECT COUNT(*) FROM regional_routes WHERE region_slug='stonevale') AS rotas,
 (SELECT COUNT(*) FROM npc_definitions_v2 WHERE home_settlement_key IN (SELECT settlement_key FROM regional_settlements WHERE region_slug='stonevale')) AS npcs,
 (SELECT COUNT(*) FROM regional_market_offers WHERE settlement_key IN (SELECT settlement_key FROM regional_settlements WHERE region_slug='stonevale')) AS ofertas,
 (SELECT COUNT(*) FROM region_borders_v2 WHERE border_key IN ('arkanor_stonevale','stonevale_arkanor')) AS fronteiras;
