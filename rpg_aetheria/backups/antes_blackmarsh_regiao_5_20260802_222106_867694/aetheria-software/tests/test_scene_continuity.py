from __future__ import annotations

import json
import heapq
import math
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2] / "frostreach-100-ramificacoes"


class SceneContinuityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = json.loads((PACKAGE / "00_despertar_frostreach.json").read_text(encoding="utf-8"))
        cls.scenes = json.loads((PACKAGE / "frostreach_fase_inicial_100.json").read_text(encoding="utf-8"))
        cls.all_scenes = [cls.root, *cls.scenes]

    def test_all_choices_and_test_results_have_transitions(self) -> None:
        choices = 0
        paths = 0
        transitions = 0
        for scene in self.all_scenes:
            for option in scene.get("opcoes", []):
                choices += 1
                test = option.get("teste")
                if test:
                    paths += 2
                    transitions += bool(test.get("transicao_sucesso"))
                    transitions += bool(test.get("transicao_falha"))
                else:
                    paths += 1
                    transitions += bool(option.get("transicao"))
        self.assertEqual(len(self.all_scenes), 100)
        self.assertEqual(choices, 300)
        self.assertEqual(paths, 399)
        self.assertEqual(transitions, paths)

    def test_editorial_repetition_and_literal_newlines_were_removed(self) -> None:
        for scene in self.all_scenes:
            text = scene.get("texto", "")
            self.assertNotIn("Para alguém que chegou sem memória", text)
            self.assertNotIn("\\n", text)

    def test_every_destination_is_known_or_a_declared_continuation(self) -> None:
        ids = {scene["id"] for scene in self.all_scenes}
        external = {"04_decisao_de_caminho"}
        missing = []
        for scene in self.all_scenes:
            for option in scene.get("opcoes", []):
                test = option.get("teste")
                destinations = (
                    [test.get("destino_sucesso"), test.get("destino_falha")]
                    if test else [option.get("destino")]
                )
                for destination in destinations:
                    if destination and destination not in ids | external:
                        missing.append((scene["id"], destination))
        self.assertEqual(missing, [])

    def test_tovin_route_is_causally_connected(self) -> None:
        by_id = {scene["id"]: scene for scene in self.all_scenes}
        boat = by_id["fr1_c08_barco_de_tovin"]
        self.assertIn("Tovin", boat["opcoes"][0]["transicao"])
        shadow = by_id["fr1_c09_sombra_no_fiorde"]
        self.assertIn("Tovin", shadow["texto"])
        self.assertIn("Serpente-Marinha", shadow["texto"])

    def test_every_internal_story_path_has_a_journey(self) -> None:
        missing = []
        for scene in self.scenes:
            for index, option in enumerate(scene.get("opcoes", []), 1):
                test = option.get("teste")
                if test:
                    for result in ("sucesso", "falha"):
                        destination = test.get(f"destino_{result}")
                        if destination and destination.startswith("fr1_") and not test.get(f"jornada_{result}"):
                            missing.append((scene["id"], index, result))
                else:
                    destination = option.get("destino")
                    if destination and destination.startswith("fr1_") and not option.get("jornada"):
                        missing.append((scene["id"], index, "direto"))
        self.assertEqual(missing, [])

    def test_old_hour_jumps_were_replaced_by_minute_actions(self) -> None:
        old_time_effects = []
        minute_effects = 0
        for scene in self.scenes:
            for option in scene.get("opcoes", []):
                groups = [option.get("efeitos") or []]
                test = option.get("teste") or {}
                groups.extend((test.get("efeitos_sucesso") or [], test.get("efeitos_falha") or []))
                for effect in (effect for group in groups for effect in group):
                    if effect.get("tipo") == "tempo":
                        old_time_effects.append((scene["id"], effect))
                    minute_effects += effect.get("tipo") == "tempo_minutos"
        self.assertEqual(old_time_effects, [])
        self.assertEqual(minute_effects, 396)

    def test_three_spawn_routes_are_parallel_not_a_continental_sequence(self) -> None:
        edges = []
        for scene in self.scenes:
            for option in scene.get("opcoes", []):
                test = option.get("teste")
                if test:
                    destinations = (test.get("destino_sucesso"), test.get("destino_falha"))
                else:
                    destinations = (option.get("destino"),)
                edges.extend((scene["id"], destination) for destination in destinations if destination)
        coast_to_plateau = [(a, b) for a, b in edges if a.startswith("fr1_c") and b.startswith("fr1_p")]
        plateau_to_mountain = [(a, b) for a, b in edges if a.startswith("fr1_p") and b.startswith("fr1_m")]
        self.assertEqual(coast_to_plateau, [])
        self.assertEqual(plateau_to_mountain, [])
        for final_origin in ("fr1_c20_estrada_de_sal", "fr1_p20_portao_do_interior", "fr1_m20_descida_das_presas"):
            self.assertTrue(any(a == final_origin and b.startswith("fr1_v") for a, b in edges))

    def test_shortest_story_routes_span_at_least_a_month_at_eight_hours_per_day(self) -> None:
        by_id = {scene["id"]: scene for scene in self.scenes}
        speeds = {"c": 1.8, "p": 2.4, "m": 1.2, "v": 1.8, "q": 1.8, "f": 1.8}

        def shortest_hours(start: str) -> float:
            visited = set()
            queue = [(0, start)]
            while queue:
                elapsed, scene_id = heapq.heappop(queue)
                if scene_id in visited:
                    continue
                visited.add(scene_id)
                if scene_id == "fr1_f09_inicio_da_historia":
                    return elapsed / 60
                family = scene_id.split("_")[1][0]
                for option in by_id[scene_id].get("opcoes", []):
                    decision_minutes = sum(
                        effect.get("valor", 0)
                        for effect in option.get("efeitos", [])
                        if effect.get("tipo") == "tempo_minutos"
                    )
                    test = option.get("teste")
                    if test:
                        paths = []
                        for result in ("sucesso", "falha"):
                            extra = sum(
                                effect.get("valor", 0)
                                for effect in test.get(f"efeitos_{result}", [])
                                if effect.get("tipo") == "tempo_minutos"
                            )
                            paths.append((
                                test.get(f"destino_{result}"),
                                test.get(f"jornada_{result}"),
                                decision_minutes + extra,
                            ))
                    else:
                        paths = [(option.get("destino"), option.get("jornada"), decision_minutes)]
                    for destination, journey, action_minutes in paths:
                        if destination not in by_id or not journey:
                            continue
                        travel_hours = max(
                            math.ceil(journey["distancia_km"] / speeds[family]),
                            math.ceil(journey["minutos_minimos"] / 60),
                        )
                        heapq.heappush(queue, (elapsed + action_minutes + travel_hours * 60, destination))
            raise AssertionError(f"Rota sem acesso ao final: {start}")

        starts = [option["destino"] for option in self.root["opcoes"]]
        route_hours = {start: shortest_hours(start) for start in starts}
        self.assertGreaterEqual(min(route_hours.values()), 30 * 8)
        self.assertGreater(max(route_hours.values()), min(route_hours.values()))


if __name__ == "__main__":
    unittest.main()
