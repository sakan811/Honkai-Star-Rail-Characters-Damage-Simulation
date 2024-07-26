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
from hsr_simulation.dmg_calculator import calculate_base_dmg, calculate_universal_dmg_reduction, \
    calculate_dmg_multipliers, calculate_total_damage, calculate_res_multipliers

logger = configure_logging_with_file('simulate_turns.log')


class Seele(Character):
    def __init__(self, atk=2000, crit_rate=0.5, crit_dmg=1, speed=115, ult_energy=120):
        super().__init__(atk, crit_rate, crit_dmg, speed, ult_energy)
        self.sheathed_blade = 0
        self.starting_spd = speed
        self.can_resurgence = True

    def take_action(self) -> float:
        self._reset_stats()
        total_dmg = []
        logger.info('Taking actions...')

        if self.skill_points > 0:
            dmg, break_amount, is_resurgence = self._use_skill()
            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Skill')
        else:
            dmg, break_amount, is_resurgence = self._use_basic_atk()
            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Basic ATK')

        self.enemy_toughness -= break_amount

        total_dmg.append(dmg)

        self._handle_resurgence_action_forward(is_resurgence)

        if self._can_use_ult():
            ult_dmg, ult_break_amount, is_resurgence = self._use_ult()

            self.enemy_toughness -= ult_break_amount

            total_dmg.append(ult_dmg)

            self.data['DMG'].append(ult_dmg)
            self.data['DMG_Type'].append('Ultimate')

            self._handle_resurgence_action_forward(is_resurgence)
            self.current_ult_energy = 5

        return sum(total_dmg)

    def _reset_stats(self):
        self.speed = self.starting_spd

    def _use_basic_atk(self) -> tuple[float, int, bool]:
        logger.info("Using basic attack...")
        dmg, break_amount, is_resurgence = self._calculate_damage(skill_multiplier=1, break_amount=20)
        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)
        self.speed *= 1.2  # action forward 20%
        return dmg, break_amount, is_resurgence

    def _use_skill(self) -> tuple[float, int, bool]:
        logger.info("Using skill...")
        dmg, break_amount, is_resurgence = self._calculate_damage(skill_multiplier=2.2, break_amount=20)
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)
        self._apply_sheathed_blade()
        return dmg, break_amount, is_resurgence

    def _use_ult(self) -> tuple[float, int, bool]:
        logger.info('Using ultimate...')
        return self._calculate_damage(skill_multiplier=4.25, break_amount=30)

    def _calculate_damage(self, skill_multiplier: float, break_amount: int) -> tuple[float, int, bool]:
        weakness_broken = self.is_enemy_weakness_broken()
        is_crit = random.random() < self.crit_rate
        base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=skill_multiplier)
        dmg_multiplier, res_multiplier, is_resurgence = self._random_resurgence(is_crit)
        dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
        total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_multiplier, dmg_reduction)
        return total_dmg, break_amount, is_resurgence

    def _apply_sheathed_blade(self):
        self.sheathed_blade = 2
        if self.sheathed_blade > 0:
            self.speed = self.starting_spd * 1.25
            logger.debug(f'Speed after Sheathed Blade Buff: {self.speed}')
            self.sheathed_blade -= 1
        logger.debug(f'Sheathed Blade: {self.sheathed_blade}')

    def _handle_resurgence_action_forward(self, is_resurgence: bool) -> None:
        logger.info('Handling resurgence action forward...')
        if is_resurgence:
            self.speed *= 2
            logger.debug(f'Speed after resurgence buff: {self.speed}')
            self.can_resurgence = False
        else:
            self.can_resurgence = True

    def _random_resurgence(self, is_crit: bool) -> tuple[float, float, bool]:
        logger.info('Random resurgence...')
        resurgence_chance = 0.5 if self.can_resurgence else 0
        is_resurgence = random.random() < resurgence_chance

        if is_resurgence:
            dmg_multipliers = [0.8]
            res_pen = [0.2]
            res_multiplier = calculate_res_multipliers(res_pen=res_pen)
            dmg_multiplier = calculate_dmg_multipliers(
                crit_dmg=self.crit_dmg if is_crit else 0,
                dmg_multipliers=dmg_multipliers
            )
        else:
            dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg if is_crit else 0)
            res_multiplier = calculate_res_multipliers()

        return dmg_multiplier, res_multiplier, is_resurgence