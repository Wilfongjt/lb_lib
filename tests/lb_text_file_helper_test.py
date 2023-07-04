import os
import unittest
from lb_lib.lb_text_file_helper import LbTextFileHelper

class LbTextFileHelperTest(unittest.TestCase):
    def setUp(self):
        #self.folder = os.getcwd()
        self.folder = '/'.join(str(__file__).split('/')[0:-1])
        self.filename = str(__file__).split('/')[-1]
        #print('folder',self.folder)
        #print('filename',self.filename)
        self.actual = LbTextFileHelper(folder=self.folder, filename=self.filename)
        self.actualNF = LbTextFileHelper(folder=self.folder, filename='nf_{}'.format(self.filename))
    def test_exists(self):
        result = self.actualNF.exists()
        self.assertFalse(result)

        result = self.actual.exists()
        self.assertTrue(result)
    def test_deleteWhenFound(self):
        pass
    def copyTo(self):
        pass
if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()