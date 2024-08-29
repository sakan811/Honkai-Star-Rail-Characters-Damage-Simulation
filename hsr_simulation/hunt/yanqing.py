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
from hsr_simulation.dmg_calculator import calculate_base_dmg, calculate_universal_dmg_reduction, \
    calculate_dmg_multipliers, calculate_total_damage, calculate_def_multipliers, calculate_res_multipliers


class YanQing(Character):
    def __init__(self, speed=109, ult_energy=140):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.default_speed = speed

        self.a6_spd_buff = 0
        self.ult_buff = 0
        self.soulsteel_sync = 0

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f'Resetting {self.__class__.__name__} data...')
        super().reset_character_data_for_each_battle()
        self.a6_spd_buff = 0
        self.ult_buff = 0
        self.soulsteel_sync = 0
        self.speed = self.default_speed
        self.crit_rate = self.default_crit_rate
        self.crit_dmg = self.default_crit_dmg

    def take_action(self) -> None:
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # simulate enemy turn
        self._simulate_enemy_weakness_broken()

        self._reset_stats()
        self._handle_soulsteel_sync_buff()

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self.soulsteel_sync > 0:
            self._handle_soulsteel_sync_follow_up()

        if self._can_use_ult():
            self._use_ult()

            if self.soulsteel_sync > 0:
                self._handle_soulsteel_sync_follow_up()

    def _reset_stats(self) -> None:
        """
        Resets stats variables
        :return: None
        """
        main_logger.info('Resetting stats...')
        if self.a6_spd_buff > 0:
            self.a6_spd_buff -= 1
        else:
            self.speed = self.default_speed

        self.crit_dmg = self.default_crit_dmg
        self.crit_rate = self.default_crit_rate

        if self._random_hit_by_enemy():
            self.soulsteel_sync = 0

        if self.ult_buff > 0:
            self.ult_buff -= 1
            self.crit_rate += 0.6
            if self.soulsteel_sync > 0:
                self.crit_dmg += 0.5

    def _handle_soulsteel_sync_buff(self) -> None:
        """
        Simulate Soulsteel Sync buff
        :return: None
        """
        main_logger.info('Simulating Soulsteel Sync buff...')
        if self.soulsteel_sync > 0:
            self.crit_rate += 0.2
            self.crit_dmg += 0.3

    def _use_skill(self) -> None:
        main_logger.info("Using skill...")
        dmg = self._calculate_damage(skill_multiplier=2.2, break_amount=20)
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)
        self.soulsteel_sync = 1

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

        self._handle_a2_trace()

    def _use_basic_atk(self) -> None:
        main_logger.info("Using basic attack...")
        dmg = self._calculate_damage(skill_multiplier=1, break_amount=10)
        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

        self._handle_a2_trace()

    def _use_ult(self) -> None:
        main_logger.info('Using ultimate...')
        self.crit_rate += 0.6
        if self.soulsteel_sync > 0:
            self.crit_dmg += 0.5

        dmg = self._calculate_damage(skill_multiplier=3.5, break_amount=30)
        self.current_ult_energy = 5

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

        self._handle_a2_trace()

    def _calculate_damage(
            self,
            skill_multiplier: float,
            break_amount: int,
            dmg_multipliers: list[float] = None,
            dot_dmg_multipliers: list[float] = None,
            res_multipliers: list[float] = None,
            def_reduction_multiplier: list[float] = None,
            can_crit: bool = True) -> float:
        """
        Calculates damage based on multipliers.
        :param skill_multiplier: Skill multiplier.
        :param break_amount: Break amount that the attack can do.
        :param dmg_multipliers: DMG multipliers.
        :param dot_dmg_multipliers: Dot DMG multipliers.
        :param res_multipliers: RES multipliers.
        :param def_reduction_multiplier: DEF reduction multipliers.
        :param can_crit: Whether the DMG can CRIT.
        :return: Damage.
        """
        main_logger.info(f'{self.__class__.__name__}: Calculating damage...')
        # reduce enemy toughness
        self.current_enemy_toughness -= break_amount

        self.check_if_enemy_weakness_broken()

        base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=skill_multiplier)

        if random.random() < self.crit_rate and can_crit:
            dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg, dmg_multipliers=dmg_multipliers)
            self._apply_speed_buff()
        else:
            dmg_multiplier = calculate_dmg_multipliers(dmg_multipliers=dmg_multipliers, dot_dmg=dot_dmg_multipliers)

        dmg_reduction = calculate_universal_dmg_reduction(self.enemy_weakness_broken)
        def_reduction = calculate_def_multipliers(def_reduction_multiplier=def_reduction_multiplier)
        res_multiplier = calculate_res_multipliers(res_multipliers)

        total_dmg = calculate_total_damage(base_dmg=base_dmg, dmg_multipliers=dmg_multiplier,
                                           res_multipliers=res_multiplier, dmg_reduction=dmg_reduction,
                                           def_reduction_multiplier=def_reduction)

        return total_dmg

    def _apply_speed_buff(self) -> None:
        main_logger.info('Applying speed buff...')
        self.speed = self.default_speed * 1.1
        self.a6_spd_buff = 2

    @staticmethod
    def _random_hit_by_enemy() -> bool:
        main_logger.info('Randomizing being hit by an enemy...')
        return random.random() < 0.5

    def _handle_soulsteel_sync_follow_up(self) -> None:
        main_logger.info('Handling Soulsteel Sync follow-up ATK...')
        if random.random() < 0.6:
            dmg, freeze_dmg = self._attack_with_freeze_chance(skill_multiplier=0.5)
            total_dmg = dmg + freeze_dmg
            self.data['DMG'].append(total_dmg)
            self.data['DMG_Type'].append('Talent')
            self._handle_a2_trace()

    def _attack_with_freeze_chance(self, skill_multiplier) -> tuple[float, float]:
        main_logger.info('Attacking with chance to freeze enemy...')
        dmg = self._calculate_damage(skill_multiplier=skill_multiplier, break_amount=10)

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=10)

        freeze_dmg = 0.5 * self.atk if random.random() < 0.65 else 0
        return dmg, freeze_dmg

    def _handle_a2_trace(self) -> None:
        main_logger.info('Handling A2 Trace...')
        if random.random() < 0.5:
            dmg = self._calculate_damage(skill_multiplier=0.3, break_amount=0)

            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Trace')
