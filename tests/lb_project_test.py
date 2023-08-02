import unittest
from lb_lib.lb_project import LbProject

class LbScriptTest(unittest.TestCase):
    def setUp(self):
        self.actual = LbProject()

    def test_getBranch(self):
        result = self.actual.getBranch()
        print(type(result))
        self.assertTrue(type(result) is str)

    #def test_CurrentBranch(self):
    #    pass

    def test_getDevelopement(self):
        result = self.actual.getDevelopment()
        self.assertTrue(type(result) is str)


    def test_current_directory(self):
        result = self.actual.current_directory()
        self.assertTrue(type(result) is str)

    def test_get_env_value(self):
        pass

    def test_getOrganization(self):
        pass
    def test_getProject(self):
        pass
    def test_getWorkspace(self):
        pass
    def hasBranch(self):
        pass
    def hasRemoteProject(self):
        pass
    def test_isCloned(self):
        pass
    def test_verify(self):
        pass




if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()