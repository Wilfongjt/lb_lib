import os
import sys
from pprint import pprint
from lb_util import LbUtil
import subprocess
import shutil


class ProjectScript(dict):
    def __init__(self):
        self['fail'] = False
        self['fail_msg'] = []
        self.WORKSPACE_FOLDER = '{}/Development/{}/{}'
        self.PROJECT_FOLDER = '{}/Development/{}/{}/{}'

    def assertTrue(self, expression):
        assert (expression == True)
        return self
    def ch_dir(self, folder):

        os.chdir(folder)
        return self
    def copy_to(self, source_file_path, destination_folder):
        # source eg /Users/jameswilfong/Development/lyttlebit/00_std/lb_lib/.env
        # destination eg /Users/jameswilfong/Development/lyttlebit/00_next/lb_test/
        try:
            shutil.copy2(source_file_path, destination_folder)
            #print(f"File '{source_file_path}' copied to '{destination_folder}' successfully.")
            self['copy_to']="ok, {}".format(str(source_file_path).split('/')[-1])
        except Exception as e:
            #print(f"Error copying file: {str(e)}")
            self.setFail(True, f"Error copying file: {str(e)}")
        return self
    def exit(self):
        sys.exit(2)
        return self
    def get(self, key):
        if key not in self:
            self.setFail(True, '{} Not Found'.format(key))
            raise Exception('{} Not Found'.format(key))
        return self[key]
    def get_workspace_folder(self):
        return self.WORKSPACE_FOLDER.format(os.environ['HOME']
                                            ,os.environ["WS_ORGANIZATION"]
                                            ,os.environ["WS_WORKSPACE"])
    def get_project_folder(self):
        return self.PROJECT_FOLDER.format(os.environ['HOME']
                                          , os.environ["WS_ORGANIZATION"]
                                          , os.environ["WS_WORKSPACE"]
                                          , os.environ["GH_PROJECT"])
    def hasFailed(self):
        return self['fail']
    def on_fail_exit(self):
        if self['fail']:
            self.report()
            #print('fails when "{}"'.format(self['fail_msg']))

            sys.exit(1)
        return self
    def print(self,ln):
        print(ln)
        return self
    def set(self, key, value):
        self[key] = value
        return self
    def setFail(self, tf, msg=None):
        #### Generalize Fail
        self['fail'] = tf
        self['fail_msg'].append(msg.replace('\n',' '))
        return self
    def subprocess(self, command):
        rc = False
        ret = subprocess.run(command, capture_output=True, shell=True)
        #print(ret)
        if ret.returncode != 0:
            self.setFail(True, ret.stderr.decode('ascii'))
            rc= ret.stderr.decoce('ascii')
        else:
            rc = ret.stdout.decode('ascii').strip()
        return rc

    def write_to(self, folder, filename, test_line):
        # write a file to the bin folder
        with open('{}/{}'.format(folder,filename), 'a') as f:
            f.write(test_line)
        self['write_to']=filename
        return self


