from __future__ import annotations

import json
import random
import unittest
from pathlib import Path

from aetheria_app.combat import CombatEngine
from aetheria_app.core import PersistentCore
from aetheria_app.core.runtime import ESPINHA_ROOT_QUEST
from aetheria_app.models import PlayerSession
from aetheria_app.procedural_exploration import ProceduralExploration, REGION_MAPS
from aetheria_app.espinha_content import (
    ESPINHA_BIOMES,
    ESPINHA_MARKETS,
    ESPINHA_NPCS,
    ESPINHA_SETTLEMENTS,
)


SOFTWARE_ROOT = Path(__file__).resolve().parents[1]
SCENES_ROOT = SOFTWARE_ROOT.parent / "data" / "scenes"


def load_scenes() -> dict[str, dict]:
    scenes: dict[str, dict] = {}
    for path in SCENES_ROOT.glob("*.json"):
        raw = json.loads(path.read_text(encoding="utf-8"))
        for scene in raw if isinstance(raw, list) else [raw]:
            scenes[scene["id"]] = scene
    return scenes


def session(region: str = "espinha_do_mundo") -> PlayerSession:
    return PlayerSession(
        name="Teste", race_slug="humanos", race_name="Humanos",
        region_slug=region, scene_id="00_despertar_espinha_cordilheira",
        life_max=30, attack=7, defense=4, mana_max=15, speed=5, critical=0.10,
        biome_slug="cordilheira_monumental" if region == "espinha_do_mundo" else "presas_de_gelo",
    )


class QuietRandom(random.Random):
    def random(self) -> float:
        return 0.99


class EspinhaContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scenes = load_scenes()
        cls.espinha = {
            scene_id: scene for scene_id, scene in cls.scenes.items()
            if scene.get("meta", {}).get("regiao") == "espinha_do_mundo"
        }

    def test_region_has_143_scenes_and_429_visible_choices(self) -> None:
        self.assertEqual(len(self.espinha), 143)
        self.assertEqual(sum(len(scene["opcoes"]) for scene in self.espinha.values()), 429)
        self.assertTrue(all(len(scene["opcoes"]) == 3 for scene in self.espinha.values()))

    def test_scene_division_is_complete(self) -> None:
        phases: dict[str, int] = {}
        for scene in self.espinha.values():
            phase = scene.get("meta", {}).get("fase")
            phases[phase] = phases.get(phase, 0) + 1
        self.assertEqual(phases, {
            "despertar": 3, "ermo": 60, "vida_urbana": 50,
            "ancora_profundidade": 18, "relacao": 12,
        })

    def test_destinations_test_results_and_retreats_exist(self) -> None:
        missing = []
        for scene in self.espinha.values():
            for option in scene["opcoes"]:
                test = option.get("teste") or {}
                combat = option.get("combate") or {}
                for destination in (option.get("destino"), test.get("destino_sucesso"), test.get("destino_falha"), combat.get("destino_fuga")):
                    if destination and destination not in self.scenes:
                        missing.append(destination)
        self.assertEqual(missing, [])

    def test_every_settlement_has_scene_market_and_three_offers(self) -> None:
        entries = {settlement["scene_id"] for settlement in ESPINHA_SETTLEMENTS}
        self.assertEqual(len(entries), 11)
        self.assertTrue(entries <= self.scenes.keys())
        self.assertEqual(set(ESPINHA_MARKETS), {settlement["id"] for settlement in ESPINHA_SETTLEMENTS})
        self.assertTrue(all(len(market["stock"]) == 3 for market in ESPINHA_MARKETS.values()))

    def test_all_fifteen_intelligent_races_and_vorath_are_persistent(self) -> None:
        races = {npc["race"] for npc in ESPINHA_NPCS}
        expected = {"Humana","Sylvani","Aureli","Aquari","Solari","Glacari","Luminari","Kragari","Ziraki","Ninfari","Umbrari","Ferrari","Drakari","Ethari","Voraki","Vorath"}
        self.assertTrue(expected <= races)

    def test_wilderness_is_detailed_unique_and_slow(self) -> None:
        combined = "\n".join(scene["texto"] for scene in self.espinha.values())
        self.assertNotIn("\\n", combined)
        self.assertNotIn("Para alguém que chegou sem memória", combined)
        wilderness = [scene for scene in self.espinha.values() if scene.get("meta", {}).get("fase") == "ermo"]
        self.assertTrue(all(len(scene["texto"]) >= 250 for scene in wilderness))
        self.assertGreater(len({scene["titulo"] for scene in wilderness}), 58)
        self.assertTrue(all(any(e.get("tipo") == "tempo_minutos" for e in scene["opcoes"][0].get("efeitos") or []) for scene in wilderness))

    def test_city_relationship_and_story_actions_consume_time_or_travel(self) -> None:
        for scene in self.espinha.values():
            phase = scene.get("meta", {}).get("fase")
            if phase in {"vida_urbana", "relacao"}:
                for option in scene["opcoes"]:
                    self.assertTrue(option.get("modo") == "exploracao_livre" or any(e.get("tipo") == "tempo_minutos" for e in option.get("efeitos") or []), scene["id"])
            if phase == "ancora_profundidade" and int(scene["meta"]["capitulo"]) < 16:
                for option in scene["opcoes"]:
                    self.assertTrue(option.get("modo") == "exploracao_livre" or option.get("jornada") or option.get("combate") or option.get("teste"), scene["id"])

    def test_scripted_and_procedural_combat_use_complete_engine(self) -> None:
        combat_options = [option for scene in self.espinha.values() for option in scene["opcoes"] if option.get("combate")]
        self.assertGreaterEqual(len(combat_options), 8)
        boss = next(option["combate"] for option in combat_options if option["combate"].get("legendary"))
        engine = CombatEngine.start(session(), boss, rng=random.Random(11))
        self.assertTrue(engine.state.active)
        self.assertGreaterEqual(engine.target().threat, 7)
        self.assertEqual(engine.state.action_points, 3)

    def test_canonical_biomes_flora_fauna_dragons_and_guardians(self) -> None:
        self.assertEqual(set(ESPINHA_BIOMES), {"cordilheira_monumental","vales_profundos","cavernas_gigantes"})
        all_species = {row[0] for biome in ESPINHA_BIOMES.values() for row in biome["fauna"] + biome["flora"]}
        for name in {"Líquen-de-Pico","Águia-das-Nuvens","Dragão-de-Pedra Ancião","Guardião de Vynium","Fungo-Luminoso","Sombra-Vorath","Dragão-de-Caverna"}:
            self.assertIn(name, all_species)


