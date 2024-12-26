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
from typing import Any, Dict, List


from hsr_simulation.character import Character
from hsr_simulation.configure_logging import main_logger
from hsr_simulation.destruction.firefly import FireFly
from hsr_simulation.destruction.xueyi import Xueyi
from hsr_simulation.erudition.jingyuan import Jingyuan
from hsr_simulation.erudition.rappa import Rappa
from hsr_simulation.hunt.boothill import Boothill
from hsr_simulation.hunt.march7th_hunt import March7thHunt
from hsr_simulation.hunt.topaz import Topaz
from hsr_simulation.nihility.acheron import Acheron
from hsr_simulation.nihility.black_swan import BlackSwan
from hsr_simulation.nihility.fugue import Fugue
from hsr_simulation.nihility.jiaoqiu import Jiaoqiu
from hsr_simulation.nihility.luka import Luka
from hsr_simulation.simulate_turns import (
    simulate_turns,
    simulate_turns_for_char_with_summon,
)


class CharacterStatsInitializer:
    @staticmethod
    def initialize_stats(character: Character) -> None:
        """
        Initialize character-specific stats based on character type.

        This method sets up initial stats and effects for different characters based on their class type.
        For example, it sets break effects for Boothill/Fugue, effect hit rates for Black Swan, etc.

        :param character: The character instance to initialize stats for
        :type character: Character
        :return: None
        :rtype: None
        """
        stats_handlers = {
            (Boothill, Fugue): lambda c: c.set_break_effect(1, 3),
            BlackSwan: lambda c: c.set_effect_hit_rate(0, 1.2),
            Acheron: lambda c: c.random_nihility_teammate(),
            March7thHunt: lambda c: c.set_shifu(),
            Luka: lambda c: c.random_enemy_hp(),
            Jiaoqiu: lambda c: c.set_effect_hit_rate(0, 1.4),
            FireFly: lambda c: c.set_break_effect(1, 3.6),
            Xueyi: lambda c: c.set_break_effect(1, 2.4),
            Rappa: lambda c: setattr(c, "atk", random.choice([2400, 3200])),
        }

        for char_types, handler in stats_handlers.items():
            if isinstance(char_types, tuple):
                if any(isinstance(character, char_type) for char_type in char_types):
                    handler(character)
                    break
            elif isinstance(character, char_types):
                handler(character)
                break


