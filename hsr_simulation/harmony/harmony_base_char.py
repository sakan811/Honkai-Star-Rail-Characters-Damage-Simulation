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

    # Default character stats
    DEFAULT_ATK = 2000
    DEFAULT_SPD = 100
    DEFAULT_CRIT_RATE = 0.5
    DEFAULT_CRIT_DMG = 1.0
    DEFAULT_ULT_ENERGY = 120
    DEFAULT_ENEMY_TOUGHNESS = 100
    DEFAULT_BREAK_EFFECT = 1
    DEFAULT_ENERGY_REGEN = 30
    
    # Speed breakpoints for bonus turn calculations
    SPEED_BREAKPOINTS = [
        (200, 6), (182, 5), (178, 4), (172, 4),
        (164, 4), (160, 3), (156, 3), (146, 3),
        (143, 2), (134, 2), (120, 1)
    ]

    def __init__(self):
        # Character stats
        self.trailblazer_atk = self.DEFAULT_ATK
        self.trailblazer_spd = self.DEFAULT_SPD
        self.trailblazer_crit_rate = self.DEFAULT_CRIT_RATE
        self.trailblazer_crit_dmg = self.DEFAULT_CRIT_DMG
        self.trailblazer_ult_energy = self.DEFAULT_ULT_ENERGY
        self.trailblazer_current_energy = 0

        # Enemy stats and state
        self.default_enemy_toughness = self.DEFAULT_ENEMY_TOUGHNESS
        self.default_break_effect = self.DEFAULT_BREAK_EFFECT
        self.enemy_toughness = self.default_enemy_toughness
        self.enemy_turn_delay = 0
        self.has_broken_once = False

    def _calculate_damage(self, atk: float, multiplier: float, 
                         dmg_bonus_multiplier: float, 
                         elemental_dmg_multiplier: float,
                         res_pen_multiplier: float,
                         additional_dmg: float = 0) -> float:
        """
        Calculate damage based on given parameters.
        
        :param atk: Base attack value
        :param multiplier: Skill/Ultimate multiplier
        :param dmg_bonus_multiplier: DMG bonus multiplier
        :param elemental_dmg_multiplier: Elemental DMG multiplier
        :param res_pen_multiplier: RES penetration multiplier
        :param additional_dmg: Additional flat damage
        :return: Calculated damage value
        """
        return ((atk * multiplier + additional_dmg) 
                * dmg_bonus_multiplier 
                * elemental_dmg_multiplier 
                * res_pen_multiplier)

    def calculate_spd_breakpoint(self, bonus_spd: int = 0) -> int:
        """
        Calculates bonus turns based on speed breakpoints.
        
        :param bonus_spd: Additional speed bonus
        :return: Number of bonus turns
        """
        total_spd = self.trailblazer_spd + bonus_spd
        
        for threshold, bonus_turns in self.SPEED_BREAKPOINTS:
            if total_spd >= threshold:
                return bonus_turns
        return 0

    def reduce_enemy_toughness(self, amount: int) -> None:
        """
        Reduce enemy toughness with minimum bound of 0.
        
        :param amount: Toughness reduction amount
        """
        self.enemy_toughness = max(self.enemy_toughness - amount, 0)

    def handle_super_break_damage(self, dmg_list: list, super_break_dmg: float) -> None:
        """
        Handle super break damage logic and state updates.
        
        :param dmg_list: List to append damage values
        :param super_break_dmg: Super break damage value
        """
        if self.enemy_turn_delay > 0:
            dmg_list.append(super_break_dmg)
            self.enemy_turn_delay -= 1
        elif self.has_broken_once and self.enemy_turn_delay <= 0:
            self._reset_enemy_state()
        else:
            self.reduce_enemy_toughness(amount=20)

    def _reset_enemy_state(self) -> None:
        """Reset enemy toughness and break state."""
        self.enemy_toughness = self.default_enemy_toughness
        self.has_broken_once = False

    def handle_break_damage(self, dmg_list: list, break_dmg: float, super_break_dmg: float) -> None:
        """
        Handle break damage application.
        
        :param dmg_list: List to append damage values
        :param break_dmg: Break damage value
        :param super_break_dmg: Super break damage value
        """
        if self.enemy_toughness <= 0 and not self.has_broken_once:
            dmg_list.extend([break_dmg, super_break_dmg])
            self.has_broken_once = True
            self.enemy_turn_delay = 1

    def regenerate_energy(self, amount: int = DEFAULT_ENERGY_REGEN) -> None:
        """
        Regenerate energy with maximum cap.
        
        :param amount: Energy regeneration amount
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
        Applies the ultimate ability of the Trailblazer character.
        
        :param dmg_list: List to append damage values
        :param atk: Attack power
        :param dmg_bonus_multiplier: Base damage multiplier
        :param elemental_dmg_multiplier: Elemental damage multiplier
        :param res_pen_multiplier: Resistance penetration multiplier
        :param additional_dmg: Additional flat damage
        :param super_break_dmg: Super break damage
        :param break_dmg: Break damage
        """
        if not self._can_use_ultimate():
            return

        ult_dmg = self._calculate_damage(
            atk=atk,
            multiplier=4.25,
            dmg_bonus_multiplier=dmg_bonus_multiplier,
            elemental_dmg_multiplier=elemental_dmg_multiplier,
            res_pen_multiplier=res_pen_multiplier,
            additional_dmg=additional_dmg
        )

        self._apply_ultimate_effects(
            dmg_list=dmg_list,
            ult_dmg=ult_dmg,
            super_break_dmg=super_break_dmg,
            break_dmg=break_dmg
        )

    def _can_use_ultimate(self) -> bool:
        """Check if character has enough energy for ultimate."""
        return self.trailblazer_current_energy >= self.trailblazer_ult_energy

    def _apply_ultimate_effects(self, dmg_list: list, ult_dmg: float, 
                              super_break_dmg: float, break_dmg: float) -> None:
        """Apply ultimate effects and handle break mechanics.
        
        :param dmg_list: List to append damage values to
        :param ult_dmg: Calculated ultimate ability damage
        :param super_break_dmg: Super break damage to apply
        :param break_dmg: Break damage to apply
        """
        dmg_list.append(ult_dmg)
        self.trailblazer_current_energy = 0
        
        self.handle_super_break_damage(dmg_list, super_break_dmg)
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
        params = self._prepare_damage_parameters(
            atk_bonus=atk_bonus,
            dmg_bonus_multiplier=dmg_bonus_multiplier,
            elemental_dmg_multiplier=elemental_dmg_multiplier,
            additional_dmg=additional_dmg,
            res_pen_multiplier=res_pen_multiplier,
            break_dmg=break_dmg,
            super_break_dmg=super_break_dmg
        )
        
        dmg_list = []
        turn_count = self._calculate_turn_count(bonus_turns)
        atk = self.trailblazer_atk * params['atk_bonus']

        for _ in range(turn_count):
            self._execute_turn_actions(
                dmg_list=dmg_list,
                atk=atk,
                **params
            )

        return sum(dmg_list)

    def _prepare_damage_parameters(self, **kwargs) -> dict:
        """Prepare and validate damage calculation parameters."""
        params = {
            'atk_bonus': self._process_multiplier(kwargs.get('atk_bonus')),
            'dmg_bonus_multiplier': self._process_multiplier(kwargs.get('dmg_bonus_multiplier')),
            'elemental_dmg_multiplier': self._process_multiplier(kwargs.get('elemental_dmg_multiplier')),
            'res_pen_multiplier': self._process_multiplier(kwargs.get('res_pen_multiplier')),
            'additional_dmg': kwargs.get('additional_dmg', 0),
            'break_dmg': kwargs.get('break_dmg', 0),
            'super_break_dmg': kwargs.get('super_break_dmg', 0)
        }
        return params

    @staticmethod
    def _process_multiplier(value: float = None) -> float:
        """
        Process multiplier values by adding 1 if a value is provided.

        :param value: The multiplier value to process
        :type value: float, optional
        :return: Processed multiplier value (1 + provided value, or 1 if no value provided)
        :rtype: float
        """
        return 1 + value if value is not None else 1

    def _calculate_turn_count(self, bonus_turns: int = None) -> int:
        """
        Calculate total number of turns including any bonus turns.

        :param bonus_turns: Number of additional turns to add
        :type bonus_turns: int, optional
        :return: Total number of turns (base 5 turns plus any bonus)
        :rtype: int
        """
        return 5 + (bonus_turns or 0)

    def _execute_turn_actions(self, dmg_list: list, atk: float, **params) -> None:
        """
        Execute all actions for a single turn including skill damage, energy regeneration,
        break mechanics and ultimate.

        :param dmg_list: List to store calculated damage values
        :type dmg_list: list
        :param atk: Attack value to use for damage calculations
        :type atk: float
        :param params: Additional parameters for damage calculations including:
            - dmg_bonus_multiplier: Damage bonus multiplier
            - elemental_dmg_multiplier: Elemental damage multiplier  
            - res_pen_multiplier: Resistance penetration multiplier
            - additional_dmg: Additional flat damage
            - super_break_dmg: Super break damage
            - break_dmg: Break damage
        :type params: dict
        :return: None
        :rtype: None
        """
        # Calculate and apply skill damage
        skill_dmg = self._calculate_damage(
            atk=atk,
            multiplier=1.25,
            dmg_bonus_multiplier=params['dmg_bonus_multiplier'],
            elemental_dmg_multiplier=params['elemental_dmg_multiplier'],
            res_pen_multiplier=params['res_pen_multiplier'],
            additional_dmg=params['additional_dmg']
        )
        dmg_list.append(skill_dmg)

        # Handle energy and break mechanics
        self.regenerate_energy()
        self.handle_super_break_damage(dmg_list, params['super_break_dmg'])
        self.handle_break_damage(dmg_list, params['break_dmg'], params['super_break_dmg'])

        # Apply ultimate
        self.apply_ultimate(
            dmg_list=dmg_list,
            atk=atk,
            **params
        )

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
