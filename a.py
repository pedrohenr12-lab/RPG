import os

print("Atualizando engine de combate (Etapa 1 - RPG de turnos)...")

os.makedirs("rpg_aetheria/engine", exist_ok=True)

arquivos = {}

# =========================================================
# GAME STATE ATUALIZADO
# =========================================================
arquivos["rpg_aetheria/engine/game_state.py"] = r'''"""
game_state.py - Atualizado para combate de turnos mais completo
"""
from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class GameState:
    # Identidade
    nome: str = "Herói"
    raca: str = "humano"
    classe_principal: str = "aventureiro_novato"

    # Atributos de combate
    vida_max: int = 20
    vida: int = 20
    mana_max: int = 10
    mana: int = 10
    ataque: int = 4
    defesa: int = 2
    velocidade: int = 5
    chance_critico: float = 0.10  # 10%

    # Progresso
    cena_atual: str = "00_despertar"
    flags: Set[str] = field(default_factory=set)
    inventario: List[str] = field(default_factory=list)
    classes_desbloqueadas: Set[str] = field(default_factory=set)

    # Status temporários (limpos após combate)
    status: Dict[str, int] = field(default_factory=dict)  # ex: {"veneno": 3}

    # NPCs e reputação
    npcs: Dict[str, str] = field(default_factory=lambda: {
        "garrick": "vivo",
        "anciao_eldor": "vivo",
    })
    reputacao: Dict[str, int] = field(default_factory=lambda: {
        "reino": 50, "rebeldes": 50, "vila_eldor": 50, "caravana": 50
    })

    # ---- Métodos ----
    def tem_flag(self, nome: str) -> bool:
        return nome in self.flags

    def adicionar_flag(self, nome: str) -> None:
        self.flags.add(nome)

    def tem_item(self, nome: str) -> bool:
        return nome in self.inventario

    def adicionar_item(self, nome: str) -> None:
        if nome not in self.inventario:
            self.inventario.append(nome)

    def gastar_mana(self, valor: int) -> bool:
        if self.mana >= valor:
            self.mana -= valor
            return True
        return False

    def curar(self, valor: int) -> None:
        self.vida = min(self.vida_max, self.vida + valor)

    def aplicar_status(self, nome: str, turnos: int) -> None:
        self.status[nome] = turnos

    def tick_status(self) -> List[str]:
        """Aplica efeitos de status e reduz duração. Retorna mensagens."""
        mensagens = []
        para_remover = []
        for st, turnos in self.status.items():
            if st == "veneno":
                dano = 2
                self.vida = max(0, self.vida - dano)
                mensagens.append(f"Veneno causa {dano} de dano!")
            elif st == "queimadura":
                dano = 3
                self.vida = max(0, self.vida - dano)
                mensagens.append(f"Queimadura causa {dano} de dano!")
            self.status[st] = turnos - 1
            if self.status[st] <= 0:
                para_remover.append(st)
                mensagens.append(f"Status '{st}' acabou.")
        for st in para_remover:
            del self.status[st]
        return mensagens

    def limpar_status(self) -> None:
        self.status.clear()

    def alterar_reputacao(self, faccao: str, valor: int) -> None:
        if faccao not in self.reputacao:
            self.reputacao[faccao] = 50
        self.reputacao[faccao] = max(0, min(100, self.reputacao[faccao] + valor))

    def esta_vivo(self) -> bool:
        return self.vida > 0

    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "raca": self.raca,
            "classe_principal": self.classe_principal,
            "vida_max": self.vida_max,
            "vida": self.vida,
            "mana_max": self.mana_max,
            "mana": self.mana,
            "ataque": self.ataque,
            "defesa": self.defesa,
            "velocidade": self.velocidade,
            "chance_critico": self.chance_critico,
            "cena_atual": self.cena_atual,
            "flags": list(self.flags),
            "inventario": self.inventario,
            "classes_desbloqueadas": list(self.classes_desbloqueadas),
            "reputacao": self.reputacao,
            "npcs": self.npcs,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GameState":
        estado = cls(
            nome=data.get("nome", "Herói"),
            raca=data.get("raca", "humano"),
            classe_principal=data.get("classe_principal", "aventureiro_novato"),
            vida_max=data.get("vida_max", 20),
            vida=data.get("vida", 20),
            mana_max=data.get("mana_max", 10),
            mana=data.get("mana", 10),
            ataque=data.get("ataque", 4),
            defesa=data.get("defesa", 2),
            velocidade=data.get("velocidade", 5),
            chance_critico=data.get("chance_critico", 0.10),
            cena_atual=data.get("cena_atual", "00_despertar"),
        )
        estado.flags = set(data.get("flags", []))
        estado.inventario = data.get("inventario", [])
        estado.classes_desbloqueadas = set(data.get("classes_desbloqueadas", []))
        estado.reputacao = data.get("reputacao", {"reino": 50, "rebeldes": 50, "vila_eldor": 50})
        estado.npcs = data.get("npcs", {})
        return estado
'''

