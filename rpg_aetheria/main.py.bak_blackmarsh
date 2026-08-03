"""
main.py
Ponto de entrada do jogo — compatível com o combate atualizado (Etapa 1).
"""

import os
import random

from engine.game_state import GameState
from engine.scene_loader import carregar_cenas
from engine.scene_engine import executar_cena
from engine.combat import combate
from engine.race_loader import carregar_racas

PASTA_CENAS = os.path.join(os.path.dirname(__file__), "data", "scenes")
ARQUIVO_RACAS = os.path.join(os.path.dirname(__file__), "data", "characters", "races.json")
ARQUIVO_INTRO_MUNDO = os.path.join(os.path.dirname(__file__), "data", "lore", "intro_mundo.txt")

REGIOES = {
    "frostreach": {
        "nome_exibicao": "Frostreach, as Terras do Gelo Eterno",
        "cena_inicial": "00_despertar_frostreach",
    },
    "eldorwood": {
        "nome_exibicao": "Eldorwood, o Coração Verde das Florestas",
        "cena_inicial": "00_despertar",
    },
    "arkanor": {
        "nome_exibicao": "Arkanor, as Terras Douradas",
        "cena_inicial": "00_despertar_arkanor",
    },
    "stonevale": {
        "nome_exibicao": "Stonevale, os Planaltos e Colinas Quebradas",
        "cena_inicial": "00_despertar_stonevale",
    },
    "blackmarsh": {
        "nome_exibicao": "Blackmarsh, os Pântanos Negros",
        "cena_inicial": "00_despertar_blackmarsh",
    },
    "espinha_do_mundo": {
        "nome_exibicao": "A Espinha do Mundo",
        "cena_inicial": "00_despertar_espinha",
    },
}


def sortear_regiao_inicial(estado: GameState) -> None:
    chave_regiao = random.choice(list(REGIOES.keys()))
    dados_regiao = REGIOES[chave_regiao]
    estado.cena_atual = dados_regiao["cena_inicial"]
    estado.adicionar_flag(f"spawn_{chave_regiao}")
    print("\n" + "-" * 60)
    print(f"O destino te jogou em: {dados_regiao['nome_exibicao']}")
    print("-" * 60)


def processar_cena_de_combate(cena: dict, estado: GameState) -> str:
    print("\n" + "=" * 60)
    print(cena["texto"])
    print("=" * 60)
    info_combate = cena["combate"]
    venceu = combate(estado, info_combate["inimigo"])
    if venceu:
        return info_combate["destino_vitoria"]
    else:
        return info_combate["destino_derrota"]


def mostrar_intro_mundo(caminho_arquivo: str) -> None:
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        texto = f.read()
    print("\n" + "=" * 60)
    print("  O MUNDO DE AETHERIA")
    print("=" * 60)
    print(texto)
    input("\n(pressione Enter para continuar)")


def escolher_raca(racas: dict) -> str:
    ids_racas = list(racas.keys())
    print("\nEscolha sua raça:")
    for i, id_raca in enumerate(ids_racas, start=1):
        dados = racas[id_raca]
        vida = dados.get("vida_max", 20)
        atk = dados.get("ataque", 4)
        def_ = dados.get("defesa", 2)
        mana = dados.get("mana_max", 10)
        print(f"\n{i}. {dados['nome_exibicao']}")
        print(f"   {dados['descricao']}")
        print(f"   (Vida: {vida} | Ataque: {atk} | Defesa: {def_} | Mana: {mana})")
    escolha = None
    while escolha is None:
        bruto = input("\n> Escolha uma raça: ").strip()
        if bruto.isdigit() and 1 <= int(bruto) <= len(ids_racas):
            escolha = ids_racas[int(bruto) - 1]
        else:
            print("Opção inválida, tente de novo.")
    return escolha


def criar_personagem(racas: dict) -> GameState:
    nome = input("\nComo se chama o seu personagem? ").strip() or "Herói"
    id_raca = escolher_raca(racas)
    dados = racas[id_raca]

    estado = GameState(
        nome=nome,
        raca=id_raca,
        vida_max=dados.get("vida_max", 20),
        vida=dados.get("vida_max", 20),
        mana_max=dados.get("mana_max", 10),
        mana=dados.get("mana_max", 10),
        ataque=dados.get("ataque", 4),
        defesa=dados.get("defesa", 2),
        velocidade=dados.get("velocidade", 5),
        chance_critico=dados.get("chance_critico", 0.10),
    )
    estado.adicionar_flag(dados["flag_racial"])

    print("\n" + "-" * 60)
    print(dados["texto_criacao"])
    print("-" * 60)
    return estado


def main():
    print("=" * 60)
    print("  AETHERIA — RPG de Turnos")
    print("=" * 60)

    racas = carregar_racas(ARQUIVO_RACAS)
    mostrar_intro_mundo(ARQUIVO_INTRO_MUNDO)
    estado = criar_personagem(racas)
    sortear_regiao_inicial(estado)
    cenas = carregar_cenas(PASTA_CENAS)

    cena_id = estado.cena_atual

    while cena_id is not None:
        if cena_id not in cenas:
            print(f"\n[erro] Cena '{cena_id}' não encontrada. Encerrando.")
            break

        cena = cenas[cena_id]
        estado.cena_atual = cena_id

        if "combate" in cena:
            cena_id = processar_cena_de_combate(cena, estado)
        else:
            cena_id = executar_cena(cena, estado)

        if not estado.esta_vivo():
            print("\nVocê não sobreviveu à jornada...")
            break

    print("\nObrigado por jogar!")
    print(f"Flags acumuladas: {sorted(estado.flags)}")
    print(f"Itens: {estado.inventario}")


if __name__ == "__main__":
    main()