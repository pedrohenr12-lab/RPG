from __future__ import annotations

import json
import random
import unittest

from aetheria_app.core import ActionRequest, PersistentCore
from aetheria_app.core.runtime import TOVIN_QUEST
from aetheria_app.models import PlayerSession


DEFINITIONS = {
    TOVIN_QUEST: {
        "id": TOVIN_QUEST,
        "title": "O barco que voltou sozinho",
        "category": "community_mystery",
        "stages": [],
    }
}


def session() -> PlayerSession:
    return PlayerSession(
        name="Teste",
        race_slug="humanos",
        race_name="Humanos",
        region_slug="frostreach",
        scene_id="fr1_c07_redes_aquari",
        life_max=20,
        attack=4,
        defense=2,
        mana_max=10,
        speed=5,
        critical=0.10,
    )


class FixedRandom(random.Random):
    def __init__(self, values: list[int]):
        super().__init__(1)
        self.values = list(values)

    def randint(self, _a: int, _b: int) -> int:
        return self.values.pop(0)


class PersistentCoreTests(unittest.TestCase):
    def test_old_flags_are_migrated_to_world_facts(self) -> None:
        player = session()
        player.flags.add("ponte_observada")
        core = PersistentCore(player, DEFINITIONS)
        self.assertTrue(core.world.get("legacy.flag.ponte_observada"))
        self.assertEqual(player.schema_version, 2)

    def test_world_state_survives_a_json_roundtrip(self) -> None:
        player = session()
        core = PersistentCore(player, DEFINITIONS)
        core.world.set("frostreach.weather", "nevasca", source="test")
        restored = PlayerSession.from_dict(json.loads(json.dumps(player.to_dict(), ensure_ascii=False)))
        restored_core = PersistentCore(restored, DEFINITIONS)
        self.assertEqual(restored_core.world.get("frostreach.weather"), "nevasca")

    def test_action_resolver_has_four_degrees(self) -> None:
        player = session()
        player.attributes["percepcao"] = 0
        core = PersistentCore(player, DEFINITIONS, rng=FixedRandom([1, 8, 12, 20]))
        results = []
        for difficulty in (15, 15, 10, 15):
            results.append(core.actions.resolve(ActionRequest(
                "test", "Teste", "percepcao", difficulty,
            )).degree)
        self.assertEqual(
            results,
            ["critical_failure", "failure", "success", "critical_success"],
        )

    def test_automatic_action_does_not_roll(self) -> None:
        core = PersistentCore(session(), DEFINITIONS)
        result = core.actions.resolve(ActionRequest(
            "look", "Olhar", duration_minutes=3,
        ))
        self.assertTrue(result.automatic)
        self.assertEqual(result.degree, "success")
        self.assertEqual(core.clock.absolute_minute, 8 * 60 + 3)

    def test_scheduled_event_waits_for_its_due_time(self) -> None:
        core = PersistentCore(session(), DEFINITIONS)
        core.scheduler.schedule(
            "weather", in_minutes=30, title="Vento mudou",
            description="O vento virou.",
            effects=[{"type": "set_fact", "key": "weather.changed", "value": True}],
        )
        core.clock.advance(29)
        self.assertEqual(core.process_due_events(), [])
        self.assertFalse(core.world.has("weather.changed"))
        core.clock.advance(1)
        self.assertEqual(len(core.process_due_events()), 1)
        self.assertTrue(core.world.get("weather.changed"))

    def test_tovin_quest_is_discovered_and_tide_really_advances(self) -> None:
        core = PersistentCore(session(), DEFINITIONS)
        core.enter_scene("fr1_c07_redes_aquari")
        quest = core.quests.get(TOVIN_QUEST)
        self.assertEqual(quest["status"], "rumored")
        core.enter_scene("fr1_c08_barco_de_tovin")
        self.assertEqual(core.quests.get(TOVIN_QUEST)["status"], "active")
        core.clock.advance(54)
        core.process_due_events()
        self.assertFalse(core.world.has("frostreach.tovin.tide_rose"))
        core.clock.advance(1)
        core.process_due_events()
        self.assertTrue(core.world.get("frostreach.tovin.tide_rose"))

    def test_rescuing_tovin_completes_quest_and_cancels_search(self) -> None:
        core = PersistentCore(session(), DEFINITIONS)
        core.enter_scene("fr1_c08_barco_de_tovin")
        core.record_choice(
            scene_id="fr1_c08_barco_de_tovin",
            option_text="Levar o barco à vila e organizar uma busca maior",
            destination="fr1_c11_ave_aurora",
            result_key="success",
        )
        self.assertTrue(any(event.event_type == "tovin_village_search" for event in core.scheduler.pending()))
        core.enter_scene("fr1_c09_sombra_no_fiorde")
        core.record_choice(
            scene_id="fr1_c09_sombra_no_fiorde",
            option_text="Distrair a criatura com peixes e retirar sobreviventes",
            destination="fr1_c10_colheita_de_alga",
            result_key="success",
        )
        quest = core.quests.get(TOVIN_QUEST)
        self.assertEqual(quest["status"], "completed")
        self.assertEqual(quest["outcome"], "rescued_injured")
        self.assertFalse(any(event.event_type == "tovin_village_search" for event in core.scheduler.pending()))

    def test_ignored_rumor_can_be_resolved_by_the_world(self) -> None:
        core = PersistentCore(session(), DEFINITIONS)
        core.enter_scene("fr1_c07_redes_aquari")
        core.clock.advance(12 * 60)
        core.process_due_events()
        quest = core.quests.get(TOVIN_QUEST)
        self.assertEqual(quest["status"], "resolved_by_world")
        self.assertEqual(core.world.get("frostreach.tovin.fate"), "resolved_without_player")

    def test_world_resolution_is_skipped_after_player_gets_involved(self) -> None:
        core = PersistentCore(session(), DEFINITIONS)
        core.enter_scene("fr1_c07_redes_aquari")
        core.enter_scene("fr1_c08_barco_de_tovin")
        core.clock.advance(12 * 60)
        core.process_due_events()
        quest = core.quests.get(TOVIN_QUEST)
        self.assertNotEqual(quest["status"], "resolved_by_world")

    def test_village_search_returns_after_three_hours(self) -> None:
        core = PersistentCore(session(), DEFINITIONS)
        core.enter_scene("fr1_c08_barco_de_tovin")
        core.record_choice(
            scene_id="fr1_c08_barco_de_tovin",
            option_text="Levar o barco à vila e organizar uma busca maior",
            destination="fr1_c11_ave_aurora",
            result_key="success",
        )
        core.clock.advance(179)
        core.process_due_events()
        self.assertEqual(core.world.get("frostreach.tovin.fate"), "missing")
        core.clock.advance(1)
        core.process_due_events()
        self.assertEqual(core.world.get("frostreach.tovin.fate"), "rescued_injured")
        self.assertEqual(core.quests.get(TOVIN_QUEST)["outcome"], "search_organized")

    def test_pending_events_survive_save_and_load(self) -> None:
        player = session()
        core = PersistentCore(player, DEFINITIONS)
        core.enter_scene("fr1_c08_barco_de_tovin")
        restored = PlayerSession.from_dict(json.loads(json.dumps(player.to_dict(), ensure_ascii=False)))
        restored_core = PersistentCore(restored, DEFINITIONS)
        self.assertTrue(any(event.event_type == "tovin_tide_rises" for event in restored_core.scheduler.pending()))
        restored_core.clock.advance(55)
        restored_core.process_due_events()
        self.assertTrue(restored_core.world.get("frostreach.tovin.tide_rose"))

    def test_same_unique_event_is_not_scheduled_twice(self) -> None:
        core = PersistentCore(session(), DEFINITIONS)
        first = core.scheduler.schedule(
            "test", in_minutes=10, title="A", description="A", unique_key="same",
        )
        second = core.scheduler.schedule(
            "test", in_minutes=20, title="B", description="B", unique_key="same",
        )
        self.assertEqual(first, second)
        self.assertEqual(len(core.scheduler.pending()), 1)

    def test_save_contains_only_json_serializable_core_data(self) -> None:
        player = session()
        core = PersistentCore(player, DEFINITIONS)
        core.enter_scene("fr1_c08_barco_de_tovin")
        json.dumps(player.to_dict(), ensure_ascii=False)


if __name__ == "__main__":
    unittest.main()
