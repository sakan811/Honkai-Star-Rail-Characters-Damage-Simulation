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
import logging

from sqlalchemy import create_engine, Engine, text


def connect_to_db() -> Engine:
    """
    Connects to the SQLite database
    :return: SQLAlchemy Engine
    """
    logging.info('Connect to SQLite database')
    engine = create_engine('sqlite:///hsr_dmg_calculation.db')

    return engine


class CharacterTable:
    def __init__(self):
        pass

    def migrate_to_character_table(
            self, table_name: str, scenario_name: str, dmg_tuple: tuple[float, int, int]
    ) -> None:
        """
        Migrates data to the given character table.
        :param table_name:  Table name
        :param scenario_name: Character name
        :param dmg_tuple: Tuple of Damage
        :return: None
        """
        logging.info(f'Migrating data to {table_name} table...')
        engine = connect_to_db()
        self._create_table(engine, table_name)
        self._insert_into_table(engine, table_name, scenario_name, dmg_tuple)

    @staticmethod
    def _create_table(engine: Engine, table_name: str) -> None:
        """
        Creates the table
        :param engine: SQLAlchemy Engine
        :param table_name:  Table name
        :return: None
        """
        logging.info(f'Creating {table_name} table...')

        query = """
        CREATE TABLE IF NOT EXISTS {table_name} 
        (
            Scenario      VARCHAR not null
                primary key,
            AverageDamage FLOAT
        );
        """.format(table_name=table_name)
        try:
            with engine.connect() as conn:
                conn.execute(text(query))
                conn.commit()
                conn.close()
        except Exception as e:
            print(e)
            conn.rollback()

    @staticmethod
    def _insert_into_table(
            engine: Engine, table_name: str, character_name: str, dmg_tuple: tuple[float, int, int]
    ) -> None:
        """
        Inserts the data to the table
        :param engine: SQLAlchemy Engine
        :param table_name:  Table name
        :param character_name: Character name
        :param dmg_tuple: Tuple of Damage
        :return: None
        """
        logging.info(f'Inserting data into {table_name} table...')

        query = """
        INSERT OR REPLACE INTO {table_name} 
        (Scenario, AverageDamage) 
        VALUES (:Scenario, :AverageDamage)
        """.format(table_name=table_name)

        params = {
            'Scenario': character_name,
            'AverageDamage': dmg_tuple[0]
        }

        try:
            with engine.connect() as conn:
                conn.execute(text(query), params)
                conn.commit()
                conn.close()
        except Exception as e:
            print(e)
            conn.rollback()


if __name__ == '__main__':
    pass
