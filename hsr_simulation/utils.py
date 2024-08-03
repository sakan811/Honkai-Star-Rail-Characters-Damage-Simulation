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

import pandas as pd
import sqlalchemy

from hsr_simulation.character import Character
from hsr_simulation.configure_logging import configure_logging_with_file, main_logger
from hsr_simulation.data_transformer import create_df_from_dict_list
from hsr_simulation.postgre import load_df_to_stage_table
from hsr_simulation.simulate_turns import simulate_cycles

script_logger = configure_logging_with_file(log_dir='logs', log_file='utils.log',
                                            logger_name='utils', level='DEBUG')


def process_result_list(
        character: Character,
        engine: sqlalchemy.engine,
        dict_list: list,
        stage_table_name: str) -> None:
    """
    Process a list of results by extracting total damage, calculating the average damage,
    converting the results into a DataFrame, adding the character's name to the DataFrame,
    and loading the DataFrame into a specified stage table in a database.
    :param character: Character class
    :param engine: SQLAlchemy engine
    :param dict_list: A list of dictionary that contains action details of the given character.
    :param stage_table_name: Stage table name
    :return: None
    """
    main_logger.info(f'Processing result list of {character.__class__.__name__}...')

    df = create_df_from_dict_list(dict_list)

    add_char_name_to_df(character, df)

    load_df_to_stage_table(df, engine, stage_table_name)


def add_char_name_to_df(character: Character, df: pd.DataFrame) -> None:
    """
    Add character name to dataframe
    :param character: Character class
    :param df: Dataframe
    :return: None
    """
    main_logger.info(f'Adding character name {character.__class__.__name__} to dataframe...')
    df['Character'] = f'{character.__class__.__name__}'


def start_simulations(character: Character, max_cycles: int, simulation_num: int) -> list[dict[str, list[Any]]]:
    """
    Start simulations.
    :param character: Character to simulate
    :param max_cycles: Max number of cycles to simulate
    :param simulation_num: Number of simulations
    :return: A list of Character's action details as a dictionary.
    """
    main_logger.info(f'Starting simulations for {character.__class__.__name__}...')
    result_list = [simulate_cycles(character, max_cycles, i) for i in range(simulation_num)]
    return result_list
