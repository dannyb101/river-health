import pytest
from app.Connections.db_nrfa import DB_NRFA

# Create session persistent Database connection
@pytest.fixture(scope='session')
def connection():
    return DB_NRFA()

def test_retrieve_all_station_info(connection):
    """
    GIVEN a nrfa station name
    WHEN the database is called
    THEN retrieve one valid nrfa station name
    """

    first_nrfa_station_name = connection.retrieve_all_station_info()[0]['station_name']
    assert first_nrfa_station_name == 'Wick at Tarroul'
