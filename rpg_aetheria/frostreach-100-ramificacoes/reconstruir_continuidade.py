"""Remove o texto repetido e cria transições causais para todas as 300 escolhas."""
from __future__ import annotations

import json
import re
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT_FILE = PACKAGE / "00_despertar_frostreach.json"
SCENES_FILE = PACKAGE / "frostreach_fase_inicial_100.json"


NARRATIVE_OVERRIDES = {
    "fr1_c09_sombra_no_fiorde": (
        "As botas terminam junto a uma placa quebrada. Tovin e uma pescadora Aquari se agarram à borda enquanto "
        "a água escura se move contra a corrente. Um corpo comprido circula o barco e toca o gelo por baixo, "
        "produzindo rachaduras em sequência. Pela crista dorsal e pela névoa que sai de sua boca, pode ser uma "
        "Serpente-Marinha de Gelo; lutar dentro do fiorde seria aceitar o terreno escolhido por ela."
    ),
    "fr1_c10_colheita_de_alga": (
        "Sob uma placa transparente existe um jardim de Alga-de-Gelo. Os Aquari usam ganchos sem ponta para "
        "separar apenas as folhas maduras: parte servirá de alimento, parte neutraliza o frio deixado pelo veneno "
        "da serpente. Uma faixa inteira da colônia, porém, perdeu a cor. O dano forma um arco que aponta para águas "
        "mais profundas, como se alguma vibração estivesse afastando a vida."
    ),
    "fr1_c11_ave_aurora": (
        "Enquanto o barco e os feridos são conduzidos para terreno firme, uma Ave-Aurora acompanha o grupo. "
        "Ela não voa ao acaso: repete três círculos sobre o remo ensanguentado e depois segue a costa. Uma pena "
        "azul-prateada cai sobre o gelo e vibra no mesmo ritmo das escamas encontradas no casco de Tovin."
    ),
    "fr1_c12_canto_da_baleia": (
        "A rota indicada pela ave termina numa enseada de pedras negras. Ali, um canto grave atravessa água, gelo e "
        "ossos. As notas repetem o intervalo observado nos ataques da serpente e fazem a pena da Ave-Aurora girar. "
        "Uma Baleia-de-Gelo emerge longe da margem, mas a vibração também responde de dentro da falésia."
    ),
}


