from app.models.nrfa_csv import NRFA_CSV

# Testing two files as CSV's downloaded from the NRFA website have different formats
# this ensures that NRFA_CSV class is flexible
NRFA_1 = NRFA_CSV("./tests/files/example-nrfa-data.csv")
NRFA_2 = NRFA_CSV("./tests/files/example2-nrfa-data.csv")

# USING NRFA_1
def test_NRFA_1_mean():
    # Value calculated by importing CSV to Excel and using Average Function
    assert NRFA_1.mean == [28.989]

def test_NRFA_1_standard_deviation():
    # Value calculated by importing CSV to Excel and using STDEV Function
    assert NRFA_1.standard_deviation == [35.9042]

def test_NRFA_1_metadata():
    assert NRFA_1.name == "Usk at Chainbridge"
    assert NRFA_1.station_id == "56001"
    assert NRFA_1.grid_reference == "SO3460605591"
    assert NRFA_1.first_date_measured == "01/03/1957"
    assert NRFA_1.last_date_measured == "30/09/2021"
    assert NRFA_1.file_downloaded == "26/07/2022"

    # USING NRFA_2
def test_NRFA_2_mean():
    # Value calculated by importing CSV to Excel and using Average Function
    assert NRFA_2.mean == [2.9286]

def test_NRFA_2_standard_deviation():
    # Value calculated by importing CSV to Excel and using STDEV Function
    assert NRFA_2.standard_deviation == [3.4733]

def test_NRFA_2_metadata():
    assert NRFA_2.name == "Loch Ailsh at Loch Ailsh"
    assert NRFA_2.station_id == "3006"
    assert NRFA_2.grid_reference == "NC3157710138"
    assert NRFA_2.first_date_measured == "01/01/2006"
    assert NRFA_2.last_date_measured == "30/09/2021"
    assert NRFA_2.file_downloaded == "26/07/2022"