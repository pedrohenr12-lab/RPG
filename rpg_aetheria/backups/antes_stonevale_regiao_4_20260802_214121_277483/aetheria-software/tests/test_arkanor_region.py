from __future__ import annotations

import json
import math
import random
import unittest
from pathlib import Path

from aetheria_app.core import PersistentCore
from aetheria_app.core.runtime import ARKANOR_ROOT_QUEST
from aetheria_app.arkanor_content import (
    ARKANOR_NPCS,
    ARKANOR_SETTLEMENTS,
)
from aetheria_app.models import PlayerSession
from aetheria_app.procedural_exploration import ProceduralExploration, REGION_MAPS


SOFTWARE_ROOT = Path(__file__).resolve().parents[1]
SCENES_ROOT = SOFTWARE_ROOT.parent / "data" / "scenes"


def load_scenes() -> dict[str, dict]:
    scenes: dict[str, dict] = {}
    for path in SCENES_ROOT.glob("*.json"):
        raw = json.loads(path.read_text(encoding="utf-8"))
        entries = raw if isinstance(raw, list) else [raw]
        for scene in entries:
            scenes[scene["id"]] = scene
    return scenes


def session(region: str = "arkanor") -> PlayerSession:
    return PlayerSession(
        name="Teste",
        race_slug="humanos",
        race_name="Humanos",
        region_slug=region,
        scene_id="00_despertar_arkanor_planicies",
        life_max=20,
        attack=4,
        defense=2,
        mana_max=10,
        speed=5,
        critical=0.10,
        biome_slug="planicies_ferteis" if region == "arkanor" else "pantanos_rios",
    )


class LastChoiceRandom(random.Random):
    def random(self) -> float:
        return 0.0

    def choices(self, population, weights=None, *, cum_weights=None, k=1):
        return ["npc"] * k if "npc" in population else [population[-1]] * k


class QuietRandom(random.Random):
    def random(self) -> float:
        return 0.99


class ArkanorContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scenes = load_scenes()
        cls.arkanor = {
            scene_id: scene
            for scene_id, scene in cls.scenes.items()
            if scene.get("meta", {}).get("regiao") == "arkanor"
        }

    def test_region_has_143_scenes_and_429_visible_choices(self) -> None:
        self.assertEqual(len(self.arkanor), 143)
        self.assertEqual(sum(len(scene["opcoes"]) for scene in self.arkanor.values()), 429)
        self.assertTrue(all(len(scene["opcoes"]) == 3 for scene in self.arkanor.values()))

    def test_all_destinations_and_test_outcomes_exist(self) -> None:
        missing = []
        for scene in self.arkanor.values():
            for option in scene["opcoes"]:
                candidates = [option.get("destino")]
                test = option.get("teste") or {}
                candidates.extend((test.get("destino_sucesso"), test.get("destino_falha")))
                missing.extend(destination for destination in candidates if destination and destination not in self.scenes)
        self.assertEqual(missing, [])

    def test_content_is_divided_between_wilderness_cities_main_story_and_relationships(self) -> None:
        phases: dict[str, int] = {}
        for scene in self.arkanor.values():
            phase = scene.get("meta", {}).get("fase")
            phases[phase] = phases.get(phase, 0) + 1
        self.assertEqual(phases["nascimento"], 3)
        self.assertEqual(phases["exploracao_inicial"], 60)
        self.assertEqual(phases["vida_urbana"], 50)
        self.assertEqual(phases["ancora_medida"], 18)
        self.assertEqual(phases["relacao"], 12)

    def test_every_spatial_settlement_has_a_real_entry_scene(self) -> None:
        entries = {settlement["scene_id"] for settlement in ARKANOR_SETTLEMENTS}
        self.assertEqual(len(entries), 11)
        self.assertTrue(entries <= self.scenes.keys())

    def test_all_fifteen_intelligent_races_are_represented_by_persistent_npcs(self) -> None:
        races = {npc["race"] for npc in ARKANOR_NPCS}
        expected = {
            "Humana", "Sylvani", "Aureli", "Aquari", "Solari", "Glacari", "Luminari",
            "Kragari", "Ziraki", "Ninfari", "Umbrari", "Ferrari", "Drakari", "Ethari", "Voraki",
        }
        self.assertEqual(races, expected)

    def test_narratives_have_real_newlines_and_no_old_repeated_sentence(self) -> None:
        combined = "\n".join(scene["texto"] for scene in self.arkanor.values())
        self.assertNotIn("\\n", combined)
        self.assertNotIn("Para alguém que chegou sem memória", combined)
        self.assertNotIn("nenhuma escolha é tratada como decoração", combined.lower())

    def test_slow_pacing_is_encoded_in_city_relationship_and_main_quest_actions(self) -> None:
        for scene in self.arkanor.values():
            phase = scene.get("meta", {}).get("fase")
            if phase in {"vida_urbana", "relacao"}:
                for option in scene["opcoes"]:
                    effects = option.get("efeitos") or []
                    self.assertTrue(
                        option.get("modo") == "exploracao_livre"
                        or any(effect.get("tipo") == "tempo_minutos" for effect in effects),
                        f"ação instantânea em {scene['id']}",
                    )
            if phase == "ancora_medida" and int(scene["meta"]["capitulo"]) < 16:
                for option in scene["opcoes"]:
                    self.assertTrue(
                        option.get("modo") == "exploracao_livre" or option.get("jornada"),
                        f"capítulo principal sem viagem real em {scene['id']}",
                    )


