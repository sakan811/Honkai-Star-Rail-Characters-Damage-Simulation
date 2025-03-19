import pytest
from hsr_simulation.character import Character
from hsr_simulation.simulate_cycles import (
    simulate_cycles,
    simulate_cycles_for_character_with_summon,
)
from hsr_simulation.hunt.topaz import Topaz
from hsr_simulation.erudition.jingyuan import Jingyuan
from hsr_simulation.nihility.black_swan import BlackSwan
from hsr_simulation.hunt.boothill import Boothill
from typing import List
import random


class MockCharacter(Character):
    def __init__(self):
        # Initialize with test data
        self.data = {"DMG": [], "DMG_Type": [], "Simulate Round No.": []}
        # Basic character attributes
        self.speed = 100  # Changed to match typical character speed
        self.atk = 2000
        self.crit_rate = 0.5
        self.crit_dmg = 1.0
        self.ult_energy = 0

        # Battle state attributes
        self.enemy_weakness_broken = False
        self.enemy_weakness_gauge = 0
        self.break_effect = 1.0
        self.effect_hit_rate = 1.0
        self.current_hp = 10000
        self.max_hp = 10000

        # Action mechanics
        self.skill_points = 1
        self.enemy_toughness = 600
        self.current_enemy_toughness = 600
        self.enemy_turn_delayed_duration_weakness_broken = 0
        self.char_action_value = 0
        self.char_action_value_for_action_forward = []
        self.summon_action_value_for_action_forward = []  # Added for summon mechanics
        self.battle_start = True

    def take_action(self) -> None:
        """Simulate taking an action during battle"""
        # Calculate action value based on speed
        self.char_action_value = self.calculate_action_value(self.speed)

        # Simulate enemy weakness mechanics
        self._simulate_enemy_weakness_broken()

        # Take action based on available resources
        if self.ult_energy >= 140:
            self._use_ult()
        elif self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        # Check enemy weakness state after action
        self.check_if_enemy_weakness_broken()

    def _use_basic_atk(self) -> None:
        """Use basic attack"""
        dmg = self._calculate_damage(
            skill_multiplier=self.BASIC_ATK_MULTIPLIER,
            break_amount=self.BASIC_ATK_BREAK_AMOUNT,
        )
        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Normal")
        self._update_skill_point_and_ult_energy(
            skill_points=1, ult_energy=self.BASIC_ATK_ENERGY_GAIN
        )

    def _use_skill(self) -> None:
        """Use skill"""
        dmg = self._calculate_damage(
            skill_multiplier=self.SKILL_MULTIPLIER, break_amount=self.SKILL_BREAK_AMOUNT
        )
        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Skill")
        self._update_skill_point_and_ult_energy(
            skill_points=-1, ult_energy=self.SKILL_ENERGY_GAIN
        )

    def _use_ult(self) -> None:
        """Use ultimate"""
        dmg = self._calculate_damage(
            skill_multiplier=self.ULT_MULTIPLIER, break_amount=self.ULT_BREAK_AMOUNT
        )
        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Ultimate")
        self.ult_energy = self.DEFAULT_ULT_ENERGY_AFTER_ULT

    def calculate_action_value(self, speed: float) -> float:
        """Calculate action value based on speed"""
        char_action_value = self.ACTION_VALUE_BASE / speed
        self.char_action_value = char_action_value
        return char_action_value

    def _update_skill_point_and_ult_energy(
        self, skill_points: int, ult_energy: int
    ) -> None:
        """Update skill points and ultimate energy"""
        self.skill_points = max(0, min(1, self.skill_points + skill_points))
        self.ult_energy = max(0, min(140, self.ult_energy + ult_energy))

    def _calculate_damage(
        self,
        skill_multiplier: float,
        break_amount: int,
        dmg_multipliers: List[float] = None,
        can_crit: bool = True,
    ) -> float:
        """Calculate damage for an action"""
        base_dmg = self.atk * skill_multiplier

        if can_crit and random.random() < self.crit_rate:
            base_dmg *= 1 + self.crit_dmg

        if not self.enemy_weakness_broken:
            base_dmg *= 0.8

        self.current_enemy_toughness = max(
            0, self.current_enemy_toughness - break_amount
        )

        if dmg_multipliers:
            for multiplier in dmg_multipliers:
                base_dmg *= multiplier

        return base_dmg

    def check_if_enemy_weakness_broken(self) -> None:
        """Check if enemy weakness is broken"""
        if self.current_enemy_toughness <= 0 and not self.enemy_weakness_broken:
            self.enemy_weakness_broken = True
            self.enemy_weakness_gauge = 1

    def start_battle(self):
        """Initialize battle state"""
        super().start_battle()
        self.data = {"DMG": [], "DMG_Type": [], "Simulate Round No.": []}
        self.skill_points = 1
        self.ult_energy = 0
        self.current_enemy_toughness = self.enemy_toughness
        self.enemy_weakness_broken = False
        self.enemy_weakness_gauge = 0
        self.char_action_value = 0
        self.char_action_value_for_action_forward = []
        self.summon_action_value_for_action_forward = []  # Reset summon action values

    def reset_character_data_for_each_battle(self):
        self.data = {"DMG": [], "DMG_Type": [], "Simulate Round No.": []}
        self.enemy_weakness_broken = False
        self.enemy_weakness_gauge = 0
        self.skill_points = 1
        self.ult_energy = 0
        self.current_enemy_toughness = self.enemy_toughness
        self.char_action_value_for_action_forward = []
        self.summon_action_value_for_action_forward = []  # Reset summon action values


