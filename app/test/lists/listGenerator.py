class listGenerator():

	def __init__(self):
		self.__test_cases = []

	def addTestCase(self, test_case):
		if isinstance(test_case, list):
			self.__test_cases.extend(test_case)
		else:
			self.__test_cases.append(test_case)

	def getTestCaseList(self):
		return self.__test_cases
