from app.utils.qube_utils import calculate_Qube_mean, calculate_Qube_standard_deviation

def test_Qube_mean():
    file_path = "./tests/files/example-Qube-data.csv"
    mean = calculate_Qube_mean(file_path)

    # Value calculated by importing CSV to Excel and using Average Function
    assert mean == [27.9541]

def test_Qube_standard_deviation():
    file_path = "./tests/files/example-Qube-data.csv"
    standard_deviation = calculate_Qube_standard_deviation(file_path)

    # Value calculated by importing CSV to Excel and using STDEV Function
    assert standard_deviation == [30.8332]