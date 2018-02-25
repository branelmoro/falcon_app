# from psycopg2 import connect
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



# dbcredentials = {
# 	"host":"127.0.0.1",
# 	"user":"branelm",
# 	"password":"root",
# 	"database":"postgres",
# 	"port":5432
# }

# con = connect(**dbcredentials)

# con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
# cur = con.cursor()

# sql = """
# CREATE DATABASE testdb1 WITH TEMPLATE laborstack OWNER branelm CONNECTION LIMIT = -1;
# """

# cur.execute(sql)
# cur.close()
# con.close()



# exit()















import sys

if len(sys.argv) <= 1:
	exit("invalid app provided")

app_name = sys.argv[1]

from app.config import DOCLEANUP

from app.config import PGDB1
print(PGDB1)

if app_name == "app":
	from app.test import test_cases
	from falcon_test import api
elif app_name == "admin_panel":
	from admin import app as api
else:
	exit("invalid app name - "+app_name+" provided")


from falcon import testing

a = testing.TestClient(api)


# result = a.simulate_get('/')
# print(result)
# exit()

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


DOCLEANUP()