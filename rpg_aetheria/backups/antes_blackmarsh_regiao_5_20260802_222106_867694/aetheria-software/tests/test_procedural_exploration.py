from __future__ import annotations

import random
import unittest

from aetheria_app.models import PlayerSession
from aetheria_app.procedural_exploration import ProceduralExploration


def session() -> PlayerSession:
    return PlayerSession(
        name="Teste",
        race_slug="humanos",
        race_name="Humanos",
        region_slug="frostreach",
        scene_id="00_despertar_frostreach",
        life_max=20,
        attack=4,
        defense=2,
        mana_max=10,
        speed=5,
        critical=0.10,
    )


class ProceduralExplorationTests(unittest.TestCase):
    def test_travel_is_usually_a_quiet_half_hour(self) -> None:
        game = ProceduralExploration(session(), rng=random.Random(7))
        idle = game.start("Início")
        self.assertTrue(any(choice["id"].startswith("travel:") for choice in idle.choices))

        quiet = game.choose("travel:norte")
        self.assertEqual(game.session.hour, 8)
        self.assertEqual(game.session.minute, 30)
        self.assertTrue(any(choice["id"].startswith("travel:") for choice in quiet.choices))
        self.assertFalse(any(choice["id"].startswith("event:") for choice in quiet.choices))

    def test_actions_change_after_information_is_revealed(self) -> None:
        game = ProceduralExploration(session(), rng=random.Random(6))
        game.start("Início")
        turn = game.choose("support:survey")
        self.assertTrue(any(choice["id"].startswith("event:") for choice in turn.choices))
        before = {choice["id"] for choice in turn.choices}
        reveal = next(
            (choice["id"] for choice in turn.choices if choice["id"] in {"event:study", "event:observe", "event:scout"}),
            turn.choices[0]["id"],
        )
        after_turn = game.choose(reveal)
        after = {choice["id"] for choice in after_turn.choices}
        self.assertNotEqual(before, after)

    def test_story_destination_requires_real_travel_blocks(self) -> None:
        class QuietRandom(random.Random):
            def random(self) -> float:
                return 0.99

        player = session()
        game = ProceduralExploration(player, rng=QuietRandom(1))
        game.start("Início")
        turn = game.queue_story_journey(
            "fr1_p02_neve_que_apaga",
            "A neve fecha o trecho anterior.",
            "alcançar a elevação adiante",
            {"distancia_km": 4.5, "minutos_minimos": 120},
        )
        self.assertFalse(any(choice["id"].startswith("scene:") for choice in turn.choices))
        self.assertEqual((player.hour, player.minute), (8, 0))

        for _ in range(5):
            turn = game.choose("journey:normal")
            if any(choice["id"] == "journey:arrive" for choice in turn.choices):
                break
        self.assertGreaterEqual(player.awake_minutes, 120)
        self.assertTrue(any(choice["id"] == "journey:arrive" for choice in turn.choices))
        arrival = game.choose("journey:arrive")
        self.assertTrue(any(choice["id"].startswith("scene:") for choice in arrival.choices))

    def test_character_must_sleep_after_twenty_awake_hours(self) -> None:
        player = session()
        game = ProceduralExploration(player, rng=random.Random(3))
        game.start("Início")
        player.advance_minutes(20 * 60)
        turn = game.choose("continue")
        ids = {choice["id"] for choice in turn.choices}
        self.assertNotIn("travel:norte", ids)
        self.assertIn("support:sleep", ids)

        slept = game.choose("support:sleep")
        self.assertEqual(player.awake_minutes, 0)
        self.assertEqual(player.day_phase, "Tarde")
        self.assertIn("A noite passa", slept.title)

    def test_interruptions_are_rare_and_never_exceed_two_per_day(self) -> None:
        interruptions = 0
        samples = 500
        for seed in range(samples):
            game = ProceduralExploration(session(), rng=random.Random(seed))
            game.start("Início")
            turn = game.choose("travel:norte")
            interruptions += any(choice["id"].startswith("event:") for choice in turn.choices)
        self.assertLess(interruptions, samples * 0.15)
        self.assertGreater(interruptions, 0)

        game = ProceduralExploration(session(), rng=random.Random(12))
        game.start("Início")
        first = game._roll_interruption(1.0, "norte", near_civilization=False)
        second = game._roll_interruption(1.0, "norte", near_civilization=False)
        third = game._roll_interruption(1.0, "norte", near_civilization=False)
        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        self.assertIsNone(third)

    def test_clock_uses_minutes_and_day_phases(self) -> None:
        player = session()
        self.assertEqual(player.day_phase, "Manhã")
        player.advance_minutes(4 * 60 + 15)
        self.assertEqual((player.day, player.hour, player.minute), (1, 12, 15))
        self.assertEqual(player.day_phase, "Tarde")
        player.advance_minutes(6 * 60 + 45)
        self.assertEqual(player.day_phase, "Noite")
        player.advance_minutes(5 * 60)
        self.assertEqual((player.day, player.hour), (2, 0))
        self.assertEqual(player.day_phase, "Madrugada")

    def test_travel_after_eight_hours_requires_a_forced_march_roll(self) -> None:
        player = session()
        game = ProceduralExploration(player, rng=random.Random(4))
        game.start("Início")
        player.travel_minutes_today = 8 * 60
        note = game._apply_movement_cost(60, 1.8, "normal")
        self.assertIn("MARCHA FORÇADA", note)
        self.assertIn("D20", note)
        self.assertIn("marcha_forcada", player.flags)

    def test_no_standalone_d20_button_exists(self) -> None:
        game = ProceduralExploration(session(), rng=random.Random(22))
        observed: set[str] = set()
        turn = game.start("Início")
        for _ in range(80):
            observed.update(choice["id"] for choice in turn.choices)
            choice = turn.choices[0]["id"]
            turn = game.choose(choice)
            if not turn.choices:
                break
        self.assertNotIn("support:d20", observed)
        self.assertGreater(len(observed), 8)

    def test_state_remains_json_serializable(self) -> None:
        import json

        player = session()
        game = ProceduralExploration(player, rng=random.Random(31))
        game.start("Início")
        game.choose("travel:oeste")
        json.dumps(player.to_dict(), ensure_ascii=False)

    def test_portuguese_scene_effect_names_update_session_fields(self) -> None:
        player = session()
        player.change_need("energia", -4)
        player.change_need("fome", 7)
        player.change_need("sede", 9)
        self.assertEqual(player.energy, 96)
        self.assertEqual(player.hunger, 22)
        self.assertEqual(player.thirst, 24)


if __name__ == "__main__":
    unittest.main()
