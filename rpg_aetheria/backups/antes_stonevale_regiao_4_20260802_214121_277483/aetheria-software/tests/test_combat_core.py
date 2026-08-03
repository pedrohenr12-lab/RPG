from __future__ import annotations

import json
import random
import unittest

from aetheria_app.combat.careers import (
    BATTLE_CLASSES,
    CAREERS,
    PROFESSIONS,
    SkillTreeService,
    apply_starting_careers,
)
from aetheria_app.combat.engine import CombatEngine, StatusEffect, adapt_item_rows
from aetheria_app.models import PlayerSession


def make_session(battle: str = "guerreiro", profession: str = "ferreiro") -> PlayerSession:
    session = PlayerSession(
        name="Teste", race_slug="humanos", race_name="Humanos",
        region_slug="frostreach", scene_id="teste", life_max=40,
        attack=8, defense=5, mana_max=20, speed=6, critical=0.05,
    )
    apply_starting_careers(session, battle, profession)
    return session


def event(**changes):
    base = {
        "kind": "fauna", "name": "Lobo de Teste", "slug": "lobo_teste",
        "behavior": "predator", "threat": 2, "description": "um predador se aproxima",
    }
    base.update(changes)
    return base


class CareerTests(unittest.TestCase):
    def test_exactly_forty_paths_and_six_hundred_nodes(self):
        self.assertEqual(40, len(CAREERS))
        self.assertEqual(24, len(BATTLE_CLASSES))
        self.assertEqual(16, len(PROFESSIONS))
        self.assertEqual(600, sum(len(career.nodes) for career in CAREERS.values()))
        self.assertIn("mago", CAREERS)
        self.assertIn("clerigo", CAREERS)
        self.assertIn("anciao", CAREERS)
        self.assertIn("guerreiro", CAREERS)

    def test_every_path_has_three_branches_and_fifteen_unique_nodes(self):
        all_slugs = []
        for career in CAREERS.values():
            self.assertEqual(3, len(career.branches), career.name)
            self.assertEqual(15, len(career.nodes), career.name)
            all_slugs.extend(node.slug for node in career.nodes)
            for branch in career.branches.values():
                self.assertEqual([1, 2, 3, 4, 5], [node.tier for node in branch])
                self.assertFalse(branch[0].prerequisites)
                for previous, current in zip(branch, branch[1:]):
                    self.assertEqual((previous.slug,), current.prerequisites)
        self.assertEqual(len(all_slugs), len(set(all_slugs)))

    def test_skill_purchase_requires_path_prerequisite_and_points(self):
        session = make_session()
        branch = next(iter(BATTLE_CLASSES["guerreiro"].branches.values()))
        with self.assertRaises(ValueError):
            SkillTreeService.purchase(session, branch[1].slug)
        learned = SkillTreeService.purchase(session, branch[0].slug)
        self.assertEqual(branch[0].slug, learned.slug)
        self.assertIn(learned.slug, session.unlocked_skills)
        self.assertEqual(2, session.skill_points)

    def test_third_node_unlocks_an_active_technique(self):
        session = make_session()
        session.skill_points = 10
        branch = next(iter(BATTLE_CLASSES["guerreiro"].branches.values()))
        for node in branch[:3]:
            SkillTreeService.purchase(session, node.slug)
        actions = SkillTreeService.unlocked_actions(session)
        self.assertEqual(1, len(actions))
        engine = CombatEngine.start(session, event(), rng=random.Random(13))
        engine.target().position = 1
        action_id = f"skill:{next(iter(actions))}"
        self.assertIn(action_id, {row["id"] for row in engine.available_actions()})

    def test_profession_levels_from_use_and_battle_class_from_combat_xp(self):
        session = make_session()
        session.profession_xp = 119
        gained = SkillTreeService.grant_xp(session, 2, profession=True)
        self.assertEqual(1, gained)
        self.assertEqual(2, session.profession_level)
        session.class_xp = 119
        gained = SkillTreeService.grant_xp(session, 2)
        self.assertEqual(1, gained)
        self.assertEqual(2, session.class_level)


