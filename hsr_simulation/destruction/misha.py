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


class Misha(Character):
    def __init__(self, speed: float = 96, ult_energy: int = 100):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.hit_per_action = 3
        self.enemy_frozen = False

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
        self.hit_per_action = 3
        self.enemy_frozen = False

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        self._simulate_enemy_weakness_broken()

        # simulate ally using skill points
        skill_point_used = random.choice([0, 3])
        self.hit_per_action += skill_point_used

        # simulate Talent
        if skill_point_used > 0:
            self.current_ult_energy += 2 * skill_point_used

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
        dmg = self._calculate_damage(skill_multiplier=2, break_amount=20)

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Skill")

        self.hit_per_action += 1
        self.hit_per_action = min(self.hit_per_action, 10)

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")

        hit_num = self.hit_per_action

        freeze_enemy_chance = 0.2

        for i in range(hit_num):
            if i == 0:
                # simulate A2 trace
                freeze_enemy_chance += 0.8
            else:
                freeze_enemy_chance = 0.2

            # simulate A4 trace
            freeze_enemy_chance *= 1.6

            # attempt to freeze enemy
            if not self.enemy_frozen:
                if random.random() < freeze_enemy_chance:
                    self.enemy_frozen = True

            # simulate A6 trace
            if self.enemy_frozen:
                self.crit_dmg += 0.3

            dmg = self._calculate_damage(skill_multiplier=0.6, break_amount=10)

            self.data["DMG"].append(dmg)
            self.data["DMG_Type"].append("Ultimate")

        self.hit_per_action = 3
        self.crit_dmg = self.default_crit_dmg

    def _simulate_enemy_turn(self) -> None:
        """
        Simulate enemy's turn.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is simulating enemy turn...")
        # simulate enemy turn
        self.check_if_enemy_weakness_broken()
        if self.enemy_frozen:
            self.enemy_frozen = False

            dmg = self._calculate_damage(skill_multiplier=0.3, break_amount=0)

            self.data["DMG"].append(dmg)
            self.data["DMG_Type"].append("Freeze DMG")
