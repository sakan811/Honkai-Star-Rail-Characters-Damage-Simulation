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


class Hanya(HarmonyCharacter):
    def __init__(self):
        super().__init__()
        self.DEFAULT_SPD = 164.47

    def ult_buff(self) -> float:
        atk_buff = 0.6
        return atk_buff

    def talent_buff(self) -> float:
        return 0.3

    def a2_trace_buff(self) -> float:
        atk_buff = 0.1
        return atk_buff

    def a6_trace_buff(self) -> float:
        return self.energy_regen_buff(total_energy_gain=2)

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        bonus_turn = self.calculate_spd_breakpoint(bonus_spd=0.2 * self.DEFAULT_SPD)

        buffed_dmg = self.calculate_trailblazer_dmg(
            atk_bonus=self.ult_buff() + self.a2_trace_buff(),
            dmg_bonus_multiplier=self.talent_buff() + self.a6_trace_buff(),
            bonus_turns=bonus_turn,
        )
        return self.calculate_percent_change(base_dmg, buffed_dmg)