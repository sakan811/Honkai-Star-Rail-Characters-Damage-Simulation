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


class TrailblazerPhysical(Character):
    def __init__(self, speed: float = 100, ult_energy: int = 120):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.talent_buff = 0

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
        self.talent_buff = 0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        self._simulate_enemy_weakness_broken()

        if self.battle_start:
            self.battle_start = False

            # simulate A2 trace
            self.current_ult_energy += 15

        self._increase_atk()

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

            self.current_ult_energy = 5

    def _simulate_talent(self) -> None:
        """
        Simulate talent.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is simulating talent...")
        self.talent_buff += 1
        self.talent_buff = min(self.talent_buff, 2)

        self._increase_atk()

    def _increase_atk(self) -> None:
        """
        Increase attack power from Talent.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is increasing attack power...")
        if self.talent_buff > 0:
            self.atk = self.default_atk * (1 + (0.2 + self.talent_buff))

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
        dmg = self._calculate_damage(skill_multiplier=1.25, break_amount=20)

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Skill")

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")
        # simulate A6 trace
        dmg_multiplier = 0.25

        # randomize between 2 ultimate attack modes
        skill_multiplier = random.choice([4.5, 2.7])
        dmg = self._calculate_damage(
            skill_multiplier=skill_multiplier,
            break_amount=20,
            dmg_multipliers=[dmg_multiplier],
        )

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Ultimate")

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
            self._simulate_talent()
