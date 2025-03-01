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


class Tingyun(HarmonyCharacter):
    BENEDICT_HIT_NUM = 3
    def __init__(self):
        super().__init__()

    def ult_buff(self) -> int:
        # assume Tingyun gain 50 energy per 5 cycles
        ult_gain = int(50 / 5)
        return ult_gain

    def skill_buff(self) -> float:
        # assume Tingyun has 4000 ATK
        atk_buff = 2000 * 0.5
        return atk_buff

    def a6_trace_buff(self, ally_atk) -> float:
        additional_dmg = ally_atk * 0.6
        return additional_dmg

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        ally_atk = self.trailblazer_atk + self.skill_buff()
        
        additional_dmg = self.a6_trace_buff(ally_atk) + (0.4 * ally_atk)
        
        # account for Benedict's 3 hits from Trailblazer's Skill, Ult, and Basic ATK
        additional_dmg = additional_dmg * self.BENEDICT_HIT_NUM

        energy_regen_buff = self.energy_regen_buff(
            total_energy_gain=self.ult_buff() + 30
        )

        atk_buff = self.calculate_percent_change(
            self.trailblazer_atk, ally_atk, decimal_mode=True
        )

        buffed_dmg = self.calculate_trailblazer_dmg(
            dmg_bonus_multiplier=energy_regen_buff,
            atk_bonus=atk_buff,
            dmg_from_harmony_char=additional_dmg,
        )
        return self.calculate_percent_change(base_dmg, buffed_dmg)