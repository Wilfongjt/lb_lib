import os
import unittest
from dep.pylyttlebit import LbUtil
from dep.pylyttlebit.lb_exceptions import BadFolderNameException, FolderNotFoundException,SubfolderCopyException, FolderAlreadyExistsException
from dep.pylyttlebit.lb_constants import LbConstants
from dep.pylyttlebit.lb_constants import LbC
from os import listdir
from os.path import isfile, join
import shutil


class LbUtilTest(unittest.TestCase):

    def setUp(self) -> None:
        self.actual = LbUtil()
        # use a .env extention to avoid pushing to github
        #self.TEMP_FILENAME = '{}.env'.format(str(__file__).split('/')[-1])

        # create a temp folder in users home folder
        LbUtil().create_folder(LbConstants().TEMP_FOLDER)


    def tearDown(self) -> None:
        # remove all files and folders in temp folder
        if self.tearDown_folder_exists(LbConstants().TEMP_FOLDER):
            shutil.rmtree(LbConstants().TEMP_FOLDER)

    def tearDown_get_file_list(self, path, ext=None):
        #### Get List of File Names on request
        onlyfiles = []
        #print('listdir', path)
        exists = os.path.isdir('{}'.format(path))
        if not exists:
            return onlyfiles

        if len(listdir(path)) > 0:
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
            if ext != None and ext != '*':
                onlyfiles = [f for f in onlyfiles if f.startswith(ext) or f.endswith(ext)]

        # return list of filenames
        return [fn for fn in onlyfiles if '.DS_Store' not in fn]


    def tearDown_folder_exists(self, folder):
        #### Test if a given folder exists on request
        ##* folder exists when found on drive ... [x] has test
        exists = os.path.isdir('{}'.format(folder))
        return exists

    def tearDown_create_empty_file(self, folder=LbConstants().TEMP_FOLDER, filename=LbConstants().EMPTY_FILENAME):
        #print('create file', folder, filename)

        with open('{}/{}'.format(folder, filename), 'w') as f:
            f.writelines([''])
        exists = os.path.isfile('{}/{}'.format(folder,filename))
        self.assertTrue(exists)
        #self.assertTrue(LbUtil().file_exists(LbConstants().temp_folder, LbConstants().EMPTY_FILENAME))

    def test_copy_folder(self):
        result = None
        srcfolder = None
        dstfolder = None

        # fail when source folder not found
        with self.assertRaises(FolderNotFoundException):
            result = self.actual.copy_folder(srcfolder, dstfolder)

        # dont copy to subfolder of source
        srcfolder = '/'.join(str(__file__).split('/')[0:-1])
        dstfolder =  '{}/asubfolder'.format(srcfolder)

        with self.assertRaises(SubfolderCopyException):
            result = self.actual.copy_folder(srcfolder, dstfolder)

        # copy source folder, subfolders, and files to destination folder when source folder is found

        srcfolder = '/'.join(str(__file__).split('/')[0:-1])
        dstfolder = '{}/asubfolder'.format(LbConstants().TEMP_FOLDER)

        result = self.actual.copy_folder(srcfolder, dstfolder)
        self.assertNotEqual(len(self.tearDown_get_file_list(dstfolder)), 0)
        #if 1==1: return

        # dont overwrite destination folder
        with self.assertRaises(FolderAlreadyExistsException):
            result = self.actual.copy_folder(srcfolder, dstfolder)

        # return LbUtil
        self.assertTrue(result, LbUtil)

    def test_create_folder(self):
        # create all folders when needed ... [x] has test

        result = None
        with self.assertRaises(BadFolderNameException):
            result = self.actual.create_folder(None)

        folder = '/junk' # can create folder outside of users secure space
        with self.assertRaises(OSError):
            self.actual.create_folder(folder)
        # create when good folder name

        result = self.actual.create_folder(LbConstants().DISPOSABLE_FOLDER)
        self.assertTrue(type(result) is LbUtil)

        ##* return LbUtil ... [] has test
        self.assertTrue(result, LbUtil)

        #pass

    def test_current_directory(self):
        result = self.actual.current_directory()
        self.assertTrue(type(result) is str)

    #def test_create_empty_file(self):
    #    result = self.actual.create_empty_file(LbC().temp_folder, LbC().EMPTY_FILENAME)
    #    self.assertTrue(os.path.isfile('{}/{}'.format(LbC().temp_folder, LbC().EMPTY_FILENAME)))

    def test_delete_file(self):
        # delete a file that doesnt exist
        # confirm file doesnt exist
        exists = os.path.isfile('{}/{}'.format(LbConstants().TEMP_FOLDER, LbConstants().EMPTY_FILENAME))
        self.assertFalse(exists)

        # attempt a delete of non-existing file... delete is skipped when file doesnt exist
        result = self.actual.delete_file(LbConstants().TEMP_FOLDER, LbConstants().EMPTY_FILENAME)
        self.assertTrue(type(result) is LbUtil)

        # create empty file to delete and confirm exists
        self.tearDown_create_empty_file(folder=LbConstants().TEMP_FOLDER, filename=LbConstants().EMPTY_FILENAME)

        # make sure file exists
        exists = os.path.isfile('{}/{}'.format(LbConstants().TEMP_FOLDER, LbConstants().EMPTY_FILENAME))
        self.assertTrue(exists)

        # delete file
        result = self.actual.delete_file(LbConstants().TEMP_FOLDER, LbConstants().EMPTY_FILENAME)

        # confirm delete
        exists = os.path.isfile('{}/{}'.format(LbConstants().TEMP_FOLDER, LbConstants().EMPTY_FILENAME))
        self.assertFalse(exists)

        # confirn LbUnit
        self.assertTrue(type(result) is LbUtil)

    def test_delete_folder(self):

        # attempt to delete a file that doesnt exist

        createfolder = None
        deletefolder = None
        with self.assertRaises(BadFolderNameException):
            LbUtil().create_folder(createfolder)

        # delete a folder, subfolders and file
        createfolder = '{}/temporary/anothertemp'.format(LbConstants().TEMP_FOLDER)
        deletefolder = '{}/temporary'.format(LbConstants().TEMP_FOLDER)

        # create a folder
        LbUtil().create_folder(createfolder)

        # add an empty file and assert it exists
        self.tearDown_create_empty_file(folder=createfolder)

        # confirm folder exists
        self.assertTrue(os.path.isdir(createfolder))

        # delete folder
        result = LbUtil().delete_folder(deletefolder)

        # confirm folder is deleted
        self.assertFalse(os.path.isdir(createfolder))

        # confirn LbUnit
        self.assertTrue(type(result) is LbUtil)

    def test_delete_folder_files(self):
        result = None
        # create two files
        folder = '{}/delete_folder_files'.format(LbConstants().TEMP_FOLDER)
        LbUtil().create_folder(folder)

        # add two empty files and assert existance
        self.tearDown_create_empty_file(folder=folder,filename='one.env')
        self.tearDown_create_empty_file(folder=folder,filename='two.env')

        # delete both files
        result = LbUtil().delete_folder_files(folder,ext='*')

        # confirm deleted
        self.assertTrue(self.tearDown_get_file_list(folder)==[])

        # confirn LbUnit
        self.assertTrue(type(result) is LbUtil)

    def test_get_env_value(self):
        # None when not found
        result = self.actual.get_env_value('NotAKey')
        self.assertEqual(result, 'TBD')

        result = self.actual.get_env_value('USER')
        self.assertTrue(result != 'TBD')

        # str when found
        self.assertTrue(type(result) is str)


    #def test_create_delete_folder_file(self):
    #    # none existant folder
    #    filename = 'abcedef.txt'
    #    folder = '{}/abcd'.format(os.path.expanduser('~'))
    #    with self.assertRaises(BadFolderNameException):
    #        result = self.actual.create_folder(None)
    #    # create the folder
    #    result = self.actual.create_folder(folder).folder_exists(folder)
    #    self.assertTrue(result)
    #    # create folder twice
    #    result = self.actual.create_folder(folder).folder_exists(folder)
    #    self.assertTrue(result)
    #    # add file
    #    with open('{}/{}'.format(folder, filename), 'w') as f:
    #        line_list = []  # empty file
    #        f.writelines(['{}\n'.format(ln) for ln in line_list])
    #    with open('{}/{}'.format(folder, 'blind_delete.txt'), 'w') as f:
    #        line_list = []  # empty file
    #        f.writelines(['{}\n'.format(ln) for ln in line_list])
    #    # delete file
    #    result = self.actual.delete_file(folder, filename).file_exists(folder, filename)
    #    self.assertFalse(result)

    #    # delete files from folder
    #    result = self.actual.delete_folder_files(folder, 'txt').get_file_list(folder)
    #    self.assertEqual(result, [])
    #    # delete folder
    #    result = self.actual.delete_folder(folder).folder_exists(folder)
    #    self.assertFalse(result)

    #    #copy_folder(self, src_folder, dst_folder)
    def test_file_age(self):
        folder = os.getcwd()
        filename = str(__file__).split('/')[-1]
        result = self.actual.file_age(folder, filename)
        #print('result', result)
        self.assertTrue(result >= 0)
        self.assertTrue(type(result) is float)

    def test_file_exists(self):
        # file doesnt exist when folder is none and file is none
        result = self.actual.file_exists(None, None)
        self.assertFalse(result)
        # file doesnt exist when good file not found
        result = self.actual.file_exists(os.getcwd(),'xqd.abc')
        self.assertFalse(result)
        # file found when good folder and good filename
        filename = str(__file__).split('/')[-1]
        folder = '/'.join(str(__file__).split('/')[0:-1])
        result = self.actual.file_exists(folder, filename)
        self.assertTrue(result)
        self.assertTrue(type(result) is bool)

    def test_folder_exists(self):
        # not found
        result = self.actual.folder_exists('/notafolder')
        self.assertFalse(result)
        # found
        result = self.actual.folder_exists(os.getcwd())
        self.assertTrue(result)
        self.assertTrue(type(result) is bool)


    def test_get_file_extension(self):
        result = self.actual.get_file_extension(str(__file__))
        self.assertEqual(result, 'py')
        self.assertTrue(type(result) is str)


    def test_get_file_list(self):
        folder = os.getcwd().replace('/tests','')
        #print(LbConstants().APP_FOLDER_KEY, folder)

        ##* return [] when folder is None
        result = self.actual.get_folder_list(None)
        self.assertTrue(result == [])

        ##* returns [] when folder NOT found
        result = self.actual.get_folder_list('/notafolder')
        self.assertTrue(result == [])
        #print('test_get_file_list folder', folder)
        result = self.actual.get_folder_list(folder)
        self.assertNotEqual(result, [])

        ##* return all files when ext = "*"
        result = self.actual.get_folder_list(folder)
        self.assertNotEqual(result, [])

        ##* return files when file has specified extention
        result = self.actual.get_folder_list(folder)
        self.assertNotEqual(result, [])

        self.assertTrue(type(result) is list)

    def test_get_folder_list(self):

        ##* return [] when folder is None
        result = self.actual.folder_exists(None)
        self.assertFalse(result == [])

        ##* returns [] when folder NOT found
        result = self.actual.folder_exists('/notafolder')
        self.assertFalse(result==[])

        ##* returns [] when no folders found
        result = self.actual.get_folder_list(os.path.expanduser('~'))
        self.assertTrue(result != [])

        ##* return list
        self.assertTrue(type(result) is list)

    def test_is_empty(self):
        # folder=None filename is None
        result = self.actual.is_empty(None, None)
        self.assertTrue(result)
        # create empty file

        self.tearDown_create_empty_file(LbC().TEMP_FOLDER, LbC().EMPTY_FILENAME)
        #print('filelist',self.tearDown_get_file_list(LbC().temp_folder,'*'))

        # file should exist
        result = self.actual.is_empty(LbC().TEMP_FOLDER, LbC().EMPTY_FILENAME)
        self.assertTrue(result)

        filename = str(__file__).split('/')[-1]
        folder = '/'.join(str(__file__).split('/')[0:-1])
        #print('folder', folder)
        result = self.actual.is_empty(folder, filename )
        self.assertFalse(result)

if __name__ == "__main__":
    # execute as script
    unittest.main()