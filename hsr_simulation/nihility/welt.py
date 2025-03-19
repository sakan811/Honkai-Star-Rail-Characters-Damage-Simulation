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
    calculate_total_damage,
    calculate_res_multipliers,
    calculate_def_multipliers,
)


class Welt(Character):
    def __init__(self, speed: float = 102, ult_energy: int = 120):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.enemy_slowed = 0
        self.imprisoned = 0
        self.a2_buff = 0

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f"Resetting {self.__class__.__name__} data...")
        super().reset_character_data_for_each_battle()
        self.enemy_slowed = 0
        self.imprisoned = 0
        self.a2_buff = 0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        # simulate enemy turn
        self._simulate_enemy_weakness_broken()

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

            self.current_ult_energy = 5

            # simulate A4 trace
            self.current_ult_energy += 10

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        dmg_multiplier = self._apply_a2_trace()
        dmg = self._calculate_damage(
            skill_multiplier=1, break_amount=10, dmg_multipliers=dmg_multiplier
        )

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self._record_damage(dmg, "Basic ATK")

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        num_hit = 3
        for _ in range(num_hit):
            dmg_multiplier = self._apply_a2_trace()
            dmg = self._calculate_damage(
                skill_multiplier=0.72, break_amount=10, dmg_multipliers=dmg_multiplier
            )
            self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

            self._record_damage(dmg, "Skill")

            # simulate Talent
            if random.random() < 0.75:
                self.enemy_slowed = 2

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")
        dmg_multiplier = self._apply_a2_trace()

        dmg = self._calculate_damage(
            skill_multiplier=1.5, break_amount=20, dmg_multipliers=dmg_multiplier
        )

        self._record_damage(dmg, "Ultimate")

        self._apply_talent_dmg()

        self.a2_buff = 2

    def _apply_a2_trace(self):
        """
        Simulate a2 trace damage buff.
        """
        main_logger.info(f"{self.__class__.__name__} is applying a2 trace...")
        dmg_multiplier = [0]
        if self.a2_buff > 0:
            dmg_multiplier.append(0.12)
        return dmg_multiplier

    def _apply_talent_dmg(self) -> None:
        """
        Apply Talent DMG
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is applying Talent DMG...")
        if self.enemy_slowed > 0 or self.imprisoned > 0:
            dmg_multiplier = self._apply_a2_trace()
            dmg = self._calculate_damage(
                skill_multiplier=0.6, break_amount=0, dmg_multipliers=dmg_multiplier
            )
            self._record_damage(dmg, "Talent")

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

        if self.enemy_weakness_broken:
            # simulate A6 trace
            dmg_multipliers.append(0.2)

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
