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


class Mydei(Character):
    def __init__(self, speed: float = 102, ult_energy: int = 160):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.default_hp = 8000  # Recommended endgame stats
        self.current_hp = self.default_hp
        self.charge = 0
        self.max_charge = 200
        self.vendetta_active = False
        self.bloodied_chiton_bonus = 0  # A6 trace
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
        self.current_hp = self.default_hp
        self.charge = 0
        self.vendetta_active = False
        self._apply_bloodied_chiton()  # Apply A6 trace at battle start

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        self._simulate_enemy_weakness_broken()

        # Handle Vendetta state
        if self.vendetta_active:
            if self.charge >= 150:
                self._use_godslayer_be_god()
                self.charge = 0
            else:
                self._use_kingslayer_be_king()

        # Normal action flow
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

        self._record_damage(dmg, "Kingslayer Be King")

    def _use_godslayer_be_god(self) -> None:
        """
        Simulate Godslayer Be God damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using Godslayer Be God...")

        # Calculate damage
        dmg = self._calculate_damage(
            skill_multiplier=2.8, break_amount=30
        )  # 280% of Max HP

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=10)

        self._record_damage(dmg, "Godslayer Be God")

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
        self.current_hp = min(self.default_hp, self.current_hp + self.default_hp * 0.25)
        self.default_hp *= 1.5  # Max HP increases by 50%

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
