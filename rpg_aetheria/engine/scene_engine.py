"""
scene_engine.py

O coração do jogo. Responsável por:
- Mostrar o texto e as opções de uma cena.
- Filtrar opções cujas condições não são atendidas (ex: precisa de um item
  ou flag que o jogador não tem).
- Aplicar os "efeitos" de uma escolha (ganhar flag, item, dano, reputação).
- Levar o jogador para a próxima cena.

Formato esperado de uma cena no JSON (ver data/scenes/ para exemplos):

{
  "id": "01_vila_eldor",
  "texto": "Texto descritivo da cena...",
  "opcoes": [
    {
      "texto": "Aceitar ajuda do Ancião",
      "condicao": {"nao_tem_flag": "recusou_anciao"},   // opcional
      "efeitos": [{"tipo": "flag", "valor": "em_divida"}], // opcional
      "destino": "02_aprendendo_basico"
    }
  ]
}
"""

from engine.game_state import GameState
from engine.condition_system import avaliar_condicao, encontrar_variacao_de_cena


def condicao_atendida(condicao, estado: GameState) -> bool:
    """Avalia se uma condição é satisfeita — usa o novo sistema."""
    return avaliar_condicao(condicao, estado)


def aplicar_efeitos(efeitos: list, estado: GameState) -> None:
    """Aplica a lista de efeitos de uma escolha ao estado do jogador."""
    if not efeitos:
        return

    for efeito in efeitos:
        tipo = efeito.get("tipo")

        if tipo == "flag":
            estado.adicionar_flag(efeito["valor"])
        elif tipo == "remover_flag":
            estado.remover_flag(efeito["valor"])
        elif tipo == "item":
            estado.adicionar_item(efeito["valor"])
        elif tipo == "dano":
            estado.vida = max(0, estado.vida - efeito["valor"])
        elif tipo == "cura":
            estado.vida = min(estado.vida_max, estado.vida + efeito["valor"])
        elif tipo == "reputacao":
            estado.alterar_reputacao(efeito["faccao"], efeito["valor"])
        else:
            print(f"[aviso] tipo de efeito desconhecido: {tipo}")


def opcoes_disponiveis(cena: dict, estado: GameState) -> list:
    """Retorna só as opções cuja condição é atendida pelo estado atual."""
    disponiveis = []
    for opcao in cena.get("opcoes", []):
        if condicao_atendida(opcao.get("condicao"), estado):
            disponiveis.append(opcao)
    return disponiveis


def executar_cena(cena: dict, estado: GameState) -> str:
    """
    Mostra a cena no terminal, pede escolha ao jogador, aplica efeitos
    e retorna o id da PRÓXIMA cena.
    
    Se a cena tem variações, seleciona a correta baseada nas flags do jogador.
    """
    # Encontra a variação correta da cena (se houver)
    cena = encontrar_variacao_de_cena(cena, estado)
    
    print("\n" + "=" * 60)
    print(cena["texto"])
    print("=" * 60)

    opcoes = opcoes_disponiveis(cena, estado)

    if not opcoes:
        # Cena sem opções = fim de jogo (ex: uma cena de final)
        return None

    for i, opcao in enumerate(opcoes, start=1):
        print(f"{i}. {opcao['texto']}")

    escolha = None
    while escolha is None:
        bruto = input("\n> Escolha uma opção: ").strip()
        if bruto.isdigit() and 1 <= int(bruto) <= len(opcoes):
            escolha = opcoes[int(bruto) - 1]
        else:
            print("Opção inválida, tente de novo.")

    aplicar_efeitos(escolha.get("efeitos"), estado)
    return escolha.get("destino")
