import shutil
from pathlib import Path

origem = Path(__file__).resolve().parent
destino = Path.cwd() / "data" / "scenes"
if not destino.is_dir(): raise SystemExit("Abra o terminal dentro de rpg_aetheria e tente novamente.")
for nome in ("00_despertar.json", "01_vila_eldor.json", "eldorwood_exploracao.json", "eldorwood_racas_e_bestiario.json"):
    shutil.copy2(origem / nome, destino / nome)
print("Cenas de Eldorwood instaladas.")
