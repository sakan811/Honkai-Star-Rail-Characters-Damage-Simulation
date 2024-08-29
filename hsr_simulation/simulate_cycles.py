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

import numpy as np

from hsr_simulation.character import Character
from hsr_simulation.configure_logging import main_logger
from hsr_simulation.destruction.firefly import FireFly
from hsr_simulation.destruction.xueyi import Xueyi
from hsr_simulation.hunt.boothill import Boothill
from hsr_simulation.hunt.march7th_hunt import March7thHunt
from hsr_simulation.hunt.topaz import Topaz
from hsr_simulation.nihility.acheron import Acheron
from hsr_simulation.nihility.black_swan import BlackSwan
from hsr_simulation.nihility.jiaoqiu import Jiaoqiu
from hsr_simulation.nihility.luka import Luka
from hsr_simulation.simulate_turns import simulate_turns, simulate_turns_for_char_with_summon


def set_stats_for_some_char(character: Character) -> None:
    """
    Set stats for some character.
    :param character: Character to set stats for.
    :return: None.
    """
    if isinstance(character, Boothill):
        character.set_break_effect(1, 3)
    elif isinstance(character, BlackSwan):
        character.set_effect_hit_rate(0, 1.2)
    elif isinstance(character, Acheron):
        character.random_nihility_teammate()
    elif isinstance(character, March7thHunt):
        character.set_shifu()
    elif isinstance(character, Luka):
        character.random_enemy_hp()
    elif isinstance(character, Jiaoqiu):
        character.set_effect_hit_rate(0, 1.4)
    elif isinstance(character, FireFly):
        character.set_break_effect(1, 3.6)
    elif isinstance(character, Xueyi):
        character.set_break_effect(1, 2.4)


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
    main_logger.debug(f'Total cycles action value: {cycles_action_val}')

    set_stats_for_some_char(character)

    # Indicate that the battle starts
    character.start_battle()

    # simulate turns for character within the given cycles
    char_turn_count = simulate_turns(character, cycles_action_val)

    main_logger.debug(f'Total number of {character.__class__.__name__} turns: {char_turn_count}')

    row_num = len(character.data['DMG'])
    character.data['Simulate Round No.'] = [simulate_round for _ in range(row_num)]
    data_dict: dict[str, list] = character.data

    # reset the character data
    character.reset_character_data_for_each_battle()

    return data_dict


def simulate_cycles_for_character_with_summon(
        character: Character,
        summon: Character,
        max_cycles: int,
        simulate_round: int) -> dict[str, list[Any]]:
    """
    Simulate cycles for Character and their summon.
    :param character: Character
    :param summon: Summon of the given character
    :param max_cycles: Cycles to simulate.
    :param simulate_round: Indicate the current round of the simulation.
    :return: Dictionary that contains action details of Topaz.
    """
    main_logger.info(f'Simulating turns for {character.__class__.__name__} and {summon.__class__.__name__}...')

    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    main_logger.debug(f'Total cycles action value: {cycles_action_val}')

    # re-initialize characters' summon
    if isinstance(character, Topaz):
        summon = character.summon_numby(character)

    # Indicate that the battle starts
    character.start_battle()

    cycles_action_value_for_character = cycles_action_val
    cycles_action_value_for_summon = cycles_action_val

    character_end = False
    summon_end = False

    # simulate character and their summon turns within the given cycles
    summon_turn_count, character_turn_count = simulate_turns_for_char_with_summon(cycles_action_value_for_summon,
                                                                                  cycles_action_value_for_character,
                                                                                  summon,
                                                                                  summon_end,
                                                                                  character, character_end)

    main_logger.debug(f'Total number of {character.__class__.__name__} turns: {character_turn_count}')
    main_logger.debug(f'Total number of {summon.__class__.__name__} turns: {summon_turn_count}')

    # find the number of character turns within the given cycles
    num_turn = len(character.data['DMG'])

    # add Simulate Round No. to data dictionary
    character.data['Simulate Round No.'] = np.full(num_turn, simulate_round)

    # assign character data dictionary to a variable
    data_dict = character.data

    # reset the character and their summon data
    character.reset_character_data_for_each_battle()

    return data_dict
