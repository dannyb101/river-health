from app import create_app

def test_defaults_get_route():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/defaults' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.get('/defaults/')
        assert response.status_code == 200

#Commented, as due to the lack of a mock database this is interacting with the 
#database and inserting false mock data
# def test_defaults_post_route():
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/defaults' page is requested (POST)
#     THEN check that the response is valid
#     """
#     flask_app = create_app()

#     with flask_app.test_client() as test_client:

#         # Create strings for route
#         url = '/defaults'
        
#         # Create mock form data for input variables (without file)
#         mock_request_data = {'cso_bod_conc_mgl': '125', 'cso_nh3_conc_mgl' : '8', 'river_bod_mgl' : '3.5', 'river_bod_mgl_sd' : '2.5', 'river_nh3_mgl' : '0.2', 'river_nh3_mgl_sd' : '0.3',
#                 'river_do_conc_mgl' : '7', 'river_do_conc_mgl_sd' : '0.001', 'river_temp_celcius' : '17',
#                 'river_temp_celcius_sd' : '1.82', 'river_ph' : '8', 'river_ph_sd' : '0.001', 'river_mannings_no' : '0.03', 
#                 'river_bod_decay_rate_day' : '0.35', 'river_nh3_decay_rate_day' : '2',
#                 'river_nh3_gain_bod_gN_gO2' : '0.29', 'river_nh3_yield_factor_gN_gO2' : '0.109', 
#                 'reaeration_constant' : '3.9', 'velocity_exponent' : '0.5', 'depth_exponent' : '-1.5',
#                 'river_length_stretch_m': '1000', 'river_longslope_m_m' : '7.815', 'river_bedwidth_m' : '45',
#                 'river_sideslope_m_m' : '7.815', 'num_sims' : '2', 'num_years' : '10' }


#         # Execute route
#         response = test_client.post(url, content_type='multipart/form-data', data=mock_request_data)

#         # Test route posts data
#         assert response.status_code == 308