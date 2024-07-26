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
import sqlite3

import pandas as pd

from configure_logging import configure_logging_with_file
from hsr_simulation.hunt.boothill import Boothill
from hsr_simulation.hunt.danheng import DanHeng
from hsr_simulation.hunt.dr_ratio import DrRatio
from hsr_simulation.hunt.seele import Seele
from hsr_simulation.hunt.sushang import Sushang
from hsr_simulation.hunt.topaz import Topaz, Numby, simulate_turns_for_topaz
from hsr_simulation.hunt.yanqing import YanQing
from hsr_simulation.simulate_turns import simulate_turns

logger = configure_logging_with_file('hsr_dmg_cal.log')


if __name__ == '__main__':
    data_dict = {
        'character': [],
        'average_dmg': []
    }

    simulation_num = 100
    max_cycles = 10

    character = Seele()
    total_dmg = [simulate_turns(character, max_cycles) for _ in range(simulation_num)]
    avg_dmg = sum(total_dmg) / len(total_dmg)
    logger.debug(f'Average Damage: {avg_dmg}')
    data_dict['character'].append('Seele')
    data_dict['average_dmg'].append(avg_dmg)

    character = DanHeng()
    total_dmg = [simulate_turns(character, max_cycles) for _ in range(simulation_num)]
    avg_dmg = sum(total_dmg) / len(total_dmg)
    logger.debug(f'Average Damage: {avg_dmg}')
    data_dict['character'].append('Dan Heng')
    data_dict['average_dmg'].append(avg_dmg)

    character = YanQing()
    total_dmg = [simulate_turns(character, max_cycles) for _ in range(simulation_num)]
    avg_dmg = sum(total_dmg) / len(total_dmg)
    character.add_data_to_table()
    logger.debug(f'Average Damage: {avg_dmg}')
    data_dict['character'].append('Yanqing')
    data_dict['average_dmg'].append(avg_dmg)

    character = Sushang()
    total_dmg = [simulate_turns(character, max_cycles) for _ in range(simulation_num)]
    avg_dmg = sum(total_dmg) / len(total_dmg)
    logger.debug(f'Average Damage: {avg_dmg}')
    data_dict['character'].append('Sushang')
    data_dict['average_dmg'].append(avg_dmg)

    topaz = Topaz()
    numby = Numby(topaz)
    total_dmg = [simulate_turns_for_topaz(topaz, numby, max_cycles) for _ in range(simulation_num)]
    avg_dmg = sum(total_dmg) / len(total_dmg)
    logger.debug(f'Average Damage: {avg_dmg}')
    data_dict['character'].append('Topaz')
    data_dict['average_dmg'].append(avg_dmg)

    character = DrRatio()
    total_dmg = [simulate_turns(character, max_cycles) for _ in range(simulation_num)]
    avg_dmg = sum(total_dmg) / len(total_dmg)
    logger.debug(f'Average Damage: {avg_dmg}')
    data_dict['character'].append('Dr. Ratio')
    data_dict['average_dmg'].append(avg_dmg)

    character = Boothill()
    total_dmg = [simulate_turns(character, max_cycles) for _ in range(simulation_num)]
    avg_dmg = sum(total_dmg) / len(total_dmg)
    character.add_data_to_table()
    logger.debug(f'Average Damage: {avg_dmg}')
    data_dict['character'].append('Boothill')
    data_dict['average_dmg'].append(avg_dmg)

    df = pd.DataFrame.from_dict(data_dict)
    db = 'hsr_dmg_calculation.db'
    with sqlite3.connect(db) as connection:
        dtype = {
            'character': 'text primary key',
            'average_dmg': 'float not null'
        }

        df.to_sql(name='Hunt', con=connection, if_exists='replace', dtype=dtype, index=False)