class EspinhaSpatialAndWorldTests(unittest.TestCase):
    def test_frostreach_to_espinha_border_is_physical_and_optional(self) -> None:
        player = session("frostreach")
        player.position_x, player.position_y = -1800.0, -2999.9
        game = ProceduralExploration(player, rng=QuietRandom(2))
        turn = game.choose("travel:sul")
        self.assertIn("border:cross", {choice["id"] for choice in turn.choices})
        self.assertEqual(player.region_slug, "frostreach")
        game.choose("border:cross")
        self.assertEqual(player.region_slug, "espinha_do_mundo")
        self.assertEqual(player.biome_slug, "cordilheira_monumental")

    def test_espinha_to_frostreach_border_is_physical(self) -> None:
        player = session()
        player.position_x, player.position_y = -1800.0, 2999.6
        game = ProceduralExploration(player, rng=QuietRandom(3))
        turn = game.choose("travel:norte")
        self.assertIn("border:cross", {choice["id"] for choice in turn.choices})
        game.choose("border:cross")
        self.assertEqual(player.region_slug, "frostreach")

    def test_stonevale_and_espinha_connect_both_ways(self) -> None:
        player = session("stonevale")
        player.biome_slug = "platos_aridos"
        player.position_x, player.position_y = -2999.4, -1180.0
        game = ProceduralExploration(player, rng=QuietRandom(4))
        turn = game.choose("travel:oeste")
        self.assertIn("border:cross", {choice["id"] for choice in turn.choices})
        game.choose("border:cross")
        self.assertEqual(player.region_slug, "espinha_do_mundo")
        player.position_x, player.position_y = 2999.6, -1180.0
        player.biome_slug = "vales_profundos"
        game = ProceduralExploration(player, rng=QuietRandom(5))
        turn = game.choose("travel:leste")
        self.assertIn("border:cross", {choice["id"] for choice in turn.choices})
        game.choose("border:cross")
        self.assertEqual(player.region_slug, "stonevale")

    def test_spawn_biomes_change_border_distance(self) -> None:
        spawns = REGION_MAPS["espinha_do_mundo"]["spawns"]
        north = {biome:min(3000-y for x,y in points) for biome,points in spawns.items()}
        self.assertLess(north["cordilheira_monumental"], 1000)
        self.assertGreater(north["cavernas_gigantes"], north["cordilheira_monumental"] + 2000)

    def test_altitude_economy_and_conditions_survive_save_roundtrip(self) -> None:
        player = session()
        player.coins, player.hypoxia, player.vertical_risk = 17, 61, 38
        player.economy_history.append({"delta": -5, "reason": "chá"})
        restored = PlayerSession.from_dict(player.to_dict())
        self.assertEqual((restored.coins, restored.hypoxia, restored.vertical_risk), (17,61,38))
        self.assertEqual(restored.economy_history[0]["reason"], "chá")

    def test_movement_accumulates_altitude_risk(self) -> None:
        player = session()
        game = ProceduralExploration(player, rng=QuietRandom(6))
        game.choose("travel:norte")
        self.assertGreater(player.hypoxia, 0)
        self.assertGreater(player.vertical_risk, 0)

    def test_ignored_story_advances_without_player(self) -> None:
        player = session()
        definitions = {ESPINHA_ROOT_QUEST:{"id":ESPINHA_ROOT_QUEST,"title":"A Âncora da Profundidade","category":"primary_optional","stages":[]}}
        core = PersistentCore(player, definitions)
        core.enter_scene("r6_q01_o_pulso_sob_as_minas")
        self.assertEqual(core.quests.get(ESPINHA_ROOT_QUEST)["status"], "rumored")
        core.record_choice(scene_id="r6_q01_o_pulso_sob_as_minas",option_text="Registrar o rumor",destination=None,result_key="success")
        core.clock.advance(7 * 24 * 60)
        core.process_due_events()
        quest = core.quests.get(ESPINHA_ROOT_QUEST)
        self.assertEqual(quest["status"], "transformed")
        self.assertEqual(quest["outcome"], "forges_expand_and_dampers_fail")

    def test_accepted_story_waits_for_player(self) -> None:
        player = session()
        definitions = {ESPINHA_ROOT_QUEST:{"id":ESPINHA_ROOT_QUEST,"title":"A Âncora da Profundidade","category":"primary_optional","stages":[]}}
        core = PersistentCore(player, definitions)
        core.enter_scene("r6_q01_o_pulso_sob_as_minas")
        core.record_choice(scene_id="r6_q01_o_pulso_sob_as_minas",option_text="Priorizar trabalhadores",destination="r6_q02_sete_tremores_medidos",result_key="success")
        core.clock.advance(7 * 24 * 60)
        core.process_due_events()
        self.assertEqual(core.quests.get(ESPINHA_ROOT_QUEST)["status"], "active")
        self.assertFalse(core.world.has("espinha.profundidade.world_progress"))


if __name__ == "__main__":
    unittest.main()
