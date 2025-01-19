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
from hsr_simulation.hunt.boothill import Boothill
from hsr_simulation.hunt.danheng import DanHeng
from hsr_simulation.hunt.dr_ratio import DrRatio
from hsr_simulation.hunt.feixiao import Feixiao
from hsr_simulation.hunt.march7th_hunt import March7thHunt
from hsr_simulation.hunt.moze import Moze
from hsr_simulation.hunt.seele import Seele
from hsr_simulation.hunt.sushang import Sushang
from hsr_simulation.hunt.topaz import Topaz
from hsr_simulation.hunt.yanqing import YanQing
from hsr_simulation.postgre import generate_dmg_view_query
from hsr_simulation.simulate_battles import start_simulations, start_simulations_for_char_with_summon
from hsr_simulation.utils import process_result_list
from hsr_simulation.postgre import PostgresOperations


def start_sim_hunt(simulation_num: int, max_cycles: int) -> None:
    """
    Start simulations for Hunt characters
    :param simulation_num: Number of simulations
    :param max_cycles: Maximum number of cycles to simulate
    :return: None
    """
    main_logger.info('Starting Hunt characters simulations...')

    db = PostgresOperations()

    # Setup database tables
    stage_table_name = 'HuntStage'
    view_name = 'Hunt'
    db.drop_stage_table(stage_table_name)
    db.drop_view(view_name)

    # Hunt characters list
    hunt_char_list: list[Character] = [Seele(), DanHeng(), YanQing(), Sushang(), 
                                     Topaz(), DrRatio(), Boothill(), March7thHunt(), 
                                     Feixiao(), Moze()]

    for hunt_char in hunt_char_list:
        if isinstance(hunt_char, Topaz):
            numby = hunt_char.summon_numby(hunt_char)
            dict_list = start_simulations_for_char_with_summon(hunt_char, numby, 
                                                             max_cycles, simulation_num)
        else:
            dict_list = start_simulations(hunt_char, max_cycles, simulation_num)
        process_result_list(hunt_char, dict_list, stage_table_name)

    query = generate_dmg_view_query(view_name, stage_table_name)
    db.create_view(view_name, query)
