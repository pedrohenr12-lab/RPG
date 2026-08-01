"""
main.py

Ponto de entrada do jogo. Carrega as cenas, cria o estado inicial do
jogador e roda o laço principal: mostra a cena atual, processa a
escolha (ou o combate, se a cena tiver um), e vai para a próxima cena
— até chegar numa cena sem opções (um final).
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

# Cada região aponta pra sua própria cena de despertar. O spawn é
# sorteado entre elas — o jogador não escolhe onde cai nesse mundo.
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
    """Sorteia em qual região o personagem desperta e ajusta o estado."""
    chave_regiao = random.choice(list(REGIOES.keys()))
    dados_regiao = REGIOES[chave_regiao]

    estado.cena_atual = dados_regiao["cena_inicial"]
    estado.adicionar_flag(f"spawn_{chave_regiao}")

    print("\n" + "-" * 60)
    print(f"O destino te jogou em: {dados_regiao['nome_exibicao']}")
    print("-" * 60)


def processar_cena_de_combate(cena: dict, estado: GameState) -> str:
    """Roda o combate definido numa cena e decide a próxima cena pelo resultado."""
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
    """Mostra o texto de contexto do mundo antes da criação do personagem."""
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        texto = f.read()

    print("\n" + "=" * 60)
    print("  O MUNDO DE AETHERIA")
    print("=" * 60)
    print(texto)
    input("\n(pressione Enter para continuar)")


def escolher_raca(racas: dict) -> str:
    """Mostra as raças disponíveis e devolve o id da raça escolhida."""
    ids_racas = list(racas.keys())

    print("\nEscolha sua raça:")
    for i, id_raca in enumerate(ids_racas, start=1):
        dados = racas[id_raca]
        print(f"\n{i}. {dados['nome_exibicao']}")
        print(f"   {dados['descricao']}")
        print(f"   (Vida: {dados['vida_max']} | Ataque: {dados['ataque']} | Defesa: {dados['defesa']})")

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
    dados_raca = racas[id_raca]

    estado = GameState(
        nome=nome,
        raca=id_raca,
        vida_max=dados_raca["vida_max"],
        vida=dados_raca["vida_max"],
        ataque=dados_raca["ataque"],
        defesa=dados_raca["defesa"],
    )
    estado.adicionar_flag(dados_raca["flag_racial"])

    print("\n" + "-" * 60)
    print(dados_raca["texto_criacao"])
    print("-" * 60)

    return estado


def main():
    print("=" * 60)
    print("  AETHERIA — Demo do Motor de RPG")
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

    print("\nObrigado por jogar essa demo!")
    print(f"Flags acumuladas: {sorted(estado.flags)}")
    print(f"Itens: {estado.inventario}")


if __name__ == "__main__":
    main()