class GitScript(ProjectScript):
    def __init__(self):
        super().__init__()
        self['env_folder_name']=os.getcwd()
        self['env_file_name']='.env'

        self.GIT_URL_TEMPLATE = 'https://github.com/{}/{}.git'
        self.GIT_CLONE_TEMPLATE = 'git clone {}' # project_url
        self.GIT_CREATE_BRANCH_TEMPLATE = 'git branch {}' #
        self.GIT_STAGE_TEMPLATE='git add .' # no variables
        self.GIT_COMMIT_TEMPLATE='git commit -m {}' # GH_MESSAGE
        self.GIT_CURR_BRANCH_COMMAND="git symbolic-ref --short HEAD 2>/dev/null"

        self.GIT_HAS_BRANCH_COMMAND='git branch'
        self.GIT_CHECKOUT_BRANCH_TEMPLATE='git checkout {}' # <branch name>

    def get_project_name(self, folder):

        if 'project_name' not in self:
            last_folder = os.getcwd()
            self.ch_dir(folder)
            command = "git remote show origin"
            std_out = self.subprocess(command)
            std_out = std_out.split('\n')
            std_out = [o.strip() for o in std_out if 'Fetch' in o]
            std_out = std_out[0].split(':', maxsplit=1)
            std_out = std_out[1].split('/')[-1].replace('.git','')
            #print('get_project_name', std_out)
            self['project_name'] = std_out
            self.ch_dir(last_folder)

        return self['project_name']
    def get_branch_current(self, folder=None):
        # folder is the project_folder
        rc = None

        last_folder = os.getcwd()
        if folder:
            self.ch_dir(folder)

        command = self.GIT_CURR_BRANCH_COMMAND
        rc = self.subprocess(command)
        #ret = subprocess.run(command, capture_output=True, shell=True)
        #print(ret)
        #if ret.returncode != 0:
        #    self.setFail(True, ret.stderr.decode('ascii'))
        #else:
        #    rc = ret.stdout.decode('ascii').strip()

        self.ch_dir(last_folder)
        #print('get_branch_current', rc)
        return rc
    def get_project_info(self, key=None, project_folder=None):
        # return all info when key is None
        # return single item when

        rc = {}

        last_folder = os.getcwd()
        if project_folder:
            self.ch_dir(project_folder)

        command = "git remote show origin"
        std_out = self.subprocess(command)

        #print('A std_out', std_out)
        #ret = subprocess.run(command, capture_output=True, shell=True)
        #print('B std_out', std_out)

        std_out = std_out.split('\n')
        std_out=[o.strip() for o in std_out]
        print('C std_out', std_out)
        #collect_branch = False
        # fetch_url and push_url

        # Current Branch Name
        rc['current_branch']=self.get_branch_current(folder=project_folder)

        # Project Name
        rc['project_name']=self.get_project_name(project_folder)
        #print('get_project_info', rc)

        # Remote Branches
        command = 'git branch'
        std_out = self.subprocess(command)
        std_out=[br for br in std_out.split() if br!='*']
        rc['branches']=std_out

        self.ch_dir(last_folder)
        return self
    def get_branches(self,project_folder):
        command = 'git branch'
        std_out = self.subprocess(command)
        std_out = [br for br in std_out.split() if br != '*']
        #print('get_branches ', std_out)
        self['branches'] = std_out
        #print('get_branches ', self['branches'])

        return self['branches']

    def get_env_value(self, key):
        rc = None
        if key in os.environ:
            rc=os.environ[key]
        return rc
    def has_branch(self, branch_name, project_folder):
        rc = False
        if branch_name in self.get_branches(project_folder):
            rc = True
        return rc

    def load_env(self, folder=None, filename=None):
        env_file_name = filename or self.get('env_file_name')
        env_folder_name = folder or self.get('env_folder_name') or os.getcwd()
        line_list=[]
        if LbUtil().file_exists(env_folder_name, env_file_name):
            with open('{}/{}'.format(env_folder_name, env_file_name)) as file:
                line_list = file.readlines()
                line_list = [ln.replace('\n', '') for ln in line_list]

        for ln in line_list:
            if '=' in ln:
                ln = ln.split('=')
                self.set(ln[0],ln[1])
                os.environ[ln[0]]=ln[1]

        return self

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

        ##* find "key=" then replace with "key=value"
        i=0
        found=False
        for ln in line_list:
            if ln.startswith('{}='.format(key)):
                found = True
                line_list[i]='{}={}'.format(key,value)
                ##* set stash variable
                self.set(key, value)
                ##* set envioron variable
                os.environ[key]=value
                break
            i+=1

        ##* key not found then append

        if not found:
            line_list.append('{}={}'.format(key,value))
            ##* set stash variable
            self.set(key,value)
            ##* set envioron variable
            os.environ[key] = value

        ##* save after every set

        with open('{}/{}'.format(env_folder_name, env_file_name), 'w') as f:
            f.writelines(['{}\n'.format(ln) for ln in line_list])

        return self

    def show_env(self):
        pprint(self)
        return self
    def showTitle(self, title):
        print('title: {}'.format(title))
        return self

    def validate_input(self, key, value):
        ##* test for Null key
        ##* test for Null value
        ##* test for TBD value
        if not key:
            self.setFail(True, 'Key is None')
        elif not value:
            self.setFail(True, '{} value is None'.format(key))
        elif value == 'TBD':
            self.setFail(True, '{} value is TBD'.format(key))
        return self
    def validate_inputs(self, prefix=['WS_', 'GH_']):
        ## fail when inputs are invalid
        for key in os.environ:
            for pfx in prefix:
                if key.startswith(pfx):
                    self.validate_input(key, os.environ[key])

        return self

    def create_workspace(self, folder):

        os.makedirs(folder, exist_ok=True)

        self['create_workspace'] = 'ok'
        return self
    def clone_project_in(self, gh_user, gh_project, workspace_folder):

        project_folder='{}/{}'.format(workspace_folder,gh_project)
        project_url = self.GIT_URL_TEMPLATE.format(gh_user, gh_project)
        last_folder=os.getcwd()
        self.ch_dir(workspace_folder)
        ##* folder exists when found on drive
        exists = os.path.isdir('{}'.format(project_folder))
        if exists:
            self['clone_project']='found'
        else:
            command = self.GIT_CLONE_TEMPLATE.format(project_url)
            ret = subprocess.run(command, capture_output=True, shell=True)
            #print(ret)
            if ret.returncode != 0:
                self['clone_project']=str(ret.stderr)
            else:
                self['clone_project']='created'

            exists = os.path.isdir('{}'.format(project_folder))
            if exists:
                os.chdir(project_folder)
            else:
                self.setFail(True, str(ret.stderr))
        self.ch_dir(last_folder)
        return self
    def create_branch(self, gh_branch, project_folder):
        ##* restore starting folder
        last_folder = os.getcwd()

        ##* dont create main
        #print('create_branch branch',branch)
        #print('create_branch has branch',self.has_branch(branch, project_folder))
        if self.has_branch(gh_branch, project_folder):
            ##* dont recreate a branch
            self['create_branch'] = 'found'
            return self

        self.ch_dir(project_folder)

        command = self.GIT_CREATE_BRANCH_TEMPLATE.format(gh_branch)
        ret = subprocess.run(command, capture_output=True, shell=True)
        #print("create_branch ret ",ret)

        if ret.returncode != 0:
            self['create_branch'] = '"{}"'.format(ret.stdout.decode('ascii').replace('\n', ''))
        else:
            self['create_branch'] = 'created'

        self.ch_dir(last_folder)
        return self

    def stage_branch(self, gh_branch, project_folder):
        #
        # change folder when project_folder is NOT equal to current folder
        # stage branch when branch is equal to current branch
        # change folder back to original folder on return
        # dont stage main branch

        last_folder=os.getcwd()

        #print('get_project_name'.format(self.get_project_name(project_folder)))
        #print('get_branch_current'.format(self.get_branch_current(project_folder)))
        #print('get_branches'.format(self.get_branches(project_folder)))

        ##* dont stage main

        # print('get_project_info',self.get_project_info(project_folder=project_folder) )

        #print('get_project_info current_branch',self.get_project_info(key='current_branch',project_folder=project_folder) )
        #print('get_project_info remote_branches',self.get_project_info(key='remote_branches',project_folder=project_folder) )

        #print('get_project_info project_name',self.get_project_info(key='project_name',project_folder=project_folder) )

        #print('curr bin',self.get_project_name(folder=project_folder) )
        #print('stage_branch project_folder',project_folder)
        #if self.get_branch_current(folder=project_folder) == 'main':
        #    self['stage_branch']='"Dont stage main branch"'
        #    self.setFail(True, "Dont stage main branch")
        #    return self

        # checkout branch

        self.ch_dir(project_folder)
        self.checkout_branch(project_folder,gh_branch)
        command = self.GIT_STAGE_TEMPLATE
        ret = subprocess.run(command, capture_output=True, shell=True)
        # print(ret)

        if ret.returncode != 0:
            self['stage_branch'] = '"{}"'.format(ret.stdout.decode('ascii').replace('\n',' '))
        else:
            self['stage_branch'] = 'staged'

        self.ch_dir(last_folder)

        return self
    def commit_branch(self, gh_branch, project_folder):
        self['commit_branch']='undefined'

        ##* restore starting folder
        ##* dont commit main
        if self.get_branch_current(folder=project_folder) == 'main':
            self['commit_branch']='"Dont commit main branch"'
            self.setFail(True, "Dont commit main branch")
            return self
        last_folder = os.getcwd()
        self.ch_dir(project_folder)
        command = self.GIT_COMMIT_TEMPLATE.format(os.environ['GH_MESSAGE'])
        ret = subprocess.run(command, capture_output=True, shell=True)
        if ret.returncode != 0:
            #print(ret)
            self['commit_branch'] = '"{}"'.format(ret.stdout.decode('ascii').replace('\n',' '))

        else:
            self['commit_branch'] = 'committed'

        self.ch_dir(last_folder)
        return self
    def checkout_branch(self, folder, branch_name):

        # checkout when branch_name != branch_current

        if self.get_branch_current(folder=folder) != branch_name:
            return self

        last_folder = os.getcwd()
        self.ch_dir(folder)

        command=self.GIT_CHECKOUT_BRANCH_TEMPLATE.format(branch_name)
        ret = subprocess.run(command, capture_output=True, shell=True)
        # print(ret)
        if ret.returncode != 0:
            self.setFail(True, ret.stderr.decode('ascii'))
        else:
            rc = ret.stdout.decode('ascii').strip()

        self.ch_dir(last_folder)

        return self

    def pull_origin(self,project_folder, branch):
        last_folder = os.getcwd()
        self.ch_dir(project_folder)
        command =  'git pull origin {}'.format(branch)
        ret = subprocess.run(command, capture_output=True, shell=True)
        # print(ret)
        if ret.returncode != 0:
            self.setFail(True, ret.stderr.decode('ascii'))
        else:
            rc = ret.stdout.decode('ascii').strip()

        self.ch_dir(last_folder)
        return self
    def rebase(self,project_folder, branch):
        last_folder = os.getcwd()
        self.ch_dir(project_folder)
        # get current branch
        last_branch = self.get_branch_current(folder=project_folder)

        # checkout main branch
        self.checkout_branch(project_folder, "main")
        # refresh main branch
        self.pull_origin(project_folder, 'main')
        # restore original branch
        self.checkout_branch(project_folder, branch)
        # rebase
        command = 'git rebase {}'.format(branch)
        ret = subprocess.run(command, capture_output=True, shell=True)
        # print(ret)
        if ret.returncode != 0:
            self.setFail(True, ret.stderr.decode('ascii'))
        else:
            rc = ret.stdout.decode('ascii').strip()

        self.checkout_branch(project_folder, last_branch)
        self.ch_dir(last_folder)
        return self

    def push_branch(self, no_yes, project_folder, branch):
        ##* restore starting folder

        if no_yes in ['N']:
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
        command = 'git push origin {}'.format(branch)
        ret = subprocess.run(command, capture_output=True, shell=True)
        # print(ret)
        if ret.returncode != 0:
            self.setFail(True, ret.stderr.decode('ascii'))
        else:
            self['push']='ok, {}'.format(branch)
            rc = ret.stdout.decode('ascii').strip()
        # restore the bin's original branch
        self.checkout_branch(project_folder, last_branch)
        # restore original folder
        self.ch_dir(last_folder)
        return self
    def show_git_hub(self, gh_user, gh_project):
        command = 'open -a safari "https://github.com/{}/{}"'.format(gh_user, gh_project)
        ret = subprocess.run(command, capture_output=True, shell=True)
        # print(ret)
        if ret.returncode != 0:
            self.setFail(True, ret.stderr.decode('ascii'))
        else:
            self['git_hub'] = 'open, {}'.format(gh_project)
            #rc = ret.stdout.decode('ascii').strip()
        return self
    def report(self):
        print('Report')
        for key in self:
            print('    - {} is {}'.format(key, self[key]))
        #pprint(self)
        return self

    def use(self, project_folder, branch):
    return self

