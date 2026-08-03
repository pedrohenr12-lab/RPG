from __future__ import annotations

import json
import random
import unittest
from pathlib import Path

from aetheria_app.combat import CombatEngine
from aetheria_app.core import PersistentCore
from aetheria_app.core.runtime import BLACKMARSH_ROOT_QUEST
from aetheria_app.models import PlayerSession
from aetheria_app.procedural_exploration import ProceduralExploration, REGION_MAPS
from aetheria_app.blackmarsh_content import (
    BLACKMARSH_BIOMES,
    BLACKMARSH_MARKETS,
    BLACKMARSH_NPCS,
    BLACKMARSH_SETTLEMENTS,
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


def session(region: str = "blackmarsh") -> PlayerSession:
    return PlayerSession(
        name="Teste",
        race_slug="humanos",
        race_name="Humanos",
        region_slug=region,
        scene_id="00_despertar_blackmarsh_pantanos",
        life_max=30,
        attack=7,
        defense=4,
        mana_max=15,
        speed=5,
        critical=0.10,
        biome_slug="pantanos_vastos" if region == "blackmarsh" else "vales_verdes",
    )


class QuietRandom(random.Random):
    def random(self) -> float:
        return 0.99


class BlackmarshContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scenes = load_scenes()
        cls.blackmarsh = {
            scene_id: scene
            for scene_id, scene in cls.scenes.items()
            if scene.get("meta", {}).get("regiao") == "blackmarsh"
        }

    def test_region_has_143_scenes_and_429_visible_choices(self) -> None:
        self.assertEqual(len(self.blackmarsh), 143)
        self.assertEqual(sum(len(scene["opcoes"]) for scene in self.blackmarsh.values()), 429)
        self.assertTrue(all(len(scene["opcoes"]) == 3 for scene in self.blackmarsh.values()))

    def test_scene_division_is_complete(self) -> None:
        phases: dict[str, int] = {}
        for scene in self.blackmarsh.values():
            phase = scene.get("meta", {}).get("fase")
            phases[phase] = phases.get(phase, 0) + 1
        self.assertEqual(phases, {
            "nascimento": 3,
            "exploracao_inicial": 60,
            "vida_urbana": 50,
            "limiar": 18,
            "relacao": 12,
        })

    def test_destinations_and_test_outcomes_exist(self) -> None:
        missing = []
        for scene in self.blackmarsh.values():
            for option in scene["opcoes"]:
                test = option.get("teste") or {}
                for destination in (
                    option.get("destino"),
                    test.get("destino_sucesso"),
                    test.get("destino_falha"),
                ):
                    if destination and destination not in self.scenes:
                        missing.append(destination)
        self.assertEqual(missing, [])

    def test_every_spatial_settlement_has_a_real_entry_scene_and_market(self) -> None:
        entries = {settlement["scene_id"] for settlement in BLACKMARSH_SETTLEMENTS}
        self.assertEqual(len(entries), 11)
        self.assertTrue(entries <= self.scenes.keys())
        self.assertEqual(set(BLACKMARSH_MARKETS), {settlement["id"] for settlement in BLACKMARSH_SETTLEMENTS})
        self.assertTrue(all(market["stock"] for market in BLACKMARSH_MARKETS.values()))

    def test_all_fifteen_intelligent_races_are_persistent_npcs(self) -> None:
        races = {npc["race"] for npc in BLACKMARSH_NPCS}
        expected = {
            "Humana", "Sylvani", "Aureli", "Aquari", "Solari", "Glacari", "Luminari",
            "Kragari", "Ziraki", "Ninfari", "Umbrari", "Ferrari", "Drakari", "Ethari", "Voraki",
        }
        self.assertTrue(expected <= races)
        self.assertIn("Vorath", races)

    def test_narratives_are_slow_detailed_and_do_not_repeat_old_sentence(self) -> None:
        combined = "\n".join(scene["texto"] for scene in self.blackmarsh.values())
        self.assertNotIn("\\n", combined)
        self.assertNotIn("Para alguém que chegou sem memória", combined)
        self.assertNotIn("nenhuma escolha é tratada como decoração", combined.lower())
        wilderness = [scene for scene in self.blackmarsh.values() if scene.get("meta", {}).get("fase") == "exploracao_inicial"]
        self.assertTrue(all(len(scene["texto"]) >= 260 for scene in wilderness))
        self.assertGreater(len({scene["titulo"] for scene in wilderness}), 55)

    def test_city_relationship_and_story_actions_consume_time_or_travel(self) -> None:
        for scene in self.blackmarsh.values():
            phase = scene.get("meta", {}).get("fase")
            if phase in {"vida_urbana", "relacao"}:
                for option in scene["opcoes"]:
                    self.assertTrue(
                        option.get("modo") == "exploracao_livre"
                        or any(effect.get("tipo") == "tempo_minutos" for effect in option.get("efeitos") or []),
                        scene["id"],
                    )
            if phase == "limiar" and int(scene["meta"]["capitulo"]) < 16:
                for option in scene["opcoes"]:
                    self.assertTrue(
                        option.get("modo") == "exploracao_livre"
                        or option.get("jornada")
                        or option.get("combate")
                        or option.get("teste"),
                        scene["id"],
                    )

    def test_scripted_and_procedural_combat_use_the_complete_engine(self) -> None:
        combat_options = [
            option
            for scene in self.blackmarsh.values()
            for option in scene["opcoes"]
            if option.get("combate")
        ]
        self.assertGreaterEqual(len(combat_options), 8)
        boss = next(option["combate"] for option in combat_options if option["combate"].get("legendary"))
        engine = CombatEngine.start(session(), boss, rng=random.Random(11))
        self.assertTrue(engine.state.active)
        self.assertGreaterEqual(engine.target().threat, 7)
        self.assertEqual(engine.state.action_points, 3)

    def test_biomes_contain_canonical_flora_fauna_and_bosses(self) -> None:
        self.assertEqual(set(BLACKMARSH_BIOMES), {"pantanos_vastos", "mangues_gigantes", "ilhas_vegetacao_flutuante"})
        all_species = {row[0] for biome in BLACKMARSH_BIOMES.values() for row in biome["fauna"] + biome["flora"]}
        for name in {"Musgo-Negro", "Crocodilo-Negro", "Ninfa-Negra", "Mangue-Gigante", "Guardião de Harmonix", "Guardião de Orbitium"}:
            self.assertIn(name, all_species)


class BlackmarshSpatialAndWorldTests(unittest.TestCase):
    def test_arkanor_to_blackmarsh_border_is_physical_and_optional(self) -> None:
        player = session("arkanor")
        player.position_x = 1000.0
        player.position_y = -1299.3
        player.biome_slug = "vales_verdes"
        game = ProceduralExploration(player, rng=QuietRandom(2))
        turn = game.choose("travel:sul")
        self.assertIn("border:cross", {choice["id"] for choice in turn.choices})
        self.assertEqual(player.region_slug, "arkanor")
        game.choose("border:cross")
        self.assertEqual(player.region_slug, "blackmarsh")
        self.assertEqual(player.biome_slug, "mangues_gigantes")

    def test_blackmarsh_to_arkanor_border_is_physical(self) -> None:
        player = session()
        player.position_x = -2999.9
        player.position_y = 1800.0
        game = ProceduralExploration(player, rng=QuietRandom(3))
        turn = game.choose("travel:oeste")
        self.assertIn("border:cross", {choice["id"] for choice in turn.choices})
        game.choose("border:cross")
        self.assertEqual(player.region_slug, "arkanor")
        self.assertEqual(player.biome_slug, "vales_verdes")

    def test_spawn_biomes_change_distance_to_stonevale(self) -> None:
        spawns = REGION_MAPS["blackmarsh"]["spawns"]
        distances = {biome: min(3000.0 - y for x, y in points) for biome, points in spawns.items()}
        self.assertLess(distances["pantanos_vastos"], 1000.0)
        self.assertGreater(distances["ilhas_vegetacao_flutuante"], distances["pantanos_vastos"] + 900.0)

    def test_tropical_survival_and_trade_survive_save_roundtrip(self) -> None:
        player = session()
        player.coins = 17
        player.wetness = 61
        player.toxicity = 28
        player.infection = 13
        player.economy_history.append({"delta": -5, "reason": "água"})
        restored = PlayerSession.from_dict(player.to_dict())
        self.assertEqual(restored.coins, 17)
        self.assertEqual(restored.economy_history[0]["reason"], "água")
        self.assertEqual((restored.wetness, restored.toxicity, restored.infection), (61, 28, 13))

    def test_stonevale_and_blackmarsh_connect_both_ways(self) -> None:
        player = session("stonevale")
        player.position_x = 520.0
        player.position_y = -1799.3
        player.biome_slug = "vales_ferteis_isolados"
        game = ProceduralExploration(player, rng=QuietRandom(7))
        turn = game.choose("travel:sul")
        self.assertIn("border:cross", {choice["id"] for choice in turn.choices})
        game.choose("border:cross")
        self.assertEqual(player.region_slug, "blackmarsh")

        player.position_x = 520.0
        player.position_y = 2999.9
        player.biome_slug = "pantanos_vastos"
        game = ProceduralExploration(player, rng=QuietRandom(8))
        turn = game.choose("travel:norte")
        self.assertIn("border:cross", {choice["id"] for choice in turn.choices})
        game.choose("border:cross")
        self.assertEqual(player.region_slug, "stonevale")

    def test_ignored_story_advances_without_the_player(self) -> None:
        player = session()
        definitions = {BLACKMARSH_ROOT_QUEST: {"id":BLACKMARSH_ROOT_QUEST,"title":"O Limiar","category":"primary_optional","stages":[]}}
        core = PersistentCore(player, definitions)
        core.enter_scene("r5_q01_as_ilhas_formam_uma_porta")
        self.assertEqual(core.quests.get(BLACKMARSH_ROOT_QUEST)["status"], "rumored")
        core.record_choice(scene_id="r5_q01_as_ilhas_formam_uma_porta",option_text="Registrar o rumor e voltar à própria vida",destination=None,result_key="success")
        core.clock.advance(6 * 24 * 60)
        core.process_due_events()
        quest = core.quests.get(BLACKMARSH_ROOT_QUEST)
        self.assertEqual(quest["status"], "transformed")
        self.assertEqual(quest["outcome"], "sacrifices_expand_and_rescue_network_reacts")

    def test_accepted_story_waits_for_player(self) -> None:
        player = session()
        definitions = {BLACKMARSH_ROOT_QUEST: {"id":BLACKMARSH_ROOT_QUEST,"title":"O Limiar","category":"primary_optional","stages":[]}}
        core = PersistentCore(player, definitions)
        core.enter_scene("r5_q01_as_ilhas_formam_uma_porta")
        core.record_choice(scene_id="r5_q01_as_ilhas_formam_uma_porta",option_text="Priorizar moradores das duas margens",destination="r5_q02_a_terceira_noite",result_key="success")
        core.clock.advance(6 * 24 * 60)
        core.process_due_events()
        self.assertEqual(core.quests.get(BLACKMARSH_ROOT_QUEST)["status"], "active")
        self.assertFalse(core.world.has("blackmarsh.limiar.world_progress"))


if __name__ == "__main__":
    unittest.main()
