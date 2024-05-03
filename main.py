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

from Character import Character
from sql_lite_pipeline import CharacterTable
from character_dictionary import return_character_dict


def calculate_damage(class_object: Character, scenario_param: bool | int) -> tuple[float, int, int]:
    """
    Calculates character's damage based on scenarios.
    :param class_object: 'Character' class object.
    :param scenario_param: Parameter to set scenarios.
    :return: Tuple with damage calculated from scenarios.
    """
    return class_object.calculate_battles(scenario_param)


def migrate_to_sqlite(
        table_name: str,
        scenario_name: str,
        dmg_tuple: tuple[float, int, int]) -> None:
    """
    Migrates character data to SQLite database.
    :param table_name: Table name.
    :param scenario_name: Scenario name.
    :param dmg_tuple: Tuple with damage calculated from scenarios.
    :return: None
    """
    CharacterTable().migrate_to_character_table(table_name, scenario_name, dmg_tuple)


def main() -> None:
    """
    Main function.

    Calculate data of given character and migrate data to SQLite database.

    :return: None
    """
    char_dict = return_character_dict()

    for key, value in char_dict.items():
        character_object: Character = value[0]
        scenario_param_list: list[int | str] = value[1]
        scenario_list: list[str] = value[2]
        character_name: str = key

        for i, scenario_name in enumerate(scenario_list):
            dmg_tuple = calculate_damage(character_object, scenario_param_list[i])
            migrate_to_sqlite(character_name, scenario_name, dmg_tuple)


if __name__ == '__main__':
    main()
