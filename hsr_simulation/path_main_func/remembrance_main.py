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
from hsr_simulation.postgre import generate_dmg_view_query
from hsr_simulation.remembrance.algaea import Algaea
from hsr_simulation.remembrance.remembrance_trailblazer import RemembranceTrailblazer
from hsr_simulation.simulate_battles import start_simulations
from hsr_simulation.utils import process_result_list
from hsr_simulation.postgre import PostgresOperations


def start_sim_remembrance(simulation_num: int, max_cycles: int) -> None:
    """
    Start simulations for Remembrance characters
    :param simulation_num: Number of simulations
    :param max_cycles: Maximum number of cycles to simulate
    :return: None
    """
    main_logger.info("Starting Remembrance characters simulations...")

    db = PostgresOperations()

    # Setup database tables
    stage_table_name = "RemembranceStage"
    view_name = "Remembrance"
    db.drop_stage_table(stage_table_name)
    db.drop_view(view_name)

    # Remembrance characters list
    remembrance_char_list: list[Character] = [RemembranceTrailblazer(), Algaea()]

    for remembrance_char in remembrance_char_list:
        dict_list = start_simulations(remembrance_char, max_cycles, simulation_num)
        process_result_list(remembrance_char, dict_list, stage_table_name)

    query = generate_dmg_view_query(view_name, stage_table_name)
    db.create_view(view_name, query)
