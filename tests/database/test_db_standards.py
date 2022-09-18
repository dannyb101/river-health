import pytest
from app.Connections.db_standards import DB_WFD_STANDARDS


@pytest.fixture(scope="session")
def connection_standards():
    return DB_WFD_STANDARDS()

def test_num_standards(connection_standards):
    """
    GIVEN a DB_WFD_STANDARDS object
    WHEN get_all_standards is called
    THEN assert that the number of entries in the standards table is 16
    """
    assert len(connection_standards.get_all_standards()) == 16

def test_get_standard(connection_standards):
    """
    GIVEN A DB_WFD_STANDARDS object
    WHEN get_all_standards is called
    THEN assert that the river type, standard and pollutant are correct
    """
    standards = connection_standards.get_all_standards()
    for standard in standards:
        assert standard[0] in ["1_2_4_6", "3_5_7"]
        assert standard[1] in ["bod", "nh3"]
        assert standard[2] in ["high", "good", "moderate", "poor"]

