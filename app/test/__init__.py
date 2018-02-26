from sysparams import PARAMS
test_cases = []
if "test_case" in PARAMS:
	test = __import__(name=PARAMS["app"]+".test.tests."+PARAMS["test_case"], fromlist=[PARAMS["test_case"]])
	test_cases.append(test.test_case)
elif "list" in PARAMS:
	test_list = __import__(name=PARAMS["app"]+".test.lists."+PARAMS["list"], fromlist=[PARAMS["list"]])
	test_cases = test_list.test_cases
else:
	from .lists import list1 as test_cases