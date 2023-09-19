import os
import sys
#from pprint import pprint
import subprocess
import shutil
from lb_recorder import LbRecorder

class UtilityScript(dict, LbRecorder):
    def __init__(self):
        LbRecorder.__init__(self)
        self['fail'] = False
        self['fail_msg'] = []
    def ch_dir(self, folder):
        # self.addStep('ch_dir')
        os.chdir(folder)
        return self
    def copy_to(self, source_file_path, destination_folder):
        # source eg /Users/jameswilfong/Development/lyttlebit/00_std/lb_lib/.env
        # destination eg /Users/jameswilfong/Development/lyttlebit/00_next/lb_test/
        try:
            self.addStep('copy_to')
            shutil.copy2(source_file_path, destination_folder)
            # print(f"File '{source_file_path}' copied to '{destination_folder}' successfully.")
            self['copy_to'] = "ok, {}".format(str(source_file_path).split('/')[-1])
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

        # write a file to the project folder
        with open('{}/{}'.format(folder,filename), 'a') as f:
            f.write(test_line)
        self['write_to']=filename
        return self

def main():
    from pprint import pprint
    start_folder = os.getcwd() # script should start and stop in the same folder
    actual = UtilityScript()
    assert (actual)
    assert (actual.on_fail_exit()) # should be ok


if __name__ == "__main__":
    # execute as script
    main()
    #mainProjectScript()