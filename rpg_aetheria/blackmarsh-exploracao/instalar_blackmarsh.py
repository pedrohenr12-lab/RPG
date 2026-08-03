"""Instala Blackmarsh e o gancho de exploração no projeto rpg_aetheria."""
from pathlib import Path
import re
import shutil

origem = Path(__file__).resolve().parent
projeto = Path.cwd()
scenes, engine = projeto / "data" / "scenes", projeto / "engine"
if not scenes.is_dir() or not engine.is_dir():
    raise SystemExit("Abra o PowerShell dentro da pasta rpg_aetheria e tente novamente.")
for arquivo in ("00_despertar_blackmarsh.json", "blackmarsh_cenas_sensoriais.json"):
    shutil.copy2(origem / arquivo, scenes / arquivo)
shutil.copy2(origem / "engine" / "blackmarsh_exploration.py", engine / "blackmarsh_exploration.py")

motor = engine / "scene_engine.py"
texto = motor.read_text(encoding="utf-8")
marca = "# GANCHO_BLACKMARSH_EXPLORACAO"
gancho = '''    # GANCHO_BLACKMARSH_EXPLORACAO
    if opcao.get("modo") == "exploracao_blackmarsh":
        aplicar_efeitos(opcao.get("efeitos"), estado)
        from engine.blackmarsh_exploration import iniciar_exploracao_blackmarsh
        return iniciar_exploracao_blackmarsh(estado, opcao.get("bioma_inicial", "aleatorio"))
\n'''
if marca not in texto:
    if "    sucesso = True\n" not in texto:
        raise SystemExit("Cenas copiadas, mas não encontrei o ponto seguro para integrar scene_engine.py. Veja INTEGRAR_MAIN.md.")
    shutil.copy2(motor, motor.with_suffix(".py.bak_blackmarsh"))
    motor.write_text(texto.replace("    sucesso = True\n", gancho + "    sucesso = True\n", 1), encoding="utf-8")

alterou = False
for candidato in (projeto / "data" / "regions.py", projeto / "data" / "regioes.py", projeto / "main.py"):
    if not candidato.is_file():
        continue
    dado = candidato.read_text(encoding="utf-8")
    padrao = r"(blackmarsh[\s\S]{0,600}?[\"']cena_inicial[\"']\s*:\s*)[\"'][^\"']+[\"']"
    novo, n = re.subn(padrao, r'\1"00_despertar_blackmarsh"', dado, count=1, flags=re.IGNORECASE)
    if n:
        shutil.copy2(candidato, candidato.with_suffix(candidato.suffix + ".bak_blackmarsh"))
        candidato.write_text(novo, encoding="utf-8")
        alterou = True
        break
print("Exploração de Blackmarsh instalada.")
print("Cena inicial atualizada automaticamente." if alterou else "Cena inicial não localizada automaticamente; veja INTEGRAR_MAIN.md.")
