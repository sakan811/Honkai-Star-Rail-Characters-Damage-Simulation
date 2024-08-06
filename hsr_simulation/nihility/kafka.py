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

from hsr_simulation.character import Character
from hsr_simulation.configure_logging import main_logger


class Kafka(Character):
    def __init__(
            self,
            atk: int = 2000,
            crit_rate: float = 0.5,
            crit_dmg: float = 1.0,
            speed: float = 100,
            ult_energy: int = 120
    ):
        super().__init__(atk, crit_rate, crit_dmg, speed, ult_energy)
        self.shock = 0
        self.talent_cooldown = False

    def reset_character_data(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f'Resetting {self.__class__.__name__} data...')
        super().reset_character_data()
        self.shock = 0
        self.talent_cooldown = False

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        self._calculate_shock_dmg_on_enemy()

        # simulate Talent
        if not self.talent_cooldown:
            self._use_talent()
        else:
            self.talent_cooldown = False

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
        :return: None.
        """
        main_logger.info("Using basic attack...")
        dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10)
        self.enemy_toughness -= break_amount

        if self.is_enemy_weakness_broken():
            self.do_break_dmg(break_type='Lightning')

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None.
        """
        main_logger.info("Using skill...")
        dmg, break_amount = self._calculate_damage(skill_multiplier=1.6, break_amount=20)
        self.enemy_toughness -= break_amount

        if self.is_enemy_weakness_broken():
            self.do_break_dmg(break_type='Lightning')

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        if self.shock > 0:
            self._use_shock(skill_trigger=True)

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info('Using ultimate...')
        dmg, break_amount = self._calculate_damage(skill_multiplier=0.8, break_amount=20)
        self.enemy_toughness -= break_amount

        if self.is_enemy_weakness_broken():
            self.do_break_dmg(break_type='Lightning')

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

        self.shock = 2

        self._use_shock()

    def _use_talent(self) -> None:
        """
        Simulate Talent damage.
        :return: None
        """
        main_logger.info('Using talent...')
        dmg, break_amount = self._calculate_damage(skill_multiplier=1.4, break_amount=10)
        self.enemy_toughness -= break_amount

        if self.is_enemy_weakness_broken():
            self.do_break_dmg(break_type='Lightning')

        self.shock = 2
        self.talent_cooldown = True

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Talent')

    def _use_shock(self, skill_trigger: bool = False) -> float:
        """
        Simulate Shock damage.
        :param skill_trigger: Whether the DoT is triggered by Kafka's Skill
        :return: Damage
        """
        main_logger.info('Using Shock DoT...')
        if skill_trigger:
            dmg, break_amount = self._calculate_damage(skill_multiplier=2.9, break_amount=0, can_crit=False)
            dmg *= 0.75
        else:
            dmg, break_amount = self._calculate_damage(skill_multiplier=2.9, break_amount=0, can_crit=False)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('DoT')

        return dmg

    def _calculate_shock_dmg_on_enemy(self) -> None:
        """
        Calculate shock dmg on enemy's turn.
        :return: None.
        """
        main_logger.info('Calculating shock dmg on enemy turn...')
        if self.shock > 0:
            self.shock -= 1
            self._use_shock()


