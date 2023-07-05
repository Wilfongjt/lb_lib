
import os
from os.path import isfile, join
from os import listdir
import shutil
from lb_lib.lb_exceptions import BadFileNameException, BadFolderNameException


class LbUtil():
    def hello_world(self):
        print("I am LbUtil!")
    def get_file_extension(self, filename):
        lst = filename.split('.')[1:]
        ext = '.'.join(lst)
        return ext

    def folder_exists(self, folder):
        exists = os.path.isdir('{}'.format(folder))
        return exists

    def file_exists(self, folder, filename):
        exists = os.path.isfile('{}/{}'.format(folder, filename))
        return exists

    def copy_folder(self, src_folder, dst_folder):

        shutil.copytree(src_folder,
                        dst_folder,
                        dirs_exist_ok=True)

        return self

    def create_folder(self, folder):
        # create all folders in a given path
        # No trailing / in folder
        # path = folder
        if not folder:
            raise BadFolderNameException('BadFolderName {}'.format(folder))
        try:
            p = ''
            for sub in folder.split('/'):
                if len(sub) > 0:
                    p += '/{}'.format(sub)
                    # print('check folder ', p)
                    if not os.path.exists(p):
                        # print('create folder ', p)
                        os.mkdir('{}/'.format(p))

            # if not self.folder_exists('{}/'.format(path)):
            #    os.mkdir('{}/'.format(path))

            # print("Successfully created the directory %s " % path)
        except OSError:
            path = None
            print("FAILURE: Creation of the directory %s failed" % path)

        return self

    def delete_folder(self, folder):
        # Note: You can only remove empty folders.
        if self.folder_exists(folder):
            # print('delete_folder', folder)
            os.rmdir(folder)
        return self

    def delete_folder_files(self, folder, ext):
        # ext = 'js'
        self.deleted_file_list = self.get_file_list(folder, ext)
        for filename in self.deleted_file_list:
            self.delete_file(folder, filename)

        return self

    def delete_file(self, folder, file_name):

        if self.file_exists(folder, file_name):
            os.remove("{}/{}".format(folder, file_name))
        return self

    def get_file_list(self, path, ext=None):
        onlyfiles = []

        if len(listdir(path)) > 0:
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
            if ext != None and ext != '*':
                onlyfiles = [f for f in onlyfiles if f.startswith(ext) or f.endswith(ext)]

        # return onlyfiles
        return [fn for fn in onlyfiles if '.DS_Store' not in fn]

    def get_folder_list(self, path):
        onlyfolders = []

        if len(listdir(path)) > 0:
            onlyfolders = ['{}/{}'.format(path, f) for f in listdir(path) if not isfile(join(path, f))]
            # if ext != None:
            #    onlyfolders = [f for f in onlyfolders if f.startswith(ext) or f.endswith(ext)]

        # return onlyfiles
        return [fn for fn in onlyfolders]

def main():
    print('lb_util')

if __name__ == "__main__":
    # execute as script
    main()