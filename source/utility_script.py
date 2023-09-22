import os
import sys
#from pprint import pprint
import subprocess
import shutil
from source.lb_recorder import LbRecorder
from os import listdir
from os.path import isfile, join

class UtilityScript(dict, LbRecorder):
    def __init__(self):
        LbRecorder.__init__(self)
        self['fail'] = False
        self['fail_msg'] = []
    def ch_dir(self, folder):
        # self.addStep('ch_dir')
        os.chdir(folder)
        return self
    def copy_to(self, source_file_path, destination_folder, overwrite=False):
        #### copy file to another folder
        # source eg /Users/jameswilfong/Development/lyttlebit/00_std/lb_lib/.env
        # destination eg /Users/jameswilfong/Development/lyttlebit/00_next/lb_test/
        try:
            fn = str(source_file_path).split('/')[-1]
            if not self.file_exists(destination_folder, fn):
                self.addStep('copy_to')
                shutil.copy2(source_file_path, destination_folder)
                self['copy_to'] = "ok, {}".format(fn)
            elif overwrite:
                self.addStep('copy_to')
                shutil.copy2(source_file_path, destination_folder)
                self['copy_to'] = "overwrite, {}".format(fn)
            else:
                self.addStep('copy_to')
                self['copy_to'] = "skip, {}".format(fn)

        except Exception as e:
            # print(f"Error copying file: {str(e)}")
            self.set_fail(True, f"Error copying file: {str(e)}")
        return self
    def exit(self):
        self.addStep('exit')
        sys.exit(2)
        return self
    def folder_exists(self, folder):
        #self.addStep('folder_exists')

        #### Test if a given folder exists on request
        ##* folder exists when found on drive ... [x] has test
        exists = os.path.isdir('{}'.format(folder))
        ##* returns bool ... [x] has test
        return exists

    def create_folders(self, folder):
        #self.addStep('[Create-folder]')
        if not self.folder_exists(folder):
            os.makedirs(folder, exist_ok=True)

        return self
    def file_exists(self, folder, filename):
        #### Test if a given folder and file exist on request

        ##* file exists when folder exists and file exists ... [x] has test
        exists = os.path.isfile('{}/{}'.format(folder, filename))

        ##* return bool ... [x] has test
        return exists

    def get(self, key):
        if key not in self:
            self.set_fail(True, '{} Not Found'.format(key))
            raise Exception('{} Not Found'.format(key))
        return self[key]
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

    def get_env_value(self, key):
        #self.addStep('get_env_value')
        rc = None
        if key in os.environ:
            rc=os.environ[key]
        return rc
    def hasFailed(self):
        return self['fail']
    def on_fail_exit(self):
        if self['fail']:
            self.addStep('failed')
            self.report()
            # print('fails when "{}"'.format(self['fail_msg']))
            sys.exit(1)
        return self
    def print(self, ln):
        print(ln)
        return self
    def set(self, key, value):
        #self.addStep(key)
        self[key] = value
        return self
    def set_fail(self, tf, msg=None):
        #### Generalize Fail
        self['fail'] = tf
        self['fail_msg'].append(msg.replace('\n',' '))
        return self
    def subprocess(self, command, verbose=False):
        rc = False
        ret = subprocess.run(command, capture_output=True, shell=True)
        if verbose:
            self.print('subprocess'.format(command))
        if ret.returncode != 0:
            self.set_fail(True, ret.stderr.decode('ascii'))
            if verbose:
                self.print('    - ret {}'.format(ret))
            #rc= ret.stderr.decoce('ascii')
        else:
            if verbose:
                self.print('    - ret {}'.format(ret))
            rc = ret.stdout.decode('ascii').strip()
        return rc
    def write_to(self, folder, filename, test_line):
        self.addStep('write-to')

        # write a file to the bin folder
        with open('{}/{}'.format(folder,filename), 'a') as f:
            f.write(test_line)
        self['write_to']=filename
        return self

def main():
    start_folder = os.getcwd() # script should start and stop in the same folder
    actual = UtilityScript()
    assert (actual)
    assert (actual.on_fail_exit()) # should be ok

def main_document():
    from dep.pylyttlebit import LbDocComments
    print('utility_script')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()


if __name__ == "__main__":
    # execute as script
    main()
    #mainProjectScript()