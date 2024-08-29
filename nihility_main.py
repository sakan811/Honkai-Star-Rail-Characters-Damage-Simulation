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
import sqlalchemy
from sqlalchemy import create_engine

from hsr_simulation.character import Character
from hsr_simulation.configure_logging import main_logger
from hsr_simulation.nihility.acheron import Acheron
from hsr_simulation.nihility.black_swan import BlackSwan
from hsr_simulation.nihility.guinanfei import Guinanfei
from hsr_simulation.nihility.jiaoqiu import Jiaoqiu
from hsr_simulation.nihility.kafka import Kafka
from hsr_simulation.nihility.luka import Luka
from hsr_simulation.nihility.pela import Pela
from hsr_simulation.nihility.sampo import Sampo
from hsr_simulation.nihility.silver_wolf import SilverWolf
from hsr_simulation.nihility.welt import Welt
from hsr_simulation.postgre import get_db_postgre_url, drop_stage_table, drop_view, create_view
from hsr_simulation.simulate_battles import start_simulations
from hsr_simulation.utils import process_result_list


def start_sim_nihility(simulation_num: int, max_cycles: int) -> None:
    """
    Start simulations for Nihility characters
    :param simulation_num: Number of simulations
    :param max_cycles: Maximum number of cycles to simulate
    :return: None
    """
    main_logger.info('Starting Nihility characters simulations...')

    # get PostgreSQL connection URL
    postgres_url: str = get_db_postgre_url()
    engine: sqlalchemy.engine = create_engine(postgres_url)

    # drop stage table if exists
    stage_table_name: str = 'NihilityStage'
    drop_stage_table(postgres_url, stage_table_name)

    # drop view if exist
    view_name: str = 'Nihility'
    drop_view(postgres_url, view_name)

    # Nihility characters list
    nihility_char_list: list[Character] = [Kafka(), BlackSwan(), Acheron(),
                                           Guinanfei(), Pela(), Luka(),
                                           SilverWolf(), Sampo(), Welt(),
                                           Jiaoqiu()]

    for nihility_char in nihility_char_list:
        result_list: list[dict[str, list]] = start_simulations(nihility_char, max_cycles, simulation_num)
        process_result_list(nihility_char, engine, result_list, stage_table_name)

    create_view(postgres_url, view_name, stage_table_name)
