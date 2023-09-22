import os
#import sys
#from pprint import pprint
import subprocess
#import shutil
#from lb_util import LbUtil
#from lb_recorder import LbRecorder

from code.project_script import ProjectScript
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
        branches = self.get_branches(project_folder)

        if branch_name in branches:
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

def main():
    from pprint import pprint
    start_folder = os.getcwd() # script should start and stop in the same folder
    actual = GitCommands()
    assert (actual)
    assert (actual.on_fail_exit()) # should be ok

def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_constants')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

if __name__ == "__main__":
    # execute as script
    main()
    #mainProjectScript()