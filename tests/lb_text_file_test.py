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
        self.temp_folder = '/'.join(str(__file__).split('/')[0:-1])
        self.temp_folder = '{}/temp'.format(self.temp_folder)
        self.temp_filename = '{}.env'.format(str(__file__).split('/')[-1])
        # create a temp folder
        #self.deleteTempFolder()
        #self.createTempFolder()
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

    def test_folder_exists(self):
        folder = '/'.join(str(__file__).split('/')[0:-1])
        filename = str(__file__).split('/')[-1]
        notfolder = '/notanexistingfolder'
        notfile = 'aaaa.txt'
        # exists false, when folder is default and file is default

        result = self.actual.exists()
        self.assertFalse(result)

        # fail when folder is not default and folder not exists and file is default

        self.actual.setFolder(notfolder)
        result = self.actual.exists()
        self.assertFalse(result)

        # fail when folder is not default and folder not exists and file is default

        self.actual.setFolder(folder)
        result = self.actual.exists()
        self.assertFalse(result)

        # exists false, when folder is not default and folder not exists and file is not default and file not exist

        self.actual.setFolder(folder)
        self.actual.setFilename(notfile)
        result = self.actual.exists()
        self.assertFalse(result)

        # exists false, when folder is not default and folder exists and file is not default and file exits

        self.actual.setFolder(folder)
        self.actual.setFilename(filename)
        result = self.actual.exists()
        self.assertTrue(result)

    def test_file_exists(self):
        folder = '/'.join(str(__file__).split('/')[0:-1])
        filename = str(__file__).split('/')[-1]
        notfile = 'aaaa.txt'

        # fail when filename is None
        result = self.actual.file_exists()
        self.assertFalse(result)

        # fail when filename doesnt exist
        self.actual.setFilename(notfile)
        result = self.actual.file_exists()

        # true when file exists
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
        self.actual.setFolder(self.temp_folder)
        self.actual.setFilename(self.temp_filename)

        result = self.actual.exists()
        self.assertTrue(result)
    def test_load(self):
        # empty by defualt
        self.assertEqual(self.actual, [])
        # load goes into list
        result = self.actual.load(['a','b'])
        self.assertEqual(result, ['a', 'b'])

    def test_validate(self):

        # fail when folder is None
        with self.assertRaises(BadFolderNameException):
            self.actual.validate()

        # fail when folder doesnt exist
        self.actual.setFolder('/asdfasdfasdf')
        with self.assertRaises(FolderNotFoundException):
            self.actual.validate()

        # fail when file doesnt exist
        self.actual.setFolder(self.temp_folder)
        with self.assertRaises(BadFileNameException):
            self.actual.validate()

        # self.actual.setFolder()

    def test_open(self):
        # false when folder is default
        # false when file is default
        # true when folder file found
        filename = str(__file__).split('/')[-1]
        folder = '/'.join(str(__file__).split('/')[0:-1])
        result = ''
        with self.assertRaises(FolderNotFoundException):
            result = self.actual.open()

        # false when file is default
        self.actual.setFolder(folder)
        with self.assertRaises(FileNotFoundException):
            result = self.actual.open()

        # folder and file found
        self.actual.setFolder(folder)
        self.actual.setFilename(filename)
        result = self.actual.open()
        self.assertNotEqual(result, [])

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
        # success when folder exists and filename is valid
        self.actual.setFolder(self.temp_folder)
        self.actual.setFilename(self.temp_filename)
        result = self.actual.save()
        self.assertEqual(result, [])
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
        self.assertTrue(type(result) is LbTextFile)

    def test_delete(self):

        result = self.actual\
            .setFolder(self.temp_folder)\
            .setFilename(self.temp_filename)\
            .load(['a','b'])\
            .save()

        self.assertEqual(result, ['a', 'b'])
        self.assertTrue(result.exists())
        # delete when  exists
        result = self.actual.delete()
        # clear list
        self.assertEqual(result, [])

        self.assertFalse(result.exists())

    def test_isEmpty(self):
        self.assertTrue(self.actual.isEmpty())

        self.actual.setFolder(self.temp_folder).setFilename(self.temp_filename)




if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()