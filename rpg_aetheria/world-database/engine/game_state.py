from dataclasses import dataclass, field

@dataclass
class GameState:
    nome: str = "Herói"; raca: str = "humano"
    vida_max: int = 20; vida: int = 20
    mana_max: int = 10; mana: int = 10
    velocidade: int = 5; chance_critico: float = 0.10
    ataque: int = 4; defesa: int = 2; cena_atual: str = "00_despertar"
    flags: set = field(default_factory=set); inventario: list = field(default_factory=list)
    reputacao: dict = field(default_factory=lambda: {"reino": 50, "rebeldes": 50, "vila_eldor": 50})
    atributos: dict = field(default_factory=lambda: {"sobrevivencia": 0, "percepcao": 0, "forca": 0, "agilidade": 0, "vontade": 0, "social": 0})
    energia: int = 100; fome: int = 15; sede: int = 15; temperatura: int = 0
    dia: int = 1; hora: int = 8; xp: int = 0
    descobertas: dict = field(default_factory=dict)
    diario: list = field(default_factory=list)
    regioes_descobertas: set = field(default_factory=set)
    biomas_descobertos: set = field(default_factory=set)
    def tem_flag(self, nome): return nome in self.flags
    def adicionar_flag(self, nome): self.flags.add(nome)
    def remover_flag(self, nome): self.flags.discard(nome)
    def tem_item(self, nome): return nome in self.inventario
    def adicionar_item(self, nome): self.inventario.append(nome)
    def alterar_reputacao(self, faccao, valor): self.reputacao[faccao] = max(0, min(100, self.reputacao.get(faccao, 50) + valor))
    def esta_vivo(self): return self.vida > 0
    def to_dict(self):
        d = self.__dict__.copy()
        for chave in ("flags", "regioes_descobertas", "biomas_descobertos"): d[chave] = list(d[chave])
        return d
    @classmethod
    def from_dict(cls, dados):
        estado = cls()
        for chave, valor in dados.items(): setattr(estado, chave, set(valor) if chave in {"flags", "regioes_descobertas", "biomas_descobertos"} else valor)
        return estado
