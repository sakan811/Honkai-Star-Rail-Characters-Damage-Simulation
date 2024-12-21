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

from hsr_simulation.character import Character
from hsr_simulation.configure_logging import main_logger
from hsr_simulation.destruction.arlan import Arlan
from hsr_simulation.destruction.blade import Blade
from hsr_simulation.destruction.clara import Clara
from hsr_simulation.destruction.firefly import FireFly
from hsr_simulation.destruction.hook import Hook
from hsr_simulation.destruction.imbibitor_lunae import ImbibitorLunae
from hsr_simulation.destruction.jingliu import Jingliu
from hsr_simulation.destruction.misha import Misha
from hsr_simulation.destruction.trailblazer_physical import TrailblazerPhysical
from hsr_simulation.destruction.xueyi import Xueyi
from hsr_simulation.destruction.yunli import Yunli
from hsr_simulation.postgre import get_db_postgre_url, drop_stage_table, drop_view, create_view, generate_dmg_view_query
from hsr_simulation.simulate_battles import start_simulations
from hsr_simulation.utils import process_result_list


def start_sim_destruction(simulation_num: int, max_cycles: int) -> None:
    """
    Start simulations for Destruction characters
    :param simulation_num: Number of simulations
    :param max_cycles: Maximum number of cycles to simulate
    :return: None
    """
    main_logger.info('Starting Destruction characters simulations...')

    # get PostgreSQL connection URL
    postgres_url = get_db_postgre_url()
    engine = create_engine(postgres_url)

    # drop stage table if exists
    stage_table_name = 'DestructionStage'
    drop_stage_table(postgres_url, stage_table_name)

    # drop view if exist
    view_name = 'Destruction'
    drop_view(postgres_url, view_name)

    # Destruction characters list
    destruction_char_list: list[Character] = [Jingliu(), Hook(), Arlan(), Blade(), Clara(), ImbibitorLunae(), FireFly(),
                                              TrailblazerPhysical(), Misha(), Xueyi(), Yunli()]

    for destruction_char in destruction_char_list:
        result_list: list[dict[str, list]] = start_simulations(destruction_char, max_cycles, simulation_num)
        process_result_list(destruction_char, engine, result_list, stage_table_name)

    query = generate_dmg_view_query(view_name, stage_table_name)
    create_view(postgres_url, view_name, query)
