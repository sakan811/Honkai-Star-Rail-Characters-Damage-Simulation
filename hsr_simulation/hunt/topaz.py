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

from configure_logging import configure_logging_with_file
from hsr_simulation.character import Character
from hsr_simulation.simulate_turns import calculate_action_value

logger = configure_logging_with_file('simulate_turns.log')


class Topaz(Character):
    def __init__(
            self,
            atk: int = 2000,
            crit_rate: float = 0.5,
            crit_dmg: float = 1.0,
            speed: float = 110,
            ult_energy: int = 130
    ):
        super().__init__(atk, crit_rate, crit_dmg, speed, ult_energy)
        self.windfall_bonanza = 0
        self.numby_action_forward = False
        self.numby_spd = 80

    def take_action(self) -> float:
        """
        Simulate taking actions.
        :return: Total damage.
        """
        logger.info('Taking actions...')
        total_dmg = []

        # reset stats
        self.numby_spd = 80

        if self.skill_points > 0:
            dmg, break_amount = self._use_skill()

            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Skill')
        else:
            dmg, break_amount = self._use_basic_atk()

            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Basic ATK')

        total_dmg.append(dmg)

        if self._can_use_ult():
            ult_dmg, ult_break_amount = self._use_ult()

            ult_dmg = self.enemy_has_fire_weakness()

            total_dmg.append(ult_dmg)
            self.enemy_toughness -= ult_break_amount
            self.current_ult_energy = 5

        return sum(total_dmg)

    def _use_basic_atk(self) -> tuple[float, int]:
        """
        Simulate basic atk damage.
        :return: Damage and break amount.
        """
        logger.info("Using basic attack...")
        if self.enemy_has_fire_weakness():
            dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10, dmg_multipliers=[0.15])
        else:
            dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10)
        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.enemy_toughness -= break_amount

        # Numby action forward
        self.numby_spd *= 1.5

        return dmg, break_amount

    def _use_skill(self) -> tuple[float, int]:
        """
        Simulate skill damage.
        :return: Damage and break amount.
        """
        logger.info("Using skill...")
        if self.enemy_has_fire_weakness():
            dmg, break_amount = self._calculate_damage(skill_multiplier=1.5, break_amount=20,
                                                       dmg_multipliers=[0.5, 0.15])
        else:
            dmg, break_amount = self._calculate_damage(skill_multiplier=1.5, break_amount=20, dmg_multipliers=[0.5])
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.enemy_toughness -= break_amount

        # Numby action forward
        self.numby_spd *= 1.5

        return dmg, break_amount

    def _use_ult(self) -> tuple[float, int]:
        """
        Simulate ultimate damage.
        :return: Damage and break amount.
        """
        logger.info('Using ultimate...')
        self.windfall_bonanza = 2
        return 0, 0

    def enemy_has_fire_weakness(self) -> bool:
        logger.info('Whether the enemy has fire weakness...')
        if random.random() < 0.5:
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
        self.in_windfall_bonanza = False
        self.windfall_bonanza_attacks = 0

    def take_action(self) -> float:
        logger.info("Numby is taking action...")

        # reset stats
        self.crit_dmg = self.topaz.crit_dmg

        if self.windfall_bonanza > 0:
            self.in_windfall_bonanza = True
            self.crit_dmg += 0.25

            if self.enemy_has_fire_weakness():
                dmg, break_amount = self._calculate_damage(skill_multiplier=3, break_amount=20,
                                                           dmg_multipliers=[0.15])

                self.data['DMG'].append(dmg)
                self.data['DMG_Type'].append('Numby with Ult Buff')
            else:
                dmg, break_amount = self._calculate_damage(skill_multiplier=3, break_amount=20)

                self.data['DMG'].append(dmg)
                self.data['DMG_Type'].append('Numby')

            self.windfall_bonanza -= 1
            self.current_ult_energy += 15
        else:
            self.in_windfall_bonanza = False

            if self.enemy_has_fire_weakness():
                dmg, break_amount = self._calculate_damage(skill_multiplier=1.5, break_amount=20,
                                                           dmg_multipliers=[0.15])
            else:
                dmg, break_amount = self._calculate_damage(skill_multiplier=1.5, break_amount=20)

            self.current_ult_energy += 5

        self.enemy_toughness -= break_amount

        if self.in_windfall_bonanza:
            # random number of allies to attack
            follow_up_atk_ally_num = random.choice([1, 2])
            # Numby action forward
            self.topaz.numby_spd *= 1.5 * (1 + follow_up_atk_ally_num)

            self.simulate_break_amount_from_ally(follow_up_atk_ally_num, is_in_windfall_bonanza=True)
        else:
            if self._random_ally_follow_up_atk():
                # Numby action forward
                self.topaz.numby_spd *= 1.5

                self.simulate_break_amount_from_ally(follow_up_atk_ally_num=1)

        return dmg

    def simulate_break_amount_from_ally(self, follow_up_atk_ally_num: int, is_in_windfall_bonanza: bool = False):
        logger.info("Simulating break amount from all allies...")
        if is_in_windfall_bonanza:
            break_amount = random.choice([10, 20, 30])
            break_amount_from_allies = break_amount * follow_up_atk_ally_num
            self.enemy_toughness -= break_amount_from_allies
        else:
            break_amount = random.choice([10, 20, 30])
            self.enemy_toughness -= break_amount

    def _random_ally_follow_up_atk(self) -> bool:
        """
        Simulate random follow-up atk from ally.
        :return: Whether an ally does follow-up attack
        """
        logger.info('Random ally follow-up atk...')
        # random number of allies that can do follow up attack
        follow_up_atk_ally_num = random.choice([0, 1])

        if random.random() < (0.33 * follow_up_atk_ally_num):
            logger.debug('Ally does follow-up atk')
            return True
        else:
            return False


