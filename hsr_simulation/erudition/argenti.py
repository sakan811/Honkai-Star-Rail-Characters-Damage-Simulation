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


class Argenti(Character):
    def __init__(
            self,
            speed: float = 103,
            ult_energy: int = 180
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.ult_energy_to_consume = random.choices([90, 180], weights=[0.2, 0.8])[0]
        self.apotheosis = 0
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
        self.ult_energy_to_consume = random.choices([90, 180], weights=[0.2, 0.8])[0]
        self.apotheosis = 0
        self.enemy_on_field = random.choice([1, 2, 3, 4, 5])

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        self._simulate_enemy_weakness_broken()

        # simulate A4 trace
        self.current_ult_energy += 2 * self.enemy_on_field

        if self.battle_start:
            self.battle_start = False
            self.apotheosis += 1

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()
            self.current_ult_energy -= self.ult_energy_to_consume
            self.current_ult_energy += 5

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        dmg_multiplier = self._simulate_a6_trace()

        self._simulate_num_enemy_hits()

        single_target_dmg = self._calculate_damage(skill_multiplier=1, break_amount=10, dmg_multipliers=[dmg_multiplier])

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(single_target_dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg_multiplier = self._simulate_a6_trace()

        self._simulate_num_enemy_hits()

        dmg = self._calculate_damage(skill_multiplier=1.2, break_amount=10, dmg_multipliers=[dmg_multiplier])

        # other target DMG
        for _ in range(self.enemy_on_field - 1):
            dmg += self._calculate_damage(skill_multiplier=1.2, break_amount=10, dmg_multipliers=[dmg_multiplier])

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using ultimate...')
        dmg_multiplier = self._simulate_a6_trace()

        self._simulate_num_enemy_hits()

        dmg = 0
        if self.ult_energy_to_consume == 90:
            dmg = self._calculate_damage(skill_multiplier=1.6, break_amount=20, dmg_multipliers=[dmg_multiplier])

            # other target DMG
            for _ in range(self.enemy_on_field - 1):
                dmg += self._calculate_damage(skill_multiplier=1.6, break_amount=20, dmg_multipliers=[dmg_multiplier])
        elif self.ult_energy_to_consume == 180:
            dmg = self._calculate_damage(skill_multiplier=2.8, break_amount=20, dmg_multipliers=[dmg_multiplier])

            # other target DMG
            for _ in range(self.enemy_on_field - 1):
                dmg += self._calculate_damage(skill_multiplier=2.8, break_amount=20, dmg_multipliers=[dmg_multiplier])

            # extra hits
            num_hit = 6
            for _ in range(num_hit):
                dmg += self._calculate_damage(skill_multiplier=0.95, break_amount=2, dmg_multipliers=[dmg_multiplier])

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

    def _can_use_ult(self) -> bool:
        return self.current_ult_energy >= self.ult_energy_to_consume

    def _simulate_num_enemy_hits(self) -> None:
        """
        Simulate the number of enemies being hit.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__}: simulate number of enemy being hit by this character...')
        num_hits = self.enemy_on_field
        self.current_ult_energy += 3 * num_hits

        self.apotheosis += num_hits
        self.apotheosis = min(self.apotheosis, 10)

        self.crit_rate = self.default_crit_rate * (1 + (0.025 * self.apotheosis))

    def _simulate_a6_trace(self) -> float:
        """
        Simulate A6 Trace.
        :return: DMG Multiplier
        """
        main_logger.info(f'{self.__class__.__name__}: simulate A6 Trace...')
        current_enemy_hp = random.choice([True, False])
        if current_enemy_hp:
            return 0.15
        else:
            return 0
