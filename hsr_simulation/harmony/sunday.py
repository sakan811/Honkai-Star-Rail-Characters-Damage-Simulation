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


class Sunday(HarmonyCharacter):
    def __init__(self):
        super().__init__()

    def talent_buff(self):
        crit_rate_increase = 0.2
        return crit_rate_increase

    def a2_trace_buff(self, ult_energy_regen):
        energy_gain_from_sunday_ult = self.trailblazer_ult_energy * 0.2
        if energy_gain_from_sunday_ult < 40:
            energy_gain_from_sunday_ult = 40
        energy_gain_from_sunday_ult_in_five_cycles = energy_gain_from_sunday_ult / 5
        total_energy_gain = int(30 + energy_gain_from_sunday_ult_in_five_cycles)
        return self.energy_regen_buff(total_energy_gain)

    def skill_buff(self):
        skill_base_buff = 0.3
        with_summon_skill_buff = skill_base_buff + 0.5
        skill_buff = (skill_base_buff + with_summon_skill_buff) / 2
        return skill_buff

    def ult_buff(self):
        ult_energy_regen = self.trailblazer_ult_energy * 0.2
        ult_energy_regen_buff = self.a2_trace_buff(ult_energy_regen)

        sunday_crit_dmg = self.trailblazer_crit_dmg + 2.0939

        crit_dmg_increased = (0.3 * sunday_crit_dmg) + 0.12
        final_trailblazer_crit_dmg = self.trailblazer_crit_dmg + crit_dmg_increased
        final_trailblazer_crit_rate = self.trailblazer_crit_rate + self.talent_buff()

        crit_buff = self.crit_buff(
            crit_rate=final_trailblazer_crit_rate,
            crit_dmg=final_trailblazer_crit_dmg,
            base_crit_rate=self.trailblazer_crit_rate,
            base_crit_dmg=self.trailblazer_crit_dmg,
        )

        return ult_energy_regen_buff + crit_buff

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        dmg_buff = self.skill_buff() + self.ult_buff()

        # assume Sunday give 1 extra turns in total from his Skill
        bonus_turn = 1
        buffed_dmg = self.calculate_trailblazer_dmg(
            dmg_bonus_multiplier=dmg_buff, bonus_turns=bonus_turn
        )

        return self.calculate_percent_change(base_dmg, buffed_dmg)
