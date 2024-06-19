import logging

import numpy as np

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

from characters.Hunt import *
from characters.Nihility import *
from characters.Destruction import *


def return_character_dict():
    """
    Returns a dictionary with the following data:

    - Character name as Key
    - Tuple as Value.

    The Tuple contains the following data:

    - 'Character' class object
    - Scenario parameter as List
    - Scenario name as List

    :return: Dictionary that contains data for calculating character's damage and migrating to SQLite database.
    """
    logging.info('Return character dictionary.')

    firefly_break_effect_list: list[float] = np.arange(1, 3.61, 0.1).tolist()
    firefly_scenario_list: list[str] = [f'{int(i * 100)}% Break Effect' for i in firefly_break_effect_list]

    character_dict = {
        'Seele': (Seele(), [False, True], ['Seele With No Resurgence Buff', 'Seele With Resurgence Buff']),
        'DrRatio': (DrRatio(), [0, 1, 2, 3], ['0 Debuff', '1 Debuff', '2 Debuff', '3 Debuff']),
        'Numby': (Numby(), [False, True], ['Numby With No Ult Buff', 'Numby With Ult Buff']),
        'Acheron': (
            Acheron(),
            [0, 1, 2],
            [
                'Acheron With No Nihility Teammate',
                'Acheron With 1 Nihility Teammate',
                'Acheron With 2 Nihility Teammates'
            ]
        ),
        'ImbibitorLunae': (
            ImbibitorLunae(),
            [1, 2, 3],
            [
                'ImbibitorLunae With Enhanced-Once Basic Atk',
                'ImbibitorLunae With Enhanced-Twice Basic Atk',
                'ImbibitorLunae With Enhanced-Thrice Basic Atk'
            ]
        ),
        'Firefly': (
            Firefly(),
            firefly_break_effect_list,
            firefly_scenario_list
        )
    }
    return character_dict

