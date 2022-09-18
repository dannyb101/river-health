import math
import pandas as pd
import numpy as np
import urllib.request
import json
import re


def convert_cso_csv_to_df(file_path):

    df = pd.read_csv(file_path, dtype=str)

    df.columns = df.columns.str.lower()

    # remove seconds column and additional headers if present
    if "seconds" in df.columns:
        df.drop("seconds", axis=1, inplace=True)

    # if first cell is empty or does not contain a date of format dd/mm/yyyy then row is deleted
    while not bool(re.search(r'(\d{2}\/\d{2}\/\d{4})', str(df.iloc[0, 0]))):
        df.drop(index=df.index[0], axis=0, inplace=True)

    # rename columns
    columns = ["time"]
    for i in range(1, len(df.columns)):
        columns.append("sum_cso_flow_m3/s_" + str(i))
    df.set_axis(columns, axis=1, inplace=True)

    # convert columns except time to float
    types_dict = {key: np.float64 for key in columns[1:]}
    for col, col_type in types_dict.items():
        df[col] = df[col].astype(col_type)

    return df


def sum_df_over_hour(df):
    """
    convert dataframe from flow rate (m3/s) per 5 mins
    to volume (l) per hour
    """
    if len(df.iloc[0, 0].split()[-1]) > 5:
        date_format = "%d/%m/%Y %H:%M:%S"
    else:
        date_format = "%d/%m/%Y %H:%M"
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], format=date_format)
    df.set_index(df.columns[0], inplace=True)

    # remove negative cso flow rates
    df[df < 0] = 0

    # sum flow rate over the hour
    df = df.resample("H").sum(min_count=1)

    # volume = flow rate x time
    seconds_in_5_min_sample = 5 * 60
    df = df.applymap(lambda x: convert_m3_to_l(x * seconds_in_5_min_sample))
    df.rename(lambda x: "cso_vol_l_" + x.split("_")[-1], axis=1, inplace=True)

    return df


"""
Function takes the dataframe created from create_outputs_dataframe() as input,
returns a dictionary of bod_99_percentile and nh3_99_percentile
"""


def ninety_ninth_percentile(dataframe):

    pre_spill_bod_series = dataframe["upstream_bod_mg/l"]
    pre_spill_nh3_series = dataframe["upstream_nh3_mg/l"]

    post_spill_bod_series = dataframe["mix_bod_mg/l"]
    post_spill_nh3_series = dataframe["mix_nh3_mg/l"]

    pre_spill_bod_99_percentile = np.percentile(pre_spill_bod_series, 99)
    pre_spill_nh3_99_percentile = np.percentile(pre_spill_nh3_series, 99)

    post_spill_bod_99_percentile = np.percentile(post_spill_bod_series, 99)
    post_spill_nh3_99_percentile = np.percentile(post_spill_nh3_series, 99)

    return {
        "pre_spill_bod_99_percentile": pre_spill_bod_99_percentile,
        "pre_spill_nh3_99_percentile": pre_spill_nh3_99_percentile,
        "post_spill_bod_99_percentile": post_spill_bod_99_percentile,
        "post_spill_nh3_99_percentile": post_spill_nh3_99_percentile,
    }


def convert_m3_to_l(volume):
    return volume * 1000


def convert_mg_to_kg(mass):
    return mass / 1000000


def convert_kg_to_mg(mass):
    return mass * 1000000


def excel_file_to_river_stretch_names(file_path):

    return sorted(
        pd.read_excel(file_path, sheet_name="Rivers and Canals")["WB name"].tolist()
    )


"""
Function that scrapes NRFA for river data
"""


def scrape_nrfa():

    base_url = "https://nrfaapps.ceh.ac.uk/nrfa/ws"
    query = "station=*&format=json-object&fields=id,name"
    station_info_url = "{BASE}/station-info?{QUERY}".format(BASE=base_url, QUERY=query)
    response = urllib.request.urlopen(station_info_url).read()
    response = json.loads(response)

    station_info_list = []

    for i in response["data"]:
        station_info_list.append((i["id"], i["name"]))

    return station_info_list


def calculate_mixed_mean_sd(dataframe):
    """
    Calculates the mean and sd of the mixed columns (flow, bod, ammonia)
    """
    mean_mixed_flow = dataframe["mix_flow_l/s"].mean()
    sd_mixed_flow = dataframe["mix_flow_l/s"].std()
    mean_mixed_bod = dataframe["mix_bod_mg/l"].mean()
    sd_mixed_bod = dataframe["mix_bod_mg/l"].std()
    mean_mixed_nh3 = dataframe["mix_nh3_mg/l"].mean()
    sd_mixed_nh3 = dataframe["mix_nh3_mg/l"].std()

    return (
        mean_mixed_flow,
        sd_mixed_flow,
        mean_mixed_bod,
        sd_mixed_bod,
        mean_mixed_nh3,
        sd_mixed_nh3,
    )


def calculate_soaf_impact_class(impact_score):
    if impact_score <= 5:
        return "No Impact"
    elif impact_score <= 9:
        return "Very Low"
    elif impact_score <= 19:
        return "Low"
    elif impact_score <= 29:
        return "Moderate"
    elif impact_score <= 39:
        return "High"
    else:
        return "Severe"
