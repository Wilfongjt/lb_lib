import unittest
from pylyttlebit.lb_project import LbProject

class LbProjectTest(unittest.TestCase):
    def setUp(self):
        self.actual = LbProject()

    def test_getBranch(self):
        result = self.actual.getBranch()
        #print(type(result))
        self.assertTrue(type(result) is str)

    #def test_CurrentBranch(self):
    #    pass

    def test_getDevelopement(self):
        result = self.actual.getDevelopmentFromPath()
        self.assertTrue(type(result) is str)

    def test_getOrganization(self):
        result = self.actual.getDevelopmentFromPath()
        self.assertTrue(type(result) is str)

    def test_getProject(self):
        result = self.actual.getProjectFromPath()
        self.assertTrue(type(result) is str)

    def test_getWorkspace(self):
        result = self.actual.getWorkspaceFromPath()
        self.assertTrue(type(result) is str)

    def test_hasBranch(self):
        result = self.actual.hasBranch('abcdefghij')
        #print('result', result)
        self.assertFalse(result)
        # cannot predict what branch the user will select so cant test
        self.assertTrue(type(result) is bool)

    def test_hasRemoteProject(self):
        url = 'https://github.com/Wilfongjt/lb_lib'
        #result = self.actual.hasRemoteProject(url)
        #self.assertTrue(type(result) is bool)
        # cant predict the users github username
        pass

    def test_isCloned(self):
        result = self.actual.isCloned(self.actual.getProjectFromPath())
        pass

    def test_verify(self):
        pass

if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()