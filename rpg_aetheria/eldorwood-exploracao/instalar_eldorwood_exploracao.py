"""Instala Eldorwood e seu gancho de exploração no projeto rpg_aetheria."""
from pathlib import Path
import re
import shutil

origem = Path(__file__).resolve().parent
projeto = Path.cwd()
scenes, engine = projeto / "data" / "scenes", projeto / "engine"
if not scenes.is_dir() or not engine.is_dir():
    raise SystemExit("Abra o PowerShell dentro de rpg_aetheria e tente novamente.")
for arquivo in ("00_despertar_eldorwood.json", "eldorwood_cenas_sensoriais.json"):
    shutil.copy2(origem / arquivo, scenes / arquivo)
shutil.copy2(origem / "engine" / "eldorwood_exploration.py", engine / "eldorwood_exploration.py")

motor = engine / "scene_engine.py"
texto = motor.read_text(encoding="utf-8")
marca = "# GANCHO_ELDORWOOD_EXPLORACAO"
gancho = '''    # GANCHO_ELDORWOOD_EXPLORACAO
    if opcao.get("modo") == "exploracao_eldorwood":
        aplicar_efeitos(opcao.get("efeitos"), estado)
        from engine.eldorwood_exploration import iniciar_exploracao_eldorwood
        return iniciar_exploracao_eldorwood(estado, opcao.get("bioma_inicial", "aleatorio"))

'''
if marca not in texto:
    if "    sucesso = True\n" not in texto:
        raise SystemExit("Cenas copiadas, mas não encontrei o ponto seguro de scene_engine.py. Veja INTEGRAR_MAIN.md.")
    shutil.copy2(motor, motor.with_suffix(".py.bak_eldorwood"))
    motor.write_text(texto.replace("    sucesso = True\n", gancho + "    sucesso = True\n", 1), encoding="utf-8")

alterou = False
for candidato in (projeto / "data" / "regions.py", projeto / "data" / "regioes.py", projeto / "main.py"):
    if not candidato.is_file():
        continue
    dado = candidato.read_text(encoding="utf-8")
    padrao = r"(eldorwood[\s\S]{0,600}?[\"']cena_inicial[\"']\s*:\s*)[\"'][^\"']+[\"']"
    novo, n = re.subn(padrao, r'\1"00_despertar_eldorwood"', dado, count=1, flags=re.IGNORECASE)
    if n:
        shutil.copy2(candidato, candidato.with_suffix(candidato.suffix + ".bak_eldorwood"))
        candidato.write_text(novo, encoding="utf-8")
        alterou = True
        break
print("Exploração de Eldorwood instalada.")
print("Cena inicial atualizada automaticamente." if alterou else "Cena inicial não localizada automaticamente; veja INTEGRAR_MAIN.md.")

