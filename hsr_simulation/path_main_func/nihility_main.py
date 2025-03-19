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
from hsr_simulation.nihility.acheron import Acheron
from hsr_simulation.nihility.black_swan import BlackSwan
from hsr_simulation.nihility.fugue import Fugue
from hsr_simulation.nihility.guinanfei import Guinanfei
from hsr_simulation.nihility.jiaoqiu import Jiaoqiu
from hsr_simulation.nihility.kafka import Kafka
from hsr_simulation.nihility.luka import Luka
from hsr_simulation.nihility.pela import Pela
from hsr_simulation.nihility.sampo import Sampo
from hsr_simulation.nihility.silver_wolf import SilverWolf
from hsr_simulation.nihility.welt import Welt
from hsr_simulation.postgre import generate_dmg_view_query
from hsr_simulation.simulate_battles import start_simulations
from hsr_simulation.utils import process_result_list
from hsr_simulation.postgre import PostgresOperations


def start_sim_nihility(simulation_num: int, max_cycles: int) -> None:
    """Start simulations for Nihility characters"""
    main_logger.info("Starting Nihility characters simulations...")

    db = PostgresOperations()

    # Setup database tables
    stage_table_name = "NihilityStage"
    view_name = "Nihility"
    db.drop_stage_table(stage_table_name)
    db.drop_view(view_name)

    # Nihility characters list
    nihility_char_list: list[Character] = [
        Kafka(),
        BlackSwan(),
        Acheron(),
        Guinanfei(),
        Pela(),
        Luka(),
        SilverWolf(),
        Sampo(),
        Welt(),
        Jiaoqiu(),
        Fugue(),
    ]

    for nihility_char in nihility_char_list:
        dict_list = start_simulations(nihility_char, max_cycles, simulation_num)
        process_result_list(nihility_char, dict_list, stage_table_name)

    query = generate_dmg_view_query(view_name, stage_table_name)
    db.create_view(view_name, query)
