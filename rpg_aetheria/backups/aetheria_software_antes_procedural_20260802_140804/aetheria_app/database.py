from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Iterable

from .config import DatabaseSettings


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

    def table_exists(self, table: str) -> bool:
        row = self.fetch_one(
            "SELECT COUNT(*) AS total FROM information_schema.tables "
            "WHERE table_schema=%s AND table_name=%s",
            (self.settings.database, table),
        )
        return bool(row and row["total"])


class WorldRepository:
    TABLES = ("regions", "biomes", "races", "species", "item_catalog", "characters_rpg", "game_saves")

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

    def saves(self) -> list[dict]:
        if not self.db.table_exists("characters_rpg"):
            return []
        return self.db.fetch_all(
            "SELECT c.id,c.name,COALESCE(r.name,'Raça desconhecida') AS race,"
            "c.current_scene_key,c.created_at FROM characters_rpg c "
            "LEFT JOIN races r ON r.id=c.race_id ORDER BY c.id DESC LIMIT 100"
        )
