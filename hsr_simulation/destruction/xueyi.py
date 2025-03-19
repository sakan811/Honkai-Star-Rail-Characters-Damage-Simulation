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


class Xueyi(Character):
    def __init__(self, speed: float = 103, ult_energy: int = 120):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.karma_stack = 0
        self.a2_trace_dmg_multiplier = self.break_effect

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
        self.karma_stack = 0
        self.a2_trace_dmg_multiplier = self.break_effect

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        self._simulate_enemy_weakness_broken()

        # simulate enemy toughness reduction from allies
        self.karma_stack += random.choice([0, 3])

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
            skill_multiplier=1,
            break_amount=10,
            dmg_multipliers=[self.a2_trace_dmg_multiplier],
        )

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Basic ATK")

        self._gain_karma_stack()
        if self.karma_stack >= 8:
            self._use_follow_up_atk()

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg = self._calculate_damage(
            skill_multiplier=1.4,
            break_amount=20,
            dmg_multipliers=[self.a2_trace_dmg_multiplier],
        )

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Skill")

        self._gain_karma_stack()
        if self.karma_stack >= 8:
            self._use_follow_up_atk()

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")
        base_break_amount = 40

        break_amount = base_break_amount * self.break_effect
        break_amount = int(break_amount)

        dmg_increased = 1 - (break_amount / base_break_amount)

        # simulate A4 trace
        if self.current_enemy_toughness >= self.enemy_toughness:
            a4_trace_dmg_multiplier = 0.1
        else:
            a4_trace_dmg_multiplier = 0

        dmg = self._calculate_damage(
            skill_multiplier=2.5,
            break_amount=break_amount,
            dmg_multipliers=[
                dmg_increased,
                self.a2_trace_dmg_multiplier,
                a4_trace_dmg_multiplier,
            ],
        )

        self.data["DMG"].append(dmg)
        self.data["DMG_Type"].append("Ultimate")

        self._gain_karma_stack()
        if self.karma_stack >= 8:
            self._use_follow_up_atk()

    def _gain_karma_stack(self) -> None:
        """
        Gain karma stack.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is gaining karma stack...")
        self.karma_stack += 1
        base_max_karma_stack = 8

        # simulate A6 trace
        additional_stack = 6
        max_karma_stack = base_max_karma_stack + additional_stack

        self.karma_stack = min(self.karma_stack, max_karma_stack)

    def _use_follow_up_atk(self) -> None:
        """
        Simulate follow-up attack damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using follow-up attack...")
        num_hit = 3

        for _ in range(num_hit):
            dmg = self._calculate_damage(skill_multiplier=0.9, break_amount=5)

            self.data["DMG"].append(dmg)
            self.data["DMG_Type"].append("Talent")

            self.current_ult_energy += 2

        self.karma_stack -= 8
