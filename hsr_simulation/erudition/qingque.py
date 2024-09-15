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


class Qingque(Character):
    def __init__(
            self,
            speed: float = 98,
            ult_energy: int = 140
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.skill_buff = 0
        self.tile_suit = [0, 1, 2]
        self.hand = [0]
        self.hidden_hand = False
        self.a2_trace_buff = True
        self.a4_trace_buff = False
        self.enemy_on_field = random.choice([0, 1, 2, 3, 4, 5])
        self.past_ally_turn: int = random.choice([1, 2, 3])

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
        self.skill_buff = 0
        self.tile_suit = [0, 1, 2]
        self.hand = [0]
        self.hidden_hand = False
        self.a2_trace_buff = True
        self.a4_trace_buff = False
        self.enemy_on_field = random.choice([0, 1, 2, 3, 4, 5])
        self.past_ally_turn: int = random.choice([1, 2, 3])

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        self._simulate_enemy_weakness_broken()

        # simulate drawing tiles on ally turn
        self._draw_tiles(draw_num=self.past_ally_turn)

        # A6 trace speed buff only lasts for 1 turn
        self.speed = self.default_speed

        self._check_hand()

        if self.skill_points > 0 and not self.hidden_hand:
            self._use_skill()

        self._check_hand()

        if self.hidden_hand:
            self._use_enhanced_basic_atk()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()
            self.current_ult_energy = 5

        # reset stats after taking actions
        self.crit_dmg = self.default_crit_dmg
        self.a4_trace_buff = False

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        dmg_multiplier = 0
        if self.a4_trace_buff:
            dmg_multiplier = 0.1

        dmg = self._calculate_damage(skill_multiplier=1, break_amount=10, dmg_multipliers=[dmg_multiplier])

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_enhanced_basic_atk(self) -> None:
        """
        Simulate enhanced basic atk damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using enhanced basic attack...")
        dmg_multiplier = 0
        if self.a4_trace_buff:
            dmg_multiplier = 0.1

        dmg = self._calculate_damage(skill_multiplier=2.4, break_amount=20, dmg_multipliers=[dmg_multiplier])

        # adjacent target DMG
        adjacent_target = min(self.enemy_on_field - 1, 2)
        for _ in range(adjacent_target):
            dmg += self._calculate_damage(skill_multiplier=1, break_amount=10, dmg_multipliers=[dmg_multiplier])

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Enhanced Basic ATK')

        # simulate A6 trace buff
        self.speed *= 1.1

        # reset stats after using enhanced basic atk
        self.atk = self.default_atk
        self.hidden_hand = False

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        self._draw_tiles(draw_num=2)

        self.crit_dmg += 0.28
        self.a4_trace_buff = True

        if self.a2_trace_buff:
            self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=0)
            self.a2_trace_buff = False
        else:
            self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=0)

    def _draw_tiles(self, draw_num: int) -> None:
        """
        Draw tiles.
        :param draw_num: Number of tiles to draw.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is drawing tiles...')
        for _ in range(draw_num):
            tile = random.choice(self.tile_suit)
            if tile == self.hand[0] and len(self.hand) < 4:
                self.hand.append(tile)

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using ultimate...')
        dmg_multiplier = 0
        if self.a4_trace_buff:
            dmg_multiplier = 0.1

        dmg = self._calculate_damage(skill_multiplier=2, break_amount=20, dmg_multipliers=[dmg_multiplier])

        # other target DMG
        for _ in range(self.enemy_on_field - 1):
            dmg += self._calculate_damage(skill_multiplier=2, break_amount=20, dmg_multipliers=[dmg_multiplier])

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

        self.hand = [0, 0, 0, 0]

    def _check_hand(self) -> None:
        """
        Check if the hand is full of the same tile.
        :return: None
        """
        if len(self.hand) == 4:
            self.hidden_hand = True
            self.hand = [0]
            self.atk *= 1.72
