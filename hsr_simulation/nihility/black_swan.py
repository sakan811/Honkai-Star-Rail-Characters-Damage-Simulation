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


class BlackSwan(Character):
    def __init__(
            self,
            speed: float = 102,
            ult_energy: int = 120
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.arcana = 0
        self.epiphany = 0
        self.enemy_def_reduced = 0
        self.a6_dmg_multiplier = min(0.72, 0.6 * self.break_effect)

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f'Resetting {self.__class__.__name__} data...')
        super().reset_character_data_for_each_battle()
        self.arcana = 0
        self.epiphany = 0
        self.enemy_def_reduced = 0
        self.a6_dmg_multiplier = min(0.72, 0.6 * self.break_effect)

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # simulate enemy turn
        self._simulate_enemy_weakness_broken()

        # simulate A4 Trace
        if self.battle_start:
            main_logger.debug('Battle starts')
            self.battle_start = False
            self._apply_arcana()

        self._enemy_turn()

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

            self.current_ult_energy = 5

        # simulate A4 Trace br randomizing ally's DoT attack
        main_logger.debug('Randomizing ally DoT attack...')
        if random.random() < 0.5:
            self._apply_arcana()

    def _apply_arcana(self) -> None:
        """
        Apply Arcana stack with base inflicting chance.
        :return:
        """
        main_logger.info('Apply Arcana stack...')
        base_chance = 0.65 * (1 + self.effect_hit_rate)
        if random.random() < base_chance:
            self.arcana += 1

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        main_logger.info("Using basic attack...")
        if self.enemy_def_reduced > 0:
            dmg = self._calculate_damage(skill_multiplier=0.6, break_amount=10,
                                         dmg_multipliers=[0.208, self.a6_dmg_multiplier])
        else:
            dmg = self._calculate_damage(skill_multiplier=0.6, break_amount=10,
                                         dmg_multipliers=[self.a6_dmg_multiplier])

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self._record_damage(dmg, 'Basic ATK')

        # generate Arcana stack
        self._apply_arcana()
        if self.epiphany > 0:
            self._apply_arcana()

        # simulate A2 Trace
        if self.epiphany > 0:
            self._apply_arcana()

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info("Using skill...")
        if self.enemy_def_reduced > 0:
            dmg = self._calculate_damage(skill_multiplier=0.9, break_amount=20,
                                         dmg_multipliers=[0.208, self.a6_dmg_multiplier])
        else:
            dmg = self._calculate_damage(skill_multiplier=0.9, break_amount=20,
                                         dmg_multipliers=[self.a6_dmg_multiplier])

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self._record_damage(dmg, 'Skill')

        # generate Arcana
        self.arcana += 1

        # reduce enemy's DEF
        self.enemy_def_reduced = 3

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info('Using ultimate...')
        if self.enemy_def_reduced > 0:
            dmg = self._calculate_damage(skill_multiplier=1.2, break_amount=30,
                                         dmg_multipliers=[0.208, self.a6_dmg_multiplier])
        else:
            dmg = self._calculate_damage(skill_multiplier=1.2, break_amount=30,
                                         dmg_multipliers=[self.a6_dmg_multiplier])

        self._record_damage(dmg, 'Ultimate')

        self.epiphany = 2

    def _enemy_turn(self) -> None:
        """
        Simulate enemy turn
        :return: None
        """
        main_logger.info('Simulating enemy turn...')
        main_logger.debug(f'Arcana stack on enemy: {self.arcana}')
        main_logger.debug(f'Epiphany stack on enemy: {self.epiphany}')
        self._apply_talent_dmg()

        if self.epiphany > 0:
            self.epiphany -= 1

    def _apply_talent_dmg(self) -> None:
        """
        Simulate talent damage.
        :return: None
        """
        main_logger.info('Simulating talent damage...')
        epiphany_multiplier = 0
        if self.epiphany > 0:
            epiphany_multiplier = 0.25
            # generate Arcana stack
            self._apply_arcana()

        if self.arcana > 0:
            if self.arcana >= 7:
                dmg_multiplier = [epiphany_multiplier, self.a6_dmg_multiplier]
                dot_multiplier = 0.12 * self.arcana
                dmg = self._calculate_damage(skill_multiplier=2.4, break_amount=0, dot_dmg_multipliers=[dot_multiplier],
                                             dmg_multipliers=dmg_multiplier, def_reduction_multiplier=[0.2],
                                             can_crit=False)
            else:
                dmg_multiplier = [0.12 * self.arcana, epiphany_multiplier, self.a6_dmg_multiplier]
                dot_multiplier = 0.12 * self.arcana
                dmg = self._calculate_damage(skill_multiplier=2.4, break_amount=0, dot_dmg_multipliers=[dot_multiplier],
                                             dmg_multipliers=dmg_multiplier,
                                             can_crit=False)

            self._record_damage(dmg, 'DoT')

            if self.epiphany <= 0:
                main_logger.debug('Epiphany stack is zero or less. Reset Arcana stack to 1.')
                self.arcana = 1
