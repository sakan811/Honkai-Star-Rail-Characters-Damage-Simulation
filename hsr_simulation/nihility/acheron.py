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


class Acheron(Character):
    def __init__(
            self,
            atk: int = 2000,
            crit_rate: float = 0.5,
            crit_dmg: float = 1.0,
            speed: float = 101,
            ult_energy: int = 0
    ):
        super().__init__(atk, crit_rate, crit_dmg, speed, ult_energy)
        self.slash_dream = 0
        self.crimson_knot = 0
        self.a4_dmg_multiplier = 0
        self.a6_dmg_multiplier = 0
        self.a6_buff = 0
        self.nihility_teammate_num = 0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # simulate applying debuff on enemy
        if self.nihility_teammate_num > 0:
            main_logger.info('Applying debuff on enemy from ally')
            self.crimson_knot += 1 * self.nihility_teammate_num
            self.crimson_knot = min(9, self.crimson_knot)
            self._update_skill_point_and_ult_energy(skill_points=0, slash_dream=1 * self.nihility_teammate_num)
        main_logger.debug(f'Current Crimson Knot: {self.crimson_knot}')

        if self.a6_buff > 0:
            self.a6_buff -= 1
        main_logger.debug(f'Current A6 Buff: {self.a6_buff}')

        if self.a6_buff <= 0:
            self.a6_dmg_multiplier = 0
        main_logger.debug(f'Current A6 Dmg Multiplier: {self.a6_dmg_multiplier}')

        # Simulate A2 Trace
        if self.battle_start:
            main_logger.info('Battle start!')
            self.battle_start = False
            self.slash_dream += 5
            self.crimson_knot += 5

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        main_logger.debug(f'Current Slash Dream: {self.slash_dream}')

        if self._can_use_ult():
            self._use_ult()
            self._update_skill_point_and_ult_energy(skill_points=0, slash_dream=-9)
            self.crimson_knot = self.slash_dream

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info("Using basic attack...")
        dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10,
                                                   dmg_multipliers=[self.a4_dmg_multiplier, self.a6_dmg_multiplier])
        self.enemy_toughness -= break_amount

        if self.is_enemy_weakness_broken():
            self.do_break_dmg(break_type='Lightning')
            self._update_skill_point_and_ult_energy(skill_points=0, slash_dream=1)

        self._update_skill_point_and_ult_energy(skill_points=1, slash_dream=0)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info("Using skill...")
        dmg_multiplier = [self.a4_dmg_multiplier, self.a6_dmg_multiplier]
        dmg, break_amount = self._calculate_damage(skill_multiplier=1.6, break_amount=20,
                                                   dmg_multipliers=dmg_multiplier)
        self.enemy_toughness -= break_amount

        if self.is_enemy_weakness_broken():
            self.do_break_dmg(break_type='Lightning')
            self._update_skill_point_and_ult_energy(skill_points=0, slash_dream=1)

        self._update_skill_point_and_ult_energy(skill_points=-1, slash_dream=1)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

        self.crimson_knot += 1
        self.crimson_knot = min(9, self.crimson_knot)

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info('Using ultimate...')
        total_dmg = []
        res_pen = [0.2]

        # Rainblade
        for _ in range(3):
            # A6 Trace
            if self.crimson_knot > 0:
                self.a6_dmg_multiplier += 0.3
                self.a6_dmg_multiplier = min(0.9, self.a6_dmg_multiplier)
                self.a6_buff = 3

            # Rainblade hits
            rainblade_dmg, break_amount = self._calculate_damage(skill_multiplier=0.24, break_amount=5,
                                                                 res_multipliers=res_pen,
                                                                 dmg_multipliers=[self.a4_dmg_multiplier,
                                                                                  self.a6_dmg_multiplier])
            self.enemy_toughness -= break_amount

            if self.is_enemy_weakness_broken():
                self.do_break_dmg(break_type='Lightning')
                self._update_skill_point_and_ult_energy(skill_points=0, slash_dream=1)

            total_dmg.append(rainblade_dmg)

            # remove Crimson Knot from enemy
            add_skill_multiplier, removed_crimson_knot = self._remove_crimson_knot()

            # additional DMG from removing Crimson Knot
            for _ in range(removed_crimson_knot):
                base_skill_multiplier = 0.15
                final_skill_multiplier = base_skill_multiplier + add_skill_multiplier
                additional_dmg, break_amount = self._calculate_damage(skill_multiplier=final_skill_multiplier,
                                                                      break_amount=0,
                                                                      dmg_multipliers=[self.a4_dmg_multiplier,
                                                                                       self.a6_dmg_multiplier],
                                                                      res_multipliers=res_pen)

                total_dmg.append(additional_dmg)

        # Stygian Resurge
        stygian_dmg, break_amount = self._calculate_damage(skill_multiplier=1.2, break_amount=5,
                                                           res_multipliers=res_pen,
                                                           dmg_multipliers=[self.a4_dmg_multiplier,
                                                                            self.a6_dmg_multiplier])
        self.enemy_toughness -= break_amount

        if self.is_enemy_weakness_broken():
            self.do_break_dmg(break_type='Lightning')
            self._update_skill_point_and_ult_energy(skill_points=0, slash_dream=1)

        total_dmg.append(stygian_dmg)

        # remove Crimson Knot from enemy
        self._remove_crimson_knot(remove_amount=self.crimson_knot)

        # A6 Trace
        for _ in range(6):
            additional_dmg, break_amount = self._calculate_damage(skill_multiplier=0.25, break_amount=0,
                                                                  dmg_multipliers=[self.a4_dmg_multiplier,
                                                                                   self.a6_dmg_multiplier],
                                                                  res_multipliers=res_pen)
            total_dmg.append(additional_dmg)

        # Find max DMG
        self.crit_rate = 1
        max_dmg, break_amount = self._calculate_damage(skill_multiplier=3.72, break_amount=0, res_multipliers=res_pen,
                                                       dmg_multipliers=[self.a4_dmg_multiplier, self.a6_dmg_multiplier])
        self.crit_rate = 0.5

        final_total_dmg = float(sum(total_dmg))
        final_dmg = min(final_total_dmg, max_dmg)

        self.data['DMG'].append(final_dmg)
        self.data['DMG_Type'].append('Ultimate')

    def _remove_crimson_knot(self, remove_amount: int = 3) -> tuple[float, int]:
        """
        Remove Crimson Knot.
        :param remove_amount: Amount to remove Crimson Knot.
        :return: Additional Skill Multiplier and number of removed Crimson Knot
        """
        main_logger.info("Removing crimson knot from enemy...")
        removed = min(remove_amount, self.crimson_knot)
        self.crimson_knot -= removed
        add_skill_multiplier = min(0.6, 0.2 * removed)
        return add_skill_multiplier, removed

    def _can_use_ult(self) -> bool:
        return self.slash_dream >= 9

    def _update_skill_point_and_ult_energy(self, skill_points: int, slash_dream: int) -> None:
        """
        Update skill points and ultimate energy.
        :param skill_points: Skill points.
        :param slash_dream: Slash Dream stack.
        :return: None
        """
        main_logger.info('Updating skill points and Slash Dream stacks...')
        self.skill_points += skill_points
        self.slash_dream += slash_dream
        # ensure that the Slash Dream not exceed 12 stacks
        self.slash_dream = min(12, self.slash_dream)

    def random_nihility_teammate(self) -> None:
        """
        Random Nihility teammate
        :return: None
        """
        main_logger.info('Random Nihility teammate...')
        self.nihility_teammate_num = random.choice([1, 2])
        if self.nihility_teammate_num == 1:
            self.a4_dmg_multiplier = 0.15
        elif self.nihility_teammate_num == 2:
            self.a4_dmg_multiplier = 0.6

    def reset_character_data(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f'Resetting {self.__class__.__name__} data...')
        super().reset_character_data()
        self.slash_dream = 0
        self.crimson_knot = 0
        self.a4_dmg_multiplier = 0
        self.a6_dmg_multiplier = 0
        self.a6_buff = 0
        self.nihility_teammate_num = 0