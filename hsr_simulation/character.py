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
from hsr_simulation.dmg_calculator import calculate_base_dmg, calculate_dmg_multipliers, \
    calculate_total_damage, calculate_universal_dmg_reduction

logger = configure_logging_with_file('simulate_turns.log')


class Character:
    def __init__(
            self,
            atk: int = 2000,
            crit_rate: float = 0.5,
            crit_dmg: float = 1.0,
            speed: float = 90,
            ult_energy: int = 140
    ):
        """
        Initialize the character.
        :param atk: Attack.
        :param crit_rate: Critical rate.
        :param crit_dmg: Critical damage.
        :param speed: Speed.
        :param ult_energy: Ultimate energy.
        """
        self.atk = atk
        self.crit_rate = crit_rate
        self.crit_dmg = crit_dmg
        self.speed = speed
        self.skill_points = 3
        self.ult_energy = ult_energy
        self.current_ult_energy = 0
        self.enemy_toughness = 50
        self.break_effect = 1

    def take_action(self) -> float:
        """
        Simulate character's action
        :return: Damage
        """
        total_dmg = []
        logger.info('Taking actions...')
        if self.skill_points > 0:
            skill_dmg, break_amount = self.use_skill(self.check_enemy_toughness())
            logger.debug(f'Skill dmg: {skill_dmg}')

            self.skill_points -= 1
            self.current_ult_energy += 30

            self.enemy_toughness -= break_amount

            total_dmg.append(skill_dmg)
        else:
            basic_atk_dmg, break_amount = self.basic_atk(self.check_enemy_toughness())
            logger.debug(f'Basic atk dmg: {basic_atk_dmg}')

            self.skill_points += 1
            self.current_ult_energy += 10

            self.enemy_toughness -= break_amount

            total_dmg.append(basic_atk_dmg)

        if self.current_ult_energy >= self.ult_energy:
            ult_dmg, break_amount = self.use_ult(self.check_enemy_toughness())
            logger.debug(f'ult dmg: {ult_dmg}')

            total_dmg.append(ult_dmg)

            self.enemy_toughness -= break_amount

            self.current_ult_energy = 5

        return sum(total_dmg)

    def check_enemy_toughness(self) -> bool:
        """
        Check enemy toughness.
        :return: Weakness Broken Indicator
        """
        logger.info('Checking Enemy Toughness...')
        if self.enemy_toughness <= 0:
            logger.debug('Weakness Broken')
            weakness_broken = True
            self.enemy_toughness = 50
        else:
            weakness_broken = False
        return weakness_broken

    def basic_atk(self, weakness_broken: bool) -> tuple[float, int]:
        """
        Basic atk calculation.
        :param weakness_broken: Weakness Broken Indicator.
        :return: Basic atk damage and Break Amount.
        """
        logger.info("Doing a basic atk...")
        break_amount = 20
        if random.random() < self.crit_rate:
            base_dmg = calculate_base_dmg(atk=self.atk)
            dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, dmg_reduction)
            return total_dmg, break_amount
        else:
            base_dmg = calculate_base_dmg(atk=self.atk)
            dmg_multiplier = 1
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, dmg_reduction)
            return total_dmg, break_amount

    def use_skill(self, weakness_broken: bool) -> tuple[float, int]:
        """
        Uses skill.
        :param weakness_broken: Weakness Broken Indicator.
        :return: Damage and Break Amount
        """
        logger.info("Doing a skill attack...")
        break_amount = 10
        if random.random() < self.crit_rate:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=2)
            dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, dmg_reduction)
            return total_dmg, break_amount
        else:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=2)
            dmg_multiplier = 1
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, dmg_reduction)
            return total_dmg, break_amount

    def use_ult(self, weakness_broken: bool) -> tuple[float, int]:
        """
        Uses ultimate skill.
        :param weakness_broken: Weakness Broken Indicator.
        :return: Damage and Break Amount
        """
        logger.info('Using ultimate...')
        break_amount = 20
        if random.random() < self.crit_rate:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=4)
            dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, dmg_reduction)
            return total_dmg, break_amount
        else:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=4)
            dmg_multiplier = 1
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, dmg_reduction)
            return total_dmg, break_amount
