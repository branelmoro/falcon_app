import sys, traceback

if len(sys.argv) <= 1:
	exit("invalid app provided")

app_name = sys.argv[1]

try:
	if app_name == "app":
		import app.tests
	elif app_name == "admin_panel":
		import admin_panel.tests
	else:
		raise Exception("invalid app name - "+app_name+" provided")
except:
	exc_type, exc_value, exc_traceback = sys.exc_info()
	tb = traceback.format_list(traceback.extract_tb(exc_traceback))
	exception_message = traceback.format_exception_only(exc_type, exc_value)
	print(exception_message)