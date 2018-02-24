class listGenerator():

	def __init__(self):
		self.__test_cases = []

	def addTestCase(self, test):
		test_case = test.test_case
		if isinstance(test_case, list):
			k = 1;
			for i in test_case:
				i["name"] = str(test.__file__) + "-" + str(k)
				k = k+1
			self.__test_cases.extend(test_case)
		else:
			test_case["name"] = test.__file__
			self.__test_cases.append(test_case)

	def getTestCaseList(self):
		return self.__test_cases
