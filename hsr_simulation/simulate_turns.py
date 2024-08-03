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
from typing import Any

from hsr_simulation.character import Character
from hsr_simulation.configure_logging import configure_logging_with_file, main_logger
from hsr_simulation.hunt.boothill import Boothill
from hsr_simulation.hunt.march7th_hunt import March7thHunt
from hsr_simulation.nihility.acheron import Acheron
from hsr_simulation.nihility.black_swan import BlackSwan

script_logger = configure_logging_with_file(log_dir='logs', log_file='simulate_turns.log',
                                            logger_name='simulate_turns', level='DEBUG')


def simulate_cycles(character: Character, max_cycles: int, simulate_round: int) -> dict[str, list[Any]]:
    """
    Simulate cycles
    :param character: Character to simulate.
    :param max_cycles: Cycles to simulate.
    :param simulate_round: Indicate the current round of the simulation.
    :return: Dictionary that contains action details of the character.
    """
    main_logger.info(f'Simulating turns for {character.__class__.__name__}...')

    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    script_logger.debug(f'Total cycles action value: {cycles_action_val}')

    # re-initialize the character to reset their stats
    character.__init__()

    set_stats_for_some_char(character)

    # random enemy toughness
    character.random_enemy_toughness()

    # Indicate that the battle starts
    character.start_battle()

    char_turn_count = simulate_turns(character, cycles_action_val)

    script_logger.debug(f'Total number of {character.__class__.__name__} turns: {char_turn_count}')

    row_num = len(character.data['DMG'])
    character.data['Simulate Round No.'] = [simulate_round for _ in range(row_num)]
    data_dict: dict[str, list] = character.data
    character.clear_data()

    return data_dict


def set_stats_for_some_char(character: Character) -> None:
    """
    Set stats for some character
    :param character: Character to set stats for.
    :return: None
    """
    if isinstance(character, Boothill):
        character.set_break_effect(1, 3)
    elif isinstance(character, BlackSwan):
        character.set_effect_hit_rate(1, 2)
    elif isinstance(character, Acheron):
        character.random_nihility_teammate()
    elif isinstance(character, March7thHunt):
        character.set_shifu()


def simulate_turns(character: Character, cycles_action_val: float) -> int:
    """
    Simulate the character's turns
    :param character: Character to simulate.
    :param cycles_action_val: Cycles action value.
    :return: Character's turns.
    """
    main_logger.info(f'Simulate turns for {character.__class__.__name__}...')

    char_turn_count = 0
    while cycles_action_val > 0:
        char_spd = character.speed
        script_logger.debug(f'{character.__class__.__name__} current speed: {char_spd}')

        char_action_val = character.calculate_action_value(char_spd)
        script_logger.debug(f'{character.__class__.__name__} current action value: {char_action_val}')

        if cycles_action_val < char_action_val:
            break
        else:
            character.take_action()

            cycles_action_val -= char_action_val
            char_turn_count += 1

            # simulate Action Forward
            script_logger.debug(f'{character.__class__.__name__} current speed: {character.speed}')
            char_action_val_to_be_added = sum(character.char_action_value)
            script_logger.debug(f'{character.__class__.__name__} action value to be added: {char_action_val_to_be_added}')
            cycles_action_val += char_action_val_to_be_added

    return char_turn_count


if __name__ == '__main__':
    pass
