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

SELECT COUNT(*) AS salvamentos_existentes FROM game_saves;
