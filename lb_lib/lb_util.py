
import os
from os.path import isfile, join
from os import listdir
import shutil
from lb_lib.lb_exceptions import BadFileNameException, \
                                 BadFolderNameException, \
                                 FolderNotFoundException, \
                                 FolderAlreadyExistsException, \
                                 SubfolderCopyException

class LbUtil():
    def hello_world(self):
        print("I am LbUtil!")

    def copy_folder(self, src_folder, dst_folder):
        #### Copy source folder and files on request
        ##* Copy fails when source folder doesnt exist ... [x] has test
        if not self.folder_exists(src_folder):
            raise FolderNotFoundException('Source folder {}'.format(src_folder))
        ##* Copy fails when destination folder is contained in source folder ... [x] has test
        if src_folder in dst_folder:
            raise SubfolderCopyException('Source folder {} contains {}'.format(src_folder,dst_folder))
        ##* dont overwrite destination folder when found ... [x] has test
        if self.folder_exists(dst_folder):
            raise FolderAlreadyExistsException('Destination folder already exists "{}"'.format(dst_folder))
        ##* copy source folder, subfolders, and files to destination folder when source folder is found ... [x] has test
        shutil.copytree(src_folder,
                        dst_folder,
                        dirs_exist_ok=True)
        ##* return LbUtil ... [x] has test
        return self

    def create_folder(self, folder):
        #### Create all folders in a given path on request
        # No trailing / in folder
        # path = folder
        if not folder:
            raise BadFolderNameException('BadFolderName {}'.format(folder))
        ##* create all folders when needed ... [x] has test
        p = ''
        for sub in folder.split('/'):
            if len(sub) > 0:
                p += '/{}'.format(sub)
                # print('check folder ', p)
                if not os.path.exists(p):
                    # print('create folder ', p)
                    os.mkdir('{}/'.format(p))
        ##* return LbUtil ... [x] has test
        return self

    def delete_file(self, folder, file_name):
        #### Delete file on request
        if self.file_exists(folder, file_name):
            ##* delete file when folder and file are found ... [x] has test
            os.remove("{}/{}".format(folder, file_name))

        ##* skip file delete when folder and file are NOT found ... [x] has test

        ##* return LbUtil ... [x] has test
        return self


    def delete_folder(self, folder):
        #### Delete folder on request
        # Note: You can only remove empty folders.

        ##* remove all files and folders in folder ... [x] has test
        if self.folder_exists(folder):
            shutil.rmtree(folder)

        ##* return LbUtil ... [x] has test
        return self

    def delete_folder_files(self, folder, ext):
        #### Delete all files in a folder on request
        # ext = 'js'
        ##* Delete all files when files are found in a folder ... [x] has test
        self.deleted_file_list = self.get_file_list(folder, ext)
        for filename in self.deleted_file_list:
            self.delete_file(folder, filename)
        ##* return LbUtil ... [x] has test
        return self

    def file_exists(self, folder, filename):
        #### Test if a given folder and file exist on request

        ##* file exists when folder exists and file exists ... [x] has test
        exists = os.path.isfile('{}/{}'.format(folder, filename))

        ##* return bool ... [x] has test
        return exists

    def folder_exists(self, folder):
        #### Test if a given folder exists on request
        ##* folder exists when found on drive ... [x] has test
        exists = os.path.isdir('{}'.format(folder))
        ##* returns bool ... [x] has test
        return exists

    def get_file_extension(self, filename):
        #### Get file extension on request
        ext = filename.split('.')[-1]
        ##* return extension/string ... [x] has test
        return ext

    def get_file_list(self, path, ext=None):
        #### Get List of File Names on request
        onlyfiles = []

        ##* return [] when folder is None ... [x] has test
        if not path:
            return []

        ##* returns [] when folder NOT found ... [x] has test
        if not self.folder_exists(path):
            return []
        # get list of files
        lst = listdir(path)

        ##* returns [] when no files found ... [ ] has test

        if lst == []:
            return []
        ##* return all files when ext = "*" ... [x] has test
        onlyfiles = [f for f in lst if isfile(join(path, f))]

        ##* return files when file has specified extention ... [x] has test
        if ext != None and ext != '*':
            onlyfiles = [f for f in onlyfiles if f.startswith(ext) or f.endswith(ext)]

        ##* return list of filenames when files found [x] has test
        return [fn for fn in onlyfiles if '.DS_Store' not in fn]

    def get_folder_list(self, path):
        #### Get List of Folder Names on request

        onlyfolders = []
        ##* return [] when folder is None ... [x] has test
        if not path:
            return []

        ##* returns [] when folder NOT found ... [x] has test
        if not self.folder_exists(path):
            return []

        # get list of folders and files
        lst = listdir(path)

        ##* returns [] when no folders found ... [x] has test
        if lst == []:
            return []

        onlyfolders = ['{}/{}'.format(path, f) for f in lst if not isfile(join(path, f))]

        ## return list ... [x] has test
        return [fn for fn in onlyfolders]

def main():
    from lb_lib.lb_doc_comments import LbDocComments
    print('lb_util')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()




if __name__ == "__main__":
    # execute as script
    main()