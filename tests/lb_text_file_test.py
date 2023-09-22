import unittest
import os
from dep.pylyttlebit.lb_constants import LbC
from dep.pylyttlebit import LbTextFile
from dep.pylyttlebit.lb_exceptions import FolderNotFoundException, BadFileNameException, BadFolderNameException
from dep.pylyttlebit import LbUtil

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
        #self.TEMP_FILENAME = '{}.env'.format(str(__file__).split('/')[-1])
        # create a temp folder
        #self.temp_folder = '/'.join(str(__file__).split('/')[0:-1])
        #self.temp_folder = '{}/temp'.format(self.temp_folder)
        #LbUtil().create_folder(self.temp_folder)
        LbUtil().create_folder(LbC().TEMP_FOLDER)
    def tearDown(self):
        #print('tearDown')

        # remove all files in temp folder
        LbUtil().delete_folder_files(LbC().TEMP_FOLDER, '*')
        # remove temp folder
        LbUtil().delete_folder(LbC().TEMP_FOLDER)

    def tearDown_create_empty_file(self, folder=LbC().TEMP_FOLDER, filename=LbC().EMPTY_FILENAME):
        #print('create file', folder, filename)
        with open('{}/{}'.format(folder, filename), 'w') as f:
            f.writelines([''])
        exists = os.path.isfile('{}/{}'.format(folder,filename))
        self.assertTrue(exists)
        #self.assertTrue(LbUtil().file_exists(LbConstants().temp_folder, LbConstants().EMPTY_FILENAME))


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

    '''
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
    '''

    #def test_file_exists(self):
    #    folder = '/'.join(str(__file__).split('/')[0:-1])
    #    filename = str(__file__).split('/')[-1]
    #    notfile = 'aaaa.txt'

    #    # file does not exist when filename is None
    #    result = self.actual.file_exists()
    #    self.assertFalse(result)

    #    # file does not exist when filename is not None
    #    self.actual.setFilename(notfile)
    #    result = self.actual.file_exists()

    #    # file exists when folder and filename is not None and file is found
    #    self.actual.setFolder(folder)
    #    self.actual.setFilename(filename)
    #    result = self.actual.file_exists()
    #    self.assertTrue(result)

    def test_exists(self):

        # false when ~/None/None
        result = self.actual.exists()
        self.assertFalse(result)

        # folder exists but file does not
        self.actual.setFolder(LbC().TEMP_FOLDER)
        result = self.actual.exists()
        self.assertFalse(result)

        # folder exists and file exists
        #print('file       ', len(__file__))
        self.actual.setFolder('/'.join(str(__file__).split('/')[0:-1]))
        self.actual.setFilename(str(__file__).split('/')[-1])
        #print('test_exists {}/{}'.format(self.actual.getFolder(),self.actual.getFilename()))
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
        self.actual.setFolder(LbC().TEMP_FOLDER)
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
        self.actual.setFolder(LbC().TEMP_FOLDER)
        with self.assertRaises(BadFileNameException):
            self.actual.save()

        # create file when doesnt exist
        self.actual.setFolder(LbC().TEMP_FOLDER)     # set good folder
        self.actual.setFilename(LbC().TEMP_FILENAME) # set good filename
        self.assertFalse(self.actual.exists())      # prove file doesnt exist
        result = self.actual.save()                 # save empty file
        self.assertEqual(result, [])                # is empty

        # overwrite file when file exists
        self.actual.setFolder(LbC().TEMP_FOLDER)     # set good folder
        self.actual.setFilename(LbC().TEMP_FILENAME) # set good existing file
        result = self.actual.load(['a', 'b']).save()# load some data
        self.assertEqual(result, ['a', 'b'])
        result = LbTextFile().setFolder(LbC().TEMP_FOLDER).setFilename(LbC().TEMP_FILENAME).open()
        self.assertEqual(result, ['a', 'b'])

        # returns LbTextFile
        self.assertTrue(type(result) is LbTextFile)

    def test_saveAs(self):
        # save a file
        self.actual.setFolder(LbC().TEMP_FOLDER)
        self.actual.setFilename(LbC().TEMP_FILENAME)
        result = self.actual.save()
        self.assertEqual(result, [])

        # saveAs
        with self.assertRaises(BadFolderNameException):
            self.actual.saveAs(None,None)
        # fail when good folder with bad filename
        with self.assertRaises(BadFileNameException):
            self.actual.saveAs(LbC().TEMP_FOLDER, None)
        # fail when good folder name, good filename but folder doesnt exist
        with self.assertRaises(BadFileNameException):
            self.actual.saveAs(LbC().TEMP_FOLDER, None)
        # write empty file
        result = self.actual.saveAs(LbC().TEMP_FOLDER, LbC().TEMP_FILENAME)
        self.assertTrue(LbUtil().file_exists(LbC().TEMP_FOLDER, LbC().TEMP_FILENAME))
        # confirm file is empty
        self.assertEqual(result,[])
        # overwrite empty file with some data
        self.actual.load(['one','two'])
        result = self.actual.saveAs(LbC().TEMP_FOLDER, LbC().TEMP_FILENAME)
        self.assertEqual(result, ['one', 'two'])

        # returns LbTextFile
        self.assertTrue(type(result) is LbTextFile)

    def test_delete(self):
        # create a file to delete
        self.tearDown_create_empty_file()
        self.actual.setFolder(LbC().TEMP_FOLDER).setFilename(LbC().EMPTY_FILENAME)
        # delete when  exists
        result = self.actual.delete()
        # clear list
        self.assertEqual(result, [])        # list was cleard
        self.assertFalse(result.exists())   # file was removed
        # returns empty LbTextFile
        self.assertTrue(type(result) is LbTextFile)
        self.assertEqual(result, [])  # LbTextFile is empty

    def test_isEmpty(self):
        #print('test_isEmpty 1')
        # file is empty when file doesnt exist
        result = self.actual.isEmpty()
        self.assertTrue(not self.actual.exists() and result)
        #print('test_isEmpty 2')

        # file is empty when has no lines

        self.tearDown_create_empty_file()
        #print('test_isEmpty 3')

        result = self.actual\
            .setFolder(LbC().TEMP_FOLDER)\
            .setFilename(LbC().EMPTY_FILENAME)\
            .isEmpty()

        #print('test_isEmpty 4')
        #print('test_isEmpty 4.1 filelist', LbUtil().get_file_list(LbC().temp_folder,'*'))
        #print('test_isEmpty 4.2 result', result)
        #print('test_isEmpty 4.3 exists', self.actual.exists(), self.actual.getFilename() )

        self.assertTrue(result)
        #print('test_isEmpty 5')

        # return LbTextFile
        self.assertTrue(type(result) is bool)
        #print('test_isEmpty out')


if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()