def simulate_turns_for_topaz(topaz: Topaz, numby: Numby, max_cycles: int) -> float:
    """
    Simulate turns for Topaz and Numby.
    :param topaz: Topaz character
    :param numby: Numby character
    :param max_cycles: Cycles to simulate.
    :return: Total damage done within the given cycles.
    """
    logger.info(f'Simulating turns for Topaz and Numby...')

    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    logger.debug(f'Total cycles action value: {cycles_action_val}')

    cycles_action_value_for_topaz = cycles_action_val
    cycles_action_value_for_numby = cycles_action_val

    total_dmg_list = []

    topaz_end = False
    numby_end = False

    topaz_turn_count = 0
    numby_turn_count = 0

    while True:
        if topaz_end and numby_end:
            break
        else:
            if not topaz_end:
                topaz_spd = topaz.speed
                logger.debug(f'Topaz speed: {topaz_spd}')
                topaz_action_val = calculate_action_value(topaz_spd)
                logger.debug(f'Topaz action value: {topaz_action_val}')

                total_topaz_action_dmg = topaz.take_action()
                cycles_action_value_for_topaz -= topaz_action_val

                total_dmg_list.append(total_topaz_action_dmg)
                topaz_turn_count += 1

            if not numby_end:
                numby_spd = topaz.numby_spd
                logger.debug(f'Numby speed: {numby_spd}')
                numby_action_val = calculate_action_value(numby_spd)
                logger.debug(f'Numby action value: {numby_action_val}')

                total_numby_action_dmg = numby.take_action()
                cycles_action_value_for_numby -= numby_action_val

                total_dmg_list.append(total_numby_action_dmg)
                numby_turn_count += 1

            # calculate whether Topaz has turns left
            if cycles_action_value_for_topaz < topaz_action_val:
                topaz_end = True

            # calculate whether Numby has turns left
            if cycles_action_value_for_numby < numby_action_val:
                numby_end = True

    total_dmg = sum(total_dmg_list)
    logger.debug(f'Total damage: {total_dmg}')
    logger.debug(f'Total turns: {len(total_dmg_list)}')
    logger.debug(f'Total number of Topaz turns: {topaz_turn_count}')
    logger.debug(f'Total number of Numby turns: {numby_turn_count}')

    return total_dmg


if __name__ == '__main__':
    pass
