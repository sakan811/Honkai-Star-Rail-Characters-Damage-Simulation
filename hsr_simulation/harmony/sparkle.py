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


class Sparkle(HarmonyCharacter):
    def __init__(self):
        super().__init__()

    def skill_buff(self) -> None:
        sparkle_crit_dmg = self.trailblazer_crit_dmg + 2.1019
        self.trailblazer_crit_dmg += ((0.24 * sparkle_crit_dmg) + 0.45)

    def talent_buff(self) -> float:
        dmg_buff = (0.06 + self.ult_buff()) * 3
        return dmg_buff

    def ult_buff(self) -> float:
        return 0.1

    def a6_trace_buff(self) -> float:
        atk_buff = 0.45
        return atk_buff

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        # assume Sparkle give 50% action forward 1 time in total from her Skill
        bonus_turn = 0.5
        
        self.skill_buff()

        buffed_dmg = self.calculate_trailblazer_dmg(
            dmg_bonus_multiplier=self.talent_buff() + self.a6_trace_buff(),
            atk_bonus=self.ult_buff(),
            bonus_turns=bonus_turn,
        )
        return self.calculate_percent_change(base_dmg, buffed_dmg)