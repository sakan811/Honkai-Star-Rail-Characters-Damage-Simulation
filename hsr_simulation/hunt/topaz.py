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
from hsr_simulation.dmg_calculator import calculate_base_dmg, calculate_universal_dmg_reduction, \
    calculate_dmg_multipliers, calculate_total_damage, calculate_res_multipliers
from hsr_simulation.character import Character

logger = configure_logging_with_file('simulate_turns.log')


class Topaz(Character):
    def __init__(self,
                 atk=2000,
                 crit_rate=0.5,
                 crit_dmg=1,
                 speed=110,
                 ult_energy=100
                 ):
        super().__init__(
            atk,
            crit_rate,
            crit_dmg,
            speed,
            ult_energy
        )
        self.starting_spd = speed
        self.can_get_talent = True
        self.talent_buff = 0
        self.a4_trace_buff = 0

    def take_action(self) -> float:
        """
        Simulate character's action
        :return: Damage
        """
        # Reset Dan Heng's speed after A4 buff is gone
        if self.a4_trace_buff > 0:
            self.a4_trace_buff -= 1
        else:
            self.speed = self.starting_spd

        # Talent buff can be obtained again after 2 turns
        if self.talent_buff > 0:
            self.talent_buff -= 1
        else:
            self.can_get_talent = True

        total_dmg = []
        logger.info('Taking actions...')
        if self.skill_points > 0:
            skill_dmg, break_amount = self.use_skill(self.check_enemy_toughness())
            logger.debug(f'Skill dmg: {skill_dmg}')

            self.skill_points -= 1
            self.current_ult_energy += 30

            self.enemy_toughness -= break_amount

            total_dmg.append(skill_dmg)
        else:
            basic_atk_dmg, break_amount = self.basic_atk(self.check_enemy_toughness())
            logger.debug(f'Basic atk dmg: {basic_atk_dmg}')

            self.skill_points += 1
            self.current_ult_energy += 20

            self.enemy_toughness -= break_amount

            total_dmg.append(basic_atk_dmg)

        self._handle_a4_trace()

        if self.current_ult_energy >= self.ult_energy:
            ult_dmg, break_amount = self.use_ult(self.check_enemy_toughness())
            logger.debug(f'ult dmg: {ult_dmg}')

            total_dmg.append(ult_dmg)

            self.enemy_toughness -= break_amount

            self.current_ult_energy = 5

        self._handle_a4_trace()

        return sum(total_dmg)

    def basic_atk(self, weakness_broken: bool) -> tuple[float, int]:
        """
        Basic atk calculation.
        :param weakness_broken: Weakness Broken Indicator.
        :return: Basic atk damage and Break Amount.
        """
        logger.info("Doing a basic atk...")
        break_amount = 10
        if random.random() < self.crit_rate:
            base_dmg = calculate_base_dmg(atk=self.atk)
            dmg_multiplier, res_pen = self._random_talent(is_crit=True)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)
            return total_dmg, break_amount
        else:
            base_dmg = calculate_base_dmg(atk=self.atk)
            dmg_multiplier, res_pen = self._random_talent(is_crit=False)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)
            return total_dmg, break_amount

    def use_skill(self, weakness_broken: bool) -> tuple[float, int]:
        """
        Uses skill.
        :param weakness_broken: Weakness Broken Indicator.
        :return: Damage and Break Amount
        """
        logger.info("Doing a skill attack...")
        break_amount = 20
        if random.random() < self.crit_rate:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=2.6)
            dmg_multiplier, res_pen = self._random_talent(is_crit=True)

            if self._random_enemy_slowed():
                dmg_multiplier += 0.4

            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)
            return total_dmg, break_amount
        else:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=2.6)
            dmg_multiplier, res_pen = self._random_talent(is_crit=False)

            if self._random_enemy_slowed():
                dmg_multiplier += 0.4

            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)
            return total_dmg, break_amount

    def use_ult(self, weakness_broken: bool) -> tuple[float, int]:
        """
        Uses ultimate skill.
        :param weakness_broken: Weakness Broken Indicator.
        :return: Damage and Break Amount
        """
        logger.info('Using ultimate...')
        break_amount = 30
        if random.random() < self.crit_rate:
            if self._random_enemy_slowed():
                base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=5.2)
            else:
                base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=4)

            dmg_multiplier, res_pen = self._random_talent(is_crit=True)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)
            return total_dmg, break_amount
        else:
            if self._random_enemy_slowed():
                base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=5.2)
            else:
                base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=4)

            dmg_multiplier, res_pen = self._random_talent(is_crit=False)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)
            return total_dmg, break_amount

    @staticmethod
    def _random_enemy_slowed() -> bool:
        logger.info('Randomizing enemy slowed')
        if random.random() < 0.5:
            return True
        else:
            return False

    def _handle_a4_trace(self) -> None:
        logger.info('Handling A4 Trace...')
        if random.random() < 0.5:
            self.speed = self.starting_spd * 1.2
            self.a4_trace_buff = 2

    def _random_talent(self, is_crit: bool) -> tuple[float, float]:
        """
        Random talent to determine multipliers.
        :param is_crit: Whether it's a crit hit.
        :return: Damage multiplier and Res multiplier.
        """
        logger.info('Random resurgence...')
        if self.can_get_talent:
            talent_chance = 0.5
        else:
            talent_chance = 0

        if is_crit:
            if random.random() < talent_chance:
                res_pen = [0.36]
                res_multiplier = calculate_res_multipliers(res_pen=res_pen)
                dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg)
                self.talent_buff = 2
                return dmg_multiplier, res_multiplier
            else:
                dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg)
                res_multiplier = calculate_res_multipliers()
                return dmg_multiplier, res_multiplier
        else:
            if random.random() < talent_chance:
                dmg_multiplier = calculate_dmg_multipliers()
                res_pen = [0.36]
                res_multiplier = calculate_res_multipliers(res_pen=res_pen)
                self.talent_buff = 2
                return dmg_multiplier, res_multiplier
            else:
                return 1, 1