def test_simulate_cycles():
    character = MockCharacter()
    max_cycles = 5
    simulate_round = 1

    result = simulate_cycles(character, max_cycles, simulate_round)

    assert "Simulate Round No." in result
    assert "DMG" in result
    assert "DMG_Type" in result
    assert len(result["Simulate Round No."]) == len(result["DMG"])
    assert all(round_no == simulate_round for round_no in result["Simulate Round No."])


def test_simulate_cycles_for_character_with_summon():
    character = MockCharacter()
    summon = MockCharacter()
    max_cycles = 5
    simulate_round = 1

    result = simulate_cycles_for_character_with_summon(
        character, summon, max_cycles, simulate_round
    )

    assert "Simulate Round No." in result
    assert "DMG" in result
    assert "DMG_Type" in result
    assert len(result["Simulate Round No."]) == len(result["DMG"])
    assert all(round_no == simulate_round for round_no in result["Simulate Round No."])


def test_simulate_cycles_with_zero_cycles():
    """Test simulation with zero cycles"""
    character = MockCharacter()
    result = simulate_cycles(character, max_cycles=0, simulate_round=1)

    assert len(result["DMG"]) == 0
    assert len(result["DMG_Type"]) == 0
    assert len(result["Simulate Round No."]) == 0


def test_character_stats_initialization():
    """Test character stats initialization for different character types"""
    characters = [
        Boothill(),  # Tests break_effect setting
        BlackSwan(),  # Tests effect_hit_rate setting
        MockCharacter(),  # Tests default case
    ]

    for character in characters:
        result = simulate_cycles(character, max_cycles=5, simulate_round=1)
        assert "DMG" in result
        assert "DMG_Type" in result
        assert "Simulate Round No." in result


def test_summon_initialization():
    """Test summon initialization for characters with summons"""
    # Test Topaz with Numby
    topaz = Topaz()
    numby = topaz.summon_numby(topaz)
    result = simulate_cycles_for_character_with_summon(
        topaz, numby, max_cycles=5, simulate_round=1
    )

    assert len(result["DMG"]) > 0
    assert len(result["DMG_Type"]) > 0
    assert all(round_no == 1 for round_no in result["Simulate Round No."])

    # Test Jingyuan with Lightning Lord
    jingyuan = Jingyuan()
    lightning_lord = jingyuan.summon_lightning_lord(jingyuan)
    result = simulate_cycles_for_character_with_summon(
        jingyuan, lightning_lord, max_cycles=5, simulate_round=1
    )

    assert len(result["DMG"]) > 0
    assert len(result["DMG_Type"]) > 0
    assert all(round_no == 1 for round_no in result["Simulate Round No."])


def test_cycles_action_value_calculation():
    """Test cycles action value calculation"""
    character = MockCharacter()

    # Test with different max_cycles values
    test_cases = [
        (1, 150),  # min cycles
        (5, 550),  # mid cycles
        (10, 1050),  # max cycles
    ]

    for max_cycles, expected_action_val in test_cases:
        result = simulate_cycles(character, max_cycles, simulate_round=1)
        assert (
            len(result["DMG"]) > 0
        )  # Should have some actions with the given action value


def test_data_reset_between_battles():
    """Test that character data is properly reset between battles"""
    character = MockCharacter()

    # Run first simulation
    result1 = simulate_cycles(character, max_cycles=5, simulate_round=1)

    # Run second simulation
    result2 = simulate_cycles(character, max_cycles=5, simulate_round=2)

    # Check that data was reset properly
    assert len(result1["DMG"]) == len(result1["Simulate Round No."])
    assert len(result2["DMG"]) == len(result2["Simulate Round No."])
    assert all(round_no == 1 for round_no in result1["Simulate Round No."])
    assert all(round_no == 2 for round_no in result2["Simulate Round No."])


if __name__ == "__main__":
    pytest.main()
