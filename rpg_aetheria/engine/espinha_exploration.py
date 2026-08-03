"""Exploração livre e sobrevivência para A Espinha do Mundo.

Este módulo não depende do banco MySQL durante a partida. Ele usa o GameState
existente, preserva flags/inventário e pode ser expandido para consultar o banco
mais tarde.
"""
from __future__ import annotations

import random


BIOMES = {
    "cordilheira_monumental": {
        "nome": "Cordilheira Monumental",
        "perigo": 5,
        "temperatura": (-25, -5),
        "locais": ["Pico dos Ventos", "Fortaleza Anã Abandonada", "Câmara de Pressium"],
        "visoes": [
            "Picos de rocha e neve rasgam o teto de nuvens. A gravidade mais fraca permite agulhas de pedra impossivelmente altas.",
            "Uma muralha de gelo azul devolve a luz em ângulos quebrados; sob ela, a sombra parece mais profunda que deveria.",
        ],
        "sons": ["o vento assobia por fendas estreitas", "pedras se deslocam muito acima", "um grito de águia desaparece entre os picos"],
        "odores": ["ferro frio e neve", "poeira mineral recém-exposta", "fumaça velha, trazida de uma rota distante"],
        "flora": ["Líquen-de-Pico", "Flor-de-Neve Eterna", "Fungo-de-Pressium", "Arbusto-Anão de Montanha"],
        "hostis": [("Urso-de-Montanha", 22, 6, 3, 4), ("Lobo-de-Altitude", 15, 5, 2, 3), ("Guardião de Pressium", 30, 8, 5, 5)],
        "raros": [("Dragão-de-Pedra Ancião", 45, 11, 7, 5), ("Espírito-do-Vento", 18, 6, 4, 4)],
    },
    "vales_profundos": {
        "nome": "Vales Profundos entre Picos",
        "perigo": 4,
        "temperatura": (-10, 8),
        "locais": ["Vale das Sombras", "Entrada dos Ecos", "Veio de Vynium"],
        "visoes": [
            "As paredes do vale escondem o sol cedo demais. Pequenos rios somem sob pedras e reaparecem como fios prateados.",
            "Há marcas de cascos na neve rala e arranhões na rocha; você não sabe qual animal deixou cada sinal.",
        ],
        "sons": ["um eco responde tarde demais", "água corre debaixo de pedras", "um corvo imita uma voz humana ao longe"],
        "odores": ["musgo úmido e cobre", "terra fria", "resina antiga vinda de arbustos baixos"],
        "flora": ["Flor-de-Cristal", "Líquen-de-Eco", "Arbusto-de-Cobre", "Samambaia-de-Vale"],
        "hostis": [("Serpente-de-Rocha", 14, 4, 2, 2), ("Sombra-dos-Vales", 24, 7, 4, 5), ("Guardião de Vynium", 28, 8, 5, 5)],
        "raros": [("Eco-Vivo dos Vales", 20, 6, 3, 4), ("Predador Sombrio", 25, 8, 4, 5)],
    },
    "cavernas_gigantes": {
        "nome": "Cavernas Gigantes",
        "perigo": 5,
        "temperatura": (3, 7),
        "locais": ["Cidade Anã Soterrada", "Câmara de Luminite", "Lago sem Luz"],
        "visoes": [
            "Cristais de Luminite iluminam a caverna sem chama. As sombras não acompanham perfeitamente seus passos.",
            "Colunas de pedra desaparecem no escuro. Fios de seda brilhante cruzam uma passagem baixa.",
        ],
        "sons": ["gotas caem em intervalos quase musicais", "asas batem muito longe", "um rangido mineral percorre a parede"],
        "odores": ["pedra molhada e fungo", "água estagnada", "ar metálico vindo de uma fenda"],
        "flora": ["Fungo-Luminoso", "Flor-de-Luminite", "Líquen-de-Harmonix", "Raiz-Cega"],
        "hostis": [("Aranha-de-Cristal", 16, 5, 2, 3), ("Morcego-Gigante de Caverna", 17, 5, 1, 2), ("Sombra-Vorath", 27, 8, 4, 5)],
        "raros": [("Guardião de Luminite", 30, 9, 5, 5), ("Dragão-de-Caverna", 42, 11, 7, 5), ("Eco-Ancião", 22, 7, 4, 5)],
    },
}

