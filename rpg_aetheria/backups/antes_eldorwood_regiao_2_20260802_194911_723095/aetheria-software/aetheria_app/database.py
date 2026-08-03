from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Iterable

from .config import DatabaseSettings


CORE_SCHEMA_STATEMENTS = (
    """CREATE TABLE IF NOT EXISTS game_saves (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        character_id INT NOT NULL,
        slot_name VARCHAR(60) NOT NULL DEFAULT 'autosave',
        state_json JSON NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uq_character_slot (character_id, slot_name),
        CONSTRAINT fk_game_save_character FOREIGN KEY(character_id)
            REFERENCES characters_rpg(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    """CREATE TABLE IF NOT EXISTS game_event_log (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        character_id INT NOT NULL,
        event_type VARCHAR(80) NOT NULL,
        region_slug VARCHAR(80) NULL,
        scene_key VARCHAR(120) NULL,
        event_data JSON NULL,
        occurred_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_event_character_time (character_id, occurred_at),
        CONSTRAINT fk_game_event_character FOREIGN KEY(character_id)
            REFERENCES characters_rpg(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    """CREATE TABLE IF NOT EXISTS quest_definitions_v2 (
        quest_key VARCHAR(160) PRIMARY KEY,
        title VARCHAR(200) NOT NULL,
        category VARCHAR(80) NOT NULL,
        definition_json JSON NOT NULL,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    """CREATE TABLE IF NOT EXISTS character_world_facts (
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
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    """CREATE TABLE IF NOT EXISTS scheduled_world_events (
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
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    """CREATE TABLE IF NOT EXISTS character_quests_v2 (
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
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    """CREATE TABLE IF NOT EXISTS quest_objectives_v2 (
        character_id INT NOT NULL,
        quest_key VARCHAR(160) NOT NULL,
        objective_key VARCHAR(160) NOT NULL,
        status VARCHAR(40) NOT NULL,
        progress_value DECIMAL(12,3) NOT NULL DEFAULT 0,
        objective_state_json JSON NOT NULL,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY(character_id, quest_key, objective_key),
        CONSTRAINT fk_core_objective_character FOREIGN KEY(character_id)
            REFERENCES characters_rpg(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
)


class DatabaseUnavailable(RuntimeError):
    pass


@dataclass
class ConnectionResult:
    ok: bool
    message: str


class MySQLDatabase:
    """Conexão única, pequena e explícita. A senha nunca é gravada em arquivo."""

    def __init__(self, settings: DatabaseSettings):
        self.settings = settings
        self._connection = None

    @property
    def connected(self) -> bool:
        try:
            return bool(self._connection and self._connection.is_connected())
        except Exception:
            return False

    def connect(self, password: str) -> ConnectionResult:
        self.disconnect()
        try:
            import mysql.connector
        except ImportError:
            return ConnectionResult(False, "Instale mysql-connector-python para usar o banco.")

        try:
            self._connection = mysql.connector.connect(
                host=self.settings.host,
                port=self.settings.port,
                user=self.settings.user,
                password=password,
                database=self.settings.database,
                connection_timeout=5,
                autocommit=False,
                charset="utf8mb4",
                use_unicode=True,
            )
            self._connection.ping(reconnect=True, attempts=1, delay=0)
            return ConnectionResult(True, f"Conectado ao banco {self.settings.database}.")
        except Exception as exc:
            self._connection = None
            return ConnectionResult(False, f"Não foi possível conectar: {exc}")

    def disconnect(self) -> None:
        if self._connection is not None:
            try:
                self._connection.close()
            except Exception:
                pass
        self._connection = None

    def fetch_all(self, query: str, params: Iterable[Any] | None = None) -> list[dict]:
        if not self.connected:
            raise DatabaseUnavailable("O MySQL não está conectado.")
        cursor = self._connection.cursor(dictionary=True)
        try:
            cursor.execute(query, tuple(params or ()))
            return list(cursor.fetchall())
        finally:
            cursor.close()

    def fetch_one(self, query: str, params: Iterable[Any] | None = None) -> dict | None:
        rows = self.fetch_all(query, params)
        return rows[0] if rows else None

    def execute(self, query: str, params: Iterable[Any] | None = None) -> int:
        if not self.connected:
            raise DatabaseUnavailable("O MySQL não está conectado.")
        cursor = self._connection.cursor()
        try:
            cursor.execute(query, tuple(params or ()))
            self._connection.commit()
            return int(cursor.lastrowid or 0)
        except Exception:
            self._connection.rollback()
            raise
        finally:
            cursor.close()

    def execute_many(self, query: str, rows: Iterable[Iterable[Any]]) -> int:
        if not self.connected:
            raise DatabaseUnavailable("O MySQL não está conectado.")
        materialized = [tuple(row) for row in rows]
        if not materialized:
            return 0
        cursor = self._connection.cursor()
        try:
            cursor.executemany(query, materialized)
            self._connection.commit()
            return int(cursor.rowcount or 0)
        except Exception:
            self._connection.rollback()
            raise
        finally:
            cursor.close()

    def table_exists(self, table: str) -> bool:
        row = self.fetch_one(
            "SELECT COUNT(*) AS total FROM information_schema.tables "
            "WHERE table_schema=%s AND table_name=%s",
            (self.settings.database, table),
        )
        return bool(row and row["total"])


class WorldRepository:
    TABLES = (
        "regions", "biomes", "races", "species", "item_catalog",
        "characters_rpg", "game_saves", "character_world_facts",
        "scheduled_world_events", "character_quests_v2",
    )

    def __init__(self, database: MySQLDatabase):
        self.db = database

    def counts(self) -> dict[str, int | None]:
        result: dict[str, int | None] = {}
        for table in self.TABLES:
            try:
                if not self.db.table_exists(table):
                    result[table] = None
                    continue
                row = self.db.fetch_one(f"SELECT COUNT(*) AS total FROM `{table}`")
                result[table] = int(row["total"] if row else 0)
            except Exception:
                result[table] = None
        return result

    def races(self) -> list[dict]:
        if not self.db.table_exists("races"):
            return []
        return self.db.fetch_all(
            "SELECT id,slug,name,physical_description AS description,habitat,"
            "base_height_min,base_height_max FROM races ORDER BY id"
        )

    def regions(self) -> list[dict]:
        if not self.db.table_exists("regions"):
            return []
        return self.db.fetch_all(
            "SELECT id,slug,name,continent,climate,lore FROM regions ORDER BY id"
        )

    def species(self, limit: int = 500) -> list[dict]:
        if not self.db.table_exists("species"):
            return []
        return self.db.fetch_all(
            "SELECT common_name AS name,kingdom,class_name,behavior,threat,"
            "edible,poisonous,legendary FROM species ORDER BY kingdom,common_name LIMIT %s",
            (limit,),
        )

    def exploration_species(self, region_slug: str, limit: int = 1000) -> list[dict]:
        """Espécies válidas para encontros, já filtradas pelos biomas da região."""
        required = ("species", "species_biomes", "biomes", "regions")
        if not all(self.db.table_exists(table) for table in required):
            return []
        return self.db.fetch_all(
            "SELECT s.slug,s.common_name AS name,s.kingdom,s.behavior,s.threat,"
            "s.description,s.edible,s.poisonous,s.legendary,b.slug AS biome_slug,"
            "sb.encounter_weight FROM species s "
            "JOIN species_biomes sb ON sb.species_id=s.id "
            "JOIN biomes b ON b.id=sb.biome_id "
            "JOIN regions r ON r.id=b.region_id "
            "WHERE r.slug=%s ORDER BY b.id,s.kingdom,s.common_name LIMIT %s",
            (region_slug, limit),
        )

    def items(self, limit: int = 500) -> list[dict]:
        if not self.db.table_exists("item_catalog"):
            return []
        return self.db.fetch_all(
            "SELECT name,category_slug,item_kind,rarity,tier,damage_min,damage_max,"
            "defense,magic_power,effect_key FROM item_catalog ORDER BY category_slug,tier,name LIMIT %s",
            (limit,),
        )

    def save_character(self, name: str, race_slug: str, scene_key: str) -> int:
        race = self.db.fetch_one("SELECT id FROM races WHERE slug=%s", (race_slug,))
        race_id = race["id"] if race else None
        return self.db.execute(
            "INSERT INTO characters_rpg(name,race_id,current_scene_key) VALUES(%s,%s,%s)",
            (name, race_id, scene_key),
        )

    def save_game(self, character_id: int, state: dict, slot_name: str = "autosave") -> None:
        if not character_id or not self.db.table_exists("game_saves"):
            return
        payload = json.dumps(state, ensure_ascii=False)
        self.db.execute(
            "INSERT INTO game_saves(character_id,slot_name,state_json) VALUES(%s,%s,%s) "
            "ON DUPLICATE KEY UPDATE state_json=VALUES(state_json),updated_at=CURRENT_TIMESTAMP",
            (character_id, slot_name, payload),
        )
        self.db.execute(
            "UPDATE characters_rpg SET current_scene_key=%s WHERE id=%s",
            (state.get("scene_id"), character_id),
        )
        self.sync_core_state(character_id, state.get("core_state") or {})

    def load_game(self, character_id: int, slot_name: str = "autosave") -> dict | None:
        if not self.db.table_exists("game_saves"):
            return None
        row = self.db.fetch_one(
            "SELECT state_json FROM game_saves WHERE character_id=%s AND slot_name=%s",
            (character_id, slot_name),
        )
        if not row:
            return None
        payload = row.get("state_json")
        if isinstance(payload, dict):
            return payload
        if isinstance(payload, (bytes, bytearray)):
            payload = payload.decode("utf-8")
        return json.loads(payload) if isinstance(payload, str) else None

    def ensure_core_schema(self, quest_definitions: dict[str, dict] | None = None) -> None:
        for statement in CORE_SCHEMA_STATEMENTS:
            self.db.execute(statement)
        rows = []
        for quest_id, definition in (quest_definitions or {}).items():
            rows.append((
                quest_id,
                str(definition.get("title") or quest_id),
                str(definition.get("category") or "side"),
                json.dumps(definition, ensure_ascii=False),
            ))
        self.db.execute_many(
            "INSERT INTO quest_definitions_v2(quest_key,title,category,definition_json) "
            "VALUES(%s,%s,%s,%s) ON DUPLICATE KEY UPDATE title=VALUES(title),"
            "category=VALUES(category),definition_json=VALUES(definition_json)",
            rows,
        )

    def sync_core_state(self, character_id: int, core: dict) -> None:
        if not core or not self.db.table_exists("character_world_facts"):
            return
        facts = []
        for key, record in (core.get("facts") or {}).items():
            facts.append((
                character_id, key,
                json.dumps(record.get("value"), ensure_ascii=False),
                record.get("category", "world"), record.get("source"),
                record.get("certainty", "confirmed"),
                record.get("visibility", "character"),
                int(record.get("day") or 1), int(record.get("absolute_minute") or 0),
                record.get("description", ""),
            ))
        self.db.execute_many(
            "INSERT INTO character_world_facts(character_id,fact_key,fact_value_json,category,"
            "source_key,certainty,visibility,occurred_day,occurred_minute,description) "
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE "
            "fact_value_json=VALUES(fact_value_json),category=VALUES(category),source_key=VALUES(source_key),"
            "certainty=VALUES(certainty),visibility=VALUES(visibility),occurred_day=VALUES(occurred_day),"
            "occurred_minute=VALUES(occurred_minute),description=VALUES(description)",
            facts,
        )
        events = []
        for event in core.get("scheduled_events") or []:
            events.append((
                character_id, event.get("event_id"), event.get("event_type"),
                int(event.get("due_absolute_minute") or 0), event.get("status", "scheduled"),
                event.get("title", "Evento"), json.dumps(event, ensure_ascii=False),
            ))
        self.db.execute_many(
            "INSERT INTO scheduled_world_events(character_id,event_key,event_type,due_absolute_minute,status,title,event_json) "
            "VALUES(%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE event_type=VALUES(event_type),"
            "due_absolute_minute=VALUES(due_absolute_minute),status=VALUES(status),title=VALUES(title),"
            "event_json=VALUES(event_json)",
            events,
        )
        quests = []
        objectives = []
        for quest_id, quest in (core.get("quests") or {}).items():
            quests.append((
                character_id, quest_id, quest.get("status", "unknown"), quest.get("stage"),
                quest.get("outcome"), json.dumps(quest, ensure_ascii=False),
            ))
            for objective_id, objective in (quest.get("objectives") or {}).items():
                objectives.append((
                    character_id, quest_id, objective_id, objective.get("status", "active"),
                    float(objective.get("progress") or 0), json.dumps(objective, ensure_ascii=False),
                ))
        self.db.execute_many(
            "INSERT INTO character_quests_v2(character_id,quest_key,status,current_stage,outcome_key,quest_state_json) "
            "VALUES(%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE status=VALUES(status),"
            "current_stage=VALUES(current_stage),outcome_key=VALUES(outcome_key),quest_state_json=VALUES(quest_state_json)",
            quests,
        )
        self.db.execute_many(
            "INSERT INTO quest_objectives_v2(character_id,quest_key,objective_key,status,progress_value,objective_state_json) "
            "VALUES(%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE status=VALUES(status),"
            "progress_value=VALUES(progress_value),objective_state_json=VALUES(objective_state_json)",
            objectives,
        )

    def saves(self) -> list[dict]:
        if not self.db.table_exists("characters_rpg"):
            return []
        has_saves = self.db.table_exists("game_saves")
        if has_saves:
            return self.db.fetch_all(
                "SELECT c.id,c.name,COALESCE(r.name,'Raça desconhecida') AS race,"
                "c.current_scene_key,c.created_at,gs.updated_at,"
                "CASE WHEN gs.id IS NULL THEN 0 ELSE 1 END AS has_save "
                "FROM characters_rpg c LEFT JOIN races r ON r.id=c.race_id "
                "LEFT JOIN game_saves gs ON gs.character_id=c.id AND gs.slot_name='autosave' "
                "ORDER BY COALESCE(gs.updated_at,c.created_at) DESC LIMIT 100"
            )
        return self.db.fetch_all(
            "SELECT c.id,c.name,COALESCE(r.name,'Raça desconhecida') AS race,"
            "c.current_scene_key,c.created_at,0 AS has_save FROM characters_rpg c "
            "LEFT JOIN races r ON r.id=c.race_id ORDER BY c.id DESC LIMIT 100"
        )
