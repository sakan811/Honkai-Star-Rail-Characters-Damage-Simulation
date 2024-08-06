import os

import pandas as pd
import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from hsr_simulation.configure_logging import main_logger


load_dotenv()


def get_db_postgre_url() -> str:
    """
    Get a PostgreSQL connection URL from environment variables.
    :return: PostgreSQL connection URL
    """
    main_logger.info('Getting PostgreSQL connection URL...')

    db_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': 'postgres',
        'password': os.getenv('DB_PASSWORD'),
        'host': 'localhost',
        'port': '5432'
    }

    # Format the PostgreSQL connection URL
    url = (
        f"postgresql://{db_params['user']}:{db_params['password']}"
        f"@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"
    )

    return url


def drop_stage_table(postgres_url: str, stage_table_name: str):
    """
    Drop a stage table in the database
    :param postgres_url: Postgres URL
    :param stage_table_name: Stage table name
    :return: None
    """
    main_logger.info(f'Dropping view {stage_table_name}...')
    engine = create_engine(postgres_url)
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS public.\"{stage_table_name}\" CASCADE;"))
        conn.commit()


def load_df_to_stage_table(
        df: pd.DataFrame,
        engine: sqlalchemy.engine,
        stage_table_name: str) -> None:
    """
    Load a dataframe to a stage table in the database
    :param df: Dataframe
    :param engine: SQLAlchemy engine
    :param stage_table_name: Stage table name
    :return: None
    """
    main_logger.info(f'Loading dataframe to {stage_table_name}...')
    with engine.connect() as conn:
        df.to_sql(stage_table_name, conn, if_exists='append', index=False)


def create_view(postgres_url: str,
                view_name: str,
                stage_table_name: str) -> None:
    """
    Create a view in the database.
    :param postgres_url: Postgres database URL.
    :param view_name: View name.
    :param stage_table_name: Stage table name.
    :return: None
    """
    main_logger.info(f'Creating view {view_name}...')
    engine = create_engine(postgres_url)
    with engine.connect() as conn:
        query = f'''
        CREATE OR REPLACE VIEW public.\"{view_name}\" as
        with DMGbyRound as (
            select  "Character", 
                    sum("DMG") as "AvgDMGbyRound", 
                    "DMG_Type",
                    "Simulate Round No."
            from public.\"{stage_table_name}\"
            group by "Character", "Simulate Round No.", "DMG_Type"
            order by "Character"
        ) 
        select "Character", avg("AvgDMGbyRound") as "AvgDMG", "DMG_Type"
        from DMGbyRound
        group by "Character", "DMG_Type"
        order by "Character"
        '''
        conn.execute(text(query))
        conn.commit()


def drop_view(postgres_url: str, view_name: str) -> None:
    """
    Drop a view in the database
    :param postgres_url: Postgres URL
    :param view_name: View name
    :return: None
    """
    main_logger.info(f'Dropping view {view_name}...')
    engine = create_engine(postgres_url)
    with engine.connect() as conn:
        conn.execute(text(f"DROP VIEW IF EXISTS public.\"{view_name}\" CASCADE;"))
        conn.commit()
