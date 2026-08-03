"""Exploração livre, sobrevivência tropical e encontros da Região 5: Blackmarsh."""
from __future__ import annotations

import random

BIOMES = {
    "pantanos_vastos": {
        "nome": "Pântanos Vastos", "perigo": 5, "temperatura": (28, 38),
        "locais": ["Fenda Selada", "Luzes de Blackmarsh", "Corredor das Raízes Negras"],
        "visoes": [
            "Água marrom-preta reflete um céu branco de chuva. Cada raiz submersa parece uma mão tentando encontrar apoio.",
            "A neblina baixa desfaz a distância: uma árvore a vinte passos parece uma figura esperando por você.",
        ],
        "sons": ["insetos vibram em camadas", "algo pesado respira sob a água", "uma ave bate asas e some na chuva"],
        "odores": ["lama quente e folhas em decomposição", "água parada", "um doce floral forte demais para ser seguro"],
        "flora": ["Musgo-Negro", "Alga-Pura de Aquanium", "Flor-de-Fogo-Fátuo", "Cogumelo-de-Sombra"],
        "hostis": [("Crocodilo-Negro", 28, 8, 4, 5), ("Serpente-d’Água Gigante", 21, 7, 3, 5), ("Sapo-Gigante de Blackmarsh", 18, 5, 2, 3)],
        "raros": [("Vulto-das-Fendas", 26, 8, 4, 5), ("Ninfa-Negra", 24, 7, 4, 5), ("Guardião da Fenda Selada", 36, 10, 6, 5)],
    },
    "mangues_gigantes": {
        "nome": "Mangues Gigantes", "perigo": 4, "temperatura": (25, 35),
        "locais": ["Labirinto de Mangue", "Cavernas da Maré", "Salina de Raízes"],
        "visoes": [
            "Raízes aéreas se cruzam acima da lama como costelas de um animal imenso. A maré apaga pegadas com paciência.",
            "Pequenos espelhos de água salgada refletem folhas cristalizadas e um céu que muda rápido demais.",
        ],
        "sons": ["água infiltra cavernas", "carapaças raspam na lama", "morcegos respondem ao próprio eco"],
        "odores": ["sal, algas e madeira úmida", "terra recém-revirada", "fruta fermentada"],
        "flora": ["Mangue-Gigante", "Alga-Salobra", "Planta-de-Sal", "Samambaia-Costeira"],
        "hostis": [("Crocodilo-Costeiro", 23, 7, 3, 4), ("Serpente-de-Raiz", 17, 5, 2, 3), ("Caranguejo-Gigante de Mangue", 20, 6, 4, 3)],
        "raros": [("Eco-das-Raízes", 20, 6, 3, 4), ("Guardião de Harmonix", 31, 9, 5, 5)],
    },
    "ilhas_vegetacao_flutuante": {
        "nome": "Ilhas de Vegetação Flutuante", "perigo": 5, "temperatura": (26, 37),
        "locais": ["Ilhas Migrantes", "Mar de Turfa", "Núcleo de Orbitium"],
        "visoes": [
            "O solo sob seus pés cede quase imperceptivelmente. Plantas e turfa formam uma ilha que não estava aqui em mapas antigos.",
            "Flores coloridas crescem sobre uma camada de musgo espesso; abaixo dela há apenas água escura e movimento lento.",
        ],
        "sons": ["turfa estala sob pressão", "aves chamam de ilha em ilha", "bolhas sobem em círculos que não parecem naturais"],
        "odores": ["terra quente e água ácida", "vegetação esmagada", "um perfume doce que irrita a garganta"],
        "flora": ["Musgo-Flutuante", "Planta-Venenosa de Patterium", "Cogumelo-Migrante", "Vinhas-de-Turfa"],
        "hostis": [("Serpente-Flutuante", 19, 6, 2, 4), ("Rã-Flutuante", 14, 4, 2, 2), ("Caramujo-Gigante", 22, 5, 5, 2)],
        "raros": [("Sombra-Flutuante", 27, 8, 4, 5), ("Espírito-das-Ilhas", 22, 6, 4, 4), ("Guardião de Orbitium", 34, 10, 6, 5)],
    },
}

TRANSICOES = {
    "pantanos_vastos": {"norte": "mangues_gigantes", "sul": "pantanos_vastos", "leste": "ilhas_vegetacao_flutuante", "oeste": "pantanos_vastos"},
    "mangues_gigantes": {"norte": "mangues_gigantes", "sul": "pantanos_vastos", "leste": "ilhas_vegetacao_flutuante", "oeste": "mangues_gigantes"},
    "ilhas_vegetacao_flutuante": {"norte": "mangues_gigantes", "sul": "pantanos_vastos", "leste": "ilhas_vegetacao_flutuante", "oeste": "pantanos_vastos"},
}


