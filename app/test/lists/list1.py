from .listGenerator import listGenerator
lg = listGenerator()



from .. import tests
lg.addTestCase(tests.test1.test_case)

test_cases = lg.getTestCaseList()