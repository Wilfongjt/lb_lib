import unittest
from dep.pylyttlebit import LbDocFolders


class LbDocFoldersTest(unittest.TestCase):
    def setUp(self):
        self.actual = LbDocFolders()

    def test_getLineList(self):
        pass

    def test_setTitle(self):
        # no test
        pass

    def test_getTitle(self):
        # no test
        pass

    def test_ignore(self):
        # dont ignore
        result = self.actual.ignore('abc')
        self.assertFalse(result)
        # ignore when folder in ignore list
        result = self.actual.ignore('.git')
        self.assertTrue(result)
        ## return bool
        self.assertTrue(type(result) is bool)


    #def test_load(self):
    #    line_list = ['','']
    #    result = self.actual.load(line_list)
    #    ## return bool
    #    self.assertTrue(type(result) is LbDocFolders)

    #def test_open(self):
    #    ##* fail when source folder is not found
    #    with self.assertRaises(FolderNotFoundException):
    #        self.actual.open()
    #    ##* ignore unnessessary folders ... no test

    #    ##* add folders when found ... [] has test

    #    ##* add files when found ... [] has test

    #    ##* return LbDocFolders ... [] has test

    #    pass

    def save(self):
        pass

    def test_validate(self):
        pass


if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()