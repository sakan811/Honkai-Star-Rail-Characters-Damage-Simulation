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

from hsr_simulation.configure_logging import main_logger
from hsr_simulation.harmony.asta import Asta
from hsr_simulation.harmony.bronya import Bronya
from hsr_simulation.harmony.hanya import Hanya
from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter
from hsr_simulation.harmony.harmony_trailblazer import HarmonyTrailblazer
from hsr_simulation.harmony.robin import Robin
from hsr_simulation.harmony.ruanmei import RuanMei
from hsr_simulation.harmony.sparkle import Sparkle
from hsr_simulation.harmony.sunday import Sunday
from hsr_simulation.harmony.tingyun import Tingyun
from hsr_simulation.harmony.tribbie import Tribbie
from hsr_simulation.harmony.yukong import Yukong
from hsr_simulation.postgre import PostgresOperations


def start_sim_harmony() -> None:
    """Start simulations for Harmony characters"""
    main_logger.info("Starting Harmony characters simulations...")

    db = PostgresOperations()

    # Setup database tables
    stage_table_name = "HarmonyStage"
    view_name = "Harmony"
    db.drop_stage_table(stage_table_name)
    db.drop_view(view_name)

    # Harmony characters list
    harmony_char_list: list[HarmonyCharacter] = [
        Sunday(), Asta(), Bronya(), Hanya(), Robin(),
        RuanMei(), Sparkle(), Tingyun(), HarmonyTrailblazer(),
        Yukong(), Tribbie()
    ]

    # Collect results
    results = [
        {"Character": harmony_char.__class__.__name__,
         "PotentialDMGIncreased": harmony_char.potential_buff()}
        for harmony_char in harmony_char_list
    ]

    if results:
        results_df = pd.DataFrame(results)
        main_logger.info(f"Storing Harmony simulation results into {stage_table_name}...")
        db.load_dataframe(results_df, stage_table_name)

    query = f'''
    CREATE OR REPLACE VIEW public."{view_name}" AS
    SELECT * FROM public."{stage_table_name}"
    ORDER BY "PotentialDMGIncreased" DESC;
    '''
    db.create_view(view_name, query)
