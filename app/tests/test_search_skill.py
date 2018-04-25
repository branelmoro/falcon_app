from . import HTTPTESTER, HTTP_200, HTTP_405

def test_search_skill_get5():
	test_case = {
		"path":"/save-search-skill/sdsdfsdfsd",
		"method":"GET"
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.status == HTTP_405

def test_search_skill_get4():
	test_case = {
		"path":"/save-search-skill/_find_",
		"method":"GET"
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.status == HTTP_405

def test_search_skill_get2():
	test_case = {
		"path":"/save-search-skill/",
		"method":"POST"
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.status == HTTP_405

def test_search_skill_get1():
	test_case = {
		"path":"/save-search-skill/23",
		"method":"GET"
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.content == ''
	assert response.status == HTTP_405

def test_search_skill_get3():
	test_case = {
		"path":"/save-search-skill/",
		"method":"GET"
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.status == HTTP_405