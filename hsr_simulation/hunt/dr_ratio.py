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

from hsr_simulation.configure_logging import configure_logging_with_file, main_logger
from hsr_simulation.character import Character

script_logger = configure_logging_with_file(log_dir='logs', log_file='dr_ratio.log',
                                          logger_name='dr_ratio', level='DEBUG')


class DrRatio(Character):
    def __init__(self,
                 atk=2000,
                 crit_rate=0.5,
                 crit_dmg=1,
                 speed=103,
                 ult_energy=140
                 ):
        super().__init__(
            atk,
            crit_rate,
            crit_dmg,
            speed,
            ult_energy
        )
        self.wiseman_folly = 0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # reset stats
        self.crit_rate = 0.5
        self.crit_dmg = 1

        if self.skill_points > 0:
            self._use_skill()

            self._simulate_talent()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

            self.current_ult_energy = 5

        # simulate ult debuff
        if self.wiseman_folly > 0:
            self.wiseman_folly -= 1

            ally_atk_num = random.choice([1, 2])
            for _ in range(ally_atk_num):
                self._follow_up_atk()

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        script_logger.info("Using basic attack...")
        dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10)
        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.enemy_toughness -= break_amount

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        script_logger.info("Using skill...")

        # simulate A2 Trace
        debuff_on_enemy = random.choice([0, 1, 2, 3, 4, 5, 6])
        self.crit_rate += 0.025 * debuff_on_enemy
        self.crit_dmg += 0.05 * debuff_on_enemy

        # simulate A6 Trace
        if debuff_on_enemy >= 3:
            multiplier = 0.1 * debuff_on_enemy
            if multiplier > 0.5:
                multiplier = 0.5
        else:
            multiplier = 0

        dmg, break_amount = self._calculate_damage(skill_multiplier=1.5, break_amount=20, dmg_multipliers=[multiplier])
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.enemy_toughness -= break_amount

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        script_logger.info('Using ultimate...')
        self.wiseman_folly = 2
        ult_dmg, break_amount = self._calculate_damage(skill_multiplier=2.4, break_amount=30)

        self.enemy_toughness -= break_amount

        self.data['DMG'].append(ult_dmg)
        self.data['DMG_Type'].append('Ultimate')

    def _follow_up_atk(self) -> None:
        """
        Simulate follow-up attack damage.
        :return: None
        """
        script_logger.info('Using follow-up attack...')
        dmg, break_amount = self._calculate_damage(skill_multiplier=2.7, break_amount=10)
        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=5)

        self.enemy_toughness -= break_amount

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Talent')

    def _simulate_talent(self) -> None:
        """
        Simulate talent.
        :return: None
        """
        script_logger.info('Simulating talent...')
        if self.wiseman_folly > 0:
            debuff_on_enemy = random.choice([1, 2, 3])
            if random.random() < 0.4 + (0.2 * debuff_on_enemy):
                self._follow_up_atk()
        else:
            debuff_on_enemy = random.choice([0, 1, 2, 3])
            if random.random() < 0.4 + (0.2 * debuff_on_enemy):
                self._follow_up_atk()



