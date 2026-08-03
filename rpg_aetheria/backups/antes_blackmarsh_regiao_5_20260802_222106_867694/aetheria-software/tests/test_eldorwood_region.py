from __future__ import annotations

import json
import math
import random
import unittest
from pathlib import Path

from aetheria_app.core import PersistentCore
from aetheria_app.core.runtime import ELDORWOOD_ROOT_QUEST
from aetheria_app.eldorwood_content import (
    ELDORWOOD_NPCS,
    ELDORWOOD_SETTLEMENTS,
    REGION_MAPS,
)
from aetheria_app.models import PlayerSession
from aetheria_app.procedural_exploration import ProceduralExploration


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


def session(region: str = "eldorwood") -> PlayerSession:
    return PlayerSession(
        name="Teste",
        race_slug="humanos",
        race_name="Humanos",
        region_slug=region,
        scene_id="00_despertar_eldorwood_floresta",
        life_max=20,
        attack=4,
        defense=2,
        mana_max=10,
        speed=5,
        critical=0.10,
        biome_slug="floresta_densa_antiga" if region == "eldorwood" else "planalto_central_frostreach",
    )


class LastChoiceRandom(random.Random):
    def random(self) -> float:
        return 0.0

    def choices(self, population, weights=None, *, cum_weights=None, k=1):
        return [population[-1]] * k


class QuietRandom(random.Random):
    def random(self) -> float:
        return 0.99


class EldorwoodContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scenes = load_scenes()
        cls.eldorwood = {
            scene_id: scene
            for scene_id, scene in cls.scenes.items()
            if scene.get("meta", {}).get("regiao") == "eldorwood"
        }

    def test_region_has_143_scenes_and_429_visible_choices(self) -> None:
        self.assertEqual(len(self.eldorwood), 143)
        self.assertEqual(sum(len(scene["opcoes"]) for scene in self.eldorwood.values()), 429)
        self.assertTrue(all(len(scene["opcoes"]) == 3 for scene in self.eldorwood.values()))

    def test_all_destinations_and_test_outcomes_exist(self) -> None:
        missing = []
        for scene in self.eldorwood.values():
            for option in scene["opcoes"]:
                candidates = [option.get("destino")]
                test = option.get("teste") or {}
                candidates.extend((test.get("destino_sucesso"), test.get("destino_falha")))
                missing.extend(destination for destination in candidates if destination and destination not in self.scenes)
        self.assertEqual(missing, [])

    def test_content_is_divided_between_wilderness_cities_main_story_and_relationships(self) -> None:
        phases: dict[str, int] = {}
        for scene in self.eldorwood.values():
            phase = scene.get("meta", {}).get("fase")
            phases[phase] = phases.get(phase, 0) + 1
        self.assertEqual(phases["nascimento"], 3)
        self.assertEqual(phases["exploracao_inicial"], 60)
        self.assertEqual(phases["vida_urbana"], 50)
        self.assertEqual(phases["raiz_ancora"], 18)
        self.assertEqual(phases["relacao"], 12)

    def test_every_spatial_settlement_has_a_real_entry_scene(self) -> None:
        entries = {settlement["scene_id"] for settlement in ELDORWOOD_SETTLEMENTS}
        self.assertEqual(len(entries), 11)
        self.assertTrue(entries <= self.scenes.keys())

    def test_all_fifteen_intelligent_races_are_represented_by_persistent_npcs(self) -> None:
        races = {npc["race"] for npc in ELDORWOOD_NPCS}
        expected = {
            "Humana", "Sylvani", "Aureli", "Aquari", "Solari", "Glacari", "Luminari",
            "Kragari", "Ziraki", "Ninfari", "Umbrari", "Ferrari", "Drakari", "Ethari", "Voraki",
        }
        self.assertEqual(races, expected)

    def test_narratives_have_real_newlines_and_no_old_repeated_sentence(self) -> None:
        combined = "\n".join(scene["texto"] for scene in self.eldorwood.values())
        self.assertNotIn("\\n", combined)
        self.assertNotIn("Para alguém que chegou sem memória", combined)
        self.assertNotIn("nenhuma escolha é tratada como decoração", combined.lower())

    def test_slow_pacing_is_encoded_in_city_relationship_and_main_quest_actions(self) -> None:
        for scene in self.eldorwood.values():
            phase = scene.get("meta", {}).get("fase")
            if phase in {"vida_urbana", "relacao"}:
                for option in scene["opcoes"]:
                    effects = option.get("efeitos") or []
                    self.assertTrue(
                        option.get("modo") == "exploracao_livre"
                        or any(effect.get("tipo") == "tempo_minutos" for effect in effects),
                        f"ação instantânea em {scene['id']}",
                    )
            if phase == "raiz_ancora" and int(scene["meta"]["capitulo"]) < 16:
                for option in scene["opcoes"]:
                    self.assertTrue(
                        option.get("modo") == "exploracao_livre" or option.get("jornada"),
                        f"capítulo principal sem viagem real em {scene['id']}",
                    )


