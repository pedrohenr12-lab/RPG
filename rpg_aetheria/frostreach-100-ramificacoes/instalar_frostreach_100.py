from __future__ import annotations
import json
import shutil
from datetime import datetime
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
FILES = ("00_despertar_frostreach.json", "frostreach_fase_inicial_100.json")

def main():
    project = PACKAGE.parent
    if not (project / "data" / "scenes").is_dir():
        print("ERRO: copie esta pasta para dentro de rpg_aetheria antes de executar.")
        raise SystemExit(1)
    scenes = project / "data" / "scenes"
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = scenes / f"backup_frostreach_antes_100_{stamp}"
    backup.mkdir(parents=True, exist_ok=True)
    old_root = scenes / "00_despertar_frostreach.json"
    if old_root.exists():
        shutil.copy2(old_root, backup / old_root.name)
    for name in FILES:
        shutil.copy2(PACKAGE / name, scenes / name)
    world = project / "data" / "world"
    world.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PACKAGE / "manifest_frostreach_fase_inicial.json", world / "manifest_frostreach_fase_inicial.json")

    print("Frostreach instalada: 100 cenas e 300 escolhas.")
    print(f"Backup da cena inicial anterior: {backup}")
    print("A interface existente foi preservada. Use aetheria-software/ATUALIZAR_AETHERIA.bat para atualizá-la.")
    print("A cena inicial continua sendo 00_despertar_frostreach.")

if __name__ == "__main__":
    main()
