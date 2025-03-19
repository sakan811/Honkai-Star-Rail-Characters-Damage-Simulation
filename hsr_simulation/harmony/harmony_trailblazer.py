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

from hsr_simulation.dmg_calculator import calculate_super_break_dmg
from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter


class HarmonyTrailblazer(HarmonyCharacter):
    def __init__(self):
        super().__init__()

    def ult_buff(self) -> float:
        break_effect = self.default_break_effect * 1.3
        return calculate_super_break_dmg(
            base_toughness_reduce=20, break_effect=break_effect
        )

    def a2_trace_buff(self) -> float:
        super_break_dmg_multiplier = 0.6
        return super_break_dmg_multiplier

    def potential_buff(self) -> float:
        base_dmg = self.calculate_trailblazer_dmg()

        super_break_dmg = self.ult_buff() * (1 + self.a2_trace_buff())
        buffed_dmg = self.calculate_trailblazer_dmg(
            dmg_from_harmony_char=super_break_dmg
        )
        return self.calculate_percent_change(base_dmg, buffed_dmg)
