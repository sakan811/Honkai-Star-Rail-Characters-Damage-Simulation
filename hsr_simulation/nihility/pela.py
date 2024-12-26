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


class Pela(Character):
    def __init__(
            self,
            speed: float = 105,
            ult_energy: int = 110
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.enemy_has_buff = False
        self.a6_buff = False
        self.exposed = 0
        self.a2_multiplier = 0.2

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f'Resetting {self.__class__.__name__} data...')
        super().reset_character_data_for_each_battle()
        self.enemy_has_buff = False
        self.a6_buff = False
        self.exposed = 0
        self.a2_multiplier = 0.2

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # random debuff on enemy
        self.enemy_has_buff = random.choice([True, False])

        # simulate enemy turn
        self._simulate_enemy_weakness_broken()

        # simulate enemy turn
        if self.exposed > 0:
            self.exposed -= 1

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        dmg_multipler = 0
        if self.exposed > 0:
            dmg_multipler += 0.4 + self.a2_multiplier
            self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=10)

        if self.a6_buff:
            dmg_multipler += 0.2
            self.a6_buff = False

        dmg = self._calculate_damage(skill_multiplier=1, break_amount=10, dmg_multipliers=[dmg_multipler])

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self._record_damage(dmg, 'Basic ATK')

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg_multipler = 0
        if self.exposed > 0:
            dmg_multipler += 0.4 + self.a2_multiplier
            self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=10)

        if self.a6_buff:
            dmg_multipler += 0.2
            self.a6_buff = False

        dmg = self._calculate_damage(skill_multiplier=2.1, break_amount=20,
                                     dmg_multipliers=[dmg_multipler])

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self._record_damage(dmg, 'Skill')

        # A6 trace
        if self.enemy_has_buff:
            self.a6_buff = True

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using ultimate...')
        self.current_ult_energy = 5

        dmg_multipler = 0

        if self.exposed > 0:
            dmg_multipler += 0.4 + self.a2_multiplier
            self.current_ult_energy += 10

        if self.a6_buff:
            dmg_multipler += 0.2
            self.a6_buff = False

        dmg = self._calculate_damage(skill_multiplier=1, break_amount=20, dmg_multipliers=[dmg_multipler])

        self._record_damage(dmg, 'Ultimate')

        self.exposed = 2
