import pytest
from app.Connections.db_archive import DB_ARCHIVE

# Create session persistent Database connection
@pytest.fixture(scope='session')
def connection():
    return DB_ARCHIVE()

@pytest.fixture(scope='session')
def recent_id(connection):
    return connection.get_most_recent_id()

@pytest.mark.skip(reason="Flaky test")
def test_db_archive_columns(connection):
    """
    GIVEN a database archive connection
    WHEN the database is called
    THEN check that all columns are returned
    """
    all_archive_row = connection.get_all_archive_results()
    list_of_archive_columns= list(all_archive_row[0].keys())
    assert list_of_archive_columns == ['id', 'created','name_of_simulation','username', 'river_stretch_id', 'standards_id', 'cso_id', 'water_body_id', 'qube_csv']

def test_get_most_recent_id(connection, recent_id):
    """
    GIVEN a database archive connection
    WHEN the get_most_recent_id method is called
    THEN check that the most recent id is a uuid 
    """
    if recent_id == 0:
        assert recent_id == 0
    else:
        assert len(recent_id) == 36
        assert type(recent_id) == str

def test_get_archive_by_id(connection, recent_id):
    """
    GIVEN a database archive connection
    WHEN the get_archive_by_id method is called
    THEN check that the correct row is returned
    """
    if recent_id == 0:
        assert recent_id == 0
    else:
        archive_by_id = connection.get_archive_by_id(recent_id)
        assert archive_by_id[0]['id'] == recent_id

def test_check_id_exists(connection):
    """
    GIVEN a database archive connection
    WHEN the check_id_exists method is called with an improper id
    THEN check_id_exists method returns None
    """
    false_id = 'This Will Not Work'
    assert connection.check_id_exists(false_id) == None
