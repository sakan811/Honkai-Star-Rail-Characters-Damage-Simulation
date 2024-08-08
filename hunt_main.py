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
from hsr_simulation.hunt.boothill import Boothill
from hsr_simulation.hunt.danheng import DanHeng
from hsr_simulation.hunt.dr_ratio import DrRatio
from hsr_simulation.hunt.march7th_hunt import March7thHunt
from hsr_simulation.hunt.seele import Seele
from hsr_simulation.hunt.sushang import Sushang
from hsr_simulation.hunt.topaz import Topaz
from hsr_simulation.hunt.yanqing import YanQing
from hsr_simulation.postgre import get_db_postgre_url, drop_stage_table, drop_view, create_view
from hsr_simulation.simulate_battles import start_simulations, start_simulations_for_char_with_summon
from hsr_simulation.utils import process_result_list


def start_sim_hunt(base_char: Character, simulation_num: int, max_cycles: int) -> None:
    """
    Start simulations for Hunt characters
    :param base_char: Base Character class
    :param simulation_num: Number of simulations
    :param max_cycles: Maximum number of cycles to simulate
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

    # Hunt characters list
    hunt_char_list = [Seele(base_char), DanHeng(base_char), YanQing(base_char), Sushang(base_char), Topaz(base_char),
                      DrRatio(base_char), Boothill(base_char), March7thHunt(base_char)]

    for hunt_char in hunt_char_list:
        # when the character is Topaz
        if isinstance(hunt_char, Topaz):
            numby = hunt_char.summon_numby()
            dict_list = start_simulations_for_char_with_summon(hunt_char, numby, max_cycles, simulation_num)
            process_result_list(hunt_char, engine, dict_list, stage_table_name)
        else:
            dict_list = start_simulations(hunt_char, max_cycles, simulation_num)
            process_result_list(hunt_char, engine, dict_list, stage_table_name)

    create_view(postgres_url, view_name, stage_table_name)
