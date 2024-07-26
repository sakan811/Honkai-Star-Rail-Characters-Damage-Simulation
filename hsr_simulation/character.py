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
import sqlite3

import pandas as pd

from configure_logging import configure_logging_with_file
from hsr_simulation.dmg_calculator import calculate_base_dmg, calculate_dmg_multipliers, \
    calculate_total_damage, calculate_universal_dmg_reduction, calculate_res_multipliers, calculate_break_damage

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
        self.atk = atk
        self.crit_rate = crit_rate
        self.crit_dmg = crit_dmg
        self.speed = speed
        self.skill_points = 3
        self.ult_energy = ult_energy
        self.current_ult_energy = 0
        self.enemy_toughness = 50
        self.break_effect = 1
        self.data = {
            'DMG': [],
            'DMG_Type': []
        }
        self.db_path = 'hsr_char_action_dmg.db'

    def take_action(self) -> float:
        """
        Simulate taking actions.
        :return: Total damage.
        """
        logger.info('Taking actions...')
        total_dmg = []

        if self.skill_points > 0:
            dmg = self._use_skill()
            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Skill')
        else:
            dmg = self._use_basic_atk()
            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Basic ATK')

        total_dmg.append(dmg)

        if self._can_use_ult():
            ult_dmg = self._use_ult()
            total_dmg.append(ult_dmg)

            self.data['DMG'].append(ult_dmg)
            self.data['DMG_Type'].append('Ultimate')

            self.current_ult_energy = 5

        return sum(total_dmg)

    def is_enemy_weakness_broken(self) -> bool:
        """
        Check whether enemy is weakness broken.
        :return: Weakness broken indicator
        """
        logger.info('Checking Enemy Toughness...')
        if self.enemy_toughness <= 0:
            logger.debug('Weakness Broken')
            self.enemy_toughness = 50
            return True
        return False

    def _use_basic_atk(self) -> float:
        """
        Simulate basic atk damage.
        :return: Damage.
        """
        logger.info("Using basic attack...")
        dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10)
        self.enemy_toughness -= break_amount

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)
        return dmg

    def do_break_dmg(self, dmg: float, break_type: str = 'None') -> float:
        """
        Do break damage if enemy is weakness broken.
        :param dmg: DMG to be added with break damage.
        :param break_type: Break type, e.g., Physical, Fire, etc.
        :return: Total DMG
        """
        logger.info('Doing break damage...')
        if self.is_enemy_weakness_broken():
            break_dmg = calculate_break_damage(break_type=break_type, target_max_toughness=self.enemy_toughness)
        else:
            break_dmg = 0
        dmg += break_dmg
        return dmg

    def _use_skill(self) -> float:
        """
        Simulate skill damage.
        :return: Damage .
        """
        logger.info("Using skill...")
        dmg, break_amount = self._calculate_damage(skill_multiplier=2, break_amount=20)
        self.enemy_toughness -= break_amount

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)
        return dmg

    def _use_ult(self) -> float:
        """
        Simulate ultimate damage.
        :return: Damage and break amount.
        """
        logger.info('Using ultimate...')
        dmg, break_amount = self._calculate_damage(skill_multiplier=4, break_amount=30)
        self.enemy_toughness -= break_amount

        return dmg

    def _calculate_damage(
            self,
            skill_multiplier: float,
            break_amount: int,
            dmg_multipliers: list[float] = None,
            res_multipliers: list[float] = None) -> tuple[float, int]:
        """
        Calculates damage based on skill_multiplier.
        :param skill_multiplier: Skill multiplier.
        :param break_amount: Break amount that the attack can do.
        :param dmg_multipliers: DMG multipliers.
        :param res_multipliers: RES multipliers.
        :return: Damage and break amount.
        """
        logger.info('Calculating damage...')
        weakness_broken = self.is_enemy_weakness_broken()
        if random.random() < self.crit_rate:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=skill_multiplier)
            dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg, dmg_multipliers=dmg_multipliers)
        else:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=skill_multiplier)
            dmg_multiplier = 1

        dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
        res_multiplier = calculate_res_multipliers()
        total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_multiplier, dmg_reduction)

        return total_dmg, break_amount

    def _can_use_ult(self) -> bool:
        return self.current_ult_energy >= self.ult_energy

    def _update_skill_point_and_ult_energy(self, skill_points: int, ult_energy: int) -> None:
        """
        Update skill points and ultimate energy.
        :param skill_points: Skill points.
        :param ult_energy: Ultimate energy.
        :return: None
        """
        logger.info('Updating skill points and ultimate energy...')
        self.skill_points += skill_points
        self.current_ult_energy += ult_energy

    def set_break_effect(self, min_break: float, max_break: float) -> None:
        """
        Set break effect for some characters.
        :param min_break: Min break effect.
        :param max_break: Max break effect.
        :return: None
        """
        logger.info('Setting break effect...')
        break_effect = random.uniform(min_break, max_break)
        self.break_effect = break_effect

    def random_enemy_toughness(self) -> None:
        logger.info('Randomizing enemy toughness...')
        self.enemy_toughness = random.randint(60, 200)

    def add_data_to_table(self):
        with sqlite3.connect(self.db_path) as connection:
            df = pd.DataFrame(self.data)
            df['Character'] = f'{self.__class__.__name__}'
            table_name = f'{self.__class__.__name__}'
            df.to_sql(name=table_name, con=connection, if_exists='replace')