# Transições autorais para o arco de Tovin mostrado durante o teste do jogador.
OVERRIDES: dict[tuple[str, int, str], str] = {
    ("fr1_c06_fumaca_brumafiorde", 1, "direct"): (
        "Você desce a encosta com as mãos abertas. A fumaça vem de um corte no gelo onde três moradores recolhem "
        "uma rede; eles interrompem o trabalho quando percebem que você não reconhece a costa nem suas palavras."
    ),
    ("fr1_c06_fumaca_brumafiorde", 2, "success"): (
        "Escondido pelo relevo, você conta três pescadores, um barco vazio e marcas de pressa. Ao contornar o grupo, "
        "encontra a embarcação presa entre placas antes que os moradores notem sua presença."
    ),
    ("fr1_c06_fumaca_brumafiorde", 2, "failure"): (
        "Uma rajada muda a direção da fumaça e revela sua silhueta. Os pescadores largam a rede e o cercam a uma "
        "distância segura, obrigando uma apresentação imediata."
    ),
    ("fr1_c06_fumaca_brumafiorde", 3, "direct"): (
        "Coberto com Musgo-de-Fiorde, você evita o grupo, mas chega perto demais da água. As marcas furtivas "
        "terminam quando uma sombra grande altera a corrente sob o gelo."
    ),
    ("fr1_c07_redes_aquari", 1, "direct"): (
        "Você segura a corda da rede e admite que não sabe onde está. A franqueza reduz a desconfiança; em troca da "
        "ajuda, a Northariana conta que Tovin desapareceu. O grupo conduz você até o pequeno barco que voltou sem ele."
    ),
    ("fr1_c07_redes_aquari", 2, "success"): (
        "Sua pergunta toca no perigo certo. Uma Aquari mostra pegadas que saem do barco e atravessam a plataforma. "
        "Vocês as seguem até uma placa quebrada, onde sobreviventes tentam não chamar a atenção do que circula abaixo."
    ),
    ("fr1_c07_redes_aquari", 2, "failure"): (
        "A pergunta direta parece uma tentativa de esconder sua própria história. Antes de confiar em você, os "
        "moradores exigem que examine a única prova disponível: o barco de Tovin, preso adiante entre as placas."
    ),
    ("fr1_c07_redes_aquari", 3, "direct"): (
        "Você aceita puxar redes em troca de comida. O trabalho seguinte exige abrir um corte seguro no gelo e colher "
        "a Alga-de-Gelo que sustenta pescadores durante as marés longas."
    ),
    ("fr1_c08_barco_de_tovin", 1, "direct"): (
        "Você segue as botas enquanto os sulcos ainda têm bordas. Elas cruzam o fiorde e terminam junto a uma placa "
        "quebrada: Tovin e outra pescadora estão presos acima de uma sombra que nada contra a corrente."
    ),
    ("fr1_c08_barco_de_tovin", 2, "success"): (
        "As escamas conservam um veneno de frio interno. Comparando cheiro e cor, você conclui que a Alga-de-Gelo "
        "pode retardá-lo; os pescadores abrem uma placa transparente e revelam a colônia usada como antídoto."
    ),
    ("fr1_c08_barco_de_tovin", 2, "failure"): (
        "A escama se parte e libera névoa sobre sua mão. Antes que consiga terminar o antídoto, impactos ritmados "
        "sacodem o casco; a criatura responsável ainda circula sob o gelo."
    ),
    ("fr1_c08_barco_de_tovin", 3, "direct"): (
        "Você prende uma corda ao barco e retorna com reforços. Durante o arrasto, uma Ave-Aurora circula o remo "
        "ensanguentado e deixa cair uma pena que vibra como as escamas no casco — a primeira pista que aponta além da vila."
    ),
    ("fr1_c09_sombra_no_fiorde", 1, "direct"): (
        "Os peixes desviam a serpente pelo tempo necessário. Tovin é retirado com marcas azuladas no braço; para "
        "impedir que o frio avance por suas veias, os Aquari levam todos até uma colônia de Alga-de-Gelo."
    ),
    ("fr1_c09_sombra_no_fiorde", 2, "success"): (
        "Você calcula a sequência das rachaduras e cruza pelas placas que acabaram de liberar pressão. Na margem, "
        "uma Ave-Aurora repete círculos sobre o remo de Tovin, como se seguisse o mesmo pulso da criatura."
    ),
    ("fr1_c09_sombra_no_fiorde", 2, "failure"): (
        "A placa escolhida inclina antes do último passo. Você rompe a camada superficial e cai sobre um jardim de "
        "algas; os pescadores o retiram usando os mesmos ganchos empregados na colheita."
    ),
    ("fr1_c09_sombra_no_fiorde", 3, "direct"): (
        "Imóvel, você percebe que os ataques obedecem a intervalos sonoros. Quando um canto grave percorre o fiorde, "
        "a serpente interrompe o círculo e mergulha; a origem do som está além das pedras negras."
    ),
    ("fr1_c10_colheita_de_alga", 1, "direct"): (
        "Você aprende a cortar somente folhas maduras e ajuda a estabilizar os feridos. Quando o trabalho termina, "
        "uma Ave-Aurora pousa sobre os ganchos e reage às escamas trazidas do barco."
    ),
    ("fr1_c10_colheita_de_alga", 2, "success"): (
        "A faixa morta não foi comida nem envenenada: as células se romperam por vibração. Seguindo o arco do dano, "
        "você chega a pedras onde o canto de uma Baleia-de-Gelo atravessa a plataforma."
    ),
    ("fr1_c10_colheita_de_alga", 2, "failure"): (
        "A maré cobre suas medições antes de uma conclusão segura. Ao recuar, você nota uma Ave-Aurora repetindo "
        "sobre a área pálida o mesmo desenho que tentou registrar."
    ),
    ("fr1_c10_colheita_de_alga", 3, "direct"): (
        "Com alimento suficiente, você ajuda a fechar o corte no gelo. A rede prende uma tábua marcada por letras "
        "antigas; seguindo outros fragmentos, o grupo localiza um naufrágio que a maré vinha desenterrando."
    ),
    ("fr1_c11_ave_aurora", 1, "direct"): (
        "Você acompanha a ave por enseadas sucessivas. Ela pousa onde a rocha vibra, segundos antes de um canto "
        "profundo atravessar o fiorde e alterar a direção de toda a fauna ao redor."
    ),
    ("fr1_c11_ave_aurora", 2, "success"): (
        "Ao registrar o voo, você percebe que os círculos apontam para madeiras sob o gelo. A pena ilumina inscrições "
        "num casco antigo, revelando um naufrágio escondido pela maré."
    ),
    ("fr1_c11_ave_aurora", 2, "failure"): (
        "O vento apaga parte do desenho antes que termine. A ave abandona a margem quando um canto subterrâneo faz "
        "a placa vibrar; resta seguir o som em vez do voo."
    ),
    ("fr1_c11_ave_aurora", 3, "direct"): (
        "Você leva a pena aos anciãos. Antes de chegar à casa do conselho, reconhece o mesmo brilho vazando de "
        "caixotes descarregados às escondidas — Luminite que não aparece nos registros da vila."
    ),
}


