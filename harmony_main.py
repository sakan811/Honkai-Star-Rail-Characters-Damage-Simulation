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


import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

from hsr_simulation.configure_logging import main_logger
from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter
from hsr_simulation.harmony.harmony_char import Sunday, Asta, Bronya, Hanya, Robin, RuanMei, Sparkle, Tingyun, \
    HarmonyTrailblazer, Yukong
from hsr_simulation.postgre import get_db_postgre_url, drop_stage_table, drop_view, create_view, load_df_to_stage_table


def start_sim_harmony() -> None:
    """
    Start simulations for Harmony characters and store the results in the database.
    :return: None
    """
    main_logger.info('Starting Harmony characters simulations...')

    # Get PostgreSQL connection URL
    postgres_url: str = get_db_postgre_url()
    engine: sqlalchemy.engine = create_engine(postgres_url)

    # Drop stage table if exists
    stage_table_name: str = 'HarmonyStage'
    drop_stage_table(postgres_url, stage_table_name)

    # Drop view if exists
    view_name: str = 'Harmony'
    drop_view(postgres_url, view_name)

    # Harmony characters list
    harmony_char_list: list[HarmonyCharacter] = [Sunday(), Asta(), Bronya(), Hanya(), Robin(), RuanMei(), Sparkle(),
                                                 Tingyun(), HarmonyTrailblazer(), Yukong()]

    # Collect results to store
    results = []
    for harmony_char in harmony_char_list:
        char_name = harmony_char.__class__.__name__
        buff_value = harmony_char.potential_buff()
        results.append({"Character": char_name, "PotentialDMGIncreased": buff_value})

    # Store results in the database
    if results:
        results_df = pd.DataFrame(results)  # Create a DataFrame from the results
        main_logger.info(f'Storing Harmony simulation results into {stage_table_name}...')
        load_df_to_stage_table(results_df, engine, stage_table_name)

    # Create a view for summarized data
    query = f'''
    CREATE OR REPLACE VIEW public."{view_name}" AS
    SELECT * FROM public."{stage_table_name}"
    ORDER BY "PotentialDMGIncreased" DESC;
    '''
    create_view(postgres_url, view_name, query)
