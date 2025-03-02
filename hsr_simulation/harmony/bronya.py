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


class Bronya(HarmonyCharacter):
    BONUS_TURNS = 1
    def __init__(self):
        super().__init__()

    def skill_buff(self) -> float:
        skill_buff_value = 0.66
        return skill_buff_value

    def ult_buff(self) -> float:
        return 0.55

    def a6_trace_buff(self) -> float:
        return 0.1

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        bronya_crit_dmg = 1.8731 + self.trailblazer_crit_dmg
        final_trailblazer_crit_dmg = self.trailblazer_crit_dmg + ((0.16 * bronya_crit_dmg) + 0.2)
        
        crit_buff = self.crit_buff(
            crit_rate=self.trailblazer_crit_rate,
            crit_dmg=final_trailblazer_crit_dmg,
            base_crit_rate=self.trailblazer_crit_rate,
            base_crit_dmg=self.trailblazer_crit_dmg
        )

        dmg_buff = self.a6_trace_buff() + self.skill_buff() + crit_buff
        buffed_dmg = self.calculate_trailblazer_dmg(
            dmg_bonus_multiplier=dmg_buff,
            atk_bonus=self.ult_buff(),
            bonus_turns=self.BONUS_TURNS,
        )
        return self.calculate_percent_change(base_dmg, buffed_dmg)