TRANSICOES = {
    "cordilheira_monumental": {"norte": "cordilheira_monumental", "sul": "vales_profundos", "leste": "vales_profundos", "oeste": "cordilheira_monumental"},
    "vales_profundos": {"norte": "cordilheira_monumental", "sul": "vales_profundos", "leste": "cavernas_gigantes", "oeste": "vales_profundos"},
    "cavernas_gigantes": {"norte": "vales_profundos", "sul": "cavernas_gigantes", "leste": "cavernas_gigantes", "oeste": "cavernas_gigantes"},
}


def _get(estado, nome, padrao):
    if not hasattr(estado, nome):
        setattr(estado, nome, padrao)
    return getattr(estado, nome)


def _flag(estado, nome):
    if hasattr(estado, "adicionar_flag"):
        estado.adicionar_flag(nome)
    else:
        _get(estado, "flags", set()).add(nome)


def _tem_flag(estado, nome):
    return estado.tem_flag(nome) if hasattr(estado, "tem_flag") else nome in _get(estado, "flags", set())


def _item(estado, nome):
    if hasattr(estado, "adicionar_item"):
        estado.adicionar_item(nome)
    else:
        _get(estado, "inventario", []).append(nome)


def _rolar(estado, atributo, dificuldade, nome):
    dado = random.randint(1, 20)
    bonus = int(_get(estado, "atributos", {}).get(atributo, 0))
    total = dado + bonus
    sucesso = dado == 20 or (dado != 1 and total >= dificuldade)
    print(f"\n🎲 {nome}: d20 ({dado}) + {bonus} = {total} | dificuldade {dificuldade}")
    print("✓ Sucesso." if sucesso else "✗ Falha.")
    return sucesso


def _avancar(estado, horas, frio=0):
    """Avança tempo sem depender de uma versão específica de rpg_systems.py."""
    _get(estado, "hora", 8)
    _get(estado, "dia", 1)
    _get(estado, "energia", 100)
    _get(estado, "fome", 15)
    _get(estado, "sede", 15)
    estado.hora += horas
    while estado.hora >= 24:
        estado.hora -= 24
        estado.dia += 1
    estado.energia = max(0, estado.energia - max(1, horas * 3))
    estado.fome = min(100, estado.fome + horas * 2)
    estado.sede = min(100, estado.sede + horas * 3)
    estado.exposicao_frio = max(0, _get(estado, "exposicao_frio", 0) + frio)
    if estado.fome >= 85 or estado.sede >= 85:
        estado.vida = max(0, estado.vida - 1)
        print("A fome ou a sede já estão prejudicando sua vida.")
    if estado.exposicao_frio >= 70:
        estado.vida = max(0, estado.vida - 2)
        estado.energia = max(0, estado.energia - 5)
        print("O frio atravessa suas roupas. Você perde 2 de vida.")


def _periodo(estado):
    hora = _get(estado, "hora", 8)
    return "manhã" if 6 <= hora < 12 else "tarde" if 12 <= hora < 18 else "noite"


def _status(estado):
    print(f"\n[DIA {estado.dia} — {estado.hora:02d}:00, {_periodo(estado)}] "
          f"Vida {estado.vida}/{estado.vida_max} | Energia {estado.energia}/100 | "
          f"Fome {estado.fome}/100 | Sede {estado.sede}/100 | Frio {estado.exposicao_frio}/100")


def _mostrar_sentidos(estado, detalhe=False):
    b = BIOMES[estado.bioma_espinha]
    temperatura = random.randint(*b["temperatura"])
    estado.temperatura = temperatura
    print("\n" + "—" * 68)
    print(f"{b['nome'].upper()} — {estado.local_espinha}")
    print(random.choice(b["visoes"]))
    print(f"Você ouve {random.choice(b['sons'])}; o ar cheira a {random.choice(b['odores'])}.")
    print(f"Temperatura estimada: {temperatura}°C. A flora visível inclui {random.choice(b['flora'])}.")
    if detalhe:
        print("Você se obriga a olhar devagar: direção do vento, neve mexida, pedras soltas e qualquer brilho que não pertença ao céu.")
    print("—" * 68)


