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


class DrRatio(Character):
    def __init__(self,
                 base_char: Character,
                 speed=103,
                 ult_energy=140
                 ):
        super().__init__(atk=base_char.default_atk, crit_rate=base_char.default_crit_rate,
                         crit_dmg=base_char.crit_dmg, speed=speed, ult_energy=ult_energy)
        self.debuff_on_enemy = []

    def reset_character_data(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f'Resetting {self.__class__.__name__} data...')
        super().reset_character_data()
        self.debuff_on_enemy = []

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # reset stats
        self.crit_rate = 0.5
        self.crit_dmg = 1

        # simulate applying debuff on enemy by allies
        debuff_num = random.choice([1, 2, 3])
        for _ in range(debuff_num):
            self.debuff_on_enemy.append('debuff')

        # simulate enemy turn
        if len(self.debuff_on_enemy) > 0:
            self.debuff_on_enemy.pop(0)
        if self.weakness_broken:
            if self.enemy_turn_delayed_duration_weakness_broken > 0:
                self.enemy_turn_delayed_duration_weakness_broken -= 1
            else:
                self.regenerate_enemy_toughness()

        if self.skill_points > 0:
            self._use_skill()
            self._simulate_talent()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

            self.current_ult_energy = 5

        # simulate ult debuff
        if 'wiseman_folly' in self.debuff_on_enemy:
            self.debuff_on_enemy.remove('wiseman_folly')
            ally_atk_num = random.choice([1, 2])
            for _ in range(ally_atk_num):
                self._follow_up_atk()

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info("Using basic attack...")
        dmg = self._calculate_damage(skill_multiplier=1, break_amount=10)
        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info("Using skill...")

        # simulate A2 Trace
        crit_rate_multiplier = 0.025
        crit_dmg_multiplier = 0.05
        self.crit_rate += min(crit_rate_multiplier * 6, crit_rate_multiplier * len(self.debuff_on_enemy))
        self.crit_dmg += min(crit_dmg_multiplier * 6, crit_dmg_multiplier * len(self.debuff_on_enemy))

        # simulate A6 Trace
        if len(self.debuff_on_enemy) >= 3:
            multiplier = min(0.1 * len(self.debuff_on_enemy), 0.5)
        else:
            multiplier = 0

        dmg = self._calculate_damage(skill_multiplier=1.5, break_amount=20, dmg_multipliers=[multiplier])
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info('Using ultimate...')

        self.debuff_on_enemy.append('wiseman_folly')
        self.debuff_on_enemy.append('wiseman_folly')

        ult_dmg = self._calculate_damage(skill_multiplier=2.4, break_amount=30)

        self.data['DMG'].append(ult_dmg)
        self.data['DMG_Type'].append('Ultimate')

    def _follow_up_atk(self) -> None:
        """
        Simulate follow-up attack damage.
        :return: None
        """
        main_logger.info('Using follow-up attack...')
        dmg = self._calculate_damage(skill_multiplier=2.7, break_amount=10)
        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=5)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Talent')

    def _simulate_talent(self) -> None:
        """
        Simulate talent.
        :return: None
        """
        main_logger.info('Simulating talent...')
        follow_up_chance = 0.4 + (0.2 * len(self.debuff_on_enemy))
        final_follow_up_chance = min(1.0, follow_up_chance)
        if random.random() < final_follow_up_chance:
            self._follow_up_atk()

    def check_if_enemy_weakness_broken(self, break_type: str = 'None') -> None:
        """
        Check whether enemy is weakness broken.
        :param break_type: Break DMG type, e.g., Physical, Fire, etc.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__}: Checking Enemy Toughness...')
        if self.current_enemy_toughness <= 0 and not self.weakness_broken:
            self.enemy_turn_delayed_duration_weakness_broken = 1
            self.weakness_broken = True
            self.debuff_on_enemy.append('debuff')
            main_logger.debug(f'{self.__class__.__name__}: Enemy is Weakness Broken')
