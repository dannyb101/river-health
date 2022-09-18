from enum import unique
import pandas as pd
import numpy as np
from app.models.waterbodies import Cso, River
import app.models.waterbodies as wb
import app.utils.data_utils as du
import pytest
import uuid

@pytest.fixture(scope='session')
def num_sims():
    return 2

@pytest.fixture(scope='session')
def trunc_unique_id():
    return str(uuid.uuid4()).split('-')[0]

@pytest.fixture(scope='session')
def cso_dict():
    return {'1234':{'bod_conc':125, 'nh3_conc':8}}

@pytest.fixture(scope='session')
def multi_cso(cso_dict, trunc_unique_id):
    return wb.create_multi_cso('./tests/files/example-cso-spills.csv', cso_dict, trunc_unique_id)

@pytest.fixture(scope='session')
def cso(cso_dict):
    cso_df = du.convert_cso_csv_to_df('./tests/files/example-cso-spills.csv')
    summed_cso_df = du.sum_df_over_hour(cso_df)
    return Cso(summed_cso_df,'1234', cso_dict['1234']['bod_conc'], cso_dict['1234']['nh3_conc'])

@pytest.fixture(scope='session')
def river():
    #instantiate river using mean and std from 'Example UPM output.xlsx'
    return River('Taf', 56.95086735, 4.07327551, 1.1435, 61.84489328, 3.832259258, 1.035409496)

@pytest.fixture(scope='session')
def river_df(river, multi_cso):
    return river.add_cso_spill(multi_cso)

@pytest.fixture(scope='session')
def full_simulation(river, multi_cso, num_sims, trunc_unique_id):
    return river.run_simulations(multi_cso, num_sims, trunc_unique_id)

def test_multi_cso_columns(multi_cso):
    """
    GIVEN a CSO object (that has a dataframe as attribute)
    WHEN accessing column names
    THEN expected column names are returned
    """
    cso_columns = ['cso_vol_l', 'cso_bod_kg', 'cso_nh3_kg']
    assert all([a == b for a, b in zip(multi_cso.data_frame.columns, cso_columns)])

def test_cso_pollutants(cso):
    """
    GIVEN a cso object 
    WHEN providing a volume taken from the example-cso-spills.csv file
    THEN return the expected pollutant masses
    """
    cso_vol_l = 4827.0
    cso_bod_kg =0.6034
    cso_nh3_kg = 0.0386
    assert cso.calculate_pollutant_mass(cso_vol_l) == [cso_bod_kg, cso_nh3_kg]

def test_cso_datatypes(multi_cso):
    """
    GIVEN a csv file for cso spills
    WHEN instantiating a cso object using that csv file
    THEN expect the cso data_frame attribute to have the appropriate data types
    """
    cso_datatypes = {
        'cso_bod_kg': np.dtype('float64'),
        'cso_nh3_kg': np.dtype('float64'),
        'cso_vol_l': np.dtype('float64')
    }
    assert multi_cso.data_frame.dtypes.to_dict() == cso_datatypes

def test_river_columns(river_df):
    """
    GIVEN a River object (that has a dataframe as attribute)
    WHEN accessing column names
    THEN expected column names are returned
    """
    river_columns = ['cso_vol_l', 'cso_bod_kg', 'cso_nh3_kg', 'upstream_flow_l/s', 'upstream_bod_mg/l', 'upstream_nh3_mg/l','mix_flow_l/s', 'mix_bod_mg/l', 'mix_nh3_mg/l']
    assert all([a == b for a, b in zip(river_df.columns, river_columns)])

def test_river_datatypes(river_df):
    """
    GIVEN a river object
    WHEN the function add_cso_spill is invoked
    THEN confirm the column names of the returned dataframe are as expected
    """
    river_datatypes = {
        'cso_vol_l': np.dtype('float64'),
        'cso_bod_kg': np.dtype('float64'),
        'cso_nh3_kg': np.dtype('float64'),
        'upstream_flow_l/s': np.dtype('float64'),
        'upstream_bod_mg/l': np.dtype('float64'),
        'upstream_nh3_mg/l': np.dtype('float64'),
        'mix_flow_l/s': np.dtype('float64'),
        'mix_bod_mg/l': np.dtype('float64'),
        'mix_nh3_mg/l': np.dtype('float64')
    }
    assert river_df.dtypes.to_dict() == river_datatypes

def test_river_df(river_df):
    """
    GIVEN a river object
    WHEN the function add_cso_spill is invoked
    THEN confirm the mixed flow rate is equal to the sum of the cso and upstream flows
    """
    cso_flow = river_df['cso_vol_l'][0] / 3600
    upstream_flow = river_df['upstream_flow_l/s'][0]
    mix_flow = river_df['mix_flow_l/s'][0]
    assert cso_flow + upstream_flow == mix_flow

def test_simulation_return_types(full_simulation):
    """
    GIVEN a river object
    WHEN the function run_simulations is invoked
    THEN confirm dataframe and pollutant concentrations are returned
    """
    assert type(full_simulation[0]) == type(full_simulation[1]) == type(full_simulation[2]) == type(full_simulation[3]) == np.float64
    assert type(full_simulation[4]) == pd.core.frame.DataFrame
    assert len(full_simulation) == 5

def test_simulation_num_runs(full_simulation, river_df, num_sims):
    """
    GIVEN a river object
    WHEN the function run_simulations is invoked
    THEN confirm the number of runs is as expected
    """
    assert len(full_simulation[4]) == len(river_df) * num_sims

def test_sim_event_id(full_simulation, multi_cso, num_sims):
    """
    GIVEN a river object
    WHEN the function run_simulations is invoked
    THEN confirm the final event_id is as expected
    """
    sim_id = '_' + str(num_sims) if num_sims > 9 else '_0' + str(num_sims)
    assert full_simulation[4]['sim_id'].iloc[-1] == str(multi_cso.cso_id) + sim_id