class EldorwoodSpatialTests(unittest.TestCase):
    def test_scripted_journey_changes_real_coordinates(self) -> None:
        player = session()
        player.position_x = 0.0
        player.position_y = 1500.0
        game = ProceduralExploration(player, rng=QuietRandom(1))
        game.queue_story_journey(
            "r2_f02_samambaias_em_espiral",
            "A observação terminou.",
            "seguir ao norte",
            {"distancia_km": 3.4, "minutos_minimos": 120, "direcao": "norte"},
        )
        game.choose("journey:normal")
        self.assertGreater(player.position_y, 1500.0)
        self.assertEqual(player.position_x, 0.0)
        stored = player.exploration["coordinates_by_region"]["eldorwood"]
        self.assertAlmostEqual(stored["y"], player.position_y, places=3)

    def test_eldorwood_to_frostreach_border_is_physical_and_optional(self) -> None:
        player = session()
        player.biome_slug = "colinas_arborizadas"
        player.position_x = 450.0
        player.position_y = 2999.2
        game = ProceduralExploration(player, rng=QuietRandom(2))
        turn = game.choose("travel:norte")
        self.assertIn("border:cross", {choice["id"] for choice in turn.choices})
        self.assertEqual(player.region_slug, "eldorwood")
        crossed = game.choose("border:cross")
        self.assertEqual(player.region_slug, "frostreach")
        self.assertEqual(player.biome_slug, "planalto_central_frostreach")
        self.assertIn("atravessou_eldorwood_frostreach", player.flags)
        self.assertIn("Frostreach", crossed.narrative)

    def test_frostreach_to_eldorwood_border_is_also_physical(self) -> None:
        player = session("frostreach")
        player.position_x = 450.0
        player.position_y = -2999.2
        game = ProceduralExploration(player, rng=QuietRandom(3))
        turn = game.choose("travel:sul")
        self.assertIn("border:cross", {choice["id"] for choice in turn.choices})
        game.choose("border:cross")
        self.assertEqual(player.region_slug, "eldorwood")
        self.assertEqual(player.biome_slug, "colinas_arborizadas")

    def test_spawn_biome_changes_distance_to_frostreach(self) -> None:
        spawns = REGION_MAPS["eldorwood"]["spawns"]
        minimum_distances = {
            biome: min(3000.0 - y for x, y in points if -900.0 <= x <= 1250.0)
            for biome, points in spawns.items()
            if any(-900.0 <= x <= 1250.0 for x, y in points)
        }
        self.assertLess(minimum_distances["colinas_arborizadas"], 600.0)
        self.assertGreater(minimum_distances["pantanos_rios"], 2500.0)
        self.assertGreater(
            minimum_distances["pantanos_rios"],
            minimum_distances["floresta_densa_antiga"] + 1000.0,
        )

    def test_road_can_generate_travelers_but_not_teleport_to_a_distant_city(self) -> None:
        player = session()
        player.position_x = 305.0
        player.position_y = 1510.0
        game = ProceduralExploration(player, rng=LastChoiceRandom(4))
        self.assertTrue(game._near_civilization())
        event = game._roll_interruption(1.0, "norte", near_civilization=True)
        self.assertIsNotNone(event)
        self.assertEqual(event["kind"], "npc")

    def test_relationships_persist_across_region_crossing(self) -> None:
        player = session()
        core = PersistentCore(player, {})
        core.relationships.apply(
            "sael_ithyr",
            {"trust": 70, "respect": 50, "warmth": 50},
            reason="jornada compartilhada",
            name="Sael Ithyr",
        )
        game = ProceduralExploration(player, relationships=core.relationships, rng=QuietRandom(5))
        player.position_x = 450.0
        player.position_y = 2999.2
        player.biome_slug = "colinas_arborizadas"
        game.state["biome"] = "colinas_arborizadas"
        game.choose("travel:norte")
        game.choose("border:cross")
        record = core.relationships.get("sael_ithyr")
        self.assertEqual(record["status"], "devoted")
        self.assertEqual(player.region_slug, "frostreach")
        json.dumps(player.to_dict(), ensure_ascii=False)

    def test_ignored_primary_story_advances_without_the_player(self) -> None:
        player = session()
        definitions = {
            ELDORWOOD_ROOT_QUEST: {
                "id": ELDORWOOD_ROOT_QUEST,
                "title": "As folhas pronunciam nomes",
                "category": "primary_optional",
                "stages": [],
            }
        }
        core = PersistentCore(player, definitions)
        core.enter_scene("r2_q01_folhas_pronunciam")
        self.assertEqual(core.quests.get(ELDORWOOD_ROOT_QUEST)["status"], "rumored")
        core.record_choice(
            scene_id="r2_q01_folhas_pronunciam",
            option_text="Registrar o rumor e voltar à exploração",
            destination=None,
            result_key="success",
        )
        core.clock.advance(3 * 24 * 60)
        core.process_due_events()
        quest = core.quests.get(ELDORWOOD_ROOT_QUEST)
        self.assertEqual(quest["status"], "transformed")
        self.assertEqual(quest["outcome"], "investigation_led_by_council")
        self.assertEqual(core.world.get("eldorwood.raiz_ancora.world_progress"), "council_quarantine")

    def test_primary_story_does_not_advance_without_player_after_acceptance(self) -> None:
        player = session()
        definitions = {
            ELDORWOOD_ROOT_QUEST: {
                "id": ELDORWOOD_ROOT_QUEST,
                "title": "As folhas pronunciam nomes",
                "category": "primary_optional",
                "stages": [],
            }
        }
        core = PersistentCore(player, definitions)
        core.enter_scene("r2_q01_folhas_pronunciam")
        core.record_choice(
            scene_id="r2_q01_folhas_pronunciam",
            option_text="Observar por três ciclos de chuva",
            destination="r2_q02_desaparecidos_dossel",
            result_key="success",
        )
        core.clock.advance(3 * 24 * 60)
        core.process_due_events()
        self.assertEqual(core.quests.get(ELDORWOOD_ROOT_QUEST)["status"], "active")
        self.assertFalse(core.world.has("eldorwood.raiz_ancora.world_progress"))


if __name__ == "__main__":
    unittest.main()
