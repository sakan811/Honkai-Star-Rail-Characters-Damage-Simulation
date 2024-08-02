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

from hsr_simulation.configure_logging import configure_logging_with_file, main_logger
from hsr_simulation.character import Character

script_logger = configure_logging_with_file(log_dir='logs', log_file='march7th_hunt.log',
                                          logger_name='march7th_hunt', level='DEBUG')


class March7thHunt(Character):
    def __init__(
            self,
            atk: int = 2000,
            crit_rate: float = 0.5,
            crit_dmg: float = 1.0,
            speed: float = 102,
            ult_energy: int = 110
    ):
        super().__init__(atk, crit_rate, crit_dmg, speed, ult_energy)
        self.has_shifu = False
        self.charge = 0
        self.ult_buff = False
        self.talent_buff = False
        self.battle_start = True

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')
        self._sim_shifu()

        # reset stats
        self.speed = 102
        self.talent_buff = False

        # simulate A2 Trace
        if self.battle_start:
            self.battle_start = False
            self.speed *= 1.25

        if self.skill_points > 0 and not self.has_shifu:
            self._use_skill()
        elif self.has_shifu and self.charge >= 7:
            self.talent_buff = True

            # simulate immediate action
            self.speed *= 2

            self.charge = 0
            self._enhanced_basic_atk()
        else:
            self._use_basic_atk()
            self._additional_dmg()

        if self._can_use_ult():
            self._use_ult()

            self.current_ult_energy = 5

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        script_logger.info("Using basic attack...")
        dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10)
        self.enemy_toughness -= break_amount

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

        self._additional_dmg()
        self.charge += 1

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        script_logger.info("Using skill...")
        self.has_shifu = True

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        script_logger.info('Using ultimate...')
        if self.talent_buff:
            dmg, break_amount = self._calculate_damage(skill_multiplier=2.4, break_amount=30, dmg_multipliers=[0.8])
            self.enemy_toughness -= break_amount
        else:
            dmg, break_amount = self._calculate_damage(skill_multiplier=2.4, break_amount=30)
            self.enemy_toughness -= break_amount

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

        self.ult_buff = True

    def _additional_dmg(self) -> None:
        """
        Simulate additional damage from SKill.
        :return: None
        """
        script_logger.info("Simulating additional damage from skill...")
        dmg, break_amount = self._calculate_damage(skill_multiplier=0.2, break_amount=0)
        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

    def _enhanced_basic_atk(self) -> None:
        """
        Use enhanced basic ATK
        :return: None
        """
        script_logger.info("Using enhanced basic ATK...")
        extra_hit_chance = 0.6
        if self.ult_buff:
            self.ult_buff = False
            initial_hit_num = 5
            extra_hit_chance = 0.8
        else:
            initial_hit_num = 3

        for _ in range(initial_hit_num):
            dmg, break_amount = self._calculate_damage(skill_multiplier=0.8, break_amount=5, dmg_multipliers=[0.8])

            self.enemy_toughness -= break_amount

            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Enhanced Basic ATK')

            self._additional_dmg()

        # Attempt to deal extra hits
        max_extra_hits = 3
        extra_hits = 0
        while extra_hits < max_extra_hits:
            if random.random() < extra_hit_chance:
                dmg, break_amount = self._calculate_damage(skill_multiplier=0.8, break_amount=5, dmg_multipliers=[0.8])

                self.enemy_toughness -= break_amount

                self.data['DMG'].append(dmg)
                self.data['DMG_Type'].append('Enhanced Basic ATK')

                self._additional_dmg()

                extra_hits += 1
            else:
                break

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=30)

    def _sim_shifu(self) -> None:
        """
        Simulate March 7th's Shifu.
        :return: None
        """
        script_logger.info("Simulating Shifu...")
        self.charge += 1

        # random break amount
        break_amount = random.choice([10, 20])
        self.enemy_toughness -= break_amount

        # simulate Shifu using Ultimate
        if random.random() < 0.25:
            self.charge += 1
            self.enemy_toughness -= 30
