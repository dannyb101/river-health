import datetime
from distutils.sysconfig import customize_compiler
import uuid
import pandas as pd
from flask import Blueprint, render_template, request

from app.utils import data_utils, graphs
from app.utils.WFD_standards import WFD_Standards
from app.views.outputs import outputs_route
from app.models.waterbodies import River, Cso
import app.models.waterbodies as wb
from app.Connections import db_river_stretch, db_nrfa, db_serialised_inputs, db_standards, db_archive, db_variables, db_water_body_type, db_results, fs_server

inputs = Blueprint('inputs', __name__)

# Route to home
@inputs.route('/', methods=['GET'])
def home():

    previous_simulations = db_serialised_inputs.DB_SERIALISED_INPUTS().get_all_mixed_results()
    defaults = db_variables.DB_VARIABLES().retrieve_most_recent_defaults()
    river_stretches = db_river_stretch.DB_RIVER_STRETCH().retrieve_all_stretch_names()
    nrfa_stations = db_nrfa.DB_NRFA().retrieve_all_station_info()

    # return 'Arup River Health Project Home'
    return render_template('inputs.html', defaults=defaults, river_stretches=river_stretches, nrfa_stations=nrfa_stations, previous_simulations=previous_simulations)

# Route for submitting a calculation
@inputs.route('/', methods=['POST'])
def get_form_data():
    # Make the function expect that the POST request has a header
    headers = request.headers

    # Take form inputs using built-in flask request.form method
    # and recast from immutable to mutable dict
    form_dict = dict(request.form)

    # Explicitly assign form dictionary values and convert them to correct data types
    river_stretch_name = form_dict.get('river_stretch_name')

    river_flow_ls = float(form_dict.get('river_flow_ls'))
    river_flow_ls_sd = float(form_dict.get('river_flow_ls_sd'))
    river_bod_mgl = float(form_dict.get('river_bod_mgl'))
    river_bod_mgl_sd = float(form_dict.get('river_bod_mgl_sd'))
    river_nh3_mgl = float(form_dict.get('river_nh3_mgl'))
    river_nh3_mgl_sd = float(form_dict.get('river_nh3_mgl_sd'))
    river_do_conc_mgl = float(form_dict.get('river_do_conc_mgl'))
    river_do_conc_mgl_sd = float(form_dict.get('river_do_conc_mgl_sd'))
    river_temp_celcius = float(form_dict.get('river_temp_celcius'))
    river_temp_celcius_sd = float(form_dict.get('river_temp_celcius_sd'))
    river_ph = float(form_dict.get('river_ph'))
    river_ph_sd = float(form_dict.get('river_ph_sd'))

    river_length_stretch_m = float(form_dict.get('river_length_stretch_m'))
    river_longslope_m_m = float(form_dict.get('river_longslope_m_m'))
    river_bedwidth_m = float(form_dict.get('river_bedwidth_m'))
    river_sideslope_m_m = float(form_dict.get('river_sideslope_m_m'))

    reaeration_constant = float(form_dict.get('reaeration_constant'))
    velocity_exponent = float(form_dict.get('velocity_exponent'))
    depth_exponent = float(form_dict.get('depth_exponent'))

    river_mannings_no = float(form_dict.get('river_mannings_no'))
    river_bod_decay_rate_day = float(form_dict.get('river_bod_decay_rate_day'))
    river_nh3_decay_rate_day = float(form_dict.get('river_nh3_decay_rate_day'))
    river_nh3_gain_bod_gN_gO2 = float(form_dict.get('river_nh3_gain_bod_gN_gO2'))
    river_nh3_yield_factor_gN_gO2 = float(form_dict.get('river_nh3_yield_factor_gN_gO2'))

    num_sims = int(form_dict.get('num_sims'))
    num_years = int(form_dict.get('num_years'))
    name_of_sim = form_dict.get('name_of_sim')

    cso_dict = {}
    for key, value in form_dict.items():
        if 'cso_id_' in key:
            cso_num = key.split('_')[-1]
            bod_conc = float(form_dict.get(f"cso_bod_conc_mgl_{cso_num}"))
            nh3_conc = float(form_dict.get(f"cso_nh3_conc_mgl_{cso_num}"))
            cso_dict[value] = {'bod_conc': bod_conc, 'nh3_conc': nh3_conc}

    # Create Unique ID for calculation
    unique_id = str(uuid.uuid4())

    # Instantiate river object
    river = River(river_stretch_name, river_flow_ls, river_flow_ls_sd, river_bod_mgl, river_bod_mgl_sd, river_nh3_mgl, river_nh3_mgl_sd, river_do_conc_mgl, river_do_conc_mgl_sd, river_temp_celcius, river_temp_celcius_sd, river_ph, river_ph_sd)

    # Save CSO CSV and then retrieve for use in calculation (This must come before CSO CSV is used in calculations)
    file_server_connnection = fs_server.FS_SERVER()
    file_server_connnection.save_file_storage_object_as_csv(folder_name='CSO', file=request.files['cso_csv'], unique_id=unique_id)
    cso_form_file = file_server_connnection.get_csv(folder_name='CSO', file_name=unique_id)

    # Get same CSV used to calculate mean and s.d. in nrfa rest controller
    # Warning: the following code assumes that the nrfa station will always be 
    # uploaded but in a later iteration this will be an optional input.
    nrfa_csv = False
    if "station_id" in form_dict.keys():


