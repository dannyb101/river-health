import pytest
from app.Connections.db_water_body_type import DB_WATER_BODY_TYPE

# Create session persistent Database connection
@pytest.fixture(scope='session')
def connection():
    return DB_WATER_BODY_TYPE()

def test_retrieve_water_body_id(connection):
    """
    GIVEN a water body type
    WHEN the database is called
    THEN return the correct water body id
    """
    id = connection.retrieve_water_body_id(water_body_type= '1_2_4_6')
    assert id == 1

def test_retrieve_water_body_type(connection):
    """
    GIVEN a water body id
    WHEN the database is called
    THEN return the correct water body type
    """
    type = connection.retrieve_water_body_type(water_body_id= 2)
    assert type == '3_5_7'