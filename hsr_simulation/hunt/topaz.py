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
from hsr_simulation.configure_logging import configure_logging_with_file, main_logger

script_logger = configure_logging_with_file(log_dir='logs', log_file='topaz.log',
                                            logger_name='topaz', level='DEBUG')


class Topaz(Character):
    def __init__(
            self,
            atk: int = 2000,
            crit_rate: float = 0.5,
            crit_dmg: float = 1.0,
            speed: float = 110,
            ult_energy: int = 130,
            numby_spd: int = 80
    ):
        super().__init__(atk, crit_rate, crit_dmg, speed, ult_energy)
        self.summon_speed = numby_spd
        self.windfall_bonanza = 0
        self.numby_action_forward = False

    def enemy_has_fire_weakness(self) -> bool:
        main_logger.info('Whether the enemy has fire weakness...')
        if random.random() < self.chance_of_certain_enemy_weakness:
            return True
        else:
            return False

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # reset stats
        self.summon_speed = 80
        self.summon_action_value_for_action_forward = []

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

            self.enemy_has_fire_weakness()

            self.current_ult_energy = 5

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None.
        """
        script_logger.info("Using basic attack...")
        if self.enemy_has_fire_weakness():
            dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10, dmg_multipliers=[0.15])
        else:
            dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10)

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.enemy_toughness -= break_amount

        if self.is_enemy_weakness_broken():
            self.do_break_dmg(break_type='Fire')

        # Numby action forward
        self.summon_action_value_for_action_forward.append(
            self.simulate_action_forward(action_forward_percent=0.5, speed=self.summon_speed)
        )

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        script_logger.info("Using skill...")
        if self.enemy_has_fire_weakness():
            dmg, break_amount = self._calculate_damage(skill_multiplier=1.5, break_amount=20,
                                                       dmg_multipliers=[0.5, 0.15])
        else:
            dmg, break_amount = self._calculate_damage(skill_multiplier=1.5, break_amount=20, dmg_multipliers=[0.5])
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.enemy_toughness -= break_amount

        if self.is_enemy_weakness_broken():
            self.do_break_dmg(break_type='Fire')

        # Numby action forward
        self.summon_action_value_for_action_forward.append(
            self.simulate_action_forward(action_forward_percent=0.5, speed=self.summon_speed)
        )

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: Damage and break amount.
        """
        script_logger.info('Using ultimate...')
        self.windfall_bonanza = 2

    def simulate_action_forward(self, action_forward_percent: float, speed: float) -> float:
        """
        Simulate action forward.
        :param action_forward_percent: Action forward percent.
        :param speed: Character speed.
        :return: Action value
        """
        script_logger.info(f'Simulate action forward {action_forward_percent * 100}%...')
        script_logger.debug(f'{self.__class__.__name__} current speed: {speed}')
        action_value = self.calculate_action_value(speed)
        script_logger.debug(f'{self.__class__.__name__}: Current Action value {action_value}')
        return action_value * action_forward_percent


def random_ally_follow_up_atk() -> bool:
    """
    Simulate random follow-up atk from ally.
    :return: Whether an ally does follow-up attack
    """
    main_logger.info('Random ally follow-up atk...')
    # random number of allies that can do follow up attack
    follow_up_atk_ally_num = random.choice([0, 1])

    if random.random() < (0.33 * follow_up_atk_ally_num):
        script_logger.debug('Ally does follow-up atk')
        return True
    else:
        return False


class Numby(Topaz):
    def __init__(self, topaz: Topaz):
        super().__init__(
            atk=topaz.atk,
            crit_rate=topaz.crit_rate,
            crit_dmg=topaz.crit_dmg,
            speed=topaz.summon_speed,
            ult_energy=0
        )
        self.topaz = topaz
        self.windfall_bonanza_attacks = 0

    def _numby_attack(self, with_ult_buff: bool = False) -> None:
        """
        Simulate Numby's attack
        :param with_ult_buff: Whether Numby has Ult buff.
        :return: None
        """
        if with_ult_buff:
            script_logger.info('Numby attacking with Ult buff...')
            if self.enemy_has_fire_weakness():
                dmg, break_amount = self._calculate_damage(skill_multiplier=3, break_amount=20,
                                                           dmg_multipliers=[0.15])

                self.topaz.enemy_toughness -= break_amount

                if self.is_enemy_weakness_broken():
                    self.topaz.do_break_dmg(break_type='Fire')

                self.topaz.data['DMG'].append(dmg)
                self.topaz.data['DMG_Type'].append('Numby with Ult Buff')
            else:
                dmg, break_amount = self._calculate_damage(skill_multiplier=3, break_amount=20)

                self.topaz.enemy_toughness -= break_amount

                if self.is_enemy_weakness_broken():
                    self.topaz.do_break_dmg(break_type='Fire')

                self.topaz.data['DMG'].append(dmg)
                self.topaz.data['DMG_Type'].append('Numby with Ult Buff')
        else:
            script_logger.info('Numby attacking...')
            if self.enemy_has_fire_weakness():
                dmg, break_amount = self._calculate_damage(skill_multiplier=1.5, break_amount=20,
                                                           dmg_multipliers=[0.15])

                self.topaz.enemy_toughness -= break_amount

                if self.is_enemy_weakness_broken():
                    self.topaz.do_break_dmg(break_type='Fire')

                self.topaz.data['DMG'].append(dmg)
                self.topaz.data['DMG_Type'].append('Numby')
            else:
                dmg, break_amount = self._calculate_damage(skill_multiplier=1.5, break_amount=20)

                self.topaz.enemy_toughness -= break_amount

                if self.is_enemy_weakness_broken():
                    self.topaz.do_break_dmg(break_type='Fire')

                self.topaz.data['DMG'].append(dmg)
                self.topaz.data['DMG_Type'].append('Numby')

    def take_action(self) -> None:
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # reset stats
        self.crit_dmg = self.topaz.crit_dmg
        self.topaz.summon_speed = 80

        if self.topaz.windfall_bonanza > 0:
            self.crit_dmg += 0.25

            self._numby_attack(with_ult_buff=True)

            self.topaz.windfall_bonanza -= 1
            self.current_ult_energy += 15
        else:
            self._numby_attack()

            self.current_ult_energy += 5

        # Simulate ally's follow-up attacks
        if self.topaz.windfall_bonanza > 0:
            # random number of allies to attack
            follow_up_atk_ally_num = random.choice([1, 2])

            # Numby action forward
            self.topaz.summon_action_value_for_action_forward.append(
                self.topaz.simulate_action_forward(action_forward_percent=0.5 * follow_up_atk_ally_num,
                                                   speed=self.topaz.summon_speed)
            )
        else:
            if random_ally_follow_up_atk():
                # Numby action forward
                self.topaz.summon_action_value_for_action_forward.append(
                    self.topaz.simulate_action_forward(action_forward_percent=0.5, speed=self.topaz.summon_speed)
                )


if __name__ == '__main__':
    pass
