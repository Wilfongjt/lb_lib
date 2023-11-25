import os
import sys
from pprint import pprint
import subprocess
import shutil
from lb_util import LbUtil
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
        #self.addStep(name)
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
    def get_workspace_folder(self):

        fldr=self.WORKSPACE_FOLDER.format(os.environ['HOME']
                                     , os.environ["WS_ORGANIZATION"]
                                     , os.environ["WS_WORKSPACE"])
        return fldr
    def get_project_folder(self):
        fl=self.PROJECT_FOLDER.format(os.environ['HOME']
                                      , os.environ["WS_ORGANIZATION"]
                                      , os.environ["WS_WORKSPACE"]
                                      , os.environ["GH_PROJECT"])
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
        self.addStep('[Load-env]')
        env_file_name = filename or self.get('env_file_name')
        env_folder_name = folder or self.get('env_folder_name') or os.getcwd()
        line_list=[]
        if LbUtil().file_exists(env_folder_name, env_file_name):
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
        if LbUtil().file_exists(env_folder_name, env_file_name):
            with open('{}/{}'.format(env_folder_name, env_file_name)) as file:
                line_list = file.readlines()
                line_list = [ln.replace('\n', '') for ln in line_list]

        ##* find "name=" then replace with "name=value"
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

        ##* name not found then append

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
        ##* test for Null name
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
    os.chdir('../..') # switch to workspace folder
    assert (actual.is_workspace_folder())

