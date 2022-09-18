import pytest
from app.Connections.db_connect import DB_CONNECT

# Create session persistent Database connection
@pytest.fixture(scope='session')
def connection():
    return DB_CONNECT()

# Check Connection by getting all current tables
# PLEASE Note: Tables are subject to change, therefore assert statement may also need to be changed
def test_retrieve_all_tables(connection):
    assert (('archive',), ('cso_inputs',), ('nrfa',), ('results',),('river_types',), ('serialised_inputs',), ('standards',), ('standards_update',), ('stretch_name',), ('users',), ('variables',), ('water_body_type',),) == connection.show_all_tables()