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


class Serval(Character):
    def __init__(
            self,
            speed: float = 104,
            ult_energy: int = 100
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.shock = 0
        self.a6_trace_buff = 0
        self.enemy_on_field = random.choice([0, 1, 2, 3, 4, 5])

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
        self.shock = 0
        self.a6_trace_buff = 0
        self.enemy_on_field = random.choice([0, 1, 2, 3, 4, 5])

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # simulate enemy turn
        self._simulate_enemy_weakness_broken()
        if self.shock > 0:
            self.shock -= 1
            self._apply_shock_dmg()

        if self.battle_start:
            self.battle_start = False

            # simulate A4 trace
            self.current_ult_energy += 15

        if self.a6_trace_buff > 0:
            self.a6_trace_buff -= 1
            if self.a6_trace_buff <= 0:
                self.atk = self.default_atk

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        self._simulate_defeating_enemy()

        if self._can_use_ult():
            self._use_ult()
            self.current_ult_energy = 5
            self._simulate_defeating_enemy()

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

        if self.shock > 0:
            self._apply_talent_dmg()

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg = self._calculate_damage(skill_multiplier=1.4, break_amount=20)

        # adjacent target DMG
        adjacent_target = min(self.enemy_on_field - 1, 2)
        for _ in range(adjacent_target):
            dmg += self._calculate_damage(skill_multiplier=0.5, break_amount=10)

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

        base_chance = 0.8

        # simulate A2 trace
        shock_inflicting_chance = base_chance + 0.2

        if random.random() < shock_inflicting_chance:
            self.shock = 2

        if self.shock > 0:
            self._apply_talent_dmg()

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using ultimate...')
        dmg = self._calculate_damage(skill_multiplier=1.8, break_amount=20)

        # other target DMG
        for _ in range(self.enemy_on_field - 1):
            dmg += self._calculate_damage(skill_multiplier=1.8, break_amount=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

        if self.shock > 0:
            self.shock += 2
            self._apply_talent_dmg()

    def _apply_shock_dmg(self) -> None:
        """
        Simulate applying shock damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is applying shock damage...')
        dmg = self._calculate_damage(skill_multiplier=1.04, break_amount=0, can_crit=False)

        # other target DMG
        enemy_on_field = self.enemy_on_field - 1
        for _ in range(enemy_on_field):
            dmg += self._calculate_damage(skill_multiplier=1.04, break_amount=0, can_crit=False)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('DoT')

    def _apply_talent_dmg(self) -> None:
        """
        Simulate applying talent damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is applying talent damage...')
        dmg = self._calculate_damage(skill_multiplier=0.72, break_amount=0)

        # other target DMG
        for _ in range(self.enemy_on_field - 1):
            dmg += self._calculate_damage(skill_multiplier=0.72, break_amount=0)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Talent')

    def _simulate_defeating_enemy(self) -> None:
        """
        Simulate defeating enemy.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is defeating enemy...')
        enemy_defeated = random.choices([True, False], weights=[0.2, 0.8])[0]
        if enemy_defeated:
            self.a6_trace_buff = 2
            self.atk = self.default_atk * 1.2
