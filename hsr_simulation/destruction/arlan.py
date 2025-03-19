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

from hsr_simulation.character import Character
from hsr_simulation.configure_logging import main_logger


class Arlan(Character):
    def __init__(self, speed: float = 102, ult_energy: int = 110):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.default_hp: int = 3600
        self.current_hp: int = self.default_hp

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
        self.default_hp: int = 3600

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

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        hp_cost = self.default_atk * 0.15
        if self.current_hp > hp_cost:
            self.current_hp -= hp_cost
        else:
            self.current_hp = 1
        dmg = self._calculate_damage(skill_multiplier=2.4, break_amount=20)
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Skill")

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")
        single_target_dmg = self._calculate_damage(
            skill_multiplier=3.2, break_amount=20
        )

        self.data["DMG"].append(single_target_dmg)
        self.data["DMG_Type"].append("Ultimate")

    def _apply_talent_effect(self) -> None:
        """
        Apply talent effect to increase damage based on missing HP.
        :return: None
        """
        missing_hp_percent = (self.default_hp - self.current_hp) / self.default_hp
        dmg_increase = min(missing_hp_percent * 0.72, 0.72)
        self.atk *= 1 + dmg_increase
