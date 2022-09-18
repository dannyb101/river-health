from flask import request
from app import create_app
from werkzeug.datastructures import FileStorage


def test_home_get_route():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200


def test_home_has_template():
    """
    GIVEN a Flask application test environment
    WHEN the '/' page is posted (POST)
    THEN check that the response contains a template with num_years
    """
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.get("/")
        assert "num_years" in response.get_data(as_text=True)

    return


# def test_home_post_route():
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/' page is requested (POST)
#     THEN check that the response redirects to outputs page
#     """
#     flask_app = create_app()

#     with flask_app.test_client() as test_client:

#         # Create strings for route
#         url = "/"

#         # Create mock form data for input variables (without file)
#         mock_request_data = {
#             "river_stretch_name": "Aber",
#             "cso_id_1": "123",
#             "river_flow_ls": "1",
#             "river_flow_ls_sd": "1",
#             "river_bod_mgl": "4.23",
#             "river_bod_mgl_sd": "1",
#             "river_nh3_mgl": "0.61",
#             "river_nh3_mgl_sd": "1",
#             "river_do_conc_mgl": "100",
#             "river_do_conc_mgl_sd": "1",
#             "river_temp_celcius": "18",
#             "river_temp_celcius_sd": "1",
#             "river_ph": "7.0",
#             "river_ph_sd": "1",
#             "reaeration_constant": "2",
#             "velocity_exponent": "2",
#             "depth_exponent": "1",
#             "river_length_stretch_m": "1000",
#             "river_longslope_m_m": "1",
#             "river_bedwidth_m": "3",
#             "river_sideslope_m_m": "5",
#             "cso_bod_conc_mgl_1": "125",
#             "cso_nh3_conc_mgl_1": "8",
#             "river_mannings_no": "0.025",
#             "river_bod_decay_rate_day": "0.3",
#             "river_nh3_decay_rate_day": "1",
#             "river_nh3_yield_factor_gN_gO2": "1",
#             "river_nh3_gain_bod_gN_gO2": "1",
#             "num_sims": "2",
#             "num_years": "10",
#             "river_type": "WFD water body types 3, 5 and 7",
#             "name_of_sim": "Test1",
#         }

#         # Create mock form data for file
#         file_path = "./tests/files/example-cso-spills.csv"

#         my_file = FileStorage(
#             stream=open(file_path, "rb"),
#             filename="cso-spills.csv",
#             content_type="text/csv",
#         )

#         # Add file data to mock form data
#         mock_request_data["cso_csv"] = my_file

#         # Create mock form data for file
#         file_path = "./tests/files/example-Qube-data.csv"

#         qube_data = FileStorage(
#             stream=open(file_path, "rb"),
#             filename="qube-data.csv",
#             content_type="text/csv",
#         )

#         # Add file data to mock form data
#         mock_request_data["qube_csv"] = qube_data

#         # Execute route
#         response = test_client.post(
#             url, content_type="multipart/form-data", data=mock_request_data
#         )

#         # Test route
#         assert response.status_code == 200
