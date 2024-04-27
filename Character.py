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


class Character:
    def __init__(
            self,
            atk,
            crit_rate,
            crit_dmg,
            elemental_dmg,
            speed,
            skill_multiplier,
            ult_multiplier,
            ult_energy
    ):
        self.atk = atk
        self.crit_rate = crit_rate
        self.crit_dmg = crit_dmg
        self.elemental_dmg = elemental_dmg
        self.speed = speed
        self.skill_multiplier = skill_multiplier
        self.ult_multiplier = ult_multiplier
        self.results = []
        self.ult_energy = ult_energy
        self.current_ult_energy = 0

    def _simulate_skill_and_ult(self, skill: bool, ult: bool, crit: bool):
        if skill:
            dmg = self.atk * self.skill_multiplier

            if crit:
                dmg *= self.crit_dmg

            dmg *= self.elemental_dmg

            self.results.append(dmg)

            self.current_ult_energy += 30
        else:
            dmg = self.atk * self.ult_multiplier

            if crit:
                dmg *= self.crit_dmg

            dmg *= self.elemental_dmg

            self.results.append(dmg)

            self.current_ult_energy = 5

    def _simulate_actions_during_each_turn(self):
        crit = random.random() < self.crit_rate

        self._simulate_skill_and_ult(skill=True, ult=False, crit=crit)

        if self.current_ult_energy >= self.ult_energy:
            self._simulate_skill_and_ult(skill=False, ult=True, crit=crit)

    def _simulate_total_turns_from_given_cycles(self, cycles: int):
        char_action_value = 10000 / self.speed
        cycles_action_value = 150 + (100 * (cycles - 1))
        turns = cycles_action_value / char_action_value
        turns = int(turns)

        for turn in range(1, turns + 1):
            self._simulate_actions_during_each_turn()
            self._simulate_ally_turn()
            self._simulate_buff_duration_on_character()
            self._simulate_enemy_turn()
            self._simulate_debuff_duration_on_enemy()

    def _simulate_cycles(self):
        self.results = []
        cycles = 30

        self._simulate_total_turns_from_given_cycles(cycles)

        total_dmg_after_all_cycles = sum(self.results)

        return total_dmg_after_all_cycles

    def calculate_battles(self, *args):
        self._set_scenario(args)

        total_dmg_from_each_battle = []

        for _ in range(1000):
            self._reset_variables()
            self._simulate_enter_battle_effect()

            total_dmg_from_all_cycles = self._simulate_cycles()

            total_dmg_from_each_battle.append(total_dmg_from_all_cycles)

        avg_dmg = sum(total_dmg_from_each_battle) / len(total_dmg_from_each_battle)

        return avg_dmg, min(total_dmg_from_each_battle), max(total_dmg_from_each_battle)

    def _reset_variables(self):
        self.current_ult_energy = 0

    def _simulate_enter_battle_effect(self):
        pass

    def _simulate_buff_duration_on_character(self):
        pass

    def _simulate_debuff_duration_on_enemy(self):
        pass

    def _simulate_enemy_turn(self):
        pass

    def _simulate_ally_turn(self):
        pass

    def _set_scenario(self, *args):
        pass