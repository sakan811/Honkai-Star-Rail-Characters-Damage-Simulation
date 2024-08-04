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
            char_action_val_to_be_added = sum(character.char_action_value_for_action_forward)
            script_logger.debug(f'{character.__class__.__name__} action value to be added: {char_action_val_to_be_added}')

            # ensure that the character action value to be added not exceeds the action value,
            # used to subtract the cycle action value
            char_action_val_to_be_added = min(char_action_val_to_be_added, char_action_val)
            cycles_action_val += char_action_val_to_be_added

    return char_turn_count


def simulate_turns_for_character_with_summon(
        character: Character,
        summon,
        max_cycles: int,
        simulate_round: int) -> dict[str, list[Any]]:
    """
    Simulate turns for Topaz and Numby.
    :param character: Character
    :param summon: Summon of the given character
    :param max_cycles: Cycles to simulate.
    :param simulate_round: Indicate the current round of the simulation.
    :return: Dictionary that contains action details of Topaz.
    """
    main_logger.info(f'Simulating turns for {character.__class__.__name__} and {summon.__class__.__name__}...')

    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    script_logger.debug(f'Total cycles action value: {cycles_action_val}')

    # re-initialize Character and their summon to reset their stats
    character.__init__()
    summon.__init__(character)

    # random enemy toughness
    character.random_enemy_toughness()

    cycles_action_value_for_character = cycles_action_val
    cycles_action_value_for_summon = cycles_action_val

    character_end = False
    summon_end = False

    summon_turn_count, character_turn_count = simulate_actions_for_char_with_summon(cycles_action_value_for_summon,
                                                                                    cycles_action_value_for_character,
                                                                                    summon,
                                                                                    summon_end,
                                                                                    character, character_end)

    script_logger.debug(f'Total number of {character.__class__.__name__} turns: {character_turn_count}')
    script_logger.debug(f'Total number of {summon.__class__.__name__} turns: {summon_turn_count}')

    num_turn = len(character.data['DMG'])
    character.data['Simulate Round No.'] = [simulate_round for _ in range(num_turn)]
    data_dict = character.data
    character.clear_data()

    return data_dict


def simulate_actions_for_char_with_summon(
        cycles_action_value_for_summon,
        cycles_action_value_for_char,
        summon,
        summon_end,
        character,
        character_end) -> tuple[int, int]:
    """
    Simulate actions for Character and their summon.
    :param cycles_action_value_for_summon: Cycles action value of Summon.
    :param cycles_action_value_for_char: Cycles action value of Character.
    :param summon: Summoned character
    :param summon_end: Whether Summon's cycles end
    :param character: Character
    :param character_end: Whether Character's cycles end
    :return: Summon and Character turn count
    """
    main_logger.info(f'Simulating turns for {summon.__class__.__name__} and {character.__class__.__name__}...')

    character_turn_count = 0
    summon_turn_count = 0
    while True:
        if character_end and summon_end:
            break
        else:
            if not character_end:
                character_speed = character.speed
                script_logger.debug(f'{character.__class__.__name__} speed: {character_speed}')
                character_action_value = character.calculate_action_value(character_speed)
                script_logger.debug(f'{character.__class__.__name__} action value: {character_action_value}')

                # calculate whether Character has turns left
                if cycles_action_value_for_char >= character_action_value:
                    character.take_action()

                    cycles_action_value_for_char -= character_action_value
                    character_turn_count += 1

                    # simulate Action Forward
                    script_logger.debug(f'{character.__class__.__name__} current speed: {character.speed}')
                    char_action_val_to_be_added = sum(character.char_action_value_for_action_forward)
                    script_logger.debug(
                        f'{character.__class__.__name__} action value to be added: {char_action_val_to_be_added}')

                    # ensure that the character action value to be added not exceeds the action value,
                    # used to subtract the cycle action value
                    char_action_val_to_be_added = min(char_action_val_to_be_added, character_action_value)
                    cycles_action_value_for_char += char_action_val_to_be_added
                else:
                    character_end = True

            if not summon_end:
                summon_spd = character.summon_speed
                script_logger.debug(f'{summon.__class__.__name__} speed: {summon_spd}')
                summon_action_val = summon.calculate_action_value(summon_spd)
                script_logger.debug(f'{summon.__class__.__name__} action value: {summon_action_val}')

                # calculate whether Summon has turns left
                if cycles_action_value_for_summon >= summon_action_val:
                    summon.take_action()

                    cycles_action_value_for_summon -= summon_action_val
                    summon_turn_count += 1

                    # simulate Action Forward
                    script_logger.debug(f'{summon.__class__.__name__} current speed: {character.summon_speed}')
                    char_action_val_to_be_added = sum(character.summon_action_value_for_action_forward)
                    script_logger.debug(
                        f'{summon.__class__.__name__} action value to be added: {char_action_val_to_be_added}')
                    cycles_action_value_for_summon += char_action_val_to_be_added

                    # ensure it Summon's cycles action value not exceed Character's current cycles action value
                    cycles_action_value_for_summon = min(cycles_action_value_for_summon, cycles_action_value_for_char)
                else:
                    summon_end = True
    return summon_turn_count, character_turn_count


def start_simulations_for_char_with_summon(
        character: Character,
        summon,
        max_cycles: int,
        simulation_num: int) -> list[dict[str, list[Any]]]:
    """
    Start simulations for Topaz and Numby.
    :param character: Character
    :param summon: Summon of the given character
    :param max_cycles: Max number of cycles to simulate
    :param simulation_num: Number of simulations
    :return: A list of Topaz's action details as a dictionary.
    """
    main_logger.info(f'Start simulations for {character.__class__.__name__} and {summon.__class__.__name__}...')
    result_list = [simulate_turns_for_character_with_summon(character, summon, max_cycles, i) for i in
                   range(simulation_num)]
    return result_list


if __name__ == '__main__':
    pass
