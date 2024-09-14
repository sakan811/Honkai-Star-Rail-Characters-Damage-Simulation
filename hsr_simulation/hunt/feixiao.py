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


class Feixiao(Character):
    def __init__(
            self,
            speed: float = 112,
            ult_energy: int = 0
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.flying_aureus = 0
        self.can_use_talent = True
        self.talent_buff = 0
        self.a6_trace_buff = 0
        self.talent_is_used = False

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
        self.flying_aureus = 0
        self.can_use_talent = True
        self.talent_buff = 0
        self.a6_trace_buff = 0
        self.talent_is_used = False

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')
        self._simulate_enemy_weakness_broken()

        # simulate A2 Trace
        if self.battle_start:
            self.battle_start = False
            self.flying_aureus += 3
        if not self.talent_is_used:
            self._gain_flying_aureus_stack()

        self.can_use_talent = True
        self.talent_is_used = False

        if self.talent_buff > 0:
            self.talent_buff -= 1

        if self.a6_trace_buff > 0:
            self.a6_trace_buff -= 1
            if self.a6_trace_buff == 0:
                self.atk = self.default_atk

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()
            self.flying_aureus -= 6

        # simulate allies attack
        ally_atk_num = random.choices([0, 1, 2, 3, 4, 5, 6], [0.1, 0.5, 0.2, 0.1, 0.05, 0.025, 0.025])[0]

        if ally_atk_num > 0 and self.can_use_talent:
            self._use_follow_up_atk()
            self.can_use_talent = False

        for _ in range(ally_atk_num):
            self._gain_flying_aureus_stack()

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        dmg_multiplier = 0
        if self.talent_buff > 0:
            dmg_multiplier = 0.6

        dmg = self._calculate_damage(skill_multiplier=1, break_amount=10, dmg_multipliers=[dmg_multiplier])

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=0)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

        self._gain_flying_aureus_stack()

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        # simulate A6 trace
        if self.a6_trace_buff <= 0:
            self.a6_trace_buff = 3
            self.atk *= 1.48

        dmg_multiplier = 0
        if self.talent_buff > 0:
            dmg_multiplier = 0.6

        dmg = self._calculate_damage(skill_multiplier=2, break_amount=20, dmg_multipliers=[dmg_multiplier])

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=0)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

        self._use_follow_up_atk()

        self._gain_flying_aureus_stack()

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using ultimate...')

        # simulate A4 trace
        self.crit_dmg += 0.36

        self.break_effect = self.default_break_effect * 2

        dmg_multiplier = 0
        # talent buff
        if self.talent_buff > 0:
            dmg_multiplier += 0.6

        skill_multiplier = random.choice([5.2, 7])
        dmg = self._calculate_damage(skill_multiplier=skill_multiplier, break_amount=int(30 * self.break_effect),
                                     dmg_multipliers=[dmg_multiplier])
        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

        # reset stats after Ultimate
        self.break_effect = self.default_break_effect
        self.crit_dmg = self.default_crit_dmg

    def _can_use_ult(self) -> bool:
        return self.flying_aureus >= 6

    def _use_follow_up_atk(self) -> None:
        """
        Simulate follow-up attack damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using follow-up attack...")
        dmg_multiplier = 0
        if self.talent_buff > 0:
            dmg_multiplier = 0.6

        dmg = self._calculate_damage(skill_multiplier=1.1, break_amount=5, dmg_multipliers=[dmg_multiplier])

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Talent')

        self.talent_buff = 2

        self.talent_is_used = True

        self._gain_flying_aureus_stack()

    def _gain_flying_aureus_stack(self) -> None:
        """
        Gain a stack of Flying Aureus.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is gaining Flying Aureus stack...")
        self.flying_aureus += 0.5
        self.flying_aureus = min(self.flying_aureus, 12)
