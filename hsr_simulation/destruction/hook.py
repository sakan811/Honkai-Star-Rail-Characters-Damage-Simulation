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


class Hook(Character):
    def __init__(
            self,
            speed: float = 94,
            ult_energy: int = 120
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.burn: int = 0
        self.can_use_enhanced_skill: bool = False

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
        self.burn: int = 0
        self.can_use_enhanced_skill: bool = False

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # simulate enemy turn
        self._simulate_enemy_weakness_broken()
        if self.burn > 0:
            self._apply_burn_dmg()
            self.burn -= 1

        # reset stats for each action
        self.char_action_value_for_action_forward = []

        if self.skill_points > 0 and not self.can_use_enhanced_skill:
            self._use_skill()
        elif self.skill_points > 0 and self.can_use_enhanced_skill:
            self._use_enhanced_skill()
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

        if self.burn > 0:
            self._apply_talent_dmg()

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        dmg = self._calculate_damage(skill_multiplier=2.4, break_amount=20)

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

        if self.burn > 0:
            self._apply_talent_dmg()

        self.burn = 2

    def _use_enhanced_skill(self) -> None:
        """
        Simulate enhanced skill damage.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using enhanced skill...")
        dmg = self._calculate_damage(skill_multiplier=2.8, break_amount=20)

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Enhanced Skill')

        if self.burn > 0:
            self._apply_talent_dmg()

        self.burn = 2

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is using ultimate...')
        dmg = self._calculate_damage(skill_multiplier=4, break_amount=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

        if self.burn > 0:
            self._apply_talent_dmg()

        self.can_use_enhanced_skill = True

        # simulate A6 trace
        self.current_ult_energy += 5
        action_value_from_action_fwd: float = self.simulate_action_forward(action_forward_percent=0.2)
        self.char_action_value_for_action_forward.append(action_value_from_action_fwd)

    def _apply_burn_dmg(self) -> None:
        """
        Apply burn damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is applying burn damage...')
        dmg = self._calculate_damage(skill_multiplier=0.65, break_amount=0, can_crit=False)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('DoT')

    def _apply_talent_dmg(self) -> None:
        """
        Apply talent damage.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is applying talent damage...')
        dmg = self._calculate_damage(skill_multiplier=1, break_amount=0)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Talent')

        self.current_ult_energy += 5
