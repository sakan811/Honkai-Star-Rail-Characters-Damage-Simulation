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

from hsr_simulation.dmg_calculator import calculate_break_damage
from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter


class RuanMei(HarmonyCharacter):
    def __init__(self):
        super().__init__()

    def skill_buff(self) -> float:
        return 0.32

    def talent_buff(self) -> float:
        spd_buff = 0.1
        return spd_buff

    def ult_buff(self) -> float:
        res_pen = 0.25
        return res_pen

    def a6_trace_buff(self) -> float:
        return 0.36

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        bonus_turn = self.calculate_spd_breakpoint(
            bonus_spd=self.talent_buff() * self.trailblazer_spd
        )

        break_dmg = calculate_break_damage(break_type="Ice", target_max_toughness=100)
        avg_ruan_mei_break_effect = 1.8621
        break_effect = 1 + avg_ruan_mei_break_effect
        final_break_dmg = (break_dmg * 1.2 * break_effect) + (
            break_dmg * 0.5 * break_effect
        )

        buffed_dmg = self.calculate_trailblazer_dmg(
            dmg_bonus_multiplier=self.skill_buff() + self.a6_trace_buff(),
            res_pen_multiplier=self.ult_buff(),
            bonus_turns=bonus_turn,
            dmg_from_harmony_char=final_break_dmg,
        )
        return self.calculate_percent_change(base_dmg, buffed_dmg)
