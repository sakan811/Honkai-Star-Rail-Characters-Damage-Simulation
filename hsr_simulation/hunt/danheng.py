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


class DanHeng(Character):
    def __init__(self, base_char: Character, speed=110, ult_energy=100):
        super().__init__(atk=base_char.default_atk, crit_rate=base_char.default_crit_rate,
                         crit_dmg=base_char.crit_dmg, speed=speed, ult_energy=ult_energy)
        self.default_speed = speed
        self.can_get_talent = True
        self.talent_buff = 0
        self.a4_trace_buff = 0

    def reset_character_data(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f'Resetting {self.__class__.__name__} data...')
        super().reset_character_data()
        self.speed = self.default_speed
        self.can_get_talent = True
        self.talent_buff = 0
        self.a4_trace_buff = 0

    def take_action(self) -> None:
        main_logger.info(f'{self.__class__.__name__} is taking actions...')
        # simulate enemy turn
        if self.weakness_broken:
            if self.enemy_turn_delayed_duration_weakness_broken > 0:
                self.enemy_turn_delayed_duration_weakness_broken -= 1
            else:
                self.regenerate_enemy_toughness()

        self._reset_buffs()
        super().take_action()

    def _use_basic_atk(self) -> None:
        main_logger.info('Using basic atk...')
        if self._is_enemy_slowed():
            dmg = self._calculate_damage(skill_multiplier=1, break_amount=10, dmg_multipliers=[0.4])
        else:
            dmg = self._calculate_damage(1, 10)

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_skill(self) -> None:
        main_logger.info('Using skill...')
        dmg = self._calculate_damage(2.6, 20)

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

    def _use_ult(self) -> None:
        main_logger.info('Using ult...')
        multiplier = 5.2 if self._is_enemy_slowed() else 4
        dmg = self._calculate_damage(multiplier, 30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

    def _apply_talent(self) -> None:
        """
        Simulate talent
        :return: None
        """
        main_logger.info('Simulating talent...')
        if self.can_get_talent and random.random() < 0.5:
            self.talent_buff = 2
            self.can_get_talent = False

    def _reset_buffs(self):
        main_logger.info('Resetting buffs...')
        if self.a4_trace_buff > 0:
            self.a4_trace_buff -= 1
        else:
            self.speed = self.default_speed

        if self.talent_buff > 0:
            self.talent_buff -= 1
        else:
            self.can_get_talent = True

    def _handle_a4_trace(self):
        if random.random() < 0.5:
            self.speed = self.default_speed * 1.2
            self.a4_trace_buff = 2

    @staticmethod
    def _is_enemy_slowed() -> bool:
        return random.random() < 0.5
