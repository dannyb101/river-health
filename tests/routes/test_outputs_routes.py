from app import create_app

def test_outputs_get_route():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/outputs' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.get('/outputs/')
        assert response.status_code == 200