# THIS DOESN"T WORK NO CSV UPLOADED....................




        nrfa_station_id=str(form_dict.get('nrfa_station_id'))
        url = "https://nrfaapps.ceh.ac.uk/nrfa/ws/time-series?format=nrfa-csv&data-type=gdf&station=" + nrfa_station_id
        df = pd.read_csv(url, header=0)
        file_server_connnection.save_dataframe_as_csv(folder_name='NRFA', dataframe=df, unique_id=unique_id)
        nrfa_csv = True

    # Check if River Flow and Mean autopopulated by Qube CSV and save it
    qube_csv = False
    if request.files['qube_csv']:
        qube_csv = True
        file_server_connnection.save_file_storage_object_as_csv(folder_name='QUBE', file=request.files['qube_csv'], unique_id=unique_id)

   
    
    multi_cso = wb.create_multi_cso(cso_form_file, cso_dict, unique_id)


    # Delete Local CSO CSV (Good housekeeping)
    file_server_connnection.delete_local_file(folder_name='CSO', file_name=unique_id)

    # Create spill dataframe
    pre_spill_bod_ninety_ninth_percentile, pre_spill_nh3_ninety_ninth_percentile, post_spill_bod_ninety_ninth_percentile, post_spill_nh3_ninety_ninth_percentile, df = river.run_simulations(multi_cso, num_sims, unique_id.split('-')[0])

    #Save Outputs Dataframe to remote storage
    file_server_connnection.save_dataframe_as_csv(folder_name='OUTPUT', dataframe=df, unique_id=unique_id)

    # evaluate river type and create standards
    river_type = True if form_dict.get('river_type') == "1_2_4_6" else False
    wfd_standard_bod = WFD_Standards(is_1_2_4_6=river_type, is_bod=True)
    wfd_standard_nh3 = WFD_Standards(is_1_2_4_6=river_type, is_bod=False)

    pre_spill_bod_wfd_std_attained, post_spill_bod_wfd_std_attained, in_class_bod_percentage_deteriotation, bod_score =  wfd_standard_bod.score_and_stds_attained(pre_spill_bod_ninety_ninth_percentile, post_spill_bod_ninety_ninth_percentile)
    pre_spill_nh3_wfd_std_attained, post_spill_nh3_wfd_std_attained, in_class_nh3_percentage_deteriotation, nh3_score = wfd_standard_nh3.score_and_stds_attained(pre_spill_nh3_ninety_ninth_percentile, post_spill_nh3_ninety_ninth_percentile)

    # Instantiate graph objects
    bod_graph = graphs.Graph(df, post_spill_bod_ninety_ninth_percentile, pre_spill_bod_ninety_ninth_percentile, 'BOD', True)
    nh3_graph = graphs.Graph(df, post_spill_nh3_ninety_ninth_percentile, pre_spill_nh3_ninety_ninth_percentile, 'NH3', False)

    # Method saves graphs as html cards to be displayed on the outputs page
    bod_graph.create_and_save_graph_99(unique_id=unique_id)
    nh3_graph.create_and_save_graph_99(unique_id=unique_id)


    # Adding Variables used to Variables Database (Make sure isDefault=False)
    variables_connection = db_variables.DB_VARIABLES()
    variables_connection.insert_into_variables(
        unique_id= unique_id, isDefault=False,
        river_flow_ls=river_flow_ls, river_flow_ls_sd=river_flow_ls_sd,
        river_bod_mgl=river_bod_mgl, river_bod_mgl_sd=river_bod_mgl_sd, river_nh3_mgl=river_nh3_mgl, river_nh3_mgl_sd=river_nh3_mgl_sd, 
        river_do_conc_mgl=river_do_conc_mgl, river_do_conc_mgl_sd=river_do_conc_mgl_sd, river_temp_celcius=river_temp_celcius, river_temp_celcius_sd=river_temp_celcius_sd,
        river_ph=river_ph, river_ph_sd=river_ph_sd,
        river_length_stretch_m=river_length_stretch_m, river_longslope_m_m=river_longslope_m_m, river_bedwidth_m=river_bedwidth_m, river_sideslope_m_m=river_sideslope_m_m,
        reaeration_constant=reaeration_constant, velocity_exponent=velocity_exponent, depth_exponent=depth_exponent,
        river_mannings_no=river_mannings_no, river_bod_decay_rate_day=river_bod_decay_rate_day, river_nh3_decay_rate_day=river_nh3_decay_rate_day, river_nh3_gain_bod_gN_gO2=river_nh3_gain_bod_gN_gO2, river_nh3_yield_factor_gN_gO2=river_nh3_yield_factor_gN_gO2,
        num_sims=num_sims,num_years=num_years
        )
    variables_connection.insert_cso_variables(cso_data=cso_dict, unique_id=unique_id)
    
    # Adding results to Result Database
    results_connection = db_results.DB_RESULTS()
    results_connection.insert_into_results(
        unique_id=unique_id, 
        nh3_pre_spill=pre_spill_nh3_ninety_ninth_percentile, nh3_post_spill=post_spill_nh3_ninety_ninth_percentile, nh3_wfd_standard_pre_spill=pre_spill_nh3_wfd_std_attained, nh3_wfd_standard_post_spill=post_spill_nh3_wfd_std_attained, nh3_in_class_deterioration=in_class_nh3_percentage_deteriotation, nh3_soaf_score=nh3_score,
        bod_pre_spill=pre_spill_bod_ninety_ninth_percentile, bod_post_spill=post_spill_bod_ninety_ninth_percentile, bod_wfd_standard_pre_spill=pre_spill_bod_wfd_std_attained, bod_wfd_standard_post_spill=post_spill_bod_wfd_std_attained, bod_in_class_deterioration=in_class_bod_percentage_deteriotation, bod_soaf_score=bod_score
        )
    
    # Get current standards id
    standards_connection = db_standards.DB_WFD_STANDARDS()
    current_standards = standards_connection.get_latest_standards_id()

    # Get river stretch id
    river_connection = db_river_stretch.DB_RIVER_STRETCH()
    river_stretch_id = river_connection.retrieve_river_stretch_id(river_name=river.river_stretch_name)

    # Get water body id
    water_body_connection = db_water_body_type.DB_WATER_BODY_TYPE()
    water_body_type = "1_2_4_6"
    if river_type == False:
        water_body_type = "3_5_7"
    water_body_id = water_body_connection.retrieve_water_body_id(water_body_type=water_body_type)

    
    # Adding to Archive Database
    username = form_dict.get('username')
    archive_connection = db_archive.DB_ARCHIVE()
    archive_connection.insert_into_archive(unique_id=unique_id, name_of_simulation=name_of_sim, username=username ,river_stretch_id=river_stretch_id ,standards_id=current_standards, water_body_id=water_body_id, qube_csv=qube_csv, nrfa_csv=nrfa_csv)

    #Populating table in database with output mixed river data
    mean_mixed_flow, sd_mixed_flow, mean_mixed_bod, sd_mixed_bod, mean_mixed_nh3, sd_mixed_nh3 = data_utils.calculate_mixed_mean_sd(df)
    output_mixed_data_connection = db_serialised_inputs.DB_SERIALISED_INPUTS()
    output_mixed_data_connection.insert_into_mixed_output_results(unique_id=unique_id, mean_mixed_flow= mean_mixed_flow, sd_mixed_flow=sd_mixed_flow, mean_mixed_bod=mean_mixed_bod, sd_mixed_bod=sd_mixed_bod, mean_mixed_nh3=mean_mixed_nh3, sd_mixed_nh3=sd_mixed_nh3)

    # Redirect to outputs page
    return outputs_route(unique_id=unique_id)
