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
from hsr_simulation.dmg_calculator import calculate_break_damage, calculate_super_break_dmg
from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter


class Sunday(HarmonyCharacter):
    def __init__(self):
        super().__init__()

    def talent_buff(self, *args, **kwargs):
        return self.trailblazer_crit_rate + 0.2

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

        crit_dmg_increased = ((0.3 * sunday_crit_dmg) + 0.12)
        final_crit_dmg = self.trailblazer_crit_dmg + crit_dmg_increased
        final_crit_rate = self.talent_buff()

        crit_buff = self.crit_buff(final_crit_rate, final_crit_dmg)

        return crit_buff + ult_energy_regen_buff

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        dmg_buff = self.skill_buff() + self.ult_buff()

        # assume Sunday give 3 extra turns in total from his Skill due to 3 starting skill points
        bonus_turn = 3
        buffed_dmg = self.calculate_trailblazer_dmg(dmg_bonus_multiplier=dmg_buff, bonus_turns=bonus_turn)

        return self.calculate_percent_change(base_dmg, buffed_dmg)


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

        buffed_dmg = self.calculate_trailblazer_dmg(atk_bonus=self.talent_buff(),
                                                    elemental_dmg_multiplier=self.a4_trace_buff(),
                                                    bonus_turns=bonus_turn)
        return self.calculate_percent_change(base_dmg, buffed_dmg)


class Bronya(HarmonyCharacter):
    def __init__(self):
        super().__init__()

    def skill_buff(self, *args, **kwargs) -> float:
        return 0.66

    def ult_buff(self, *args, **kwargs) -> float:
        return 0.55

    def a6_trace_buff(self, *args, **kwargs) -> float:
        return 0.1

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        bronya_crit_dmg = 1.8731 + self.trailblazer_crit_dmg
        final_crit_dmg = self.trailblazer_crit_dmg + ((0.16 * bronya_crit_dmg) + 0.2)
        crit_rate_buff = self.crit_buff(self.trailblazer_crit_rate, final_crit_dmg)

        # assume Bronya give 3 extra turns in total from her Skill due to 3 starting skill points
        bonus_turns = 3

        dmg_buff = self.a6_trace_buff() + self.skill_buff() + crit_rate_buff
        buffed_dmg = self.calculate_trailblazer_dmg(dmg_bonus_multiplier=dmg_buff, atk_bonus=self.ult_buff(),
                                                    bonus_turns=bonus_turns)
        return self.calculate_percent_change(base_dmg, buffed_dmg)


class Hanya(HarmonyCharacter):
    def __init__(self):
        super().__init__()

    def ult_buff(self, *args, **kwargs) -> float:
        atk_buff = 0.6
        return atk_buff

    def talent_buff(self, *args, **kwargs) -> float:
        return 0.3

    def a2_trace_buff(self, *args, **kwargs) -> float:
        atk_buff = 0.1
        return atk_buff

    def a6_trace_buff(self, *args, **kwargs) -> float:
        return self.energy_regen_buff(total_energy_gain=2)

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        bonus_turn = self.calculate_spd_breakpoint(bonus_spd=0.2 * self.trailblazer_spd)

        buffed_dmg = self.calculate_trailblazer_dmg(atk_bonus=self.ult_buff() + self.a2_trace_buff(),
                                                    dmg_bonus_multiplier=self.talent_buff() + self.a6_trace_buff(),
                                                    bonus_turns=bonus_turn)
        return self.calculate_percent_change(base_dmg, buffed_dmg)


class Robin(HarmonyCharacter):
    def __init__(self):
        super().__init__()

    def skill_buff(self, *args, **kwargs) -> float:
        return 0.5

    def talent_buff(self, *args, **kwargs) -> float:
        crit_dmg = 0.2
        return crit_dmg

    def ult_buff(self, *args, **kwargs) -> float:
        atk_increased = (0.228 * self.trailblazer_atk) + 200
        final_atk = self.trailblazer_atk + atk_increased
        atk_buff = self.calculate_percent_change(self.trailblazer_atk, final_atk, decimal_mode=True)
        return atk_buff

    def a4_trace_buff(self, *args, **kwargs) -> float:
        # average CRIT DMG as it's only for follow-up characters
        crit_dmg = 0.25 / 2
        return crit_dmg

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        # assume Robin give 1 extra turn in total from her Ult
        bonus_turn = 1

        final_crit_dmg = self.trailblazer_crit_dmg + self.talent_buff() + self.a4_trace_buff()
        crit_buff = self.crit_buff(self.trailblazer_crit_rate, final_crit_dmg)
        additional_dmg = (1.2 * self.trailblazer_atk) * 1.5
        buffed_dmg = self.calculate_trailblazer_dmg(dmg_bonus_multiplier=self.skill_buff() + crit_buff,
                                                    atk_bonus=self.ult_buff(),
                                                    additional_dmg=additional_dmg,
                                                    bonus_turns=bonus_turn)
        return self.calculate_percent_change(base_dmg, buffed_dmg)


