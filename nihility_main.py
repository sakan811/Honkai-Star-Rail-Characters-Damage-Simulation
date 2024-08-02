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
from sqlalchemy import create_engine

from hsr_simulation.configure_logging import configure_logging_with_file, main_logger
from hsr_simulation.nihility.acheron import Acheron
from hsr_simulation.nihility.black_swan import BlackSwan
from hsr_simulation.nihility.guinanfei import Guinanfei
from hsr_simulation.nihility.kafka import Kafka
from hsr_simulation.postgre import get_db_postgre_url, drop_stage_table, drop_view, create_view
from hsr_simulation.utils import start_simulations, process_result_list

script_logger = configure_logging_with_file(log_dir='logs', log_file='nihility_main.log',
                                            logger_name='nihility_main', level='DEBUG')


def start_sim_nihility(simulation_num: int, max_cycles: int) -> None:
    """
    Start simulations for Nihility characters
    :simulation_num: Number of simulations
    :max_cycles: Maximum number of cycles to simulate
    :return: None
    """
    main_logger.info('Starting Nihility characters simulations...')

    # get PostgreSQL connection URL
    postgres_url = get_db_postgre_url()
    engine = create_engine(postgres_url)

    # drop stage table if exists
    stage_table_name = 'NihilityStage'
    drop_stage_table(postgres_url, stage_table_name)

    # drop view if exist
    view_name = 'Nihility'
    drop_view(postgres_url, view_name)

    character = Kafka()
    result_list = start_simulations(character, max_cycles, simulation_num)
    process_result_list(character, engine, result_list, stage_table_name)

    character = BlackSwan()
    result_list = start_simulations(character, max_cycles, simulation_num)
    process_result_list(character, engine, result_list, stage_table_name)

    character = Acheron()
    result_list = start_simulations(character, max_cycles, simulation_num)
    process_result_list(character, engine, result_list, stage_table_name)

    character = Guinanfei()
    result_list = start_simulations(character, max_cycles, simulation_num)
    process_result_list(character, engine, result_list, stage_table_name)

    create_view(postgres_url, view_name, stage_table_name)
