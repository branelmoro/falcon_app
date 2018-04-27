from . import HTTPTESTER, HTTP_200, HTTP_404, HTTP_400, HTTP_405, HTTP_500
import json

def test_search_skill_get():
	http_method = 'GET'
	test_case = {
		'path':'/search-skill',
		'method':http_method
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	assert data == {'message': 'Url does not exists'}
	assert response.status == HTTP_404

	test_case = {
		'path':'/search-skill/sdfdfd',
		'method':http_method
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	assert data == {'message': 'Url does not exists'}
	assert response.status == HTTP_404

	test_case = {
		'path':'/search-skill/1',
		'method':http_method
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	assert data == {'message': 'Url does not exists'}
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
	data = json.loads(response.content.decode('utf-8'))
	assert data == {'message': 'Url does not exists'}
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

	# PUT /search-skill should send 404 not found error
	test_case = {
		'path':'/search-skill',
		'method':http_method
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	assert data == {'message': 'Url does not exists'}
	assert response.status == HTTP_404


	# PUT /search-skill/{anystring} should send 404 not found error
	test_case = {
		'path':'/search-skill/sdsd',
		'method':http_method
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	assert data == {'message': 'Url does not exists'}
	assert response.status == HTTP_404


	# PUT /search-skill/{int} is valid
	# but it should send 404 as {int} does not exists
	test_case = {
		'path':'/search-skill/20',
		'method':http_method,
		'body':'{"status":"invalid"}'
	}
	response = HTTPTESTER.simulate_request(**test_case)
	# assert response.content == ''
	assert response.status == HTTP_404


	# PUT /search-skill/{int} is valid
	# but it should send 400 as no updated data sent in body
	test_case = {
		'path':'/search-skill/1',
		'method':http_method
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	assert data == {'search_skill_id': 'Please provide information to update'}
	assert response.status == HTTP_400


	# PUT /search-skill/{int} is valid and data sent in body is valid
	test_case = {
		'path':'/search-skill/1',
		'method':http_method,
		'body':'{"search_count":10}'
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	assert data == {'acknowledge': True, 'result': 'UPDATE 1'}
	assert response.status == HTTP_200


	# PUT /search-skill/{int} is valid and data sent in body - search_count is invalid
	# as it is string and hence it should send 400
	test_case = {
		'path':'/search-skill/1',
		'method':http_method,
		'body':'{"search_count":"10"}'
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	assert response.status == HTTP_400
	assert data == {'search_count': 'Please provide valid search count'}

	# PUT /search-skill/{int} is valid and data sent in body is valid
	test_case = {
		'path':'/search-skill/1',
		'method':http_method,
		'body':'{"assigned_to":10}'
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	assert data == {'acknowledge': True, 'result': 'UPDATE 1'}
	assert response.status == HTTP_200

	test_case = {
		'path':'/search-skill/1',
		'method':http_method,
		'body':'{"assigned_to":"10"}'
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	assert response.status == HTTP_400
	assert data == {'assigned_to': 'Please provide valid admin user id'}

	test_case = {
		'path':'/search-skill/1',
		'method':http_method,
		'body':'{"status":10}'
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	assert response.status == HTTP_400
	assert data == {'status': 'Please provide valid status - invalid, valid, pending'}

	test_case = {
		'path':'/search-skill/1',
		'method':http_method,
		'body':'{"status":"10"}'
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	assert response.status == HTTP_400
	assert data == {'status': 'Please provide valid status - invalid, valid, pending'}

	# PUT /search-skill/{int} is valid and data sent in body is valid
	test_case = {
		'path':'/search-skill/1',
		'method':http_method,
		'body':'{"status":"invalid"}'
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	assert data == {'acknowledge': True, 'result': 'UPDATE 1'}
	assert response.status == HTTP_200




def test_search_skill_find():

	test_case = {
		'path':'/search-skill/_find_',
		'method':'GET'
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	# assert data == {}
	assert response.status == HTTP_200


	test_case = {
		'path':'/search-skill/_find_/1',
		'method':'GET'
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	# assert data == {}
	assert response.status == HTTP_200


	test_case = {
		'path':'/search-skill/_find_/1',
		'method':'POST'
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	# assert data == {}
	assert response.status == HTTP_200


	test_case = {
		'path':'/search-skill/_find_/12',
		'method':'GET'
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	# assert data == {}
	assert response.status == HTTP_200


	test_case = {
		'path':'/search-skill/_find_/12',
		'method':'POST'
	}
	response = HTTPTESTER.simulate_request(**test_case)
	data = json.loads(response.content.decode('utf-8'))
	# assert data == {}
	assert response.status == HTTP_200