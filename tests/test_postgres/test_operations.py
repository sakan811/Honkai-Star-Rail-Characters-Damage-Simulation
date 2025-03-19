import pytest
import pandas as pd
from sqlalchemy import text
from hsr_simulation.postgre import PostgresOperations


@pytest.fixture
def db():
    return PostgresOperations()


@pytest.fixture
def sample_df():
    return pd.DataFrame({"Character": ["Test1", "Test2"], "DMG": [100, 200]})


@pytest.fixture(autouse=True)
def cleanup_tables(db):
    """Cleanup tables before and after each test"""
    # Cleanup before test
    db.execute_query("DROP TABLE IF EXISTS test_table CASCADE")
    db.execute_query("DROP VIEW IF EXISTS test_view CASCADE")

    yield

    # Cleanup after test
    db.execute_query("DROP TABLE IF EXISTS test_table CASCADE")
    db.execute_query("DROP VIEW IF EXISTS test_view CASCADE")


def test_table_operations(db, sample_df):
    """Test table creation and dropping"""
    table_name = "test_table"

    # Test loading dataframe
    db.load_dataframe(sample_df, table_name)

    # Verify data was loaded
    with db.get_engine().connect() as conn:
        result = conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}"')).scalar()
        assert result == 2

        # Verify actual data
        rows = (
            conn.execute(text(f'SELECT * FROM "{table_name}" ORDER BY "Character"'))
            .mappings()
            .all()
        )
        assert len(rows) == 2
        assert rows[0]["Character"] == "Test1"
        assert rows[0]["DMG"] == 100

    # Test dropping table
    db.drop_stage_table(table_name)

    # Verify table was dropped
    with db.get_engine().connect() as conn:
        result = conn.execute(
            text("SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = :name)"),
            {"name": table_name},
        ).scalar()
        assert not result


def test_view_operations(db, sample_df):
    """Test view creation and dropping"""
    table_name = "test_table"
    view_name = "test_view"

    # Setup test data
    db.load_dataframe(sample_df, table_name)

    # Create view
    query = f'''
    CREATE OR REPLACE VIEW public."{view_name}" AS 
    SELECT * FROM public."{table_name}"
    '''
    db.create_view(view_name, query)

    # Verify view exists and data
    with db.get_engine().connect() as conn:
        # Check view exists
        result = conn.execute(
            text("SELECT EXISTS (SELECT FROM pg_views WHERE viewname = :name)"),
            {"name": view_name},
        ).scalar()
        assert result

        # Verify view data
        rows = (
            conn.execute(text(f'SELECT * FROM "{view_name}" ORDER BY "Character"'))
            .mappings()
            .all()
        )
        assert len(rows) == 2
        assert rows[0]["Character"] == "Test1"
        assert rows[0]["DMG"] == 100

    # Drop view
    db.drop_view(view_name)

    # Verify view was dropped
    with db.get_engine().connect() as conn:
        result = conn.execute(
            text("SELECT EXISTS (SELECT FROM pg_views WHERE viewname = :name)"),
            {"name": view_name},
        ).scalar()
        assert not result

    # Cleanup
    db.drop_stage_table(table_name)