class ArkanorSpatialTests(unittest.TestCase):
    def test_scripted_journey_changes_real_coordinates(self) -> None:
        player = session()
        player.position_x = 0.0
        player.position_y = 1500.0
        game = ProceduralExploration(player, rng=QuietRandom(1))
        game.queue_story_journey(
            "r3_p02_canal_de_botanium",
            "A observação terminou.",
            "seguir ao norte",
            {"distancia_km": 3.4, "minutos_minimos": 120, "direcao": "norte"},
        )
        game.choose("journey:normal")
        self.assertGreater(player.position_y, 1500.0)
        self.assertEqual(player.position_x, 0.0)
        stored = player.exploration["coordinates_by_region"]["arkanor"]
        self.assertAlmostEqual(stored["y"], player.position_y, places=3)

    def test_arkanor_to_eldorwood_border_is_physical_and_optional(self) -> None:
        player = session()
        player.biome_slug = "planicies_ferteis"
        player.position_x = 450.0
        player.position_y = 2999.2
        game = ProceduralExploration(player, rng=QuietRandom(2))
        turn = game.choose("travel:norte")
        self.assertIn("border:cross", {choice["id"] for choice in turn.choices})
        self.assertEqual(player.region_slug, "arkanor")
        crossed = game.choose("border:cross")
        self.assertEqual(player.region_slug, "eldorwood")
        self.assertEqual(player.biome_slug, "pantanos_rios")
        self.assertIn("atravessou_arkanor_eldorwood", player.flags)
        self.assertIn("Eldorwood", crossed.narrative)

    def test_eldorwood_to_arkanor_border_is_also_physical(self) -> None:
        player = session("eldorwood")
        player.position_x = 430.0
        player.position_y = -1599.7
        game = ProceduralExploration(player, rng=QuietRandom(3))
        turn = game.choose("travel:sul")
        self.assertIn("border:cross", {choice["id"] for choice in turn.choices})
        game.choose("border:cross")
        self.assertEqual(player.region_slug, "arkanor")
        self.assertEqual(player.biome_slug, "planicies_ferteis")

    def test_spawn_biome_changes_distance_to_eldorwood(self) -> None:
        spawns = REGION_MAPS["arkanor"]["spawns"]
        minimum_distances = {
            biome: min(3000.0 - y for x, y in points if -1100.0 <= x <= 1600.0)
            for biome, points in spawns.items()
            if any(-1100.0 <= x <= 1600.0 for x, y in points)
        }
        self.assertLess(minimum_distances["planicies_ferteis"], 1000.0)
        self.assertGreater(minimum_distances["vales_verdes"], 2500.0)
        self.assertGreater(
            minimum_distances["vales_verdes"],
            minimum_distances["planicies_ferteis"] + 1500.0,
        )

    def test_road_can_generate_travelers_but_not_teleport_to_a_distant_city(self) -> None:
        player = session()
        player.position_x = 0.0
        player.position_y = 1180.0
        game = ProceduralExploration(player, rng=LastChoiceRandom(4))
        self.assertTrue(game._near_civilization())
        event = game._roll_interruption(1.0, "norte", near_civilization=True)
        self.assertIsNotNone(event)
        self.assertEqual(event["kind"], "npc")

    def test_relationships_persist_across_region_crossing(self) -> None:
        player = session()
        core = PersistentCore(player, {})
        core.relationships.apply(
            "liora_sen",
            {"trust": 70, "respect": 50, "warmth": 50},
            reason="jornada compartilhada",
            name="Liora Sen",
        )
        game = ProceduralExploration(player, relationships=core.relationships, rng=QuietRandom(5))
        player.position_x = 450.0
        player.position_y = 2999.2
        player.biome_slug = "planicies_ferteis"
        game.state["biome"] = "planicies_ferteis"
        game.choose("travel:norte")
        game.choose("border:cross")
        record = core.relationships.get("liora_sen")
        self.assertEqual(record["status"], "devoted")
        self.assertEqual(player.region_slug, "eldorwood")
        json.dumps(player.to_dict(), ensure_ascii=False)

    def test_ignored_primary_story_advances_without_the_player(self) -> None:
        player = session()
        definitions = {
            ARKANOR_ROOT_QUEST: {
                "id": ARKANOR_ROOT_QUEST,
                "title": "O manuscrito lê você",
                "category": "primary_optional",
                "stages": [],
            }
        }
        core = PersistentCore(player, definitions)
        core.enter_scene("r3_q01_manuscrito_le_voce")
        self.assertEqual(core.quests.get(ARKANOR_ROOT_QUEST)["status"], "rumored")
        core.record_choice(
            scene_id="r3_q01_manuscrito_le_voce",
            option_text="Registrar o rumor e voltar à exploração",
            destination=None,
            result_key="success",
        )
        core.clock.advance(4 * 24 * 60)
        core.process_due_events()
        quest = core.quests.get(ARKANOR_ROOT_QUEST)
        self.assertEqual(quest["status"], "transformed")
        self.assertEqual(quest["outcome"], "conclave_secures_fragment")
        self.assertEqual(core.world.get("arkanor.ancora_medida.world_progress"), "fragment_secured_by_conclave")

    def test_primary_story_does_not_advance_without_player_after_acceptance(self) -> None:
        player = session()
        definitions = {
            ARKANOR_ROOT_QUEST: {
                "id": ARKANOR_ROOT_QUEST,
                "title": "O manuscrito lê você",
                "category": "primary_optional",
                "stages": [],
            }
        }
        core = PersistentCore(player, definitions)
        core.enter_scene("r3_q01_manuscrito_le_voce")
        core.record_choice(
            scene_id="r3_q01_manuscrito_le_voce",
            option_text="Observar sem tocar durante uma hora",
            destination="r3_q02_quatro_leituras",
            result_key="success",
        )
        core.clock.advance(4 * 24 * 60)
        core.process_due_events()
        self.assertEqual(core.quests.get(ARKANOR_ROOT_QUEST)["status"], "active")
        self.assertFalse(core.world.has("arkanor.ancora_medida.world_progress"))


if __name__ == "__main__":
    unittest.main()
