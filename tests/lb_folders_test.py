import unittest
import os
from pylyttlebit.lb_folders import LbFolders
class LbFoldersTest(unittest.TestCase):
    def setUp(self):
        self.actual = LbFolders()
    def tearDown(self):
        pass
    def test_getDevelopmentFolder(self):
        result = self.actual.getDevelopmentFolder()
        self.assertTrue(result.endswith('Development'))
    def test_getFolder(self):
        result = self.actual.getFolder(1)
        self.assertTrue(result.endswith('Development'))
        #print('result', result)
        result = self.actual.getFolder(2)
        #print('result', result)
        self.assertFalse(result.endswith('Development'))

    def test_getOrganizationFolder(self):
        result = self.actual.getOrganizationFolder()
        self.assertTrue(type(result) is str)

    def test_getWorkspaceFolder(self):
        result = self.actual.getWorkspaceFolder()
        self.assertTrue(type(result) is str)
    def test_getProjectFolder(self):
        result = self.actual.getProjectFolder()
        self.assertTrue(type(result) is str)
        self.assertTrue(result.endswith('lb_lib'))

    def test_getToolsFolder(self):
        result = self.actual.getToolsFolder()
        self.assertTrue(type(result) is str)
        self.assertTrue(result.endswith('_tools'))

    def test_getLibraryFolder(self):
        result = self.actual.getLibraryFolder()
        self.assertTrue(type(result) is str)
        self.assertTrue(result.endswith('pylyttlebit'))

    def test_getScriptsFolder(self):
        result = self.actual.getScriptsFolder()
        self.assertTrue(type(result) is str)
        self.assertTrue(result.endswith('scripts'))

if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()