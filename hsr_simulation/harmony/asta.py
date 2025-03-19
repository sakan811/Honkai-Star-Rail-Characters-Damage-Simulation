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

from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter


class Asta(HarmonyCharacter):
    SKILL_NUM_HIT = 3
    A2_TRACE_NUM_HIT = 5

    def __init__(self):
        super().__init__()
        self.DEFAULT_ATK = 1760.86
        self.bonus_turn = self.calculate_spd_breakpoint(bonus_spd=self.ult_buff())

    def skill_buff(self) -> float:
        data = []
        intial_hit_dmg = 0.5 * self.DEFAULT_ATK

        # further DMG 1 time
        further_hit_dmg = 0.5 * self.DEFAULT_ATK
        total_dmg = intial_hit_dmg + further_hit_dmg * self.SKILL_NUM_HIT
        data.append(total_dmg)

        # further DMG 2 times
        further_hit_dmg = 0.5 * self.DEFAULT_ATK * 2
        total_dmg = intial_hit_dmg + further_hit_dmg * self.SKILL_NUM_HIT
        data.append(total_dmg)

        # further DMG 3 times
        further_hit_dmg = 0.5 * self.DEFAULT_ATK * 3
        total_dmg = intial_hit_dmg + further_hit_dmg * self.SKILL_NUM_HIT
        data.append(total_dmg)

        # further DMG 4 times
        further_hit_dmg = 0.5 * self.DEFAULT_ATK * 4
        total_dmg = intial_hit_dmg + further_hit_dmg * self.SKILL_NUM_HIT
        data.append(total_dmg)

        return sum(data) / len(data)

    def talent_buff(self) -> float:
        atk_buff = 0.14
        stacks = 5
        return atk_buff * stacks

    def ult_buff(self) -> int:
        spd_buff = 50
        return spd_buff

    def a2_trace_buff(self) -> float:
        # DoT damage per hit
        dot_dmg_per_hit = 0.5 * self.DEFAULT_ATK
        # Total potential damage across all hits
        total_potential_dmg = dot_dmg_per_hit * self.A2_TRACE_NUM_HIT
        # Account for 80% chance of applying the DoT
        expected_dmg = total_potential_dmg * 0.8
        return expected_dmg

    def a4_trace_buff(self) -> float:
        return 0.18

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        buffed_dmg = self.calculate_trailblazer_dmg(
            atk_bonus=self.talent_buff(),
            elemental_dmg_multiplier=self.a4_trace_buff(),
            bonus_turns=self.bonus_turn,
        )
        return self.calculate_percent_change(base_dmg, buffed_dmg)