class GitCommands(ProjectScript):
    def __init__(self):
        super().__init__()
        self.GIT_CURR_BRANCH_COMMAND="git symbolic-ref --short HEAD 2>/dev/null"
        self.GIT_HAS_BRANCH_COMMAND='git branch'
        self.GIT_CHECKOUT_BRANCH_TEMPLATE='git checkout {}' # <branch name>
        self.GIT_UNCOMMITTED_FILES_COMMAND='git status --porcelain'
        self.GIT_PULL_ORIGIN_TEMPLATE = 'git pull origin {}'
        self.GIT_PUSH_ORIGIN_TEMPLATE = 'git push origin {}'
    def checkout_branch(self, folder, branch_name):
        # change folder and set branch
        # checkout when branch_name != branch_current
        # fail when current branch has uncommitted file(s)

        last_folder = os.getcwd() # change back when fail
        self.addStep('checkout')
        #self.addStep('(bin:{})'.format(self.get_project_name(folder)))

        self.ch_dir(folder) # change to new folder

        #self.addStep('checkout-branch')

        command=self.GIT_CHECKOUT_BRANCH_TEMPLATE.format(branch_name)
        ret = subprocess.run(command, capture_output=True, shell=True)
        # print(ret)
        if ret.returncode != 0:
            self.set_fail(True, ret.stderr.decode('ascii'))
            self.addStep('({})'.format('failed'))
            self.ch_dir(last_folder)
        else:
            rc = ret.stdout.decode('ascii').strip()
            self.addStep('(bin:{}, branch: {})'.format(self.get_project_name(),branch_name))

        #self.ch_dir(last_folder)

        return self
    def create_branch(self, project_folder=None, branch=None):
        #print('bin-name {}'.format(self.get_project_name(project_folder)))
        #print('create branch {} project_folder {}'.format(branch, project_folder))
        self.addStep('[Create-branch]')

        ##* restore starting folder
        #last_folder = os.getcwd()

        ##* dont create main
        if not branch:
            raise Exception('create_branch invalid branch {}'.format(branch))

        if not self.is_project(project_folder=project_folder):
            raise Exception('bin NOT FOUND: {}'.format(project_folder))

        if self.has_branch(project_folder, branch):
            ##* dont recreate a branch
            self['create_branch'] = 'found for {} @ {}'.format(branch, project_folder)
            self.addStep('(branch: {})'.format(self.get_branch_current(folder=project_folder)))
            return self

        #self.ch_dir(project_folder)

        command = self.GIT_CREATE_BRANCH_TEMPLATE.format(branch)
        ret = subprocess.run(command, capture_output=True, shell=True)
        #print("create_branch ret ",ret)

        if ret.returncode != 0:
            self['create_branch'] = '"{}"'.format(ret.stdout.decode('ascii').replace('\n', ''))
            self.addStep('failed')
        else:
            self['create_branch'] = 'created for {} @ {}'.format(branch, project_folder)
            self.addStep('(branch: {})'.format(self.get_branch_current(folder=project_folder)))
        #self.ch_dir(last_folder)
        return self
    def get_project_name(self):
        #pprint(os.environ)
        if 'GH_PROJECT' in os.environ:
            self['project_name']=os.environ['GH_PROJECT']
        else:
            self['project_name']='TBD'
        return self['project_name']
    def get_branch_current(self, folder=None):
        # folder is the project_folder
        rc = None

        last_folder = os.getcwd()
        if folder:
            self.ch_dir(folder)

        command = self.GIT_CURR_BRANCH_COMMAND
        #rc = self.subprocess(command)
        #print('get_branch_current rc {}'.format(rc))
        ret = subprocess.run(command, capture_output=True, shell=True)
        #print('ret', ret)
        #rc = self.subprocess(command)
        #print('get_branch_current rc {}'.format(rc))

        if ret.returncode != 0:
            self.set_fail(True, ret.stderr.decode('ascii'))
        else:
            rc = ret.stdout.decode('ascii').strip()

        self.ch_dir(last_folder)
        #print('get_branch_current', rc)
        return rc
    def get_branches(self,project_folder):
        if not self.folder_exists(project_folder):
            return []

        self.ch_dir(project_folder)
        command = self.GIT_HAS_BRANCH_COMMAND
        std_out = self.subprocess(command)
        std_out = [br for br in std_out.split() if br != '*']
        self['branches'] = std_out

        return self['branches']
    def getUncommittedFiles(self):
        rc = ''
        command=self.GIT_UNCOMMITTED_FILES_COMMAND
        ret = subprocess.run(command, capture_output=True, shell=True)
        #print(ret)
        if ret.returncode != 0:
            self.addStep('(failed)')
        else:
            #self.addStep('(uncommitted)')
            rc = ret.stdout.decode('ascii')
            rc = rc.split('\n')
            rc = [f.strip().replace('  ',' ').split(' ') for f in rc if f != '']
            rc = [{"track": t[0], "file": t[1]} for t in rc]
            #print('rc',rc)
        return rc
    def has_branch(self, project_folder,  branch_name):
        rc = False
        command = self.GIT_HAS_BRANCH_COMMAND
        sp = self.subprocess(command)
        #print('has_branch', sp)
        if branch_name in sp:
            rc = True

        return rc
    def is_project(self, project_folder):
        # check folder for .git

        rc=False
        fldr = '{}/.git'.format(project_folder)

        if self.folder_exists(fldr):
            rc=True

        return rc
    def pull_origin(self,project_folder, branch):
        self.addStep('pull-origin')
        #self.addStep('(pull-origin: {})'.format(branch))
        if branch != self.get_branch_current(folder=project_folder):
            self.set_fail(True, 'Unexpected branch')
            return self

        last_folder = os.getcwd()
        self.ch_dir(project_folder)
        #self.addStep('(pull-origin: {})'.format(branch))

        #command =  'git pull origin {}'.format(branch)

        command = self.GIT_PULL_ORIGIN_TEMPLATE.format(branch)
        ret = subprocess.run(command, capture_output=True, shell=True)
        # print(ret)
        if ret.returncode != 0:
            self.set_fail(True, ret.stderr.decode('ascii'))
            self.addStep('({})'.format('failed'))
        else:
            rc = ret.stdout.decode('ascii').strip()
            self.addStep('(bin:{},branch:{})'.format(self.get_project_name(),self.get_branch_current(project_folder)))
            #self.addStep('({})'.format(self.get_branch_current(project_folder)))

        self.ch_dir(last_folder)
        return self

