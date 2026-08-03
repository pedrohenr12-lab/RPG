"""Substitui as cenas antigas de Frostreach por exploração livre detalhada.

Os arquivos antigos conhecidos são copiados para data/scenes/backup_frostreach_legacy
antes de serem removidos. Isso permite restaurá-los se necessário.
"""
from pathlib import Path
import re
import shutil

origem = Path(__file__).resolve().parent
projeto = Path.cwd()
scenes, engine = projeto / "data" / "scenes", projeto / "engine"
if not scenes.is_dir() or not engine.is_dir():
    raise SystemExit("Abra o PowerShell dentro de rpg_aetheria e tente novamente.")

backup = scenes / "backup_frostreach_legacy"
legados = ("00_despertar_frostreach.json", "00b_frostreach_abrigo.json", "01_stonhelm_hub.json", "frostreach_expedicao.json")
for nome in legados:
    antigo = scenes / nome
    if antigo.is_file():
        backup.mkdir(exist_ok=True)
        shutil.copy2(antigo, backup / nome)
        antigo.unlink()

for arquivo in ("00_despertar_frostreach.json", "frostreach_cenas_sensoriais.json"):
    shutil.copy2(origem / arquivo, scenes / arquivo)
shutil.copy2(origem / "engine" / "frostreach_exploration.py", engine / "frostreach_exploration.py")

motor = engine / "scene_engine.py"
texto = motor.read_text(encoding="utf-8")
marca = "# GANCHO_FROSTREACH_EXPLORACAO"
gancho = '''    # GANCHO_FROSTREACH_EXPLORACAO
    if opcao.get("modo") == "exploracao_frostreach":
        aplicar_efeitos(opcao.get("efeitos"), estado)
        from engine.frostreach_exploration import iniciar_exploracao_frostreach
        return iniciar_exploracao_frostreach(estado, opcao.get("bioma_inicial", "aleatorio"))

'''
if marca not in texto:
    if "    sucesso = True\n" not in texto:
        raise SystemExit("Cenas instaladas, mas não encontrei o ponto seguro de scene_engine.py. Veja INTEGRAR_MAIN.md.")
    shutil.copy2(motor, motor.with_suffix(".py.bak_frostreach"))
    motor.write_text(texto.replace("    sucesso = True\n", gancho + "    sucesso = True\n", 1), encoding="utf-8")

alterou = False
for candidato in (projeto / "data" / "regions.py", projeto / "data" / "regioes.py", projeto / "main.py"):
    if not candidato.is_file():
        continue
    dado = candidato.read_text(encoding="utf-8")
    padrao = r"(frostreach[\s\S]{0,600}?[\"']cena_inicial[\"']\s*:\s*)[\"'][^\"']+[\"']"
    novo, n = re.subn(padrao, r'\1"00_despertar_frostreach"', dado, count=1, flags=re.IGNORECASE)
    if n:
        shutil.copy2(candidato, candidato.with_suffix(candidato.suffix + ".bak_frostreach"))
        candidato.write_text(novo, encoding="utf-8")
        alterou = True
        break
print("Frostreach antigo arquivado e nova exploração instalada.")
print("Cena inicial atualizada automaticamente." if alterou else "Cena inicial não localizada automaticamente; veja INTEGRAR_MAIN.md.")

