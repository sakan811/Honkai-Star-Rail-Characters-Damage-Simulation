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


class Tribbie(HarmonyCharacter):
    # Additional DMG from the zone only last for 2 turns within 5 cycles
    ZONE_DMG_HIT_NUM = 2

    def __init__(self):
        super().__init__()
        # Initialize with base HP first
        self.base_hp = 6000
        self.hp = self.base_hp
        # Update HP with trace buff after initialization
        self.hp = self.base_hp + self.a4_trace_buff()

        self.a2_multiplier = 1 + self.a2_trace_buff()

    def skill_buff(self) -> float:
        return 0.24

    def talent_buff(self) -> float:
        """
        Tribbie's talent DMG from follow-up attacks
        :return: talent DMG
        """
        data = []

        # DMG for 1 Ult from ally
        talent_dmg = 0.18 * self.hp * self.a2_multiplier
        data.append(talent_dmg)

        # DMG for 2 Ult from ally
        talent_dmg = 0.18 * self.hp * 2 * self.a2_multiplier
        data.append(talent_dmg)

        # DMG for 3 Ult from ally
        talent_dmg = 0.18 * self.hp * 3 * self.a2_multiplier
        data.append(talent_dmg)

        # Average DMG
        return sum(data) / len(data)

    def ult_buff(self, *args, **kwargs) -> float:
        """
        Tribbie's ult DMG
        :return: ult DMG
        """
        data = []

        # Initial hit on 1 enemy
        initial_dmg = 0.3 * self.hp * self.a2_multiplier
        data.append(initial_dmg)

        # Initial hit on 2 enemies
        initial_dmg = 0.3 * self.hp * self.a2_multiplier * 2
        data.append(initial_dmg)

        # Initial hit on 3 enemies
        initial_dmg = 0.3 * self.hp * self.a2_multiplier * 3
        data.append(initial_dmg)

        # Initial hit on 4 enemies
        initial_dmg = 0.3 * self.hp * self.a2_multiplier * 4
        data.append(initial_dmg)

        # Initial hit on 5 enemies
        initial_dmg = 0.3 * self.hp * self.a2_multiplier * 5
        data.append(initial_dmg)

        # DMG for 1 enemy hit
        zone_additional_dmg = (
            0.12 * self.hp * self.a2_multiplier * self.ZONE_DMG_HIT_NUM
        )
        data.append(zone_additional_dmg)

        # DMG for 2 enemy hit
        zone_additional_dmg = (
            0.12 * self.hp * 2 * self.a2_multiplier * self.ZONE_DMG_HIT_NUM
        )
        data.append(zone_additional_dmg)

        # DMG for 3 enemy hit
        zone_additional_dmg = (
            0.12 * self.hp * 3 * self.a2_multiplier * self.ZONE_DMG_HIT_NUM
        )
        data.append(zone_additional_dmg)

        # DMG for 4 enemy hit
        zone_additional_dmg = (
            0.12 * self.hp * 4 * self.a2_multiplier * self.ZONE_DMG_HIT_NUM
        )
        data.append(zone_additional_dmg)

        # DMG for 5 enemy hit
        zone_additional_dmg = (
            0.12 * self.hp * 5 * self.a2_multiplier * self.ZONE_DMG_HIT_NUM
        )
        data.append(zone_additional_dmg)

        return sum(data) / len(data)

    def a2_trace_buff(self, *args, **kwargs) -> float:
        return 0.72 * 3

    def a4_trace_buff(self) -> float:
        # Use base_hp instead of hp to avoid circular reference
        return 0.09 * (self.base_hp * 3)

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        zone_dmg_multiplier = 0.3

        tribbie_dmg = self.ult_buff() + self.talent_buff()

        buffed_dmg = self.calculate_trailblazer_dmg(
            dmg_bonus_multiplier=zone_dmg_multiplier,
            res_pen_multiplier=self.skill_buff(),
            dmg_from_harmony_char=tribbie_dmg,
        )
        return self.calculate_percent_change(base_dmg, buffed_dmg)