class GitScript(GitCommands):
    def __init__(self):
        super().__init__()
        self['env_folder_name']=os.getcwd()
        self['env_file_name']='.env'

        self.GIT_URL_TEMPLATE = 'https://github.com/{}/{}.git'
        self.GIT_CLONE_TEMPLATE = 'git clone {}' # project_url
        self.GIT_CREATE_BRANCH_TEMPLATE = 'git branch {}' #
        self.GIT_STAGE_TEMPLATE='git add .' # no variables
        self.GIT_COMMIT_TEMPLATE='git commit -m {}' # GH_MESSAGE
        self.GIT_REBASE = 'git rebase {}'
        self.OPEN_GOOGLE_CHROME_TEMPLATE = 'open -a "Google Chrome" "https://github.com/{}/{}"'
        #self.GIT_CURR_BRANCH_COMMAND="git symbolic-ref --short HEAD 2>/dev/null"

        #self.GIT_HAS_BRANCH_COMMAND='git branch'
        #self.GIT_CHECKOUT_BRANCH_TEMPLATE='git checkout {}' # <branch name>
    def validate_inputs(self, prefix=['WS_', 'GH_']):
        self.addStep('[Validate-inputs]')

        ## fail when inputs are invalid
        for key in os.environ:
            for pfx in prefix:
                if key.startswith(pfx):
                    self.validate_input(key, os.environ[key])

        return self
    def clone_project_in(self, gh_user, gh_project, workspace_folder):
        self.addStep('[Clone-bin]')

        project_folder='{}/{}'.format(workspace_folder,gh_project)
        project_url = self.GIT_URL_TEMPLATE.format(gh_user, gh_project)
        #last_folder=os.getcwd()
        self.ch_dir(workspace_folder)
        ##* folder exists when found on drive
        exists = os.path.isdir('{}'.format(project_folder))
        if exists:
            self['clone_project']='found @ {}'.format(project_folder)
            self['project_name'] = gh_project
            self.addStep('cloned')
            self.addStep('(bin:{})'.format(self.get_project_name()))
            # self.addStep('(bin: {})'.format(self.get_project_name(project_folder)))
        else:
            self.addStep('cloning')
            command = self.GIT_CLONE_TEMPLATE.format(project_url)
            ret = subprocess.run(command, capture_output=True, shell=True)
            print('ret',ret)
            if ret.returncode != 0:
                self['clone_project']=str(ret.stderr)
                self.addStep('(failed)')
            else:

                self['clone_project']='created @ {}'.format(project_folder)
                self['project_name']=gh_project
                self.addStep('(bin:{})'.format(self.get_project_name()))

                self.checkout_branch(project_folder, 'main')

        #self.ch_dir(last_folder)
        return self
    def stage_branch(self, gh_branch, project_folder):
        #
        # change folder when project_folder is NOT equal to current folder
        # stage branch when branch is equal to current branch
        # change folder back to original folder on return
        # dont stage main branch
        self.addStep('[Stage-branch]'.format(gh_branch))

        #last_folder=os.getcwd()

        # checkout branch

        #self.ch_dir(project_folder)
        #self.checkout_branch(project_folder,gh_branch)
        command = self.GIT_STAGE_TEMPLATE
        ret = subprocess.run(command, capture_output=True, shell=True)
        # print(ret)

        if ret.returncode != 0:
            self['stage_branch'] = '"{}"'.format(ret.stdout.decode('ascii').replace('\n',' '))
            self.addStep('failed')
        else:
            self['stage_branch'] = 'staged for {} @ {}'.format(gh_branch, project_folder)
            self.addStep('(staged:{})'.format(gh_branch))
        #self.ch_dir(last_folder)

        return self
    def commit_branch(self, gh_branch, project_folder):
        # commit changes to local repo
        self.addStep('[Commit-branch]')

        self['commit_branch']='undefined'
        last_folder = os.getcwd()
        ##* restore starting folder
        ##* dont commit main
        if self.get_branch_current(folder=project_folder) == 'main':
            #check get_branh_current
            self['commit_branch']='"Dont commit for {} @ {}"'.format(self.get_branch_current(folder=project_folder), project_folder)
            self.set_fail(True, "Dont commit main branch for {}".format(project_folder))
            return self

        self.checkout_branch(project_folder,gh_branch)

        #self.ch_dir(project_folder)
        command = self.GIT_COMMIT_TEMPLATE.format(os.environ['GH_MESSAGE'])
        ret = subprocess.run(command, capture_output=True, shell=True)
        if ret.returncode not in [0,1]:
            #print(ret)
            self.set_fail(True, ret.stdout.decode('ascii').replace('\n', ' '))
            self['commit_branch'] = '"{}"'.format(ret.stdout.decode('ascii').replace('\n',' '))

        else:
            self.addStep('committed')
            self.addStep('(bin:{},branch:{})'.format(self.get_project_name(),gh_branch))
            self['commit_branch'] = 'committed for {} @ {}'.format(gh_branch, project_folder)

        self.ch_dir(last_folder)
        return self
    def rebase(self,project_folder, branch):
        self.addStep('[Rebase]')

        #last_folder = os.getcwd()
        # dont bother if error has occured
        if self.hasFailed():
            self.addStep('failed-prior')
            self['rebase'] = 'Cannot rebase due to prior failure'
            return self
        # make sure branch is available @ bin
        if not self.has_branch(project_folder, branch):
            self.addStep('failed-branch')
            self.set_fail(True, 'Cannot rebase, {} branch NOT FOUND @ {}'.format(branch, project_folder))
            self['rebase']='Cannot rebase, {} branch NOT FOUND @ {}'.format(branch, project_folder)
            return self
        # set the folder
        #self.ch_dir(project_folder)
        # get current branch
        last_branch = self.get_branch_current(folder=project_folder)
        if last_branch != branch:
            raise Exception('expected brach {} is not current branch {}'.format(branch, last_branch))
        # checkout main branch
        self.checkout_branch(project_folder, "main")
        # refresh main branch
        self.pull_origin(project_folder, 'main')
        # restore original branch
        self.checkout_branch(project_folder, branch)
        self.addStep('rebase')
        # rebase
        command = self.GIT_REBASE.format(branch)
        ret = subprocess.run(command, capture_output=True, shell=True)
        # print(ret)
        if ret.returncode != 0:
            self.addStep('(failed-rebase)')
            self.set_fail(True, ret.stderr.decode('ascii'))
            self['rebase']='{}'.format(ret.stderr.decode('ascii'))

        else:
            self.addStep('(branch: {})'.format(self.get_branch_current(folder=os.getcwd())))
            rc = ret.stdout.decode('ascii').strip()
            self['rebase']='ok'

        #self.checkout_branch(project_folder, last_branch)
        #self.ch_dir(last_folder)
        return self
    def push_branch(self, no_yes, project_folder, branch):
        ##* restore starting folder
        self.addStep('[Push-branch]')

        if no_yes in ['N']:
            self.addStep('skipped')
            self['push']='skipped'
            return self
        #
        last_folder = os.getcwd()
        self.ch_dir(project_folder)
        # get current branch
        last_branch = self.get_branch_current(folder=project_folder)
        # checkout the target branch
        self.checkout_branch(project_folder, branch)
        # run the command
        #command = 'git push origin {}'.format(branch)

        command = self.GIT_PUSH_ORIGIN_TEMPLATE.format(branch)
        ret = subprocess.run(command, capture_output=True, shell=True)
        # print(ret)
        if ret.returncode != 0:
            self.addStep('failed')
            self.set_fail(True, ret.stderr.decode('ascii'))
        else:
            self.addStep('success')
            self['push']='ok, {}'.format(branch)
            rc = ret.stdout.decode('ascii').strip()
        # restore the bin's original branch
        self.checkout_branch(project_folder, last_branch)
        # restore original folder
        self.ch_dir(last_folder)
        return self
    def show_git_hub(self, gh_user, gh_project):

        #command = 'open -a "Google Chrome" "https://github.com/{}/{}"'.format(gh_user, gh_project)
        #command = 'open -a safari "https://github.com/{}/{}"'.format(gh_user, gh_project)
        #print('command', command)
        command = self.OPEN_GOOGLE_CHROME_TEMPLATE.format(gh_user, gh_project)
        ret = subprocess.run(command, capture_output=True, shell=True)
        # print(ret)
        if ret.returncode != 0:
            self.set_fail(True, ret.stderr.decode('ascii'))
        else:
            self['git_hub'] = 'open, {}'.format(gh_project)
            #rc = ret.stdout.decode('ascii').strip()
        return self
    def report(self):
        print('Report')
        for key in self:
            print('    - {} is {}'.format(key, self[key]))
        #pprint(self)
        print('    - actual process: {}'.format(self.getSteps()))
        return self
    def use(self, project_folder, branch):
        self.addStep('[Use]')

        # change folder to bin folder
        # checkout branch
        self.ch_dir(project_folder)
        self.checkout_branch(project_folder, branch)

        return self

