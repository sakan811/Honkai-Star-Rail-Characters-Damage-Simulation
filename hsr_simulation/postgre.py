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
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT')
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
    try:
        engine = create_engine(postgres_url)
        with engine.connect() as conn:
            conn.execute(text(f"DROP TABLE IF EXISTS public.\"{stage_table_name}\" CASCADE;"))
            conn.commit()
    except sqlalchemy.OperationalError as e:
        main_logger.error('OperationalError')
        main_logger.error(e, exc_info=True)
        conn.rollback()
        conn.close()


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
    try:
        with engine.connect() as conn:
            df.to_sql(stage_table_name, conn, if_exists='append', index=False)
    except sqlalchemy.OperationalError as e:
        main_logger.error('OperationalError')
        main_logger.error(e, exc_info=True)
        conn.rollback()
        conn.close()


def generate_dmg_view_query(view_name: str, stage_table_name: str) -> str:
    """
    Generate an SQL query to create or replace a view summarizing damage data.

    :param view_name: The name of the view to be created or replaced.
    :param stage_table_name: The name of the stage table used in the query.
    :return: The constructed SQL query as a string.
    """
    return f'''
    CREATE OR REPLACE VIEW public.\"{view_name}\" AS
    WITH DMGbyRound AS (
        SELECT "Character", 
               SUM("DMG") AS "AvgDMGbyRound", 
               "DMG_Type",
               "Simulate Round No."
        FROM public.\"{stage_table_name}\"
        GROUP BY "Character", "Simulate Round No.", "DMG_Type"
        ORDER BY "Character"
    )
    SELECT "Character", AVG("AvgDMGbyRound") AS "AvgDMG", "DMG_Type"
    FROM DMGbyRound
    GROUP BY "Character", "DMG_Type"
    ORDER BY "Character"
    '''


def create_view(postgres_url: str,
                view_name: str,
                query: str) -> None:
    """
    Create a view in the database.
    :param postgres_url: Postgres database URL.
    :param view_name: View name.
    :param query: Query to create the view.
    :return: None
    """
    main_logger.info(f'Creating view {view_name}...')
    try:
        engine = create_engine(postgres_url)
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()
    except sqlalchemy.OperationalError as e:
        main_logger.error('OperationalError')
        main_logger.error(e, exc_info=True)
        conn.rollback()
        conn.close()


def drop_view(postgres_url: str, view_name: str) -> None:
    """
    Drop a view in the database
    :param postgres_url: Postgres URL
    :param view_name: View name
    :return: None
    """
    main_logger.info(f'Dropping view {view_name}...')
    try:
        engine = create_engine(postgres_url)
        with engine.connect() as conn:
            conn.execute(text(f"DROP VIEW IF EXISTS public.\"{view_name}\" CASCADE;"))
            conn.commit()
    except sqlalchemy.OperationalError as e:
        main_logger.error('OperationalError')
        main_logger.error(e, exc_info=True)
        conn.rollback()
        conn.close()
