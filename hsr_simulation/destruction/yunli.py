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


class Yunli(Character):
    def __init__(self, speed: float = 94, ult_energy: int = 240):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.is_parry = False
        self.parry_missed = False

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
        self.is_parry = False
        self.parry_missed = False

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        self._simulate_enemy_weakness_broken()

        # simulate being attacked by enemies
        self.current_ult_energy += 15
        self._use_follow_up_atk()

        # simulate Parry from Ultimate
        if self.is_parry:
            parry_success = random.choices([True, False])
            if parry_success:
                self._parry(is_being_attacked=True)
            else:
                self._parry(is_being_attacked=False)

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

            self.current_ult_energy -= 120
            self.current_ult_energy = max(0, self.current_ult_energy)

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
        dmg = self._calculate_damage(skill_multiplier=1.2, break_amount=20)

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Skill")

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")
        self.is_parry = True

    def _can_use_ult(self) -> bool:
        return self.current_ult_energy >= 120

    def _use_follow_up_atk(self) -> None:
        """
        Simulate follow-up attack damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using follow-up attack...")
        # simulate A6 trace
        self.atk = self.default_atk * 1.3

        dmg = self._calculate_damage(skill_multiplier=1.2, break_amount=10)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Talent")

        self.current_ult_energy += 10

        self.atk = self.default_atk

    def _parry(self, is_being_attacked: bool) -> None:
        """
        Simulate parry.
        :param is_being_attacked: Whether the character is being attacked.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is parrying...")
        # simulate A6 trace
        self.atk = self.default_atk * 1.3

        self.crit_dmg += 1

        if is_being_attacked or self.parry_missed:
            self.parry_missed = False
            dmg = self._calculate_damage(skill_multiplier=2.2, break_amount=20)
            hit_num = 6
            for _ in range(hit_num):
                dmg += self._calculate_damage(skill_multiplier=0.72, break_amount=0)
        else:
            dmg = self._calculate_damage(skill_multiplier=2.2, break_amount=20)

            # simulate A2 trace
            self.parry_missed = True

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Ultimate")

        # reset stats after attack
        self.crit_dmg = self.default_crit_dmg
        self.atk = self.default_atk
        self.is_parry = False
