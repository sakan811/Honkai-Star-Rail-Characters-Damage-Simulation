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
from hsr_simulation.summon import Summon


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
        main_logger.debug(f'{character.__class__.__name__} current speed: {char_spd}')

        char_action_val = character.calculate_action_value(char_spd)
        main_logger.debug(f'{character.__class__.__name__} current action value: {char_action_val}')

        if cycles_action_val < char_action_val:
            break
        else:
            character.take_action()

            cycles_action_val -= char_action_val
            char_turn_count += 1

            # simulate Action Forward
            main_logger.debug(f'{character.__class__.__name__} current speed: {character.speed}')
            char_action_val_to_be_added = sum(character.char_action_value_for_action_forward)
            main_logger.debug(
                f'{character.__class__.__name__} action value to be added: {char_action_val_to_be_added}')

            # ensure that the character action value to be added not exceeds the action value,
            # used to subtract the cycle action value
            char_action_val_to_be_added = min(char_action_val_to_be_added, char_action_val)
            cycles_action_val += char_action_val_to_be_added

    return char_turn_count


def simulate_turns_for_char_with_summon(
        cycles_action_value_for_summon: float,
        cycles_action_value_for_char: float,
        summon: Summon,
        summon_end: bool,
        character: Character,
        character_end: bool) -> tuple[int, int]:
    """
    Simulate turns for Character and their summon.
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
                main_logger.debug(f'{character.__class__.__name__} speed: {character_speed}')
                character_action_value = character.calculate_action_value(character_speed)
                main_logger.debug(f'{character.__class__.__name__} action value: {character_action_value}')

                # calculate whether Character has turns left
                if cycles_action_value_for_char >= character_action_value:
                    character.take_action()

                    cycles_action_value_for_char -= character_action_value
                    character_turn_count += 1

                    # simulate Action Forward
                    main_logger.debug(f'{character.__class__.__name__} current speed: {character.speed}')
                    char_action_val_to_be_added = sum(character.char_action_value_for_action_forward)
                    main_logger.debug(
                        f'{character.__class__.__name__} action value to be added: {char_action_val_to_be_added}')

                    # ensure that the character action value to be added not exceeds the action value,
                    # used to subtract the cycle action value
                    char_action_val_to_be_added = min(char_action_val_to_be_added, character_action_value)
                    cycles_action_value_for_char += char_action_val_to_be_added
                else:
                    character_end = True

            if not summon_end:
                main_logger.debug(f'{summon.__class__.__name__} speed: {summon.speed}')
                summon_action_val = summon.calculate_action_value(summon.speed)
                main_logger.debug(f'{summon.__class__.__name__} action value: {summon_action_val}')

                # calculate whether Summon has turns left
                if cycles_action_value_for_summon >= summon_action_val:
                    summon.take_action()

                    cycles_action_value_for_summon -= summon_action_val
                    summon_turn_count += 1

                    # simulate Action Forward
                    main_logger.debug(f'{summon.__class__.__name__} current speed: {summon.speed}')
                    char_action_val_to_be_added = sum(summon.summon_action_value_for_action_forward)
                    main_logger.debug(
                        f'{summon.__class__.__name__} action value to be added: {char_action_val_to_be_added}')
                    cycles_action_value_for_summon += char_action_val_to_be_added

                    # ensure it Summon's cycles action value not exceed Character's current cycles action value
                    cycles_action_value_for_summon = min(cycles_action_value_for_summon, cycles_action_value_for_char)

                    # reset summon stats
                    summon.reset_summon_stat()
                else:
                    summon_end = True
    return summon_turn_count, character_turn_count


if __name__ == '__main__':
    pass
