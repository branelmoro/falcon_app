import sys, traceback

if len(sys.argv) <= 1:
	exit("invalid app provided")

from sysparams import PARAMS

if "app" not in PARAMS:
	exit("app not provided")
else:
	app_name = PARAMS["app"]

TEST_API = None


def common_callback(response):
	# print("in common_callback")
	return True


def dotest(testcase):

	if "callback" not in testcase:
		callback = common_callback
		# exit("invalid testcase")
	else:
		callback = testcase["callback"]
		del testcase["callback"]

	test_name = "(callback to previous)"
	if "name" in testcase:
		test_name = ", file - "+testcase["name"]
		del testcase["name"]

	result = TEST_API.simulate_request(**testcase)

	test_result = callback(result)

	if test_result is True:
		print("testcase passed - "+testcase["method"]+" "+testcase["path"]+test_name)
	elif test_result is False:
		raise Exception("testcase failed - "+testcase["method"]+" "+testcase["path"]+test_name)
	elif isinstance(test_result, dict):
		test_result = dotest(test_result)

	return test_result





try:

	if app_name == "app":
		from app.test import test_cases
		from falcon_test import api
	elif app_name == "admin_panel":
		from admin import app as api
	else:
		raise Exception("invalid app name - "+app_name+" provided")

	from falcon import testing

	TEST_API = testing.TestClient(api)

	for test_criteria in test_cases:
		dotest(test_criteria)

except:

	exc_type, exc_value, exc_traceback = sys.exc_info()
	tb = traceback.format_list(traceback.extract_tb(exc_traceback))
	exception_message = traceback.format_exception_only(exc_type, exc_value)
	print(exception_message)