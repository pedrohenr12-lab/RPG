from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppPaths:
    software_root: Path
    project_root: Path
    data_root: Path
    scenes_root: Path
    races_file: Path
    intro_file: Path
    arquivo_configuracao: Path

    @classmethod
    def detectar(cls, software_root: Path) -> "AppPaths":
        software_root = software_root.resolve()
        configured = os.getenv("AETHERIA_PROJECT_ROOT", "").strip()
        candidates: list[Path] = []
        if configured:
            candidates.append(Path(configured))

        # O aplicativo pode ser executado diretamente da pasta de entregas do
        # Codex ou depois de ser copiado para rpg_aetheria. Procure primeiro ao
        # redor do executável e do diretório atual; depois verifique os locais
        # usuais do projeto no Windows. Isso evita cair silenciosamente no modo
        # genérico só porque a interface foi aberta de outra pasta.
        candidates.extend((
            software_root.parent,
            software_root,
            software_root.parent.parent,
            Path.cwd(),
            *Path.cwd().parents,
        ))
        user = Path.home()
        candidates.extend((
            user / "OneDrive" / "Área de Trabalho" / "RPG" / "rpg_aetheria",
            user / "OneDrive" / "Desktop" / "RPG" / "rpg_aetheria",
            user / "Desktop" / "RPG" / "rpg_aetheria",
            user / "Documents" / "RPG" / "rpg_aetheria",
        ))

        expanded: list[Path] = []
        for candidate in candidates:
            expanded.append(candidate)
            expanded.append(candidate / "rpg_aetheria")

        project_root = software_root.parent
        seen: set[str] = set()
        for candidate in expanded:
            try:
                key = str(candidate.resolve()).casefold()
            except OSError:
                continue
            if key in seen:
                continue
            seen.add(key)
            if (candidate / "data" / "scenes").is_dir():
                project_root = candidate.resolve()
                break

        config_dir = software_root / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        data_root = project_root / "data"
        return cls(
            software_root=software_root,
            project_root=project_root,
            data_root=data_root,
            scenes_root=data_root / "scenes",
            races_file=data_root / "characters" / "races.json",
            intro_file=data_root / "lore" / "intro_mundo.txt",
            arquivo_configuracao=config_dir / "database.json",
        )


@dataclass
class DatabaseSettings:
    host: str = "127.0.0.1"
    port: int = 3306
    user: str = "root"
    database: str = "aetheria_rpg"

    @classmethod
    def carregar(cls, path: Path) -> "DatabaseSettings":
        env = {
            "host": os.getenv("AETHERIA_DB_HOST"),
            "port": os.getenv("AETHERIA_DB_PORT"),
            "user": os.getenv("AETHERIA_DB_USER"),
            "database": os.getenv("AETHERIA_DB_NAME"),
        }
        data: dict = {}
        if path.exists():
            try:
                loaded = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    data.update(loaded)
            except (OSError, ValueError):
                pass
        data.update({key: value for key, value in env.items() if value not in (None, "")})
        try:
            data["port"] = int(data.get("port", 3306))
        except (TypeError, ValueError):
            data["port"] = 3306
        allowed = {key: data[key] for key in ("host", "port", "user", "database") if key in data}
        return cls(**allowed)

    def salvar(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def senha_ambiente() -> str:
        return os.getenv("AETHERIA_DB_PASSWORD", "")
