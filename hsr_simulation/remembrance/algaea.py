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

from hsr_simulation.character import Character
from hsr_simulation.configure_logging import main_logger


class Algaea(Character):
    # Constants for skill multipliers and break amounts
    BASIC_ATK_MULTIPLIER: float = 1.0  # 100% ATK
    BASIC_ATK_BREAK_AMOUNT: int = 10
    BASIC_ATK_ENERGY_GAIN: int = 10

    # Enhanced Basic ATK (Joint Attack)
    ENHANCED_BASIC_ATK_MULTIPLIER: float = 2.0  # 200% ATK
    ENHANCED_BASIC_ATK_BREAK_AMOUNT: int = 20
    ENHANCED_BASIC_ATK_ENERGY_GAIN: int = 20

    # Skill
    SKILL_ENERGY_GAIN: int = 20

    # Ultimate
    ULT_ENERGY_COST: int = 350
    ULT_ENERGY_GAIN: int = 5
    SUPREME_STANCE_SPEED_BUFF_PERCENT: float = 0.15  # 15% per stack
    SUPREME_STANCE_DURATION: int = 3  # Duration in turns

    # Talent
    TALENT_ADDITIONAL_DMG_MULTIPLIER: float = 0.3  # 30% ATK
    TALENT_ENERGY_GAIN: int = 10

    # Major Traces
    MYOPIC_DOOM_AGLAEA_SPD_MULTIPLIER: float = 7.2  # 720% SPD
    MYOPIC_DOOM_GARMENTMAKER_SPD_MULTIPLIER: float = 3.6  # 360% SPD
    SPEEDING_SOL_ENERGY_THRESHOLD: float = 0.5  # 50%

    def __init__(self, speed: float = 102, ult_energy: int = 350):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.garmentmaker = None
        self.supreme_stance = False
        self.seam_stitch_target = False
        self.retained_speed_buff_stacks = 0  # For Last Thread of Fate trace
        self.supreme_stance_turns_left = 0  # Track Supreme Stance duration
        self.supreme_stance_atk_boost = 0  # Track ATK boost during Supreme Stance
        self._apply_speeding_sol()  # Apply A6 trace at start

    def _apply_speeding_sol(self) -> None:
        """Apply A6 trace - The Speeding Sol."""
        if self.current_ult_energy < self.ult_energy * self.SPEEDING_SOL_ENERGY_THRESHOLD:
            self.current_ult_energy = int(self.ult_energy * self.SPEEDING_SOL_ENERGY_THRESHOLD)
            main_logger.info(f"{self.__class__.__name__} regenerated energy to 50% due to The Speeding Sol")

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f"Resetting {self.__class__.__name__} data...")
        super().reset_character_data_for_each_battle()
        self.supreme_stance = False
        self.seam_stitch_target = False
        self.speed = self.default_speed
        self.supreme_stance_turns_left = 0
        self.supreme_stance_atk_boost = 0
        self._apply_speeding_sol()  # Apply A6 trace at battle start
        if self.garmentmaker:
            self.garmentmaker.reset_character_data_for_each_battle()
            # Apply retained speed buff stacks from Last Thread of Fate
            if self.retained_speed_buff_stacks > 0:
                self.garmentmaker.speed_buff_stacks = self.retained_speed_buff_stacks
                self.garmentmaker._apply_speed_buff_without_increment()

    def _update_supreme_stance(self) -> None:
        """Update Supreme Stance state and ATK boost."""
        if self.supreme_stance and self.supreme_stance_turns_left > 0:
            # Calculate ATK boost from A2 trace for both characters
            self.supreme_stance_atk_boost = (self.speed * self.MYOPIC_DOOM_AGLAEA_SPD_MULTIPLIER) + (self.garmentmaker.speed * self.MYOPIC_DOOM_GARMENTMAKER_SPD_MULTIPLIER)            
            self.supreme_stance_turns_left -= 1
            main_logger.info(f"{self.__class__.__name__} Supreme Stance turns left: {self.supreme_stance_turns_left}")
            
            if self.supreme_stance_turns_left <= 0:
                self._end_supreme_stance()
        else:
            self.supreme_stance_atk_boost = 0

    def _end_supreme_stance(self) -> None:
        """End Supreme Stance and handle Garmentmaker's disappearance."""
        if self.garmentmaker:
            # Store 1 stack of speed buff before disappearing (A4 trace)
            self.retained_speed_buff_stacks = min(1, self.garmentmaker.speed_buff_stacks)
            main_logger.info(f"{self.__class__.__name__} retained {self.retained_speed_buff_stacks} speed buff stack(s) from Last Thread of Fate")
            
            # Reset Garmentmaker's ATK to default before disappearing
            self.garmentmaker.atk = self.garmentmaker.default_atk
            self.garmentmaker.disappear()
            self.garmentmaker = None
        self.supreme_stance = False
        self.seam_stitch_target = False
        self.supreme_stance_turns_left = 0
        self.supreme_stance_atk_boost = 0
        # Reset speed to default only when Supreme Stance ends
        self.speed = self.default_speed

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        # enemy's turn
        self._simulate_enemy_weakness_broken()

        # Update Supreme Stance state and ATK boost
        self._update_supreme_stance()
        
        # reset stats for each action
        self.char_action_value_for_action_forward = []

        # Aglaea's turn
        if self.skill_points > 0 and not self.garmentmaker:
            self._use_skill()
        else:
            if self.supreme_stance:
                self._use_enhanced_basic_atk()
            else:
                self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()
        
        # Garmentmaker's turn
        if self.garmentmaker:
            self.garmentmaker.take_action()

    def _use_basic_atk(self) -> None:
        """Simulate basic attack damage."""
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        dmg = self._calculate_damage(
            skill_multiplier=self.BASIC_ATK_MULTIPLIER,
            break_amount=self.BASIC_ATK_BREAK_AMOUNT,
        )
        self._update_skill_point_and_ult_energy(1, self.BASIC_ATK_ENERGY_GAIN)
        self._record_damage(dmg, "Basic ATK")
        
        # Apply seam stitch after attacks if Garmentmaker is present
        self._apply_seam_stitch()

        # Apply additional damage from talent if target has seam stitch
        if self.seam_stitch_target:
            additional_dmg = self._calculate_damage(
                skill_multiplier=self.TALENT_ADDITIONAL_DMG_MULTIPLIER,
                break_amount=0,
            )
            self._record_damage(additional_dmg, "Talent")
            self._update_skill_point_and_ult_energy(0, self.TALENT_ENERGY_GAIN)

    def _use_enhanced_basic_atk(self) -> None:
        """Simulate enhanced basic attack (Joint Attack) damage."""
        main_logger.info(f"{self.__class__.__name__} is using enhanced basic attack...")
        # Aglaea's damage
        dmg = self._calculate_damage(
            skill_multiplier=self.ENHANCED_BASIC_ATK_MULTIPLIER,
            break_amount=self.ENHANCED_BASIC_ATK_BREAK_AMOUNT,
        )
        self._record_damage(dmg, "Enhanced Basic ATK")
        
        # Apply seam stitch after attacks if Garmentmaker is present
        self._apply_seam_stitch()

        # Garmentmaker's damage if present
        if self.garmentmaker:
            garmentmaker_dmg = self.garmentmaker._calculate_damage(
                skill_multiplier=self.ENHANCED_BASIC_ATK_MULTIPLIER,
                break_amount=self.ENHANCED_BASIC_ATK_BREAK_AMOUNT,
            )
            self._record_damage(garmentmaker_dmg, "Enhanced Basic ATK")

        self._update_skill_point_and_ult_energy(0, self.ENHANCED_BASIC_ATK_ENERGY_GAIN)

        # Apply additional damage from talent if target has seam stitch
        if self.seam_stitch_target:
            additional_dmg = self._calculate_damage(
                skill_multiplier=self.TALENT_ADDITIONAL_DMG_MULTIPLIER,
                break_amount=0,
            )
            self._record_damage(additional_dmg, "Talent")
            self._update_skill_point_and_ult_energy(0, self.TALENT_ENERGY_GAIN)

    def _use_skill(self) -> None:
        """Simulate skill - summon or heal Garmentmaker."""
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        if not self.garmentmaker:
            self.garmentmaker = Garmentmaker()
            self.garmentmaker.set_aglaea(self)
        else:
            # Restore Garmentmaker
            self.garmentmaker.reset_character_data_for_each_battle()

        self._update_skill_point_and_ult_energy(-1, self.SKILL_ENERGY_GAIN)
        self.garmentmaker.take_action()

    def _use_ult(self) -> None:
        """Simulate ultimate - enter Supreme Stance and summon/heal Garmentmaker."""
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")
        
        # Summon or reset Garmentmaker
        if not self.garmentmaker:
            self.garmentmaker = Garmentmaker()
            self.garmentmaker.set_aglaea(self)
        else:
            self.garmentmaker.reset_character_data_for_each_battle()

        # Enter Supreme Stance
        self.supreme_stance = True
        self.supreme_stance_turns_left = self.SUPREME_STANCE_DURATION
        
        # Inherit speed buff stacks from Garmentmaker
        if self.garmentmaker.speed_buff_stacks > 0:
            speed_buff = self.garmentmaker.speed_buff_stacks * self.SUPREME_STANCE_SPEED_BUFF_PERCENT
            self.speed *= (1 + speed_buff)
        
        self.current_ult_energy = self.DEFAULT_ULT_ENERGY_AFTER_ULT

        # Take immediate action
        self.char_action_value_for_action_forward.append(self.simulate_action_forward(1))

    def _apply_seam_stitch(self) -> None:
        """Apply seam stitch to Garmentmaker."""
        if self.garmentmaker and not self.seam_stitch_target:
            self.seam_stitch_target = True
            self.garmentmaker.seam_stitch_target = True

    def _calculate_damage(self, skill_multiplier: float, break_amount: int) -> float:
        """Calculate damage with current ATK including Supreme Stance boost if active."""
        # Add Supreme Stance ATK boost to base ATK before calculation
        original_atk = self.atk
        self.atk += self.supreme_stance_atk_boost
        
        damage = super()._calculate_damage(skill_multiplier, break_amount)
        
        # Restore original ATK
        self.atk = original_atk
        return damage

