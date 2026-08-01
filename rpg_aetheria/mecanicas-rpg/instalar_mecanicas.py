import shutil
from pathlib import Path

origem = Path(__file__).resolve().parent / "engine"
destino = Path.cwd() / "engine"
if not destino.is_dir():
    raise SystemExit("Abra o terminal dentro da pasta rpg_aetheria e rode este comando novamente.")
backup = destino / "backup_mecanicas_rpg"
backup.mkdir(exist_ok=True)
for nome in ("game_state.py", "scene_engine.py"):
    arquivo = destino / nome
    if arquivo.exists(): shutil.copy2(arquivo, backup / nome)
for arquivo in origem.glob("*.py"):
    shutil.copy2(arquivo, destino / arquivo.name)
print("Mecânicas instaladas. Backup em engine/backup_mecanicas_rpg")
