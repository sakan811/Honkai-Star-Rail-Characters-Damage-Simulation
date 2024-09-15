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


class Jade(Character):
    def __init__(
            self,
            speed: float = 103,
            ult_energy: int = 140
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.debt_collector = 0
        self.ult_buff = 0
        self.charge = 0
        self.pawned_asset = 0
        self.enemy_on_field = random.choice([1, 2, 3, 4, 5])
        self.enemy_enter_battle = random.choice([0, 1, 2, 3, 4, 5])
        self.num_of_enemy_being_hit = random.choice([1, 2, 3, 4, 5])

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
        self.debt_collector = 0
        self.ult_buff = 0
        self.charge = 0
        self.pawned_asset = 0
        self.enemy_on_field = random.choice([1, 2, 3, 4, 5])
        self.enemy_enter_battle = random.choice([0, 1, 2, 3, 4, 5])
        self.num_of_enemy_being_hit = random.choice([1, 2, 3, 4, 5])

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # reset stats for each action
        self.char_action_value_for_action_forward = []

        if self.battle_start:
            self.battle_start = False
            self.char_action_value_for_action_forward.append(self.simulate_action_forward(0.5))

        self._simulate_enemy_weakness_broken()

        # simulate enemies enter battle
        self.pawned_asset += self.enemy_enter_battle
        self.pawned_asset = min(self.pawned_asset, 50)

        # simulate A6 trace
        self._gain_atk_buff()

        # simulate Debt Collector turn
        if self.debt_collector > 0:
            self._debt_collector_dmg()
            # simulate A2 trace
            self.pawned_asset += 3
            self.pawned_asset = min(self.pawned_asset, 50)
        if self.charge >= 8:
            self._use_follow_up_atk()

        if self.debt_collector > 0:
            self.debt_collector -= 1

        if self.skill_points > 0 >= self.debt_collector:
            self._use_skill()
        else:
            self._use_basic_atk()
            if self.charge >= 8:
                self._use_follow_up_atk()

        if self._can_use_ult():
            self._use_ult()
            self.current_ult_energy = 5

            if self.charge >= 8:
                self._use_follow_up_atk()

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        self._gain_crit_dmg_buff()

        dmg = self._calculate_damage(skill_multiplier=0.9, break_amount=10)

        # adjacent target DMG
        adjacent_target = min(self.enemy_on_field - 1, 2)
        for _ in range(adjacent_target):
            dmg += self._calculate_damage(skill_multiplier=0.3, break_amount=5)

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

        self._gain_charge(target_num=3)

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)
        self.debt_collector = 3

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using ultimate...')
        self._gain_crit_dmg_buff()

        dmg = self._calculate_damage(skill_multiplier=2.4, break_amount=20)
        for _ in range(self.enemy_on_field - 1):
            dmg += self._calculate_damage(skill_multiplier=2.4, break_amount=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

        self.ult_buff = 2

        self._gain_charge(target_num=self.enemy_on_field)

    def _debt_collector_dmg(self) -> None:
        """
        Simulate Debt Collector damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using Debt Collector...')
        dmg = self._calculate_damage(skill_multiplier=0.25, break_amount=0)

        # simulate AoE attack from Debt Collector
        if random.random() < 0.5:
            for _ in range(self.enemy_on_field - 1):
                dmg += self._calculate_damage(skill_multiplier=0.25, break_amount=0)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

        self._gain_charge(target_num=self.num_of_enemy_being_hit)

    def _use_follow_up_atk(self) -> None:
        """
        Simulate Follow-up attack damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using Follow-up attack...')
        self._gain_crit_dmg_buff()

        skill_multiplier = 1.2

        if self.ult_buff > 0:
            skill_multiplier += 0.8
            self.ult_buff -= 1

        dmg = self._calculate_damage(skill_multiplier=skill_multiplier, break_amount=10)

        # other target DMG
        for _ in range(self.enemy_on_field - 1):
            dmg += self._calculate_damage(skill_multiplier=skill_multiplier, break_amount=10)

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=10)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Talent')

        self.pawned_asset += 5
        self.pawned_asset = min(self.pawned_asset, 50)

        self.charge = 0

    def _gain_crit_dmg_buff(self) -> None:
        """
        Simulate gaining Critical Damage buff.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is gaining Critical Damage buff...')
        self.crit_dmg = self.default_crit_dmg + (0.024 * self.pawned_asset)

    def _gain_charge(self, target_num: int) -> None:
        """
        Simulate gaining Charge.
        :param target_num: Number of targets being hit.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is gaining Charge...')
        self.charge += target_num
        self.charge = min(self.charge, 8)

    def _gain_atk_buff(self) -> None:
        """
        Simulate gaining ATK buff.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is gaining ATK buff...')
        self.atk = self.default_atk + (0.005 * self.pawned_asset)
