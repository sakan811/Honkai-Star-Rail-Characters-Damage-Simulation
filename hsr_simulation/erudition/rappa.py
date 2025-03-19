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

from hsr_simulation.character import Character
from hsr_simulation.configure_logging import main_logger


class Rappa(Character):
    def __init__(self, speed: float = 96, ult_energy: int = 140):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.enemy_on_field = random.choice([1, 2, 3, 4, 5])
        self.sealform = False
        self.chroma_ink = 0
        self.charge = 0
        self.a6_trace_buff = 0

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data,
        to ensure the character starts with default stats and battle-related data,
        in each battle simulation.
        :return: None
        """
        main_logger.info(f"Resetting {self.__class__.__name__} data...")
        super().reset_character_data_for_each_battle()
        self.enemy_on_field = random.choice([1, 2, 3, 4, 5])
        self.sealform = False
        self.chroma_ink = 0
        self.charge = 0
        self.a6_trace_buff = 0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")
        self._simulate_enemy_weakness_broken()

        if self.a6_trace_buff > 0:
            self.a6_trace_buff -= 1

        # reset stats
        self.char_action_value_for_action_forward = []

        # reset stats after exit Sealform
        if self.chroma_ink <= 0:
            self.sealform = False
            self.break_effect = self.default_break_effect

        if self.skill_points > 0 and not self.sealform:
            self._use_skill()
        elif self.sealform and self.chroma_ink > 0:
            self._use_enhanced_basic_atk()
        else:
            self._use_basic_atk()

        if self._can_use_ult() and not self.sealform:
            self._use_ult()
            self.current_ult_energy = 5

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        dmg = self._calculate_damage(skill_multiplier=1, break_amount=10)

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Basic ATK")

    def _use_enhanced_basic_atk(self) -> None:
        """
        Simulate enhanced basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using enhanced basic attack...")
        self.chroma_ink -= 1

        dmg = 0
        for _ in range(2):
            dmg += self._calculate_damage(skill_multiplier=1, break_amount=10)
            self._simulate_a4_trace(enemy_toughness_reduction=10)

            # adjacent target DMG
            adjacent_target = min(self.enemy_on_field - 1, 2)
            for _ in range(adjacent_target):
                dmg += self._calculate_damage(skill_multiplier=0.5, break_amount=10)
                self._simulate_a4_trace(enemy_toughness_reduction=10)

        # final hit
        dmg += self._calculate_damage(skill_multiplier=1, break_amount=5)
        self._simulate_a4_trace(enemy_toughness_reduction=5)

        # other target DMG
        for _ in range(self.enemy_on_field - 1):
            dmg += self._calculate_damage(skill_multiplier=1, break_amount=5)
            self._simulate_a4_trace(enemy_toughness_reduction=5)

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=20)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Enhanced Basic ATK")

        self._simulate_talent_dmg()

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg = self._calculate_damage(skill_multiplier=1.2, break_amount=10)

        # other target DMG
        for _ in range(self.enemy_on_field - 1):
            dmg += self._calculate_damage(skill_multiplier=1.2, break_amount=10)

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Skill")

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")
        self.sealform = True
        self.chroma_ink = 3
        self.break_effect += 0.3
        self.char_action_value_for_action_forward.append(
            self.simulate_action_forward(1)
        )

    def check_if_enemy_weakness_broken(self) -> None:
        """
        Check whether enemy is weakness broken.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__}: Checking Enemy Toughness...")
        if self.current_enemy_toughness <= 0 and not self.enemy_weakness_broken:
            self.enemy_turn_delayed_duration_weakness_broken = 1
            self.enemy_weakness_broken = True

            # simulate Talent
            self.charge += 1

            # simulate A2 trace
            if random.random() < 0.5:
                self.charge += 1
                self.current_ult_energy += 10

            self.charge = min(self.charge, 10)

            main_logger.debug(f"{self.__class__.__name__}: Enemy is Weakness Broken")

    def _simulate_talent_dmg(self) -> None:
        """
        Simulate talent damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__}: Simulating talent damage...")
        dmg = self.do_break_dmg(break_type="Imaginary") * 0.6
        dmg *= 1 + (0.5 * self.charge)

        # simulate A6 trace
        if self.a6_trace_buff > 0:
            additional_break_dmg_multiplier = 0
            if self.atk > 2400:
                excess_atk = (self.atk - 2400) // 100
                additional_break_dmg_multiplier = 0.01 * excess_atk
                additional_break_dmg_multiplier = min(
                    additional_break_dmg_multiplier, 0.08
                )

            dmg *= 1 + (0.02 + additional_break_dmg_multiplier)

        base_toughness_reduction = 2
        additional_toughness_reduction = 1 * self.charge

        toughness_reduction = additional_toughness_reduction + base_toughness_reduction

        self._calculate_damage(skill_multiplier=0, break_amount=toughness_reduction)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Talent")

        self.charge = 0

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

    def _simulate_a4_trace(self, enemy_toughness_reduction: int) -> None:
        """
        Simulate A4 trace.
        :param enemy_toughness_reduction: Enemy toughness reduction from an attack
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__}: Simulating A4 trace...")
        if self.enemy_weakness_broken:
            dmg = self._deal_super_break_dmg(
                enemy_toughness_reduction=enemy_toughness_reduction,
                break_effect=self.break_effect,
            )
            dmg *= 0.6

            self.data["DMG"].append(dmg)
            self.data["DMG_Type"].append("Super Break DMG")
