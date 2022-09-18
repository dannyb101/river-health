import pytest
from app.Connections.db_variables import DB_VARIABLES

# Create session persistent Database connection
@pytest.fixture(scope='session')
def connection():
    return DB_VARIABLES()

def test_checks_db_columns(connection):
    defaults_from_database = connection.retrieve_most_recent_defaults()
    list_of_default_keys = list(defaults_from_database.keys())
    assert list_of_default_keys == ['id', 'isDefault', 'created', 
                'river_flow_ls', 'river_flow_ls_sd', 'river_bod_mgl', 'river_bod_mgl_sd', 'river_nh3_mgl', 'river_nh3_mgl_sd',
                'river_do_conc_mgl', 'river_do_conc_mgl_sd', 'river_temp_celcius', 'river_temp_celcius_sd', 'river_ph', 'river_ph_sd',
                'cso_bod_conc_mgl', 'cso_nh3_conc_mgl',
                'river_length_stretch_m', 'river_longslope_m_m', 'river_bedwidth_m','river_sideslope_m_m', 
                'reaeration_constant', 'velocity_exponent', 'depth_exponent',
                'river_mannings_no', 'river_bod_decay_rate_day', 'river_nh3_decay_rate_day', 'river_nh3_gain_bod_gN_gO2', 'river_nh3_yield_factor_gN_gO2', 
                'num_sims', 'num_years']