import pytest
from app.Connections import db_variables, db_archive

@pytest.fixture(scope='session')
def var_connection():
	return db_variables.DB_VARIABLES()

@pytest.fixture(scope='session')
def arch_connection():
	return db_archive.DB_ARCHIVE()

@pytest.fixture(scope='session')
def recent_id(arch_connection):
	return arch_connection.get_most_recent_id()

def test_retrieve_inputs(var_connection, recent_id):
	"""
	GIVEN a database variables connection
	WHEN the database is called
	THEN check that all columns are returned
	"""
	if recent_id == 0:
		pytest.skip("Reason: database empty")
	all_inputs_row = var_connection.retrieve_inputs(recent_id)
	list_of_variables_columns= list(all_inputs_row.keys())
	for var in list_of_variables_columns:
		# unknown number of cso inputs returned, ensure that the prefix to cso input name is present
		if var[:3] == 'cso':
			var = "_".join(var.split("_")[:-1])
		assert var in [
			"depth_exponent",
			"num_sims",
			"num_years",
			"river_flow_ls",
			"river_flow_ls_sd", 
			"river_bod_mgl",
			"river_bod_mgl_sd",
			"river_nh3_mgl",
			"river_nh3_mgl_sd",
			"river_do_conc_mgl",
			"river_do_conc_mgl_sd",
			"river_temp_celcius",
			"river_temp_celcius_sd",
			"river_ph",
			"river_ph_sd", 
			"river_length_stretch_m",
			"river_longslope_m_m",
			"river_bedwidth_m",
			"river_sideslope_m_m",
			"reaeration_constant",
			"river_mannings_no",
			"river_bod_decay_rate_day",
			"river_nh3_decay_rate_day",
			"river_nh3_gain_bod_gN_gO2",
			"river_nh3_yield_factor_gN_gO2", 
			"velocity_exponent",
			"archive_id",
			"cso_id",
			"sim_datetime",
			"river_stretch_name",
			"river_type",
			"cso_bod_conc_mgl",
			"cso_nh3_conc_mgl"
		]
