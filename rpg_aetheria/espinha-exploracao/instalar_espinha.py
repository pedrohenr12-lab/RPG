"""Instala a exploração da Espinha e aplica um pequeno gancho ao motor de cenas.

Execute este arquivo dentro da pasta rpg_aetheria. Ele cria cópias .bak antes
de alterar scene_engine.py e tenta registrar a cena inicial da região.
"""
from pathlib import Path
import re
import shutil

origem = Path(__file__).resolve().parent
projeto = Path.cwd()
scenes = projeto / "data" / "scenes"
engine = projeto / "engine"
if not scenes.is_dir() or not engine.is_dir():
    raise SystemExit("Abra o PowerShell dentro da pasta rpg_aetheria e tente novamente.")

for arquivo in ("00_despertar_espinha.json", "espinha_cenas_sensoriais.json"):
    shutil.copy2(origem / arquivo, scenes / arquivo)
shutil.copy2(origem / "engine" / "espinha_exploration.py", engine / "espinha_exploration.py")

motor = engine / "scene_engine.py"
texto = motor.read_text(encoding="utf-8")
marca = "# GANCHO_ESPINHA_EXPLORACAO"
gancho = '''    # GANCHO_ESPINHA_EXPLORACAO
    if opcao.get("modo") == "exploracao_espinha":
        aplicar_efeitos(opcao.get("efeitos"), estado)
        from engine.espinha_exploration import iniciar_exploracao_espinha
        return iniciar_exploracao_espinha(estado, opcao.get("bioma_inicial", "aleatorio"))
\n'''
if marca not in texto:
    if "    sucesso = True\n" not in texto:
        raise SystemExit("Cenas copiadas, mas não encontrei o ponto seguro para integrar scene_engine.py. Veja INTEGRAR_MAIN.md.")
    shutil.copy2(motor, motor.with_suffix(".py.bak_espinha"))
    motor.write_text(texto.replace("    sucesso = True\n", gancho + "    sucesso = True\n", 1), encoding="utf-8")

# Tenta mudar somente o valor cena_inicial da entrada que já contém 'espinha'.
alterou_regiao = False
for candidato in (projeto / "data" / "regions.py", projeto / "data" / "regioes.py", projeto / "main.py"):
    if not candidato.is_file():
        continue
    dado = candidato.read_text(encoding="utf-8")
    padrao = r"((?:espinha_do_mundo|espinha_mundo|espinha)[\s\S]{0,600}?[\"']cena_inicial[\"']\s*:\s*)[\"'][^\"']+[\"']"
    novo, n = re.subn(padrao, r'\1"00_despertar_espinha"', dado, count=1, flags=re.IGNORECASE)
    if n:
        shutil.copy2(candidato, candidato.with_suffix(candidato.suffix + ".bak_espinha"))
        candidato.write_text(novo, encoding="utf-8")
        alterou_regiao = True
        break

print("Exploração da Espinha instalada.")
print("Gancho do motor: pronto.")
print("Cena inicial da região atualizada automaticamente." if alterou_regiao else "Cena inicial não foi localizada automaticamente; siga INTEGRAR_MAIN.md.")
