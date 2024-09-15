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


class Himeko(Character):
    def __init__(
            self,
            speed: float = 96,
            ult_energy: int = 120
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.charge = 0
        self.burn = 0
        self.enemy_on_field: int = random.choice([1, 2, 3, 4, 5])
        self.enemy_defeated: int = random.choice([i for i in range(0, self.enemy_on_field + 1)])
        self.enemy_weakness_broken_num: int = random.choice([i for i in range(0, self.enemy_on_field + 1)])
        self.ult_is_used = False

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
        self.charge = 0
        self.burn = 0
        self.enemy_on_field: int = random.choice([1, 2, 3, 4, 5])
        self.enemy_defeated: int = random.choice([i for i in range(0, self.enemy_on_field + 1)])
        self.enemy_weakness_broken_num: int = random.choice([i for i in range(0, self.enemy_on_field + 1)])
        self.ult_is_used = False

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        self._simulate_enemy_weakness_broken()

        if self.burn > 0:
            self._apply_burn_dmg()
            self.burn -= 1
        else:
            self.ult_is_used = False

        # simulate teammates weakness-break enemies
        self.charge += self.enemy_weakness_broken_num
        self.charge = min(self.charge, 3)

        if self.battle_start:
            self.battle_start = False
            self.charge += 1

        # reset stats for each action
        self.crit_rate = self.default_crit_rate

        self._simulate_a6_trace()

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

            self.current_ult_energy = 5

            # simulate defeating the enemy
            enemy_defeated = self.enemy_defeated
            self.current_ult_energy += enemy_defeated * 5

        # simulate teammate attack
        if self.charge >= 3:
            self._use_follow_up_atk()

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        dmg_multiplier = self._simulate_a4_trace()

        dmg = self._calculate_damage(skill_multiplier=1, break_amount=10, dmg_multipliers=[dmg_multiplier])

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

        self._simulate_a2_trace()

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg_multiplier = self._simulate_a4_trace()

        dmg = self._calculate_damage(skill_multiplier=2, break_amount=20, dmg_multipliers=[dmg_multiplier])

        # adjacent target DMG
        adjacent_target = min(self.enemy_on_field - 1, 2)
        for _ in range(adjacent_target):
            dmg += self._calculate_damage(skill_multiplier=0.8, break_amount=10, dmg_multipliers=[dmg_multiplier])

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

        self._simulate_a2_trace()

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using ultimate...')
        dmg_multiplier = self._simulate_a4_trace()

        dmg = self._calculate_damage(skill_multiplier=2.3, break_amount=20, dmg_multipliers=[dmg_multiplier])

        # other target DMG
        for _ in range(self.enemy_on_field - 1):
            dmg += self._calculate_damage(skill_multiplier=2.3, break_amount=20, dmg_multipliers=[dmg_multiplier])

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

        self._simulate_a2_trace()

        self.ult_is_used = True

    def _use_follow_up_atk(self) -> None:
        """
        Simulate follow-up attack damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using follow-up attack...")
        dmg_multiplier = self._simulate_a4_trace()

        dmg = self._calculate_damage(skill_multiplier=1.4, break_amount=10, dmg_multipliers=[dmg_multiplier])

        # other target DMG
        for _ in range(self.enemy_on_field - 1):
            dmg += self._calculate_damage(skill_multiplier=1.4, break_amount=10, dmg_multipliers=[dmg_multiplier])

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=10)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Talent')

        self.charge = 0

        self._simulate_a2_trace()

    def check_if_enemy_weakness_broken(self) -> None:
        """
        Check whether enemy is weakness broken.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__}: Checking Enemy Toughness...')
        if self.current_enemy_toughness <= 0 and not self.enemy_weakness_broken:
            self.enemy_turn_delayed_duration_weakness_broken = 1
            self.enemy_weakness_broken = True
            main_logger.debug(f'{self.__class__.__name__}: Enemy is Weakness Broken')

            self.charge += self.enemy_weakness_broken_num
            self.charge = min(self.charge, 3)

    def _apply_burn_dmg(self) -> None:
        """
        Apply burn damage to the enemy.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__}: Applying Burn Damage...')
        dmg = 0
        max_targets = 5 if self.ult_is_used else 3
        enemy_on_field = min(self.enemy_on_field, max_targets)
        for _ in range(enemy_on_field):
            dmg += self._calculate_damage(skill_multiplier=0.3, break_amount=0, can_crit=False)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('DoT')

    def _simulate_a2_trace(self) -> None:
        """
        Simulate A2 Trace.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__}: Simulating A2 Trace...')
        if random.random() < 0.5:
            self.burn = 2

    def _simulate_a4_trace(self) -> float:
        """
        Simulate A4 Trace.
        :return: DMG Multiplier
        """
        main_logger.info(f'{self.__class__.__name__}: Simulating A4 Trace...')
        if self.burn > 0:
            dmg_multiplier = 0.2
        else:
            dmg_multiplier = 0
        return dmg_multiplier

    def _simulate_a6_trace(self) -> None:
        """
        Simulate A6 Trace.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__}: Simulating A6 Trace...')
        if random.random() < 0.5:
            self.crit_rate += self.default_crit_rate + 0.15
