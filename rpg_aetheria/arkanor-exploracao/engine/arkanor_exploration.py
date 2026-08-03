"""Exploração livre, sobrevivência e encontros sociais para Arkanor."""
from __future__ import annotations
import random

B = {
    "planicies_ferteis": {
        "nome":"Planícies Férteis","perigo":2,"temp":(8,26),
        "locais":["Campos Dourados","Estrada do Aurenta","Portões de Arkanor"],
        "visao":["Campos de trigo dourado se movem em ondas até onde sua visão alcança. Torres da capital são uma promessa distante.", "Cercas baixas, carroças e trilhas de animais cruzam a grama alta; escolher uma rota muda quem poderá vê-lo."],
        "sons":["moinhos e aves de rapina","rodas de carroça muito longe","insetos escondidos entre espigas"],
        "odores":["trigo seco e terra fértil","fumaça de fogão distante","capim esmagado por rebanhos"],
        "flora":["Trigo-Dourado de Arkanor","Arbusto-de-Fruto-Solar","Girassol-Simétrico","Raiz-de-Cálcio"],
        "hostis":[("Lobo-de-Planície",16,5,2,3),("Hiena-das-Planícies",17,5,2,3),("Leão-de-Campo",25,7,4,4)],
        "raros":[("Titã das Planícies",40,9,6,5),("Predador-Celeste",28,8,4,5)],
    },
    "colinas_suaves": {
        "nome":"Colinas Suaves","perigo":2,"temp":(7,23),
        "locais":["Círculo de Orbitium","Vinhedos das Colinas","Tocas de Arkanor"],
        "visao":["Morros ondulantes formam camadas de verde e pedra. Algumas rochas erodidas em círculos parecem deliberadas.", "Bosques dispersos protegem ruínas de muros baixos e vinhas que sobem as encostas."],
        "sons":["abelhas nas moitas","um falcão circulando alto","pedras pequenas rolando de uma toca"],
        "odores":["uva azeda e solo seco","madeira de carvalho","erva de fonte recém-amassada"],
        "flora":["Carvalho-Suave","Arbusto-de-Fruto-Doce","Flor-de-Pedra Circular","Vinhas-de-Colina"],
        "hostis":[("Javali-Comum",19,6,3,3),("Texugo-de-Arkanor",15,5,2,2),("Falcão-Circular",14,4,2,2)],
        "raros":[("Cervo Astral",24,6,3,4),("Predador-Espiral",23,7,3,4)],
    },
    "vales_verdes": {
        "nome":"Vales Verdes","perigo":2,"temp":(10,24),
        "locais":["Porto do Aurenta","Cascatas Verdes","Nascente Pura"],
        "visao":["O rio se curva entre colinas; reflexos de água e folhas escondem profundidades que você ainda não sabe medir.", "Cascatas transformam pedra em musgo e deixam o ar tão úmido que cada cor parece mais forte."],
        "sons":["água em movimento e martins-pescadores","barcos prendendo cordas no porto","sapos respondendo uns aos outros"],
        "odores":["água doce, salgueiro e peixe","musgo de cascata","fruta madura trazida por comerciantes"],
        "flora":["Salgueiro-do-Aurenta","Lírio-d’Água Verde","Flor-de-Água-Pura","Vinhas-de-Rio"],
        "hostis":[("Cobra-d’Água",14,4,1,1),("Javali-Comum",19,6,3,3),("Lontra-Predadora",17,5,2,2)],
        "raros":[("Guardião das Águas",29,8,5,5),("Libélula-Circular Gigante",18,5,2,3)],
    },
}
T = {
    "planicies_ferteis":{"norte":"planicies_ferteis","sul":"vales_verdes","leste":"colinas_suaves","oeste":"planicies_ferteis"},
    "colinas_suaves":{"norte":"planicies_ferteis","sul":"vales_verdes","leste":"colinas_suaves","oeste":"planicies_ferteis"},
    "vales_verdes":{"norte":"planicies_ferteis","sul":"vales_verdes","leste":"colinas_suaves","oeste":"vales_verdes"},
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
def advance(e,hours):
    get(e,"dia",1); get(e,"hora",8); get(e,"energia",100); get(e,"fome",15); get(e,"sede",15)
    e.hora+=hours
    while e.hora>=24: e.hora-=24; e.dia+=1
    e.energia=max(0,e.energia-max(1,hours*2)); e.fome=min(100,e.fome+hours*2); e.sede=min(100,e.sede+hours*3)
    if e.fome>=85 or e.sede>=85: e.vida=max(0,e.vida-1); print("A fome ou a sede começam a reduzir sua vida.")
def status(e):
    print(f"\n[DIA {e.dia} — {e.hora:02d}:00, {period(e)}] Vida {e.vida}/{e.vida_max} | Energia {e.energia}/100 | Fome {e.fome}/100 | Sede {e.sede}/100")
def sensory(e,careful=False):
    b=B[e.bioma_arkanor]; e.temperatura=random.randint(*b["temp"])
    print("\n"+"—"*68); print(f"{b['nome'].upper()} — {e.local_arkanor}")
    print(random.choice(b["visao"])); print(f"Você ouve {random.choice(b['sons'])}; sente {random.choice(b['odores'])}.")
    print(f"Temperatura: {e.temperatura}°C. Flora próxima: {random.choice(b['flora'])}.")
    if careful: print("Você observa marcas de rodas, rastros, postes de estrada, fumaça e os lugares onde alguém poderia estar vendo você.")
    print("—"*68)
def sortear_nascimento_arkanor(e):
    e.bioma_arkanor=random.choices(list(B),weights=(42,30,28),k=1)[0]; e.local_arkanor=random.choice(B[e.bioma_arkanor]["locais"])
    flag(e,"descobriu_regiao_arkanor"); flag(e,f"descobriu_bioma_{e.bioma_arkanor}"); return "00_despertar_arkanor"
def hit(e,enemy):
    name,_,atk,_,_=enemy; die=random.randint(1,20); dmg=max(1,atk+die//6-int(getattr(e,"defesa",0)))
    e.vida=max(0,e.vida-dmg); print(f"{name} ataca: d20 {die}. Você sofre {dmg} de dano.")
def combat(e,enemy):
    name,hp,atk,defense,threat=enemy; print(f"\n⚠ {name} escolhe atacá-lo. Longe da estrada, ninguém é obrigado a ouvir seus gritos.")
    while hp>0 and e.vida>0:
        print(f"\n{name}: {hp} de vida | Você: {e.vida}/{e.vida_max}"); a=input("[l]utar  [f]ugir  [u]sar Poção de Cura: ").strip().lower()
        if a=="f":
            if roll(e,"agilidade",10+threat,"Fugir pelo terreno"): print("Você escapa e deixa rastros atrás."); advance(e,1); flag(e,f"fugiu_de_{slug(name)}"); return
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
      "planicies_ferteis":["Uma carroça diminui a velocidade ao vê-lo. O condutor pode oferecer carona, cobrar caro ou chamar guardas.", "Um grupo de trabalhadores observa suas roupas estranhas, cochicha e volta ao campo."],
      "colinas_suaves":["Uma família de cultivadores deixa uma jarra de água perto da estrada; não há bilhete, só uma expectativa silenciosa.", "Um vigia de colina pergunta de onde você veio. A resposta moldará o primeiro rumor sobre você."],
      "vales_verdes":["No porto, uma barqueira procura alguém para carregar caixas. O pagamento pode ser comida, informação ou uma passagem.", "Um curandeiro recolhe ervas perto da nascente e observa seus ferimentos antes de falar."],
    }
    print("\nENCONTRO SOCIAL: "+random.choice(choices[e.bioma_arkanor])); flag(e,f"encontrou_pessoa_{e.bioma_arkanor}")
    if hasattr(e,"alterar_reputacao"): e.alterar_reputacao("reino",1)
def event(e):
    b=B[e.bioma_arkanor]; chance=.04+b["perigo"]*.03+(.05 if period(e)=="noite" else 0)
    if random.random()<chance: combat(e,random.choice(b["raros"] if random.random()<.05 else b["hostis"]))
    elif random.random()<.23: social(e)
def move(e,direction):
    old=e.bioma_arkanor; dest=T[old][direction]; e.bioma_arkanor=dest; e.local_arkanor=random.choice(B[dest]["locais"]); advance(e,2); flag(e,f"caminhou_{old}_{direction}")
    if not has(e,f"descobriu_bioma_{dest}"): flag(e,f"descobriu_bioma_{dest}"); print(f"\n✦ DESCOBERTO: {B[dest]['nome']}.")
    print(f"\nVocê caminha para {direction}. Estradas ajudam, mas nem toda trilha leva a uma cidade."); sensory(e); event(e)
def collect(e):
    b=B[e.bioma_arkanor]; plant=random.choice(b["flora"]); dc=13 if "Água-Pura" in plant or "Circular" in plant else 10
    print(f"\nVocê procura {plant}, escolhendo apenas o que pode coletar sem destruir o lugar.")
    if roll(e,"sobrevivencia",dc,"Coletar com cuidado"): item(e,plant); e.xp=get(e,"xp",0)+3; flag(e,f"coletou_{slug(plant)}"); print(f"Você obtém: {plant}.")
    else: print("Você não encontra um exemplar seguro desta vez.")
    advance(e,1)
def road(e):
    print("\nVocê segue os sinais de passagem humana: rodas, marcos, fumaça e pontes. Isso pode levá-lo a ajuda — e a perguntas.")
    if roll(e,"percepcao",11,"Encontrar uma rota habitada"):
        e.local_arkanor="Posto de estrada" if e.bioma_arkanor=="planicies_ferteis" else ("Aldeia de colina" if e.bioma_arkanor=="colinas_suaves" else "Porto do Aurenta")
        flag(e,"encontrou_rota_habitada_arkanor"); advance(e,2); print(f"Você chega a {e.local_arkanor}. A civilização está próxima, mas ninguém sabe quem você é."); social(e)
    else: advance(e,2); print("As trilhas se cruzam e se desfazem. Você não encontra um caminho confiável.")
def fish(e):
    if e.bioma_arkanor!="vales_verdes": print("Sem rio ou lago acessível, pescar aqui seria perder tempo."); return
    print("\nVocê prepara uma tentativa silenciosa de pesca, observando correnteza e sombras.")
    if roll(e,"sobrevivencia",12,"Pescar no Aurenta"): item(e,"Peixe-Prateado"); flag(e,"pescou_no_aurenta"); print("Você pega um Peixe-Prateado.")
    else: print("A corrente leva sua chance embora.")
    advance(e,2)
def rest(e):
    safe=has(e,"encontrou_rota_habitada_arkanor") or e.local_arkanor=="Porto do Aurenta"; print("\nVocê descansa em intervalos curtos, sempre atento a passos e vozes.")
    advance(e,3); e.energia=min(100,e.energia+(30 if safe else 16)); event(e)
def eat(e):
    inv=get(e,"inventario",[]); food=next((x for x in inv if any(w in x.lower() for w in ("trigo","fruto","carne","peixe","baga","alga"))),None)
    if not food: print("Você não tem alimento seguro."); return
    inv.remove(food); e.fome=max(0,e.fome-28); print(f"Você come {food}.")
def drink(e):
    inv=get(e,"inventario",[]); water=next((x for x in inv if "água" in x.lower() or "agua" in x.lower()),None)
    if water: inv.remove(water); e.sede=max(0,e.sede-35); print(f"Você bebe {water}."); return
    if e.bioma_arkanor=="vales_verdes" and roll(e,"sobrevivencia",10,"Encontrar água segura"): e.sede=max(0,e.sede-22); print("Você encontra água limpa entre os salgueiros.")
    else: print("Você não tem água potável.")
def iniciar_exploracao_arkanor(e,bioma_inicial="aleatorio"):
    if bioma_inicial=="aleatorio" or bioma_inicial not in B: sortear_nascimento_arkanor(e)
    else: e.bioma_arkanor=bioma_inicial; e.local_arkanor=random.choice(B[bioma_inicial]["locais"]); flag(e,f"descobriu_bioma_{bioma_inicial}")
    print("\n"+"="*68+"\nARKANOR — EXPLORAÇÃO LIVRE\nEste mundo é estranho, mas aqui há estradas, famílias, leis e comércio. Você pode procurar ajuda, evitar cidades ou construir uma reputação antes que o mundo construa uma para você.\n"+"="*68)
    sensory(e,True)
    if random.random()<.08: print("\nVocê acordou perto demais de um animal hostil."); combat(e,random.choice(B[e.bioma_arkanor]["hostis"]))
    while e.vida>0:
        status(e)
        cmd=input("\n[n]orte [s]ul [l]este [o]este | [v]er [c]oletar [r]ota habitada [p]escar | [d]escansar [e] comer [b] beber [i]tens | [q] sair: ").strip().lower()
        if cmd in {"n","s","l","o"}: move(e,{"n":"norte","s":"sul","l":"leste","o":"oeste"}[cmd])
        elif cmd=="v": sensory(e,True); advance(e,1)
        elif cmd=="c": collect(e)
        elif cmd=="r": road(e)
        elif cmd=="p": fish(e)
        elif cmd=="d": rest(e)
        elif cmd=="e": eat(e)
        elif cmd=="b": drink(e)
        elif cmd=="i": print("\nInventário: "+(", ".join(get(e,"inventario",[])) or "vazio")+"\nMarcas: "+", ".join(sorted(get(e,"flags",set()))[-6:]))
        elif cmd=="q": print("Você interrompe a exploração para reorganizar os pensamentos."); return "00_despertar_arkanor"
        else: print("Comando desconhecido. A estrada continua diante de você.")
    print("\nVocê sucumbe em Arkanor."); return "fim_derrota"

