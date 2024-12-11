class HarmonyCharacter:
    """
    Class representing a Harmony character.
    Using some Physical Trailblazer stats as a baseline.
    Default crit rate and crit DMG are set to 50% and 100% respectively.
    """
    def __init__(self):
        self.trailblazer_crit_rate = 0.5
        self.trailblazer_crit_dmg = 1
        self.trailblazer_ult_energy = 120

    def a2_trace_buff(self, *args, **kwargs) -> float:
        """
        Calculate a potential buff from A2 Trace.
        """
        raise NotImplementedError("a2_trace_buff method is not implemented")

    def a4_trace_buff(self, *args, **kwargs) -> float:
        """
        Calculate a potential buff from A4 Trace.
        """
        raise NotImplementedError("a4_trace_buff method is not implemented")

    def a6_trace_buff(self, *args, **kwargs) -> float:
        """
        Calculate a potential buff from A6 Trace.
        """
        raise NotImplementedError("a6_trace_buff method is not implemented")

    def skill_buff(self, *args, **kwargs) -> float:
        """
        Calculate a potential buff from Skill.
        """
        raise NotImplementedError("skill_buff method is not implemented")

    def ult_buff(self, *args, **kwargs) -> float:
        """
        Calculate a potential buff from Ultimate.
        """
        raise NotImplementedError("ult_buff method is not implemented")

    def talent_buff(self, *args, **kwargs) -> float:
        """
        Calculate a potential buff from Talent.
        """
        raise NotImplementedError("talent_buff method is not implemented")

    def potential_buff(self, *args, **kwargs) -> float:
        """
        Calculate a potential buff from a Harmony character as a percentage.
        :param args: Arguments
        :param kwargs: Keyword arguments
        :return: Potential buff as a percentage
        """
        raise NotImplementedError("potential_buff method is not implemented")

    @staticmethod
    def crit_buff(crit_rate: float, crit_dmg: float) -> float:
        """
        Calculate the percentage increase in damage due to critical hits.
        :param crit_rate: Crit rate (as a decimal, e.g., 0.5 for 50%)
        :param crit_dmg: Crit damage (as a decimal, e.g., 1.5 for 150% crit damage)
        :return: Damage increase as a percentage
        """
        base_damage = 1
        average_damage = (1 - crit_rate) * base_damage + crit_rate * (base_damage * crit_dmg)
        damage_increase = (average_damage / base_damage - 1) * 100
        return damage_increase


class Sunday(HarmonyCharacter):
    def __init__(self):
        super().__init__()

    def talent_buff(self, *args, **kwargs):
        return self.trailblazer_crit_rate + 0.2

    def a2_trace_buff(self, ult_energy_regen):
        if ult_energy_regen < 40:
            ult_energy_regen = 40
        return (ult_energy_regen / self.trailblazer_ult_energy) * 100

    def skill_buff(self):
        skill_base_buff = 0.3
        with_summon_skill_buff = skill_base_buff + 0.5
        skill_buff = (skill_base_buff + with_summon_skill_buff) / 2
        return skill_buff * 100

    def ult_buff(self):
        ult_energy_regen = self.trailblazer_ult_energy * 0.2
        ult_energy_regen_buff_percent = self.a2_trace_buff(ult_energy_regen)

        sunday_crit_dmg_from_trace = 0.373
        sunday_crit_dmg = self.trailblazer_crit_dmg + sunday_crit_dmg_from_trace

        crit_dmg_increased = ((0.3 * sunday_crit_dmg) + 0.12)
        final_crit_dmg = self.trailblazer_crit_dmg + crit_dmg_increased
        final_crit_rate = self.talent_buff()

        crit_buff_percent = self.crit_buff(final_crit_rate, final_crit_dmg)

        return crit_buff_percent + ult_energy_regen_buff_percent

    def potential_buff(self):
        return self.skill_buff() + self.ult_buff()


sunday_buff = Sunday().potential_buff()
print(sunday_buff)