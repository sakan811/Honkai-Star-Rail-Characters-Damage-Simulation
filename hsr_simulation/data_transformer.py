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


def create_df_from_dict_list(dict_list: list[dict]) -> pd.DataFrame:
    """
    Create a dataframe from a list of dictionaries.
    :param dict_list: Dictionaries to create the dataframe from.
    :return: Dataframe created from a list of dictionaries.
    """
    main_logger.info('Creating dataframe from a list of dictionary...')
    df_list = []
    for entry in dict_list:
        df = pd.DataFrame({
            'DMG': entry['DMG'],
            'DMG_Type': entry['DMG_Type'],
            'Simulate Round No.': entry['Simulate Round No.']
        })
        df_list.append(df)

    return pd.concat(df_list)
