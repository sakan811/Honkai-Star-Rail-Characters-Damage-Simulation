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

class HarmonyCharacter:
    """
    Class representing a Harmony character.
    Using some Physical Trailblazer stats as a baseline.
    Default crit rate and crit DMG are set to 50% and 100% respectively.
    """

    def __init__(self):
        self.trailblazer_atk = 2000
        self.trailblazer_spd = 100
        self.trailblazer_crit_rate = 0.5
        self.trailblazer_crit_dmg = 1
        self.trailblazer_ult_energy = 120
        self.trailblazer_current_energy = 0
        self.default_enemy_toughness = 100
        self.default_break_effect = 1
        self.enemy_toughness = self.default_enemy_toughness
        self.enemy_turn_delay = 0
        self.has_broken_once = False
        self.enemy_turn_delay = 0

    def calculate_spd_breakpoint(self, bonus_spd: int = 0) -> int:
        """
        Calculates the additional bonus turns a character earns based on their speed
        and a given bonus speed. This calculation is determined by matching the
        character's total speed to predefined speed breakpoints.

        The method iterates through a set of breakpoint thresholds and their
        corresponding bonus turns. If the character's speed meets or exceeds a
        threshold, the corresponding bonus turns are returned. Otherwise, the
        default value of 0 is returned if no thresholds are met.

        :param bonus_spd: An integer representing the additional speed bonus to be
            added to the base trailblazer speed.
        :return: An integer representing the number of bonus turns earned based on
            the calculated speed.
        """
        trailblazer_spd = self.trailblazer_spd + bonus_spd
        spd_breakpoints = [
            (200, 6), (182, 5), (178, 4), (172, 4),
            (164, 4), (160, 3), (156, 3), (146, 3),
            (143, 2), (134, 2), (120, 1)
        ]

        for threshold, bonus_turns in spd_breakpoints:
            if trailblazer_spd >= threshold:
                return bonus_turns
        return 0

    def reduce_enemy_toughness(self, amount: int) -> None:
        """
        Reduce the enemy's toughness and reset if necessary.
        :param amount: Amount to reduce toughness by
        """
        self.enemy_toughness = max(self.enemy_toughness - amount, 0)

    def handle_super_break_damage(self, dmg_list: list, super_break_dmg: float) -> None:
        """
        Handle the logic for applying super break damage and updating enemy toughness states.
        :param dmg_list: List to append damage values
        :param super_break_dmg: Super break damage to apply
        :return: None
        """
        if self.enemy_turn_delay > 0:
            dmg_list.append(super_break_dmg)
            self.enemy_turn_delay -= 1
        elif self.has_broken_once and self.enemy_turn_delay <= 0:
            self.enemy_toughness = self.default_enemy_toughness
            self.has_broken_once = False
        else:
            self.reduce_enemy_toughness(amount=20)

    def handle_break_damage(self, dmg_list: list, break_dmg: float, super_break_dmg: float) -> None:
        """
        Handle the logic for applying break damage when an enemy's toughness reaches zero.
        :param dmg_list: List to append damage values
        :param break_dmg: Standard break damage
        :param super_break_dmg: Super break damage
        :return: None
        """
        if self.enemy_toughness <= 0 and not self.has_broken_once:
            dmg_list.append(break_dmg)
            dmg_list.append(super_break_dmg)
            self.has_broken_once = True
            self.enemy_turn_delay = 1

    def regenerate_energy(self, amount: int = 30) -> None:
        """
        Regenerate energy for Trailblazer.
        :param amount: Amount of energy to regenerate
        """
        self.trailblazer_current_energy = min(
            self.trailblazer_current_energy + amount,
            self.trailblazer_ult_energy
        )

    def apply_ultimate(
            self,
            dmg_list: list,
            atk: float,
            dmg_bonus_multiplier: float,
            elemental_dmg_multiplier: float,
            res_pen_multiplier: float,
            additional_dmg: float,
            super_break_dmg: float,
            break_dmg: float,
    ) -> None:
        """
        Applies the ultimate ability of the Trailblazer character. If the character's current
        energy meets or exceeds the required energy for their ultimate ability, it calculates
        and applies the damage dealt by the ability. The calculated damage is based on the
        character's attack power, additional damage, and multipliers. Additionally, it handles
        super break damage and break damage effects. The final damage values are stored in
        the provided damage list, and the character's energy is reset.

        :param dmg_list: The list where the calculated damage values will be appended.
        :param atk: The attack power of the character.
        :param dmg_bonus_multiplier: Multiplier applied to the ultimate's base damage.
        :param elemental_dmg_multiplier: Multiplier applied to account for elemental damage.
        :param res_pen_multiplier: Multiplier for resistance penetration effects.
        :param additional_dmg: Additional flat damage added to the ultimate calculation.
        :param super_break_dmg: The amount of damage applied due to super break effects.
        :param break_dmg: The amount of damage applied due to standard break effects.
        :return: None
        """
        if self.trailblazer_current_energy >= self.trailblazer_ult_energy:
            ult_dmg = (
                    (atk * 4.25 + additional_dmg)
                    * dmg_bonus_multiplier
                    * elemental_dmg_multiplier
                    * res_pen_multiplier
            )

            dmg_list.append(ult_dmg)
            self.trailblazer_current_energy = 0

            # Handle super break damage
            self.handle_super_break_damage(dmg_list, super_break_dmg)

            # Handle break damage
            self.handle_break_damage(dmg_list, break_dmg, super_break_dmg)

    def calculate_trailblazer_dmg(self,
                                  atk_bonus: float = None,
                                  dmg_bonus_multiplier: float = None,
                                  elemental_dmg_multiplier: float = None,
                                  additional_dmg: float = None,
                                  res_pen_multiplier: float = None,
                                  bonus_turns: int = None,
                                  break_dmg: float = None,
                                  super_break_dmg: float = None) -> float:
        """
        Calculate the damage done by Trailblazer over five cycles.
        :param atk_bonus: ATK bonus
        :param dmg_bonus_multiplier: DMG bonus multiplier
        :param elemental_dmg_multiplier: Elemental DMG multiplier
        :param additional_dmg: Additional flat DMG
        :param res_pen_multiplier: RES pen multiplier
        :param bonus_turns: Bonus turns
        :param break_dmg: Break DMG
        :param super_break_dmg: Super Break DMG
        :return: Total DMG over five cycles
        """
        dmg_list = []

        atk_bonus = (1 + atk_bonus) if atk_bonus is not None else 1
        dmg_bonus_multiplier = (1 + dmg_bonus_multiplier) if dmg_bonus_multiplier is not None else 1
        elemental_dmg_multiplier = (1 + elemental_dmg_multiplier) if elemental_dmg_multiplier is not None else 1
        additional_dmg = additional_dmg if additional_dmg is not None else 0
        res_pen_multiplier = (1 + res_pen_multiplier) if res_pen_multiplier is not None else 1
        break_dmg = break_dmg if break_dmg is not None else 0
        super_break_dmg = super_break_dmg if super_break_dmg is not None else 0

        atk = self.trailblazer_atk * atk_bonus

        if bonus_turns is not None:
            turn_count = 5 + bonus_turns
        else:
            turn_count = 5

        for _ in range(turn_count):
            skill_dmg = (((atk * 1.25) + additional_dmg) * dmg_bonus_multiplier * elemental_dmg_multiplier *
                         res_pen_multiplier)
            dmg_list.append(skill_dmg)

            # Regenerate energy
            self.regenerate_energy(amount=30)

            # Handle super break damage
            self.handle_super_break_damage(dmg_list, super_break_dmg)

            # Handle break damage
            self.handle_break_damage(dmg_list, break_dmg, super_break_dmg)

            # Handle ultimate damage
            self.apply_ultimate(
                dmg_list=dmg_list,
                atk=atk,
                dmg_bonus_multiplier=dmg_bonus_multiplier,
                elemental_dmg_multiplier=elemental_dmg_multiplier,
                res_pen_multiplier=res_pen_multiplier,
                additional_dmg=additional_dmg,
                super_break_dmg=super_break_dmg,
                break_dmg=break_dmg
            )

        total_dmg = sum(dmg_list)
        return total_dmg

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
        damage_increase = (average_damage / base_damage - 1)
        return damage_increase

    def energy_regen_buff(self, total_energy_gain: int) -> float:
        """
        Calculate the percentage increase in energy regen.
        :param total_energy_gain: Total energy gain
        :return: Potential DMG buff as multiplier
        """
        return total_energy_gain / self.trailblazer_ult_energy

    @staticmethod
    def calculate_percent_change(base_value: float, new_value: float, decimal_mode: bool = False) -> float:
        """
        Calculate the percentage change between two values.
        :param base_value: Base value
        :param new_value: New value
        :param decimal_mode: Whether to output as a float value
        :return: Percentage change as percent or decimal
        """
        return ((new_value - base_value) / base_value) * 100 if not decimal_mode \
            else (new_value - base_value) / base_value
