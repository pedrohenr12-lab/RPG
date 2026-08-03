"""Exploração livre e sobrevivência extrema da Região 1: Frostreach."""
from __future__ import annotations
import random

B = {
    "orla_costeira_gelo": {
        "nome":"Orla Costeira do Gelo","perigo":4,"temp":(-25,2),
        "locais":["Fiordes da Aurora","Cavernas de Pressium","Falésias do Vento"],
        "visao":["Fiordes escuros cortam gelo branco-azulado. A aurora desenha anéis fracos sobre o mar congelado.", "Falésias molhadas e gelo fino dividem a costa; cada maré reorganiza o caminho que parecia seguro."],
        "sons":["mar sob uma placa de gelo", "vento batendo em cavernas", "o canto distante e grave de uma baleia"],
        "odores":["sal, ferro e neve", "algas presas sob o gelo", "fumaça longínqua trazida pelo vento"],
        "flora":["Musgo-de-Fiorde","Alga-de-Gelo","Flor-de-Maré","Cristal-Verde"],
        "hostis":[("Urso-Costeiro de Frost",24,7,3,4),("Serpente-Marinha de Gelo",22,7,3,5),("Caranguejo-de-Pressium",18,5,5,2)],
        "raros":[("Baleia-de-Gelo",30,8,4,4),("Guardião de Pressium",32,9,6,5)],
    },
    "planalto_central_frostreach": {
        "nome":"Planalto Central","perigo":4,"temp":(-24,-6),
        "locais":["Tundra do Silêncio","Fendas dos Vorath","Rota das Renas"],
        "visao":["Tundra sem fim se abre sob um céu pálido. Vento apaga rastros antes que você entenda quem os deixou.", "Fendas avermelhadas cortam a neve: cicatrizes da Guerra dos Vorath, quentes demais para parecerem naturais."],
        "sons":["vento cortante", "corvos discutindo sobre restos", "cascos de rena muito longe"],
        "odores":["neve limpa e ferro", "pelagem molhada", "terra quente demais perto das fendas"],
        "flora":["Musgo-Congelado","Grama-de-Gelo","Flor-do-Vento Polar","Líquen-de-Fenda"],
        "hostis":[("Lobo-de-Gelo",20,6,2,4),("Mamute-das-Presas",30,7,4,3),("Raposa-Ártica acuada",13,4,1,2)],
        "raros":[("Yeti-das-Presas",34,9,5,5),("Lobo Fractal",26,8,4,5)],
    },
    "presas_de_gelo": {
        "nome":"Presas de Gelo","perigo":5,"temp":(-30,-5),
        "locais":["Pico de Aldric","Cavernas de Luminite","Passagem das Presas"],
        "visao":["Picos quebram o mar de nuvens. Cristais de Luminite dão à neve um brilho que não vem do sol.", "Uma passagem estreita entre montanhas parece segura até você perceber seda congelada atravessando a rocha."],
        "sons":["gelo estalando muito abaixo", "grito de águia contra o vento", "um ruído mineral vindo de uma caverna"],
        "odores":["ar seco e pedra fria", "cristal recém-fraturado", "pelo de predador em caverna alta"],
        "flora":["Líquen-de-Pico","Musgo-de-Caverna","Flor-de-Gelo Eterna","Fungo-Luminoso"],
        "hostis":[("Urso-Glacial das Presas",32,9,5,5),("Aranha-de-Gelo",17,5,2,3),("Dragão-de-Gelo Menor",27,8,4,5)],
        "raros":[("Yeti-das-Presas",34,9,5,5),("Dragão-de-Caverna",42,11,7,5),("Espírito-do-Vento",21,6,3,4)],
    },
}
T = {
    "orla_costeira_gelo":{"norte":"orla_costeira_gelo","sul":"planalto_central_frostreach","leste":"presas_de_gelo","oeste":"orla_costeira_gelo"},
    "planalto_central_frostreach":{"norte":"presas_de_gelo","sul":"planalto_central_frostreach","leste":"orla_costeira_gelo","oeste":"planalto_central_frostreach"},
    "presas_de_gelo":{"norte":"presas_de_gelo","sul":"planalto_central_frostreach","leste":"presas_de_gelo","oeste":"orla_costeira_gelo"},
}
def get(e,n,d):
    if not hasattr(e,n): setattr(e,n,d)
    return getattr(e,n)
