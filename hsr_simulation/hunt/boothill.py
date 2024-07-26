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
import math
import random

from configure_logging import configure_logging_with_file
from hsr_simulation.character import Character
from hsr_simulation.dmg_calculator import calculate_break_damage

logger = configure_logging_with_file('simulate_turns.log')


class Boothill(Character):
    def __init__(
            self,
            atk: int = 2000,
            crit_rate: float = 0.5,
            crit_dmg: float = 1.0,
            speed: float = 107,
            ult_energy: int = 115
    ):
        super().__init__(atk, crit_rate, crit_dmg, speed, ult_energy)
        self.pocket_trickshot = 0
        self.standoff_turns = 0
        self.win_battle = False

    def take_action(self) -> float:
        """
        Simulate taking actions.
        :return: Total damage.
        """
        total_dmg = []

        if self.skill_points > 0 >= self.standoff_turns:
            self._use_skill()
            dmg = self._use_enhanced_basic_atk()
            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Enhanced Basic ATK')
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
        if self.enemy_toughness <= 0:
            self.enemy_toughness = 50
            self._end_standoff()
            return True
        return False

    def _use_basic_atk(self) -> float:
        if self.standoff_turns > 0:
            self.standoff_turns -= 1
            return self._use_enhanced_basic_atk()
        else:
            dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10)
            self.enemy_toughness -= break_amount
            self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)
            return dmg

    def _use_enhanced_basic_atk(self) -> float:
        dmg, break_amount = self._calculate_damage(skill_multiplier=2.2, break_amount=20)
        break_amount *= (1 + 0.5 * self.pocket_trickshot)  # Talent: Five Peas in a Pod
        self.enemy_toughness -= break_amount

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=30)

        if self.is_enemy_weakness_broken():
            self.win_battle = True

            # Talent: Five Peas in a Pod
            break_dmg_multiplier = [0.7, 1.2, 1.7][min(self.pocket_trickshot, 2)]
            target_toughness = min(self.enemy_toughness, 16 * 10)
            break_dmg = break_dmg_multiplier * calculate_break_damage(break_type='Physical',
                                                                      target_max_toughness=target_toughness)
            self.data['DMG'].append(break_dmg)
            self.data['DMG_Type'].append('Talent')

            dmg += break_dmg

        return dmg

    def _use_skill(self) -> None:
        if not self.win_battle:
            self.pocket_trickshot = 0

        self.standoff_turns = 2
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=0)

    def _use_ult(self) -> float:
        dmg, break_amount = self._calculate_damage(skill_multiplier=4, break_amount=30)
        self.enemy_toughness -= break_amount

        return dmg

    def _calculate_damage(
            self,
            skill_multiplier: float,
            break_amount: int,
            dmg_multipliers: list[float] = None,
            res_multipliers: list[float] = None) -> tuple[float, int]:

        weakness_broken = self.is_enemy_weakness_broken()

        # Store original crit values
        original_crit_rate = self.crit_rate
        original_crit_dmg = self.crit_dmg

        # A2 Major Trace: Ghost Load
        crit_rate_boost = min(0.3, 0.1 * self.break_effect)
        crit_dmg_boost = min(1.5, 0.5 * self.break_effect)
        self.crit_rate += crit_rate_boost
        self.crit_dmg += crit_dmg_boost

        if random.random() < self.crit_rate:
            base_dmg = self.atk * skill_multiplier
            dmg_multiplier = 1 + self.crit_dmg
        else:
            base_dmg = self.atk * skill_multiplier
            dmg_multiplier = 1

        # Reset crit values
        self.crit_rate = original_crit_rate
        self.crit_dmg = original_crit_dmg

        if dmg_multipliers:
            dmg_multiplier *= math.prod(dmg_multipliers)

        dmg_reduction = 0.9 if weakness_broken else 1  # Simplified damage reduction
        res_multiplier = 1  # Simplified resistance multiplier
        if res_multipliers:
            res_multiplier *= math.prod(res_multipliers)

        total_dmg = base_dmg * dmg_multiplier * res_multiplier * dmg_reduction
        return total_dmg, break_amount

    def _can_use_ult(self) -> bool:
        return self.current_ult_energy >= self.ult_energy

    def _update_skill_point_and_ult_energy(self, skill_points: int, ult_energy: int) -> None:
        self.skill_points += skill_points
        self.current_ult_energy += ult_energy

        # A6 Major Trace: Point Blank
        if self.standoff_turns > 0 and self.pocket_trickshot < 3:
            self.current_ult_energy += 10

    def _end_standoff(self) -> None:
        self.standoff_turns = 0
        self.pocket_trickshot = min(self.pocket_trickshot + 1, 3)


if __name__ == '__main__':
    pass