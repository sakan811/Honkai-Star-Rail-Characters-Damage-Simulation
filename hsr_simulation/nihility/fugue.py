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


class Fugue(Character):
    DEF_REDUCTION = 0.18  # Define DEF reduction as a class constant
    
    def __init__(self, speed: float = 102, ult_energy: int = 130):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.foxian_player = 0
        self.foxian_player_def_reduce_turn = 0
        # Add Cloudflame Luster tracking
        self.cloudflame_luster = 0
        self.cloudflame_luster_active = False

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f"Resetting {self.__class__.__name__} data...")
        super().reset_character_data_for_each_battle()
        self.foxian_player = 0
        self.foxian_player_def_reduce_turn = 0
        # Reset Cloudflame Luster
        self.cloudflame_luster = 0
        self.cloudflame_luster_active = False

    def _apply_cloudflame_luster(self) -> None:
        """
        Apply Cloudflame Luster effect when Fugue is on field
        """
        if not self.cloudflame_luster_active:
            self.cloudflame_luster = 0.4 * self.enemy_toughness
            self.cloudflame_luster_active = True

    def check_if_enemy_weakness_broken(self) -> None:
        """
        Override to handle Cloudflame Luster mechanics
        """
        main_logger.info(f'{self.__class__.__name__}: Checking Enemy Toughness...')
        if self.current_enemy_toughness <= 0:
            excess_break = abs(self.current_enemy_toughness)  # Get the excess break amount
            if not self.enemy_weakness_broken:
                self.enemy_turn_delayed_duration_weakness_broken = 1
                self.enemy_weakness_broken = True
                main_logger.debug(f'{self.__class__.__name__}: Enemy is Weakness Broken')
                self._apply_cloudflame_luster()
                # Apply excess break to Cloudflame Luster if any
                if excess_break > 0:
                    self.cloudflame_luster = max(0, self.cloudflame_luster - excess_break)
            elif self.cloudflame_luster > 0:
                # When enemy is already broken, reduce Cloudflame Luster by excess break amount
                old_cloudflame = self.cloudflame_luster
                self.cloudflame_luster = max(0, self.cloudflame_luster - excess_break)
                # Only trigger super break when Cloudflame Luster is fully depleted
                if old_cloudflame > 0 and self.cloudflame_luster <= 0:
                    self.last_break_amount = excess_break

    def _calculate_damage(
            self,
            skill_multiplier: float,
            break_amount: int,
            dmg_multipliers: list[float] = None,
            dot_dmg_multipliers: list[float] = None,
            res_multipliers: list[float] = None,
            def_reduction_multiplier: list[float] = None,
            can_crit: bool = True) -> float:
        """
        Calculate regular damage and store break amount for talent processing
        """
        # Apply break effect to break amount
        modified_break_amount = int(break_amount * self.break_effect)
        
        # Reduce enemy toughness
        self.current_enemy_toughness -= modified_break_amount
        self.check_if_enemy_weakness_broken()
        
        # Store break amount for talent processing if enemy is broken and no Cloudflame Luster
        if self.enemy_weakness_broken and modified_break_amount > 0 and self.cloudflame_luster <= 0:
            self.last_break_amount = modified_break_amount
        
        return super()._calculate_damage(
            skill_multiplier=skill_multiplier,
            break_amount=modified_break_amount,
            dmg_multipliers=dmg_multipliers,
            dot_dmg_multipliers=dot_dmg_multipliers,
            res_multipliers=res_multipliers,
            def_reduction_multiplier=def_reduction_multiplier,
            can_crit=can_crit
        )

    def _apply_talent_dmg(self) -> None:
        """
        Simulate talent damage - converts break amount to Super Break DMG when enemy is broken
        """
        main_logger.info("Simulating talent damage...")
        
        # If enemy is broken and we have stored break amount, convert to Super Break DMG
        if self.enemy_weakness_broken and hasattr(self, 'last_break_amount') and self.last_break_amount > 0:
            super_break_dmg = self._deal_super_break_dmg(
                enemy_toughness_reduction=self.last_break_amount,
                break_effect=self.break_effect
            )
            self.data['DMG'].append(super_break_dmg)
            self.data['DMG_Type'].append('Super Break DMG')
            
            # Clear the stored break amount after processing
            self.last_break_amount = 0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        self._simulate_enemy_weakness_broken()
        self._apply_talent_dmg()  # Process any pending super break damage

        if self.skill_points > 0 and self.foxian_player <= 0:
            self._use_skill()
        elif self.foxian_player > 0:
            self._use_enhance_basic_atk()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()
            self.current_ult_energy = 5
        
        self._apply_talent_dmg()  # Process any new super break damage

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info("Using basic attack...")

        def_reduce = self.DEF_REDUCTION if self.foxian_player_def_reduce_turn > 0 else 0
        if self.foxian_player_def_reduce_turn > 0:
            self.foxian_player_def_reduce_turn -= 1

        dmg = self._calculate_damage(
            skill_multiplier=1, 
            break_amount=10, 
            def_reduction_multiplier=[def_reduce]
        )
        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Basic ATK")

    def _use_enhance_basic_atk(self) -> None:
        """
        Simulate enhance basic atk damage.
        :return: None
        """
        main_logger.info("Using enhance basic attack...")
        did_foxian_player_attack = random.choice([True, False])

        def_reduce = self.DEF_REDUCTION if did_foxian_player_attack else 0
        if did_foxian_player_attack:
            self.foxian_player_def_reduce_turn = 2

        dmg = self._calculate_damage(
            skill_multiplier=1, 
            break_amount=10, 
            def_reduction_multiplier=[def_reduce]
        )
        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Enhanced Basic ATK")

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info("Using skill...")
        # simulate A4 Trace
        if self.battle_start:
            self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=30)
            self.battle_start = False
            self._simulate_a4_trace()  # Apply A4 trace effect at battle start
        else:
            self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)
        
        dmg = 0
    
        self.foxian_player = 3  # Reset Foxian Player duration

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Skill")

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info("Using ultimate...")
        def_reduce = self.DEF_REDUCTION if self.foxian_player_def_reduce_turn > 0 else 0
        if self.foxian_player_def_reduce_turn > 0:
            self.foxian_player_def_reduce_turn -= 1

        dmg = self._calculate_damage(
            skill_multiplier=2, 
            break_amount=20, 
            def_reduction_multiplier=[def_reduce]
        )

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Ultimate")

    def _simulate_a4_trace(self) -> None:
        """
        Simulate A4 Trace mechanics
        :return: None
        """
        main_logger.info("Simulating A4 Trace...")
        self.break_effect = self.default_break_effect * 1.3
