"""Exploração livre, sobrevivência úmida e encontros da Região 2: Eldorwood."""
from __future__ import annotations
import random

B = {
    "floresta_densa_antiga": {
        "nome":"Floresta Densa Antiga","perigo":3,"temp":(4,16),
        "locais":["Vila Eldor","Círculo das Árvores-Anciãs","Clareira da Penumbra"],
        "visao":["O dossel é tão alto e denso que a manhã chega ao solo como crepúsculo. Raízes largas desenham caminhos que não existiam ontem.", "Musgo verde-azulado cobre troncos. Uma árvore anciã parece observar você apenas porque o vento mudou."],
        "sons":["folhas se tocando muito acima", "uma coruja chamando duas vezes", "passos leves que somem quando você para"],
        "odores":["terra molhada e casca de árvore", "erva fresca com um fundo amargo", "madeira antiga e cogumelos"],
        "flora":["Erva-da-Neblina","Cogumelo-Sombra","Raiz-de-Vida","Lírio-da-Penumbra"],
        "hostis":[("Lobo-Sombrio",18,6,2,3),("Aranha-Teia-Verde",14,4,2,2),("Sapo-de-Folha",12,3,1,1)],
        "raros":[("Espírito-das-Árvores",24,7,4,4),("Predador Sombrio",28,8,4,5)],
    },
    "pantanos_rios": {
        "nome":"Pântanos e Rios","perigo":4,"temp":(8,20),
        "locais":["Ilhas do Fogo-Fátuo","Fonte de Aquanium","Labirinto de Raízes"],
        "visao":["Água lodosa passa entre raízes retorcidas. Ilhas de vegetação flutuante parecem firmes até você observar suas bordas se moverem.", "Luzes azuladas e roxas dançam sobre o pântano. A neblina encurta o mundo a poucos passos."],
        "sons":["água puxando raízes submersas", "insetos em círculos inquietos", "um estalo pesado perto demais"],
        "odores":["lama, chuva e folhas em decomposição", "água limpa escondida sob o lodo", "flor doce que tenta encobrir cheiro de pântano"],
        "flora":["Alga-Pura","Flor-de-Fogo-Fátuo","Junco-Espiral","Raiz-Retorcida"],
        "hostis":[("Crocodilo-de-Pântano",24,7,3,5),("Serpente-d’Água",17,5,2,3),("Sapo-Gigante de Eldor",18,5,2,3)],
        "raros":[("Insetos-Fogo-Fátuo",16,5,2,3),("Guardião das Águas",29,8,5,5)],
    },
    "colinas_arborizadas": {
        "nome":"Colinas Arborizadas","perigo":2,"temp":(6,18),
        "locais":["Círculo de Patterium","Bosques Dispersos","Tocas das Colinas"],
        "visao":["Colinas baixas alternam clareiras, carvalhos e rochas simétricas. Pela primeira vez, você enxerga longe sem precisar subir numa árvore.", "Grama alta se curva ao vento; algo pequeno se move entre bagas vermelhas e some antes de ser identificado."],
        "sons":["falcões descrevendo círculos no alto", "um javali revirando terra", "vento passando por galhos mais espaçados"],
        "odores":["capim frio e bagas maduras", "pedra úmida", "chá de erva-de-vento levado de uma aldeia distante"],
        "flora":["Arbusto-de-Fruto-Vermelho","Flor-de-Pedra","Erva-de-Vento","Carvalho-de-Colina"],
        "hostis":[("Javali-de-Eldor",20,6,3,3),("Texugo-das-Colinas",15,5,2,2),("Águia-de-Colina",14,4,2,2)],
        "raros":[("Falcão-de-Patterium",18,5,2,3),("Cervo Astral",24,6,3,4)],
    },
}
T = {
    "floresta_densa_antiga":{"norte":"floresta_densa_antiga","sul":"pantanos_rios","leste":"colinas_arborizadas","oeste":"floresta_densa_antiga"},
    "pantanos_rios":{"norte":"floresta_densa_antiga","sul":"pantanos_rios","leste":"colinas_arborizadas","oeste":"pantanos_rios"},
    "colinas_arborizadas":{"norte":"floresta_densa_antiga","sul":"pantanos_rios","leste":"colinas_arborizadas","oeste":"floresta_densa_antiga"},
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
def advance(e,hours,wet=0,cold=0):
    get(e,"dia",1); get(e,"hora",8); get(e,"energia",100); get(e,"fome",15); get(e,"sede",15)
    e.hora+=hours
    while e.hora>=24: e.hora-=24; e.dia+=1
    e.energia=max(0,e.energia-max(1,hours*3)); e.fome=min(100,e.fome+hours*2); e.sede=min(100,e.sede+hours*3)
    e.umidade_corporal=min(100,get(e,"umidade_corporal",0)+wet); e.exposicao_frio=max(0,get(e,"exposicao_frio",0)+cold)
    if e.fome>=85 or e.sede>=85: e.vida=max(0,e.vida-1); print("A fome ou a sede começam a reduzir sua vida.")
    if e.exposicao_frio>=75: e.vida=max(0,e.vida-2); e.energia=max(0,e.energia-4); print("Frio e roupas molhadas tiram 2 de vida.")
def status(e):
    print(f"\n[DIA {e.dia} — {e.hora:02d}:00, {period(e)}] Vida {e.vida}/{e.vida_max} | Energia {e.energia}/100 | Fome {e.fome}/100 | Sede {e.sede}/100 | Umidade {e.umidade_corporal}/100 | Frio {e.exposicao_frio}/100")
def sensory(e,careful=False):
    b=B[e.bioma_eldorwood]; e.temperatura=random.randint(*b["temp"])
    print("\n"+"—"*68); print(f"{b['nome'].upper()} — {e.local_eldorwood}")
    print(random.choice(b["visao"])); print(f"Você ouve {random.choice(b['sons'])}; sente {random.choice(b['odores'])}.")
    print(f"Temperatura: {e.temperatura}°C. Flora próxima: {random.choice(b['flora'])}.")
    if careful: print("Você procura folhas esmagadas, teias, pegadas, marcas de faca e qualquer mudança no som da floresta.")
    print("—"*68)
def sortear_nascimento_eldorwood(e):
    e.bioma_eldorwood=random.choices(list(B),weights=(42,32,26),k=1)[0]; e.local_eldorwood=random.choice(B[e.bioma_eldorwood]["locais"])
    e.umidade_corporal=10; e.exposicao_frio=5; flag(e,"descobriu_regiao_eldorwood"); flag(e,f"descobriu_bioma_{e.bioma_eldorwood}"); return "00_despertar_eldorwood"
def hit(e,enemy):
    name,_,atk,_,_=enemy; die=random.randint(1,20); dmg=max(1,atk+die//6-int(getattr(e,"defesa",0)))
    e.vida=max(0,e.vida-dmg); print(f"{name} ataca: d20 {die}. Você sofre {dmg} de dano.")
def combat(e,enemy):
    name,hp,atk,defense,threat=enemy; print(f"\n⚠ {name} percebe você e vem atacar. A mata, a lama ou a encosta decidem o espaço da luta.")
    while hp>0 and e.vida>0:
        print(f"\n{name}: {hp} de vida | Você: {e.vida}/{e.vida_max}"); a=input("[l]utar  [f]ugir  [u]sar Poção de Cura: ").strip().lower()
        if a=="f":
            if roll(e,"agilidade",10+threat,"Fugir pelo terreno"):
                print("Você escapa, mas deixa rastros e gasta energia."); advance(e,1,wet=4 if e.bioma_eldorwood=="pantanos_rios" else 1,cold=2); flag(e,f"fugiu_de_{slug(name)}"); return
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
    encounters={
      "floresta_densa_antiga":["Uma caçadora de Eldor observa a forma como você pisa nas raízes antes de decidir se fala.", "Uma figura esguia deixa um sinal de folhas trançadas numa árvore e desaparece no dossel."],
      "pantanos_rios":["Um pescador recolhe redes em silêncio. Ele conhece as correntes, mas não confia em estranhos.", "Uma criança de Eldor amarra fitas em raízes para marcar caminho de volta antes da maré."],
      "colinas_arborizadas":["Uma família de cultivadores oferece chá de erva-de-vento, mas pergunta de onde você veio.", "Um vigia de colina aponta uma trilha segura e pede que você não perturbe as pedras simétricas."],
    }
    print("\nENCONTRO SOCIAL: "+random.choice(encounters[e.bioma_eldorwood])); flag(e,f"encontrou_pessoa_{e.bioma_eldorwood}")
    if hasattr(e,"alterar_reputacao"): e.alterar_reputacao("vila_eldor",1)
def event(e):
    b=B[e.bioma_eldorwood]; chance=.08+b["perigo"]*.035+(.07 if period(e)=="noite" else 0)
    if random.random()<chance: combat(e,random.choice(b["raros"] if random.random()<.07 else b["hostis"]))
    elif random.random()<.16: social(e)
def move(e,direction):
    old=e.bioma_eldorwood; dest=T[old][direction]; e.bioma_eldorwood=dest; e.local_eldorwood=random.choice(B[dest]["locais"])
    advance(e,2,wet=9 if dest=="pantanos_rios" else 3,cold=3 if period(e)=="noite" else 1); flag(e,f"caminhou_{old}_{direction}")
    if not has(e,f"descobriu_bioma_{dest}"): flag(e,f"descobriu_bioma_{dest}"); print(f"\n✦ DESCOBERTO: {B[dest]['nome']}.")
    print(f"\nVocê caminha para {direction}. O ritmo é lento: cada raiz, poça e ramo pode esconder um desvio."); sensory(e); event(e)
def collect(e):
    b=B[e.bioma_eldorwood]; plant=random.choice(b["flora"]); dc=14 if any(x in plant for x in ("Sombra","Fogo","Raiz-de-Vida")) else 10
    print(f"\nVocê procura {plant}, verificando cheiro, textura e marcas de veneno antes de tocar.")
    if roll(e,"sobrevivencia",dc,"Coletar em Eldorwood"): item(e,plant); e.xp=get(e,"xp",0)+3; flag(e,f"coletou_{slug(plant)}"); print(f"Você obtém: {plant}.")
    else: print("Você prefere não colher um exemplar que não consegue identificar com segurança.")
    advance(e,1,wet=4 if e.bioma_eldorwood=="pantanos_rios" else 1,cold=1)
def follow_owl(e):
    if e.bioma_eldorwood!="floresta_densa_antiga": print("Não há Coruja-das-Brumas guiando você aqui."); return
    print("\nUma Coruja-das-Brumas voa alguns metros, espera e repete o gesto. Segui-la é aceitar um presságio desconhecido.")
    if roll(e,"percepcao",13,"Seguir a coruja sem se perder"):
        flag(e,"coruja_guiou_viajante"); item(e,"Pena das Brumas"); print("A coruja o leva a uma passagem seca e deixa uma pena no caminho.")
    else: print("Você perde a coruja na neblina e encontra uma teia quase invisível."); advance(e,2,wet=3,cold=2); event(e)
def cross_water(e):
    if e.bioma_eldorwood!="pantanos_rios": print("Não há travessia perigosa de pântano neste terreno."); return
    print("\nVocê escolhe raízes e ilhas flutuantes para cruzar. A água escura não revela profundidade nem movimento.")
    if roll(e,"agilidade",14,"Cruzar sem afundar"): flag(e,"atravessou_pantano_seguro"); print("Você alcança outra margem, encharcado mas inteiro.")
    else: e.vida=max(0,e.vida-2); print("Uma raiz cede. Você se corta e perde 2 de vida."); event(e)
    advance(e,2,wet=18,cold=3)
def camp(e):
    inv=get(e,"inventario",[]); material=any(x in y for x in inv for y in ("Madeira","Vinha","Grama"))
    print("\nVocê procura terra alta e tenta montar fogo contra a umidade. A fumaça pode chamar ajuda ou chamar predadores.")
    if roll(e,"sobrevivencia",12 if material else 16,"Montar fogueira na umidade"):
        e.umidade_corporal=max(0,e.umidade_corporal-35); e.exposicao_frio=max(0,e.exposicao_frio-25); e.energia=min(100,e.energia+8); flag(e,"tem_acampamento_eldorwood"); print("A fogueira vinga sob um abrigo improvisado.")
    else: e.umidade_corporal=min(100,e.umidade_corporal+8); print("Tudo está úmido demais. A chama não resiste.")
    advance(e,1)
def rest(e):
    safe=has(e,"tem_acampamento_eldorwood") or e.local_eldorwood=="Vila Eldor"; print("\nVocê descansa em intervalos curtos, ouvindo a mata entre cada respiração.")
    advance(e,3,wet=0 if safe else 5,cold=0 if safe else 6); e.energia=min(100,e.energia+(28 if safe else 12)); event(e)
def eat(e):
    inv=get(e,"inventario",[]); food=next((x for x in inv if any(w in x.lower() for w in ("fruto","carne","peixe","baga","alga","cogumelo"))),None)
    if not food: print("Você não tem alimento que reconheça como seguro."); return
    if "Cogumelo-Sombra" in food: print("Você decide não comer Cogumelo-Sombra sem identificar a variedade."); return
    inv.remove(food); e.fome=max(0,e.fome-28); print(f"Você come {food}.")
def drink(e):
    inv=get(e,"inventario",[]); water=next((x for x in inv if "água" in x.lower() or "agua" in x.lower()),None)
    if water: inv.remove(water); e.sede=max(0,e.sede-35); print(f"Você bebe {water}."); return
    if e.bioma_eldorwood=="pantanos_rios" and roll(e,"sobrevivencia",13,"Encontrar Aquanium puro"): e.sede=max(0,e.sede-25); print("Você encontra água limpa entre raízes e algas.")
    else: print("Chuva e pântano não significam água segura.")
def iniciar_exploracao_eldorwood(e,bioma_inicial="aleatorio"):
    if bioma_inicial=="aleatorio" or bioma_inicial not in B: sortear_nascimento_eldorwood(e)
    else: e.bioma_eldorwood=bioma_inicial; e.local_eldorwood=random.choice(B[bioma_inicial]["locais"]); e.umidade_corporal=10; e.exposicao_frio=5; flag(e,f"descobriu_bioma_{bioma_inicial}")
    print("\n"+"="*68+"\nELDORWOOD — EXPLORAÇÃO LIVRE\nVocê não conhece as regras desta floresta. Uma árvore pode ser abrigo, uma raiz pode ser remédio e uma luz pode ser o início de um caminho ou de uma morte.\n"+"="*68)
    sensory(e,True)
    if random.random()<.12: print("\nAlgo hostil já estava perto quando você acordou."); combat(e,random.choice(B[e.bioma_eldorwood]["hostis"]))
    while e.vida>0:
        status(e)
        cmd=input("\n[n]orte [s]ul [l]este [o]este | [v]er [c]oletar [g] seguir coruja [t]ravessar pântano | [f]ogo [d]escansar [e] comer [b] beber [i]tens | [q] sair: ").strip().lower()
        if cmd in {"n","s","l","o"}: move(e,{"n":"norte","s":"sul","l":"leste","o":"oeste"}[cmd])
        elif cmd=="v": sensory(e,True); advance(e,1,wet=2,cold=1)
        elif cmd=="c": collect(e)
        elif cmd=="g": follow_owl(e)
        elif cmd=="t": cross_water(e)
        elif cmd=="f": camp(e)
        elif cmd=="d": rest(e)
        elif cmd=="e": eat(e)
        elif cmd=="b": drink(e)
        elif cmd=="i": print("\nInventário: "+(", ".join(get(e,"inventario",[])) or "vazio")+"\nMarcas: "+", ".join(sorted(get(e,"flags",set()))[-6:]))
        elif cmd=="q": print("Você interrompe a exploração e procura um lugar para reorganizar os pensamentos."); return "00_despertar_eldorwood"
        else: print("Comando desconhecido. A neblina continua fechando caminhos.")
    print("\nVocê sucumbe em Eldorwood."); return "fim_derrota"

