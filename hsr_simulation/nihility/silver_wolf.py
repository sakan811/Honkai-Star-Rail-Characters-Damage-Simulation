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


class SilverWolf(Character):
    def __init__(self, speed: float = 107, ult_energy: int = 110):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.specific_weakness_res_reduce = 0
        self.general_weakness_res_reduce = 0
        self.def_reduce = 0
        self.bug = 0

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f"Resetting {self.__class__.__name__} data...")
        super().reset_character_data_for_each_battle()
        self.specific_weakness_res_reduce = 0
        self.general_weakness_res_reduce = 0
        self.def_reduce = 0
        self.bug = 0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")
        # simulate debuff duration on enemy turn
        if self.def_reduce > 0:
            self.def_reduce -= 1
        if self.bug > 0:
            self.bug -= 1
        if self.specific_weakness_res_reduce > 0:
            self.specific_weakness_res_reduce -= 1
        if self.general_weakness_res_reduce > 0:
            self.general_weakness_res_reduce -= 1

        # simulate enemy turn
        self._simulate_enemy_weakness_broken()

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
        def_reduce_multiplier = [0]
        res_reduce_multiplier = [0]

        # simulate Talent
        if self.bug > 0:
            def_reduce_multiplier += [0.08]

        # simulate Ult debuff
        if self.def_reduce > 0:
            def_reduce_multiplier += [0.45]

        # simulate Skill debuff
        if self.general_weakness_res_reduce > 0:
            res_reduce_multiplier += [0.1]
        if self.specific_weakness_res_reduce > 0:
            res_reduce_multiplier += [0.2]

        dmg = self._calculate_damage(
            skill_multiplier=1,
            break_amount=10,
            def_reduction_multiplier=def_reduce_multiplier,
            res_multipliers=res_reduce_multiplier,
        )

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self._record_damage(dmg, "Basic ATK")

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        # simulate Talent
        def_reduce_multiplier = [0]
        if self.bug > 0:
            def_reduce_multiplier += [0.08]

        # simulate Ult debuff
        if self.def_reduce > 0:
            def_reduce_multiplier += [0.45]

        # simulate RES reduction to a Quantum element
        res_reduction_multiplier = [0]
        if random.random() < 0.5:
            res_reduction_multiplier = [0.2]
            self.specific_weakness_res_reduce = 2

            # simulate A4 trace
            self.specific_weakness_res_reduce += 1

        # simulate all-type RES reduction
        res_reduction_multiplier += [0.1]
        self.general_weakness_res_reduce = 2

        # simulate A6 trace
        current_debuff_on_enemy = (
            self.bug
            + self.def_reduce
            + self.specific_weakness_res_reduce
            + self.general_weakness_res_reduce
        )
        if current_debuff_on_enemy >= 3:
            res_reduction_multiplier += [0.03]

        dmg = self._calculate_damage(
            skill_multiplier=1.96,
            break_amount=20,
            res_multipliers=res_reduction_multiplier,
            def_reduction_multiplier=def_reduce_multiplier,
        )

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self._record_damage(dmg, "Skill")

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")
        # simulate DMG Res reduction to a weakness type
        res_reduction_multiplier = [0]
        if random.random() < 0.5:
            res_reduction_multiplier = [0.2]
            self.specific_weakness_res_reduce = 2

        # simulate all-type RES reduction
        res_reduction_multiplier += [0.1]
        self.general_weakness_res_reduce = 2

        # simulate DEF reduction debuff
        self.def_reduce = 3
        def_reduction_multiplier = [0.45]

        dmg = self._calculate_damage(
            skill_multiplier=3.8,
            break_amount=30,
            def_reduction_multiplier=def_reduction_multiplier,
            res_multipliers=res_reduction_multiplier,
        )

        self._record_damage(dmg, "Ultimate")

    def _apply_bugs(self, a2_trace_trigger: bool = False) -> None:
        """
        Apply bugs (Talent ability)
        :param a2_trace_trigger: Whether A2 trace triggers Bug
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is applying Bugs...")
        base_chance = 0.72

        # simulate A2 trace inflicting chance
        if a2_trace_trigger:
            base_chance = 0.65

        # only simulate DEF reduction bug
        if random.random() < base_chance:
            self.bug = 3

            # simulate A2 trace
            self.bug += 1

    def check_if_enemy_weakness_broken(self, break_type: str = "None") -> None:
        """
        Check whether enemy is weakness broken.
        :param break_type: Break DMG type, e.g., Physical, Fire, etc.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__}: Checking Enemy Toughness...")
        if self.current_enemy_toughness <= 0 and not self.enemy_weakness_broken:
            self.enemy_turn_delayed_duration_weakness_broken = 1
            self.enemy_weakness_broken = True
            self._apply_bugs()
            main_logger.debug(f"{self.__class__.__name__}: Enemy is Weakness Broken")
