import os
import unittest
from lb_lib.lb_util import LbUtil
from lb_lib.lb_exceptions import BadFileNameException, BadFolderNameException
class LbUtilTest(unittest.TestCase):

    def setUp(self) -> None:
        self.actual = LbUtil()
        #self.temp_folder = '/'.join(str(__file__).split('/')[0:-1])
        #self.temp_folder = '{}/temp'.format(self.temp_folder)
        #self.filename = 'deletable.{}'.format(str(__file__).split('/')[-1])
    def tearDown(self) -> None:
        pass

    def test_get_file_extension(self):
        result = self.actual.get_file_extension(str(__file__))
        self.assertEqual(result, 'py')

    def test_folder_exists(self):
        # not found
        result = self.actual.folder_exists('/notafolder')
        self.assertFalse(result)
        # found
        result = self.actual.folder_exists(os.getcwd())
        self.assertTrue(result)


    def test_file_exists(self):

        result = self.actual.file_exists(os.getcwd(),'xqd.abc')
        self.assertFalse(result)
        filename = str(__file__).split('/')[-1]

        folder = '/'.join(str(__file__).split('/')[0:-1])
        result = self.actual.file_exists(folder, filename)
        self.assertTrue(result)

    def test_get_folder_list(self):
        result = self.actual.folder_exists('/notafolder')
        self.assertFalse(result==[])

        result = self.actual.get_folder_list(os.path.expanduser('~'))
        self.assertTrue(result != [])


    def test_create_delete_folder_file(self):
        # none existant folder
        filename='abcedef.txt'
        folder = '{}/abcd'.format(os.path.expanduser('~'))
        with self.assertRaises(BadFolderNameException):
            result = self.actual.create_folder(None)
        # create the folder
        result = self.actual.create_folder(folder).folder_exists(folder)
        self.assertTrue(result)
        # create folder twice
        result = self.actual.create_folder(folder).folder_exists(folder)
        self.assertTrue(result)
        # add file
        with open('{}/{}'.format(folder, filename), 'w') as f:
            line_list = [] # empty file
            f.writelines(['{}\n'.format(ln) for ln in line_list])
        with open('{}/{}'.format(folder, 'blind_delete.txt'), 'w') as f:
            line_list = [] # empty file
            f.writelines(['{}\n'.format(ln) for ln in line_list])
        # delete file
        result = self.actual.delete_file(folder, filename).file_exists(folder, filename)
        self.assertFalse(result)

        # delete files from folder
        result = self.actual.delete_folder_files(folder, 'txt').get_file_list(folder)
        self.assertEqual(result, [])
        # delete folder
        result = self.actual.delete_folder(folder).folder_exists(folder)
        self.assertFalse(result)

    #def test_delete_folder(self):
    #    pass
    #    #delete_folder(self, folder)

    #def test_delete_folder_files(self):
    #    pass
    #    #delete_folder_files(self, folder, ext)


    #def test_delete_file(self):
    #    pass
    #    #delete_file(self, folder, file_name)

    def test_get_file_list(self):
        folder = os.getcwd()
        # search
        result = self.actual.get_file_list(folder, ext=None)
        self.assertNotEqual(result, [])
        # find all with *
        result = self.actual.get_file_list(folder, ext='*')
        self.assertNotEqual(result, [])

        result = self.actual.get_file_list(folder, ext='py')
        self.assertNotEqual(result, [])

    def test_copy_folder(self):
        pass
        #copy_folder(self, src_folder, dst_folder)



if __name__ == "__main__":
    # execute as script
    unittest.main()