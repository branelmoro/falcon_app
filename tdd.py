import sys

if len(sys.argv) <= 1:
	exit("invalid app provided")

app_name = sys.argv[1]

if app_name == "app":
	from app.test import test_cases
	from falcon_test import api as app
elif app_name == "admin_panel":
	from admin import app
else:
	exit("invalid app name - "+app_name+" provided")


from falcon import testing

a = testing.TestClient(app)


# result = a.simulate_get('/')
# print(result)
# exit()


def dotest(testcase):

	if "callback" not in testcase:
		exit("invalid testcase")
	else:
		callback = testcase["callback"]
		del testcase["callback"]

	test_name = "(callback to previous)"
	if "name" in testcase:
		test_name = ", file - "+testcase["name"]
		del testcase["name"]

	result = a.simulate_request(**testcase)

	test_result = callback(result)

	if test_result is True:
		print("testcase passed - "+testcase["method"]+" "+testcase["path"]+test_name)
	elif test_result is False:
		print("testcase failed - "+testcase["method"]+" "+testcase["path"]+test_name)
	elif isinstance(test_result, dict):
		test_result = dotest(test_result)

	return test_result



for test_criteria in test_cases:
	dotest(test_criteria)