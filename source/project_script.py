import os
#from lb_util import LbUtil
#from lb_recorder import LbRecorder
from source.utility_script import UtilityScript

class ProjectScript(UtilityScript):
    def __init__(self):
        super().__init__()
        self.WORKSPACE_FOLDER = '{}/Development/{}/{}'
        self.PROJECT_FOLDER = '{}/Development/{}/{}/{}'
    def assertTrue(self, expression):
        assert (expression == True)
        return self
    def create_workspace(self, folder):
        self.addStep('[Create-workspace]')
        if not self.folder_exists(folder):
            os.makedirs(folder, exist_ok=True)
            self['create_workspace'] = 'created @ {}'.format(folder)
        else:
            self['create_workspace'] = 'existing @ {}'.format(folder)
            self.addStep('(workspace:{})'.format(folder.split('/')[-1]))
        return self
    def get_input(self, msg, default, hardstop=True):
        #### Prompt user for input
        rc = '{} [{}] : '.format(msg, default)
        rc = input(rc)
        if not rc:
            rc = default
        ##* hard stop when user types 'n','N','x','X','q' or 'Q'
        if rc in ['n','N','x','X','q','Q','TBD']:
            if hardstop:
                print('stopping...Stopped')
                exit(0)
        ##* return str
        return rc
    def get_workspace_folder(self):

        fldr=self.WORKSPACE_FOLDER.format(os.environ['HOME']
                                     , os.environ["WS_ORGANIZATION"]
                                     , os.environ["WS_WORKSPACE"])
        return fldr
    def get_project_folder(self, subfolder=None):

        if 'WS_ORGANIZATION' not in os.environ:
            # this is for testing
            fl = self.PROJECT_FOLDER.format(os.environ['HOME']
                                            , self["WS_ORGANIZATION"]
                                            , self["WS_WORKSPACE"]
                                            , self["GH_PROJECT"])
        else:
            fl=self.PROJECT_FOLDER.format(os.environ['HOME']
                                          , os.environ["WS_ORGANIZATION"]
                                          , os.environ["WS_WORKSPACE"]
                                          , os.environ["GH_PROJECT"])

        if subfolder:
            fl = '{}/{}'.format(fl,subfolder)
        return fl
    def is_project_folder(self):
        # is the current folder a bin folder
        # eg ~/Development/organization/workspace/bin
        # must have Development at forth position from end

        rc = False

        fldr = os.getcwd()
        dev_pos = -4
        rc = self.validate_folder(fldr, dev_pos)

        return rc
    def is_workspace_folder(self):
        # is the current folder a workspace folder
        # eg ~/Development/organization/workspace/bin
        # must have Development at forth position from end

        rc = False

        fldr = os.getcwd()
        dev_pos = -3
        rc = self.validate_folder(fldr, dev_pos)

        return rc
    def load_env(self, folder=None, filename=None):
        #### Load Enviroment Variables on request
        self.addStep('[Load-env]')
        env_file_name = filename or self.get('env_file_name')
        env_folder_name = folder or self.get('env_folder_name') or '/'.join(os.getcwd().split('/')[0:-1])
        print('env_file_name',env_file_name)
        print('env_folder_name',env_folder_name)
        line_list=[]
        if self.file_exists(env_folder_name, env_file_name):
            with open('{}/{}'.format(env_folder_name, env_file_name)) as file:
                line_list = file.readlines()
                line_list = [ln.replace('\n', '') for ln in line_list]
                #self['environment']='read'
                #self.addStep('read')

        for ln in line_list:
            if '=' in ln:
                ln = ln.split('=')
                self.set(ln[0],ln[1])
                os.environ[ln[0]]=ln[1]
                #self['environment'] += '{}'.format(self['environment'],ln[0])
                self.addStep('variable')
        #pprint(self)
        return self
    def report(self):
        print('hasFailed', self.hasFailed())
    def set_env(self, key, value="TBD"):
        ##* add environment variable when not found
        line_list = []

        ##* open file and read text lines
        env_file_name=self.get('env_file_name')
        env_folder_name=self.get('env_folder_name')
        if self.file_exists(env_folder_name, env_file_name):
            with open('{}/{}'.format(env_folder_name, env_file_name)) as file:
                line_list = file.readlines()
                line_list = [ln.replace('\n', '') for ln in line_list]

        ##* find "key=" then replace with "key=value"
        i=0
        found=False
        for ln in line_list:
            if ln.startswith('{}='.format(key)):
                found = True
                line_list[i]='{}={}'.format(key,value)
                ##* set stash variable
                self.set(key, value)
                #self.addStep('set_env')
                ##* set envioron variable
                os.environ[key]=value
                break
            i+=1

        ##* key not found then append

        if not found:
            line_list.append('{}={}'.format(key,value))
            ##* set stash variable
            self.set(key,value)
            self.addStep('set_env-add')
            ##* set envioron variable
            os.environ[key] = value

        ##* save after every set

        with open('{}/{}'.format(env_folder_name, env_file_name), 'w') as f:
            f.writelines(['{}\n'.format(ln) for ln in line_list])

        return self
    def validate_folder(self, folder, dev_pos):
        # is the given folder a bin folder
        # eg ~/Development/organization/workspace/bin
        # bin must have Development at forth position from end
        # workspace must have Development at third position from end

        rc = True
        fldr = folder.split('/')
        # Development

        if fldr[dev_pos] != 'Development':
            rc = False

        return rc
    def validate_input(self, key, value):
        ##* test for Null key
        ##* test for Null value
        ##* test for TBD value
        #self.addStep('validate-input')
        if not key:
            self.addStep('invalid')
            self.set_fail(True, 'Key is None')
        elif not value:
            self.addStep('invalid')
            self.set_fail(True, '{} value is None'.format(key))
        elif value == 'TBD':
            self.addStep('invalid')
            self.set_fail(True, '{} value is TBD'.format(key))
        else:
            self.addStep('valid')
        return self

def mainProjectScript():
    print('Testing mainProjectScript')
    folder = '/'.join(os.getcwd().split('/')[0:-1])
    print('folder',folder)
    os.chdir(folder) # switch to bin folder
    actual = ProjectScript()
    assert (actual.validate_folder(folder,-4))
    assert (actual.is_project_folder())
    assert (not actual.validate_folder(folder,-3))
    assert (not actual.is_workspace_folder())
    folder = '/'.join(folder.split('/')[0:-1])
    assert (actual.validate_folder(folder,-3))
    os.chdir('..') # switch to workspace folder
    assert (actual.is_workspace_folder())

def main():
    start_folder = os.getcwd() # script should start and stop in the same folder
    actual = ProjectScript()
    assert (actual)
    assert (actual.on_fail_exit()) # should be ok

def main_document():
    from dep.pylyttlebit import LbDocComments
    print('project_script')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

if __name__ == "__main__":
    # execute as script
    main()
    #mainProjectScript()