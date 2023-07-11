import unittest
import os
from lb_lib.lb_text_file import LbTextFile
from lb_lib.lb_exceptions import FolderNotFoundException, FileNotFoundException, BadFileNameException, BadFolderNameException
from lb_lib.lb_util import LbUtil

# start with no file
# folder_exists false
# file_exist false
# create
# create empty file
# folder_exists true
# file_exist true
# load file
# save file
# saveAs
# delete file
# delete saveAs file

class LbTextFileTest(unittest.TestCase):
    def setUp(self):
        self.actual = LbTextFile()
        self.temp_filename = '{}.env'.format(str(__file__).split('/')[-1])
        # create a temp folder
        self.temp_folder = '/'.join(str(__file__).split('/')[0:-1])
        self.temp_folder = '{}/temp'.format(self.temp_folder)
        LbUtil().create_folder(self.temp_folder)
    def tearDown(self):
        #print('tearDown')

        # remove all files in temp folder
        LbUtil().delete_folder_files(self.temp_folder, '*')
        # remove temp folder
        LbUtil().delete_folder(self.temp_folder)
    def test_getFolder(self):
        folder = '/'.join(str(__file__).split('/')[0:-1])

        # fail when folder is None
        result = self.actual.getFolder()
        self.assertEqual(result, None)
        self.assertFalse(result)

        # success when folder is defined
        self.actual.setFolder(folder)
        result = self.actual.getFolder()
        self.assertEqual(result,folder)

    def test_getFilename(self):
        filename = '/'.join(str(__file__).split('/')[-1])

        # fail when folder is None

        result = self.actual.getFilename()
        self.assertEqual(result, None)
        self.assertFalse(result)

        # success when folder is defined

        self.actual.setFilename(filename)
        result = self.actual.getFilename()
        self.assertEqual(result, filename)

    def test_getLineList(self):
        self.actual.setFolder('/'.join(str(__file__).split('/')[0:-1]))
        self.actual.setFilename(str(__file__).split('/')[-1])
        result = self.actual.getLineList()
        self.assertTrue(len(result) > 0)

    def test_folder_exists(self):
        folder = '/'.join(str(__file__).split('/')[0:-1])
        filename = str(__file__).split('/')[-1]
        notfolder = '/notanexistingfolder'
        notfile = 'aaaa.txt'

        # false when folder is None

        result = self.actual.folder_exists()
        self.assertFalse(result)

        # false when folder in not None

        self.actual.setFolder(notfolder)
        result = self.actual.folder_exists()
        self.assertFalse(result)

        # true when folder is found

        self.actual.setFolder(folder)
        result = self.actual.folder_exists()
        self.assertTrue(result)


    def test_file_exists(self):
        folder = '/'.join(str(__file__).split('/')[0:-1])
        filename = str(__file__).split('/')[-1]
        notfile = 'aaaa.txt'

        # file does not exist when filename is None
        result = self.actual.file_exists()
        self.assertFalse(result)

        # file does not exist when filename is not None
        self.actual.setFilename(notfile)
        result = self.actual.file_exists()

        # file exists when folder and filename is not None and file is found
        self.actual.setFolder(folder)
        self.actual.setFilename(filename)
        result = self.actual.file_exists()
        self.assertTrue(result)

    def test_exists(self):
        # empty by default
        result = self.actual.exists()
        self.assertFalse(result)

        # folder exists but file does not
        self.actual.setFolder(self.temp_folder)
        result = self.actual.exists()
        self.assertFalse(result)

        # folder exists and file exists
        self.actual.setFolder('/'.join(str(__file__).split('/')[0:-1]))
        self.actual.setFilename(str(__file__).split('/')[-1])
        result = self.actual.exists()
        self.assertTrue(result)


    def test_load(self):
        # empty by defualt
        self.assertEqual(self.actual, [])
        # put lines into object list
        result = self.actual.load(['a','b'])
        self.assertEqual(result, ['a', 'b'])
        # returns LbTextFile
        self.assertTrue(type(result) is LbTextFile)

    def test_validate(self):
        result = None
        # not valid when folder is None
        with self.assertRaises(BadFolderNameException):
            result = self.actual.validate()

        # not valid when folder doesnt exist
        self.actual.setFolder('/asdfasdfasdf')
        with self.assertRaises(FolderNotFoundException):
            result = self.actual.validate()

        # not valid when file doesnt exist
        self.actual.setFolder(self.temp_folder)
        with self.assertRaises(BadFileNameException):
            result = self.actual.validate()

        # returns LbTextFile
        self.actual.setFolder('/'.join(str(__file__).split('/')[0:-1]))
        self.actual.setFilename(str(__file__).split('/')[-1])
        result = self.actual.validate()
        self.assertTrue(type(result) is LbTextFile)

    def test_open(self):
        # false when folder is default
        # false when file is default
        # true when folder file found
        filename = str(__file__).split('/')[-1]
        folder = '/'.join(str(__file__).split('/')[0:-1])
        result = ''
        with self.assertRaises(BadFolderNameException):
            result = self.actual.open()

        # false when file is default
        self.actual.setFolder(folder)
        with self.assertRaises(BadFileNameException):
            result = self.actual.open()

        # folder and file found
        self.actual.setFolder(folder)
        self.actual.setFilename(filename)
        result = self.actual.open()
        self.assertNotEqual(result, [])

        # returns LbTextFile
        self.assertTrue(type(result) is LbTextFile)

    def test_save(self):

        # fail when invalid folder name (None)
        with self.assertRaises(BadFolderNameException):
            self.actual.save()

        # fail when folder doesnt exist
        self.actual.setFolder('/abcedf')
        with self.assertRaises(FolderNotFoundException):
            self.actual.save()

        # fail when folder is ok but file name is bad
        self.actual.setFolder(self.temp_folder)
        with self.assertRaises(BadFileNameException):
            self.actual.save()

        # create file when doesnt exist
        self.actual.setFolder(self.temp_folder)     # set good folder
        self.actual.setFilename(self.temp_filename) # set good filename
        self.assertFalse(self.actual.exists())      # prove file doesnt exist
        result = self.actual.save()                 # save empty file
        self.assertEqual(result, [])                # is empty

        # overwrite file when file exists
        self.actual.setFolder(self.temp_folder)     # set good folder
        self.actual.setFilename(self.temp_filename) # set good existing file
        result = self.actual.load(['a', 'b']).save()# load some data
        self.assertEqual(result, ['a', 'b'])
        result = LbTextFile().setFolder(self.temp_folder).setFilename(self.temp_filename).open()
        self.assertEqual(result, ['a', 'b'])

        # returns LbTextFile
        self.assertTrue(type(result) is LbTextFile)

    def test_saveAs(self):
        # save a file
        self.actual.setFolder(self.temp_folder)
        self.actual.setFilename(self.temp_filename)
        result = self.actual.save()
        self.assertEqual(result, [])

        # saveAs
        with self.assertRaises(BadFolderNameException):
            self.actual.saveAs(None,None)
        # fail when good folder with bad filename
        with self.assertRaises(BadFileNameException):
            self.actual.saveAs(self.temp_folder,None)
        # fail when good folder name, good filename but folder doesnt exist
        with self.assertRaises(BadFileNameException):
            self.actual.saveAs(self.temp_folder,None)
        # write empty file
        result = self.actual.saveAs(self.temp_folder, self.temp_filename)
        self.assertTrue(LbUtil().file_exists(self.temp_folder, self.temp_filename))
        # confirm file is empty
        self.assertEqual(result,[])
        # overwrite empty file with some data
        self.actual.load(['one','two'])
        result = self.actual.saveAs(self.temp_folder, self.temp_filename)
        self.assertEqual(result, ['one', 'two'])

        # returns LbTextFile
        self.assertTrue(type(result) is LbTextFile)

    def test_delete(self):
        # create a file to delete
        result = self.actual\
            .setFolder(self.temp_folder)\
            .setFilename(self.temp_filename)\
            .load(['a','b'])\
            .save()

        self.assertEqual(result, ['a', 'b'])    # data ok
        self.assertTrue(result.exists())        # file was saved
        # delete when  exists
        result = self.actual.delete()
        # clear list
        self.assertEqual(result, [])        # list was cleard
        self.assertFalse(result.exists())   # file was removed
        # returns empty LbTextFile
        self.assertTrue(type(result) is LbTextFile)
        self.assertEqual(result, [])  # LbTextFile is empty

    def test_isEmpty(self):
        # empty file when file doesnt exist
        result = self.actual.isEmpty()
        self.assertTrue(not self.actual.exists() and result)

        # file is empty when has no lines
        result = self.actual.isEmpty()
        self.actual.setFolder(self.temp_folder).setFilename(self.temp_filename).save() # write empty file
        self.assertTrue(self.actual.exists() and result)

        # return LbTextFile
        self.assertTrue(type(result) is bool)



if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()