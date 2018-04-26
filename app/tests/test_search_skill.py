from . import HTTPTESTER, HTTP_200, HTTP_404, HTTP_400, HTTP_405, HTTP_500

def test_search_skill_get():
	http_method = 'GET'
	test_case = {
		'path':'/search-skill',
		'method':http_method
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.status == HTTP_404

	test_case = {
		'path':'/search-skill/sdfdfd',
		'method':http_method
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.status == HTTP_404

	test_case = {
		'path':'/search-skill/1',
		'method':http_method
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.status == HTTP_404



def test_search_skill_post():
	http_method = 'POST'
	test_case = {
		'path':'/search-skill',
		'method':http_method
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.status == HTTP_400

	test_case = {
		'path':'/search-skill/sdsd',
		'method':http_method
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.status == HTTP_404

	test_case = {
		'path':'/search-skill/2',
		'method':http_method
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.status == HTTP_500

	test_case = {
		'path':'/search-skill',
		'method':http_method,
		'body':'{"search_word":"carpenter"}'
	}
	response = HTTPTESTER.simulate_request(**test_case)
	# assert response.content == ''
	assert response.status == HTTP_200

	test_case = {
		'path':'/search-skill',
		'method':http_method,
		'body':'{"search_word":"carpenter"}'
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.status == HTTP_200





def test_search_skill_put():
	http_method = 'PUT'
	test_case = {
		'path':'/search-skill',
		'method':http_method
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.status == HTTP_404

	test_case = {
		'path':'/search-skill/sdsd',
		'method':http_method
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.status == HTTP_404

	test_case = {
		'path':'/search-skill/2',
		'method':http_method
	}
	response = HTTPTESTER.simulate_request(**test_case)
	# assert response.content == ''
	assert response.status == HTTP_400