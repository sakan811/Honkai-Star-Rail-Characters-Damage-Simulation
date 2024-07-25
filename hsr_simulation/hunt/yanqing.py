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
    calculate_dmg_multipliers, calculate_total_damage

logger = configure_logging_with_file('simulate_turns.log')


class YanQing(Character):
    def __init__(self,
                 atk=2000,
                 crit_rate=0.5,
                 crit_dmg=1,
                 speed=109,
                 ult_energy=140
                 ):
        super().__init__(
            atk,
            crit_rate,
            crit_dmg,
            speed,
            ult_energy
        )
        self.a6_spd_buff = 0
        self.starting_spd = speed
        self.starting_crit_rate = self.crit_rate
        self.starting_crit_dmg = self.crit_dmg
        self.soulsteel_sync = 0

    def take_action(self) -> float:
        """
        Simulate character's action
        :return: Damage
        """
        # reset stats before taking an action
        if self.a6_spd_buff > 0:
            self.a6_spd_buff -= 1
        else:
            self.speed = self.starting_spd

        self.crit_dmg = self.starting_crit_dmg
        self.crit_rate *= self.starting_crit_rate

        if self._random_hit_by_enemy():
            self.soulsteel_sync = 0

        if self.soulsteel_sync > 0:
            self.crit_rate += 0.2
            self.crit_dmg += 0.3

        total_dmg = []
        logger.info('Taking actions...')
        if self.skill_points > 0:
            skill_dmg, break_amount = self.use_skill(self.check_enemy_toughness())
            logger.debug(f'Skill dmg: {skill_dmg}')

            self.skill_points -= 1
            self.current_ult_energy += 30

            self.enemy_toughness -= break_amount

            self.soulsteel_sync = 1

            total_dmg.append(skill_dmg)
        else:
            basic_atk_dmg, break_amount = self.basic_atk(self.check_enemy_toughness())
            logger.debug(f'Basic atk dmg: {basic_atk_dmg}')

            self.skill_points += 1
            self.current_ult_energy += 20

            self.enemy_toughness -= break_amount

            total_dmg.append(basic_atk_dmg)

        follow_up_dmg = self._handle_soulsteel_sync_follow_up()
        total_dmg.append(follow_up_dmg)

        a2_dmg = self._handle_a2_trace()
        total_dmg.append(a2_dmg)

        if self.current_ult_energy >= self.ult_energy:
            self.crit_rate += 0.6

            if self.soulsteel_sync > 0:
                self.crit_dmg += 0.5

            ult_dmg, break_amount = self.use_ult(self.check_enemy_toughness())
            logger.debug(f'ult dmg: {ult_dmg}')

            total_dmg.append(ult_dmg)

            self.enemy_toughness -= break_amount

            self.current_ult_energy = 5

        follow_up_dmg = self._handle_soulsteel_sync_follow_up()
        total_dmg.append(follow_up_dmg)

        a2_dmg = self._handle_a2_trace()
        total_dmg.append(a2_dmg)

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
            res_multiplier = 1
            dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_multiplier, dmg_reduction)

            self.speed = self.starting_spd * 1.1
            self.a6_spd_buff = 2
            return total_dmg, break_amount
        else:
            base_dmg = calculate_base_dmg(atk=self.atk)
            res_multiplier = 1
            dmg_multiplier = 1
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_multiplier, dmg_reduction)
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
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=2.2)
            res_multiplier = 1
            dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_multiplier, dmg_reduction)

            self.speed = self.starting_spd * 1.1
            self.a6_spd_buff = 2
            return total_dmg, break_amount
        else:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=2.2)
            res_multiplier = 1
            dmg_multiplier = 1
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_multiplier, dmg_reduction)
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
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=3.5)
            res_multiplier = 1
            dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg)
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_multiplier, dmg_reduction)

            self.speed = self.starting_spd * 1.1
            self.a6_spd_buff = 2
            return total_dmg, break_amount
        else:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=3.5)
            res_multiplier = 1
            dmg_multiplier = 1
            dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_multiplier, dmg_reduction)
            return total_dmg, break_amount

    @staticmethod
    def _random_hit_by_enemy() -> bool:
        logger.info('Randomizing being hit by an enemy...')
        if random.random() < 0.5:
            return True
        else:
            return False

    def _handle_soulsteel_sync_follow_up(self) -> float:
        logger.info('Handling Soulsteel Sync follow-up ATK...')
        if random.random() < 0.6:
            dmg, froze = self._attack_with_freeze_chance(skill_multiplier=0.5)
            return dmg + froze
        return 0

    def _attack_with_freeze_chance(self, skill_multiplier) -> tuple[float, float]:
        """
        Simulate Soulsteel Sync follow-up ATK with a chance of freeze enemy.
        :param skill_multiplier: Skill Multiplier
        :return: Soulsteel Sync follow-up DMG and Frozen DMG.
        """
        logger.info('Attacking with chance to freeze enemy...')
        if random.random() < self.crit_rate:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=skill_multiplier)
            dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg)
            res_pen = 1
            dmg_reduction = calculate_universal_dmg_reduction(self.check_enemy_toughness())
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)

            freeze_dmg = 0
            if random.random() < 0.65:  # Freeze chance
                freeze_dmg = 0.5 * self.atk

            self.speed = self.starting_spd * 1.1
            self.a6_spd_buff = 2
            return total_dmg, freeze_dmg
        else:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=skill_multiplier)
            dmg_multiplier = 1
            res_pen = 1
            dmg_reduction = calculate_universal_dmg_reduction(self.check_enemy_toughness())
            total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)
            return total_dmg, 0

    def _handle_a2_trace(self) -> float:
        logger.info('Handling A2 Trace...')
        if random.random() < 0.5:
            if random.random() < self.crit_rate:
                base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=0.3)
                dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg)
                res_pen = 1
                dmg_reduction = calculate_universal_dmg_reduction(self.check_enemy_toughness())
                total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)

                self.speed = self.starting_spd * 1.1
                self.a6_spd_buff = 2
                return total_dmg
            else:
                base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=0.3)
                dmg_multiplier = 1
                res_pen = 1
                dmg_reduction = calculate_universal_dmg_reduction(self.check_enemy_toughness())
                total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_pen, dmg_reduction)
                return total_dmg
        else:
            return 0



