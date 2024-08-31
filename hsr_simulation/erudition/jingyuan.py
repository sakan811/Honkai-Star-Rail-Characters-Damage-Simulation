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
from hsr_simulation.dmg_calculator import calculate_base_dmg, calculate_dmg_multipliers, \
    calculate_universal_dmg_reduction, calculate_res_multipliers, calculate_def_multipliers, calculate_total_damage


class Jingyuan(Character):
    def __init__(
            self,
            speed: float = 99,
            ult_energy: int = 130
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.lightning_lord = None
        self.lighting_lord_hit_per_action = 3
        self.enemy_on_field = random.choice([1, 2, 3, 4, 5])
        self.skill_buff = 0

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data,
        to ensure the character starts with default stats and battle-related data,
        in each battle simulation.
        :return: None
        """
        main_logger.info(f'Resetting {self.__class__.__name__} data...')
        super().reset_character_data_for_each_battle()
        self.lightning_lord = None
        self.lighting_lord_hit_per_action = 3
        self.enemy_on_field = random.choice([1, 2, 3, 4, 5])
        self.skill_buff = 0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        self._simulate_enemy_weakness_broken()

        if self.battle_start:
            self.battle_start = False

            # simulate A4 trace
            self.current_ult_energy += 15

        if self.skill_buff > 0:
            self.skill_buff -= 1
            if self.skill_buff <= 0:
                self.crit_rate = self.default_crit_rate

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
        dmg = self._calculate_damage(skill_multiplier=1, break_amount=10)

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg = self._calculate_damage(skill_multiplier=1, break_amount=10)

        # other target DMG
        for _ in range(self.enemy_on_field - 1):
            dmg += self._calculate_damage(skill_multiplier=1, break_amount=10)

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

        self.lighting_lord_hit_per_action += 2
        self.lighting_lord_hit_per_action = min(self.lighting_lord_hit_per_action, 10)

        # simulate A6 trace
        self.skill_buff = 2
        if self.skill_buff > 0:
            self.crit_rate = self.default_crit_rate + 0.1

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using ultimate...')
        dmg = self._calculate_damage(skill_multiplier=2, break_amount=20)

        # other target DMG
        for _ in range(self.enemy_on_field - 1):
            dmg += self._calculate_damage(skill_multiplier=2, break_amount=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

        self.lighting_lord_hit_per_action += 3
        self.lighting_lord_hit_per_action = min(self.lighting_lord_hit_per_action, 10)

    def summon_lightning_lord(self, jingyuan: 'Jingyuan', speed: int = 60) -> 'LightingLord':
        """
        Summon Lightning Lord.
        :param jingyuan: Jing Yuan character.
        :param speed: Speed of the Lightning Lord.
        :return: None.
        """
        main_logger.info('Summon Lightning Lord...')
        self.lightning_lord = LightingLord(jingyuan=jingyuan, speed=speed, ult_energy=0)
        return self.lightning_lord


class LightingLord(Character):
    def __init__(
            self,
            jingyuan: Jingyuan,
            speed: float = 60,
            ult_energy: int = 0
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.jingyuan = jingyuan
        self.is_test = False

    def set_test(self, is_test: bool) -> None:
        """
        Set whether the test is running.
        :param is_test: Whether the test is running.
        :return: None
        """
        self.is_test = is_test

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        self.jingyuan._simulate_enemy_weakness_broken()

        # reset stats for each action
        self.speed = self.default_speed
        self.crit_rate = self.jingyuan.crit_rate

        # simulate A2 trace
        if self.jingyuan.lighting_lord_hit_per_action >= 6:
            self.crit_dmg += 0.25

        increased_hit_per_action = self.jingyuan.lighting_lord_hit_per_action - 3
        self.speed += 10 * increased_hit_per_action

        if self.jingyuan.lighting_lord_hit_per_action > 0:
            self._use_atk()

        # for testing turn count
        if self.is_test:
            self.speed = self.default_speed

    def _use_atk(self) -> None:
        """
        Simulate Lighting Lord atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using Hit per Action attack...")

        for _ in range(self.jingyuan.lighting_lord_hit_per_action):
            dmg = self._calculate_damage(skill_multiplier=0.66, break_amount=5)

            # other target DMG
            for _ in range(self.jingyuan.enemy_on_field - 1):
                dmg += self._calculate_damage(skill_multiplier=0.25, break_amount=5)

            self.jingyuan.data['DMG'].append(dmg)
            self.jingyuan.data['DMG_Type'].append('Lightning Lord')

    def reset_summon_stat_for_each_turn(self) -> None:
        """
        Reset Numby stats
        :return: None
        """
        main_logger.info(f'Resetting {self.__class__.__name__} stats ...')
        super().reset_summon_stat_for_each_turn()
        self.jingyuan.lighting_lord_hit_per_action = 3
        self.crit_dmg = self.default_crit_dmg

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
        self.jingyuan.current_enemy_toughness -= break_amount

        self.jingyuan.check_if_enemy_weakness_broken()

        base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=skill_multiplier)

        if random.random() < self.crit_rate and can_crit:
            dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg, dmg_multipliers=dmg_multipliers)
        else:
            dmg_multiplier = calculate_dmg_multipliers(dmg_multipliers=dmg_multipliers, dot_dmg=dot_dmg_multipliers)

        dmg_reduction = calculate_universal_dmg_reduction(self.jingyuan.enemy_weakness_broken)
        def_reduction = calculate_def_multipliers(def_reduction_multiplier=def_reduction_multiplier)
        res_multiplier = calculate_res_multipliers(res_multipliers)

        total_dmg = calculate_total_damage(base_dmg=base_dmg, dmg_multipliers=dmg_multiplier,
                                           res_multipliers=res_multiplier, dmg_reduction=dmg_reduction,
                                           def_reduction_multiplier=def_reduction)

        return total_dmg

