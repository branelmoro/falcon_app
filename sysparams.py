import sys

del sys.argv[0]

PARAMS = {}
for arg in sys.argv:
	inputDetails = arg.split("=", 1)
	if len(inputDetails) == 2:
		PARAMS[inputDetails[0]] = inputDetails[1]
	else:
		exit("Invalid parameter "+arg+" Provided!!")