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


class Moze(Character):
    def __init__(self, speed: float = 111, ult_energy: int = 120):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.prey_exist = False
        self.charge = 0
        self.charge_consumed = 0
        self.a2_trace_buff_cooldown = 0
        self.ally_atk_num: int = random.choices([0, 1, 2, 3], [0.1, 0.6, 0.2, 0.1])[0]

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
        self.prey_exist = False
        self.charge = 0
        self.charge_consumed = 0
        self.a2_trace_buff_cooldown = 0
        self.ally_atk_num: int = random.choices([0, 1, 2, 3], [0.1, 0.6, 0.2, 0.1])[0]

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")
        self._simulate_enemy_weakness_broken()

        # reset stats for each turn
        self.char_action_value_for_action_forward = []

        # simulate A4 trace
        if self.battle_start:
            self.battle_start = False

            # assume that each battle has only 1 wave
            self.char_action_value_for_action_forward.append(
                self.simulate_action_forward(0.3)
            )

        if self.skill_points > 0 and not self.prey_exist:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

            self.current_ult_energy = 5

        # simulate allies attacks
        for _ in range(self.ally_atk_num):
            self._talent_additional_dmg()

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

        self._consume_charge()

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg = self._calculate_damage(skill_multiplier=1.5, break_amount=20)

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Skill")

        self.charge = 9
        self.prey_exist = True

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")
        # simulate A6 trace
        dmg_multiplier = 0.25

        dmg = self._calculate_damage(
            skill_multiplier=2.7, break_amount=30, dmg_multipliers=[dmg_multiplier]
        )

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Ultimate")

        self._use_follow_up_atk()

        self._consume_charge()

    def _use_follow_up_atk(self) -> None:
        """
        Simulate follow-up attack damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using follow-up attack...")
        dmg = self._calculate_damage(skill_multiplier=1.6, break_amount=10)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Talent")

        # simulate A2 trace
        if self.a2_trace_buff_cooldown <= 0:
            self.a2_trace_buff_cooldown = 1
            self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=0)
        else:
            self.a2_trace_buff_cooldown -= 1

    def _talent_additional_dmg(self) -> None:
        """
        Simulate additional damage from talent.
        :return: None
        """
        main_logger.info(
            f"{self.__class__.__name__} is dealing talent additional DMG..."
        )
        dmg = self._calculate_damage(skill_multiplier=0.3, break_amount=0)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Talent Additional DMG")

        self._consume_charge()

    def _consume_charge(self) -> None:
        """
        Consume charge to use follow-up attack.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is consuming Charge...")
        self.charge_consumed += 1
        if self.charge_consumed == 3:
            self._use_follow_up_atk()
            self.charge_consumed = 0
            self.charge -= 3
            if self.charge <= 0:
                self.charge = 0
                self.prey_exist = False

                # simulate A4 trace
                self.char_action_value_for_action_forward.append(
                    self.simulate_action_forward(0.2)
                )
