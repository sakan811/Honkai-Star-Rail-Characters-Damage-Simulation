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


from typing import Any, List, Dict

import numpy as np

from hsr_simulation.character import Character
from hsr_simulation.configure_logging import main_logger
from hsr_simulation.simulate_cycles import simulate_cycles, simulate_cycles_for_character_with_summon


def start_simulations(character: Character, max_cycles: int, simulation_num: int) -> List[Dict[str, List[Any]]]:
    """
    Start battle simulations.
    :param character: Character to simulate
    :param max_cycles: Max number of cycles to simulate
    :param simulation_num: Number of battles to simulate
    :return: A list of Character's action details as a dictionary.
    """
    main_logger.info(f'Starting battle simulations for {character.__class__.__name__}...')

    if simulation_num <= 0:
        return []

    # Use NumPy to create an array of simulation indices
    sim_indices = np.arange(simulation_num)

    # Use NumPy's vectorize with specified output type
    vectorized_simulate = np.vectorize(
        lambda i: simulate_cycles(character, max_cycles, i),
        otypes=[object]
    )
    result_list = vectorized_simulate(sim_indices)

    return result_list.tolist()


def start_simulations_for_char_with_summon(
        character: Character,
        summon,
        max_cycles: int,
        simulation_num: int) -> List[Dict[str, List[Any]]]:
    """
    Start battle simulations for Character and their Summon.
    :param character: Character
    :param summon: Summon of the given character
    :param max_cycles: Max number of cycles to simulate
    :param simulation_num: The Number of battles to simulate
    :return: A list of Character's action details as a dictionary.
    """
    main_logger.info(f'Start battle simulations for {character.__class__.__name__} and {summon.__class__.__name__}...')

    if simulation_num <= 0:
        return []

    # Use NumPy to create an array of simulation indices
    sim_indices = np.arange(simulation_num)

    # Use NumPy's vectorize with specified output type
    vectorized_simulate = np.vectorize(
        lambda i: simulate_cycles_for_character_with_summon(character, summon, max_cycles, i),
        otypes=[object]
    )
    result_list = vectorized_simulate(sim_indices)

    return result_list.tolist()


