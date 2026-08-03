-- AETHERIA / EUDORA — NÚCLEO DE COMBATE E PROGRESSÃO V1
-- Opcional: o software cria estas tabelas automaticamente ao conectar ao MySQL.
-- Este arquivo existe para inspeção e instalação manual pelo MySQL Workbench.
USE aetheria_rpg;

CREATE TABLE IF NOT EXISTS career_definitions (
    career_key VARCHAR(80) PRIMARY KEY,
    name VARCHAR(140) NOT NULL,
    category ENUM('battle','profession') NOT NULL,
    role_name VARCHAR(120) NOT NULL,
    resource_name VARCHAR(80) NOT NULL,
    description TEXT NOT NULL,
    innate_name VARCHAR(160) NOT NULL,
    innate_description TEXT NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS skill_nodes (
    skill_key VARCHAR(180) PRIMARY KEY,
    career_key VARCHAR(80) NOT NULL,
    branch_name VARCHAR(140) NOT NULL,
    name VARCHAR(180) NOT NULL,
    description TEXT NOT NULL,
    tier TINYINT UNSIGNED NOT NULL,
    point_cost TINYINT UNSIGNED NOT NULL,
    prerequisites_json JSON NOT NULL,
    effects_json JSON NOT NULL,
    FOREIGN KEY(career_key) REFERENCES career_definitions(career_key) ON DELETE CASCADE,
    INDEX idx_skill_career_branch(career_key, branch_name, tier)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS character_progression (
    character_id INT PRIMARY KEY,
    battle_class_key VARCHAR(80) NOT NULL,
    profession_key VARCHAR(80) NOT NULL,
    class_level SMALLINT UNSIGNED NOT NULL DEFAULT 1,
    profession_level SMALLINT UNSIGNED NOT NULL DEFAULT 1,
    skill_points SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    unlocked_skills_json JSON NOT NULL,
    equipment_json JSON NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(character_id) REFERENCES characters_rpg(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS combat_history (
    combat_key VARCHAR(64) PRIMARY KEY,
    character_id INT NOT NULL,
    region_slug VARCHAR(80) NOT NULL,
    enemy_name VARCHAR(180) NULL,
    outcome_key VARCHAR(60) NOT NULL,
    rounds SMALLINT UNSIGNED NOT NULL,
    summary_json JSON NOT NULL,
    occurred_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_combat_character(character_id, occurred_at),
    FOREIGN KEY(character_id) REFERENCES characters_rpg(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- As 40 carreiras e os 600 nós são sincronizados pelo software a partir da
-- fonte canônica combat/careers.py. Assim o banco não diverge das regras usadas
-- pelo motor e a sincronização pode ser executada novamente sem duplicações.
