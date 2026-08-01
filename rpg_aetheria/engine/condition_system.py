"""
condition_system.py

Sistema que avalia condições complexas em cenas.
Permite: "tem_flag AND tem_item", "tem_flag OR não_tem_flag", etc.

Formato de condição no JSON:
  "condicao": {
    "tipo": "AND",  # AND, OR, NOT
    "items": [
      {"tipo": "tem_flag", "valor": "ajudou_garrick"},
      {"tipo": "tem_item", "valor": "Amuleto"}
    ]
  }

Ou simples:
  "condicao": {"tem_flag": "ajudou_garrick"}
"""

from engine.game_state import GameState


def avaliar_condicao(condicao, estado: GameState) -> bool:
    """
    Avalia uma condição simples ou complexa contra o estado do jogador.
    Retorna True se a condição é atendida.
    
    Formatos suportados:
    - {"tem_flag": "nome"}
    - {"tipo": "tem_flag", "valor": "nome"}  <- convertido pro anterior
    - {"tipo": "AND", "items": [...]}
    """
    if condicao is None:
        return True

    # Se tem "tipo" e "valor" (formato normalizado de item simples),
    # converte pra formato direto
    if "tipo" in condicao and "valor" in condicao and "items" not in condicao:
        tipo_op = condicao["tipo"]
        valor = condicao["valor"]
        
        # Reconstrói como condição simples
        nova_condicao = {tipo_op: valor}
        return avaliar_condicao(nova_condicao, estado)

    # Condições compostas (AND, OR, NOT)
    if "tipo" in condicao and "items" in condicao:
        tipo = condicao["tipo"]
        items = condicao.get("items", [])

        if tipo == "AND":
            return all(avaliar_condicao(item, estado) for item in items)
        elif tipo == "OR":
            return any(avaliar_condicao(item, estado) for item in items)
        elif tipo == "NOT":
            if items:
                return not avaliar_condicao(items[0], estado)
            return True
    
    # Condições simples
    if "tem_flag" in condicao and not estado.tem_flag(condicao["tem_flag"]):
        return False
    if "nao_tem_flag" in condicao and estado.tem_flag(condicao["nao_tem_flag"]):
        return False
    if "tem_item" in condicao and not estado.tem_item(condicao["tem_item"]):
        return False
    if "nao_tem_item" in condicao and estado.tem_item(condicao["nao_tem_item"]):
        return False
    if "raca" in condicao and estado.raca != condicao["raca"]:
        return False
    if "npc_vivo" in condicao:
        npc = condicao["npc_vivo"]
        if npc not in estado.npcs or estado.npcs[npc] != "vivo":
            return False
    if "npc_morto" in condicao:
        npc = condicao["npc_morto"]
        if npc not in estado.npcs or estado.npcs[npc] != "morto":
            return False
    if "reputacao_minima" in condicao:
        req = condicao["reputacao_minima"]
        faccao = req["faccao"]
        minimo = req["valor"]
        if estado.reputacao.get(faccao, 0) < minimo:
            return False
    if "reputacao_maxima" in condicao:
        req = condicao["reputacao_maxima"]
        faccao = req["faccao"]
        maximo = req["valor"]
        if estado.reputacao.get(faccao, 0) > maximo:
            return False

    return True


def encontrar_variacao_de_cena(cena: dict, estado: GameState) -> dict:
    """
    Se uma cena tem múltiplas "variações" (cada uma com condições de entrada),
    retorna a variação que o jogador atende, ou a padrão.
    
    Formato:
    {
      "id": "cena_importante",
      "variações": [
        {
          "condicao": {...},
          "texto": "versão se ajudou",
          "opcoes": [...]
        },
        {
          "condicao": {...},
          "texto": "versão se roubou",
          "opcoes": [...]
        },
        {
          "condicao": null,  # padrão, sempre válida
          "texto": "versão padrão",
          "opcoes": [...]
        }
      ]
    }
    """
    if "variações" not in cena:
        # Cena normal, sem variações
        return cena
    
    # Procura a primeira variação que o jogador atende
    for variacao in cena["variações"]:
        if avaliar_condicao(variacao.get("condicao"), estado):
            # Retorna uma cópia da cena, substituindo texto e opções
            cena_resultado = dict(cena)
            cena_resultado["texto"] = variacao.get("texto", cena.get("texto", ""))
            cena_resultado["opcoes"] = variacao.get("opcoes", cena.get("opcoes", []))
            # Remove "variações" da cena resultante
            cena_resultado.pop("variações", None)
            return cena_resultado
    
    # Fallback: retorna a cena normal
    return cena