def main():
    from pprint import pprint
    start_folder = os.getcwd() # script should start and stop in the same folder
    actual = GitScript()
    assert (actual)
    assert (actual.on_fail_exit()) # should be ok
    actual  .set('env_file_name', 'git.script.env')\
            .load_env(folder=os.getcwd(), filename='git.script.env') \
            .set_env("GH_TRUNK", "main") \
            .set_env('WS_ORGANIZATION',LbUtil().get_input('WS_ORGANIZATION', actual.get_env_value('WS_ORGANIZATION') or 'TBD', hardstop=False)) \
            .set_env('WS_WORKSPACE',LbUtil().get_input('WS_WORKSPACE', actual.get_env_value('WS_WORKSPACE') or 'TBD', hardstop=False)) \
            .set_env('GH_USER', LbUtil().get_input('GH_USER', actual.get_env_value('GH_USER') or 'TBD', hardstop=False)) \
            .set_env('GH_PROJECT',LbUtil().get_input('GH_PROJECT', actual.get_env_value('GH_PROJECT') or 'TBD', hardstop=False)) \
            .set_env('GH_BRANCH', LbUtil().get_input('GH_BRANCH', actual.get_env_value('GH_BRANCH') or 'TBD', hardstop=False)) \
            .set_env('GH_MESSAGE',LbUtil().get_input('GH_MESSAGE', actual.get_env_value('GH_MESSAGE') or 'TBD', hardstop=False))\
            .validate_inputs(prefix=['WS_', 'GH_']).on_fail_exit()\
            .create_workspace(actual.get_workspace_folder()).on_fail_exit() \
            .clone_project_in(actual.get('GH_USER')
                              , actual.get('GH_PROJECT')
                              , actual.get_workspace_folder()).on_fail_exit() \
            .create_branch(os.environ['GH_BRANCH']
                           , actual.get_project_folder()) \
            .print('m get_project_name {}'.format(actual.get_project_name(actual.get_project_folder()))) \
            .print('m get_branch_current {}'.format(actual.get_branch_current(actual.get_project_folder())))\
            .print('m get_branches {}'.format(actual.get_branches(actual.get_project_folder())))\
            .stage_branch(os.environ['GH_BRANCH']
                          , actual.get_project_folder()).on_fail_exit() \
            .commit_branch(os.environ['GH_BRANCH']
                           , actual.get_project_folder()).on_fail_exit() \
            .rebase(actual.get_project_folder(),os.environ['GH_BRANCH'])\
            .push_branch(LbUtil().get_input('Push', 'N', hardstop=False)
                     , actual.get_project_folder()
                     , os.environ['GH_BRANCH']) \
            .write_to(actual.get_project_folder(), "test_file.txt", "hello world\n")\
            .report()\
            .show_git_hub(os.environ['GH_USER'], os.environ['GH_PROJECT'])\
            .copy_to('{}/{}'.format(actual['env_folder_name'],actual['env_file_name']), actual.get_project_folder())\

    print('final folder {}'.format(os.getcwd()))
    assert(start_folder==os.getcwd()) # script should start and stop in the same folder
    print('curr folder', os.getcwd())

if __name__ == "__main__":
    # execute as script
    main()