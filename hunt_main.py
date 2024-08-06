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

from hsr_simulation.configure_logging import main_logger
from hsr_simulation.simulate_battles import start_simulations, start_simulations_for_char_with_summon
from hsr_simulation.hunt.boothill import Boothill
from hsr_simulation.hunt.danheng import DanHeng
from hsr_simulation.hunt.dr_ratio import DrRatio
from hsr_simulation.hunt.march7th_hunt import March7thHunt
from hsr_simulation.hunt.seele import Seele
from hsr_simulation.hunt.sushang import Sushang
from hsr_simulation.hunt.topaz import Topaz
from hsr_simulation.hunt.yanqing import YanQing
from hsr_simulation.postgre import get_db_postgre_url, drop_stage_table, drop_view, create_view

from hsr_simulation.utils import process_result_list


def start_sim_hunt(simulation_num: int, max_cycles: int) -> None:
    """
    Start simulations for Hunt characters
    :simulation_num: Number of simulations
    :max_cycles: Maximum number of cycles to simulate
    :return: None
    """
    main_logger.info('Starting Hunt characters simulations...')

    # get PostgreSQL connection URL
    postgres_url = get_db_postgre_url()
    engine = create_engine(postgres_url)

    # drop stage table if exists
    stage_table_name = 'HuntStage'
    drop_stage_table(postgres_url, stage_table_name)

    # drop view if exist
    view_name = 'Hunt'
    drop_view(postgres_url, view_name)

    character = Seele()
    dict_list = start_simulations(character, max_cycles, simulation_num)
    process_result_list(character, engine, dict_list, stage_table_name)

    character = DanHeng()
    dict_list = start_simulations(character, max_cycles, simulation_num)
    process_result_list(character, engine, dict_list, stage_table_name)

    character = YanQing()
    dict_list = start_simulations(character, max_cycles, simulation_num)
    process_result_list(character, engine, dict_list, stage_table_name)

    character = Sushang()
    dict_list = start_simulations(character, max_cycles, simulation_num)
    process_result_list(character, engine, dict_list, stage_table_name)

    topaz = Topaz()
    numby = topaz.summon_numby()
    dict_list = start_simulations_for_char_with_summon(topaz, numby, max_cycles, simulation_num)
    process_result_list(topaz, engine, dict_list, stage_table_name)

    character = DrRatio()
    dict_list = start_simulations(character, max_cycles, simulation_num)
    process_result_list(character, engine, dict_list, stage_table_name)

    character = Boothill()
    dict_list = start_simulations(character, max_cycles, simulation_num)
    process_result_list(character, engine, dict_list, stage_table_name)

    character = March7thHunt()
    dict_list = start_simulations(character, max_cycles, simulation_num)
    process_result_list(character, engine, dict_list, stage_table_name)

    create_view(postgres_url, view_name, stage_table_name)
