import pandas as pandas
import datetime


class NRFA_CSV:
    """
    Initialise the class with a CSV file
    Station Properties Include: ID, Name, Grid reference, First Date Measured, Last Date Measured, CSV Download Date
    Calculated Properties Include: Mean and Standard Deviation of River Flow from date of first measurement to now
    """
    def __init__(self, url):
        dataframe = pandas.read_csv(url)

        # To make Indexing quicker drop all river flow values and keep metadata
        metadata_dataframe = dataframe.dropna()

        # Download date is stored as a column header so get this detail first
        self.file_downloaded = self.convert_file_downloaded_time(metadata_dataframe.columns.values[2])

        # Rename Metadata column headers and index the rows
        column_names = ["Group", "Unique_id", "Value"]
        metadata_dataframe.columns = column_names
        metadata_dataframe = metadata_dataframe.set_index(["Group", "Unique_id"])

        # Initialise Station: ID, Name, Grid Reference, First and Last Date Measured
        self.station_id = metadata_dataframe.at[("station", "id"), "Value"]
        self.name = metadata_dataframe.at[("station", "name"), "Value"]
        self.grid_reference = metadata_dataframe.at[("station", "gridReference"), "Value"]
        self.first_date_measured = self.convert_date_measured_time(metadata_dataframe.at[("data", "first"), "Value"])
        self.last_date_measured = self.convert_date_measured_time(metadata_dataframe.at[("data", "last"), "Value"])

        # Create a new dataframe with all the Metadata dropped
        rows = len(metadata_dataframe.index)
        clean_dataframe = self.clean_dataframe(dataframe, rows)

        # Initialise River Flow: Mean and Standard Deviation
        self.mean = self.calculate_mean(clean_dataframe)
        self.standard_deviation = self.calculate_standard_deviation(clean_dataframe)

    """
    Function to convert the Date Measured metadata into a more readable format
    """
    def convert_date_measured_time(self, date_measured):
        return datetime.datetime.strptime(date_measured, "%Y-%m-%d").strftime("%d/%m/%Y")
    
    """
    Function to convert the CSV download time into a more readable format
    """
    def convert_file_downloaded_time(self, file_downloaded):
        return datetime.datetime.strptime(file_downloaded, "%Y-%m-%dT%H:%M:%S").date().strftime("%d/%m/%Y")

    """
    Function to clean dataframe to make it easier to do Mean and Standard Deviation calculations
    """
    def clean_dataframe(self, dataframe, rows):
        dataframe.drop(index=dataframe.index[:rows], axis=0, inplace=True)
        dataframe.drop(dataframe.columns[2], axis=1, inplace=True)
        dataframe.columns = ["Date", "Mean Daily Flow"]
        dataframe["Mean Daily Flow"] = pandas.to_numeric(dataframe["Mean Daily Flow"])
        return dataframe

    """
    Function which takes in cleaned dataframe (use clean_dataframe function) to calculate Mean
    """
    def calculate_mean(self, dataframe):
        return round(dataframe["Mean Daily Flow"].mean(), 4)
    
    """
    Function which takes in cleaned dataframe (use clean_dataframe function) to calculate Mean
    """
    def calculate_standard_deviation(self, dataframe):
        return round(dataframe["Mean Daily Flow"].std(), 4)