def _get(e, n, d):
    if not hasattr(e, n): setattr(e, n, d)
    return getattr(e, n)

def _flag(e, n):
    if hasattr(e, "adicionar_flag"): e.adicionar_flag(n)
    else: _get(e, "flags", set()).add(n)

def _has(e, n):
    return e.tem_flag(n) if hasattr(e, "tem_flag") else n in _get(e, "flags", set())

def _item(e, n):
    if hasattr(e, "adicionar_item"): e.adicionar_item(n)
    else: _get(e, "inventario", []).append(n)

def _roll(e, attr, dc, name):
    die = random.randint(1, 20); bonus = int(_get(e, "atributos", {}).get(attr, 0)); total = die + bonus
    ok = die == 20 or (die != 1 and total >= dc)
    print(f"\n🎲 {name}: d20 ({die}) + {bonus} = {total} | dificuldade {dc}")
    print("✓ Sucesso." if ok else "✗ Falha.")
    return ok

def _period(e):
    h = _get(e, "hora", 8)
    return "manhã" if 6 <= h < 12 else "tarde" if 12 <= h < 18 else "noite"

def _advance(e, hours, heat=0, wet=0):
    _get(e, "dia", 1); _get(e, "hora", 8); _get(e, "energia", 100); _get(e, "fome", 15); _get(e, "sede", 15)
    e.hora += hours
    while e.hora >= 24: e.hora -= 24; e.dia += 1
    e.energia = max(0, e.energia - max(1, hours * 3)); e.fome = min(100, e.fome + hours * 2); e.sede = min(100, e.sede + hours * 4)
    e.exposicao_calor = max(0, _get(e, "exposicao_calor", 0) + heat); e.umidade_corporal = min(100, _get(e, "umidade_corporal", 0) + wet)
    if e.sede >= 85 or e.fome >= 85:
        e.vida = max(0, e.vida - 1); print("A sede ou a fome começam a reduzir sua vida.")
    if e.exposicao_calor >= 75:
        e.vida = max(0, e.vida - 2); e.energia = max(0, e.energia - 5); print("O calor e a umidade drenam suas forças. Você perde 2 de vida.")
    if e.umidade_corporal >= 85:
        print("Suas roupas estão encharcadas. Descansar sem abrigo será menos eficiente.")

def _status(e):
    print(f"\n[DIA {e.dia} — {e.hora:02d}:00, {_period(e)}] Vida {e.vida}/{e.vida_max} | Energia {e.energia}/100 | Fome {e.fome}/100 | Sede {e.sede}/100 | Calor {e.exposicao_calor}/100 | Umidade {e.umidade_corporal}/100")

def _sensory(e, careful=False):
    b = BIOMES[e.bioma_blackmarsh]; e.temperatura = random.randint(*b["temperatura"])
    print("\n" + "—" * 68); print(f"{b['nome'].upper()} — {e.local_blackmarsh}")
    print(random.choice(b["visoes"])); print(f"Você ouve {random.choice(b['sons'])}; sente {random.choice(b['odores'])}.")
    print(f"Temperatura: {e.temperatura}°C. Entre a vegetação, você reconhece {random.choice(b['flora'])}.")
    if careful: print("Você observa a altura da água, folhas mordidas, rastros, bolhas, correntezas e os lugares onde o silêncio fica repentino.")
    print("—" * 68)

def sortear_nascimento_blackmarsh(e):
    e.bioma_blackmarsh = random.choices(list(BIOMES), weights=(39, 34, 27), k=1)[0]
    e.local_blackmarsh = random.choice(BIOMES[e.bioma_blackmarsh]["locais"]); e.exposicao_calor = 12; e.umidade_corporal = 20
    _flag(e, "descobriu_regiao_blackmarsh"); _flag(e, f"descobriu_bioma_{e.bioma_blackmarsh}")
    return "00_despertar_blackmarsh"

