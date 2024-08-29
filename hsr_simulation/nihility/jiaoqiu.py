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


class Jiaoqiu(Character):
    def __init__(
            self,
            speed: float = 98,
            ult_energy: int = 100
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)

        self.ashen_roast = []
        self.zone = 0

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
        self.ashen_roast = []
        self.zone = 0

    def _simulate_a4_trace(self) -> None:
        """
        Simulate A4 trace
        """
        main_logger.info(f"{self.__class__.__name__}: Simulate A4 trace...")
        if self.effect_hit_rate < 0.8:
            effect_hit_rate = 0
        else:
            effect_hit_rate = self.effect_hit_rate - 0.8
        main_logger.debug(f'Effect hit rate: {effect_hit_rate}')

        multiplier: float = effect_hit_rate // 0.15
        atk_increase: float = min(0.6 * multiplier, 2.4)
        self.atk = self.default_atk * (1 + atk_increase)

        main_logger.debug(f'Atk: {self.atk}')

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        self._simulate_enemy_turn()

        if self.battle_start:
            self.battle_start = False
            self.current_ult_energy += 15
            self._simulate_a4_trace()

        if self.zone > 0:
            self.zone -= 1

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
        dmg_multiplier = self._apply_talent()
        dmg = self._calculate_damage(skill_multiplier=1, break_amount=10, dmg_multipliers=[dmg_multiplier])

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

        self._inflict_ashen_roast()

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg_multiplier = self._apply_talent()
        dmg = self._calculate_damage(skill_multiplier=1.5, break_amount=20, dmg_multipliers=[dmg_multiplier])

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

        self._inflict_ashen_roast()

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using ultimate...')
        dmg_multiplier = self._apply_talent()
        if self.zone > 0:
            dmg_multiplier += 0.15
        dmg = self._calculate_damage(skill_multiplier=1, break_amount=20, dmg_multipliers=[dmg_multiplier])

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

        self.zone = 3

    def _inflict_ashen_roast(self) -> None:
        """
        Inflict ashen roast stack.
        """
        main_logger.info(f'{self.__class__.__name__} is inflict Ashen Roast...')
        if len(self.ashen_roast) < 5:
            self.ashen_roast.append(2)

    def _apply_talent(self) -> float:
        """
        Simulate talent effect.
        :return: DMG multiplier.
        """
        main_logger.info(f'{self.__class__.__name__} is applying talent...')
        if len(self.ashen_roast) > 0:
            if len(self.ashen_roast) == 1:
                return 0.15
            else:
                return 0.15 + (0.05 * (len(self.ashen_roast) - 1))
        else:
            return 0

    def _apply_burn_dmg(self) -> None:
        """
        Simulate burn damage.
        """
        main_logger.info(f'{self.__class__.__name__} is applying burn damage...')
        if len(self.ashen_roast) > 0:
            dmg_multiplier = self._apply_talent()
            dmg = self._calculate_damage(skill_multiplier=1.8, break_amount=0, dmg_multipliers=[dmg_multiplier],
                                         can_crit=False)

            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('DoT')

    def _simulate_enemy_turn(self) -> None:
        """
        Simulate enemy turn
        """
        main_logger.info(f'{self.__class__.__name__}: simulating enemy turn...')

        main_logger.debug(f'Current Ashen Roast stack on enemy: {len(self.ashen_roast)}')
        self._simulate_enemy_weakness_broken()

        if len(self.ashen_roast) > 0:
            self._apply_burn_dmg()
            self.ashen_roast[0] -= 1
            if self.ashen_roast[0] <= 0:
                self.ashen_roast = []

        # simulate Ult effect
        if self.zone > 0:
            if random.random() < 0.6 * (1 + self.effect_hit_rate):
                self._inflict_ashen_roast()
