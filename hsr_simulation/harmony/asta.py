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
    def __init__(self):
        super().__init__()

    def talent_buff(self) -> float:
        atk_buff = 0.14
        stacks = 5
        return atk_buff * stacks

    def ult_buff(self) -> int:
        spd_buff = 50
        return spd_buff

    def a4_trace_buff(self) -> float:
        return 0.18

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        bonus_turn = self.calculate_spd_breakpoint(bonus_spd=self.ult_buff())

        buffed_dmg = self.calculate_trailblazer_dmg(
            atk_bonus=self.talent_buff(),
            elemental_dmg_multiplier=self.a4_trace_buff(),
            bonus_turns=bonus_turn,
        )
        return self.calculate_percent_change(base_dmg, buffed_dmg)
