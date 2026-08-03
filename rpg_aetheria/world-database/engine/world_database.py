"""Banco narrativo JSON: descoberta e encontros coerentes por bioma."""
import json
import random
from pathlib import Path

def carregar_eldorwood(raiz_projeto: str | Path) -> dict:
    caminho = Path(raiz_projeto) / "data" / "world" / "eldorwood.json"
    with caminho.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)

def registrar_descoberta(estado, categoria: str, identificador: str, titulo: str) -> bool:
    chave = f"{categoria}:{identificador}"
    if chave in estado.descobertas:
        return False
    estado.descobertas[chave] = {"titulo": titulo, "categoria": categoria}
    estado.diario.append(f"Descoberta — {titulo}")
    return True

def sortear_encontro(mundo: dict, bioma_id: str, tipo: str | None = None) -> dict | None:
    bioma = mundo["biomas"].get(bioma_id)
    if not bioma:
        return None
    ids = bioma["encontros"].get(tipo, []) if tipo else sum(bioma["encontros"].values(), [])
    opcoes = [mundo["criaturas"][id_] for id_ in ids if id_ in mundo["criaturas"]]
    return random.choice(opcoes) if opcoes else None
