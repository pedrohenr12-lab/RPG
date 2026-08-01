"""
game_state.py

Guarda tudo que representa "quem é o jogador agora": atributos, flags de
história, inventário e relação com facções. É o objeto que passa entre
todas as cenas e o sistema de combate.
"""

from dataclasses import dataclass, field


@dataclass
class GameState:
    # Identidade
    nome: str = "Herói"
    raca: str = "humano"

    # Atributos de combate
    vida_max: int = 20
    vida: int = 20
    ataque: int = 4
    defesa: int = 2

    # Progresso narrativo
    cena_atual: str = "00_despertar"
    flags: set = field(default_factory=set)

    # Inventário simples: lista de nomes de itens
    inventario: list = field(default_factory=list)

    # Reputação com facções (0 a 100, começa neutro)
    reputacao: dict = field(default_factory=lambda: {
        "reino": 50,
        "rebeldes": 50,
        "vila_eldor": 50,
    })

    # ---- Métodos utilitários ----

    def tem_flag(self, nome: str) -> bool:
        return nome in self.flags

    def adicionar_flag(self, nome: str) -> None:
        self.flags.add(nome)

    def remover_flag(self, nome: str) -> None:
        self.flags.discard(nome)

    def tem_item(self, nome: str) -> bool:
        return nome in self.inventario

    def adicionar_item(self, nome: str) -> None:
        self.inventario.append(nome)

    def alterar_reputacao(self, faccao: str, valor: int) -> None:
        if faccao not in self.reputacao:
            self.reputacao[faccao] = 50
        self.reputacao[faccao] = max(0, min(100, self.reputacao[faccao] + valor))

    def esta_vivo(self) -> bool:
        return self.vida > 0

    def to_dict(self) -> dict:
        """Serializa o estado para salvar em JSON."""
        return {
            "nome": self.nome,
            "raca": self.raca,
            "vida_max": self.vida_max,
            "vida": self.vida,
            "ataque": self.ataque,
            "defesa": self.defesa,
            "cena_atual": self.cena_atual,
            "flags": list(self.flags),
            "inventario": self.inventario,
            "reputacao": self.reputacao,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GameState":
        """Reconstrói o estado a partir de um save JSON."""
        estado = cls(
            nome=data.get("nome", "Herói"),
            raca=data.get("raca", "humano"),
            vida_max=data.get("vida_max", 20),
            vida=data.get("vida", 20),
            ataque=data.get("ataque", 4),
            defesa=data.get("defesa", 2),
            cena_atual=data.get("cena_atual", "00_despertar"),
        )
        estado.flags = set(data.get("flags", []))
        estado.inventario = data.get("inventario", [])
        estado.reputacao = data.get("reputacao", {"reino": 50, "rebeldes": 50, "vila_eldor": 50})
        return estado
