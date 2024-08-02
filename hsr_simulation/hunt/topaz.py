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
from typing import Any

from hsr_simulation.character import Character
from hsr_simulation.configure_logging import configure_logging_with_file, main_logger
from hsr_simulation.simulate_turns import calculate_action_value

script_logger = configure_logging_with_file(log_dir='logs', log_file='topaz.log',
                                            logger_name='topaz', level='DEBUG')


def enemy_has_fire_weakness() -> bool:
    main_logger.info('Whether the enemy has fire weakness...')
    if random.random() < 0.5:
        return True
    else:
        return False


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
        self.numby_spd = numby_spd
        self.windfall_bonanza = 0
        self.numby_action_forward = False

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # reset stats
        self.numby_spd = 80

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

            enemy_has_fire_weakness()

            self.current_ult_energy = 5

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None.
        """
        script_logger.info("Using basic attack...")
        if enemy_has_fire_weakness():
            dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10, dmg_multipliers=[0.15])
        else:
            dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10)

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.enemy_toughness -= break_amount

        # Numby action forward
        self.numby_spd *= 1.5

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        script_logger.info("Using skill...")
        if enemy_has_fire_weakness():
            dmg, break_amount = self._calculate_damage(skill_multiplier=1.5, break_amount=20,
                                                       dmg_multipliers=[0.5, 0.15])
        else:
            dmg, break_amount = self._calculate_damage(skill_multiplier=1.5, break_amount=20, dmg_multipliers=[0.5])
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.enemy_toughness -= break_amount

        # Numby action forward
        self.numby_spd *= 1.5

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: Damage and break amount.
        """
        script_logger.info('Using ultimate...')
        self.windfall_bonanza = 2


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
            speed=topaz.numby_spd,
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
            if enemy_has_fire_weakness():
                dmg, break_amount = self._calculate_damage(skill_multiplier=3, break_amount=20,
                                                           dmg_multipliers=[0.15])

                self.enemy_toughness -= break_amount

                self.topaz.data['DMG'].append(dmg)
                self.topaz.data['DMG_Type'].append('Numby with Ult Buff')
            else:
                dmg, break_amount = self._calculate_damage(skill_multiplier=3, break_amount=20)

                self.enemy_toughness -= break_amount

                self.topaz.data['DMG'].append(dmg)
                self.topaz.data['DMG_Type'].append('Numby with Ult Buff')
        else:
            script_logger.info('Numby attacking...')
            if enemy_has_fire_weakness():
                dmg, break_amount = self._calculate_damage(skill_multiplier=1.5, break_amount=20,
                                                           dmg_multipliers=[0.15])

                self.enemy_toughness -= break_amount

                self.topaz.data['DMG'].append(dmg)
                self.topaz.data['DMG_Type'].append('Numby')
            else:
                dmg, break_amount = self._calculate_damage(skill_multiplier=1.5, break_amount=20)

                self.enemy_toughness -= break_amount

                self.topaz.data['DMG'].append(dmg)
                self.topaz.data['DMG_Type'].append('Numby')

    def take_action(self) -> None:
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # reset stats
        self.crit_dmg = self.topaz.crit_dmg
        self.topaz.numby_spd = 80

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
            self.topaz.numby_spd *= 1.5 * (1 + follow_up_atk_ally_num)

            self.simulate_break_amount_from_ally(follow_up_atk_ally_num, is_in_windfall_bonanza=True)
        else:
            if random_ally_follow_up_atk():
                # Numby action forward
                self.topaz.numby_spd *= 1.5

                self.simulate_break_amount_from_ally(follow_up_atk_ally_num=1)

    def simulate_break_amount_from_ally(self, follow_up_atk_ally_num: int, is_in_windfall_bonanza: bool = False):
        script_logger.info("Simulating break amount from all allies...")
        if self.topaz.windfall_bonanza > 0:
            break_amount = random.choice([10, 20, 30])
            break_amount_from_allies = break_amount * follow_up_atk_ally_num
            self.enemy_toughness -= break_amount_from_allies
        else:
            break_amount = random.choice([10, 20, 30])
            self.enemy_toughness -= break_amount


