from app import create_app

def test_standards_get_route():
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/standards' page is requested (GET)
	THEN check that the response is valid
	"""
	flask_app = create_app()

	with flask_app.test_client() as test_client:
		response = test_client.get('/standards/')
		assert response.status_code == 200

def test_standards_has_values():
	"""
	GIVEN a Flask application test environment
	WHEN the '/standards' page is requested (GET)
	THEN check that the response contains standards from the database
	"""
	flask_app = create_app()

	with flask_app.test_client() as test_client:
		response = test_client.get('/standards/')
		assert('WFD water body types' in response.get_data(as_text=True))
		assert('1, 2, 4, 6 and salmonid' in response.get_data(as_text=True))
		assert('3, 5 and 7' in response.get_data(as_text=True))
