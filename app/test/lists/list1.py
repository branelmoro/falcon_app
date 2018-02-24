from .listGenerator import listGenerator
lg = listGenerator()

from ..tests import test1
lg.addTestCase(test1.test_case)

test_cases = lg.getTestCaseList()