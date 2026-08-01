"""
combat.py

Sistema de combate por turnos, simples de propósito. O jogador escolhe
uma ação a cada turno; o inimigo responde com uma ação própria (por
enquanto, sempre ataca — dá pra sofisticar depois com uma "IA" real).

Formato esperado de um inimigo (normalmente definido dentro do JSON da
cena que dispara o combate):

{
  "nome": "Lobo Faminto",
  "vida": 12,
  "ataque": 3,
  "defesa": 1
}
"""

from engine.game_state import GameState


def combate(estado: GameState, inimigo: dict) -> bool:
    """
    Executa um combate por turnos. Retorna True se o jogador venceu,
    False se o jogador morreu.
    """
    vida_inimigo = inimigo["vida"]
    nome_inimigo = inimigo["nome"]
    defendendo = False

    print(f"\n⚔️  Um {nome_inimigo} aparece! Vida: {vida_inimigo}")

    while estado.esta_vivo() and vida_inimigo > 0:
        print(f"\nSua vida: {estado.vida}/{estado.vida_max}  |  {nome_inimigo}: {vida_inimigo}")
        print("1. Atacar")
        print("2. Defender (reduz o próximo dano recebido pela metade)")
        print("3. Usar item")
        print("4. Fugir")

        acao = input("> Escolha uma ação: ").strip()
        defendendo = False

        if acao == "1":
            dano = max(1, estado.ataque - inimigo.get("defesa", 0))
            vida_inimigo -= dano
            print(f"Você causou {dano} de dano.")

        elif acao == "2":
            defendendo = True
            print("Você se prepara para defender.")

        elif acao == "3":
            if "Poção de Cura" in estado.inventario:
                estado.inventario.remove("Poção de Cura")
                estado.vida = min(estado.vida_max, estado.vida + 8)
                print("Você usou uma Poção de Cura e recuperou 8 de vida.")
            else:
                print("Você não tem itens utilizáveis agora.")
                continue

        elif acao == "4":
            chance_fuga = 0.5
            import random
            if random.random() < chance_fuga:
                print("Você conseguiu fugir!")
                return True  # trata fuga como "sobreviveu", sem loot
            else:
                print("Você tentou fugir, mas não conseguiu!")

        else:
            print("Ação inválida.")
            continue

        # Turno do inimigo, se ainda estiver vivo
        if vida_inimigo > 0:
            dano_inimigo = max(1, inimigo.get("ataque", 3) - estado.defesa)
            if defendendo:
                dano_inimigo = dano_inimigo // 2
            estado.vida = max(0, estado.vida - dano_inimigo)
            print(f"{nome_inimigo} atacou! Você sofreu {dano_inimigo} de dano.")

    if estado.esta_vivo():
        print(f"\nVocê derrotou {nome_inimigo}!")
        return True
    else:
        print(f"\nVocê foi derrotado por {nome_inimigo}...")
        return False

