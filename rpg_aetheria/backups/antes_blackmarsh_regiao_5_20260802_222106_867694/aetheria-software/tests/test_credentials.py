from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from aetheria_app.config import DatabaseSettings
from aetheria_app.credential_store import WindowsCredentialStore


class CredentialStoreTests(unittest.TestCase):
    def test_target_identifies_connection_without_containing_password(self) -> None:
        settings = DatabaseSettings(
            host="127.0.0.1", port=3306, user="root", database="aetheria_rpg",
        )
        target = WindowsCredentialStore.target_name(settings)
        self.assertEqual(target, "Aetheria/MySQL/127.0.0.1:3306/aetheria_rpg/root")
        self.assertNotIn("senha", target.casefold())

    def test_database_json_never_contains_a_password_field(self) -> None:
        settings = DatabaseSettings()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "database.json"
            settings.salvar(path)
            raw = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(set(raw), {"host", "port", "user", "database"})
        self.assertNotIn("password", raw)
        self.assertNotIn("senha", raw)

    def test_non_windows_load_is_a_safe_empty_fallback(self) -> None:
        if WindowsCredentialStore.available():
            self.skipTest("Este teste cobre somente o fallback fora do Windows.")
        self.assertEqual(WindowsCredentialStore.load(DatabaseSettings()), "")
        self.assertFalse(WindowsCredentialStore.delete(DatabaseSettings()))


if __name__ == "__main__":
    unittest.main()
