import shutil
from pathlib import Path
p = Path(__file__).resolve().parent; destino = Path.cwd()
if not (destino / "engine").is_dir(): raise SystemExit("Execute dentro de rpg_aetheria.")
(destino / "data" / "world").mkdir(parents=True, exist_ok=True)
shutil.copy2(p / "engine" / "world_database.py", destino / "engine" / "world_database.py")
shutil.copy2(p / "engine" / "game_state.py", destino / "engine" / "game_state.py")
shutil.copy2(p / "data" / "world" / "eldorwood.json", destino / "data" / "world" / "eldorwood.json")
print("Banco narrativo instalado.")
