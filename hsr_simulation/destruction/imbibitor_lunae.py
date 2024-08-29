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


class ImbibitorLunae(Character):
    def __init__(
            self,
            speed: float = 102,
            ult_energy: int = 140
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.transcendence = False
        self.divine_spear = False
        self.fulgurant_leap = False
        self.outroar = 0
        self.righteous_heart = 0
        self.squama_sacrosancta = 0

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
        self.transcendence = False
        self.divine_spear = False
        self.fulgurant_leap = False
        self.outroar = 0
        self.righteous_heart = 0
        self.squama_sacrosancta = 0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        self._simulate_enemy_weakness_broken()

        if self.battle_start:
            self.battle_start = False

            # simulate A2 trace
            self.current_ult_energy += 15

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self.transcendence:
            self._use_enhanced_basic_atk(number_of_hits=3, skill_multiplier=2.6, break_amount=30)
        elif self.divine_spear:
            self._use_enhanced_basic_atk(number_of_hits=5, skill_multiplier=3.8, break_amount=35)
        elif self.fulgurant_leap:
            self._use_enhanced_basic_atk(number_of_hits=7, skill_multiplier=5, break_amount=40)

        if self._can_use_ult():
            self._use_ult()

            self.current_ult_energy = 5

        # reset stats after his turn ends
        self.outroar = 0
        self.righteous_heart = 0
        self.crit_dmg = self.default_crit_dmg
        self.transcendence = False
        self.divine_spear = False
        self.fulgurant_leap = False

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")

        # simulate A6 trace
        if random.random() < 0.5:
            self.crit_dmg += 0.24

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

        # simulate A6 trace
        if random.random() < 0.5:
            self.crit_dmg += 0.24

        skill_point_used = random.choice([1, 2, 3])

        if skill_point_used == 1:
            self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)
            self.transcendence = True
        elif skill_point_used == 2:
            self._update_skill_point_and_ult_energy(skill_points=-2, ult_energy=35)
            self.divine_spear = True
        elif skill_point_used == 3:
            self._update_skill_point_and_ult_energy(skill_points=-3, ult_energy=40)
            self.fulgurant_leap = True

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using ultimate...')
        hit_num = 3
        skill_multiplier = 3
        skill_multiplier_for_each_hit = skill_multiplier / hit_num
        break_amount_for_each_hit = 20 // hit_num

        # simulate A6 trace
        if random.random() < 0.5:
            self.crit_dmg += 0.24

        for _ in range(hit_num):
            dmg_multiplier = self._gain_righteous_buffs()

            dmg = self._calculate_damage(skill_multiplier=skill_multiplier_for_each_hit,
                                         break_amount=break_amount_for_each_hit, dmg_multipliers=[dmg_multiplier])

            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Ultimate')

        self.squama_sacrosancta = 2
        self.skill_points += self.squama_sacrosancta
        self.squama_sacrosancta = 0

    def _use_enhanced_basic_atk(self, number_of_hits: int, skill_multiplier: float, break_amount: int) -> None:
        """
        Simulate enhanced basic atk damage.
        :param number_of_hits: Number of hits.
        :param skill_multiplier: Skill multiplier.
        :param break_amount: Break amount.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using enhanced basic attack...")
        skill_multiplier_for_each_hit = skill_multiplier / number_of_hits
        break_amount_for_each_hit = break_amount // number_of_hits

        for _ in range(number_of_hits):
            if number_of_hits >= 5:
                self._gain_outroar_buffs()

            dmg_multiplier = self._gain_righteous_buffs()

            dmg = self._calculate_damage(skill_multiplier=skill_multiplier_for_each_hit,
                                         break_amount=break_amount_for_each_hit, dmg_multipliers=[dmg_multiplier])
            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Enhanced Basic ATK')

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=40)

    def _gain_outroar_buffs(self) -> None:
        """
        Gain Outroar buffs to the character.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is gaining Outroar buffs...')
        self.outroar += 1
        self.outroar = min(self.outroar, 4)

        if self.outroar > 0:
            self.crit_dmg += 0.12 * self.outroar

    def _gain_righteous_buffs(self) -> float:
        """
        Gain Righteous Heart buffs to the character.
        :return: DMG multiplier.
        """
        main_logger.info(f'{self.__class__.__name__} is gaining Righteous Heart buffs...')

        self.righteous_heart += 1
        self.righteous_heart = min(self.righteous_heart, 6)

        dmg_multiplier = 0
        if self.righteous_heart > 0:
            dmg_multiplier = 0.1 * self.righteous_heart

        return dmg_multiplier
