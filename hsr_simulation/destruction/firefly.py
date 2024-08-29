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


class FireFly(Character):
    def __init__(
            self,
            speed: float = 104,
            ult_energy: int = 240
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.complete_combustion_state = False
        self.complete_combustion_state_duration = 0

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
        self.complete_combustion_state = False
        self.complete_combustion_state_duration = 0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        self._simulate_enemy_weakness_broken()

        if self.battle_start:
            self.battle_start = False
            self.current_ult_energy = int(0.5 * self.current_ult_energy)

            # simulate A6 trace
            self._simulate_a6_trace()

        # reset stats before taking actions
        self.char_action_value_for_action_forward = []

        if self.complete_combustion_state_duration > 0:
            self.complete_combustion_state_duration -= 1

        if self.skill_points > 0 and not self.complete_combustion_state:
            self._use_skill()
        elif self.skill_points > 0 and self.complete_combustion_state:
            self._use_enhanced_skill()
        elif self.skill_points <= 0 and self.complete_combustion_state:
            self._use_enhanced_basic_atk()
        else:
            self._use_basic_atk()

        if self._can_use_ult() and not self.complete_combustion_state:
            self._use_ult()
            self.current_ult_energy = 5

        # reset stats when Complete Combustion state ends
        if self.complete_combustion_state_duration <= 0:
            self.complete_combustion_state = False
            self.speed = self.default_speed

    def _simulate_a6_trace(self) -> None:
        """
        Simulate A6 trace effect.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is simulating A6 trace...")
        multiplier = (self.atk - 1800) / 10
        self.break_effect *= 1 + (0.008 * multiplier)

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        break_amount = int(10 * self.break_effect)
        dmg = self._calculate_damage(skill_multiplier=1, break_amount=break_amount)

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_enhanced_basic_atk(self) -> None:
        """
        Simulate enhanced basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using enhanced basic attack...")
        base_break_amount = 15
        break_effect = self.break_effect + 0.5
        break_amount = int(base_break_amount * break_effect)
        dmg = self._calculate_damage(skill_multiplier=1.5, break_amount=break_amount)

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=0)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Enhanced Basic ATK')

        self._simulate_a4_trace(break_amount)

    def _simulate_a4_trace(self, break_amount) -> None:
        """
        Simulate A4 trace damage.
        :param break_amount: Amount of toughness reduction from an attack
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is simulating A4 trace...")
        if self.enemy_weakness_broken:
            super_break_dmg = self._deal_super_break_dmg(enemy_toughness_reduction=break_amount,
                                                         break_effect=self.break_effect)
            if self.break_effect >= 3.6:
                super_break_dmg *= 0.5
            elif 2 <= self.break_effect < 3.6:
                super_break_dmg *= 0.35
            else:
                super_break_dmg = 0

            # simulate Ult effect
            super_break_dmg *= 1.2

            self.data['DMG'].append(super_break_dmg)
            self.data['DMG_Type'].append('Super Break DMG')

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        break_amount = int(20 * self.break_effect)
        dmg = self._calculate_damage(skill_multiplier=2, break_amount=break_amount)

        ult_energy = int(self.ult_energy * 0.6)
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=ult_energy)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

    def _use_enhanced_skill(self) -> None:
        """
        Simulate enhanced skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using enhanced skill...")
        skill_multiplier = (0.2 * self.break_effect) + 2
        base_break_amount = 30
        break_effect = self.break_effect + 0.5
        break_amount = int(base_break_amount * break_effect)
        dmg = self._calculate_damage(skill_multiplier=skill_multiplier, break_amount=break_amount)

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=0)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Enhanced Skill')

        self._simulate_a4_trace(break_amount)

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using ultimate...')
        self.char_action_value_for_action_forward.append(self.simulate_action_forward(1))
        self.complete_combustion_state = True
        self.speed += 60
        self.complete_combustion_state_duration = 2


