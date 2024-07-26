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

from configure_logging import configure_logging_with_file
from hsr_simulation.character import Character
from hsr_simulation.hunt.boothill import Boothill

logger = configure_logging_with_file('simulate_turns.log')


def calculate_action_value(speed: float) -> float:
    """
    Calculate action value
    :param speed: Character speed
    :return: Action value
    """
    logger.info(f'Calculating action value...')
    return 10000 / speed


def simulate_turns(character: Character, max_cycles: int) -> float:
    """
    Simulate turns
    :param character: Character to simulate.
    :param max_cycles: Cycles to simulate.
    :return: Total damage done within the given cycles.
    """
    logger.info(f'Simulating turns...')

    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    logger.debug(f'Total cycles action value: {cycles_action_val}')

    total_dmg_list = []

    if isinstance(character, Boothill):
        character.set_break_effect(1, 3)

    character.random_enemy_toughness()

    while cycles_action_val > 0:
        char_spd = character.speed
        logger.debug(f'Character speed: {char_spd}')

        char_action_val = calculate_action_value(char_spd)
        logger.debug(f'Character action value: {char_action_val}')

        if cycles_action_val < char_action_val:
            break
        else:
            total_action_dmg = character.take_action()

            total_dmg_list.append(total_action_dmg)

            cycles_action_val -= char_action_val

    total_dmg = sum(total_dmg_list)
    logger.debug(f'Total damage: {total_dmg}')
    logger.debug(f'Total turns: {len(total_dmg_list)}')

    return total_dmg


if __name__ == '__main__':
    pass