def sortear_nascimento_espinha(estado):
    """Escolhe bioma e devolve a cena inicial usada pelo carregador de cenas."""
    estado.bioma_espinha = random.choices(list(BIOMES), weights=(38, 34, 28), k=1)[0]
    estado.local_espinha = random.choice(BIOMES[estado.bioma_espinha]["locais"])
    estado.exposicao_frio = 15 if estado.bioma_espinha != "cavernas_gigantes" else 8
    estado.temperatura = random.randint(*BIOMES[estado.bioma_espinha]["temperatura"])
    _flag(estado, "descobriu_regiao_espinha_do_mundo")
    _flag(estado, f"descobriu_bioma_{estado.bioma_espinha}")
    return "00_despertar_espinha"


def _encontro_social(estado):
    eventos = {
        "cordilheira_monumental": [
            "Um batedor Northariano passa distante com duas renas. Ele não o vê — ainda.",
            "Você encontra uma marca anã antiga apontando para uma passagem segura; seguir ou ignorar essa pista ficará na sua memória.",
        ],
        "vales_profundos": [
            "Uma figura encapuzada observa o vale e some antes que você consiga saber se era pessoa ou sombra.",
            "Há pegadas de botas ao lado de rastros de cervo: alguém também procura alimento aqui.",
        ],
        "cavernas_gigantes": [
            "Uma lâmpada apagada e recente revela que você não é a primeira pessoa nesta passagem.",
            "Você escuta três batidas ritmadas numa parede distante. Podem ser ferramentas; podem não ser.",
        ],
    }
    print("\nENCONTRO: " + random.choice(eventos[estado.bioma_espinha]))
    _flag(estado, f"ouviu_sinal_{estado.bioma_espinha}")


