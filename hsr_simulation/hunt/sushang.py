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


class Sushang(Character):
    def __init__(self, atk=2000, crit_rate=0.5, crit_dmg=1, speed=107, ult_energy=120):
        super().__init__(atk, crit_rate, crit_dmg, speed, ult_energy)
        self.talent_spd_buff = 0
        self.starting_spd = speed
        self.ult_buff = 0
        self.a4_trace_buff = 0

    def take_action(self) -> float:
        """
        Simulate taking actions.
        :return: Total damage.
        """
        logger.info('Taking actions...')
        total_dmg = []

        # reset stats when begins a new action
        self.speed = self.starting_spd
        self.a4_trace_buff = 0

        # talend speed buff only lasts for 2 turns
        if self.talent_spd_buff > 0:
            self.speed = self.starting_spd * 1.2
            self.talent_spd_buff -= 1
        else:
            self.speed = self.starting_spd

        if self.is_enemy_weakness_broken():
            self.speed = self.starting_spd * 1.2
            self.talent_spd_buff = 2

        if self.skill_points > 0:
            dmg, break_amount = self._use_skill()

            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Skill')

            # simulate ultimate buff
            if self.ult_buff > 0:
                self.ult_buff -= 1

                total_sword_stance_dmg = []

                sword_stance_dmg, break_amount = self._handle_sword_stance()
                sword_stance_dmg = self._handle_a4_trace(sword_stance_dmg)

                self.enemy_toughness -= break_amount

                total_sword_stance_dmg.append(sword_stance_dmg)

                # extra Sword Stance
                for _ in range(2):
                    sword_stance_dmg, break_amount = self._handle_sword_stance(is_extra=True)
                    sword_stance_dmg = self._handle_a4_trace(sword_stance_dmg)

                    self.enemy_toughness -= break_amount

                    total_sword_stance_dmg.append(sword_stance_dmg)

                sword_stance_dmg = sum(total_sword_stance_dmg)

                self.data['DMG'].append(sword_stance_dmg)
                self.data['DMG_Type'].append('Talent')
            else:
                sword_stance_dmg, break_amount = self._handle_sword_stance()
                sword_stance_dmg = self._handle_a4_trace(sword_stance_dmg)

                self.data['DMG'].append(sword_stance_dmg)
                self.data['DMG_Type'].append('Talent')

                self.enemy_toughness -= break_amount

            dmg += sword_stance_dmg
        else:
            dmg, break_amount = self._use_basic_atk()
            self.enemy_toughness -= break_amount

            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Basic ATK')

        self.enemy_toughness -= break_amount

        total_dmg.append(dmg)

        # After using skill or basic ATK, if enemy is weakness broken, Sushang's action forward
        if self.is_enemy_weakness_broken():
            self.speed *= 1.15

        if self._can_use_ult():
            ult_dmg, ult_break_amount = self._use_ult()
            self.enemy_toughness -= ult_break_amount

            total_dmg.append(ult_dmg)

            self.data['DMG'].append(ult_dmg)
            self.data['DMG_Type'].append('Ultimate')

            self.current_ult_energy = 5

            self.ult_buff = 2

            # action again
            self.speed *= 2

        return sum(total_dmg)

    def _handle_a4_trace(self, sword_stance_dmg) -> float:
        logger.info('Handling A4 Trace buff...')
        if sword_stance_dmg > 0:
            self.a4_trace_buff += 1
            sword_stance_dmg *= (1 + (2.5 * self.a4_trace_buff))
        return sword_stance_dmg

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
        dmg, break_amount = self._calculate_damage(skill_multiplier=2.1, break_amount=20)
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)
        return dmg, break_amount

    def _use_ult(self) -> tuple[float, int]:
        """
        Simulate ultimate damage.
        :return: Damage and break amount.
        """
        logger.info('Using ultimate...')
        return self._calculate_damage(skill_multiplier=3.2, break_amount=30)

    def _handle_sword_stance(self, is_extra: bool = False) -> tuple[float, int]:
        """
        Simulate sword stance damage.
        :param is_extra: Whether the sword stance is an extra trigger.
        :return: Damage and break amount.
        """
        logger.info("Using sword stance...")
        if self.is_enemy_weakness_broken():
            return self._calculate_damage(skill_multiplier=1, break_amount=0)
        else:
            if random.random() < 0.33:
                if is_extra:
                    return self._calculate_damage(skill_multiplier=0.5, break_amount=0)
                else:
                    return self._calculate_damage(skill_multiplier=1, break_amount=0)
            else:
                return 0, 0