# Costa, Planalto e Presas são três origens paralelas. A versão antiga ligava
# uma à outra em série, comprimindo milhões de quilômetros em poucas horas.
DESTINATION_OVERRIDES: dict[tuple[str, int, str], str] = {
    ("fr1_c18_flor_da_baixa_mar", 3, "direct"): "fr1_c19_conselho_brumafiorde",
    ("fr1_c19_conselho_brumafiorde", 2, "success"): "fr1_c20_estrada_de_sal",
    ("fr1_c19_conselho_brumafiorde", 3, "direct"): "fr1_c20_estrada_de_sal",
    ("fr1_c20_estrada_de_sal", 1, "direct"): "fr1_v01_portao_stonhelm",
    ("fr1_c20_estrada_de_sal", 2, "success"): "fr1_v02_registro_do_estrangeiro",
    ("fr1_c20_estrada_de_sal", 2, "failure"): "fr1_v01_portao_stonhelm",
    ("fr1_c20_estrada_de_sal", 3, "direct"): "fr1_v03_taverna_tres_bussolas",
    ("fr1_p18_circulo_symmetrium", 3, "direct"): "fr1_p19_longa_noite",
    ("fr1_p19_longa_noite", 2, "success"): "fr1_p20_portao_do_interior",
    ("fr1_p19_longa_noite", 3, "direct"): "fr1_p20_portao_do_interior",
    ("fr1_p20_portao_do_interior", 1, "direct"): "fr1_v01_portao_stonhelm",
    ("fr1_p20_portao_do_interior", 2, "success"): "fr1_v02_registro_do_estrangeiro",
    ("fr1_p20_portao_do_interior", 2, "failure"): "fr1_v01_portao_stonhelm",
    ("fr1_p20_portao_do_interior", 3, "direct"): "fr1_v03_taverna_tres_bussolas",
}