class Garmentmaker(Character):
    # Constants for skill multipliers and break amounts
    SKILL_MULTIPLIER: float = 1.1  # 110% ATK
    SKILL_BREAK_AMOUNT: int = 10
    SKILL_ENERGY_GAIN: int = 10

    # Constants for speed buff
    SPEED_BUFF: float = 55
    MAX_SPEED_BUFF_STACKS: int = 6

    # Constants for energy regeneration
    ENERGY_REGEN_ON_DISAPPEAR: int = 20

    def __init__(
        self,
        speed: float = 102 * 0.35,  # 35% of Aglaea's speed
        ult_energy: int = 0,  # Garmentmaker doesn't use ult energy
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.speed_buff_stacks = 0
        self.aglaea = None
        self.seam_stitch_target = False
        self.default_speed = speed
        self.default_atk = self.atk  # Store default ATK for reset

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f"Resetting {self.__class__.__name__} data...")
        super().reset_character_data_for_each_battle()
        self.speed_buff_stacks = 0
        self.seam_stitch_target = False
        self.speed = self.default_speed  # Reset speed to base value
        self.atk = self.default_atk  # Reset ATK to base value

    def _apply_speed_buff_without_increment(self) -> None:
        """Apply speed buff from retained stacks without incrementing the stack count."""
        if self.speed_buff_stacks > 0:
            self.speed += self.SPEED_BUFF * self.speed_buff_stacks
            main_logger.info(f"{self.__class__.__name__} applied {self.speed_buff_stacks} retained speed buff stack(s)")

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        # Reset stats for each action
        self.speed = self.default_speed

        # enemy's turn
        self._simulate_enemy_weakness_broken()

        # Apply speed buffs from previous stacks
        if self.speed_buff_stacks > 0:
            self.speed += self.SPEED_BUFF * self.speed_buff_stacks

        # Garmentmaker's turn - always use skill
        self._use_skill()
        if self.seam_stitch_target:
            self._apply_speed_buff()

    def _use_skill(self) -> None:
        """Simulate skill damage."""
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg = self._calculate_damage(
            skill_multiplier=self.SKILL_MULTIPLIER,
            break_amount=self.SKILL_BREAK_AMOUNT,
        )
        self.aglaea._update_skill_point_and_ult_energy(0, self.SKILL_ENERGY_GAIN)
        self.aglaea._record_damage(dmg, "Garmentmaker")

    def _apply_speed_buff(self) -> None:
        """Apply speed buff from talent when attacking seam stitch target."""
        if self.speed_buff_stacks < self.MAX_SPEED_BUFF_STACKS:
            self.speed_buff_stacks += 1
            self.speed += self.SPEED_BUFF
            main_logger.info(f"{self.__class__.__name__} gained speed buff stack {self.speed_buff_stacks}")

    def set_aglaea(self, aglaea: 'Algaea') -> None:
        """Set reference to Aglaea for energy regeneration."""
        self.aglaea = aglaea

    def disappear(self) -> None:
        """Handle Garmentmaker disappearing and regenerating Aglaea's energy."""
        if self.aglaea:
            self.aglaea.current_ult_energy += self.ENERGY_REGEN_ON_DISAPPEAR
            main_logger.info(f"{self.__class__.__name__} disappeared and regenerated {self.ENERGY_REGEN_ON_DISAPPEAR} energy for Aglaea")

    def _calculate_damage(self, skill_multiplier: float, break_amount: int) -> float:
        """Calculate damage with current ATK including Supreme Stance boost if active."""
        # Add Supreme Stance ATK boost to base ATK before calculation
        original_atk = self.atk
        self.atk += self.aglaea.supreme_stance_atk_boost
        
        damage = super()._calculate_damage(skill_multiplier, break_amount)
        
        # Restore original ATK
        self.atk = original_atk
        return damage