class CombatTests(unittest.TestCase):
    def test_combat_round_has_three_action_points_and_persists(self):
        session = make_session()
        engine = CombatEngine.start(session, event(), rng=random.Random(3))
        self.assertEqual(3, engine.state.action_points)
        self.assertEqual("active", session.combat_state["outcome"])
        json.dumps(session.to_dict(), ensure_ascii=False)
        restored = PlayerSession.from_dict(json.loads(json.dumps(session.to_dict())))
        resumed = CombatEngine.resume(restored, rng=random.Random(3))
        self.assertIsNotNone(resumed)
        self.assertEqual(engine.state.combat_id, resumed.state.combat_id)

    def test_attack_uses_range_hit_degree_armor_and_damage(self):
        session = make_session()
        session.attack = 100
        engine = CombatEngine.start(session, event(), rng=random.Random(4))
        target = engine.target()
        target.position = 1
        target.armor = 8
        before = target.life
        engine.perform("attack")
        self.assertLess(target.life, before)
        self.assertGreater(target.life, before - 30)
        self.assertEqual(1, engine.state.action_points)

    def test_guard_is_available_for_enemy_response_and_reduces_damage(self):
        session = make_session()
        engine = CombatEngine.start(session, event(threat=1), rng=random.Random(9))
        engine.state.player.position = 1
        engine.target().position = 1
        engine.perform("guard")
        self.assertTrue(engine.state.player.has("guarded"))
        engine.perform("end_turn")
        self.assertLessEqual(engine.state.action_points, 3)

    def test_magic_costs_mana_and_can_apply_elemental_damage(self):
        session = make_session("mago", "escriba")
        session.attack = 100
        engine = CombatEngine.start(session, event(), rng=random.Random(5))
        target = engine.target()
        target.position = 1
        before_mana = engine.state.player.mana
        before_life = target.life
        engine.perform("spell:faisca_ignea")
        self.assertLess(engine.state.player.mana, before_mana)
        self.assertLess(target.life, before_life)

    def test_artifact_consumes_charge_and_accumulates_instability(self):
        session = make_session("artifice_arcano", "engenheiro")
        session.attack = 100
        engine = CombatEngine.start(session, event(), rng=random.Random(7))
        engine.target().position = 1
        self.assertEqual(3, engine.state.artifact_charge)
        engine.perform("artifact")
        self.assertEqual(2, engine.state.artifact_charge)
        self.assertEqual(12, engine.state.artifact_instability)

    def test_nonlethal_subdual_and_victory_rewards_are_recorded(self):
        session = make_session()
        session.attack = 100
        engine = CombatEngine.start(session, event(), rng=random.Random(12))
        target = engine.target()
        target.position = 1
        target.life = 2
        before_xp = session.xp
        engine.perform("subdue")
        self.assertEqual("captured_enemy", engine.state.outcome)
        self.assertGreater(session.xp, before_xp)
        self.assertEqual(1, len(session.combat_history))

    def test_boss_changes_phase_at_health_thresholds(self):
        session = make_session()
        engine = CombatEngine.start(session, event(name="Titã de Teste", threat=6, legendary=True), rng=random.Random(10))
        boss = engine.target()
        boss.life = round(boss.life_max * 0.25)
        old_attack = boss.attack
        engine._boss_phase(boss)
        self.assertEqual(3, boss.phase)
        self.assertGreater(boss.attack, old_attack)

    def test_status_damage_ticks_and_expires(self):
        session = make_session()
        engine = CombatEngine.start(session, event(), rng=random.Random(8))
        target = engine.target()
        target.add_status(StatusEffect("burning", "Em chamas", 1, potency=3))
        before = target.life
        engine._tick_statuses(target, "start")
        self.assertLess(target.life, before)
        engine._tick_statuses(target, "end")
        self.assertFalse(target.has("burning"))

    def test_companions_enter_as_allies(self):
        session = make_session()
        session.companions.append({"id": "lia", "name": "Lia", "level": 2, "role": "healer", "active": True})
        engine = CombatEngine.start(session, event(), rng=random.Random(2))
        self.assertEqual(["Lia"], [ally.name for ally in engine.state.allies])

    def test_mysql_item_rows_feed_weapon_profiles(self):
        rows = [{
            "name": "Lança Experimental", "damage_min": 11, "damage_max": 19,
            "damage_type": "perfuracao", "range_m": 6, "tier": 3,
            "effect_key": "perfura_armadura", "effect_value": 20,
        }]
        profile = adapt_item_rows(rows)["Lança Experimental"]
        self.assertEqual("piercing", profile["damage_type"])
        self.assertEqual(2, profile["range"])
        self.assertEqual(2, profile["armor_piercing"])

    def test_legacy_save_receives_progression_defaults(self):
        current = make_session().to_dict()
        for key in (
            "battle_class_slug", "battle_class_name", "profession_slug", "profession_name",
            "skill_points", "unlocked_skills", "equipment", "combat_state",
        ):
            current.pop(key, None)
        restored = PlayerSession.from_dict(current)
        self.assertEqual("guerreiro", restored.battle_class_slug)
        self.assertEqual("cacador_coletor", restored.profession_slug)
        self.assertEqual(3, restored.skill_points)


if __name__ == "__main__":
    unittest.main()
