"""Instala o Núcleo Persistente v2 dentro do projeto rpg_aetheria.

Uso:
    py ATUALIZAR_AETHERIA.py
    py ATUALIZAR_AETHERIA.py "C:\\caminho\\para\\rpg_aetheria"
"""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path


SOURCE = Path(__file__).resolve().parent


def locate_default() -> Path | None:
    user = Path.home()
    candidates = (
        user / "OneDrive" / "Área de Trabalho" / "RPG" / "rpg_aetheria",
        user / "OneDrive" / "Desktop" / "RPG" / "rpg_aetheria",
        user / "Desktop" / "RPG" / "rpg_aetheria",
        SOURCE.parent,
        SOURCE.parent.parent,
    )
    for candidate in candidates:
        if (candidate / "data" / "scenes").is_dir():
            return candidate.resolve()
    return None


def validate_project(project: Path) -> None:
    if not (project / "data" / "scenes").is_dir():
        raise SystemExit(f"Projeto inválido: não existe {project / 'data' / 'scenes'}")


def validate_core_package() -> None:
    required = (
        SOURCE / "aetheria_app" / "core" / "runtime.py",
        SOURCE / "aetheria_app" / "core" / "world.py",
        SOURCE / "aetheria_app" / "core" / "actions.py",
        SOURCE / "aetheria_app" / "core" / "events.py",
        SOURCE / "aetheria_app" / "core" / "quests.py",
        SOURCE / "content" / "quests" / "frostreach_tovin.json",
        SOURCE / "mysql" / "core_v2.sql",
        SOURCE / "manifest_core_v2.json",
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Pacote do Núcleo v2 incompleto:\n" + "\n".join(missing))
    definition = json.loads(required[-3].read_text(encoding="utf-8"))
    if definition.get("id") != "frostreach_o_barco_que_voltou_sozinho":
        raise SystemExit("A definição da missão-piloto de Tovin é inválida.")


def backup_interface(destination: Path, project: Path) -> Path | None:
    if not destination.is_dir():
        return None
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup = project / "backups" / f"aetheria_software_antes_nucleo_v2_{stamp}"
    for relative in (
        Path("aetheria_app"),
        Path("content"),
        Path("mysql"),
        Path("iniciar_software.py"),
        Path("INICIAR_AETHERIA.bat"),
        Path("requirements.txt"),
    ):
        source = destination / relative
        target = backup / relative
        if source.is_dir():
            shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        elif source.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    return backup


def copy_software(destination: Path) -> None:
    if SOURCE.resolve() == destination.resolve():
        return
    destination.mkdir(parents=True, exist_ok=True)
    for source in SOURCE.rglob("*"):
        relative = source.relative_to(SOURCE)
        if "__pycache__" in relative.parts or source.suffix == ".pyc":
            continue
        if relative == Path("config/database.json"):
            continue
        target = destination / relative
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def install_frostreach_scenes(project: Path) -> tuple[int, Path]:
    candidates = (
        SOURCE.parent / "frostreach-100-ramificacoes",
        project / "frostreach-100-ramificacoes",
    )
    package = next((path for path in candidates if (path / "frostreach_fase_inicial_100.json").is_file()), None)
    if package is None:
        raise SystemExit("Pacote frostreach-100-ramificacoes não foi localizado.")
    scenes = project / "data" / "scenes"
    for name in ("00_despertar_frostreach.json", "frostreach_fase_inicial_100.json"):
        shutil.copy2(package / name, scenes / name)
    project_package = project / "frostreach-100-ramificacoes"
    project_package.mkdir(parents=True, exist_ok=True)
    for name in (
        "00_despertar_frostreach.json", "frostreach_fase_inicial_100.json",
        "instalar_frostreach_100.py", "reconstruir_continuidade.py",
        "README.md", "PLANO_RITMO_LENTO_FROSTREACH.md",
        "manifest_frostreach_fase_inicial.json",
    ):
        source = package / name
        if source.is_file() and source.resolve() != (project_package / name).resolve():
            shutil.copy2(source, project_package / name)
    data = json.loads((scenes / "frostreach_fase_inicial_100.json").read_text(encoding="utf-8"))
    root = json.loads((scenes / "00_despertar_frostreach.json").read_text(encoding="utf-8"))
    ids = {root["id"], *(scene["id"] for scene in data)}
    if len(ids) != 100:
        raise SystemExit(f"Validação falhou: esperado 100 cenas de Frostreach, encontrado {len(ids)}.")
    return len(ids), package


def main() -> int:
    parser = argparse.ArgumentParser(description="Atualiza Aetheria com o Núcleo Persistente v2.")
    parser.add_argument("project", nargs="?", help="Pasta principal rpg_aetheria")
    parser.add_argument("--dry-run", action="store_true", help="Valida caminhos sem copiar arquivos")
    args = parser.parse_args()
    project = Path(args.project).expanduser().resolve() if args.project else locate_default()
    if project is None:
        raise SystemExit("Não encontrei rpg_aetheria automaticamente. Informe o caminho como argumento.")
    validate_project(project)
    validate_core_package()
    destination = project / "aetheria-software"
    if args.dry_run:
        package = next((path for path in (
            SOURCE.parent / "frostreach-100-ramificacoes",
            project / "frostreach-100-ramificacoes",
        ) if (path / "frostreach_fase_inicial_100.json").is_file()), None)
        if package is None:
            raise SystemExit("Pacote frostreach-100-ramificacoes não foi localizado.")
        data = json.loads((package / "frostreach_fase_inicial_100.json").read_text(encoding="utf-8"))
        root = json.loads((package / "00_despertar_frostreach.json").read_text(encoding="utf-8"))
        scene_count = len({root["id"], *(scene["id"] for scene in data)})
        print(f"DRY-RUN OK | núcleo=v2 | projeto={project} | destino={destination} | cenas={scene_count}")
        return 0
    backup = backup_interface(destination, project)
    copy_software(destination)
    scene_count, scene_package = install_frostreach_scenes(project)

    print("=" * 64)
    print("AETHERIA — NÚCLEO PERSISTENTE V2 INSTALADO")
    print("=" * 64)
    print(f"Projeto: {project}")
    print(f"Interface: {destination}")
    print(f"Cenas de Frostreach validadas: {scene_count}")
    print("Serviços: WorldState, GameClock, ActionResolver, EventScheduler e QuestEngine")
    print("Missão-piloto: O barco que voltou sozinho")
    print("MySQL: tabelas do núcleo serão preparadas automaticamente ao conectar")
    print("Compatibilidade: saves anteriores são migrados ao carregar")
    print(f"Origem das cenas: {scene_package}")
    print(f"Backup anterior: {backup or 'não havia interface anterior'}")
    print("\nFeche qualquer janela antiga e abra:")
    print(destination / "INICIAR_AETHERIA.bat")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
