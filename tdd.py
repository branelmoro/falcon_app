import sys

if len(sys.argv) <= 1:
	exit("invalid app provided")

app_name = sys.argv[1]
from app.test import test_cases
print(test_cases)
exit()

if app_name == "app":
	from falcon_test import app
	from app.test import test_cases
	print(test_cases)
	exit()
elif app_name == "admin_panel":
	from admin_panel.test import test_cases
	from admin import app
else:
	exit("invalid app name - "+app_name+" provided")





from falcon import testing

a = testing.TestClient(app)


result = a.simulate_get('/')
print(result)

# print(sys.argv)

# exit()


def dotest(testcase):

	if "callback" not in testcase:
		exit("invalid testcase")
	else:
		callback = testcase["callback"]

	result = a.simulate_get('/')

	test_result = callback(result)

	if test_result is True:
		print("testcase passed")
	elif test_result is False:
		print("testcase failed")
	elif isinstance(test_result, dict):
		test_result = dotest(test_result)

	return test_result






for test_criteria in test_cases:
	dotest(test_criteria)






# import falcon

# class resource:

# 	on_get(req, resp):
# 		resp.body = "here it is"


# def create():
#     api = falcon.API()
#     api.add_route('/', resource()) 
#     return api

# api = create()



# # for TDD

# from falcon import testing
# import pytest
# from app import create


# @pytest.fixture(scope='module')
# def client():
#     return testing.TestClient(create())

# def test_get_message(client):
#     result = client.simulate_get('/')
#     assert result.status_code == 200