def flag(e,n):
    if hasattr(e,"adicionar_flag"): e.adicionar_flag(n)
    else: get(e,"flags",set()).add(n)
def has(e,n): return e.tem_flag(n) if hasattr(e,"tem_flag") else n in get(e,"flags",set())
def item(e,n):
    if hasattr(e,"adicionar_item"): e.adicionar_item(n)
    else: get(e,"inventario",[]).append(n)
def slug(s):
    import unicodedata
    s=unicodedata.normalize("NFD",s).encode("ascii","ignore").decode().lower()
    return "".join(c if c.isalnum() else "_" for c in s).strip("_")
def period(e):
    h=get(e,"hora",8); return "manhã" if 6<=h<12 else "tarde" if 12<=h<18 else "noite"
def roll(e,attr,dc,title):
    die=random.randint(1,20); bonus=int(get(e,"atributos",{}).get(attr,0)); total=die+bonus
    ok=die==20 or (die!=1 and total>=dc)
    print(f"\n🎲 {title}: d20 ({die}) + {bonus} = {total} | dificuldade {dc}")
    print("✓ Sucesso." if ok else "✗ Falha."); return ok
def advance(e,hours,cold=0,wet=0):
    get(e,"dia",1); get(e,"hora",8); get(e,"energia",100); get(e,"fome",15); get(e,"sede",15)
    e.hora+=hours
    while e.hora>=24: e.hora-=24; e.dia+=1
    e.energia=max(0,e.energia-max(1,hours*3)); e.fome=min(100,e.fome+hours*2); e.sede=min(100,e.sede+hours*2)
    e.exposicao_frio=max(0,get(e,"exposicao_frio",0)+cold); e.umidade_corporal=min(100,get(e,"umidade_corporal",0)+wet)
    if e.fome>=85 or e.sede>=85: e.vida=max(0,e.vida-1); print("A fome ou a sede já reduzem sua vida.")
    if e.exposicao_frio>=65: e.vida=max(0,e.vida-2); e.energia=max(0,e.energia-5); print("O frio atravessa suas roupas. Você perde 2 de vida.")
    if e.exposicao_frio>=90: e.congelamento=get(e,"congelamento",0)+1; print("Sinais de congelamento aparecem nas extremidades.")
def status(e):
    print(f"\n[DIA {e.dia} — {e.hora:02d}:00, {period(e)}] Vida {e.vida}/{e.vida_max} | Energia {e.energia}/100 | Fome {e.fome}/100 | Sede {e.sede}/100 | Frio {e.exposicao_frio}/100 | Congelamento {get(e,'congelamento',0)}")
def sensory(e,careful=False):
    b=B[e.bioma_frostreach]; e.temperatura=random.randint(*b["temp"])
    print("\n"+"—"*68); print(f"{b['nome'].upper()} — {e.local_frostreach}")
    print(random.choice(b["visao"])); print(f"Você ouve {random.choice(b['sons'])}; sente {random.choice(b['odores'])}.")
    print(f"Temperatura estimada: {e.temperatura}°C. Flora próxima: {random.choice(b['flora'])}.")
    if careful: print("Você observa a direção do vento, a qualidade da neve, pegadas, rachaduras e qualquer brilho que não pertence ao céu.")
    print("—"*68)
