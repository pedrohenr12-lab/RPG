"""Exploração livre e sobrevivência da Região 4: Stonevale."""
from __future__ import annotations
import random

B = {
    "platos_aridos": {
        "nome": "Platôs Áridos", "perigo": 4, "temp": (24, 40),
        "locais": ["Planalto de Cristal", "Salina das Luas", "Ninho da Águia do Platô"],
        "visao": ["Rocha vermelha se estende até o horizonte; cristais de Silicyn devolvem o sol como lâminas.", "Rachaduras rasas cortam o chão. Podem esconder água, escorpiões ou nada."],
        "sons": ["vento seco raspando as pedras", "um grito de águia muito alto", "areia escorrendo numa fenda"],
        "odores": ["poeira quente e minerais", "sal seco", "umidade fraca de um cacto cortado"],
        "flora": ["Cacto-de-Cristal", "Arbusto-de-Pedra", "Flor-do-Deserto", "Líquen-de-Quartzo"],
        "hostis": [("Serpente-de-Areia", 19, 6, 2, 4), ("Escorpião-de-Quartzo", 15, 5, 3, 3), ("Lagarto-de-Cristal", 18, 5, 3, 2)],
        "raros": [("Espectro-de-Pedra", 22, 7, 4, 4), ("Guardião de Silicyn", 30, 9, 6, 5)],
    },
    "canions_profundos": {
        "nome": "Cânions Profundos", "perigo": 5, "temp": (-5, 40),
        "locais": ["Cânion Proibido", "Ponte das Vinhas", "Caverna dos Ecos"],
        "visao": ["Paredes vermelhas e douradas descem por centenas de metros; um fio de água sazonal desaparece no fundo.", "A luz entra em lâminas finas. Nas sombras, a pedra conserva uma umidade velha."],
        "sons": ["um eco devolve palavras que você não disse", "pedras caem muito abaixo", "asas batem em fenda invisível"],
        "odores": ["rocha aquecida", "musgo úmido", "ar frio que sai de uma cavidade profunda"],
        "flora": ["Samambaia-de-Fenda", "Flor-de-Cachoeira", "Musgo-de-Eco", "Vinhas-de-Parede"],
        "hostis": [("Serpente-de-Fenda", 17, 5, 2, 3), ("Lagarto-de-Parede", 15, 4, 2, 2), ("Dragão-de-Pedra Menor", 29, 8, 5, 5)],
        "raros": [("Eco-Vivo", 22, 7, 4, 4), ("Guardião do Cânion Proibido", 35, 10, 6, 5)],
    },
    "vales_fertis_isolados": {
        "nome": "Vales Férteis Isolados", "perigo": 3, "temp": (18, 30),
        "locais": ["Oásis Esmeralda", "Cascata da Vida", "Nascente de Jade"],
        "visao": ["Verde intenso rompe o deserto como se o vale tivesse sido esquecido pelas estações secas.", "Água cristalina cai entre palmeiras e vinhas. A beleza faz você baixar a guarda."],
        "sons": ["cascata constante", "peixes quebrando a superfície", "o bater iridescente de pequenas asas"],
        "odores": ["água limpa e fruta madura", "musgo fresco", "flores quentes que lembram miragem"],
        "flora": ["Palmeira-de-Oásis", "Lírio-d’Água Cristalino", "Árvore-de-Vida do Vale", "Flor-de-Miragem"],
        "hostis": [("Guardião de Jade", 27, 8, 5, 5), ("Ninfa-do-Oásis", 22, 6, 4, 4), ("Borboleta-de-Luminite", 10, 3, 1, 1)],
        "raros": [("Fênix-de-Pedra", 34, 10, 5, 5), ("Cervo-de-Oásis em Pânico", 16, 4, 2, 2)],
    },
}
T = {
    "platos_aridos": {"norte":"platos_aridos","sul":"vales_fertis_isolados","leste":"canions_profundos","oeste":"platos_aridos"},
    "canions_profundos": {"norte":"platos_aridos","sul":"vales_fertis_isolados","leste":"canions_profundos","oeste":"platos_aridos"},
    "vales_fertis_isolados": {"norte":"platos_aridos","sul":"vales_fertis_isolados","leste":"canions_profundos","oeste":"vales_fertis_isolados"},
}

def get(e, n, d):
    if not hasattr(e, n): setattr(e, n, d)
    return getattr(e, n)

def flag(e, n):
    if hasattr(e, "adicionar_flag"): e.adicionar_flag(n)
    else: get(e, "flags", set()).add(n)

def has(e, n):
    return e.tem_flag(n) if hasattr(e, "tem_flag") else n in get(e, "flags", set())

