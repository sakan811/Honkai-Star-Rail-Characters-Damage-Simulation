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

from configure_logging import configure_logging_with_file
from hsr_simulation.character import Character
from hsr_simulation.dmg_calculator import calculate_base_dmg, calculate_universal_dmg_reduction, \
    calculate_dmg_multipliers, calculate_total_damage, calculate_res_multipliers

logger = configure_logging_with_file('simulate_turns.log')


class Seele(Character):
    def __init__(self,
                 atk=2000,
                 crit_rate=0.5,
                 crit_dmg=1,
                 speed=115,
                 ult_energy=120
                 ):
        super().__init__(
            atk,
            crit_rate,
            crit_dmg,
            speed,
            ult_energy
        )
        self.sheathed_blade = 0
        self.starting_spd = speed
        self.can_resurgence = True

    def take_action(self) -> float:
        """
        Simulate character's action
        :return: Damage
        """
        # Reset speed to starting value at the start of each action
        self.speed = self.starting_spd

        total_dmg = []
        logger.info('Taking actions...')
        if self.skill_points > 0:
            skill_dmg, break_amount, is_resurgence = self.use_skill(self.check_enemy_toughness())
            logger.debug(f'Skill dmg: {skill_dmg}')

            self.sheathed_blade = 2

            if self.sheathed_blade > 0:
                self.speed = self.starting_spd * 1.25
                logger.debug(f'Speed after Sheathed Blade Buff: {self.speed}')

                self.sheathed_blade -= 1

            self._handle_resurgence_action_forward(is_resurgence)

            logger.debug(f'Sheathed Blade: {self.sheathed_blade}')

            self.skill_points -= 1
            self.current_ult_energy += 30

            self.enemy_toughness -= break_amount

            total_dmg.append(skill_dmg)
        else:
            basic_atk_dmg, break_amount, is_resurgence = self.basic_atk(self.check_enemy_toughness())
            logger.debug(f'Basic atk dmg: {basic_atk_dmg}')

            # action forward 20%
            self.speed = self.speed * 1.2

            self._handle_resurgence_action_forward(is_resurgence)

            self.skill_points += 1
            self.current_ult_energy += 20

            self.enemy_toughness -= break_amount

            total_dmg.append(basic_atk_dmg)

        if self.current_ult_energy >= self.ult_energy:
            ult_dmg, break_amount, is_resurgence = self.use_ult(self.check_enemy_toughness())
            logger.debug(f'ult dmg: {ult_dmg}')

            total_dmg.append(ult_dmg)

            self._handle_resurgence_action_forward(is_resurgence)

            self.enemy_toughness -= break_amount

            self.current_ult_energy = 5

        return sum(total_dmg)

    def _handle_resurgence_action_forward(self, is_resurgence) -> None:
        """
        Handle resurgence action forward buff
        :param is_resurgence: Whether Seele is in Resurgence state.
        :return: None
        """
        logger.info('Handling resurgence action forward...')
        if is_resurgence:
            self.speed = self.speed * 2
            logger.debug(f'Speed after resurgence buff: {self.speed}')

            self.can_resurgence = False
        else:
            self.can_resurgence = True

    def basic_atk(self, weakness_broken: bool) -> tuple[float, int, bool]:
        """
        Basic atk calculation.
        :param weakness_broken: Weakness Broken Indicator.
        :return: Basic atk damage and Break Amount.
        """
        logger.info("Doing a basic atk...")
        break_amount = 20
        if random.random() < self.crit_rate:
            base_dmg = calculate_base_dmg(atk=self.atk)
            dmg_multiplier, res_pen, is_resurgence = self._random_resurgence(is_crit=True)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)
            return total_dmg, break_amount, is_resurgence
        else:
            base_dmg = calculate_base_dmg(atk=self.atk)
            dmg_multiplier, res_pen, is_resurgence = self._random_resurgence(is_crit=False)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)
            return total_dmg, break_amount, is_resurgence

    def use_skill(self, weakness_broken: bool) -> tuple[float, int, bool]:
        """
        Uses skill.
        :param weakness_broken: Weakness Broken Indicator.
        :return: Damage and Break Amount
        """
        logger.info("Doing a skill attack...")
        break_amount = 20
        if random.random() < self.crit_rate:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=2.2)
            dmg_multiplier, res_pen, is_resurgence = self._random_resurgence(is_crit=True)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)
            return total_dmg, break_amount, is_resurgence
        else:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=2.2)
            dmg_multiplier, res_pen, is_resurgence = self._random_resurgence(is_crit=False)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)
            return total_dmg, break_amount, is_resurgence

    def use_ult(self, weakness_broken: bool) -> tuple[float, int, bool]:
        """
        Uses ultimate skill.
        :param weakness_broken: Weakness Broken Indicator.
        :return: Damage and Break Amount
        """
        logger.info('Using ultimate...')
        break_amount = 30
        if random.random() < self.crit_rate:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=4.25)
            dmg_multiplier, res_pen, is_resurgence = self._random_resurgence(is_crit=True)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)
            return total_dmg, break_amount, is_resurgence
        else:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=4.25)
            dmg_multiplier, res_pen, is_resurgence = self._random_resurgence(is_crit=False)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)
            return total_dmg, break_amount, is_resurgence

    def _random_resurgence(self, is_crit: bool) -> tuple[float, float, bool]:
        """
        Random resurgence state to determine the damage multiplier.
        :param is_crit: Whether it's a crit hit.
        :return: Damage multiplier, Res multiplier, and Resurgence indicator.
        """
        logger.info('Random resurgence...')
        if self.can_resurgence:
            resurgence_chance = 0.5
        else:
            resurgence_chance = 0

        if is_crit:
            if random.random() < resurgence_chance:
                dmg_multipliers = [0.8]
                res_pen = [0.2]
                res_multiplier = calculate_res_multipliers(res_pen=res_pen)
                dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg, dmg_multipliers=dmg_multipliers)
                return dmg_multiplier, res_multiplier, True
            else:
                dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg)
                res_multiplier = calculate_res_multipliers()
                return dmg_multiplier, res_multiplier, False
        else:
            if random.random() < resurgence_chance:
                dmg_multipliers = [0.8]
                dmg_multiplier = calculate_dmg_multipliers(dmg_multipliers=dmg_multipliers)
                res_pen = [0.2]
                res_multiplier = calculate_res_multipliers(res_pen=res_pen)
                return dmg_multiplier, res_multiplier, True
            else:
                return 1, 1, False
