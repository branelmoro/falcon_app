import sys

if sys.argv and sys.argv[0] == "tdd.py":
	pass
else:
	exit("Invalid Test Case Enviornment")


from .lists import list1 as test_cases