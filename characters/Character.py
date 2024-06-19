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


class Character:
    def __init__(
            self,
            atk,
            crit_rate,
            crit_dmg,
            elemental_dmg,
            speed,
            skill_multiplier,
            ult_multiplier,
            ult_energy
    ):
        """
        Initialize the character.
        :param atk: Attack.
        :param crit_rate: Critical rate.
        :param crit_dmg: Critical damage.
        :param elemental_dmg: Elemental damage bonus.
        :param speed: Speed.
        :param skill_multiplier: Skill multiplier.
        :param ult_multiplier: Ultimate multiplier.
        :param ult_energy: Ultimate energy.
        """
        self.atk = atk
        self.crit_rate = crit_rate
        self.crit_dmg = crit_dmg
        self.elemental_dmg = elemental_dmg
        self.speed = speed
        self.skill_multiplier = skill_multiplier
        self.ult_multiplier = ult_multiplier
        self.total_dmg = []
        self.ult_energy = ult_energy
        self.current_ult_energy = 0
        self.char_action_value = 0
        self.current_char_action_value = 0

    def _simulate_skill_and_ult(self, skill: bool, ult: bool, crit: bool) -> None:
        """
        Simulate skill and ultimate.
        :param skill: True if the action is a skill.
        :param ult: True if the action is an ultimate.
        :param crit: True if the action is a critical hit.
        :return: None
        """
        if skill:
            dmg = self.atk * self.skill_multiplier

            if crit:
                dmg *= self.crit_dmg

            dmg *= self.elemental_dmg

            self.total_dmg.append(dmg)

            self.current_ult_energy += 30
        else:
            dmg = self.atk * self.ult_multiplier

            if crit:
                dmg *= self.crit_dmg

            dmg *= self.elemental_dmg

            self.total_dmg.append(dmg)

            self.current_ult_energy = 5

    def _simulate_actions_during_each_turn(self) -> None:
        """
        Simulate actions during each turn.
        :return: None
        """
        crit = random.random() < self.crit_rate

        self._simulate_skill_and_ult(skill=True, ult=False, crit=crit)

        if self.current_ult_energy >= self.ult_energy:
            self._simulate_skill_and_ult(skill=False, ult=True, crit=crit)

    def _simulate_total_turns_from_given_cycles(self, cycles: int) -> None:
        """
        Simulate total turns from given cycles.
        :param cycles: Number of cycles.
        :return: None
        """
        self.current_char_action_value = 10000 / self.speed
        cycles_action_value = 150 + (100 * (cycles - 1))

        while self.char_action_value < cycles_action_value:
            self._simulate_actions_during_each_turn()
            self._simulate_ally_turn()
            self._simulate_buff_duration_on_character()
            self._simulate_enemy_turn()
            self._simulate_debuff_duration_on_enemy()
            self._update_char_spd()
            self.char_action_value += self.current_char_action_value

        self.char_action_value = 0

    def _simulate_cycles(self) -> int:
        """
        Simulate cycles.
        :return: Total damage after all cycles.
        """
        self.total_dmg = []
        cycles = 30

        self._simulate_total_turns_from_given_cycles(cycles)

        total_dmg_after_all_cycles = sum(self.total_dmg)

        return total_dmg_after_all_cycles

    def calculate_battles(self, *args: tuple) -> tuple[float, int, int]:
        """
        Calculate the damage from each battle simulation.
        :param args: Tuple
        :return:
        """
        self._set_scenario(args)

        total_dmg_from_each_battle = []

        for _ in range(1000):
            self._reset_variables()
            self._simulate_enter_battle_effect()

            total_dmg_from_all_cycles = self._simulate_cycles()

            total_dmg_from_each_battle.append(total_dmg_from_all_cycles)

        avg_dmg = sum(total_dmg_from_each_battle) / len(total_dmg_from_each_battle)

        return avg_dmg, min(total_dmg_from_each_battle), max(total_dmg_from_each_battle)

    def _reset_variables(self) -> None:
        """
        Reset the variables for the battle simulation.
        :return: None
        """
        self.current_ult_energy = 0

    def _simulate_enter_battle_effect(self) -> None:
        """
        Simulate the character's enter battle effect.
        :return: None
        """
        pass

    def _simulate_buff_duration_on_character(self) -> None:
        """
        Simulate the character's buff duration.
        :return: None
        """
        pass

    def _simulate_debuff_duration_on_enemy(self) -> None:
        """
        Simulate the enemy's debuff duration.
        :return: None
        """
        pass

    def _simulate_enemy_turn(self) -> None:
        """
        Simulate the enemy's turn.
        :return: None
        """
        pass

    def _simulate_ally_turn(self) -> None:
        """
        Simulate ally's turn.
        :return: None
        """
        pass

    def _set_scenario(self, *args) -> None:
        """
        Set scenario for the Character.
        :param args: Arguments for the scenario.
        :return: None
        """
        pass

    def _update_char_spd(self) -> None:
        """
        Update Character's speed.
        :return: None.
        """
        pass
