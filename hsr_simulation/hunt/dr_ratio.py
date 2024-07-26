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

from configure_logging import configure_logging_with_file
from hsr_simulation.character import Character

logger = configure_logging_with_file('simulate_turns.log')


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

    def take_action(self) -> float:
        """
        Simulate taking actions.
        :return: Total damage.
        """
        logger.info('Taking actions...')
        total_dmg = []

        # reset stats
        self.crit_rate = 0.5
        self.crit_dmg = 1

        if self.skill_points > 0:
            dmg, break_amount = self._use_skill()
            self.enemy_toughness -= break_amount
            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Skill')

            follow_up_dmg, follow_up_atk_break_amount = self._simulate_talent()
            self.enemy_toughness -= follow_up_atk_break_amount
            self.data['DMG'].append(follow_up_dmg)
            self.data['DMG_Type'].append('Talent')

            dmg += follow_up_dmg
        else:
            dmg, break_amount = self._use_basic_atk()
            self.enemy_toughness -= break_amount
            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Basic ATK')

        total_dmg.append(dmg)

        if self._can_use_ult():
            ult_dmg, ult_break_amount = self._use_ult()
            self.enemy_toughness -= ult_break_amount
            total_dmg.append(ult_dmg)

            self.data['DMG'].append(ult_dmg)
            self.data['DMG_Type'].append('Ultimate')

            self.current_ult_energy = 5

        # simulate ult debuff
        if self.wiseman_folly > 0:
            self.wiseman_folly -= 1

            ally_atk_num = random.choice([1, 2])
            for _ in range(ally_atk_num):
                dmg, break_amount = self._follow_up_atk()
                self.enemy_toughness -= break_amount

                self.data['DMG'].append(dmg)
                self.data['DMG_Type'].append('Talent')

                total_dmg.append(dmg)

        return sum(total_dmg)

    def _use_basic_atk(self) -> tuple[float, int]:
        """
        Simulate basic atk damage.
        :return: Damage and break amount.
        """
        logger.info("Using basic attack...")
        dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10)
        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)
        return dmg, break_amount

    def _use_skill(self) -> tuple[float, int]:
        """
        Simulate skill damage.
        :return: Damage and break amount.
        """
        logger.info("Using skill...")

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
        return dmg, break_amount

    def _use_ult(self) -> tuple[float, int]:
        """
        Simulate ultimate damage.
        :return: Damage and break amount.
        """
        logger.info('Using ultimate...')
        self.wiseman_folly = 2
        return self._calculate_damage(skill_multiplier=2.4, break_amount=30)

    def _follow_up_atk(self) -> tuple[float, int]:
        """
        Simulate follow-up attack damage.
        :return: Damage and break amount.
        """
        logger.info('Using follow-up attack...')
        dmg, break_amount = self._calculate_damage(skill_multiplier=2.7, break_amount=10)
        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=5)
        return dmg, break_amount

    def _simulate_talent(self) -> tuple[float, int]:
        """
        Simulate talent.
        :return: Damage and break amount.
        """
        logger.info('Simulating talent...')
        if self.wiseman_folly > 0:
            debuff_on_enemy = random.choice([1, 2, 3])
            if random.random() < 0.4 + (0.2 * debuff_on_enemy):
                return self._follow_up_atk()
            else:
                return 0, 0
        else:
            debuff_on_enemy = random.choice([0, 1, 2, 3])
            if random.random() < 0.4 + (0.2 * debuff_on_enemy):
                return self._follow_up_atk()
            else:
                return 0, 0