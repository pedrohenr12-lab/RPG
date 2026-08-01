"""Rolagens e passagem de tempo para Aetheria."""
import random

def rolar_teste(estado, teste):
    atributo = teste.get("atributo", "sobrevivencia")
    dificuldade = int(teste.get("dificuldade", 10))
    dado = random.randint(1, 20)
    bonus = int(estado.atributos.get(atributo, 0))
    total = dado + bonus
    critico = dado == 20
    falha_critica = dado == 1
    sucesso = critico or (not falha_critica and total >= dificuldade)
    print(f"\n🎲 {teste.get('nome', atributo.title())}: d20 ({dado}) + {bonus} = {total} | dificuldade {dificuldade}")
    print("✓ Sucesso!" if sucesso else "✗ Falha.")
    return sucesso

def passar_tempo(estado, horas):
    estado.hora += horas
    while estado.hora >= 24:
        estado.hora -= 24
        estado.dia += 1
    estado.energia = max(0, estado.energia - max(1, horas * 2))
    estado.fome = min(100, estado.fome + horas * 2)
    estado.sede = min(100, estado.sede + horas * 3)
    if estado.fome >= 85 or estado.sede >= 85:
        estado.vida = max(0, estado.vida - 1)

def mostrar_status(estado):
    periodo = "manhã" if 6 <= estado.hora < 12 else "tarde" if 12 <= estado.hora < 18 else "noite"
    print(f"\n[DIA {estado.dia} — {estado.hora:02d}:00, {periodo}] "
          f"Vida {estado.vida}/{estado.vida_max} | Energia {estado.energia}/100 | "
          f"Fome {estado.fome}/100 | Sede {estado.sede}/100 | Temperatura {estado.temperatura}")
