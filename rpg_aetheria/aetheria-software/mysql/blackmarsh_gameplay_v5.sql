-- Região 5: Blackmarsh. Execute após schema.sql, seed_core.sql e seed_biologia.sql.
USE aetheria_rpg;
CREATE TABLE IF NOT EXISTS locations (id INT AUTO_INCREMENT PRIMARY KEY,slug VARCHAR(120) UNIQUE NOT NULL,region_id INT NOT NULL,biome_id INT NULL,name VARCHAR(160) NOT NULL,location_type VARCHAR(80) NOT NULL,danger_base TINYINT NOT NULL DEFAULT 1,description TEXT NOT NULL,FOREIGN KEY(region_id) REFERENCES regions(id),FOREIGN KEY(biome_id) REFERENCES biomes(id));
CREATE TABLE IF NOT EXISTS biome_elements (biome_id INT NOT NULL,atomic_number SMALLINT NOT NULL,PRIMARY KEY(biome_id,atomic_number),FOREIGN KEY(biome_id) REFERENCES biomes(id) ON DELETE CASCADE,FOREIGN KEY(atomic_number) REFERENCES elements(atomic_number));
INSERT INTO regions(slug,name,continent,climate,lore) VALUES ('blackmarsh','Blackmarsh','Eudora','Tropical úmido e quente, 24°C a 38°C, chuvas torrenciais e gravidade de 0,7G.','Local da maior fenda demoníaca selada na Batalha das Fendas. Anomalias e presenças antigas ainda persistem.') ON DUPLICATE KEY UPDATE name=VALUES(name),climate=VALUES(climate),lore=VALUES(lore);
INSERT INTO biomes(region_id,slug,name,climate,danger_base) SELECT id,'pantanos_vastos','Pântanos Vastos','Água marrom-preta, chuva constante, 80–95% de umidade e média de 32°C.',5 FROM regions WHERE slug='blackmarsh' ON DUPLICATE KEY UPDATE region_id=VALUES(region_id),name=VALUES(name),climate=VALUES(climate),danger_base=VALUES(danger_base);
INSERT INTO biomes(region_id,slug,name,climate,danger_base) SELECT id,'mangues_gigantes','Mangues Gigantes','Floresta costeira de raízes aéreas, marés e tempestades frequentes.',4 FROM regions WHERE slug='blackmarsh' ON DUPLICATE KEY UPDATE region_id=VALUES(region_id),name=VALUES(name),climate=VALUES(climate),danger_base=VALUES(danger_base);
INSERT INTO biomes(region_id,slug,name,climate,danger_base) SELECT id,'ilhas_vegetacao_flutuante','Ilhas de Vegetação Flutuante','Terra instável sobre turfa, chuvas torrenciais e ilhas em movimento lento.',5 FROM regions WHERE slug='blackmarsh' ON DUPLICATE KEY UPDATE region_id=VALUES(region_id),name=VALUES(name),climate=VALUES(climate),danger_base=VALUES(danger_base);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('fenda_selada',(SELECT id FROM regions WHERE slug='blackmarsh'),(SELECT id FROM biomes WHERE slug='pantanos_vastos'),'Fenda Selada','campo de batalha',5,'Local da Batalha das Fendas. O solo ainda retém anomalias e presenças antigas.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('luzes_de_blackmarsh',(SELECT id FROM regions WHERE slug='blackmarsh'),(SELECT id FROM biomes WHERE slug='pantanos_vastos'),'Luzes de Blackmarsh','pântano',5,'Luzes azul, verde e roxa podem guiar viajantes ou atraí-los para água funda.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('corredor_das_raizes_negras',(SELECT id FROM regions WHERE slug='blackmarsh'),(SELECT id FROM biomes WHERE slug='pantanos_vastos'),'Corredor das Raízes Negras','pântano',5,'Labirinto de raízes sombrias e água rasa, domínio de crocodilos e serpentes.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('labirinto_de_mangue',(SELECT id FROM regions WHERE slug='blackmarsh'),(SELECT id FROM biomes WHERE slug='mangues_gigantes'),'Labirinto de Mangue','mangue',4,'Raízes aéreas gigantes formam paredes naturais durante a maré cheia.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('cavernas_da_mare',(SELECT id FROM regions WHERE slug='blackmarsh'),(SELECT id FROM biomes WHERE slug='mangues_gigantes'),'Cavernas da Maré','caverna costeira',5,'Cavernas onde sons da água assumem padrões anômalos de Resonum.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('salina_de_raizes',(SELECT id FROM regions WHERE slug='blackmarsh'),(SELECT id FROM biomes WHERE slug='mangues_gigantes'),'Salina de Raízes','mangue',3,'Zona de salinas naturais e plantas de folhas cristalizadas.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('ilhas_migrantes',(SELECT id FROM regions WHERE slug='blackmarsh'),(SELECT id FROM biomes WHERE slug='ilhas_vegetacao_flutuante'),'Ilhas Migrantes','ilha flutuante',5,'Massas de turfa e vegetação que mudam lentamente de posição.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('mar_de_turfa',(SELECT id FROM regions WHERE slug='blackmarsh'),(SELECT id FROM biomes WHERE slug='ilhas_vegetacao_flutuante'),'Mar de Turfa','pântano',5,'Água escura sob ilhas frágeis, onde algo pode se mover fora de vista.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT INTO locations(slug,region_id,biome_id,name,location_type,danger_base,description) VALUES ('nucleo_de_orbitium',(SELECT id FROM regions WHERE slug='blackmarsh'),(SELECT id FROM biomes WHERE slug='ilhas_vegetacao_flutuante'),'Núcleo de Orbitium','sítio anômalo',5,'Área rara cuja energia pode influenciar o movimento das ilhas.') ON DUPLICATE KEY UPDATE name=VALUES(name),location_type=VALUES(location_type),danger_base=VALUES(danger_base),description=VALUES(description);
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,120 FROM biomes WHERE slug='pantanos_vastos';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,127 FROM biomes WHERE slug='pantanos_vastos';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,120 FROM biomes WHERE slug='mangues_gigantes';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,143 FROM biomes WHERE slug='mangues_gigantes';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,133 FROM biomes WHERE slug='mangues_gigantes';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,121 FROM biomes WHERE slug='ilhas_vegetacao_flutuante';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,132 FROM biomes WHERE slug='ilhas_vegetacao_flutuante';
INSERT IGNORE INTO biome_elements(biome_id,atomic_number) SELECT id,150 FROM biomes WHERE slug='ilhas_vegetacao_flutuante';
INSERT INTO species(slug,common_name,scientific_name,kingdom,class_name,behavior,threat,description,edible,poisonous,legendary) VALUES
('blackmarsh_flora_musgo_negro','Musgo-Negro',NULL,'flora','Musgo pantanoso','pacific',0,'Forma tapetes densos e esponjosos sobre a água, absorvendo tudo.',FALSE,FALSE,FALSE),
('blackmarsh_flora_lirio_de_pantano','Lírio-de-Pântano',NULL,'flora','Flor aquática','neutral',1,'Flores pálidas e grandes, de perfume adocicado e enganoso.',FALSE,FALSE,FALSE),
('blackmarsh_flora_raiz_retorcida_sombria','Raiz-Retorcida Sombria',NULL,'flora','Raiz pantanosa','territorial',1,'Raízes aéreas e submersas que criam labirintos perigosos.',FALSE,FALSE,FALSE),
('blackmarsh_flora_alga_pura_de_aquanium','Alga-Pura de Aquanium',NULL,'flora','Alga aquática','pacific',0,'Cresce apenas em pontos de água limpa; a água ao redor é cristalina e curativa.',TRUE,FALSE,FALSE),
('blackmarsh_flora_flor_de_fogo_fatuo_de_blackmarsh','Flor-de-Fogo-Fátuo de Blackmarsh',NULL,'flora','Flor mística','mystic',1,'Abre perto de luzes coloridas e tem pétalas iridescentes.',FALSE,FALSE,FALSE),
('blackmarsh_flora_samambaia_de_lama','Samambaia-de-Lama',NULL,'flora','Samambaia aquática','pacific',0,'Folhas longas e pesadas, abundantes no lodo.',FALSE,FALSE,FALSE),
('blackmarsh_flora_cogumelo_de_sombra_de_blackmarsh','Cogumelo-de-Sombra de Blackmarsh',NULL,'fungi','Fungo','neutral',2,'Cresce em troncos semi-submersos; há variedades tóxicas e alucinógenas.',FALSE,TRUE,FALSE),
('blackmarsh_flora_mangue_gigante','Mangue-Gigante',NULL,'flora','Árvore de mangue','pacific',0,'Árvores de raízes aéreas enormes que formam labirintos naturais.',FALSE,FALSE,FALSE),
('blackmarsh_flora_alga_salobra','Alga-Salobra',NULL,'flora','Alga costeira','pacific',0,'Cresce em raízes e lama de água misturada.',TRUE,FALSE,FALSE),
('blackmarsh_flora_flor_de_mare_de_blackmarsh','Flor-de-Maré de Blackmarsh',NULL,'flora','Flor costeira','pacific',0,'Abre na maré baixa com pétalas rosadas.',FALSE,FALSE,FALSE),
('blackmarsh_flora_musgo_de_raiz','Musgo-de-Raiz',NULL,'flora','Musgo de mangue','neutral',1,'Cobre raízes aéreas; é escorregadio e perigoso.',FALSE,FALSE,FALSE),
('blackmarsh_flora_samambaia_costeira','Samambaia-Costeira',NULL,'flora','Samambaia costeira','pacific',0,'Folhas longas resistentes ao sal.',FALSE,FALSE,FALSE),
('blackmarsh_flora_planta_de_sal','Planta-de-Sal',NULL,'flora','Flora salina','pacific',0,'Cresce em salinas naturais, com folhas cristalizadas.',FALSE,FALSE,FALSE),
('blackmarsh_flora_musgo_flutuante','Musgo-Flutuante',NULL,'flora','Musgo flutuante','pacific',0,'Forma a base espessa e instável das ilhas.',FALSE,FALSE,FALSE),
('blackmarsh_flora_planta_venenosa_de_patterium','Planta-Venenosa de Patterium',NULL,'flora','Flora venenosa','neutral',3,'Planta altamente tóxica de padrões simétricos.',FALSE,TRUE,FALSE),
('blackmarsh_flora_flor_de_ilha','Flor-de-Ilha',NULL,'flora','Flor flutuante','pacific',0,'Pétalas coloridas mudam de tom conforme a umidade.',FALSE,FALSE,FALSE),
('blackmarsh_flora_samambaia_flutuante','Samambaia-Flutuante',NULL,'flora','Samambaia flutuante','pacific',0,'Folhas grandes que ajudam a estabilizar as ilhas.',FALSE,FALSE,FALSE),
('blackmarsh_flora_cogumelo_migrante','Cogumelo-Migrante',NULL,'fungi','Fungo','mystic',1,'Cresce e desaparece conforme as ilhas se movem.',FALSE,FALSE,FALSE),
('blackmarsh_flora_vinhas_de_turfa','Vinhas-de-Turfa',NULL,'flora','Trepadeira','pacific',0,'Seguram a estrutura de turfa e vegetação.',FALSE,FALSE,FALSE),
('blackmarsh_fauna_crocodilo_negro','Crocodilo-Negro',NULL,'fauna','Réptil aquático','predator',5,'Predador dominante, pele quase preta, paciente e letal.',FALSE,FALSE,FALSE),
('blackmarsh_fauna_serpente_d_agua_gigante','Serpente-d''Água Gigante',NULL,'fauna','Réptil aquático','predator',5,'Pode chegar a seis metros e possui veneno potente.',FALSE,TRUE,FALSE),
('blackmarsh_fauna_garca_sombria','Garça-Sombria',NULL,'fauna','Ave aquática','predator',2,'Ave alta, silenciosa, caçadora de peixes e anfíbios.',FALSE,FALSE,FALSE),
('blackmarsh_fauna_sapo_gigante_de_blackmarsh','Sapo-Gigante de Blackmarsh',NULL,'fauna','Anfíbio','territorial',3,'Tamanho de um cão médio, com pele cheia de toxinas.',FALSE,TRUE,FALSE),
('blackmarsh_fauna_peixe_luminoso_de_blackmarsh','Peixe-Luminoso de Blackmarsh',NULL,'fauna','Peixe','neutral',1,'Brilha em azul e verde, atraindo predadores e desavisados.',FALSE,FALSE,FALSE),
('blackmarsh_fauna_inseto_fogo_fatuo_de_blackmarsh','Inseto-Fogo-Fátuo de Blackmarsh',NULL,'fauna','Inseto místico','mystic',2,'Cria as luzes coloridas; em enxames pode ser perigoso.',FALSE,FALSE,FALSE),
('blackmarsh_fauna_rato_d_agua_negro','Rato-d''Água Negro',NULL,'fauna','Roedor','neutral',1,'Vive em tocas semi-submersas e pode portar doenças.',FALSE,FALSE,FALSE),
('blackmarsh_fauna_vulto_das_fendas','Vulto-das-Fendas',NULL,'fauna','Entidade lendária','legendary',5,'Sombra que se move de forma independente, possível resto da invasão Vorath.',FALSE,FALSE,TRUE),
('blackmarsh_fauna_ninfa_negra','Ninfa-Negra',NULL,'fauna','Entidade lendária','legendary',5,'Espírito de água corrompida; pode salvar ou afogar conforme sua vontade.',FALSE,FALSE,TRUE),
('blackmarsh_fauna_guardiao_da_fenda_selada','Guardião da Fenda Selada',NULL,'fauna','Entidade lendária','legendary',5,'Entidade que vigia o local da batalha final.',FALSE,FALSE,TRUE),
('blackmarsh_fauna_caranguejo_gigante_de_mangue','Caranguejo-Gigante de Mangue',NULL,'fauna','Crustáceo','territorial',3,'Carapaça dura; vive em colônias entre raízes.',FALSE,FALSE,FALSE),
('blackmarsh_fauna_crocodilo_costeiro','Crocodilo-Costeiro',NULL,'fauna','Réptil aquático','predator',4,'Menor que o do pântano, porém mais agressivo.',FALSE,FALSE,FALSE),
('blackmarsh_fauna_ave_de_mangue','Ave-de-Mangue',NULL,'fauna','Ave','neutral',1,'Constrói ninhos nas raízes altas.',FALSE,FALSE,FALSE),
('blackmarsh_fauna_serpente_de_raiz','Serpente-de-Raiz',NULL,'fauna','Réptil','predator',3,'Camuflada entre raízes; veneno paralisante.',FALSE,TRUE,FALSE),
('blackmarsh_fauna_peixe_salobra','Peixe-Salobra',NULL,'fauna','Peixe','pacific',0,'Adaptado à água misturada de mar e rio.',FALSE,FALSE,FALSE),
('blackmarsh_fauna_morcego_de_caverna','Morcego-de-Caverna',NULL,'fauna','Mamífero voador','neutral',1,'Habita cavernas costeiras e emite sons anômalos.',FALSE,FALSE,FALSE),
('blackmarsh_fauna_eco_das_raizes','Eco-das-Raízes',NULL,'fauna','Entidade lendária','legendary',4,'Vozes antigas entre raízes que podem enganar viajantes.',FALSE,FALSE,TRUE),
('blackmarsh_fauna_guardiao_de_harmonix','Guardião de Harmonix',NULL,'fauna','Entidade lendária','legendary',5,'Criatura de raízes vivas que protege ciclos do mangue.',FALSE,FALSE,TRUE),
('blackmarsh_fauna_ra_flutuante','Rã-Flutuante',NULL,'fauna','Anfíbio','neutral',2,'Salta entre ilhas; pele colorida e tóxica.',FALSE,TRUE,FALSE),
('blackmarsh_fauna_inseto_de_patterium','Inseto-de-Patterium',NULL,'fauna','Inseto','neutral',1,'Voa em padrões geométricos; enxames irritam.',FALSE,FALSE,FALSE),
('blackmarsh_fauna_serpente_flutuante','Serpente-Flutuante',NULL,'fauna','Réptil','predator',4,'Move-se entre ilhas e tem veneno forte.',FALSE,TRUE,FALSE),
('blackmarsh_fauna_ave_migrante','Ave-Migrante',NULL,'fauna','Ave','neutral',1,'Segue as ilhas lentas em movimento.',FALSE,FALSE,FALSE),
('blackmarsh_fauna_caramujo_gigante','Caramujo-Gigante',NULL,'fauna','Molusco','territorial',2,'Vive sob ilhas; concha muito dura.',FALSE,FALSE,FALSE),
('blackmarsh_fauna_espirito_das_ilhas','Espírito-das-Ilhas',NULL,'fauna','Entidade lendária','legendary',4,'Quase nunca visto; controla o movimento lento das ilhas.',FALSE,FALSE,TRUE),
('blackmarsh_fauna_sombra_flutuante','Sombra-Flutuante',NULL,'fauna','Entidade lendária','legendary',5,'Resquício da invasão que se esconde sob ilhas.',FALSE,FALSE,TRUE),
('blackmarsh_fauna_guardiao_de_orbitium','Guardião de Orbitium',NULL,'fauna','Entidade lendária','legendary',5,'Ser de vegetação e energia que protege o equilíbrio instável.',FALSE,FALSE,TRUE)
ON DUPLICATE KEY UPDATE common_name=VALUES(common_name),class_name=VALUES(class_name),behavior=VALUES(behavior),threat=VALUES(threat),description=VALUES(description),edible=VALUES(edible),poisonous=VALUES(poisonous),legendary=VALUES(legendary);
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,3 FROM species s JOIN biomes b WHERE b.slug='pantanos_vastos' AND s.slug IN ('blackmarsh_flora_musgo_negro','blackmarsh_flora_lirio_de_pantano','blackmarsh_flora_raiz_retorcida_sombria','blackmarsh_flora_alga_pura_de_aquanium','blackmarsh_flora_flor_de_fogo_fatuo_de_blackmarsh','blackmarsh_flora_samambaia_de_lama','blackmarsh_flora_cogumelo_de_sombra_de_blackmarsh','blackmarsh_fauna_crocodilo_negro','blackmarsh_fauna_serpente_d_agua_gigante','blackmarsh_fauna_garca_sombria','blackmarsh_fauna_sapo_gigante_de_blackmarsh','blackmarsh_fauna_peixe_luminoso_de_blackmarsh','blackmarsh_fauna_inseto_fogo_fatuo_de_blackmarsh','blackmarsh_fauna_rato_d_agua_negro','blackmarsh_fauna_vulto_das_fendas','blackmarsh_fauna_ninfa_negra','blackmarsh_fauna_guardiao_da_fenda_selada');
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,6 FROM species s JOIN biomes b WHERE b.slug='mangues_gigantes' AND s.slug IN ('blackmarsh_flora_mangue_gigante','blackmarsh_flora_alga_salobra','blackmarsh_flora_flor_de_mare_de_blackmarsh','blackmarsh_flora_musgo_de_raiz','blackmarsh_flora_samambaia_costeira','blackmarsh_flora_planta_de_sal','blackmarsh_fauna_caranguejo_gigante_de_mangue','blackmarsh_fauna_crocodilo_costeiro','blackmarsh_fauna_ave_de_mangue','blackmarsh_fauna_serpente_de_raiz','blackmarsh_fauna_peixe_salobra','blackmarsh_fauna_morcego_de_caverna','blackmarsh_fauna_eco_das_raizes','blackmarsh_fauna_guardiao_de_harmonix');
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,3 FROM species s JOIN biomes b WHERE b.slug='ilhas_vegetacao_flutuante' AND s.slug IN ('blackmarsh_flora_musgo_flutuante','blackmarsh_flora_planta_venenosa_de_patterium','blackmarsh_flora_flor_de_ilha','blackmarsh_flora_samambaia_flutuante','blackmarsh_flora_cogumelo_migrante','blackmarsh_flora_vinhas_de_turfa','blackmarsh_fauna_ra_flutuante','blackmarsh_fauna_inseto_de_patterium','blackmarsh_fauna_serpente_flutuante','blackmarsh_fauna_ave_migrante','blackmarsh_fauna_caramujo_gigante','blackmarsh_fauna_espirito_das_ilhas','blackmarsh_fauna_sombra_flutuante','blackmarsh_fauna_guardiao_de_orbitium');
-- Espécies globais compatíveis com pântanos tropicais, mangues e ilhas instáveis.
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,3 FROM species s JOIN biomes b WHERE b.slug='pantanos_vastos' AND s.slug IN ('mamifero_boi_d_agua','mamifero_capivara_costeira','mamifero_lobo_aquatico','mamifero_lontra_predadora','oviparo_pato_d_agua','oviparo_garca_longa','oviparo_ra_das_aguas','oviparo_jacare_de_rio','oviparo_serpente_aquatica','oviparo_dragao_aquatico','lendario_serpente_abissal','lendario_medusa_viva');
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,3 FROM species s JOIN biomes b WHERE b.slug='mangues_gigantes' AND s.slug IN ('mamifero_capivara_costeira','mamifero_lontra_predadora','oviparo_pato_d_agua','oviparo_garca_longa','oviparo_serpente_aquatica','oviparo_ra_cacadora','oviparo_predador_abissal','lendario_guardiao_das_aguas','lendario_espectro_de_vortice');
INSERT IGNORE INTO species_biomes(species_id,biome_id,encounter_weight) SELECT s.id,b.id,2 FROM species s JOIN biomes b WHERE b.slug='ilhas_vegetacao_flutuante' AND s.slug IN ('mamifero_coelho_brilhante','mamifero_raposa_de_emboscada','oviparo_ave_luminosa','oviparo_serpente_luminosa','oviparo_serpente_fractal','oviparo_ave_espiral','lendario_quimera_elyriana','lendario_entidade_celestyn');
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='blackmarsh_flora_musgo_negro';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='blackmarsh_flora_lirio_de_pantano';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='blackmarsh_flora_raiz_retorcida_sombria';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='blackmarsh_flora_alga_pura_de_aquanium';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='blackmarsh_flora_flor_de_fogo_fatuo_de_blackmarsh';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='blackmarsh_flora_flor_de_fogo_fatuo_de_blackmarsh';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,121 FROM species WHERE slug='blackmarsh_flora_samambaia_de_lama';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='blackmarsh_flora_samambaia_de_lama';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='blackmarsh_flora_mangue_gigante';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,143 FROM species WHERE slug='blackmarsh_flora_mangue_gigante';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='blackmarsh_flora_alga_salobra';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='blackmarsh_flora_flor_de_mare_de_blackmarsh';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='blackmarsh_flora_musgo_de_raiz';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,121 FROM species WHERE slug='blackmarsh_flora_samambaia_costeira';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,126 FROM species WHERE slug='blackmarsh_flora_planta_de_sal';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,121 FROM species WHERE slug='blackmarsh_flora_musgo_flutuante';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,132 FROM species WHERE slug='blackmarsh_flora_musgo_flutuante';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,132 FROM species WHERE slug='blackmarsh_flora_planta_venenosa_de_patterium';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,121 FROM species WHERE slug='blackmarsh_flora_flor_de_ilha';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,121 FROM species WHERE slug='blackmarsh_flora_samambaia_flutuante';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,132 FROM species WHERE slug='blackmarsh_flora_cogumelo_migrante';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,121 FROM species WHERE slug='blackmarsh_flora_vinhas_de_turfa';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='blackmarsh_fauna_serpente_d_agua_gigante';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='blackmarsh_fauna_peixe_luminoso_de_blackmarsh';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='blackmarsh_fauna_peixe_luminoso_de_blackmarsh';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,127 FROM species WHERE slug='blackmarsh_fauna_inseto_fogo_fatuo_de_blackmarsh';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='blackmarsh_fauna_ninfa_negra';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,129 FROM species WHERE slug='blackmarsh_fauna_caranguejo_gigante_de_mangue';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,120 FROM species WHERE slug='blackmarsh_fauna_peixe_salobra';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,133 FROM species WHERE slug='blackmarsh_fauna_morcego_de_caverna';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,133 FROM species WHERE slug='blackmarsh_fauna_eco_das_raizes';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,143 FROM species WHERE slug='blackmarsh_fauna_guardiao_de_harmonix';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,132 FROM species WHERE slug='blackmarsh_fauna_inseto_de_patterium';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,129 FROM species WHERE slug='blackmarsh_fauna_caramujo_gigante';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,150 FROM species WHERE slug='blackmarsh_fauna_espirito_das_ilhas';
INSERT IGNORE INTO species_elements(species_id,atomic_number) SELECT id,150 FROM species WHERE slug='blackmarsh_fauna_guardiao_de_orbitium';
INSERT IGNORE INTO resources(slug,name,resource_type,description,value_base) VALUES ('alga_pura_blackmarsh','Alga-Pura de Blackmarsh','herb','Alga de água limpa e curativa.',14),('flor_fatuo_blackmarsh','Flor de Fogo-Fátuo de Blackmarsh','alchemy','Pétalas iridescentes de luz aquática.',21),('cogumelo_sombra_blackmarsh','Cogumelo de Sombra de Blackmarsh','alchemy','Fungo de efeito variável e perigoso.',12),('madeira_de_mangue','Madeira de Mangue','wood','Madeira resistente a água e sal.',11),('planta_de_sal','Planta de Sal','herb','Folhas cristalizadas de salina.',8),('vinha_de_turfa','Vinha de Turfa','herb','Fibra vegetal de ilhas flutuantes.',9),('carapaca_de_mangue','Carapaça de Mangue','hide','Carapaça dura de crustáceo gigante.',18),('peixe_salobra','Peixe Salobra','food','Peixe adaptado a água mista.',6);
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,2 FROM species s JOIN resources r WHERE s.slug='blackmarsh_flora_alga_pura_de_aquanium' AND r.slug='alga_pura_blackmarsh';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,2 FROM species s JOIN resources r WHERE s.slug='blackmarsh_flora_flor_de_fogo_fatuo_de_blackmarsh' AND r.slug='flor_fatuo_blackmarsh';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,2 FROM species s JOIN resources r WHERE s.slug='blackmarsh_flora_cogumelo_de_sombra_de_blackmarsh' AND r.slug='cogumelo_sombra_blackmarsh';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,3 FROM species s JOIN resources r WHERE s.slug='blackmarsh_flora_mangue_gigante' AND r.slug='madeira_de_mangue';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,2 FROM species s JOIN resources r WHERE s.slug='blackmarsh_flora_planta_de_sal' AND r.slug='planta_de_sal';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,3 FROM species s JOIN resources r WHERE s.slug='blackmarsh_flora_vinhas_de_turfa' AND r.slug='vinha_de_turfa';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,2 FROM species s JOIN resources r WHERE s.slug='blackmarsh_fauna_caranguejo_gigante_de_mangue' AND r.slug='carapaca_de_mangue';
INSERT IGNORE INTO species_resources(species_id,resource_id,yield_min,yield_max) SELECT s.id,r.id,1,3 FROM species s JOIN resources r WHERE s.slug='blackmarsh_fauna_peixe_salobra' AND r.slug='peixe_salobra';
SELECT b.name AS bioma,COUNT(sb.species_id) AS especies_ligadas FROM biomes b LEFT JOIN species_biomes sb ON sb.biome_id=b.id WHERE b.slug IN ('pantanos_vastos','mangues_gigantes','ilhas_vegetacao_flutuante') GROUP BY b.id,b.name ORDER BY b.name;

-- Camada jogável v5: assentamentos, rotas, fronteiras, NPCs e economia persistente.
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
('nhar_delta','blackmarsh','pantanos_vastos','Nhar-Delta','capital de confluência',142000,-240,1180,38,'r5_nhar_delta_cais_da_confluencia','Capital de plataformas, canais e assembleias; sede da Confluência e dos Vigias do Limiar.'),
('porto_lodoalto','blackmarsh','mangues_gigantes','Porto Lodoalto','cidade portuária',65000,-1520,980,28,'r5_porto_lodoalto_doca_alta','Porto Aquari acima da maré máxima, centro de barcos rasos, pescado e navegação costeira.'),
('sete_aguas','blackmarsh','pantanos_vastos','Confluência das Sete Águas','cidade de canais',42000,420,1960,24,'r5_sete_aguas_ponte_das_bacias','Sete bacias elegem vozes e disputam quarentena, abastecimento e passagem.'),
('raiz_catedral','blackmarsh','mangues_gigantes','Raiz-Catedral','cidade de mangue',28000,-2100,-120,20,'r5_raiz_catedral_portico_vivo','Cidade dentro de raízes gigantes, mantida por podas, pontes e pactos.'),
('mare_oca','blackmarsh','mangues_gigantes','Maré Oca','cidade de cavernas',19000,-1180,-860,17,'r5_mare_oca_entrada_da_caverna','Cavernas de Resonum abrem e fecham bairros conforme a maré.'),
('varzea_errante','blackmarsh','ilhas_vegetacao_flutuante','Várzea Errante','cidade flutuante',21000,1260,420,18,'r5_varzea_errante_ancoradouro_movel','Cidade cuja posição transforma endereço em data, corrente e vizinhança.'),
('farol_sal','blackmarsh','mangues_gigantes','Farol de Sal','vila de navegação',12000,-2600,-980,13,'r5_farol_sal_torre_de_conchas','Vila costeira de sinais de concha, salinas e luzes controladas.'),
('ponte_turfa','blackmarsh','ilhas_vegetacao_flutuante','Ponte-Turfa','vila flutuante',8000,2080,1120,11,'r5_ponte_turfa_passarela_flexivel','Passarelas flexíveis estabilizam ilhas sem imobilizá-las.'),
('lago_cego','blackmarsh','ilhas_vegetacao_flutuante','Lago Cego','comunidade de cura',6200,860,-1040,10,'r5_lago_cego_plataforma_de_quarentena','Comunidade médica dedicada à Febre de Duas Margens.'),
('vigilia_norte','blackmarsh','pantanos_vastos','Vigília do Norte','posto de fronteira',3400,520,2920,9,'r5_vigilia_norte_marco_das_chuvas','Posto entre Stonevale e as primeiras águas profundas de Blackmarsh.'),
('porto_cinzento','blackmarsh','mangues_gigantes','Porto Cinzento','posto fluvial',4800,-2900,1880,10,'r5_porto_cinzento_cais_de_fronteira','Entreposto ligado a Arkanor, com fiscais, barqueiros e resgatadores clandestinos.')
ON DUPLICATE KEY UPDATE region_slug=VALUES(region_slug),biome_slug=VALUES(biome_slug),name=VALUES(name),settlement_type=VALUES(settlement_type),population_estimate=VALUES(population_estimate),x_km=VALUES(x_km),y_km=VALUES(y_km),radius_km=VALUES(radius_km),entry_scene_key=VALUES(entry_scene_key),description=VALUES(description);

INSERT INTO regional_routes
(route_key,region_slug,route_type,a_x_km,a_y_km,b_x_km,b_y_km,influence_width_km,description) VALUES
('canal_da_confluencia','blackmarsh','channel',-240,1180,420,1960,28,'Nhar-Delta às Sete Águas.'),
('rota_de_lodoalto','blackmarsh','channel',-1520,980,-240,1180,25,'Porto Lodoalto a Nhar-Delta.'),
('canal_da_raiz','blackmarsh','mangrove',-1520,980,-2100,-120,20,'Lodoalto a Raiz-Catedral.'),
('rota_da_mare_oca','blackmarsh','tidal',-2100,-120,-1180,-860,18,'Raiz-Catedral a Maré Oca.'),
('rota_do_farol','blackmarsh','coastal',-1180,-860,-2600,-980,17,'Maré Oca ao Farol de Sal.'),
('canal_errante','blackmarsh','floating',-240,1180,1260,420,24,'Nhar-Delta à Várzea Errante.'),
('ponte_das_ilhas','blackmarsh','floating',1260,420,2080,1120,16,'Várzea Errante a Ponte-Turfa.'),
('rota_do_lago_cego','blackmarsh','quarantine',1260,420,860,-1040,19,'Várzea Errante ao Lago Cego.'),
('caminho_da_vigilia','blackmarsh','border',420,1960,520,2920,18,'Sete Águas à fronteira de Stonevale.'),
('rota_do_porto_cinzento','blackmarsh','border',-1520,980,-2900,1880,20,'Lodoalto à fronteira de Arkanor.')
ON DUPLICATE KEY UPDATE region_slug=VALUES(region_slug),route_type=VALUES(route_type),a_x_km=VALUES(a_x_km),a_y_km=VALUES(a_y_km),b_x_km=VALUES(b_x_km),b_y_km=VALUES(b_y_km),influence_width_km=VALUES(influence_width_km),description=VALUES(description);

INSERT INTO region_borders_v2
(border_key,source_region_slug,target_region_slug,direction_key,axis_key,coordinate_limit_km,corridor_min_km,corridor_max_km,target_biome_slug,target_x_km,target_y_km,description) VALUES
('blackmarsh_stonevale','blackmarsh','stonevale','norte','y',3000,-800,2200,'vales_ferteis_isolados',520,-1760,'Água negra cede a canais de vale e às pedras de Stonevale.'),
('stonevale_blackmarsh','stonevale','blackmarsh','sul','y',-1800,-800,2200,'pantanos_vastos',520,2960,'Vales ficam quentes, úmidos e perdem solo firme.'),
('blackmarsh_arkanor','blackmarsh','arkanor','oeste','x',-3000,1100,2700,'vales_verdes',1760,-1180,'Mangue cede a margens firmes e canais medidos de Arkanor.'),
('arkanor_blackmarsh','arkanor','blackmarsh','sul','y',-1300,600,1800,'mangues_gigantes',-2860,1880,'O Aurenta se divide e a estrada termina em embarcadouros.')
ON DUPLICATE KEY UPDATE source_region_slug=VALUES(source_region_slug),target_region_slug=VALUES(target_region_slug),direction_key=VALUES(direction_key),axis_key=VALUES(axis_key),coordinate_limit_km=VALUES(coordinate_limit_km),corridor_min_km=VALUES(corridor_min_km),corridor_max_km=VALUES(corridor_max_km),target_biome_slug=VALUES(target_biome_slug),target_x_km=VALUES(target_x_km),target_y_km=VALUES(target_y_km),description=VALUES(description);

INSERT INTO npc_definitions_v2
(npc_key,name,race_name,role_name,home_settlement_key,faction_key,x_km,y_km,description,values_json,red_lines_json) VALUES
('neris_mare_cega','Neris Maré-Cega','Ninfari','navegadora clandestina e possível companheira','varzea_errante','rede_da_mare_cega',1260,440,'Memoriza ilhas pela pressão e retira pessoas destinadas ao sacrifício.',JSON_ARRAY('liberdade','resgate','responsabilidade'),JSON_ARRAY('entregar refugiado','possuir parceiro')),
('seris_vael','Seris Vael','Ethari','emissário Vorath e possível companheiro','lago_cego','coro_do_retorno',880,-1020,'Escuta vozes do outro lado do Limiar sem fingir neutralidade.',JSON_ARRAY('libertação','verdade','autonomia'),JSON_ARRAY('usar Vorath como combustível','ocultar decisão existencial')),
('maeva_nhar','Maeva Nhar','Umbrari','Primeira Guardiã do Limiar','nhar_delta','vigias_do_limiar',-220,1200,'Conhece o custo biológico do selo e teme o custo de revelá-lo.',JSON_ARRAY('continuidade','selo','dever'),JSON_ARRAY('abrir sem evacuar','destruir registros')),
('tomas_agua_alta','Tomás Água-Alta','Humana','médico de quarentena','lago_cego','casa_das_duas_margens',840,-1060,'Separa sintoma de origem racial enquanto a fila cresce.',JSON_ARRAY('cura','prova','acesso'),JSON_ARRAY('experimento forçado','abandono de febril')),
('silea_raiz_clara','Silea Raiz-Clara','Sylvani','botânica de mangue','raiz_catedral','jardineiros_da_mare',-2080,-100,'Poda raízes sem romper corredores de peixes e moradores.',JSON_ARRAY('ciclo','cultivo','consentimento ecológico'),JSON_ARRAY('cortar raiz-mãe','envenenar canal')),
('brann_pedra_boiando','Brann Pedra-Boiando','Aureli','construtor de fundações','ponte_turfa','mestres_da_turfa',2060,1140,'Calcula peso em solo flutuante e adapta tradição de pedra.',JSON_ARRAY('estrutura','aprendizado','trabalho'),JSON_ARRAY('sobrecarregar ilha','ocultar falha')),
('suri_tres_correntes','Suri Três-Correntes','Aquari','capitã de navegação','porto_lodoalto','coro_de_navegadores',-1500,1000,'Lê maré, chuva e humor da tripulação antes de aceitar carga.',JSON_ARRAY('tripulação','fluxo livre','acordo'),JSON_ARRAY('contaminar água','abandonar passageiro')),
('amina_chuva_branca','Amina Chuva-Branca','Solari','meteorologista tropical','sete_aguas','observatorio_das_chuvas',400,1980,'Mede o céu através dos reflexos deixados pela chuva.',JSON_ARRAY('previsão honesta','evacuação','método'),JSON_ARRAY('falsificar tempestade','reter alerta')),
('ivel_gelo_morno','Ivel Gelo-Morno','Glacari','especialista em febres','lago_cego','casa_das_duas_margens',900,-1060,'Usa metabolismo lento para acompanhar pacientes por noites.',JSON_ARRAY('cuidado','isolamento proporcional','paciência'),JSON_ARRAY('quarentena racial','negar antídoto')),
('pali_luz_baixa','Pali Luz-Baixa','Luminari','pesquisadora de fogo-fátuo','nhar_delta','arquivo_das_luzes',-260,1160,'Distingue inseto, reflexo e anomalia sem tocar nas luzes.',JSON_ARRAY('curiosidade','beleza','segurança'),JSON_ARRAY('atrair criança','enjaular enxame')),
('garr_lama_firme','Garr Lama-Firme','Kragari','chefe de resgate','sete_aguas','brigada_das_bacias',440,1940,'Retira pessoas do lodo e impede curiosos de virar vítimas.',JSON_ARRAY('proteção','equipe','honra'),JSON_ARRAY('abandonar soterrado','violência por medo')),
('zikka_sete_rebites','Zikka Sete-Rebites','Ziraki','mecânica de barcos','ponte_turfa','irmandade_sete_parafusos',2100,1100,'Transforma sucata em lemes, filtros e pontes móveis.',JSON_ARRAY('invenção','autoria','reparo'),JSON_ARRAY('roubar projeto','culpar aprendiz')),
('dorra_raiz_de_ferro','Dorra Raiz-de-Ferro','Ferrari','engenheira de plataformas','raiz_catedral','mestres_da_turfa',-2120,-140,'Escuta pilares e raízes antes de autorizar peso.',JSON_ARRAY('manutenção','segurança','responsabilidade'),JSON_ARRAY('ignorar vibração','construir sobre ninho')),
('kaar_mare_quente','Kaar Maré-Quente','Drakari','guardião reformista','nhar_delta','vigias_do_limiar_reformistas',-200,1220,'Percebe febre em prisioneiros e questiona ordens antigas.',JSON_ARRAY('dever','reforma','vida'),JSON_ARRAY('sacrifício secreto','execução sem julgamento')),
('toru_turfa_funda','Toru Turfa-Funda','Voraki','cartógrafa de ilhas','varzea_errante','mapas_temporarios',1240,400,'Sente ilhas se separando antes da linha visível.',JSON_ARRAY('território móvel','precisão','acesso'),JSON_ARRAY('mapa falso','cortar ilha habitada')),
('elion_sal_calmo','Elion Sal-Calmo','Humana','mercador de antídotos','farol_sal','mercado_da_mare',-2580,-960,'Mantém preços públicos e reserva de emergência.',JSON_ARRAY('estoque','comércio','continuidade'),JSON_ARRAY('antídoto falso','monopólio durante surto')),
('asha_vael','Asha Vael','Vorath','sobrevivente entre margens',NULL,'alianca_antiga',1840,-620,'Aparece em intervalos e lembra ter ajudado a fechar o Limiar.',JSON_ARRAY('testemunho','povo','escolha'),JSON_ARRAY('reescrever aliança','usar sua vida como chave'))
ON DUPLICATE KEY UPDATE name=VALUES(name),race_name=VALUES(race_name),role_name=VALUES(role_name),home_settlement_key=VALUES(home_settlement_key),faction_key=VALUES(faction_key),x_km=VALUES(x_km),y_km=VALUES(y_km),description=VALUES(description),values_json=VALUES(values_json),red_lines_json=VALUES(red_lines_json);

INSERT INTO regional_market_offers
(settlement_key,item_key,item_name,currency_key,buy_price,sell_price,water_index,stock_state) VALUES
('nhar_delta','filtro_aquanium','Filtro de Aquanium','coroas',12,5,1.15,'available'),('nhar_delta','capa_chuva','Capa de chuva','coroas',8,3,1.15,'available'),('nhar_delta','mapa_temporario','Mapa temporário','coroas',10,4,1.15,'available'),
('porto_lodoalto','peixe_salobro','Peixe salobro','coroas',4,2,1.05,'available'),('porto_lodoalto','remo_curto','Remo curto','coroas',9,4,1.05,'available'),('porto_lodoalto','rede_mangue','Rede de mangue','coroas',11,5,1.05,'available'),
('sete_aguas','odre_tratado','Odre tratado','coroas',5,2,0.95,'available'),('sete_aguas','antidoto_comum','Antídoto comum','coroas',13,6,0.95,'available'),('sete_aguas','sino_corrente','Sino de corrente','coroas',7,3,0.95,'available'),
('raiz_catedral','fibra_mangue','Fibra de mangue','coroas',6,3,1.10,'available'),('raiz_catedral','gancho_raiz','Gancho de raiz','coroas',10,4,1.10,'available'),('raiz_catedral','alga_salobra','Alga salobra','coroas',3,1,1.10,'available'),
('mare_oca','lanterna_caverna','Lanterna de caverna','coroas',10,4,1.20,'available'),('mare_oca','tampao_resonum','Tampão de Resonum','coroas',8,3,1.20,'available'),('mare_oca','sal_medicinal','Sal medicinal','coroas',6,2,1.20,'available'),
('varzea_errante','estaca_datada','Estaca datada','coroas',6,2,1.25,'available'),('varzea_errante','poncho_turfa','Poncho de turfa','coroas',9,4,1.25,'available'),('varzea_errante','mapa_temporario','Mapa temporário','coroas',12,5,1.25,'available'),
('farol_sal','sal_raiz','Sal de raiz','coroas',4,2,1.15,'available'),('farol_sal','sinal_concha','Sinal de concha','coroas',8,3,1.15,'available'),('farol_sal','antidoto_comum','Antídoto comum','coroas',14,6,1.15,'limited'),
('ponte_turfa','tabua_flexivel','Tábua flexível','coroas',9,4,1.30,'available'),('ponte_turfa','kit_rebites','Kit de rebites','coroas',13,6,1.30,'available'),('ponte_turfa','corda_vinha','Corda de vinha','coroas',7,3,1.30,'available'),
('lago_cego','antidoto_febre','Antídoto de febre','coroas',16,7,0.85,'limited'),('lago_cego','mascara_esporos','Máscara de esporos','coroas',10,4,0.85,'available'),('lago_cego','agua_tratada','Água tratada','coroas',4,2,0.85,'available'),
('vigilia_norte','capa_chuva','Capa de chuva','coroas',9,4,1.20,'available'),('vigilia_norte','mapa_fronteira','Mapa de fronteira','coroas',8,3,1.20,'available'),('vigilia_norte','racao_selada','Ração selada','coroas',6,3,1.20,'available'),
('porto_cinzento','passagem_fluvial','Passagem fluvial','coroas',10,4,1.25,'available'),('porto_cinzento','odre_tratado','Odre tratado','coroas',6,2,1.25,'available'),('porto_cinzento','caixa_impermeavel','Caixa impermeável','coroas',12,5,1.25,'available')
ON DUPLICATE KEY UPDATE item_name=VALUES(item_name),currency_key=VALUES(currency_key),buy_price=VALUES(buy_price),sell_price=VALUES(sell_price),water_index=VALUES(water_index),stock_state=VALUES(stock_state);

SELECT
 (SELECT COUNT(*) FROM regional_settlements WHERE region_slug='blackmarsh') AS assentamentos,
 (SELECT COUNT(*) FROM regional_routes WHERE region_slug='blackmarsh') AS rotas,
 (SELECT COUNT(*) FROM npc_definitions_v2 WHERE home_settlement_key IN (SELECT settlement_key FROM regional_settlements WHERE region_slug='blackmarsh') OR npc_key='asha_vael') AS npcs,
 (SELECT COUNT(*) FROM regional_market_offers WHERE settlement_key IN (SELECT settlement_key FROM regional_settlements WHERE region_slug='blackmarsh')) AS ofertas,
 (SELECT COUNT(*) FROM region_borders_v2 WHERE border_key IN ('blackmarsh_stonevale','stonevale_blackmarsh','blackmarsh_arkanor','arkanor_blackmarsh')) AS fronteiras;
