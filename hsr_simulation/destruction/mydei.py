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

import random
from hsr_simulation.character import Character
from hsr_simulation.configure_logging import main_logger
from hsr_simulation.dmg_calculator import (
    calculate_dmg_multipliers,
    calculate_total_damage,
    calculate_universal_dmg_reduction,
    calculate_res_multipliers,
    calculate_def_multipliers,
)


class Mydei(Character):
    def __init__(self, speed: float = 102, ult_energy: int = 160):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.initial_default_hp = 8000  # Store the initial HP value
        self.default_hp = self.initial_default_hp  # Recommended endgame stats
        self.current_hp = self.default_hp
        self.charge = 0
        self.max_charge = 200
        self.vendetta_active = False
        self.bloodied_chiton_bonus = 0  # A6 trace
        self.a2_revival_count = 3  # A2 trace - Earth and Water - prevents exit from Vendetta on killing blow 3 times
        self._apply_bloodied_chiton()  # Apply A6 trace at battle start

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data,
        to ensure the character starts with default stats and battle-related data,
        in each battle simulation.
        :return: None
        """
        main_logger.info(f"Resetting {self.__class__.__name__} data...")
        super().reset_character_data_for_each_battle()
        self.default_hp = self.initial_default_hp  # Reset to initial HP value
        self.current_hp = self.default_hp
        self.charge = 0
        self.vendetta_active = False
        self.a2_revival_count = 3  # Reset A2 trace revival count
        self._apply_bloodied_chiton()  # Apply A6 trace at battle start

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        self._simulate_enemy_weakness_broken()
        
        # Simulate HP lost from enemy's attack
        enemy_attack = random.randint(1000, 8000)
        self._check_for_killing_blow(enemy_attack)
        self._gain_charge(enemy_attack)
        
        # reset action forward
        self.char_action_value_for_action_forward = []

        # Check if we need to use Godslayer Be God (during Vendetta with sufficient charge)
        if self.vendetta_active and self.charge >= 150:
            self._use_godslayer_be_god()
            self.charge = 0
            
            # After using Godslayer, Mydei still gets to take his normal action
            # This simulates the "extra turn" mentioned in the documentation
            if self.skill_points > 0:
                self._use_skill()
            else:
                self._use_basic_atk()
        # Normal action flow
        elif self.vendetta_active:
            self._use_kingslayer_be_king()
        else:
            # Normal action flow only when not in Vendetta state
            if self.skill_points > 0:
                self._use_skill()
            else:
                self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()
            self.current_ult_energy = 5

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        dmg = self._calculate_damage(
            skill_multiplier=0.5, break_amount=10
        )  # 50% of Max HP

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self._record_damage(dmg, "Basic ATK")

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")

        # Consume HP
        hp_cost = self.current_hp * 0.5
        self.current_hp = max(1, self.current_hp - hp_cost)

        # Gain charge based on HP lost
        self._gain_charge(hp_cost)

        # Calculate damage
        dmg = self._calculate_damage(
            skill_multiplier=0.9, break_amount=20
        )  # 90% of Max HP

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self._record_damage(dmg, "Skill")

    def _use_kingslayer_be_king(self) -> None:
        """
        Simulate Kingslayer Be King damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using Kingslayer Be King...")

        # Consume HP
        hp_cost = self.current_hp * 0.35
        self.current_hp = max(1, self.current_hp - hp_cost)

        # Gain charge based on HP lost
        self._gain_charge(hp_cost)

        # Calculate damage
        dmg = self._calculate_damage(
            skill_multiplier=1.1, break_amount=20
        )  # 110% of Max HP

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=30)

        self._record_damage(dmg, "Enhanced Skill")

    def _use_godslayer_be_god(self) -> None:
        """
        Simulate Godslayer Be God damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using Godslayer Be God...")

        # Handle the action forward (extra turn) for Godslayer Be God
        # This simulates Mydei getting an extra turn to use this ability
        action_value = self.simulate_action_forward(action_forward_percent=1)
        self.char_action_value_for_action_forward.append(action_value)
            
        # Calculate damage
        dmg = self._calculate_damage(
            skill_multiplier=2.8, break_amount=30
        )  # 280% of Max HP

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=10)

        self._record_damage(dmg, "Enhanced Skill 2")

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")

        # Calculate damage
        dmg = self._calculate_damage(
            skill_multiplier=1.6, break_amount=20
        )  # 160% of Max HP

        # Restore HP and gain charge
        self.current_hp = min(self.default_hp, self.current_hp + self.default_hp * 0.2)
        self._gain_charge(20)

        self._record_damage(dmg, "Ultimate")

    def _gain_charge(self, hp_lost: float) -> None:
        """
        Gain charge based on HP lost.
        :param hp_lost: Amount of HP lost
        :return: None
        """
        # 1 point of Charge for every 1% of HP lost
        charge_gain = hp_lost / self.default_hp * 100 * (1 + self.bloodied_chiton_bonus)
        self.charge = min(self.max_charge, self.charge + charge_gain)

        if self.charge >= 100 and not self.vendetta_active:
            self._enter_vendetta_state()

    def _enter_vendetta_state(self) -> None:
        """
        Enter Vendetta state.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is entering Vendetta state...")
        self.vendetta_active = True
        self.charge = 0
        
        # Store original HP and increase it for Vendetta state
        vendetta_hp_multiplier = 1.5
        self.default_hp *= vendetta_hp_multiplier  # Max HP increases by 50%
        
        # Heal 25% of new max HP
        self.current_hp = min(self.default_hp, self.current_hp + self.default_hp * 0.25)
        
        # Action forward
        action_value = self.simulate_action_forward(action_forward_percent=1)
        self.char_action_value_for_action_forward.append(action_value)

    def _apply_bloodied_chiton(self) -> None:
        """
        Apply Bloodied Chiton trace effect.
        :return: None
        """
        if self.default_hp > 4000:
            excess_hp = min(4000, self.default_hp - 4000)
            self.bloodied_chiton_bonus = excess_hp / 100 * 0.025  # 2.5% per 100 HP
            self.crit_rate += excess_hp / 100 * 0.012  # 1.2% per 100 HP

    def _check_for_killing_blow(self, damage: float) -> None:
        """
        Check if enemy attack would kill Mydei and handle it according to A2 trace rules.
        :param damage: Amount of damage from enemy attack
        :return: None
        """
        # Check if damage would reduce HP to 0 or below
        if self.current_hp <= damage:
            if self.vendetta_active:
                if self.a2_revival_count > 0:
                    # A2 trace effect: prevent exit from Vendetta state
                    main_logger.info(f"{self.__class__.__name__} A2 trace prevents death in Vendetta state! Remaining uses: {self.a2_revival_count-1}")
                    self.a2_revival_count -= 1
                    
                    # Restore 50% of max HP (per talent description)
                    self.current_hp = self.default_hp * 0.5
                else:
                    # Normal Vendetta death prevention (after A2 uses exhausted)
                    main_logger.info(f"{self.__class__.__name__} prevents death by exiting Vendetta state!")
                    self.vendetta_active = False
                    self.charge = 0
                    self.current_hp = self.default_hp * 0.5  # Restore 50% of max HP
                    
                    # Reset HP back to pre-Vendetta value
                    self.default_hp = self.initial_default_hp
                    self._apply_bloodied_chiton()  # Reapply A6 trace after resetting HP
            else:
                # If not in Vendetta, Mydei dies - reset all stats for simulation purposes
                main_logger.info(f"{self.__class__.__name__} has died! Resetting all stats for simulation...")
                self.reset_character_data_for_each_battle()
        else:
            # Normal damage taking
            self.current_hp = max(1, self.current_hp - damage)

    def _calculate_damage(
        self,
        skill_multiplier: float,
        break_amount: int,
        dmg_multipliers: list[float] = None,
        dot_dmg_multipliers: list[float] = None,
        res_multipliers: list[float] = None,
        def_reduction_multiplier: list[float] = None,
        can_crit: bool = True,
    ) -> float:
        """
        Calculates damage based on HP multipliers instead of ATK.
        Mydei is an HP scaler, so all his damage is based on his Max HP.
        :param skill_multiplier: Skill multiplier of Max HP.
        :param break_amount: Break amount that the attack can do.
        :param dmg_multipliers: DMG multipliers.
        :param dot_dmg_multipliers: Dot DMG multipliers.
        :param res_multipliers: RES multipliers.
        :param def_reduction_multiplier: DEF reduction multipliers.
        :param can_crit: Whether the DMG can CRIT.
        :return: Damage.
        """
        main_logger.info(f"{self.__class__.__name__}: Calculating HP-based damage...")
        # reduce enemy toughness
        self.current_enemy_toughness -= break_amount

        self.check_if_enemy_weakness_broken()

        # Calculate base damage using HP instead of ATK
        base_dmg = self.default_hp * skill_multiplier

        if random.random() < self.crit_rate and can_crit:
            dmg_multiplier = calculate_dmg_multipliers(
                crit_dmg=self.crit_dmg, dmg_multipliers=dmg_multipliers
            )
        else:
            dmg_multiplier = calculate_dmg_multipliers(
                dmg_multipliers=dmg_multipliers, dot_dmg=dot_dmg_multipliers
            )

        dmg_reduction = calculate_universal_dmg_reduction(self.enemy_weakness_broken)
        def_reduction = calculate_def_multipliers(
            def_reduction_multiplier=def_reduction_multiplier
        )
        res_multiplier = calculate_res_multipliers(res_multipliers)

        total_dmg = calculate_total_damage(
            base_dmg=base_dmg,
            dmg_multipliers=dmg_multiplier,
            res_multipliers=res_multiplier,
            dmg_reduction=dmg_reduction,
            def_reduction_multiplier=def_reduction,
        )

        return total_dmg
