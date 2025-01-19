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
from hsr_simulation.erudition.argenti import Argenti
from hsr_simulation.erudition.herta import Herta
from hsr_simulation.erudition.himeko import Himeko
from hsr_simulation.erudition.jade import Jade
from hsr_simulation.erudition.jingyuan import Jingyuan
from hsr_simulation.erudition.qingque import Qingque
from hsr_simulation.erudition.rappa import Rappa
from hsr_simulation.erudition.serval import Serval
from hsr_simulation.erudition.the_herta import TheHerta
from hsr_simulation.postgre import generate_dmg_view_query
from hsr_simulation.simulate_battles import start_simulations, start_simulations_for_char_with_summon
from hsr_simulation.utils import process_result_list
from hsr_simulation.postgre import PostgresOperations


def start_sim_erudition(simulation_num: int, max_cycles: int) -> None:
    """
    Start simulations for Erudition characters
    :param simulation_num: Number of simulations
    :param max_cycles: Maximum number of cycles to simulate
    :return: None
    """
    main_logger.info('Starting Erudition characters simulations...')

    db = PostgresOperations()

    # Setup database tables
    stage_table_name = 'EruditionStage'
    view_name = 'Erudition'
    db.drop_stage_table(stage_table_name)
    db.drop_view(view_name)

    # Erudition characters list
    erudition_char_list: list[Character] = [Qingque(), Argenti(), Herta(), Himeko(), Serval(), Jade(), Jingyuan(),
                                            Rappa(), TheHerta()]

    for erudition_char in erudition_char_list:
        if isinstance(erudition_char, Jingyuan):
            lightning_lord = erudition_char.summon_lightning_lord(erudition_char)
            dict_list = start_simulations_for_char_with_summon(erudition_char, lightning_lord,
                                                              max_cycles, simulation_num)
        else:
            dict_list = start_simulations(erudition_char, max_cycles, simulation_num)
        process_result_list(erudition_char, dict_list, stage_table_name)

    query = generate_dmg_view_query(view_name, stage_table_name)
    db.create_view(view_name, query)
