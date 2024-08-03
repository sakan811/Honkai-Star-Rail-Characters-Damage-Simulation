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
from hsr_simulation.dmg_calculator import calculate_base_dmg, calculate_dmg_multipliers, \
    calculate_total_damage, calculate_universal_dmg_reduction, calculate_res_multipliers, calculate_break_damage

script_logger = configure_logging_with_file(log_dir='logs', log_file='character.log',
                                            logger_name='character', level='DEBUG')


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
            'DMG_Type': [],
            'Simulate Round No.': []
        }
        self.battle_start = True
        self.effect_hit_rate = 0
        self.chance_of_certain_enemy_weakness = 0.14  # the chance of enemy being weak to a certain element
        self.char_action_value = []

    def clear_data(self):
        script_logger.info(f'Clearing {self.__class__.__name__} data dictionary...')
        self.data = {
            'DMG': [],
            'DMG_Type': [],
            'Simulate Round No.': []
        }

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')
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
        script_logger.info(f"{self.__class__.__name__} is using basic attack...")
        dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10)
        self.enemy_toughness -= break_amount

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        script_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg, break_amount = self._calculate_damage(skill_multiplier=2, break_amount=20)
        self.enemy_toughness -= break_amount

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        script_logger.info(f'{self.__class__.__name__} is using ultimate...')
        dmg, break_amount = self._calculate_damage(skill_multiplier=4, break_amount=30)
        self.enemy_toughness -= break_amount

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

    def is_enemy_weakness_broken(self) -> bool:
        """
        Check whether enemy is weakness broken.
        :return: Weakness broken indicator
        """
        script_logger.info(f'{self.__class__.__name__}: Checking Enemy Toughness...')
        if self.enemy_toughness <= 0:
            script_logger.debug(f'{self.__class__.__name__}: Weakness Broken')
            self.enemy_toughness = 50
            return True
        return False

    def do_break_dmg(self, break_type: str = 'None') -> None:
        """
        Do break damage if enemy is weakness broken.
        :param break_type: Break type, e.g., Physical, Fire, etc.
        :return: None
        """
        script_logger.info(f'{self.__class__.__name__}: Doing break damage...')
        if self.is_enemy_weakness_broken():
            break_dmg = calculate_break_damage(break_type=break_type, target_max_toughness=self.enemy_toughness)
        else:
            break_dmg = 0

        self.data['DMG'].append(break_dmg)
        self.data['DMG_Type'].append('Break DMG')

    def _calculate_damage(
            self,
            skill_multiplier: float,
            break_amount: int,
            dmg_multipliers: list[float] = None,
            res_multipliers: list[float] = None,
            can_crit: bool = True) -> tuple[float, int]:
        """
        Calculates damage based on multipliers.
        :param skill_multiplier: Skill multiplier.
        :param break_amount: Break amount that the attack can do.
        :param dmg_multipliers: DMG multipliers.
        :param res_multipliers: RES multipliers.
        :param can_crit: Whether the DMG can CRIT.
        :return: Damage and break amount.
        """
        script_logger.info(f'{self.__class__.__name__}: Calculating damage...')
        weakness_broken = self.is_enemy_weakness_broken()
        if random.random() < self.crit_rate and can_crit:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=skill_multiplier)
            dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg, dmg_multipliers=dmg_multipliers)
        else:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=skill_multiplier)
            dmg_multiplier = calculate_dmg_multipliers(dmg_multipliers=dmg_multipliers)

        dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
        res_multiplier = calculate_res_multipliers(res_multipliers)
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
        script_logger.info(f'{self.__class__.__name__}: Updating skill points and ultimate energy...')
        self.skill_points += skill_points
        self.current_ult_energy += ult_energy

    def set_break_effect(self, min_break: float, max_break: float) -> None:
        """
        Set break effect for some characters.
        :param min_break: Min break effect.
        :param max_break: Max break effect.
        :return: None
        """
        script_logger.info(f'{self.__class__.__name__}: Setting break effect...')
        break_effect = random.uniform(min_break, max_break)
        self.break_effect = break_effect

    def random_enemy_toughness(self) -> None:
        script_logger.info(f'{self.__class__.__name__}: Randomizing enemy toughness...')
        self.enemy_toughness = random.randint(60, 200)

    def start_battle(self) -> None:
        """
        Indicate that the battle starts.
        :return: None
        """
        script_logger.info(f"{self.__class__.__name__}: Battle starts...")
        self.battle_start = True

    def set_effect_hit_rate(self, min_effect_hit_rate, max_effect_hit_rate) -> None:
        """
        Set effect hit rate for the character.
        :return: None
        """
        script_logger.info(f'{self.__class__.__name__}: Set effect hit rate...')
        effect_hit_rate = random.uniform(min_effect_hit_rate, max_effect_hit_rate)
        self.effect_hit_rate = effect_hit_rate

    def simulate_action_forward(self, action_forward_percent: float) -> float:
        """
        Simulate action forward.
        :param action_forward_percent: Action forward percent.
        :return: Action value
        """
        script_logger.info(f'Simulate action forward {action_forward_percent * 100}%...')
        script_logger.debug(f'{self.__class__.__name__} current speed: {self.speed}')
        action_value = self.calculate_action_value(self.speed)
        script_logger.debug(f'{self.__class__.__name__}: Current Action value {action_value}')
        return action_value * action_forward_percent

    def calculate_action_value(self, speed: float) -> float:
        """
        Calculate action value
        :param speed: Character speed
        :return: Action value
        """
        script_logger.info(f'Calculating action value...')
        return 10000 / speed