def _enemy_hit(e, enemy):
    name, _, atk, _, _ = enemy; die = random.randint(1,20); damage = max(1, atk + die // 6 - int(getattr(e,"defesa",0)))
    e.vida = max(0, e.vida - damage); print(f"{name} ataca: d20 {die}. Você sofre {damage} de dano.")

def _combat(e, enemy):
    name, hp, atk, defense, threat = enemy
    print(f"\n⚠ {name} percebe sua presença e vem atacar. A lama, a água e as raízes limitam seus movimentos.")
    while hp > 0 and e.vida > 0:
        print(f"\n{name}: {hp} de vida | Você: {e.vida}/{e.vida_max}")
        action=input("[l]utar  [f]ugir  [u]sar Poção de Cura: ").strip().lower()
        if action == "f":
            if _roll(e,"agilidade",10+threat,"Fugir sem afundar"):
                print("Você escapa, mas perde uma hora escolhendo terreno firme."); _advance(e,1,heat=3,wet=6); _flag(e,f"fugiu_de_{slug(name)}"); return
            _enemy_hit(e,enemy); continue
        if action == "u":
            inv=_get(e,"inventario",[])
            if "Poção de Cura" in inv:
                inv.remove("Poção de Cura"); e.vida=min(e.vida_max,e.vida+8); print("Você recupera 8 de vida.")
            else: print("Você não possui Poção de Cura.")
            _enemy_hit(e,enemy); continue
        if action != "l": _enemy_hit(e,enemy); continue
        die=random.randint(1,20); bonus=int(getattr(e,"ataque",4))+int(_get(e,"atributos",{}).get("forca",0)); total=die+bonus
        if die==20 or (die!=1 and total>=10+defense):
            dmg=max(1,int(getattr(e,"ataque",4))+die//5-defense)
            if die==20: dmg*=2; print("Acerto crítico!")
            hp-=dmg; print(f"Você acerta: d20 {die} + {bonus} = {total}; causa {dmg} de dano.")
        else: print(f"Você erra: d20 {die} + {bonus} = {total}.")
        if hp>0: _enemy_hit(e,enemy)
    if e.vida>0:
        print(f"Você sobrevive a {name}. O pântano volta a fazer barulho como se nada tivesse acontecido.")
        e.xp=_get(e,"xp",0)+threat*5; _flag(e,f"sobreviveu_a_{slug(name)}")

def _social(e):
    text={
        "pantanos_vastos":"Um barco estreito, sem ocupante visível, encalha perto de você. Há marcas de remo recentes.",
        "mangues_gigantes":"Alguém amarrou pequenos sinos de concha nas raízes. O arranjo parece um aviso, não decoração.",
        "ilhas_vegetacao_flutuante":"Você vê fumaça distante sobre outra ilha, mas ela já começa a se afastar com a corrente.",
    }
    print("\nSINAL DE CIVILIZAÇÃO: " + text[e.bioma_blackmarsh]); _flag(e,f"encontrou_sinal_{e.bioma_blackmarsh}")

def _event(e):
    b=BIOMES[e.bioma_blackmarsh]; chance=0.10+b["perigo"]*.04+(0.08 if _period(e)=="noite" else 0)
    if random.random()<chance:
        _combat(e,random.choice(b["raros"] if random.random()<.08 else b["hostis"]))
    elif random.random()<.13: _social(e)

def _move(e,direction):
    old=e.bioma_blackmarsh; dest=TRANSICOES[old][direction]; e.bioma_blackmarsh=dest; e.local_blackmarsh=random.choice(BIOMES[dest]["locais"])
    heat=6 if _period(e)!="noite" else 2; wet=10 if dest!="mangues_gigantes" else 7
    _advance(e,2,heat,wet); _flag(e,f"caminhou_{old}_{direction}")
    if not _has(e,f"descobriu_bioma_{dest}"):
        _flag(e,f"descobriu_bioma_{dest}"); print(f"\n✦ DESCOBERTO: {BIOMES[dest]['nome']}.")
    print(f"\nVocê avança para {direction}. A caminhada é lenta: você testa cada apoio antes de entregar seu peso a ele.")
    _sensory(e); _event(e)

def _collect(e):
    b=BIOMES[e.bioma_blackmarsh]; plant=random.choice(b["flora"]); dc=14 if any(x in plant for x in ("Fogo", "Venenosa", "Cogumelo")) else 10
    print(f"\nVocê procura {plant}, verificando espinhos, secreções e o solo sob seus pés.")
    if _roll(e,"sobrevivencia",dc,"Coletar sem intoxicação"):
        _item(e,plant); e.xp=_get(e,"xp",0)+3; _flag(e,f"coletou_{slug(plant)}"); print(f"Você obtém: {plant}.")
    else: print("Você recua antes de tocar em algo que não entende. A prudência não dá recursos, mas mantém você vivo.")
    _advance(e,1,heat=3,wet=4)

def _follow_lights(e):
    if e.bioma_blackmarsh != "pantanos_vastos":
        print("Não há fogo-fátuo suficiente aqui; só reflexos e sombras."); return
    print("\nVocê segue as luzes devagar. Elas desenham uma rota bonita demais para inspirar confiança.")
    if _roll(e,"percepcao",14,"Distinguir fogo-fátuo de reflexo mortal"):
        _item(e,"Pétala de Fogo-Fátuo"); _flag(e,"seguiu_fogo_fatuo_com_respeito"); print("As luzes o levam a uma ilha firme e a uma flor iridescente. Você colhe apenas uma pétala.")
    else:
        print("A luz some quando seu pé entra em lama funda."); _advance(e,1,heat=4,wet=20); _event(e)

def _camp(e):
    inv=_get(e,"inventario",[]); material=any(x in y for x in inv for y in ("Vinha","Grama","Madeira"))
    print("\nAcender fogo aqui significa lutar contra água, chuva e umidade. Você também pode denunciar sua posição.")
    if _roll(e,"sobrevivencia",11 if material else 15,"Montar abrigo e fogueira"):
        e.umidade_corporal=max(0,e.umidade_corporal-35); e.exposicao_calor=max(0,e.exposicao_calor-10); e.energia=min(100,e.energia+8); _flag(e,"tem_acampamento_blackmarsh"); print("Uma chama protegida e um teto improvisado mudam sua noite.")
    else: e.umidade_corporal=min(100,e.umidade_corporal+10); print("A lenha molhada fuma, mas não sustenta chama.")
    _advance(e,1,heat=1,wet=0)

def _rest(e):
    safe=_has(e,"tem_acampamento_blackmarsh")
    print("\nVocê repousa em turnos curtos, acordando a cada ruído diferente.")
    _advance(e,3,heat=0 if safe else 6,wet=0 if safe else 8); e.energia=min(100,e.energia+(28 if safe else 12))
    if safe: e.umidade_corporal=max(0,e.umidade_corporal-12)
    _event(e)

def _drink(e):
    inv=_get(e,"inventario",[]); water=next((x for x in inv if "água" in x.lower() or "agua" in x.lower()),None)
    if water:
        inv.remove(water); e.sede=max(0,e.sede-35); print(f"Você bebe {water}."); return
    if e.bioma_blackmarsh=="pantanos_vastos" and _roll(e,"sobrevivencia",14,"Encontrar Aquanium puro"):
        e.sede=max(0,e.sede-25); print("Você encontra um ponto de água limpa entre as raízes.")
    else: print("Água ao redor não significa água potável. Beber sem saber pode custar mais do que a sede.")

def _eat(e):
    inv=_get(e,"inventario",[]); food=next((x for x in inv if any(w in x.lower() for w in ("peixe","carne","baga","fruto","alga"))),None)
    if not food: print("Você não tem alimento reconhecidamente seguro."); return
    inv.remove(food); e.fome=max(0,e.fome-28); print(f"Você come {food}. O gosto é estranho, mas seu corpo aceita o alimento.")

def _inventory(e):
    print("\nInventário: "+(", ".join(_get(e,"inventario",[])) or "vazio"))
    print("Últimas marcas: "+", ".join(sorted(_get(e,"flags",set()))[-6:]))

def iniciar_exploracao_blackmarsh(e, bioma_inicial="aleatorio"):
    if bioma_inicial=="aleatorio" or bioma_inicial not in BIOMES: sortear_nascimento_blackmarsh(e)
    else:
        e.bioma_blackmarsh=bioma_inicial; e.local_blackmarsh=random.choice(BIOMES[bioma_inicial]["locais"]); e.exposicao_calor=12; e.umidade_corporal=20; _flag(e,f"descobriu_bioma_{bioma_inicial}")
    print("\n"+"="*68+"\nBLACKMARSH — EXPLORAÇÃO LIVRE\nVocê não pertence a este mundo. Aqui, uma flor bonita, uma poça clara ou uma luz distante podem ser uma oportunidade — ou um aviso.\n"+"="*68)
    _sensory(e,True)
    if random.random()<.15:
        print("\nAlgo hostil já estava perto quando você acordou."); _combat(e,random.choice(BIOMES[e.bioma_blackmarsh]["hostis"]))
    while e.vida>0:
        _status(e)
        cmd=input("\n[n]orte [s]ul [l]este [o]este | [v]er [c]oletar [g] seguir luzes [f]ogo [d]escansar | [e] comer [b] beber [i]tens | [q] sair: ").strip().lower()
        if cmd in {"n","s","l","o"}: _move(e,{"n":"norte","s":"sul","l":"leste","o":"oeste"}[cmd])
        elif cmd=="v": _sensory(e,True); _advance(e,1,heat=2,wet=2)
        elif cmd=="c": _collect(e)
        elif cmd=="g": _follow_lights(e)
        elif cmd=="f": _camp(e)
        elif cmd=="d": _rest(e)
        elif cmd=="e": _eat(e)
        elif cmd=="b": _drink(e)
        elif cmd=="i": _inventory(e)
        elif cmd=="q": print("Você interrompe a exploração e tenta reorganizar os pensamentos."); return "00_despertar_blackmarsh"
        else: print("Comando desconhecido. A água continua se movendo enquanto você hesita.")
    print("\nVocê sucumbe em Blackmarsh."); return "fim_derrota"
