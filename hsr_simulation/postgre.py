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
from functools import wraps
from typing import Callable

import pandas as pd
import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import sqlalchemy.exc

from hsr_simulation.configure_logging import main_logger

load_dotenv()


def db_error_handler(func: Callable) -> Callable:
    """Decorator to handle database operation errors"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            return func(*args, **kwargs)
        except sqlalchemy.exc.OperationalError as e:
            main_logger.error("OperationalError")
            main_logger.error(e, exc_info=True)
            if conn is not None:
                conn.rollback()
                conn.close()
        except Exception as e:
            main_logger.error(f"Unexpected error: {str(e)}")
            main_logger.error(e, exc_info=True)
            if conn is not None:
                conn.rollback()
                conn.close()

    return wrapper


class PostgresConnection:
    """Base class for PostgreSQL database operations"""

    def __init__(self):
        self.url = self._get_db_url()

    def _get_db_url(self) -> str:
        """Get PostgreSQL connection URL from environment variables"""
        main_logger.info("Getting PostgreSQL connection URL...")

        db_params = {
            "dbname": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT"),
        }

        return (
            f"postgresql://{db_params['user']}:{db_params['password']}"
            f"@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"
        )

    def get_engine(self) -> sqlalchemy.engine.Engine:
        """Create and return a SQLAlchemy engine"""
        return create_engine(self.url)

    @db_error_handler
    def execute_query(self, query: str) -> None:
        """Execute a SQL query"""
        with self.get_engine().connect() as conn:
            conn.execute(text(query))
            conn.commit()


class PostgresOperations(PostgresConnection):
    """Class for PostgreSQL specific operations"""

    def __init__(self):
        super().__init__()

    @db_error_handler
    def drop_stage_table(self, table_name: str) -> None:
        """Drop a stage table in the database"""
        main_logger.info(f"Dropping table {table_name}...")
        query = f'DROP TABLE IF EXISTS public."{table_name}" CASCADE;'
        self.execute_query(query)

    @db_error_handler
    def drop_view(self, view_name: str) -> None:
        """Drop a view in the database"""
        main_logger.info(f"Dropping view {view_name}...")
        query = f'DROP VIEW IF EXISTS public."{view_name}" CASCADE;'
        self.execute_query(query)

    @db_error_handler
    def create_view(self, view_name: str, query: str) -> None:
        """Create a view in the database"""
        main_logger.info(f"Creating view {view_name}...")
        self.execute_query(query)

    @db_error_handler
    def load_dataframe(self, df: pd.DataFrame, table_name: str) -> None:
        """Load a DataFrame to a stage table"""
        main_logger.info(f"Loading dataframe to {table_name}...")
        with self.get_engine().connect() as conn:
            df.to_sql(table_name, conn, if_exists="append", index=False)


def generate_dmg_view_query(view_name: str, stage_table_name: str) -> str:
    """Generate SQL query for damage view"""
    return f'''
    CREATE OR REPLACE VIEW public."{view_name}" AS
    WITH DMGbyRound AS (
        SELECT "Character", 
               SUM("DMG") AS "AvgDMGbyRound", 
               "DMG_Type",
               "Simulate Round No."
        FROM public."{stage_table_name}"
        GROUP BY "Character", "Simulate Round No.", "DMG_Type"
        ORDER BY "Character"
    )
    SELECT "Character", AVG("AvgDMGbyRound") AS "AvgDMG", "DMG_Type"
    FROM DMGbyRound
    GROUP BY "Character", "DMG_Type"
    ORDER BY "Character"
    '''


def load_df_to_stage_table(df: pd.DataFrame, stage_table_name: str) -> None:
    """Legacy function for loading DataFrame"""
    db = PostgresOperations()
    db.load_dataframe(df, stage_table_name)
