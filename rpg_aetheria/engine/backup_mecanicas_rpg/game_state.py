"""
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