class RuanMei(HarmonyCharacter):
    def __init__(self):
        super().__init__()

    def skill_buff(self, *args, **kwargs) -> float:
        return 0.32

    def talent_buff(self, *args, **kwargs) -> float:
        spd_buff = 0.1
        return spd_buff

    def ult_buff(self, *args, **kwargs) -> float:
        res_pen = 0.25
        return res_pen

    def a6_trace_buff(self, *args, **kwargs) -> float:
        return 0.36

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        bonus_turn = self.calculate_spd_breakpoint(bonus_spd=self.talent_buff() * self.trailblazer_spd)

        break_dmg = calculate_break_damage(break_type = 'Ice', target_max_toughness = 100)
        avg_ruan_mei_break_effect = 1.8621
        break_effect = 1 + avg_ruan_mei_break_effect
        final_break_dmg = (break_dmg * 1.2 * break_effect) + (break_dmg * 0.5 * break_effect)

        buffed_dmg = self.calculate_trailblazer_dmg(dmg_bonus_multiplier=self.skill_buff() + self.a6_trace_buff(),
                                                    res_pen_multiplier=self.ult_buff(),
                                                    bonus_turns=bonus_turn,
                                                    break_dmg=final_break_dmg)
        return self.calculate_percent_change(base_dmg, buffed_dmg)


class Sparkle(HarmonyCharacter):
    def __init__(self):
        super().__init__()

    def skill_buff(self, *args, **kwargs) -> float:
        sparkle_crit_dmg = self.trailblazer_crit_dmg + 2.1019
        final_crit_dmg = self.trailblazer_crit_dmg + ((0.24 * sparkle_crit_dmg) + 0.45)
        return self.crit_buff(self.trailblazer_crit_rate, final_crit_dmg)

    def talent_buff(self, *args, **kwargs) -> float:
        dmg_buff = (0.06 + self.ult_buff()) * 3
        return dmg_buff

    def ult_buff(self, *args, **kwargs) -> float:
        return 0.1

    def a6_trace_buff(self, *args, **kwargs) -> float:
        atk_buff = 0.45
        return atk_buff

    def potential_buff(self):
        base_dmg = self.calculate_trailblazer_dmg()

        # assume Sparkle give 50% action forward 3 times in total from her Skill
        bonus_turn = round(3 * 0.5)

        buffed_dmg = self.calculate_trailblazer_dmg(dmg_bonus_multiplier=self.skill_buff() + self.talent_buff() + self.a6_trace_buff(),
                                                    atk_bonus=self.ult_buff(),
                                                    bonus_turns=bonus_turn)
        return self.calculate_percent_change(base_dmg, buffed_dmg)


class Tingyun(HarmonyCharacter):
    def __init__(self):
        super().__init__()

    def ult_buff(self, *args, **kwargs) -> int:
        # assume Tingyun gain 50 energy per 5 cycles
        ult_gain = int(50 / 5)
        return ult_gain

    def skill_buff(self, *args, **kwargs) -> float:
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

        energy_regen_buff = self.energy_regen_buff(total_energy_gain=self.ult_buff() + 30)

        atk_buff = self.calculate_percent_change(self.trailblazer_atk, ally_atk, decimal_mode=True)

        buffed_dmg = self.calculate_trailblazer_dmg(dmg_bonus_multiplier=energy_regen_buff,
                                                    atk_bonus=atk_buff,
                                                    additional_dmg=additional_dmg)
        return self.calculate_percent_change(base_dmg, buffed_dmg)
    
    
class HarmonyTrailblazer(HarmonyCharacter):
    def __init__(self):
        super().__init__()

    def ult_buff(self, *args, **kwargs) -> float:
        break_effect = self.default_break_effect * 1.3
        return calculate_super_break_dmg(base_toughness_reduce=30, break_effect=break_effect)

    def a2_trace_buff(self, *args, **kwargs) -> float:
        super_break_dmg_multiplier = 0.6
        return super_break_dmg_multiplier

    def potential_buff(self, *args, **kwargs) -> float:
        base_dmg = self.calculate_trailblazer_dmg()

        super_break_dmg = self.ult_buff() * (1 + self.a2_trace_buff())
        buffed_dmg = self.calculate_trailblazer_dmg(super_break_dmg=super_break_dmg)
        return self.calculate_percent_change(base_dmg, buffed_dmg)