# =========================================================
# COMBATE MELHORADO
# =========================================================
arquivos["rpg_aetheria/engine/combat.py"] = r'''"""
combat.py - Sistema de combate por turnos (Etapa 1)

- Habilidades básicas por raça
- Crítico
- Mana
- Status (veneno, queimadura, atordoado)
- IA simples do inimigo
- Loot básico
"""

import random
from engine.game_state import GameState


# Habilidades básicas por raça (custo de mana, efeito)
HABILIDADES_RACA = {
    "humano": {
        "nome": "Golpe Determinado",
        "custo_mana": 3,
        "descricao": "Ataque forte (+50% dano)",
        "tipo": "dano",
        "multiplicador": 1.5,
    },
    "elfo": {
        "nome": "Tiro Preciso",
        "custo_mana": 3,
        "descricao": "Ataque com alta chance de crítico",
        "tipo": "critico_garantido",
        "multiplicador": 1.2,
    },
    "anao": {
        "nome": "Pele de Pedra",
        "custo_mana": 4,
        "descricao": "Aumenta defesa neste turno e cura 3 de vida",
        "tipo": "buff_defesa",
        "cura": 3,
    },
    "orc": {
        "nome": "Fúria Selvagem",
        "custo_mana": 4,
        "descricao": "Ataque poderoso, mas você também toma 2 de dano",
        "tipo": "dano",
        "multiplicador": 2.0,
        "dano_proprio": 2,
    },
    "draconato": {
        "nome": "Sopro de Brasa",
        "custo_mana": 5,
        "descricao": "Dano de fogo + aplica Queimadura (2 turnos)",
        "tipo": "queimadura",
        "multiplicador": 1.3,
    },
}


def calcular_dano(atacante_atk: int, defensor_def: int, multiplicador: float = 1.0, critico: bool = False) -> int:
    base = max(1, int((atacante_atk - defensor_def * 0.5) * multiplicador))
    if critico:
        base = int(base * 1.8)
        print("💥 CRÍTICO!")
    return max(1, base)


def combate(estado: GameState, inimigo: dict) -> bool:
    """
    Combate por turnos.
    Retorna True se o jogador venceu (ou fugiu com sucesso),
    False se morreu.
    """
    vida_inimigo = inimigo["vida"]
    vida_max_inimigo = inimigo["vida"]
    nome_inimigo = inimigo["nome"]
    atk_inimigo = inimigo.get("ataque", 3)
    def_inimigo = inimigo.get("defesa", 1)
    tipo_ia = inimigo.get("ia", "agressivo")  # agressivo | defensivo | equilibrado

    status_inimigo = {}  # veneno, queimadura, atordoado
    defendendo = False
    buff_defesa = 0

    print("\n" + "=" * 50)
    print(f"⚔️  COMBATE: {nome_inimigo}")
    print("=" * 50)

    hab = HABILIDADES_RACA.get(estado.raca, HABILIDADES_RACA["humano"])

    while estado.esta_vivo() and vida_inimigo > 0:
        # --- Status do jogador ---
        for msg in estado.tick_status():
            print(f"  ⚠️  {msg}")
        if not estado.esta_vivo():
            break

        # --- Status do inimigo ---
        if "veneno" in status_inimigo:
            vida_inimigo = max(0, vida_inimigo - 2)
            print(f"  ☠️  {nome_inimigo} sofre 2 de dano de veneno!")
            status_inimigo["veneno"] -= 1
            if status_inimigo["veneno"] <= 0:
                del status_inimigo["veneno"]
        if "queimadura" in status_inimigo:
            vida_inimigo = max(0, vida_inimigo - 3)
            print(f"  🔥  {nome_inimigo} sofre 3 de dano de queimadura!")
            status_inimigo["queimadura"] -= 1
            if status_inimigo["queimadura"] <= 0:
                del status_inimigo["queimadura"]

        if vida_inimigo <= 0:
            break

        # --- HUD ---
        print(f"\n❤️  Você: {estado.vida}/{estado.vida_max}  |  💧 Mana: {estado.mana}/{estado.mana_max}")
        print(f"🐺 {nome_inimigo}: {vida_inimigo}/{vida_max_inimigo}")
        if estado.status:
            print(f"   Status: {', '.join(estado.status.keys())}")
        if status_inimigo:
            print(f"   Status inimigo: {', '.join(status_inimigo.keys())}")

        print("\n1. Atacar")
        print(f"2. Habilidade: {hab['nome']} (Mana: {hab['custo_mana']}) - {hab['descricao']}")
        print("3. Defender")
        print("4. Usar item")
        print("5. Fugir")

        acao = input("> Escolha: ").strip()
        defendendo = False
        buff_defesa = 0
        atordoado_inimigo = "atordoado" in status_inimigo

        # ===== AÇÕES DO JOGADOR =====
        if acao == "1":  # Atacar
            critico = random.random() < estado.chance_critico
            dano = calcular_dano(estado.ataque, def_inimigo, 1.0, critico)
            vida_inimigo -= dano
            print(f"Você atacou e causou {dano} de dano!")

        elif acao == "2":  # Habilidade racial
            if not estado.gastar_mana(hab["custo_mana"]):
                print("Mana insuficiente!")
                continue

            tipo = hab["tipo"]
            multi = hab.get("multiplicador", 1.0)

            if tipo == "dano":
                critico = random.random() < estado.chance_critico
                dano = calcular_dano(estado.ataque, def_inimigo, multi, critico)
                vida_inimigo -= dano
                print(f"Você usou {hab['nome']} e causou {dano} de dano!")
                if "dano_proprio" in hab:
                    estado.vida = max(0, estado.vida - hab["dano_proprio"])
                    print(f"Você sofreu {hab['dano_proprio']} de dano pela fúria!")

            elif tipo == "critico_garantido":
                dano = calcular_dano(estado.ataque, def_inimigo, multi, critico=True)
                vida_inimigo -= dano
                print(f"Você usou {hab['nome']} e causou {dano} de dano!")

            elif tipo == "buff_defesa":
                buff_defesa = 4
                estado.curar(hab.get("cura", 0))
                print(f"Você usou {hab['nome']}! Defesa aumentada e curou {hab.get('cura', 0)} de vida.")

            elif tipo == "queimadura":
                dano = calcular_dano(estado.ataque, def_inimigo, multi, False)
                vida_inimigo -= dano
                status_inimigo["queimadura"] = 2
                print(f"Você usou {hab['nome']}! {dano} de dano + Queimadura aplicada!")

        elif acao == "3":  # Defender
            defendendo = True
            print("Você se prepara para defender. (dano reduzido pela metade)")

        elif acao == "4":  # Item
            pocoes = [i for i in estado.inventario if "Poção" in i or "poção" in i.lower()]
            if not pocoes:
                print("Você não tem itens utilizáveis.")
                continue
            print("Itens disponíveis:")
            for idx, item in enumerate(pocoes, 1):
                print(f"  {idx}. {item}")
            escolha_item = input("> Qual item? ").strip()
            if escolha_item.isdigit() and 1 <= int(escolha_item) <= len(pocoes):
                item = pocoes[int(escolha_item) - 1]
                estado.inventario.remove(item)
                if "Cura" in item or "cura" in item.lower():
                    estado.curar(10)
                    print(f"Você usou {item} e recuperou 10 de vida.")
                elif "Mana" in item:
                    estado.mana = min(estado.mana_max, estado.mana + 8)
                    print(f"Você usou {item} e recuperou 8 de mana.")
                else:
                    estado.curar(6)
                    print(f"Você usou {item}.")
            else:
                print("Escolha inválida.")
                continue

        elif acao == "5":  # Fugir
            chance = 0.45 + (estado.velocidade * 0.03)
            if random.random() < chance:
                print("Você conseguiu fugir!")
                estado.limpar_status()
                return True
            else:
                print("Falha na fuga!")
        else:
            print("Ação inválida.")
            continue

        # ===== TURNO DO INIMIGO =====
        if vida_inimigo <= 0:
            break

        if atordoado_inimigo:
            print(f"{nome_inimigo} está atordoado e não age!")
            del status_inimigo["atordoado"]
            continue

        # IA simples
        if tipo_ia == "defensivo" and vida_inimigo < vida_max_inimigo * 0.4:
            print(f"{nome_inimigo} se defende!")
            def_inimigo += 2  # temporário (simplificado)
        else:
            defesa_jogador = estado.defesa + buff_defesa
            dano_inimigo = calcular_dano(atk_inimigo, defesa_jogador, 1.0, False)
            if defendendo:
                dano_inimigo = max(1, dano_inimigo // 2)
                print("(Dano reduzido pela defesa)")
            estado.vida = max(0, estado.vida - dano_inimigo)
            print(f"{nome_inimigo} atacou! Você sofreu {dano_inimigo} de dano.")

            # Chance de aplicar veneno (inimigos específicos)
            if inimigo.get("aplica_veneno") and random.random() < 0.3:
                estado.aplicar_status("veneno", 3)
                print("Você foi envenenado!")

    # ===== RESULTADO =====
    estado.limpar_status()

    if estado.esta_vivo():
        print(f"\n✅ Você derrotou {nome_inimigo}!")
        # Loot básico
        loot = inimigo.get("loot", [])
        for item in loot:
            estado.adicionar_item(item)
            print(f"  📦 Você encontrou: {item}")
        if not loot and random.random() < 0.4:
            estado.adicionar_item("Poção de Cura")
            print("  📦 Você encontrou: Poção de Cura")
        # Pequena recuperação de mana
        estado.mana = min(estado.mana_max, estado.mana + 3)
        return True
    else:
        print(f"\n💀 Você foi derrotado por {nome_inimigo}...")
        return False
'''

for caminho, conteudo in arquivos.items():
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)

print("✅ Engine de combate atualizado!")
print("Novidades:")
print(" - Mana + habilidades básicas por raça")
print(" - Crítico")
print(" - Status (veneno, queimadura)")
print(" - IA simples do inimigo")
print(" - Loot ao vencer")
print(" - Melhor feedback visual")
print("\nRode o jogo e teste um combate para ver a diferença.")