JOURNEY_OVERRIDES: dict[tuple[str, int, str], tuple[float, int]] = {
    ("fr1_c06_fumaca_brumafiorde", 1, "direct"): (0.8, 25),
    ("fr1_c07_redes_aquari", 1, "direct"): (1.4, 40),
    ("fr1_c07_redes_aquari", 3, "direct"): (0.3, 30),
    ("fr1_c08_barco_de_tovin", 1, "direct"): (1.8, 50),
    ("fr1_c08_barco_de_tovin", 2, "success"): (0.4, 25),
    ("fr1_c08_barco_de_tovin", 2, "failure"): (0.2, 10),
    ("fr1_c08_barco_de_tovin", 3, "direct"): (4.0, 150),
    ("fr1_c09_sombra_no_fiorde", 1, "direct"): (1.2, 45),
    ("fr1_c09_sombra_no_fiorde", 2, "success"): (2.5, 70),
    ("fr1_c09_sombra_no_fiorde", 2, "failure"): (0.2, 15),
    ("fr1_c09_sombra_no_fiorde", 3, "direct"): (3.5, 100),
}


def clean_text(text: str) -> str:
    text = text.replace("\\r\\n", "\n").replace("\\n", "\n")
    # Todas as 99 cenas antigas possuíam um segundo parágrafo editorial idêntico
    # dentro de cada bloco. A narrativa autoral é o primeiro parágrafo.
    return text.split("\n\n", 1)[0].strip()


def split_opening(text: str) -> tuple[str, str]:
    match = re.search(r"(?<=[.!?])\s+", text)
    if not match:
        return text, text
    return text[: match.start()].strip(), text[match.end() :].strip()


def lower_first(text: str) -> str:
    return text[:1].lower() + text[1:] if text else text


def family_and_index(scene_id: str) -> tuple[str, int]:
    match = re.match(r"fr1_([cpmvqf])(\d+)_", scene_id)
    return (match.group(1), int(match.group(2))) if match else ("x", 0)


def journey_for(source: str, destination: str, choice_index: int, result: str) -> dict:
    override = JOURNEY_OVERRIDES.get((source, choice_index, result))
    source_family, source_index = family_and_index(source)
    target_family, target_index = family_and_index(destination)
    if override:
        distance, minimum = override
    elif source_family == target_family and source_family in {"c", "p", "m"}:
        gap = max(1, abs(target_index - source_index))
        distance = (3.5 + gap * 2.8 + (choice_index - 1) * 0.7) * 1.8
        minimum = 30 + gap * 20
    elif source_family == target_family == "v":
        gap = max(1, abs(target_index - source_index))
        distance = 0.6 + gap * 0.7
        minimum = 25 + gap * 20
    elif source_family == target_family == "q":
        gap = max(1, abs(target_index - source_index))
        distance = (6.0 + gap * 3.5) * 1.8
        minimum = 90 + gap * 45
    elif source_family == target_family == "f":
        gap = max(1, abs(target_index - source_index))
        distance = 0.5 + gap * 0.8
        minimum = 30 + gap * 25
    elif target_family == "v":
        distance = (28.0 + choice_index * 9.0) * 1.8
        minimum = 8 * 60
    elif source_family == "v" and target_family == "q":
        distance = (35.0 + choice_index * 8.0) * 1.8
        minimum = 10 * 60
    elif source_family == "q" and target_family == "f":
        distance = (18.0 + choice_index * 5.0) * 1.5
        minimum = 5 * 60
    else:
        distance = 2.0 + choice_index
        minimum = 45
    terrain = {
        "c": "orla_costeira_gelo", "p": "planalto_central_frostreach",
        "m": "presas_de_gelo",
    }.get(target_family, "rota_habitada" if target_family in {"v", "f"} else "desconhecido")
    return {
        "distancia_km": round(distance, 1),
        "minutos_minimos": int(minimum),
        "terreno": terrain,
        "perto_civilizacao": target_family in {"v", "f"},
    }


def convert_time_effects(effects: list[dict], choice_index: int) -> None:
    for effect in effects:
        if effect.get("tipo") == "tempo":
            old_hours = max(1, int(effect.get("valor", 1)))
            effect["tipo"] = "tempo_minutos"
            effect["valor"] = 10 + choice_index * 5 + (old_hours - 1) * 15


