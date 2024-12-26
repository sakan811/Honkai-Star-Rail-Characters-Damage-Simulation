from sqlalchemy.engine import Engine
from hsr_simulation.postgre import PostgresConnection

def test_postgres_connection_url():
    """Test PostgreSQL connection URL generation"""
    conn = PostgresConnection()
    expected_url = "postgresql://postgres:postgres@localhost:5454/postgres"
    assert conn.url == expected_url

def test_get_engine():
    """Test engine creation"""
    conn = PostgresConnection()
    engine = conn.get_engine()
    assert isinstance(engine, Engine) 