from . import HTTPTESTER, HTTP_200

def test_server_running():
	test_case = {
		"path":"/",
		"method":"GET"
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.status == HTTP_200