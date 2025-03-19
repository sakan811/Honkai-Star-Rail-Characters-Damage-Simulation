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


class Robin(HarmonyCharacter):
    def __init__(self):
        super().__init__()
        self.DEFAULT_ATK = 4198.12

    def skill_buff(self) -> float:
        return 0.5

    def talent_buff(self) -> float:
        crit_dmg = 0.2
        return crit_dmg

    def ult_buff(self) -> float:
        atk_increased = (0.228 * self.DEFAULT_ATK) + 200
        final_atk = self.trailblazer_atk + atk_increased
        atk_buff = self.calculate_percent_change(
            self.trailblazer_atk, final_atk, decimal_mode=True
        )
        return atk_buff

    def a4_trace_buff(self) -> float:
        # average CRIT DMG as it's only for follow-up characters
        crit_dmg = 0.25 / 2
        return crit_dmg

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        # assume Robin give 1 extra turn in total from her Ult
        bonus_turn = 1

        ult_crit_dmg_multiplier = 1 + 1.5

        final_trailblazer_crit_dmg = (
            self.trailblazer_crit_dmg + self.talent_buff() + self.a4_trace_buff()
        )

        crit_buff = self.crit_buff(
            crit_rate=self.trailblazer_crit_rate,
            crit_dmg=final_trailblazer_crit_dmg,
            base_crit_rate=self.trailblazer_crit_rate,
            base_crit_dmg=self.trailblazer_crit_dmg,
        )

        additional_dmg = (
            (1.2 * self.DEFAULT_ATK) * (1 + self.skill_buff()) * ult_crit_dmg_multiplier
        )
        buffed_dmg = self.calculate_trailblazer_dmg(
            dmg_bonus_multiplier=self.skill_buff() + crit_buff,
            atk_bonus=self.ult_buff(),
            dmg_from_harmony_char=additional_dmg,
            bonus_turns=bonus_turn,
        )
        return self.calculate_percent_change(base_dmg, buffed_dmg)