def item(e, n):
    if hasattr(e, "adicionar_item"): e.adicionar_item(n)
    else: get(e, "inventario", []).append(n)

def slug(s):
    import unicodedata
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return "".join(c if c.isalnum() else "_" for c in s).strip("_")

def period(e):
    h = get(e, "hora", 8)
    return "manhã" if 6 <= h < 12 else "tarde" if 12 <= h < 18 else "noite"

def roll(e, attr, dc, title):
    die = random.randint(1, 20); bonus = int(get(e, "atributos", {}).get(attr, 0)); total = die + bonus
    ok = die == 20 or (die != 1 and total >= dc)
    print(f"\n🎲 {title}: d20 ({die}) + {bonus} = {total} | dificuldade {dc}")
    print("✓ Sucesso." if ok else "✗ Falha.")
    return ok

def advance(e, hours, heat=0, cold=0):
    get(e, "dia", 1); get(e, "hora", 8); get(e, "energia", 100); get(e, "fome", 15); get(e, "sede", 15)
    e.hora += hours
    while e.hora >= 24: e.hora -= 24; e.dia += 1
    e.energia = max(0, e.energia - max(1, hours * 3)); e.fome = min(100, e.fome + hours * 2); e.sede = min(100, e.sede + hours * 4)
    e.exposicao_calor = max(0, get(e, "exposicao_calor", 0) + heat); e.exposicao_frio = max(0, get(e, "exposicao_frio", 0) + cold)
    if e.fome >= 85 or e.sede >= 85: e.vida = max(0, e.vida - 1); print("A fome ou a sede já reduzem sua vida.")
    if e.exposicao_calor >= 75: e.vida = max(0, e.vida - 2); e.energia = max(0, e.energia - 5); print("A insolação tira 2 de vida.")
    if e.exposicao_frio >= 75: e.vida = max(0, e.vida - 2); print("O frio noturno atravessa suas roupas. Você perde 2 de vida.")

def status(e):
    print(f"\n[DIA {e.dia} — {e.hora:02d}:00, {period(e)}] Vida {e.vida}/{e.vida_max} | Energia {e.energia}/100 | Fome {e.fome}/100 | Sede {e.sede}/100 | Calor {e.exposicao_calor}/100 | Frio {e.exposicao_frio}/100")

def sensory(e, careful=False):
    b = B[e.bioma_stonevale]; e.temperatura = random.randint(*b["temp"])
    print("\n" + "—" * 68); print(f"{b['nome'].upper()} — {e.local_stonevale}")
    print(random.choice(b["visao"])); print(f"Você ouve {random.choice(b['sons'])}; sente {random.choice(b['odores'])}.")
    print(f"Temperatura estimada: {e.temperatura}°C. Próximo de você: {random.choice(b['flora'])}.")
    if careful: print("Você mede o céu, o vento, a inclinação e onde uma sombra poderá existir daqui a uma hora.")
    print("—" * 68)

def sortear_nascimento_stonevale(e):
    e.bioma_stonevale = random.choices(list(B), weights=(42,32,26), k=1)[0]
    e.local_stonevale = random.choice(B[e.bioma_stonevale]["locais"]); e.exposicao_calor = 10; e.exposicao_frio = 0
    flag(e, "descobriu_regiao_stonevale"); flag(e, f"descobriu_bioma_{e.bioma_stonevale}")
    return "00_despertar_stonevale"