def generated_transition(decision: str, opening: str, result: str, variant: int) -> str:
    decision = lower_first(decision.strip().rstrip("."))
    if result == "success":
        templates = (
            "Você consegue {decision}. O sucesso abre uma possibilidade que antes não existia. {opening}",
            "O teste confirma sua leitura: você consegue {decision}. {opening}",
            "A decisão de {decision} supera o risco imediato. {opening}",
            "Você executa o plano de {decision} antes que as condições mudem. {opening}",
        )
        return templates[variant % len(templates)].format(decision=decision, opening=opening)
    if result == "failure":
        templates = (
            "Você tenta {decision}, mas o plano falha e cobra o custo registrado. {opening}",
            "A decisão de {decision} encontra um obstáculo que você não previu. {opening}",
            "Você não consegue {decision} da forma planejada; a falha muda sua chegada. {opening}",
            "O risco vence sua tentativa de {decision}, obrigando uma rota pior. {opening}",
        )
        return templates[variant % len(templates)].format(decision=decision, opening=opening)
    templates = (
        "Você decide {decision}. {opening}",
        "Depois de avaliar o risco, você resolve {decision}. {opening}",
        "Sua escolha é {decision}; o tempo e o esforço da ação permanecem. {opening}",
        "Você age antes que a situação mude: {decision}. {opening}",
    )
    return templates[variant % len(templates)].format(decision=decision, opening=opening)


def main() -> None:
    root = json.loads(ROOT_FILE.read_text(encoding="utf-8"))
    scenes = json.loads(SCENES_FILE.read_text(encoding="utf-8"))
    by_id = {root["id"]: root, **{scene["id"]: scene for scene in scenes}}

    root["texto"] = root["texto"].replace("\\r\\n", "\n").replace("\\n", "\n")
    for scene in scenes:
        scene["texto"] = NARRATIVE_OVERRIDES.get(scene["id"], clean_text(scene["texto"]))

    openings: dict[str, str] = {}
    for scene in scenes:
        opening, continuation = split_opening(scene["texto"])
        openings[scene["id"]] = opening
        scene["texto_continuacao"] = continuation or scene["texto"]

    all_scenes = [root, *scenes]
    for scene in all_scenes:
        for index, option in enumerate(scene.get("opcoes", []), start=1):
            decision = option.get("texto", "continuar")
            variant = sum(ord(char) for char in scene["id"]) + index
            test = option.get("teste")
            if test:
                for result in ("success", "failure"):
                    pt = "sucesso" if result == "success" else "falha"
                    override_destination = DESTINATION_OVERRIDES.get((scene["id"], index, result))
                    if override_destination:
                        test[f"destino_{pt}"] = override_destination
                    destination = test.get(f"destino_{pt}") or option.get("destino")
                    opening = openings.get(destination, "O território se abre numa direção ainda sem nome.")
                    test[f"transicao_{pt}"] = OVERRIDES.get(
                        (scene["id"], index, result),
                        generated_transition(decision, opening, result, variant),
                    )
                    if destination in by_id:
                        test[f"jornada_{pt}"] = journey_for(scene["id"], destination, index, result)
                    convert_time_effects(test.get(f"efeitos_{pt}", []), index)
            else:
                override_destination = DESTINATION_OVERRIDES.get((scene["id"], index, "direct"))
                if override_destination:
                    option["destino"] = override_destination
                destination = option.get("destino") or option.get("destination_key")
                opening = openings.get(destination, "O território se abre numa direção ainda sem nome.")
                option["transicao"] = OVERRIDES.get(
                    (scene["id"], index, "direct"),
                    generated_transition(decision, opening, "direct", variant),
                )
                if destination in by_id:
                    option["jornada"] = journey_for(scene["id"], destination, index, "direct")
            convert_time_effects(option.get("efeitos", []), index)

    ROOT_FILE.write_text(json.dumps(root, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SCENES_FILE.write_text(json.dumps(scenes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Continuidade reconstruída: {len(all_scenes)} cenas.")


if __name__ == "__main__":
    main()
