from sqlalchemy import create_engine, Engine, text

def connect_to_db():
    engine = create_engine('sqlite:///hsr_dmg_calculation.db', echo=True)

    return engine


def create_table(engine: Engine, table_name: str) -> None:
    query = """
    CREATE TABLE IF NOT EXISTS {table_name} 
    (
        character      VARCHAR not null
            primary key,
        average_damage FLOAT,
        min_damage     FLOAT,
        max_damage     FLOAT
    );
    """.format(table_name=table_name)
    try:
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()
            conn.close()
    except Exception as e:
        conn.rollback()


def migrate_to_sqlite(character: tuple[float, int, int], character_name: str, table_name: str) -> None:
    """
    Migrate character data to SQLite table.
    :param character_name: Character name
    :param character: Character data as Tuple
    :param table_name: Table name
    :return: None
    """
    engine = connect_to_db()
    create_table(engine, table_name)

    query = """
    INSERT OR REPLACE INTO {table_name} 
    (character, average_damage, min_damage, max_damage) 
    VALUES (:character, :average_damage, :min_damage, :max_damage)
    """.format(table_name=table_name)

    params = {
        'character': character_name,
        'average_damage': character[0],
        'min_damage': character[1],
        'max_damage': character[2]
    }

    try:
        with engine.connect() as conn:
            conn.execute(text(query), params)
            conn.commit()
            conn.close()
    except Exception as e:
        conn.rollback()


class CharacterTable:
    def __init__(self):
        pass

    def migrate_to_character_table(self, table_name: str, character_name: str, dmg_tuple: tuple[float, int, int]):
        engine = connect_to_db()
        self._create_table(engine, table_name)
        self._insert_into_table(engine, table_name, character_name, dmg_tuple)

    @staticmethod
    def _create_table(engine: Engine, table_name: str) -> None:
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
    def _insert_into_table(engine, table_name, character_name, dmg):
        query = """
        INSERT OR REPLACE INTO {table_name} 
        (character, average_damage) 
        VALUES (:character, :average_damage)
        """.format(table_name=table_name)

        params = {
            'character': character_name,
            'average_damage': dmg[0]
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