def sortear_nascimento_frostreach(e):
    e.bioma_frostreach=random.choices(list(B),weights=(34,39,27),k=1)[0]; e.local_frostreach=random.choice(B[e.bioma_frostreach]["locais"])
    e.exposicao_frio=20 if e.bioma_frostreach!="presas_de_gelo" else 28; e.umidade_corporal=5; e.congelamento=0
    flag(e,"descobriu_regiao_frostreach"); flag(e,f"descobriu_bioma_{e.bioma_frostreach}"); return "00_despertar_frostreach"
def hit(e,enemy):
    name,_,atk,_,_=enemy; die=random.randint(1,20); dmg=max(1,atk+die//6-int(getattr(e,"defesa",0)))
    e.vida=max(0,e.vida-dmg); print(f"{name} ataca: d20 {die}. Você sofre {dmg} de dano.")
def combat(e,enemy):
    name,hp,atk,defense,threat=enemy; print(f"\n⚠ {name} percebe você e ataca. Em Frostreach, um erro de combate também é um erro contra o clima.")
    while hp>0 and e.vida>0:
        print(f"\n{name}: {hp} de vida | Você: {e.vida}/{e.vida_max}"); a=input("[l]utar  [f]ugir  [u]sar Poção de Cura: ").strip().lower()
        if a=="f":
            if roll(e,"agilidade",10+threat,"Fugir sobre gelo e neve"):
                print("Você escapa, mas gasta tempo e calor."); advance(e,1,cold=8,wet=3); flag(e,f"fugiu_de_{slug(name)}"); return
            hit(e,enemy); continue
        if a=="u":
            inv=get(e,"inventario",[])
            if "Poção de Cura" in inv: inv.remove("Poção de Cura"); e.vida=min(e.vida_max,e.vida+8); print("Você recupera 8 de vida.")
            else: print("Você não possui Poção de Cura.")
            hit(e,enemy); continue
        if a!="l": hit(e,enemy); continue
        die=random.randint(1,20); bonus=int(getattr(e,"ataque",4))+int(get(e,"atributos",{}).get("forca",0)); total=die+bonus
        if die==20 or (die!=1 and total>=10+defense):
            dmg=max(1,int(getattr(e,"ataque",4))+die//5-defense)
            if die==20: dmg*=2; print("Acerto crítico!")
            hp-=dmg; print(f"Você acerta: d20 {die} + {bonus} = {total}; causa {dmg} de dano.")
        else: print(f"Você erra: d20 {die} + {bonus} = {total}.")
        if hp>0: hit(e,enemy)
    if e.vida>0: print(f"Você sobrevive a {name}."); e.xp=get(e,"xp",0)+threat*5; flag(e,f"sobreviveu_a_{slug(name)}")
def social(e):
    choices={
        "orla_costeira_gelo":["Uma pequena embarcação Northariana aparece entre os fiordes. A tripulação observa você antes de decidir se encosta.", "Marcas de machado numa rocha indicam um abrigo de pescadores que pode estar vazio ou ocupado."],
        "planalto_central_frostreach":["Uma caravana de renas cruza a distância. Os viajantes podem ser caçadores, comerciantes ou um clã que não gosta de estranhos.", "Um corvo deixa cair um pedaço de tecido perto de você; há fumaça de acampamento muito ao sul."],
        "presas_de_gelo":["Runas anãs marcam uma pedra de passagem. Alguém conhecia uma rota segura por aqui — há muito tempo.", "Você encontra um sino de metal preso ao gelo, talvez deixado por um escalador que nunca voltou."],
    }
    print("\nSINAL DE CIVILIZAÇÃO: "+random.choice(choices[e.bioma_frostreach])); flag(e,f"encontrou_sinal_{e.bioma_frostreach}")
def event(e):
    b=B[e.bioma_frostreach]; chance=.10+b["perigo"]*.04+(.08 if period(e)=="noite" else 0)
    if random.random()<chance: combat(e,random.choice(b["raros"] if random.random()<.07 else b["hostis"]))
    elif random.random()<.12: social(e)
def move(e,direction):
    old=e.bioma_frostreach; dest=T[old][direction]; e.bioma_frostreach=dest; e.local_frostreach=random.choice(B[dest]["locais"])
    advance(e,2,cold=10 if dest=="presas_de_gelo" else 7,wet=7 if dest=="orla_costeira_gelo" else 1); flag(e,f"caminhou_{old}_{direction}")
    if not has(e,f"descobriu_bioma_{dest}"): flag(e,f"descobriu_bioma_{dest}"); print(f"\n✦ DESCOBERTO: {B[dest]['nome']}.")
    print(f"\nVocê caminha para {direction}. Atravessar esta terra exige testar cada apoio antes de entregar seu peso ao gelo."); sensory(e); event(e)
def collect(e):
    b=B[e.bioma_frostreach]; plant=random.choice(b["flora"]); dc=14 if any(x in plant for x in ("Cristal","Flor-de-Gelo","Fenda")) else 10
    print(f"\nVocê procura {plant}, protegendo os dedos e evitando quebrar um recurso que não conhece.")
    if roll(e,"sobrevivencia",dc,"Coletar no frio"): item(e,plant); e.xp=get(e,"xp",0)+3; flag(e,f"coletou_{slug(plant)}"); print(f"Você obtém: {plant}.")
    else: print("O frio e o terreno impedem uma coleta segura.")
    advance(e,1,cold=5,wet=2)
def hunt(e):
    b=B[e.bioma_frostreach]; prey={"orla_costeira_gelo":"Foca-de-Cristal","planalto_central_frostreach":"Lebre-de-Neve","presas_de_gelo":"Cabra-das-Presas"}[e.bioma_frostreach]
    print(f"\nVocê procura sinais de {prey}. Caçar pode dar alimento; também pode chamar quem caça o mesmo animal.")
    if roll(e,"sobrevivencia",14,"Rastrear e caçar"):
        item(e,"Carne de Caça Fria"); flag(e,f"cacou_{slug(prey)}"); print("Você consegue alimento, mas deixa marcas no terreno.")
        if random.random()<.25: print("O sangue na neve atraiu atenção."); event(e)
    else: print("Você gasta energia e não encontra presa.")
    advance(e,2,cold=8)
def fish(e):
    if e.bioma_frostreach!="orla_costeira_gelo": print("Não há água costeira acessível para pesca aqui."); return
    print("\nVocê abre um ponto no gelo e observa a água escura abaixo. O mar não promete devolver o que toma.")
    if roll(e,"sobrevivencia",13,"Pescar sob o gelo"): item(e,"Peixe de Gelo"); flag(e,"pescou_no_fiorde"); print("Você pesca um peixe pequeno e brilhante.")
    else: print("A linha volta vazia, e seus dedos doem mais.")
    advance(e,2,cold=9,wet=6)
def climb(e):
    if e.bioma_frostreach!="presas_de_gelo": print("Não há passagem vertical suficiente para exigir escalada aqui."); return
    print("\nVocê procura rachaduras, gelo firme e qualquer apoio que não ceda sob seu peso.")
    if roll(e,"agilidade",15,"Escalar as Presas de Gelo"): flag(e,"escalou_presas_de_gelo"); e.xp=get(e,"xp",0)+5; print("Você alcança uma saliência e vê uma rota que não existia do chão.")
    else: e.vida=max(0,e.vida-3); print("O gelo quebra. Você interrompe a queda, mas sofre 3 de dano.")
    advance(e,2,cold=12); event(e)
def camp(e):
    inv=get(e,"inventario",[]); material=any(x in y for x in inv for y in ("Madeira","Grama","Vinha","Musgo"))
    print("\nVocê procura proteção do vento e tenta uma fogueira. Sem fogo, o frio decide quanto da noite você poderá atravessar.")
    if roll(e,"sobrevivencia",12 if material else 16,"Acender fogueira em Frostreach"):
        e.exposicao_frio=max(0,e.exposicao_frio-35); e.energia=min(100,e.energia+10); flag(e,"tem_acampamento_frostreach"); print("Uma chama pequena resiste. Sua luz pode ser vista de longe.")
    else: e.exposicao_frio=min(100,e.exposicao_frio+8); print("A neve e o vento vencem a tentativa.")
    advance(e,1)
def rest(e):
    safe=has(e,"tem_acampamento_frostreach"); print("\nVocê descansa em blocos curtos, acordando a cada estalo do gelo.")
    advance(e,3,cold=0 if safe else 14,wet=0 if safe else 3); e.energia=min(100,e.energia+(30 if safe else 11)); event(e)
def eat(e):
    inv=get(e,"inventario",[]); food=next((x for x in inv if any(w in x.lower() for w in ("carne","peixe","alga","baga","fruto"))),None)
    if not food: print("Você não tem alimento seguro."); return
    inv.remove(food); e.fome=max(0,e.fome-28); print(f"Você come {food}.")
def drink(e):
    inv=get(e,"inventario",[]); water=next((x for x in inv if "água" in x.lower() or "agua" in x.lower()),None)
    if water: inv.remove(water); e.sede=max(0,e.sede-35); print(f"Você bebe {water}."); return
    if has(e,"tem_acampamento_frostreach") and roll(e,"sobrevivencia",10,"Derreter neve sem contaminar"): e.sede=max(0,e.sede-20); print("Você derrete neve e consegue água potável.")
    else: print("Neve não é água pronta. Sem calor ou cuidado, ela pode piorar sua situação.")
def iniciar_exploracao_frostreach(e,bioma_inicial="aleatorio"):
    if bioma_inicial=="aleatorio" or bioma_inicial not in B: sortear_nascimento_frostreach(e)
    else: e.bioma_frostreach=bioma_inicial; e.local_frostreach=random.choice(B[bioma_inicial]["locais"]); e.exposicao_frio=20; e.congelamento=0; flag(e,f"descobriu_bioma_{bioma_inicial}")
    print("\n"+"="*68+"\nFROSTREACH — EXPLORAÇÃO LIVRE\nVocê não pertence a este mundo. Aqui, o frio não é cenário: é uma criatura paciente que aprende cada falha sua.\n"+"="*68)
    sensory(e,True)
    if random.random()<.16: print("\nAlgo hostil já estava perto quando você acordou."); combat(e,random.choice(B[e.bioma_frostreach]["hostis"]))
    while e.vida>0:
        status(e)
        cmd=input("\n[n]orte [s]ul [l]este [o]este | [v]er [c]oletar [h] caçar [p]escar [r] escalar | [f]ogo [d]escansar [e] comer [b] beber [i]tens | [q] sair: ").strip().lower()
        if cmd in {"n","s","l","o"}: move(e,{"n":"norte","s":"sul","l":"leste","o":"oeste"}[cmd])
        elif cmd=="v": sensory(e,True); advance(e,1,cold=3)
        elif cmd=="c": collect(e)
        elif cmd=="h": hunt(e)
        elif cmd=="p": fish(e)
        elif cmd=="r": climb(e)
        elif cmd=="f": camp(e)
        elif cmd=="d": rest(e)
        elif cmd=="e": eat(e)
        elif cmd=="b": drink(e)
        elif cmd=="i": print("\nInventário: "+(", ".join(get(e,"inventario",[])) or "vazio")+"\nMarcas: "+", ".join(sorted(get(e,"flags",set()))[-6:]))
        elif cmd=="q": print("Você interrompe a exploração para reorganizar os pensamentos."); return "00_despertar_frostreach"
        else: print("Comando desconhecido. O vento continua apagando seus rastros.")
    print("\nVocê sucumbe em Frostreach."); return "fim_derrota"

