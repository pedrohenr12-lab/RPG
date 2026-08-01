"""
race_loader.py

Lê data/characters/races.json e devolve um dicionário
{id_da_raca: dados_da_raca}. Mesma filosofia do scene_loader: o motor
não sabe nada sobre quais raças existem, só sabe ler o formato.
"""

import json


def carregar_racas(caminho_arquivo: str) -> dict:
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return json.load(f)
