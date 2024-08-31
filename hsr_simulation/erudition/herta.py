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


class Herta(Character):
    def __init__(
            self,
            speed: float = 100,
            ult_energy: int = 110
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.enemy_on_field = random.choice([1, 2, 3, 4, 5])

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data,
        to ensure the character starts with default stats and battle-related data,
        in each battle simulation.
        :return: None
        """
        main_logger.info(f'Resetting {self.__class__.__name__} data...')
        super().reset_character_data_for_each_battle()
        self.enemy_on_field = random.choice([1, 2, 3, 4, 5])

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        self._simulate_enemy_weakness_broken()

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        self._simulate_follow_up_atk()

        if self._can_use_ult():
            self._use_ult()
            self.current_ult_energy = 5
            self._simulate_follow_up_atk()

        # simulate ally attacking enemy
        self._simulate_follow_up_atk()

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        dmg = self._calculate_damage(skill_multiplier=1, break_amount=10)

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg_multiplier = 0

        # simulate enemy current HP
        enemy_current_hp_more_than_50_percent = random.choice([True, False])
        if enemy_current_hp_more_than_50_percent:
            dmg_multiplier += 0.2

            # simulate A2 trace
            dmg_multiplier += 0.25

        dmg = self._calculate_damage(skill_multiplier=1, break_amount=10, dmg_multipliers=[dmg_multiplier])

        # other target DMG
        for _ in range(self.enemy_on_field - 1):
            dmg += self._calculate_damage(skill_multiplier=1, break_amount=10, dmg_multipliers=[dmg_multiplier])

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using ultimate...')
        dmg_multiplier = 0

        # simulate A6 trace
        enemy_is_frozen = random.choice([True, False])
        if enemy_is_frozen:
            dmg_multiplier += 0.2

        dmg = self._calculate_damage(skill_multiplier=2, break_amount=20, dmg_multipliers=[dmg_multiplier])

        # other target DMG
        for _ in range(self.enemy_on_field - 1):
            dmg += self._calculate_damage(skill_multiplier=2, break_amount=20, dmg_multipliers=[dmg_multiplier])

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

    def _simulate_follow_up_atk(self) -> None:
        """
        Simulate follow-up attack.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using follow-up attack...")
        # simulate enemy with current HP lower than 50%
        enemy_on_field_list = [i for i in range(1, self.enemy_on_field + 1)]
        enemy_on_field_list.append(0)
        num_enemy_current_hp_less_than_50_percent = random.choice(enemy_on_field_list)

        for _ in range(num_enemy_current_hp_less_than_50_percent):
            dmg = self._calculate_damage(skill_multiplier=0.4, break_amount=5)

            # other target DMG
            for _ in range(num_enemy_current_hp_less_than_50_percent - 1):
                dmg += self._calculate_damage(skill_multiplier=0.4, break_amount=5)

            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Talent')
