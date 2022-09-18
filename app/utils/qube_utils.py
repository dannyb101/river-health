import pandas

"""
Function takes in standard Qube data and returns: Mean of the Daily Flow
Rounded to 4 Decimal places
"""
def calculate_Qube_mean(filepath_to_csv):
    column_names = ["Date", "Mean Daily Flow"]
    dataframe = pandas.read_csv(filepath_to_csv, header=0, names=column_names)
    dataframe["Mean Daily Flow"] = pandas.to_numeric(dataframe["Mean Daily Flow"])
    return round(dataframe["Mean Daily Flow"].mean(), 4)

"""
Function takes in standard Qube data and returns: Standard Deviation of the Daily Flow
Rounded to 4 Decimal places
"""
def calculate_Qube_standard_deviation(filepath_to_csv):
    column_names = ["Date", "Mean Daily Flow"]
    dataframe = pandas.read_csv(filepath_to_csv, header=0, names=column_names)
    dataframe["Mean Daily Flow"] = pandas.to_numeric(dataframe["Mean Daily Flow"])
    return round(dataframe["Mean Daily Flow"].std(), 4)


    