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

script_logger = configure_logging_with_file(log_dir='logs', log_file='danheng.log',
                                            logger_name='danheng', level='DEBUG')


class DanHeng(Character):
    def __init__(self, atk=2000, crit_rate=0.5, crit_dmg=1, speed=110, ult_energy=100):
        super().__init__(atk, crit_rate, crit_dmg, speed, ult_energy)
        self.starting_spd = speed
        self.can_get_talent = True
        self.talent_buff = 0
        self.a4_trace_buff = 0

    def take_action(self) -> None:
        main_logger.info(f'{self.__class__.__name__} is taking actions...')
        self._reset_buffs()
        super().take_action()

    def _use_basic_atk(self) -> None:
        script_logger.info('Using basic atk...')
        if self._is_enemy_slowed():
            dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10, dmg_multipliers=[0.4])
        else:
            dmg, break_amount = self._calculate_damage(1, 10)
        self.enemy_toughness -= break_amount

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_skill(self) -> None:
        script_logger.info('Using skill...')
        dmg, break_amount = self._calculate_damage(2.6, 20)
        self.enemy_toughness -= break_amount

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

    def _use_ult(self) -> None:
        script_logger.info('Using ult...')
        multiplier = 5.2 if self._is_enemy_slowed() else 4
        dmg, break_amount = self._calculate_damage(multiplier, 30)
        self.enemy_toughness -= break_amount

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

    def _apply_talent(self) -> None:
        """
        Simulate talent
        :return: None
        """
        script_logger.info('Simulating talent...')
        if self.can_get_talent and random.random() < 0.5:
            self.talent_buff = 2
            self.can_get_talent = False

    def _reset_buffs(self):
        script_logger.info('Resetting buffs...')
        if self.a4_trace_buff > 0:
            self.a4_trace_buff -= 1
        else:
            self.speed = self.starting_spd

        if self.talent_buff > 0:
            self.talent_buff -= 1
        else:
            self.can_get_talent = True

    def _handle_a4_trace(self):
        if random.random() < 0.5:
            self.speed = self.starting_spd * 1.2
            self.a4_trace_buff = 2

    @staticmethod
    def _is_enemy_slowed() -> bool:
        return random.random() < 0.5
