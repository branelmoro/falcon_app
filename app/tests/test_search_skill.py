from . import HTTPTESTER, HTTP_200, HTTP_405

def test_search_skill_get2():
	test_case = {
		"path":"/save-search-skill/",
		"method":"GET"
	}
	response = HTTPTESTER.simulate_request(**test_case)
	assert response.status == HTTP_405

# def test_search_skill_get1():
# 	test_case = {
# 		"path":"/save-search-skill/23",
# 		"method":"GET"
# 	}
# 	response = HTTPTESTER.simulate_request(**test_case)
# 	assert response.status == HTTP_405