def simulate_turns_for_topaz(topaz: Topaz, numby: Numby, max_cycles: int, simulate_round: int) -> dict[str, list[Any]]:
    """
    Simulate turns for Topaz and Numby.
    :param topaz: Topaz character
    :param numby: Numby character
    :param max_cycles: Cycles to simulate.
    :param simulate_round: Indicate the current round of the simulation.
    :return: Dictionary that contains action details of Topaz.
    """
    main_logger.info(f'Simulating turns for Topaz and Numby...')

    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    script_logger.debug(f'Total cycles action value: {cycles_action_val}')

    cycles_action_value_for_topaz = cycles_action_val
    cycles_action_value_for_numby = cycles_action_val

    topaz_end = False
    numby_end = False

    numby_turn_count, topaz_turn_count = simulate_numby_and_topaz_actions(cycles_action_value_for_numby,
                                                                          cycles_action_value_for_topaz, numby,
                                                                          numby_end,
                                                                          topaz, topaz_end)

    script_logger.debug(f'Total number of Topaz turns: {topaz_turn_count}')
    script_logger.debug(f'Total number of Numby turns: {numby_turn_count}')

    num_turn = len(topaz.data['DMG'])
    topaz.data['Simulate Round No.'] = [simulate_round for _ in range(num_turn)]
    data_dict = topaz.data
    topaz.clear_data()

    return data_dict


def simulate_numby_and_topaz_actions(
        cycles_action_value_for_numby,
        cycles_action_value_for_topaz,
        numby,
        numby_end,
        topaz,
        topaz_end) -> tuple[int, int]:
    """
    Simulate actions for Numby and Topaz.
    :param cycles_action_value_for_numby: Cycles action value of Numby.
    :param cycles_action_value_for_topaz: Cycles action value of Topaz.
    :param numby: Numby character
    :param numby_end: Whether Numby's cycles end
    :param topaz: Topaz character
    :param topaz_end: Whether Topaz's cycles end
    :return: Numby and Topaz turns
    """
    main_logger.info(f'Simulating turns for Numby and Topaz...')

    topaz_turn_count = 0
    numby_turn_count = 0
    while True:
        if topaz_end and numby_end:
            break
        else:
            if not topaz_end:
                topaz_spd = topaz.speed
                script_logger.debug(f'Topaz speed: {topaz_spd}')
                topaz_action_val = calculate_action_value(topaz_spd)
                script_logger.debug(f'Topaz action value: {topaz_action_val}')

                # calculate whether Topaz has turns left
                if cycles_action_value_for_topaz >= topaz_action_val:
                    cycles_action_value_for_topaz -= topaz_action_val
                    topaz.take_action()
                    topaz_turn_count += 1
                else:
                    topaz_end = True

            if not numby_end:
                numby_spd = topaz.numby_spd
                script_logger.debug(f'Numby speed: {numby_spd}')
                numby_action_val = calculate_action_value(numby_spd)
                script_logger.debug(f'Numby action value: {numby_action_val}')

                # calculate whether Numby has turns left
                if cycles_action_value_for_numby >= numby_action_val:
                    cycles_action_value_for_numby -= numby_action_val
                    numby.take_action()
                    numby_turn_count += 1
                else:
                    numby_end = True
    return numby_turn_count, topaz_turn_count


def start_simulations_for_topaz(
        topaz: Topaz,
        numby: Numby,
        max_cycles: int,
        simulation_num: int) -> list[dict[str, list[Any]]]:
    """
    Start simulations for Topaz and Numby.
    :param topaz: Topaz character
    :param numby: Numby character
    :param max_cycles: Max number of cycles to simulate
    :param simulation_num: Number of simulations
    :return: A list of Topaz's action details as a dictionary.
    """
    main_logger.info('Start simulations for Topaz and Numby...')
    result_list = [simulate_turns_for_topaz(topaz, numby, max_cycles, i) for i in range(simulation_num)]
    return result_list


if __name__ == '__main__':
    pass
