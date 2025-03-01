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
    def __init__(self):
        super().__init__()
        # Initialize with base HP first
        self.base_hp = 5000
        self.hp = self.base_hp
        # Update HP with trace buff after initialization
        self.hp = self.base_hp + self.a4_trace_buff()

    def skill_buff(self) -> float:
        return 0.24

    def talent_buff(self) -> float:
        """
        Tribbie's talent DMG from follow-up attacks
        :return: talent DMG
        """
        talent_dmg_list = []
        
        # DMG for 1 Ult from ally
        talent_dmg = 0.18 * self.hp
        talent_dmg_list.append(talent_dmg)
        
        # DMG for 2 Ult from ally
        talent_dmg = 0.18 * self.hp * 2
        talent_dmg_list.append(talent_dmg)
        
        # DMG for 3 Ult from ally
        talent_dmg = 0.18 * self.hp * 3
        talent_dmg_list.append(talent_dmg)
        
        # Average DMG
        avg_talent_dmg = sum(talent_dmg_list) / len(talent_dmg_list)
        
        return avg_talent_dmg
    
    def ult_buff(self, *args, **kwargs) -> float:
        """
        Tribbie's ult DMG
        :return: ult DMG
        """
        zone_additional_dmg_list = []
                
        # DMG for 1 enemy hit
        zone_additional_dmg = 0.12 * self.hp
        zone_additional_dmg_list.append(zone_additional_dmg)
        
        # DMG for 2 enemy hits
        zone_additional_dmg = 0.12 * self.hp * 2
        zone_additional_dmg_list.append(zone_additional_dmg)
        
        # DMG for 3 enemy hits
        zone_additional_dmg = 0.12 * self.hp * 3
        zone_additional_dmg_list.append(zone_additional_dmg)
        
        # DMG for 4 enemy hits
        zone_additional_dmg = 0.12 * self.hp * 4
        zone_additional_dmg_list.append(zone_additional_dmg)
        
        # DMG for 5 enemy hits
        zone_additional_dmg = 0.12 * self.hp * 5
        zone_additional_dmg_list.append(zone_additional_dmg)
        
        # Average DMG
        avg_zone_additional_dmg = sum(zone_additional_dmg_list) / len(zone_additional_dmg_list)
        
        return avg_zone_additional_dmg
    
    def a2_trace_buff(self, *args, **kwargs) -> float:
        return 0.72 * 3

    def a4_trace_buff(self) -> float:
        # Use base_hp instead of hp to avoid circular reference
        return 0.09 * (self.base_hp * 4)

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        total_zone_additional_dmg = self.ult_buff()
        
        zone_dmg_multiplier = 0.3

        tribbie_dmg = (total_zone_additional_dmg + self.talent_buff()) * (1 + self.a2_trace_buff())
        
        buffed_dmg = self.calculate_trailblazer_dmg(
            dmg_bonus_multiplier=zone_dmg_multiplier,
            res_pen_multiplier=self.skill_buff(),
            additional_dmg=tribbie_dmg,
        )
        return self.calculate_percent_change(base_dmg, buffed_dmg)
