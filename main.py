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
import logging
import sqlite3

import pandas as pd

from hsr_simulation.character import Character
from hsr_simulation.hunt.danheng import DanHeng
from hsr_simulation.hunt.seele import Seele
from hsr_simulation.hunt.yanqing import YanQing
from hsr_simulation.simulate_turns import simulate_turns
from sql_lite_pipeline import CharacterTable
from character_dictionary import return_character_dict
from configure_logging import configure_logging_with_file

logger = configure_logging_with_file('hsr_dmg_cal.log')


def calculate_damage(class_object: Character, scenario_param: bool | int | tuple) -> tuple[float, int, int]:
    """
    Calculates character's damage based on scenarios.
    :param class_object: 'Character' class object.
    :param scenario_param: Parameter to set scenarios.
    :return: Tuple with damage calculated from scenarios.
    """
    logging.info(f'Calculates Character damage based on scenarios.')
    return class_object.calculate_battles(scenario_param)


def migrate_to_sqlite(
        table_name: str,
        scenario_name: str,
        dmg_tuple: tuple[float, int, int]) -> None:
    """
    Migrates character data to SQLite database.
    :param table_name: Table name.
    :param scenario_name: Scenario name.
    :param dmg_tuple: Tuple with damage calculated from scenarios.
    :return: None
    """
    logging.info('Migrates character data to SQLite database.')
    CharacterTable().migrate_to_character_table(table_name, scenario_name, dmg_tuple)


def main() -> None:
    """
    Main function.

    Calculate data of given character and migrate data to SQLite database.

    :return: None
    """
    char_dict = return_character_dict()

    logging.info('Looping through character dictionary...')
    for key, value in char_dict.items():
        character_object: Character = value[0]
        scenario_param_list: list[int | str] = value[1]
        scenario_list: list[str] = value[2]
        character_name: str = key

        logging.info(f'Calculating damage for {character_name}...')
        for i, scenario_name in enumerate(scenario_list):
            dmg_tuple = calculate_damage(character_object, scenario_param_list[i])
            migrate_to_sqlite(character_name, scenario_name, dmg_tuple)


if __name__ == '__main__':
    data_dict = {
        'character': [],
        'average_dmg': []
    }

    simulation_num = 100
    max_cycles = 10

    character = Seele()
    total_dmg = [simulate_turns(character, max_cycles) for _ in range(simulation_num)]
    avg_dmg = sum(total_dmg) / len(total_dmg)
    logger.debug(f'Average Damage: {avg_dmg}')
    data_dict['character'].append('Seele')
    data_dict['average_dmg'].append(avg_dmg)

    character = DanHeng()
    total_dmg = [simulate_turns(character, max_cycles) for _ in range(simulation_num)]
    avg_dmg = sum(total_dmg) / len(total_dmg)
    logger.debug(f'Average Damage: {avg_dmg}')
    data_dict['character'].append('Dan Heng')
    data_dict['average_dmg'].append(avg_dmg)

    character = YanQing()
    total_dmg = [simulate_turns(character, max_cycles) for _ in range(simulation_num)]
    avg_dmg = sum(total_dmg) / len(total_dmg)
    logger.debug(f'Average Damage: {avg_dmg}')
    data_dict['character'].append('Yanqing')
    data_dict['average_dmg'].append(avg_dmg)

    df = pd.DataFrame.from_dict(data_dict)
    db = 'hsr_dmg_calculation.db'
    with sqlite3.connect(db) as connection:
        dtype = {
            'character': 'text primary key',
            'average_dmg': 'float not null'
        }

        df.to_sql(name='Hunt', con=connection, if_exists='replace', dtype=dtype, index=False)




