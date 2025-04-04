#    Copyright 2024 Sakan Nirattisaykul
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import random

from hsr_simulation.configure_logging import main_logger
from hsr_simulation.dmg_calculator import (
    calculate_base_dmg,
    calculate_dmg_multipliers,
    calculate_total_damage,
    calculate_universal_dmg_reduction,
    calculate_res_multipliers,
    calculate_break_damage,
    calculate_def_multipliers,
    calculate_super_break_dmg,
)


class Character:
    """
    Base Character class.
    Provide methods for taking actions, e.g., Skill, Basic ATK, Ultimate, etc.
    It also includes methods for calculating damage, managing skill points and ultimate energy,
    and handling various battle-related states.
    """

    # Constants for default values
    DEFAULT_ENEMY_TOUGHNESS = 100
    DEFAULT_SKILL_POINTS = 1
    DEFAULT_BREAK_EFFECT = 1
    DEFAULT_EFFECT_HIT_RATE = 0
    DEFAULT_ULT_ENERGY_AFTER_ULT = 5
    ACTION_VALUE_BASE = 10000

    # Constants for skill multipliers and break amounts
    BASIC_ATK_MULTIPLIER = 1
    BASIC_ATK_BREAK_AMOUNT = 10
    SKILL_MULTIPLIER = 2
    SKILL_BREAK_AMOUNT = 20
    ULT_MULTIPLIER = 4
    ULT_BREAK_AMOUNT = 30

    # Constants for energy gains
    BASIC_ATK_ENERGY_GAIN = 20
    SKILL_ENERGY_GAIN = 30

    def __init__(
        self,
        atk: float = 2000,
        crit_rate: float = 0.5,
        crit_dmg: float = 1.0,
        speed: float = 90,
        ult_energy: int = 140,
    ):
        # Initialize default stats
        self._init_default_stats(atk, crit_rate, crit_dmg, speed, ult_energy)
        # Initialize current stats
        self._init_current_stats()
        # Initialize enemy stats
        self._init_enemy_stats()
        # Initialize battle data
        self._init_battle_data()

    def _init_default_stats(self, atk, crit_rate, crit_dmg, speed, ult_energy) -> None:
        """Initialize default character statistics"""
        self.default_atk = atk
        self.default_crit_rate = crit_rate
        self.default_crit_dmg = crit_dmg
        self.default_speed = speed
        self.default_ult_energy = ult_energy
        self.default_enemy_weakness_broken = False
        self.default_skill_points = self.DEFAULT_SKILL_POINTS
        self.default_break_effect = self.DEFAULT_BREAK_EFFECT
        self.default_effect_hit_rate = self.DEFAULT_EFFECT_HIT_RATE

    def _init_current_stats(self) -> None:
        """Initialize current character statistics"""
        self.atk = self.default_atk
        self.crit_rate = self.default_crit_rate
        self.crit_dmg = self.default_crit_dmg
        self.speed = self.default_speed
        self.skill_points = self.default_skill_points
        self.ult_energy = self.default_ult_energy
        self.current_ult_energy = 0
        self.break_effect = self.default_break_effect
        self.effect_hit_rate = self.default_effect_hit_rate
        self.summon_action_value_for_action_forward = []

    def _init_enemy_stats(self) -> None:
        """Initialize enemy-related statistics"""
        self.default_enemy_toughness = self.DEFAULT_ENEMY_TOUGHNESS
        self.enemy_toughness = self.default_enemy_toughness
        self.current_enemy_toughness = self.enemy_toughness
        self.enemy_turn_delayed_duration_weakness_broken = 0
        self.enemy_weakness_broken = self.default_enemy_weakness_broken

    def _init_battle_data(self) -> None:
        """Initialize battle-related data"""
        self.data: dict[str, list[float | str | int]] = {
            "DMG": [],
            "DMG_Type": [],
            "Simulate Round No.": [],
        }
        self.battle_start: bool = True
        self.char_action_value_for_action_forward: list[float] = []
        self.char_action_value: float = 0.0

    def _record_damage(self, dmg: float, dmg_type: str) -> None:
        """Record damage and its type in battle data"""
        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append(dmg_type)

    def reset_summon_stat_for_each_turn(self) -> None:
        """
        Reset Summon stats for each turn.
        :return: None
        """
        main_logger.info(f"Resetting {self.__class__.__name__} stats ...")
        self.summon_action_value_for_action_forward = []

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data,
        to ensure the character starts with default stats and battle-related data,
        in each battle simulation.
        :return: None
        """
        main_logger.info(f"Resetting {self.__class__.__name__} data...")
        # character stats
        self.atk = self.default_atk
        self.crit_rate = self.default_crit_rate
        self.crit_dmg = self.default_crit_dmg
        self.speed = self.default_speed
        self.skill_points = self.default_skill_points
        self.ult_energy = self.default_ult_energy
        self.current_ult_energy = 0
        self.break_effect = 1
        self.effect_hit_rate = 0

        # enemy-related stats
        self.enemy_toughness = self.default_enemy_toughness
        self.current_enemy_toughness = self.enemy_toughness
        self.enemy_turn_delayed_duration_weakness_broken = 0
        self.enemy_weakness_broken = self.default_enemy_weakness_broken

        # dictionary for storing character actions
        self.data: dict[str, list[float | str | int]] = {
            "DMG": [],
            "DMG_Type": [],
            "Simulate Round No.": [],
        }

        # other stats
        self.battle_start: bool = True
        self.char_action_value_for_action_forward: list[float] = []
        self.char_action_value: float = 0.0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")
        self._simulate_enemy_weakness_broken()

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

    def _use_basic_atk(self) -> None:
        """Simulate basic attack damage."""
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        dmg = self._calculate_damage(
            skill_multiplier=self.BASIC_ATK_MULTIPLIER,
            break_amount=self.BASIC_ATK_BREAK_AMOUNT,
        )
        self._update_skill_point_and_ult_energy(1, self.BASIC_ATK_ENERGY_GAIN)
        self._record_damage(dmg, "Basic ATK")

    def _use_skill(self) -> None:
        """Simulate skill damage."""
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg = self._calculate_damage(
            skill_multiplier=self.SKILL_MULTIPLIER, break_amount=self.SKILL_BREAK_AMOUNT
        )
        self._update_skill_point_and_ult_energy(-1, self.SKILL_ENERGY_GAIN)
        self._record_damage(dmg, "Skill")

    def _use_ult(self) -> None:
        """Simulate ultimate damage."""
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")
        dmg = self._calculate_damage(
            skill_multiplier=self.ULT_MULTIPLIER, break_amount=self.ULT_BREAK_AMOUNT
        )
        self._record_damage(dmg, "Ultimate")
        self.current_ult_energy = self.DEFAULT_ULT_ENERGY_AFTER_ULT

    def check_if_enemy_weakness_broken(self) -> None:
        """
        Check whether enemy is weakness broken.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__}: Checking Enemy Toughness...")
        if self.current_enemy_toughness <= 0 and not self.enemy_weakness_broken:
            self.enemy_turn_delayed_duration_weakness_broken = 1
            self.enemy_weakness_broken = True
            main_logger.debug(f"{self.__class__.__name__}: Enemy is Weakness Broken")

    def regenerate_enemy_toughness(self) -> None:
        """
        Regenerate enemy toughness after it was weakness-broken
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__}: Regenerate enemy toughness...")
        self.current_enemy_toughness = self.enemy_toughness
        self.enemy_weakness_broken = False

    def do_break_dmg(self, break_type: str = "None") -> float:
        """
        Do break damage if enemy is weakness broken.
        :param break_type: Break type, e.g., Physical, Fire, etc.
        :return: Break damage.
        """
        main_logger.info(f"{self.__class__.__name__}: Doing break damage...")
        break_dmg = calculate_break_damage(
            break_type=break_type, target_max_toughness=self.enemy_toughness
        )

        break_dmg *= self.break_effect

        return break_dmg

    def _calculate_damage(
        self,
        skill_multiplier: float,
        break_amount: int,
        dmg_multipliers: list[float] = None,
        dot_dmg_multipliers: list[float] = None,
        res_multipliers: list[float] = None,
        def_reduction_multiplier: list[float] = None,
        can_crit: bool = True,
    ) -> float:
        """
        Calculates damage based on multipliers.
        :param skill_multiplier: Skill multiplier.
        :param break_amount: Break amount that the attack can do.
        :param dmg_multipliers: DMG multipliers.
        :param dot_dmg_multipliers: Dot DMG multipliers.
        :param res_multipliers: RES multipliers.
        :param def_reduction_multiplier: DEF reduction multipliers.
        :param can_crit: Whether the DMG can CRIT.
        :return: Damage.
        """
        main_logger.info(f"{self.__class__.__name__}: Calculating damage...")
        # reduce enemy toughness
        self.current_enemy_toughness -= break_amount

        self.check_if_enemy_weakness_broken()

        base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=skill_multiplier)

        if random.random() < self.crit_rate and can_crit:
            dmg_multiplier = calculate_dmg_multipliers(
                crit_dmg=self.crit_dmg, dmg_multipliers=dmg_multipliers
            )
        else:
            dmg_multiplier = calculate_dmg_multipliers(
                dmg_multipliers=dmg_multipliers, dot_dmg=dot_dmg_multipliers
            )

        dmg_reduction = calculate_universal_dmg_reduction(self.enemy_weakness_broken)
        def_reduction = calculate_def_multipliers(
            def_reduction_multiplier=def_reduction_multiplier
        )
        res_multiplier = calculate_res_multipliers(res_multipliers)

        total_dmg = calculate_total_damage(
            base_dmg=base_dmg,
            dmg_multipliers=dmg_multiplier,
            res_multipliers=res_multiplier,
            dmg_reduction=dmg_reduction,
            def_reduction_multiplier=def_reduction,
        )

        return total_dmg

    def _can_use_ult(self) -> bool:
        return self.current_ult_energy >= self.ult_energy

    def _update_skill_point_and_ult_energy(
        self, skill_points: int, ult_energy: int
    ) -> None:
        """
        Update skill points and ultimate energy.
        :param skill_points: Skill points.
        :param ult_energy: Ultimate energy.
        :return: None
        """
        main_logger.info(
            f"{self.__class__.__name__}: Updating skill points and ultimate energy..."
        )
        self.skill_points += skill_points
        self.current_ult_energy += ult_energy

    def set_break_effect(self, min_break: float, max_break: float) -> None:
        """
        Set break effect for some characters.
        :param min_break: Min break effect.
        :param max_break: Max break effect.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__}: Setting break effect...")
        break_effect = random.choice([min_break, max_break])
        self.break_effect = break_effect

    def start_battle(self) -> None:
        """
        Indicate that the battle starts.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__}: Battle starts...")
        self.battle_start = True

    def set_effect_hit_rate(self, min_effect_hit_rate, max_effect_hit_rate) -> None:
        """
        Set effect hit rate for the character.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__}: Set effect hit rate...")
        effect_hit_rate = random.choice([min_effect_hit_rate, max_effect_hit_rate])
        self.effect_hit_rate = effect_hit_rate

    def simulate_action_forward(self, action_forward_percent: float) -> float:
        """
        Simulate action forward.
        :param action_forward_percent: Action forward percent as a float.
        :return: Action value to be added back to the total cycles action value to simulate
                character's action forward.
        """
        main_logger.info(f"Simulate action forward {action_forward_percent * 100}%...")
        main_logger.debug(f"{self.__class__.__name__} current speed: {self.speed}")
        main_logger.debug(
            f"{self.__class__.__name__} action value before taking action: {self.char_action_value}"
        )
        current_char_action_value: float = self.char_action_value
        return current_char_action_value * action_forward_percent

    def calculate_action_value(self, speed: float) -> float:
        """Calculate action value based on speed"""
        main_logger.info("Calculating action value...")
        char_action_value = self.ACTION_VALUE_BASE / speed
        self.char_action_value = char_action_value
        return char_action_value

    def _simulate_enemy_weakness_broken(self) -> None:
        """
        Simulate when the enemy is weakness broken.
        If enemy weakness is broken, its action should be delayed for 1 turn.
        :return: None
        """
        main_logger.info(
            f"{self.__class__.__name__}: Simulate when enemy is weakness broken..."
        )
        if self.enemy_weakness_broken:
            if self.enemy_turn_delayed_duration_weakness_broken > 0:
                self.enemy_turn_delayed_duration_weakness_broken -= 1
            else:
                self.regenerate_enemy_toughness()

    def _deal_super_break_dmg(
        self, enemy_toughness_reduction: int, break_effect: float
    ) -> float:
        """
        Deal super break damage.
        :param enemy_toughness_reduction: Enemy toughness reduction from an attack.
        :param break_effect: Break Effect
        :return: Super Break DMG
        """
        main_logger.info(f"{self.__class__.__name__}: Dealing super break damage...")
        return calculate_super_break_dmg(enemy_toughness_reduction, break_effect)
