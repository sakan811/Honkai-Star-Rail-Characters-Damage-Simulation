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
from hsr_simulation.dmg_calculator import calculate_break_damage


class Boothill(Character):
    def __init__(
            self,
            speed: float = 107,
            ult_energy: int = 115
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.pocket_trickshot = 0
        self.standoff_turns = 0
        self.win_battle = False
        self.is_in_standoff = False

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f'Resetting {self.__class__.__name__} data...')
        super().reset_character_data_for_each_battle()
        self.pocket_trickshot = 0
        self.standoff_turns = 0
        self.win_battle = False
        self.is_in_standoff = False

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # simulate enemy turn
        self._simulate_enemy_weakness_broken()

        # reset stats for each action
        self.crit_rate = 0.5
        self.crit_dmg = 1

        # A2 Major Trace: Ghost Load
        crit_rate_boost = min(0.3, 0.1 * self.break_effect)
        crit_dmg_boost = min(1.5, 0.5 * self.break_effect)
        self.crit_rate += crit_rate_boost
        self.crit_dmg += crit_dmg_boost

        if self.skill_points > 0 and not self.is_in_standoff:
            self._use_skill()
            self._use_enhanced_basic_atk()
        elif self.is_in_standoff:
            self._use_enhanced_basic_atk()
            if self.enemy_weakness_broken:
                self.win_battle = True
                self._sim_talent_dmg()
        elif self.skill_points <= 0 and not self.is_in_standoff:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()
            self.current_ult_energy = 5

        if self.standoff_turns > 0:
            self.standoff_turns -= 1

            # Boothill did not win battle during Stand Off
            if self.standoff_turns <= 0 and not self.enemy_weakness_broken:
                self._end_standoff()
                self.win_battle = False

    def check_if_enemy_weakness_broken(self, break_type: str = 'None') -> None:
        """
        Check whether enemy is weakness broken.
        :param break_type: Break DMG type, e.g., Physical, Fire, etc.
        :return: None
        """
        if self.current_enemy_toughness <= 0 and not self.enemy_weakness_broken:
            self.enemy_turn_delayed_duration_weakness_broken = 1
            self.enemy_weakness_broken = True
            self._end_standoff()
            main_logger.debug(f'{self.__class__.__name__}: Enemy is Weakness Broken')

    def _use_basic_atk(self) -> None:
        main_logger.info('Using Basic ATK...')
        break_amount = int(10 * self.break_effect)
        dmg = self._calculate_damage(skill_multiplier=1, break_amount=break_amount)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

    def _use_enhanced_basic_atk(self) -> None:
        main_logger.info('Using Enhanced Basic ATK...')
        # Talent: Five Peas in a Pod
        break_amount = 20 * (1 + 0.5 * self.pocket_trickshot) * self.break_effect
        break_amount = int(break_amount)

        if self.is_in_standoff:
            dmg_multiplier = 0.3
        else:
            dmg_multiplier = 0

        dmg = self._calculate_damage(skill_multiplier=2.2, break_amount=break_amount, dmg_multipliers=[dmg_multiplier])

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Enhanced Basic ATK')

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=30)

    def _sim_talent_dmg(self) -> None:
        main_logger.info('Simulating Talent Dmg...')

        # Talent: Five Peas in a Pod
        break_dmg_multiplier = [0.7, 1.2, 1.7][min(self.pocket_trickshot, 2)]
        target_toughness = min(self.enemy_toughness, 16 * 10)
        break_dmg = break_dmg_multiplier * calculate_break_damage(break_type='Physical',
                                                                  target_max_toughness=target_toughness)
        self.data['DMG'].append(break_dmg)
        self.data['DMG_Type'].append('Talent')

    def _use_skill(self) -> None:
        main_logger.info('Using Skill...')
        if not self.win_battle:
            self.pocket_trickshot = 0

        self.standoff_turns = 2
        self.is_in_standoff = True
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=0)

    def _use_ult(self) -> None:
        main_logger.info('Using Ult...')
        break_amount = int(30 * self.break_effect)

        if self.is_in_standoff:
            dmg_multiplier = 0.3
        else:
            dmg_multiplier = 0

        dmg = self._calculate_damage(skill_multiplier=4, break_amount=break_amount, dmg_multipliers=[dmg_multiplier])

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

    def _update_skill_point_and_ult_energy(self, skill_points: int, ult_energy: int) -> None:
        main_logger.info('Updating Skill points and Ult energy...')

        self.skill_points += skill_points
        self.current_ult_energy += ult_energy

        # A6 Major Trace: Point Blank
        if self.standoff_turns > 0 and self.pocket_trickshot < 3:
            self.current_ult_energy += 10

    def _end_standoff(self) -> None:
        main_logger.info('Ending Standoff...')
        self.standoff_turns = 0
        self.is_in_standoff = False
        self.pocket_trickshot = min(self.pocket_trickshot + 1, 3)


if __name__ == '__main__':
    pass
