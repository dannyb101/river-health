from app import create_app
import json

def test_get_mean_and_sd():
    """
    GIVEN station with id 1001
    WHEN mean and s.d. of river flow are requested
    THEN means river flow has the expected value
    """

    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.get('/nrfa/mean_and_sd_flow?station_id=1001&num_years=10')
        assert int(json.loads(response.data)['river_flow_ls']) == 2824