class BattleSimulator:
    @staticmethod
    def calculate_cycles_action_value(max_cycles: int) -> int:
        """
        Calculate total action value for given cycles.

        :param max_cycles: Maximum number of cycles to simulate
        :type max_cycles: int
        :return: Total action value for the cycles
        :rtype: int
        """
        return 150 + ((max_cycles - 1) * 100)

    @staticmethod
    def prepare_simulation_data(
        character: Character, simulate_round: int, row_num: int
    ) -> None:
        """
        Prepare simulation data for the character.

        :param character: Character to prepare data for
        :type character: Character
        :param simulate_round: Current simulation round number
        :type simulate_round: int
        :param row_num: Number of rows of data to prepare
        :type row_num: int
        :return: None
        :rtype: None
        """
        character.data["Simulate Round No."] = [simulate_round for _ in range(row_num)]

    @staticmethod
    def simulate_regular_battle(
        character: Character, max_cycles: int, simulate_round: int
    ) -> Dict[str, List[Any]]:
        """
        Simulate battle for regular characters.

        This method simulates a battle for characters without summons. It:
        1. Calculates total action value based on cycles
        2. Initializes character stats
        3. Simulates turns
        4. Prepares and returns battle data

        :param character: Character to simulate battle for
        :type character: Character
        :param max_cycles: Maximum number of cycles to simulate
        :type max_cycles: int
        :param simulate_round: Current simulation round number
        :type simulate_round: int
        :return: Dictionary containing battle simulation data
        :rtype: Dict[str, List[Any]]
        """
        main_logger.info(f"Simulating turns for {character.__class__.__name__}...")

        cycles_action_val = BattleSimulator.calculate_cycles_action_value(max_cycles)
        main_logger.debug(f"Total cycles action value: {cycles_action_val}")

        CharacterStatsInitializer.initialize_stats(character)
        character.start_battle()

        char_turn_count = simulate_turns(character, cycles_action_val)
        main_logger.debug(
            f"Total number of {character.__class__.__name__} turns: {char_turn_count}"
        )

        BattleSimulator.prepare_simulation_data(
            character, simulate_round, len(character.data["DMG"])
        )
        data_dict = character.data
        character.reset_character_data_for_each_battle()

        return data_dict

    @staticmethod
    def initialize_summon(character: Character, summon: Character) -> Character:
        """
        Initialize summon based on character type.

        :param character: Main character that summons
        :type character: Character
        :param summon: Summon character to initialize
        :type summon: Character
        :return: Initialized summon character
        :rtype: Character
        """
        summon_initializers = {
            Topaz: lambda c: c.summon_numby(c),
            Jingyuan: lambda c: c.summon_lightning_lord(c),
        }

        for char_type, initializer in summon_initializers.items():
            if isinstance(character, char_type):
                return initializer(character)
        return summon

    @staticmethod
    def simulate_battle_with_summon(
        character: Character, summon: Character, max_cycles: int, simulate_round: int
    ) -> Dict[str, List[Any]]:
        """
        Simulate battle for characters with summons.

        This method simulates a battle for characters with summons. It:
        1. Calculates total action value based on cycles
        2. Initializes the summon
        3. Simulates turns for both character and summon
        4. Prepares and returns battle data

        :param character: Main character to simulate battle for
        :type character: Character
        :param summon: Summon character to simulate battle for
        :type summon: Character
        :param max_cycles: Maximum number of cycles to simulate
        :type max_cycles: int
        :param simulate_round: Current simulation round number
        :type simulate_round: int
        :return: Dictionary containing battle simulation data
        :rtype: Dict[str, List[Any]]
        """
        main_logger.info(
            f"Simulating turns for {character.__class__.__name__} and {summon.__class__.__name__}..."
        )

        cycles_action_val = BattleSimulator.calculate_cycles_action_value(max_cycles)
        main_logger.debug(f"Total cycles action value: {cycles_action_val}")

        summon = BattleSimulator.initialize_summon(character, summon)
        character.start_battle()

        summon_turn_count, char_turn_count = simulate_turns_for_char_with_summon(
            cycles_action_val, cycles_action_val, summon, False, character, False
        )

        main_logger.debug(
            f"Total number of {character.__class__.__name__} turns: {char_turn_count}"
        )
        main_logger.debug(
            f"Total number of {summon.__class__.__name__} turns: {summon_turn_count}"
        )

        BattleSimulator.prepare_simulation_data(
            character, simulate_round, len(character.data["DMG"])
        )
        data_dict = character.data
        character.reset_character_data_for_each_battle()

        return data_dict


def simulate_cycles(
    character: Character, max_cycles: int, simulate_round: int
) -> Dict[str, List[Any]]:
    """
    Simulate battle cycles for a character.
    
    This function simulates battle cycles for a single character by:
    1. Calling the BattleSimulator to run a regular battle simulation
    2. Processing the results through the specified number of cycles
    
    :param character: Character to simulate battle for
    :type character: Character
    :param max_cycles: Maximum number of cycles to simulate
    :type max_cycles: int 
    :param simulate_round: Current simulation round number
    :type simulate_round: int
    :return: Dictionary containing battle simulation data
    :rtype: Dict[str, List[Any]]
    """
    return BattleSimulator.simulate_regular_battle(
        character, max_cycles, simulate_round
    )


def simulate_cycles_for_character_with_summon(
    character: Character, summon: Character, max_cycles: int, simulate_round: int
) -> Dict[str, List[Any]]:
    """
    Simulate battle cycles for a character with summon.
    
    This function simulates battle cycles for a character and their summon by:
    1. Calling the BattleSimulator to run a battle simulation with summon
    2. Processing turns for both the main character and summon
    3. Handling the interaction between character and summon actions
    
    :param character: Main character to simulate battle for
    :type character: Character
    :param summon: Summon character to simulate battle for
    :type summon: Character 
    :param max_cycles: Maximum number of cycles to simulate
    :type max_cycles: int
    :param simulate_round: Current simulation round number
    :type simulate_round: int
    :return: Dictionary containing battle simulation data
    :rtype: Dict[str, List[Any]]
    """
    return BattleSimulator.simulate_battle_with_summon(
        character, summon, max_cycles, simulate_round
    )
