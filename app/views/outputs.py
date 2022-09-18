from flask import Blueprint, render_template
from ..models.waterbodies import *
from ..utils.html_utils import dataframe_to_html_table
from ..Connections import db_archive, db_variables, fs_server
from ..utils import data_utils as du
import pandas

outputs = Blueprint('outputs', __name__)

# Route to outputs page
@outputs.route('/outputs/', methods=['GET'])
@outputs.route('/outputs/<unique_id>')
def outputs_route(unique_id=None):

    archive_connection = db_archive.DB_ARCHIVE()

    # Check if Archive is empty, in which case show Error HTML page
    if archive_connection.get_most_recent_id() == 0:
        return render_template('archive-empty.html', active_page='outputs')
    # Check if UniqueID provided or Exists, if not then show last calculation
    elif unique_id == None or archive_connection.check_id_exists(unique_id=unique_id) == None:
        return create_outputs_page(unique_id=archive_connection.get_most_recent_id())
    # Show page for the UniqueID provided (UniqueID exists)
    else:
        return create_outputs_page(unique_id=unique_id)



def create_outputs_page(unique_id):

    archive_connection = db_archive.DB_ARCHIVE()
    variables_connection = db_variables.DB_VARIABLES()
    fs_server_connection = fs_server.FS_SERVER()

    try:
        output_values = archive_connection.get_all_output_page_values(unique_id=unique_id)
        fs_server_connection.get_graph(folder_name='BOD_GRAPH', file_name=unique_id)
        fs_server_connection.get_graph(folder_name='NH3_GRAPH', file_name=unique_id)

        output_page_values = {
            "river_stretch_name": output_values['river_stretch_name'],
            "cso_input_data" : variables_connection.retrieve_cso_inputs(unique_id),
            "post_spill_bod_ninetynine_percentile": output_values['bod_post_spill'],
            "post_spill_nh3_ninetynine_percentile": output_values['nh3_post_spill'],
            "pre_spill_bod_ninetynine_percentile": output_values['bod_pre_spill'],
            "pre_spill_nh3_ninetynine_percentile": output_values['nh3_pre_spill'],
            "river_class": output_values['water_body_type'],
            "pre_spill_bod_wfd_std_attained": output_values['bod_wfd_standard_pre_spill'],
            "post_spill_bod_wfd_std_attained": output_values['bod_wfd_standard_post_spill'],
            "in_class_bod_percentage_deteriotation" : output_values['bod_in_class_deterioration'],
            "bod_score" : output_values['bod_soaf_score'],
            "pre_spill_nh3_wfd_std_attained": output_values['nh3_wfd_standard_pre_spill'],
            "post_spill_nh3_wfd_std_attained": output_values['nh3_wfd_standard_post_spill'],
            "in_class_nh3_percentage_deteriotation" : output_values['nh3_in_class_deterioration'],
            "nh3_score": output_values['nh3_soaf_score'],
            "name_of_sim" : output_values['name_of_sim'],
            "input_data":  variables_connection.retrieve_inputs(unique_id),
            "nh3_soaf_class": du.calculate_soaf_impact_class(output_values['nh3_soaf_score']),
            "bod_soaf_class":  du.calculate_soaf_impact_class(output_values['bod_soaf_score'])
        }
        bod_graph = 'graph_templates/BOD_GRAPH/' + unique_id + '.html'
        nh3_graph = 'graph_templates/NH3_GRAPH/' + unique_id + '.html'

        dataframe = fs_server_connection.get_csv(folder_name='OUTPUT', file_name=unique_id)
        dataframe = pandas.read_csv(dataframe)
        fs_server_connection.delete_local_file(folder_name='OUTPUT', file_name=unique_id)

        return render_template('outputs.html', output_page_values=output_page_values, bod_graph=bod_graph, nh3_graph=nh3_graph, tables=dataframe_to_html_table(dataframe)) 

    finally:
        fs_server_connection.delete_local_graph(folder_name='BOD_GRAPH', file_name=unique_id)
        fs_server_connection.delete_local_graph(folder_name='NH3_GRAPH', file_name=unique_id)

