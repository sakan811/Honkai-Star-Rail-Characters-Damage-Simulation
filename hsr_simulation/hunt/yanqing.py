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
    def __init__(self, atk=2000, crit_rate=0.5, crit_dmg=1, speed=109, ult_energy=140):
        super().__init__(atk, crit_rate, crit_dmg, speed, ult_energy)
        self.a6_spd_buff = 0
        self.starting_spd = speed
        self.starting_crit_rate = crit_rate
        self.starting_crit_dmg = crit_dmg
        self.ult_buff = 0
        self.soulsteel_sync = 0

    def take_action(self) -> float:
        self._reset_stats()
        self._handle_soulsteel_sync()

        total_dmg = []
        logger.info('Taking actions...')

        if self.skill_points > 0:
            dmg, break_amount = self._use_skill()
            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Skill')
        else:
            dmg, break_amount = self._use_basic_atk()
            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Basic ATK')

        self.enemy_toughness -= break_amount

        total_dmg.append(dmg)

        talent_dmg = self._handle_soulsteel_sync_follow_up()
        total_dmg.append(talent_dmg)
        self.data['DMG'].append(talent_dmg)
        self.data['DMG_Type'].append('Talent')

        trace_dmg = self._handle_a2_trace()
        total_dmg.append(trace_dmg)
        self.data['DMG'].append(trace_dmg)
        self.data['DMG_Type'].append('Trace')

        if self._can_use_ult():
            ult_dmg = self._use_ult()
            total_dmg.append(ult_dmg)
            self.data['DMG'].append(ult_dmg)
            self.data['DMG_Type'].append('Ultimate')

            talent_dmg = self._handle_soulsteel_sync_follow_up()
            total_dmg.append(talent_dmg)
            self.data['DMG'].append(talent_dmg)
            self.data['DMG_Type'].append('Talent')

            trace_dmg = self._handle_a2_trace()
            total_dmg.append(trace_dmg)
            self.data['DMG'].append(trace_dmg)
            self.data['DMG_Type'].append('Trace')

        return sum(total_dmg)

    def _reset_stats(self) -> None:
        """
        Resets stats variables
        :return: None
        """
        logger.info('Resetting stats...')
        if self.a6_spd_buff > 0:
            self.a6_spd_buff -= 1
        else:
            self.speed = self.starting_spd

        self.crit_dmg = self.starting_crit_dmg
        self.crit_rate = self.starting_crit_rate

        if self._random_hit_by_enemy():
            self.soulsteel_sync = 0

        if self.ult_buff > 0:
            self.ult_buff -= 1
            self.crit_rate += 0.6
            if self.soulsteel_sync > 0:
                self.crit_dmg += 0.5

    def _handle_soulsteel_sync(self) -> None:
        if self.soulsteel_sync > 0:
            self.crit_rate += 0.2
            self.crit_dmg += 0.3

    def _use_skill(self) -> tuple[float, int]:
        logger.info("Using skill...")
        dmg, break_amount = self._calculate_damage(skill_multiplier=2.2, break_amount=20)
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)
        self.soulsteel_sync = 1
        return dmg, break_amount

    def _use_basic_atk(self) -> tuple[float, int]:
        logger.info("Using basic attack...")
        dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10)
        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)
        return dmg, break_amount

    def _use_ult(self) -> float:
        logger.info('Using ultimate...')
        self.crit_rate += 0.6
        if self.soulsteel_sync > 0:
            self.crit_dmg += 0.5
        dmg, break_amount = self._calculate_damage(skill_multiplier=3.5, break_amount=30)
        self.current_ult_energy = 5
        self.enemy_toughness -= break_amount
        return dmg

    def _calculate_damage(self, skill_multiplier: float, break_amount: int) -> tuple[float, int]:
        """
        Calculates damage based on skill_multiplier.
        :param skill_multiplier: Skill multiplier.
        :param break_amount: Break amount that the attack can do.
        :return: Damage and break amount.
        """
        logger.info('Calculating damage...')
        weakness_broken = self.is_enemy_weakness_broken()
        if random.random() < self.crit_rate:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=skill_multiplier)
            dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg)
            self._apply_speed_buff()
        else:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=skill_multiplier)
            dmg_multiplier = 1

        res_multiplier = 1
        dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
        total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_multiplier, dmg_reduction)

        return total_dmg, break_amount

    def _apply_speed_buff(self) -> None:
        logger.info('Applying speed buff...')
        self.speed = self.starting_spd * 1.1
        self.a6_spd_buff = 2

    @staticmethod
    def _random_hit_by_enemy() -> bool:
        logger.info('Randomizing being hit by an enemy...')
        return random.random() < 0.5

    def _handle_soulsteel_sync_follow_up(self) -> float:
        logger.info('Handling Soulsteel Sync follow-up ATK...')
        if random.random() < 0.6:
            dmg, freeze_dmg = self._attack_with_freeze_chance(skill_multiplier=0.5)
            return dmg + freeze_dmg
        return 0

    def _attack_with_freeze_chance(self, skill_multiplier) -> tuple[float, float]:
        logger.info('Attacking with chance to freeze enemy...')
        dmg, break_amount = self._calculate_damage(skill_multiplier=skill_multiplier, break_amount=10)

        self.enemy_toughness -= break_amount

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=10)

        freeze_dmg = 0.5 * self.atk if random.random() < 0.65 else 0
        return dmg, freeze_dmg

    def _handle_a2_trace(self) -> float:
        logger.info('Handling A2 Trace...')

        # Random whether the enemy can do AOE attack
        target_to_be_attacked_by_enemy = random.choice([1, 3])
        if target_to_be_attacked_by_enemy == 1:
            chance = 0.25
        else:
            chance = 0.75

        if random.random() < chance:
            return self._calculate_damage(skill_multiplier=0.3, break_amount=0)[0]
        return 0

    def _can_use_ult(self) -> bool:
        return self.current_ult_energy >= self.ult_energy