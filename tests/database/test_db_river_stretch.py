import pytest
from app.Connections.db_river_stretch import DB_RIVER_STRETCH

# Create session persistent Database connection
@pytest.fixture(scope='session')
def connection():
    return DB_RIVER_STRETCH()

def test_retrieve_river_stretch_id(connection):
    """
    GIVEN a river stretch name
    WHEN the database is called
    THEN retrieve the correct id
    """
    id = connection.retrieve_river_stretch_id(river_name='Aber')
    assert id == 1


def test_retrieve_river_stretch_name(connection):
    """
    GIVEN a river stretch id
    WHEN the database is called
    THEN retrieve the correct name
    """
    name = connection.retrieve_river_stretch_name(river_stretch_id = '1')
    assert name == 'Aber'