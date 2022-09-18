from flask import Blueprint, render_template, request
from app.Connections.db_variables import DB_VARIABLES
import uuid


defaults = Blueprint('defaults', __name__)

# Route to defaults page
@defaults.route('/defaults/', methods=['GET'])
def get_defaults_page():

    connection = DB_VARIABLES()

    defaults = connection.retrieve_most_recent_defaults()

    # return populated defaults page, with up-to-date defaults
    return render_template('defaults.html', defaults=defaults)

@defaults.route('/defaults/', methods=['POST'])
def post_defaults_data():

    connection = DB_VARIABLES()

    # Make the function expect that the POST request has a header
    headers = request.headers

    # Take form inputs using built-in flask request.form method
    # and recast from immutable to mutable dict
    defaults_form_dict = dict(request.form)

    cso_bod_conc_mgl=float(defaults_form_dict.get('cso_bod_conc_mgl'))
    cso_nh3_conc_mgl=float(defaults_form_dict.get('cso_nh3_conc_mgl'))

    unique_id = str(uuid.uuid4())

    cso_data = {
        unique_id:{
            'bod_conc': cso_bod_conc_mgl,
            'nh3_conc': cso_nh3_conc_mgl
        }
    }


    connection.insert_into_variables(
        unique_id= unique_id,
        isDefault=True,
        river_flow_ls=None,
        river_flow_ls_sd=None,
        river_bod_mgl=float(defaults_form_dict.get('river_bod_mgl')),
        river_bod_mgl_sd=float(defaults_form_dict.get('river_bod_mgl_sd')),
        river_nh3_mgl=float(defaults_form_dict.get('river_nh3_mgl')),
        river_nh3_mgl_sd=float(defaults_form_dict.get('river_nh3_mgl_sd')), 
        river_do_conc_mgl=float(defaults_form_dict.get('river_do_conc_mgl')),
        river_do_conc_mgl_sd=float(defaults_form_dict.get('river_do_conc_mgl_sd')),
        river_temp_celcius=float(defaults_form_dict.get('river_temp_celcius')),
        river_temp_celcius_sd=float(defaults_form_dict.get('river_temp_celcius_sd')),
        river_ph=float(defaults_form_dict.get('river_ph')), 
        river_ph_sd=float(defaults_form_dict.get('river_ph_sd')),
        river_length_stretch_m=float(defaults_form_dict.get('river_length_stretch_m')),
        river_longslope_m_m=float(defaults_form_dict.get('river_longslope_m_m')),
        river_bedwidth_m=float(defaults_form_dict.get('river_bedwidth_m')),
        river_sideslope_m_m=float(defaults_form_dict.get('river_sideslope_m_m')),
        reaeration_constant=float(defaults_form_dict.get('reaeration_constant')),
        velocity_exponent=float(defaults_form_dict.get('velocity_exponent')),
        depth_exponent=float(defaults_form_dict.get('depth_exponent')),
        river_mannings_no=float(defaults_form_dict.get('river_mannings_no')),
        river_bod_decay_rate_day=float(defaults_form_dict.get('river_bod_decay_rate_day')),
        river_nh3_decay_rate_day=float(defaults_form_dict.get('river_nh3_decay_rate_day')),
        river_nh3_gain_bod_gN_gO2=float(defaults_form_dict.get('river_nh3_gain_bod_gN_gO2')),
        river_nh3_yield_factor_gN_gO2=float(defaults_form_dict.get('river_nh3_yield_factor_gN_gO2')),
        num_sims=int(defaults_form_dict.get('num_sims')),
        num_years=int(defaults_form_dict.get('num_years'))
        )
    connection.insert_cso_variables(unique_id=unique_id, cso_data=cso_data)

    # return populated defaults page, with up-to-date defaults
    return get_defaults_page()

@defaults.route('/defaults/reset', methods=['GET'])
def reset_defaults():
    connection = DB_VARIABLES()
    connection.populate_variables()
    return get_defaults_page()