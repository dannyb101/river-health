from flask import Blueprint, request
from app.models.nrfa_csv import NRFA_CSV
import json
from app.Connections import db_nrfa
import os, ssl
from app.utils.data_utils import convert_m3_to_l
import datetime

# WARNING: When testing the application on a Mac computer, the controller methods
# in this class threw SSL: CERTIFICATE_VERIFY_FAILED errors. This was as a result
# of server certificate validation being added by default, in version 2.7.9 of python.
# The following if statement turns this off in the environment variables. This provides
# a temporary fix to the problem but should be replaced.
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

nrfa = Blueprint('nrfa', __name__)

# Rest controller to get JSON of mean flow and s.d. flow of river
@nrfa.route('/nrfa/mean_and_sd_flow', methods=['GET'])
def get_mean_and_sd():

    station_id = request.args.get('station_id')
    num_years = float(request.args.get('num_years'))

    # URL to get same csv as in test files (example-nrfa-data.csv):ß
    # https://nrfaapps.ceh.ac.uk/nrfa/ws/time-series?format=nrfa-csv&data-type=gdf&station=56001

    base_url = "https://nrfaapps.ceh.ac.uk/nrfa/ws/"
    query_web_service = "time-series"
    query_format = "?format=nrfa-csv"
    query_data_type = "&data-type=gdf"
    query_station = "&station=" + station_id
    days_in_year = 365.25
    start_date = (datetime.datetime.now() - datetime.timedelta(days=(num_years*days_in_year))).strftime("%Y-%m-%d")
    # query always returns flow data from 10 years ago to present
    query_start_date = "&start-date=" + start_date
    url = base_url + query_web_service + query_format + query_data_type + query_station + query_start_date

    # Leverage NRFA_CSV class
    nrfa_csv = NRFA_CSV(url)
    
    # Convert units from m^3/s to l/s
    river_flow_ls = convert_m3_to_l(nrfa_csv.mean)
    river_flow_ls_sd = convert_m3_to_l(nrfa_csv.standard_deviation)
    
    return json.dumps({'river_flow_ls' : river_flow_ls, 'river_flow_ls_sd' : river_flow_ls_sd})


@nrfa.route('/nrfa/add', methods=['POST'])
def post_station_info_from_nrfa():

    connection_nrfa = db_nrfa.DB_NRFA()
    connection_nrfa.populate_nrfa_table()

    return ""