def hit(e, enemy):
    name, _, atk, _, _ = enemy; die = random.randint(1, 20); dmg = max(1, atk + die // 6 - int(getattr(e, "defesa", 0)))
    e.vida = max(0, e.vida - dmg); print(f"{name} ataca: d20 {die}. Você sofre {dmg} de dano.")

def combat(e, enemy):
    name, hp, atk, defense, threat = enemy
    print(f"\n⚠ {name} percebe você e avança. Em Stonevale, terreno aberto não garante fuga.")
    while hp > 0 and e.vida > 0:
        print(f"\n{name}: {hp} de vida | Você: {e.vida}/{e.vida_max}")
        a = input("[l]utar  [f]ugir  [u]sar Poção de Cura: ").strip().lower()
        if a == "f":
            if roll(e, "agilidade", 10 + threat, "Fugir pelo terreno"):
                print("Você escapa, mas perde tempo e água."); advance(e, 1, heat=4 if period(e)!="noite" else 0, cold=3 if period(e)=="noite" else 0); flag(e, f"fugiu_de_{slug(name)}"); return
            hit(e, enemy); continue
        if a == "u":
            inv = get(e, "inventario", [])
            if "Poção de Cura" in inv: inv.remove("Poção de Cura"); e.vida = min(e.vida_max, e.vida + 8); print("Você recupera 8 de vida.")
            else: print("Você não possui Poção de Cura.")
            hit(e, enemy); continue
        if a != "l": hit(e, enemy); continue
        die = random.randint(1,20); bonus = int(getattr(e,"ataque",4)) + int(get(e,"atributos",{}).get("forca",0)); total = die + bonus
        if die == 20 or (die != 1 and total >= 10 + defense):
            dmg = max(1, int(getattr(e,"ataque",4)) + die // 5 - defense)
            if die == 20: dmg *= 2; print("Acerto crítico!")
            hp -= dmg; print(f"Você acerta: d20 {die} + {bonus} = {total}; causa {dmg} de dano.")
        else: print(f"Você erra: d20 {die} + {bonus} = {total}.")
        if hp > 0: hit(e, enemy)
    if e.vida > 0: print(f"Você sobrevive a {name}."); e.xp = get(e,"xp",0) + threat * 5; flag(e, f"sobreviveu_a_{slug(name)}")

def event(e):
    b = B[e.bioma_stonevale]; chance = .08 + b["perigo"]*.035 + (.06 if period(e)=="noite" else 0)
    if random.random() < chance: combat(e, random.choice(b["raros"] if random.random()<.07 else b["hostis"]))
    elif random.random() < .12:
        signs = {"platos_aridos":"Pedras empilhadas por alguém apontam para uma fenda, mas não dizem se há água.", "canions_profundos":"Uma corda velha está presa acima da parede. Alguém passou por aqui.", "vales_fertis_isolados":"Um círculo de pedras limpas perto da nascente sugere um lugar sagrado."}
        print("\nSINAL DE CIVILIZAÇÃO: " + signs[e.bioma_stonevale]); flag(e, f"encontrou_sinal_{e.bioma_stonevale}")

def move(e, direction):
    old=e.bioma_stonevale; dest=T[old][direction]; e.bioma_stonevale=dest; e.local_stonevale=random.choice(B[dest]["locais"])
    advance(e,2,heat=7 if period(e)!="noite" and dest!="vales_fertis_isolados" else 2,cold=5 if period(e)=="noite" and dest=="canions_profundos" else 0); flag(e,f"caminhou_{old}_{direction}")
    if not has(e,f"descobriu_bioma_{dest}"): flag(e,f"descobriu_bioma_{dest}"); print(f"\n✦ DESCOBERTO: {B[dest]['nome']}.")
    print(f"\nVocê segue para {direction}. A viagem exige pausas para escolher sombra, apoio e uma rota segura."); sensory(e); event(e)

def collect(e):
    b=B[e.bioma_stonevale]; plant=random.choice(b["flora"]); dc=14 if any(x in plant for x in ("Cristal","Miragem","Eco")) else 10
    print(f"\nVocê procura {plant}, sem desperdiçar água ou tocar em espinhos sem necessidade.")
    if roll(e,"sobrevivencia",dc,"Coletar em Stonevale"): item(e,plant); e.xp=get(e,"xp",0)+3; flag(e,f"coletou_{slug(plant)}"); print(f"Você obtém: {plant}.")
    else: print("Você não consegue coletar nada seguro desta vez.")
    advance(e,1,heat=3 if period(e)!="noite" else 0)

def water(e):
    print("\nVocê procura insetos, plantas, sombra, umidade na pedra e o comportamento de animais.")
    dc=9 if e.bioma_stonevale=="vales_fertis_isolados" else 13 if e.bioma_stonevale=="canions_profundos" else 16
    if roll(e,"sobrevivencia",dc,"Encontrar água potável"): item(e,"Água Potável"); flag(e,f"encontrou_agua_{e.bioma_stonevale}"); print("Você encontra água suficiente para um recipiente improvisado.")
    else: print("Você encontra apenas sal, pedra úmida demais ou uma poça que não inspira confiança.")
    advance(e,1,heat=3 if period(e)!="noite" else 0)

def climb(e):
    if e.bioma_stonevale!="canions_profundos": print("Não há parede de cânion para escalar aqui."); return
    print("\nVocê testa rocha, vinhas e o peso do próprio corpo. Uma queda não é um erro pequeno.")
    if roll(e,"agilidade",14,"Escalar parede de cânion"): flag(e,"escalou_parede_de_stonevale"); e.xp=get(e,"xp",0)+5; print("Você alcança um terraço e enxerga uma rota oculta.")
    else: e.vida=max(0,e.vida-3); print("Uma pedra cede. Você para a queda, mas sofre 3 de dano.")
    advance(e,2,heat=4 if period(e)!="noite" else 0,cold=3 if period(e)=="noite" else 0); event(e)

def mirage(e):
    if e.bioma_stonevale!="vales_fertis_isolados": print("Não há Flor-de-Miragem perto; apenas distorção de calor."); return
    print("\nO calor desenha água onde talvez só exista pedra. Você escolhe confiar nos detalhes, não nos olhos.")
    if roll(e,"percepcao",13,"Distinguir miragem de caminho"): item(e,"Flor-de-Miragem"); flag(e,"respeitou_miragem_do_vale"); print("Você encontra a flor sem arrancar sua raiz.")
    else: print("Você caminha em círculos até perceber que o oásis estava atrás de você."); advance(e,2,heat=7)

def camp(e):
    inv=get(e,"inventario",[]); material=any(x in y for x in inv for y in ("Madeira","Vinha","Grama"))
    print("\nVocê monta abrigo. Uma fogueira pode salvar do frio noturno ou denunciar sua luz a quilômetros.")
    if roll(e,"sobrevivencia",11 if material else 15,"Montar acampamento"):
        e.exposicao_calor=max(0,e.exposicao_calor-12); e.exposicao_frio=max(0,e.exposicao_frio-25); e.energia=min(100,e.energia+8); flag(e,"tem_acampamento_stonevale"); print("O abrigo resiste ao vento.")
    else: print("O vento leva calor e faíscas antes de a fogueira firmar.")
    advance(e,1)

def rest(e):
    safe=has(e,"tem_acampamento_stonevale") or e.bioma_stonevale=="vales_fertis_isolados"; print("\nVocê descansa sem baixar completamente a guarda.")
    advance(e,3,heat=0 if safe else 3,cold=0 if safe else 5); e.energia=min(100,e.energia+(28 if safe else 12)); event(e)

def eat(e):
    inv=get(e,"inventario",[]); food=next((x for x in inv if any(w in x.lower() for w in ("fruto","carne","peixe","baga","alga"))),None)
    if not food: print("Você não tem alimento que reconheça como seguro."); return
    inv.remove(food); e.fome=max(0,e.fome-28); print(f"Você come {food}.")

def drink(e):
    inv=get(e,"inventario",[]); water_item=next((x for x in inv if "água" in x.lower() or "agua" in x.lower()),None)
    if not water_item: print("Você não tem água potável. Procure-a antes que a sede escolha por você."); return
    inv.remove(water_item); e.sede=max(0,e.sede-38); e.exposicao_calor=max(0,e.exposicao_calor-8); print(f"Você bebe {water_item}.")

def explore_stonevale(e, bioma_inicial="aleatorio"):
    if bioma_inicial=="aleatorio" or bioma_inicial not in B: sortear_nascimento_stonevale(e)
    else: e.bioma_stonevale=bioma_inicial; e.local_stonevale=random.choice(B[bioma_inicial]["locais"]); e.exposicao_calor=10; flag(e,f"descobriu_bioma_{bioma_inicial}")
    print("\n"+"="*68+"\nSTONEVALE — EXPLORAÇÃO LIVRE\nVocê é estrangeiro neste mundo. O deserto não explica suas regras; ele cobra cada erro em água, energia, silêncio e distância.\n"+"="*68)
    sensory(e,True)
    if random.random()<.14: print("\nUm predador ou guardião já estava perto quando você acordou."); combat(e,random.choice(B[e.bioma_stonevale]["hostis"]))
    while e.vida>0:
        status(e)
        cmd=input("\n[n]orte [s]ul [l]este [o]este | [v]er [c]oletar [a] água [r] escalar [m] miragem | [f]ogo [d]escansar [e] comer [b] beber [i]tens | [q] sair: ").strip().lower()
        if cmd in {"n","s","l","o"}: move(e,{"n":"norte","s":"sul","l":"leste","o":"oeste"}[cmd])
        elif cmd=="v": sensory(e,True); advance(e,1,heat=2 if period(e)!="noite" else 0)
        elif cmd=="c": collect(e)
        elif cmd=="a": water(e)
        elif cmd=="r": climb(e)
        elif cmd=="m": mirage(e)
        elif cmd=="f": camp(e)
        elif cmd=="d": rest(e)
        elif cmd=="e": eat(e)
        elif cmd=="b": drink(e)
        elif cmd=="i": print("\nInventário: "+(", ".join(get(e,"inventario",[])) or "vazio")+"\nMarcas: "+", ".join(sorted(get(e,"flags",set()))[-6:]))
        elif cmd=="q": print("Você interrompe a exploração para reorganizar os pensamentos."); return "00_despertar_stonevale"
        else: print("Comando desconhecido. O sol continua avançando mesmo assim.")
    print("\nVocê sucumbe em Stonevale."); return "fim_derrota"

# Nome usado pelo gancho do motor de cenas.
iniciar_exploracao_stonevale = explore_stonevale

