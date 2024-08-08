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


class March7thHunt(Character):
    def __init__(
            self,
            base_char: Character,
            speed: float = 102,
            ult_energy: int = 110
    ):
        super().__init__(atk=base_char.default_atk, crit_rate=base_char.default_crit_rate,
                         crit_dmg=base_char.crit_dmg, speed=speed, ult_energy=ult_energy)
        self.has_shifu = False
        self.charge = 0
        self.ult_buff = False
        self.talent_buff = False
        self.battle_start = True
        self.shifu = None

    def reset_character_data(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f'Resetting {self.__class__.__name__} data...')
        super().reset_character_data()
        self.has_shifu = False
        self.charge = 0
        self.ult_buff = False
        self.talent_buff = False
        self.battle_start = True
        self.shifu = None

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')
        # simulate enemy turn
        if self.weakness_broken:
            if self.enemy_turn_delayed_duration_weakness_broken > 0:
                self.enemy_turn_delayed_duration_weakness_broken -= 1
            else:
                self.regenerate_enemy_toughness()

        # simulate Shifu turn
        self._sim_shifu()

        # reset stats
        self.speed = 102
        self.char_action_value_for_action_forward = []

        # simulate A2 Trace
        if self.battle_start:
            self.battle_start = False
            self.speed *= 1.25

        if self.skill_points > 0 and not self.has_shifu:
            self._use_skill()
        elif self.has_shifu and self.charge >= 7:
            self.talent_buff = True

            # simulate immediate action
            self.char_action_value_for_action_forward.append(self.simulate_action_forward(action_forward_percent=1))

            # check if ult can be used
            if self._can_use_ult():
                self._use_ult()
                self.current_ult_energy = 5

            self.charge -= 7
            self._enhanced_basic_atk()

            self.talent_buff = False
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
        main_logger.info("Using basic attack...")
        break_amount = 10
        if self.shifu == 'DMG':
            self._additional_dmg()
        else:
            break_amount *= 2

        dmg = self._calculate_damage(skill_multiplier=1, break_amount=break_amount)

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

        self.charge += 1
        # ensure Charge not exceed 10
        self.charge = min(10, self.charge)

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info("Using skill...")
        self.has_shifu = True

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info('Using ultimate...')
        if self.talent_buff:
            dmg = self._calculate_damage(skill_multiplier=2.4, break_amount=30, dmg_multipliers=[0.8])
        else:
            dmg = self._calculate_damage(skill_multiplier=2.4, break_amount=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

        self.ult_buff = True

    def _additional_dmg(self) -> None:
        """
        Simulate additional damage from SKill.
        :return: None
        """
        main_logger.info("Simulating additional damage from skill...")
        dmg = self._calculate_damage(skill_multiplier=0.2, break_amount=0)
        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Additional DMG')

    def _enhanced_basic_atk(self) -> None:
        """
        Use enhanced basic ATK
        :return: None
        """
        main_logger.info("Using enhanced basic ATK...")
        default_break_amount = 5
        break_amount = default_break_amount
        if self.shifu == 'DMG':
            self._additional_dmg()
        else:
            break_amount = default_break_amount * 2

        extra_hit_chance = 0.6
        if self.ult_buff:
            self.ult_buff = False
            initial_hit_num = 5
            extra_hit_chance = 0.8
        else:
            initial_hit_num = 3

        for _ in range(initial_hit_num):
            dmg = self._calculate_damage(skill_multiplier=0.8, break_amount=break_amount, dmg_multipliers=[0.8])

            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Enhanced Basic ATK')

        # Attempt to deal extra hits
        max_extra_hits = 3
        extra_hits = 0
        while extra_hits < max_extra_hits:
            if random.random() < extra_hit_chance:
                dmg = self._calculate_damage(skill_multiplier=0.8, break_amount=break_amount, dmg_multipliers=[0.8])

                self.data['DMG'].append(dmg)
                self.data['DMG_Type'].append('Enhanced Basic ATK')

                extra_hits += 1
            else:
                break

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=30)

    def _sim_shifu(self) -> None:
        """
        Simulate March 7th's Shifu.
        :return: None
        """
        main_logger.info("Simulating Shifu...")
        self.charge += 1
        # ensure Charge not exceed 10
        self.charge = min(10, self.charge)

        # random break amount
        break_amount = random.choice([10, 20])
        self.current_enemy_toughness -= break_amount

        # simulate Shifu using Ultimate
        if random.random() < 0.25:
            self.charge += 1
            # ensure Charge not exceed 10
            self.charge = min(10, self.charge)
            self.current_enemy_toughness -= 30

    def set_shifu(self) -> None:
        """
        Set March 7th's Shifu
        :return: None
        """
        main_logger.info('Setting Shifu...')
        choice = random.choice(['DMG', 'SUPPORT'])
        self.shifu = choice
        main_logger.debug(f'Current Shifu is {self.shifu} Type')