def _golpe_inimigo(estado, inimigo):
    _, _, ataque, defesa, _ = inimigo
    dado = random.randint(1, 20)
    dano = max(1, ataque + dado // 6 - int(getattr(estado, "defesa", 0)))
    estado.vida = max(0, estado.vida - dano)
    print(f"{inimigo[0]} ataca: d20 {dado}. Você sofre {dano} de dano.")


def _combate(estado, inimigo):
    nome, vida, ataque, defesa, ameaca = inimigo
    print(f"\n⚠ {nome} percebe você e avança. Não é uma cena decorativa: ele ataca.")
    while vida > 0 and estado.vida > 0:
        print(f"\n{nome}: {vida} de vida | Sua vida: {estado.vida}/{estado.vida_max}")
        acao = input("[l]utar  [f]ugir  [u]sar item: ").strip().lower()
        if acao == "f":
            if _rolar(estado, "agilidade", 10 + ameaca, "Fugir pelo terreno"):
                print("Você escapa, mas perde tempo e deixa rastros.")
                _avancar(estado, 1, frio=5)
                _flag(estado, f"fugiu_de_{slug(nome)}")
                return
            _golpe_inimigo(estado, inimigo)
            continue
        if acao == "u":
            inventario = _get(estado, "inventario", [])
            if "Poção de Cura" in inventario:
                inventario.remove("Poção de Cura")
                estado.vida = min(estado.vida_max, estado.vida + 8)
                print("Você usa uma Poção de Cura e recupera 8 de vida.")
            else:
                print("Você não tem uma Poção de Cura utilizável.")
            _golpe_inimigo(estado, inimigo)
            continue
        if acao != "l":
            print("A indecisão não para o inimigo.")
            _golpe_inimigo(estado, inimigo)
            continue
        dado = random.randint(1, 20)
        bonus = int(getattr(estado, "ataque", 4)) + int(_get(estado, "atributos", {}).get("forca", 0))
        total = dado + bonus
        if dado == 20 or (dado != 1 and total >= 10 + defesa):
            dano = max(1, int(getattr(estado, "ataque", 4)) + dado // 5 - defesa)
            if dado == 20:
                dano *= 2
                print("Acerto crítico!")
            vida -= dano
            print(f"Você ataca: d20 {dado} + {bonus} = {total}. {nome} sofre {dano} de dano.")
        else:
            print(f"Você erra: d20 {dado} + {bonus} = {total}.")
        if vida > 0:
            _golpe_inimigo(estado, inimigo)
    if estado.vida > 0:
        print(f"Você sobrevive ao confronto com {nome}. O silêncio que sobra é pior do que esperava.")
        estado.xp = _get(estado, "xp", 0) + 5 * ameaca
        _flag(estado, f"sobreviveu_a_{slug(nome)}")


def _encontro(estado):
    b = BIOMES[estado.bioma_espinha]
    chance = 0.10 + b["perigo"] * 0.035 + (0.10 if _periodo(estado) == "noite" else 0)
    if random.random() >= chance:
        if random.random() < 0.12:
            _encontro_social(estado)
        return
    criatura = random.choice(b["raros"] if random.random() < 0.07 else b["hostis"])
    _combate(estado, criatura)


def _mover(estado, direcao):
    destino = TRANSICOES[estado.bioma_espinha][direcao]
    origem = estado.bioma_espinha
    estado.bioma_espinha = destino
    estado.local_espinha = random.choice(BIOMES[destino]["locais"])
    frio = 8 if destino != "cavernas_gigantes" else 2
    _avancar(estado, 2, frio)
    _flag(estado, f"caminhou_{origem}_{direcao}")
    if not _tem_flag(estado, f"descobriu_bioma_{destino}"):
        _flag(estado, f"descobriu_bioma_{destino}")
        print(f"\n✦ DESCOBERTO: {BIOMES[destino]['nome']}.")
    print(f"\nVocê caminha para {direcao}. Duas horas passam escolhendo cada apoio e ouvindo o mundo antes de pisar.")
    _mostrar_sentidos(estado)
    _encontro(estado)


def _coletar(estado):
    b = BIOMES[estado.bioma_espinha]
    planta = random.choice(b["flora"])
    dificuldade = 13 if "Flor" in planta or "Luminite" in planta else 10
    print(f"\nVocê procura com cuidado: {planta} pode estar ao alcance, mas o terreno cobra atenção.")
    if _rolar(estado, "sobrevivencia", dificuldade, "Coletar sem se ferir"):
        _item(estado, planta)
        estado.xp = _get(estado, "xp", 0) + 3
        print(f"Você obtém: {planta}. A descoberta fica registrada na sua memória.")
        _flag(estado, f"coletou_{slug(planta)}")
    else:
        print("Você não encontra um exemplar seguro. O tempo e o frio continuam cobrando seu preço.")
    _avancar(estado, 1, frio=3)


def _fogueira(estado):
    inventario = _get(estado, "inventario", [])
    tem_material = any("Madeira" in x or "Vinha" in x or "Grama" in x for x in inventario)
    print("\nVocê escolhe uma reentrância protegida, separa pedras e tenta acordar uma chama contra o vento.")
    dificuldade = 11 if tem_material else 15
    if _rolar(estado, "sobrevivencia", dificuldade, "Acender fogueira"):
        estado.exposicao_frio = max(0, estado.exposicao_frio - 30)
        estado.energia = min(100, estado.energia + 10)
        _flag(estado, "tem_fogueira_espinha")
        print("A chama pequena resiste. Você recupera calor, mas sua luz também pode ser vista de longe.")
    else:
        estado.exposicao_frio = min(100, estado.exposicao_frio + 8)
        print("A chama morre. Seus dedos doem mais do que antes.")
    _avancar(estado, 1, frio=0)


def _descansar(estado):
    protegido = _tem_flag(estado, "tem_fogueira_espinha") or estado.bioma_espinha == "cavernas_gigantes"
    print("\nVocê descansa sem se entregar totalmente ao sono; escuta o ambiente entre cada respiração.")
    _avancar(estado, 3, frio=0 if protegido else 12)
    estado.energia = min(100, estado.energia + (28 if protegido else 14))
    if protegido:
        estado.exposicao_frio = max(0, estado.exposicao_frio - 12)
        print("O abrigo permite recuperar parte das forças.")
    else:
        print("Sem abrigo confiável, o descanso ajuda pouco e o frio encontra cada fresta.")
    _encontro(estado)


def _alimentar(estado):
    inventario = _get(estado, "inventario", [])
    comida = next((x for x in inventario if any(p in x.lower() for p in ("carne", "peixe", "baga", "fruto", "alga", "pão"))), None)
    if not comida:
        print("Você não tem comida segura. Caçar ou coletar agora pode ser necessário.")
        return
    inventario.remove(comida)
    estado.fome = max(0, estado.fome - 28)
    print(f"Você come {comida}. A fome diminui, embora o ambiente continue estranho ao seu paladar.")


def _beber(estado):
    inventario = _get(estado, "inventario", [])
    agua = next((x for x in inventario if "água" in x.lower() or "agua" in x.lower()), None)
    if agua:
        inventario.remove(agua)
        estado.sede = max(0, estado.sede - 35)
        print(f"Você bebe {agua}.")
    elif estado.bioma_espinha == "cavernas_gigantes":
        if _rolar(estado, "sobrevivencia", 12, "Encontrar água sem contaminação"):
            estado.sede = max(0, estado.sede - 20)
            print("Você encontra uma gota constante de água limpa entre cristais.")
        else:
            print("A água que você encontra tem cheiro metálico demais para arriscar.")
    else:
        print("Você não tem água potável. Neve, gelo e água parada não são automaticamente seguros.")


def _inventario(estado):
    itens = _get(estado, "inventario", [])
    print("\nInventário: " + (", ".join(itens) if itens else "vazio"))
    print("Marcas persistentes: " + ", ".join(sorted(_get(estado, "flags", set()))[-6:]))


def iniciar_exploracao_espinha(estado, bioma_inicial="aleatorio"):
    """Loop livre chamado por uma opção de cena com modo=exploracao_espinha."""
    if bioma_inicial == "aleatorio" or bioma_inicial not in BIOMES:
        sortear_nascimento_espinha(estado)
    else:
        estado.bioma_espinha = bioma_inicial
        estado.local_espinha = random.choice(BIOMES[bioma_inicial]["locais"])
        estado.exposicao_frio = 12 if bioma_inicial != "cavernas_gigantes" else 7
        _flag(estado, f"descobriu_bioma_{bioma_inicial}")

    print("\n" + "=" * 68)
    print("A ESPINHA DO MUNDO — EXPLORAÇÃO LIVRE")
    print("Você não reconhece esta terra. Cada som, cheiro e padrão no gelo precisa ser aprendido.")
    print("=" * 68)
    _mostrar_sentidos(estado, detalhe=True)
    if random.random() < 0.14:
        print("\nAlgo perigoso já estava perto de você quando acordou.")
        _combate(estado, random.choice(BIOMES[estado.bioma_espinha]["hostis"]))

    while estado.vida > 0:
        _status(estado)
        comando = input("\n[n]orte [s]ul [l]este [o]este | [v]er [c]oletar [f]ogo [d]escansar | [e] comer [b] beber [i]tens | [q] sair: ").strip().lower()
        if comando in {"n", "s", "l", "o"}:
            _mover(estado, {"n": "norte", "s": "sul", "l": "leste", "o": "oeste"}[comando])
        elif comando == "v":
            _mostrar_sentidos(estado, detalhe=True)
            _avancar(estado, 1, frio=2)
        elif comando == "c":
            _coletar(estado)
        elif comando == "f":
            _fogueira(estado)
        elif comando == "d":
            _descansar(estado)
        elif comando == "e":
            _alimentar(estado)
        elif comando == "b":
            _beber(estado)
        elif comando == "i":
            _inventario(estado)
        elif comando == "q":
            print("Você interrompe a exploração e procura um lugar para reorganizar os pensamentos.")
            return "00_despertar_espinha"
        else:
            print("Comando desconhecido. O mundo não para enquanto você decide.")
    print("\nVocê sucumbe na Espinha do Mundo.")
    return "fim_derrota"