def main():
    from pprint import pprint
    start_folder = os.getcwd() # script should start and stop in the same folder
    actual = GitScript()
    assert (actual)
    assert (actual.on_fail_exit()) # should be ok

    actual  .print('* INITIALIZE')\
            .set('env_file_name', 'git.script.env')\
            .load_env(folder=os.getcwd(), filename='git.script.env') \
            .set_env("GH_TRUNK", "main") \
            .set_env('WS_ORGANIZATION',LbUtil().get_input('WS_ORGANIZATION', actual.get_env_value('WS_ORGANIZATION') or 'TBD', hardstop=False)) \
            .set_env('WS_WORKSPACE',LbUtil().get_input('WS_WORKSPACE', actual.get_env_value('WS_WORKSPACE') or 'TBD', hardstop=False)) \
            .set_env('GH_USER', LbUtil().get_input('GH_USER', actual.get_env_value('GH_USER') or 'TBD', hardstop=False)) \
            .set_env('GH_PROJECT',LbUtil().get_input('GH_PROJECT', actual.get_env_value('GH_PROJECT') or 'TBD', hardstop=False)) \
            .set_env('GH_BRANCH', LbUtil().get_input('GH_BRANCH', actual.get_env_value('GH_BRANCH') or 'TBD', hardstop=False)) \
            .set_env('GH_MESSAGE',LbUtil().get_input('GH_MESSAGE', actual.get_env_value('GH_MESSAGE') or 'TBD', hardstop=False))\
            .print('* VALIDATE INPUTS')\
            .validate_inputs(prefix=['WS_', 'GH_']).on_fail_exit() \
            .print('* CREATE WORKSPACE')\
            .create_workspace(actual.get_workspace_folder()).on_fail_exit() \
            .print('  1. cwd              {}'.format(os.getcwd())) \
            .print('  1. workspace folder {}'.format(actual.get_workspace_folder()))\
            .print('  1. bin folder   {}'.format(actual.get_project_folder()))

    actual  .print('  2. bin nm {}'.format(actual.get_project_name())) \
            .print('  2. is_project {}'.format(actual.is_project(actual.get_project_folder()))) \
            .print('  2. branches   {}'.format(actual.get_branches(actual.get_project_folder()))) \
            .print('  2. cwd        {}'.format(os.getcwd())) \
            .print('  2. current br {}'.format(actual.get_branch_current()))

    actual  .print('* CLONE')\
            .clone_project_in(actual.get('GH_USER')
                              , actual.get('GH_PROJECT')
                              , actual.get_workspace_folder()).on_fail_exit()\
            .print('  2. bin nm {}'.format(actual.get_project_name()))\
            .print('  2. is_project {}'.format(actual.is_project(actual.get_project_folder())))\
            .print('  2. branches   {}'.format(actual.get_branches(actual.get_project_folder())))\
            .print('  2. cwd        {}'.format(os.getcwd()))\
            .print('  2. current br {}'.format(actual.get_branch_current()))\
            .report()

    actual  .print('* CREATE BRANCH')\
            .create_branch(project_folder=actual.get_project_folder(), branch=os.environ['GH_BRANCH']) \
            .print('  3. cwd        {}'.format(os.getcwd())) \
            .print('  3. current br {}'.format(actual.get_branch_current())) \
            .print('  3. branches   {}'.format(actual.get_branches(actual.get_project_folder())))

    actual  .print('* USE')\
            .use(actual.get_project_folder(),actual.get_env_value('GH_BRANCH')) \
            .print('  4. cwd        {}'.format(os.getcwd()))\
            .print('  4. current br {}'.format(actual.get_branch_current()))\
            .print('  4. branches   {}'.format(actual.get_branches(actual.get_project_folder())))

    actual  .print('* STAGE BRANCH')\
            .stage_branch(os.environ['GH_BRANCH']
                          , actual.get_project_folder()).on_fail_exit() \
            .print('  5. cwd        {}'.format(os.getcwd())) \
            .print('  5. current br {}'.format(actual.get_branch_current())) \
            .print('  5. branches   {}'.format(actual.get_branches(actual.get_project_folder())))

    #actual.report()

    actual  .print('* COMMIT')\
            .commit_branch(os.environ['GH_BRANCH']
                          , actual.get_project_folder()) \
            .print('  6. cwd {}'.format(os.getcwd()))\
            .print('  6. uncommitted {}'.format(actual.getUncommittedFiles()))
    #actual.report()

    actual  .print('* REBASE') \
            .rebase(actual.get_project_folder(),os.environ['GH_BRANCH'])

    #actual.report()

    actual  .print('* PUSH BRANCH')\
            .push_branch(LbUtil().get_input('Push', 'N', hardstop=False)
                     , actual.get_project_folder()
                     , os.environ['GH_BRANCH']) 
                     
    actual.report()                 

    actual  .write_to(actual.get_project_folder(), "test_file.txt", "hello world\n")\
            .show_git_hub(os.environ['GH_USER'], os.environ['GH_PROJECT'])
    #        .copy_to('{}/{}'.format(actual['env_folder_name'],actual['env_file_name']), actual.get_project_folder())\

    print('final folder {}'.format(os.getcwd()))
    #assert(start_folder==os.getcwd()) # script should start and stop in the same folder
    print('curr folder', os.getcwd())

if __name__ == "__main__":
    # execute as script
    main()
    #mainProjectScript()