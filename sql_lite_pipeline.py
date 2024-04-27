from sqlalchemy import create_engine, Engine, text


def connect_to_db() -> Engine:
    """
    Connects to the SQLite database
    :return: SQLAlchemy Engine
    """
    engine = create_engine('sqlite:///hsr_dmg_calculation.db', echo=True)

    return engine


class CharacterTable:
    def __init__(self):
        pass

    def migrate_to_character_table(
            self, table_name: str, character_name: str, dmg_tuple: tuple[float, int, int]
    ) -> None:
        """
        Migrates data to the given character table.
        :param table_name:  Table name
        :param character_name: Character name
        :param dmg_tuple: Tuple of Damage
        :return: None
        """
        engine = connect_to_db()
        self._create_table(engine, table_name)
        self._insert_into_table(engine, table_name, character_name, dmg_tuple)

    @staticmethod
    def _create_table(engine: Engine, table_name: str) -> None:
        """
        Creates the table
        :param engine: SQLAlchemy Engine
        :param table_name:  Table name
        :return: None
        """
        query = """
        CREATE TABLE IF NOT EXISTS {table_name} 
        (
            character      VARCHAR not null
                primary key,
            average_damage FLOAT
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
        query = """
        INSERT OR REPLACE INTO {table_name} 
        (character, average_damage) 
        VALUES (:character, :average_damage)
        """.format(table_name=table_name)

        params = {
            'character': character_name,
            'average_damage': dmg_tuple[0]
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
