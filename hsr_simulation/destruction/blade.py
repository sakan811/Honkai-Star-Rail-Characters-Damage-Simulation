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


class Blade(Character):
    def __init__(self, speed: float = 97, ult_energy: int = 130):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.default_hp = 7000  # Initialize default_hp
        self.hp_loss_tally = 0  # Initialize HP loss tally for Ultimate
        self.charge_stacks = 0  # Initialize Charge stacks for Talent
        self.hellscape_active = False
        self.hellscape_turns = 0

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
        self.hp_loss_tally = 0  # Initialize HP loss tally for Ultimate
        self.charge_stacks = 0  # Initialize Charge stacks for Talent
        self.hellscape_active = False
        self.hellscape_turns = 0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        self._simulate_enemy_weakness_broken()

        # simulate being hit by an enemy
        if random.random() < 0.5:
            self.charge_stacks += 1
            self._apply_talent_effect()

        if self.skill_points > 0 and not self.hellscape_turns:
            self._use_skill()
        elif self.hellscape_active:
            if self.hellscape_turns > 0:
                self.hellscape_turns -= 1
                self._use_enhanced_basic_atk()

            if self.hellscape_turns <= 0:
                self.hellscape_active = False
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
        dmg = self._calculate_damage(skill_multiplier=1, break_amount=10)

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Basic ATK")

    def _use_enhanced_basic_atk(self) -> None:
        """
        Simulate enhanced basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using enhanced basic attack...")
        hp_cost = self.default_hp * 0.10

        self.hp_loss_tally += hp_cost
        self.hp_loss_tally = min(self.hp_loss_tally, int(self.default_hp * 0.9))

        dmg_from_atk = self.atk * 0.4
        dmg_from_max_hp = self.default_hp
        skill_multiplier: float = sum([dmg_from_atk, dmg_from_max_hp]) / self.atk

        dmg = self._calculate_damage(skill_multiplier=skill_multiplier, break_amount=20)

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=30)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Enhanced Basic ATK")

        self.charge_stacks += 1
        self._apply_talent_effect()

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        hp_cost = self.default_hp * 0.30

        self.hp_loss_tally += hp_cost
        self.hp_loss_tally = min(self.hp_loss_tally, int(self.default_hp * 0.9))

        self.hellscape_active = True
        self.hellscape_turns = 3

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=0)

        self.charge_stacks += 1
        self._apply_talent_effect()

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")
        dmg_from_atk = self.atk * 0.4
        dmg_from_max_hp = self.default_hp
        skill_multiplier: float = (
            sum([dmg_from_atk, dmg_from_max_hp, self.hp_loss_tally]) / self.atk
        )

        dmg = self._calculate_damage(skill_multiplier=skill_multiplier, break_amount=20)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Ultimate")

        self.hp_loss_tally = 0  # Reset HP loss tally after Ultimate

        self.charge_stacks += 1
        self._apply_talent_effect()

    def _apply_talent_effect(self) -> None:
        if self.charge_stacks >= 5:
            dmg_from_atk = self.atk * 0.44
            dmg_from_max_hp = self.default_hp * 1.1
            skill_multiplier: float = sum([dmg_from_atk, dmg_from_max_hp]) / self.atk

            dmg = self._calculate_damage(
                skill_multiplier=skill_multiplier, break_amount=10
            )
            self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=10)

            # simulate A6 trace
            dmg *= 1.2

            self.data["DMG"].append(dmg)
            self.data["DMG_Type"].append("Talent")

            self.charge_stacks = 0  # Reset Charge stacks after follow-up attack
