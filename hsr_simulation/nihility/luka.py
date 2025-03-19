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
from hsr_simulation.dmg_calculator import (
    calculate_base_dmg,
    calculate_dmg_multipliers,
    calculate_universal_dmg_reduction,
    calculate_res_multipliers,
    calculate_total_damage,
    calculate_def_multipliers,
)


class Luka(Character):
    def __init__(self, speed: float = 103, ult_energy: int = 130):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.bleed = 0
        self.fighting_will = 0
        self.ult_buff = 0
        self.enemy_hp = 0

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f"Resetting {self.__class__.__name__} data...")
        super().reset_character_data_for_each_battle()
        self.bleed = 0
        self.fighting_will = 0
        self.ult_buff = 0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        # simulate applying Bleed on enemy turn
        if self.bleed > 0:
            self.bleed -= 1
            self._apply_bleed()

        # simulate enemy turn
        self._simulate_enemy_weakness_broken()

        # simulate Talent
        if self.battle_start:
            self.battle_start = False
            self.fighting_will += 1

        if self.ult_buff > 0:
            self.ult_buff -= 1

        if self.skill_points > 0 and self.fighting_will < 2:
            self._use_skill()
        elif self.fighting_will >= 2:
            self.fighting_will -= 2
            self._use_enhanced_basic_atk()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

            self.current_ult_energy = 5

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        if self.ult_buff > 0:
            dmg = self._calculate_damage(
                skill_multiplier=1, break_amount=10, dmg_multipliers=[0.2]
            )
        else:
            dmg = self._calculate_damage(skill_multiplier=1, break_amount=10)

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self._record_damage(dmg, "Basic ATK")

        self._get_fighting_will(fighting_will_amount=1)

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg = self._calculate_damage(skill_multiplier=1.2, break_amount=20)

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self._record_damage(dmg, "Skill")

        self.bleed = 3
        self._get_fighting_will(fighting_will_amount=1)

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")
        if self.ult_buff > 0:
            dmg = self._calculate_damage(
                skill_multiplier=3.3, break_amount=30, dmg_multipliers=[0.2]
            )
        else:
            dmg = self._calculate_damage(skill_multiplier=3.3, break_amount=30)

        self._record_damage(dmg, "Ultimate")

        self._get_fighting_will(fighting_will_amount=2)
        self.ult_buff = 3

    def _apply_bleed(self, talent_trigger: bool = False) -> None:
        """
        Applying Bleed damage.
        :param talent_trigger: True if talent triggers this Bleed, False otherwise.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is applying bleed...")
        # simulate Bleed Multiplier that comes from enemy HP
        if self.ult_buff > 0:
            dmg = self._calculate_damage(
                break_amount=0, dmg_multipliers=[0.2], can_crit=False, is_bleed=True
            )
        else:
            dmg = self._calculate_damage(break_amount=0, can_crit=False, is_bleed=True)

        if talent_trigger:
            dmg *= 0.85

        self._record_damage(dmg, "DoT")

    def _use_enhanced_basic_atk(self) -> None:
        """
        Simulate enhanced basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using enhanced basic atk...")
        if self.ult_buff > 0:
            dmg_multiplier = [0.2]
        else:
            dmg_multiplier = [0]

        # simulate Direct Punches
        for _ in range(3):
            dmg = self._calculate_damage(
                skill_multiplier=0.2, break_amount=20, dmg_multipliers=dmg_multiplier
            )

            # simulate A6 trace
            if random.random() < 0.5:
                additional_dmg = self._calculate_damage(
                    skill_multiplier=0.2,
                    break_amount=20,
                    dmg_multipliers=dmg_multiplier,
                )
            else:
                additional_dmg = 0
            dmg += additional_dmg

            self._record_damage(dmg, "Enhanced Basic ATK")

        # simulate Rising Uppercut
        dmg = self._calculate_damage(
            skill_multiplier=0.8, break_amount=20, dmg_multipliers=dmg_multiplier
        )

        self._record_damage(dmg, "Enhanced Basic ATK")

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=20)

        # simulate Talent when attacking enemy with Bleed using enhanced basic atk
        if self.bleed > 0:
            self._apply_bleed(talent_trigger=True)

    def _get_fighting_will(self, fighting_will_amount: int) -> None:
        """
        Simulate getting Fighting Will stacks.
        :fighting_will_amount: Amount of fighting will to get.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is getting fighting_will stack...")
        self.fighting_will += fighting_will_amount
        # simulate A4 trace
        self.current_ult_energy += 3
        # ensure Fighting Will stacks not exceed 4
        self.fighting_will = min(4, self.fighting_will)
        main_logger.debug(
            f"{self.__class__.__name__} current fighting_will: {self.fighting_will}"
        )

    def random_enemy_hp(self) -> None:
        """
        Random enemy's HP
        """
        main_logger.info(f"{self.__class__.__name__} is randomizing enemy HP")
        self.enemy_hp = random.choice([480, 28166])
        main_logger.info(f"Enemy HP: {self.enemy_hp}")

    def _calculate_damage(
        self,
        skill_multiplier: float = 0.0,
        break_amount: int = 0,
        dmg_multipliers: list[float] = None,
        dot_dmg_multipliers: list[float] = None,
        res_multipliers: list[float] = None,
        def_reduction_multiplier: list[float] = None,
        can_crit: bool = True,
        is_bleed: bool = False,
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
        :param is_bleed: Whether the DMG is Bleed DMG.
        :return: Damage.
        """
        main_logger.info(f"{self.__class__.__name__}: Calculating damage...")
        # reduce enemy toughness
        self.current_enemy_toughness -= break_amount

        self.check_if_enemy_weakness_broken()

        if is_bleed:
            # ensure that the multiplier not exceeds 338% of ATK
            base_dmg = min(0.24 * self.enemy_hp, 3.38 * self.atk)
        else:
            base_dmg = calculate_base_dmg(
                atk=self.atk, skill_multiplier=skill_multiplier
            )

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
