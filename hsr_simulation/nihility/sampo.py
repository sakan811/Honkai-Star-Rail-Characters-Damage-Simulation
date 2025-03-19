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


class Sampo(Character):
    def __init__(self, speed: float = 102, ult_energy: int = 120):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.ult_buff = 0
        self.wind_shear = []

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f"Resetting {self.__class__.__name__} data...")
        super().reset_character_data_for_each_battle()
        self.wind_shear = []
        self.ult_buff = 0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        # simulate applying Wind Shear on enemy turn
        self._apply_wind_shear_dmg()

        # simulate enemy turn
        self._simulate_enemy_weakness_broken()

        # simulate debuffs on enemy
        if self.ult_buff > 0:
            self.ult_buff -= 1
        if len(self.wind_shear) > 0:
            self.wind_shear[0] -= 1
            if self.wind_shear[0] == 0:
                self.wind_shear = []

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
        dmg = self._calculate_damage(skill_multiplier=1, break_amount=10)

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self._record_damage(dmg, "Basic ATK")

        self._inflict_wind_shear()

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=0)
        hit_num = 5
        for _ in range(hit_num):
            dmg = self._calculate_damage(skill_multiplier=0.56, break_amount=10)

            self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=6)

            self._record_damage(dmg, "Skill")

        self._inflict_wind_shear()

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")
        dmg = self._calculate_damage(skill_multiplier=1.6, break_amount=20)

        self._record_damage(dmg, "Ultimate")

        self.ult_buff = 2

        self._inflict_wind_shear()

    def _inflict_wind_shear(self) -> None:
        """
        Inflict Wind Shear DoT stack
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is inflicting Wind Shear...")
        if random.random() < 0.65:
            # ensure Wind Shear stacks not exceed 5
            if len(self.wind_shear) < 5:
                base_wind_shear_duration = 3

                # simulate A2 trace
                base_wind_shear_duration += 1

                self.wind_shear.append(base_wind_shear_duration)

    def _apply_wind_shear_dmg(self) -> None:
        """
        Apply Wind Shear DoT damage
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__}: Wind Shear is dealing damage...")
        hit_num = len(self.wind_shear)
        # apply Wind Shear DMG by the number of Wind Shear stacks
        for _ in range(hit_num):
            # simulate Ult DoT buff
            dot_dmg_multiplier = [0]
            if self.ult_buff > 0:
                dot_dmg_multiplier += [0.3]

            dmg = self._calculate_damage(
                skill_multiplier=0.52,
                break_amount=0,
                dot_dmg_multipliers=dot_dmg_multiplier,
                can_crit=False,
            )

            self._record_damage(dmg, "DoT")
