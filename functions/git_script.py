import os
#import sys
#from pprint import pprint
import subprocess
#import shutil
#from lb_util import LbUtil
#from lb_recorder import LbRecorder

from git_commands import GitCommands
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
        self.addStep('[Clone-project]')

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
            self.addStep('(project:{})'.format(self.get_project_name()))
            # self.addStep('(project: {})'.format(self.get_project_name(project_folder)))
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
                self.addStep('(project:{})'.format(self.get_project_name()))

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
            self.addStep('(project:{},branch:{})'.format(self.get_project_name(),gh_branch))
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
        # make sure branch is available @ project
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
        # restore the project's original branch
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

        # change folder to project folder
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

if __name__ == "__main__":
    # execute as script
    main()
    #mainProjectScript()