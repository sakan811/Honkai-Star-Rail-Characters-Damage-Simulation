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


class Yukong(HarmonyCharacter):
    def __init__(self):
        super().__init__()

    def skill_buff(self) -> float:
        atk_buff = 0.8
        return atk_buff

    def potential_buff(self) -> float:
        base_dmg = self.calculate_trailblazer_dmg()

        atk_buff = self.skill_buff()

        final_crit_rate = self.trailblazer_crit_rate + 0.28
        final_crit_dmg = self.trailblazer_crit_dmg + 0.65

        crit_buff = self.crit_buff(final_crit_rate, final_crit_dmg)

        buffed_dmg = self.calculate_trailblazer_dmg(
            atk_bonus=atk_buff, dmg_bonus_multiplier=crit_buff
        )
        return self.calculate_percent_change(base_dmg, buffed_dmg)