"""Instala o pacote de cenas de Frostreach no projeto Aetheria.

Uso (a partir da pasta `rpg_aetheria/` ou da pasta que a contém):
    python frostreach-scenes/instalar_cenas_frostreach.py

Para apenas conferir o que será feito:
    python frostreach-scenes/instalar_cenas_frostreach.py --dry-run
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


# Os arquivos do pacote ficam na mesma pasta deste instalador.
PASTA_PACOTE = Path(__file__).resolve().parent
ARQUIVOS_DA_CENA = (
    "00_despertar_frostreach.json",
    "00b_frostreach_abrigo.json",
    "01_stonhelm_hub.json",
    "frostreach_expedicao.json",
)


def validar_json(caminho: Path) -> int:
    """Valida o JSON e retorna quantas cenas o arquivo contém."""
    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    cenas = dados if isinstance(dados, list) else [dados]
    for cena in cenas:
        if not isinstance(cena, dict) or "id" not in cena:
            raise ValueError(f"Cena inválida em {caminho.name}: falta o campo 'id'.")
    return len(cenas)


def instalar() -> None:
    projeto = Path.cwd()
    # Aceita os dois jeitos mais comuns de abrir o terminal:
    # 1. dentro de rpg_aetheria/; 2. uma pasta acima dela.
    if (projeto / "data" / "scenes").is_dir():
        pasta_cenas = projeto / "data" / "scenes"
    else:
        pasta_cenas = projeto / "rpg_aetheria" / "data" / "scenes"
    modo_simulacao = "--dry-run" in sys.argv

    if not pasta_cenas.is_dir():
        raise SystemExit(
            "Projeto não encontrado. Execute este comando dentro da pasta "
            "'rpg_aetheria' ou na pasta que a contém."
        )

    fontes = [PASTA_PACOTE / nome for nome in ARQUIVOS_DA_CENA]
    ausentes = [fonte.name for fonte in fontes if not fonte.is_file()]
    if ausentes:
        raise SystemExit(f"Arquivos do pacote ausentes: {', '.join(ausentes)}")

    total_cenas = sum(validar_json(fonte) for fonte in fontes)
    existentes = [pasta_cenas / fonte.name for fonte in fontes if (pasta_cenas / fonte.name).exists()]

    print(f"Projeto: {projeto}")
    print(f"Destino: {pasta_cenas}")
    print(f"Arquivos: {len(fontes)} | Cenas do pacote: {total_cenas}")

    if modo_simulacao:
        print("\nSimulação: nenhum arquivo foi alterado.")
        for fonte in fontes:
            acao = "substituir" if (pasta_cenas / fonte.name).exists() else "adicionar"
            print(f"- {acao}: {fonte.name}")
        return

    # Só três arquivos existentes são substituídos; preserve-os antes.
    if existentes:
        carimbo = datetime.now().strftime("%Y%m%d-%H%M%S")
        pasta_backup = pasta_cenas / f"backup_frostreach_{carimbo}"
        pasta_backup.mkdir()
        for destino in existentes:
            shutil.copy2(destino, pasta_backup / destino.name)
        print(f"Backup criado em: {pasta_backup.name}")

    for fonte in fontes:
        destino = pasta_cenas / fonte.name
        shutil.copy2(fonte, destino)
        print(f"OK: {destino.name}")

    print("\nInstalação concluída. Execute 'python main.py' dentro de rpg_aetheria para testar.")


if __name__ == "__main__":
    instalar()
