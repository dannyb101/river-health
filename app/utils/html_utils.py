import pandas as pd
"""
Style dataframe into more human readable format
Removes Index from Time to allow it to become a column header
"""
def dataframe_to_html_table(dataframe):
    # Remove all rows where the flow is less than or equal zero (CSO not overflowing during that period)
    dataframe = dataframe[dataframe['cso_vol_l'] > 0]
    dataframe['time'] = pd.to_datetime(dataframe['time'], format='%Y-%m-%d %H:%M:%S')
    dataframe['time'] = dataframe['time'].dt.strftime('%-I%p - %d/%m/%Y')

    # Rename columns to match current UPM output
    dataframe.columns = [['','','Total Spill Discharge','Total Spill Discharge','Total Spill Discharge','Upstream River','Upstream River','Upstream River','Initial Mixed River','Initial Mixed River','Initial Mixed River'],
    ['Event Date & Time','Simulation ID','Vol (l)','BOD (kg)','NH3 (kg)','Flow (l/s)','BOD (mg/l)','NH3 (mg/l)','Flow (l/s)','BOD (mg/l)','NH3 (mg/l)']]

    dataframe['Total Spill Discharge', 'Vol (l)'] = dataframe['Total Spill Discharge', 'Vol (l)'].apply(lambda x: int(x))

    # Convert Dataframe to HTML
    return [dataframe.to_html(classes='data', header="true", index= False, float_format=lambda x: '%.3f' % x)]


# """
# Convert dataframe into csv
# The user will be able to download output in csv format
# """
# def dataframe_to_excel(dataframe):
#     dataframe = dataframe.reset_index()

#     # Remove all rows where the flow is less than or equal zero (CSO not overflowing during that period)
#     dataframe = dataframe[dataframe['cso_vol_l'] > 0]   

#     # Rename columns to match current UPM output
#     dataframe.columns = [['','','Total Spill Discharge','Total Spill Discharge','Total Spill Discharge','Upstream River','Upstream River','Upstream River','Initial Mixed River','Initial Mixed River','Initial Mixed River'],
#     ['Event Date & Time','Simulation ID','Vol (l)','BOD (kg)','NH3 (kg)','Flow (l/s)','BOD (mg/l)','NH3 (mg/l)','Flow (l/s)','BOD (mg/l)','NH3 (mg/l)']]

#     # Convert Dataframe to csv
#     dataframe.to_csv("app/static/downloads/output_data.csv", index= False)





    
