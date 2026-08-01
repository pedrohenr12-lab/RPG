"""
scene_loader.py

Lê todos os arquivos .json da pasta data/scenes e monta um dicionário
{id_da_cena: dados_da_cena}. O motor (scene_engine.py) só trabalha com
esse dicionário — nunca sabe nem se importa que os dados vieram de
arquivos separados.

Isso é o que permite adicionar conteúdo novo sem tocar no código: basta
criar mais um arquivo .json na pasta de cenas.
"""

import json
import os


def carregar_cenas(pasta_cenas: str) -> dict:
    cenas = {}
    for nome_arquivo in os.listdir(pasta_cenas):
        if not nome_arquivo.endswith(".json"):
            continue
        caminho = os.path.join(pasta_cenas, nome_arquivo)
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # Cada arquivo pode ter UMA cena ou uma LISTA de cenas
        if isinstance(dados, list):
            for cena in dados:
                cenas[cena["id"]] = cena
        else:
            cenas[dados["id"]] = dados

    return cenas
