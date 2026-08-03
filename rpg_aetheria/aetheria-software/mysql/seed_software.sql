-- Persistência da interface desktop de Aetheria.
-- Execute depois de schema.sql. Seguro para executar novamente.
USE aetheria_rpg;

CREATE TABLE IF NOT EXISTS game_saves (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    character_id INT NOT NULL,
    slot_name VARCHAR(60) NOT NULL DEFAULT 'autosave',
    state_json JSON NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_character_slot (character_id, slot_name),
    CONSTRAINT fk_game_save_character
        FOREIGN KEY (character_id) REFERENCES characters_rpg(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS game_event_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    character_id INT NOT NULL,
    event_type VARCHAR(80) NOT NULL,
    region_slug VARCHAR(80) NULL,
    scene_key VARCHAR(120) NULL,
    event_data JSON NULL,
    occurred_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_event_character_time (character_id, occurred_at),
    CONSTRAINT fk_game_event_character
        FOREIGN KEY (character_id) REFERENCES characters_rpg(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS quest_definitions_v2 (
    quest_key VARCHAR(160) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    category VARCHAR(80) NOT NULL,
    definition_json JSON NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS character_world_facts (
    character_id INT NOT NULL,
    fact_key VARCHAR(220) NOT NULL,
    fact_value_json JSON NULL,
    category VARCHAR(60) NOT NULL DEFAULT 'world',
    source_key VARCHAR(180) NULL,
    certainty VARCHAR(40) NOT NULL DEFAULT 'confirmed',
    visibility VARCHAR(40) NOT NULL DEFAULT 'character',
    occurred_day INT NOT NULL DEFAULT 1,
    occurred_minute INT NOT NULL DEFAULT 0,
    description TEXT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(character_id, fact_key),
    CONSTRAINT fk_core_fact_character FOREIGN KEY(character_id)
        REFERENCES characters_rpg(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS scheduled_world_events (
    character_id INT NOT NULL,
    event_key VARCHAR(80) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    due_absolute_minute INT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'scheduled',
    title VARCHAR(200) NOT NULL,
    event_json JSON NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(character_id, event_key),
    INDEX idx_core_event_due(character_id, status, due_absolute_minute),
    CONSTRAINT fk_core_event_character FOREIGN KEY(character_id)
        REFERENCES characters_rpg(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS character_quests_v2 (
    character_id INT NOT NULL,
    quest_key VARCHAR(160) NOT NULL,
    status VARCHAR(40) NOT NULL,
    current_stage VARCHAR(120) NULL,
    outcome_key VARCHAR(120) NULL,
    quest_state_json JSON NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(character_id, quest_key),
    INDEX idx_core_quest_status(character_id, status),
    CONSTRAINT fk_core_quest_character FOREIGN KEY(character_id)
        REFERENCES characters_rpg(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS quest_objectives_v2 (
    character_id INT NOT NULL,
    quest_key VARCHAR(160) NOT NULL,
    objective_key VARCHAR(160) NOT NULL,
    status VARCHAR(40) NOT NULL,
    progress_value DECIMAL(12,3) NOT NULL DEFAULT 0,
    objective_state_json JSON NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(character_id,quest_key,objective_key),
    CONSTRAINT fk_core_objective_character FOREIGN KEY(character_id)
        REFERENCES characters_rpg(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SELECT COUNT(*) AS salvamentos_existentes FROM game_saves;
