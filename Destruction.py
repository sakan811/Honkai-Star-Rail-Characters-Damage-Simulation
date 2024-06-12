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

from Character import Character


class ImbibitorLunae(Character):
    def __init__(self,
                 atk=3000,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=102,
                 skill_multiplier=0,
                 ult_multiplier=3.0,
                 ult_energy=140,
                 ):
        super().__init__(
            atk,
            crit_rate,
            crit_dmg,
            elemental_dmg,
            speed,
            skill_multiplier,
            ult_multiplier,
            ult_energy
        )

    def _simulate_skill_and_ult(self, skill: bool, ult: bool, crit: bool):
        dmg = 0

        if skill:
            if self.enhancement_amount == 1:
                self.righteous_heart += 3
                if self.enhancement_amount > 6:
                    self.righteous_heart = 6
                dmg = self.atk * 2.6
                self.current_ult_energy += 30
            elif self.enhancement_amount == 2:
                self.righteous_heart += 5
                if self.enhancement_amount > 6:
                    self.righteous_heart = 6
                dmg = self.atk * 3.8
                self.outroar += 1
                if self.outroar > 4:
                    self.outroar = 4
                self.current_ult_energy += 35
            elif self.enhancement_amount == 3:
                self.righteous_heart += 7
                if self.enhancement_amount > 6:
                    self.righteous_heart = 6
                dmg = self.atk * 5
                self.outroar += 3
                if self.outroar > 4:
                    self.outroar = 4
                self.current_ult_energy += 40

            if crit:
                crit_dmg = self.crit_dmg
                if self.outroar > 0:
                    crit_dmg += (0.12 * self.outroar)
                    dmg *= crit_dmg
                else:
                    dmg *= crit_dmg

                attack_imaginary_weakness_enemy = random.random() < 0.5
                if attack_imaginary_weakness_enemy:
                    crit_dmg += 0.24
                    dmg *= crit_dmg

            dmg *= self.elemental_dmg

            if self.righteous_heart > 0:
                dmg *= 1 + (0.1 * self.righteous_heart)

            self.total_dmg.append(dmg)
        else:
            self.righteous_heart += 3
            if self.enhancement_amount > 6:
                self.righteous_heart = 6

            dmg = self.atk * self.ult_multiplier

            if crit:
                crit_dmg = self.crit_dmg
                if self.outroar > 0:
                    crit_dmg += (0.12 * self.outroar)
                    dmg *= crit_dmg
                else:
                    dmg *= crit_dmg

                attack_imaginary_weakness_enemy = random.random() < 0.5
                if attack_imaginary_weakness_enemy:
                    crit_dmg += 0.24
                    dmg *= crit_dmg

            dmg *= self.elemental_dmg

            if self.righteous_heart > 0:
                dmg *= 1 + (0.1 * self.righteous_heart)

            self.total_dmg.append(dmg)

            self.current_ult_energy = 5

    def _reset_variables(self):
        self.outroar = 0
        self.righteous_heart = 0

    def _simulate_buff_duration_on_character(self):
        self.outroar = 0
        self.righteous_heart = 0

    def _set_scenario(self, enhancement_amount):
        # set a scenario when using only the given version of Enhanced Basic ATK
        self.enhancement_amount = enhancement_amount[0]

    def _simulate_enter_battle_effect(self):
        self.current_ult_energy += 15


class Firefly(Character):
    def __init__(self,
                 atk=3000,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=104,
                 skill_multiplier=2,
                 ult_multiplier=0,
                 ult_energy=240,
                 ):
        super().__init__(
            atk,
            crit_rate,
            crit_dmg,
            elemental_dmg,
            speed,
            skill_multiplier,
            ult_multiplier,
            ult_energy
        )
        self.complete_combustion = 0
        self.action_forward_counter = 0

    def _simulate_skill_and_ult(self, skill: bool, ult: bool, crit: bool):
        if skill:
            if self.complete_combustion > 0:
                dmg = self.atk * ((0.2 * self.break_effect) + 2)

                if crit:
                    dmg *= self.crit_dmg

                dmg *= self.elemental_dmg

                if self.break_effect >= 2:
                    super_break_dmg = 3767.5533 * (1 + self.break_effect)
                    if 2 <= self.break_effect < 3.6:
                        super_break_dmg = super_break_dmg * 0.35
                    elif self.break_effect >= 3.6:
                        super_break_dmg = super_break_dmg * 0.5

                    dmg += super_break_dmg

                self.total_dmg.append(dmg)
            else:
                dmg = self.atk * self.skill_multiplier

                if crit:
                    dmg *= self.crit_dmg

                dmg *= self.elemental_dmg

                self.total_dmg.append(dmg)

                self.current_ult_energy += self.ult_energy * 0.6

                self.action_forward_counter += 1
        else:
            # I estimated that the Complete Combustion effect lasts 3 turns
            # By calculating Firefly's speed
            self.complete_combustion = 3
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
            self._simulate_skill_and_ult(skill=True, ult=False, crit=crit)

    def _simulate_buff_duration_on_character(self) -> None:
        """
        Simulate the character's buff duration.
        :return: None
        """
        if self.complete_combustion > 0:
            self.complete_combustion -= 1

    def _update_char_spd(self) -> None:
        """
        Update Character's speed.
        :return: None.
        """
        if self.action_forward_counter > 0:
            self.action_forward_counter -= 1
            self.current_char_action_value = 10000 / (self.speed * 1.25)

        if self.complete_combustion:
            self.current_char_action_value = 10000 / (self.speed + 60)
        else:
            self.current_char_action_value = 10000 / self.speed

    def _set_scenario(self, break_effect: tuple) -> None:
        """
        Set scenario for the Character.
        :param break_effect: Amount of Break Effect.
        :return: None
        """
        self.break_effect = break_effect[0]

    def _simulate_enter_battle_effect(self) -> None:
        """
        Simulate the character's enter battle effect.
        :return: None
        """
        # Simulate Firefly's Talent
        self.ult_energy += self.ult_energy * 0.5
