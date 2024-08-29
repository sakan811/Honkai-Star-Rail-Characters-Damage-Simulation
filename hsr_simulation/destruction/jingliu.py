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


class Jingliu(Character):
    ATK_MULTIPLIER_OPTIONS: list[float] = [0.6, 1.8]
    MAX_SYZYGY: int = 3
    CRIT_RATE_BONUS: float = 0.5

    def __init__(
            self,
            speed: float = 96,
            ult_energy: int = 140
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)

        self.syzygy: int = 0
        self.atk_multiplier: float = 0
        self.spectral_transmigration: bool = False

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
        self.syzygy: int = 0
        self.atk_multiplier: float = 0
        self.spectral_transmigration: bool = False

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        self._simulate_enemy_weakness_broken()

        # simulate ATK to be increased when using enhanced Skill
        if self.battle_start:
            self.battle_start = False
            self.atk_multiplier = 1 + random.choice(self.ATK_MULTIPLIER_OPTIONS)

        # reset stats for each action
        self.char_action_value_for_action_forward = []

        # exit Spectral Transmigration state when Syzygy stack is 0
        # also reset the CRIT RATE
        if self.syzygy <= 0:
            self.spectral_transmigration = False
            self.crit_rate = self.default_crit_rate

        if self.skill_points > 0 and not self.spectral_transmigration:
            self._use_skill()
        elif self.spectral_transmigration:
            self._use_enhanced_skill()
        elif self.skill_points <= 0 and not self.spectral_transmigration:
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

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg = self._calculate_damage(skill_multiplier=2, break_amount=20)

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

        if self.syzygy < self.MAX_SYZYGY:
            self.syzygy += 1
            if self.syzygy >= 2 and not self.spectral_transmigration:
                self._enter_spectral_transmigration()

        # simulate A4 trace
        action_value: float = self.simulate_action_forward(action_forward_percent=0.1)
        self.char_action_value_for_action_forward.append(action_value)

    def _use_enhanced_skill(self) -> None:
        """
        Simulate enhanced skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        self.atk = self.default_atk * self.atk_multiplier
        self.syzygy -= 1

        dmg = self._calculate_damage(skill_multiplier=2.5, break_amount=20)

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Enhanced Skill')

        self.atk = self.default_atk

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using ultimate...')
        if self.spectral_transmigration:
            self.atk = self.default_atk * self.atk_multiplier
            dmg_multiplier = 0.2
        else:
            dmg_multiplier = 0

        dmg = self._calculate_damage(skill_multiplier=3, break_amount=20, dmg_multipliers=[dmg_multiplier])

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

        if self.syzygy < self.MAX_SYZYGY:
            self.syzygy += 1
            if self.syzygy >= 2 and not self.spectral_transmigration:
                self._enter_spectral_transmigration()

        self.atk = self.default_atk

    def _enter_spectral_transmigration(self) -> None:
        """
        Simulate Spectral Transmigration state.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is entering Spectral Transmigration state...")
        action_value: float = self.simulate_action_forward(action_forward_percent=1)
        self.char_action_value_for_action_forward.append(action_value)
        self.crit_rate = self.default_crit_rate + self.CRIT_RATE_BONUS
        self.spectral_transmigration = True
        self.current_ult_energy += 5
