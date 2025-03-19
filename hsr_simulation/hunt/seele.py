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


class Seele(Character):
    def __init__(self, speed=115, ult_energy=120):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.sheathed_blade = 0
        self.default_speed = speed
        self.can_resurgence = True
        self.buff_state = False
        self.current_normal_enemy: int = random.choice(
            [2, 4]
        )  # simulate the number of non-boss enemies

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f"Resetting {self.__class__.__name__} data...")
        super().reset_character_data_for_each_battle()
        self.sheathed_blade = 0
        self.speed = self.default_speed
        self.can_resurgence = True
        self.buff_state = False
        self.current_normal_enemy: int = random.choice(
            [2, 4]
        )  # simulate the number of non-boss enemies

    def take_action(self) -> None:
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        # simulate enemy turn
        self._simulate_enemy_weakness_broken()

        self._reset_stats_before_begin_actions()

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        is_resurgence = self._random_resurgence()
        self._handle_resurgence_action_forward(is_resurgence)

        if self._can_use_ult():
            self._use_ult()
            self.current_ult_energy = 5

            is_resurgence = self._random_resurgence()
            self._handle_resurgence_action_forward(is_resurgence)

    def _reset_stats_before_begin_actions(self) -> None:
        """
        Reset stats before begin actions.
        :return: None
        """
        self.speed = self.default_speed
        self.char_action_value_for_action_forward = []

    def _use_basic_atk(self) -> None:
        main_logger.info("Using basic attack...")
        res_pen = self._simulate_a4_trace()
        dmg = self._calculate_damage(
            skill_multiplier=1, break_amount=20, res_multipliers=[res_pen]
        )
        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)
        self.char_action_value_for_action_forward.append(
            self.simulate_action_forward(action_forward_percent=0.2)
        )

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Basic ATK")

    def _use_skill(self) -> None:
        main_logger.info("Using skill...")
        res_pen = self._simulate_a4_trace()
        dmg = self._calculate_damage(
            skill_multiplier=2.2, break_amount=20, res_multipliers=[res_pen]
        )

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)
        self._apply_sheathed_blade_buff()

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Skill")

    def _use_ult(self) -> None:
        main_logger.info("Using ultimate...")
        res_pen = self._simulate_a4_trace()
        ult_dmg = self._calculate_damage(
            skill_multiplier=4.25, break_amount=30, res_multipliers=[res_pen]
        )

        self.data["DMG"].append(ult_dmg)
        self.data["DMG_Type"].append("Ultimate")

    def _apply_sheathed_blade_buff(self):
        if self.sheathed_blade > 0:
            self.speed *= 1.25
            main_logger.debug(f"Speed after Sheathed Blade Buff: {self.speed}")
            self.sheathed_blade -= 1
        else:
            self.sheathed_blade = 2
        main_logger.debug(f"Sheathed Blade: {self.sheathed_blade}")

    def _handle_resurgence_action_forward(self, is_resurgence: bool) -> None:
        main_logger.info("Handling resurgence action forward...")
        if is_resurgence:
            self.char_action_value_for_action_forward.append(
                self.simulate_action_forward(action_forward_percent=1)
            )
            self.can_resurgence = False
            self.buff_state = True
        else:
            self.can_resurgence = True
            self.buff_state = False

    def _random_resurgence(self) -> bool:
        main_logger.info("Random resurgence...")
        resurgence_chance = 0.5 if self.can_resurgence else 0
        return random.random() < resurgence_chance

    def _simulate_a4_trace(self) -> float:
        """
        Simulate A4 trace.
        :return: Quantum RES PEN.
        """
        main_logger.info(f"{self.__class__.__name__}: Simulating A4 trace...")
        if self.buff_state:
            return 0.2
        else:
            return 0
