import os
import time
import subprocess
from pathlib import Path
from os import listdir
from os.path import isfile, join
from pylyttlebit.lb_util import LbUtil

class LbProject(LbUtil):

    def getBranch(self):
        #### Get branch name on request
        ##* branch is found in .git repo eg (HEAD ref: refs/heads/00_init)
        # get the project folder
        pos = 4
        rc = self.current_directory().split('/')
        idx = rc.index('Development')  # os.getcwd().split('/').index('Development')

        # pad with TBD
        while idx + pos > len(rc):
            rc.append('TBD')

        rc = rc[0:idx + pos]
        # print('getBranch', rc)

        head_dir = Path('/'.join(rc)) / ".git" / "HEAD"

        with head_dir.open("r") as f:
            content = f.read().splitlines()

        for line in content:
            if line[0:4] == "ref:":
                return line.partition("refs/heads/")[2]

        ##* returns str
        return ""


    def depgetCurrentBranch(self, project_folder):
        head_dir = Path(".") / ".git" / "HEAD"
        # head_dir = Path(project_folder) / ".git" / "HEAD"
        print('project folder', project_folder)
        print('cwd', os.getcwd())
        print('head_dir', head_dir)

        # head_dir = '../.git/HEAD'
        with head_dir.open("r") as f:
            content = f.read().splitlines()

        for line in content:
            if line[0:4] == "ref:":
                return line.partition("refs/heads/")[2]
        return ""

    def getDevelopmentFromPath(self):
        #### Get Development Folder Name on request
        ##* Split the current folder name
        # look for Development folder
        # print(type(self.current_directory()),self.current_directory())
        ##* retrieve  from folder name eg "/User/~/Development/\<organization>/\<workspace>/\<project>/"

        pos = 1
        # split folder
        rc = self.current_directory().split('/')
        # find "Development" index
        idx = rc.index('Development')
        # set defaults folder names to "TBD"
        while idx + pos > len(rc):
            rc.append('TBD')

        # trim off everything past expected positon
        rc = rc[0:idx + pos]
        #print('rc',rc)
        # print('dev', '/'.join(rc))
        #print('rc',rc[-1])
        #return rc[idx + pos - 1]
        ##* return str
        return rc[-1]

    def getOrganizationFromPath(self):
        #### Get the Organization Name on request
        # get the organization folder
        ##* retrieve \<organization> from path eg "~/Development/\<organization>/\<workspace>/\<project>/"

        pos = 2
        rc = self.current_directory().split('/')
        idx = rc.index('Development')
        # pad path with TBD
        while idx + pos > len(rc):
            rc.append('TBD')

        rc = rc[0:idx + pos]
        ##* return str ... [x] has test
        return rc[-1]

    def getProjectFolder(self):
        rc = self.current_directory()
        print('rc', rc)
        return rc
    def getProjectFromPath(self):
        #### Get the Project Name on request
        ##* retrieve \<project> from path eg "~/Development/\<organization>/\<workspace>/\<project>/"

        pos = 4
        rc = self.current_directory().split('/')
        idx = rc.index('Development')  # os.getcwd().split('/').index('Development')

        # pad with TBD
        while idx + pos > len(rc):
            rc.append('TBD')

        rc = rc[0:idx + pos]
        ##* return str ... [x] has test
        return rc[-1]

    def getWorkspaceFromPath(self):
        #### Get the Workspace Name on request
        ##* retrieve \<workspace> from path eg "~/Development/\<organization>/\<workspace>/\<project>/"

        # get the workspace folder
        pos = 3
        rc = self.current_directory().split('/')
        idx = rc.index('Development')  # os.getcwd().split('/').index('Development')

        # pad with TBD
        while idx + pos > len(rc):
            rc.append('TBD')

        rc = rc[0:idx + pos]
        # print('ws', '/'.join(rc))
        ##* return str ... [x] has test
        return rc[-1]

    def hasBranch(self, branch_name):
        #### Test for a branch by name on request
        # check if github repo exists
        ##* use "git branch" command and search for branch name in result
        result = subprocess.run(["git", "branch"], capture_output=True, text=True)
        # 0 mean success
        #print('hasBranch', result.stdout)
        if result.returncode == 0:
            if branch_name in result.stdout:
                ##* True is not testable because
                return True
        ##* return bool ... [x] has test
        return False

    def hasRemoteProject(self, url):
        #### Test for Project on GitHub on request
        # check if github repo exists

        ##* use "git ls-remote" command and search for branch name in result

        result = subprocess.run(["git", "ls-remote", "-h", url], capture_output=True, text=True)
        # 0 mean success
        #print('hasRemoteProject', result)
        if result.returncode == 0:
            return True
        ##* return bool
        return False

    def hello_world(self):
        print("I am LbProject!")

    def isCloned(self, project_folder):
        #### Test for".git" in Project
        # expects the cur folder to be a project folder
        # print('cwd', os.getcwd())
        # print('isCloned', project_folder, end='')
        exists = os.path.isdir('{}/.git'.format(project_folder))
        # print(exists)
        ##* return bool
        return exists

    def prompt(self, msg, default, hardstop=True):
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

    def verify(self, prompts, prefix=None):
        #### Verify List of Prompt Values
        ##* eg []
        # make sure values are ok
        if not prefix:
            for p in prompts:
                if prompts[p] in ['TBD']:
                    return False
        else: # eg WS_ or GH_
            for p in prompts:
                if prompts[p] in ['TBD']:
                    if p.startswith(prefix):
                        return False
        return True

def main():
    from pylyttlebit.lb_folders import LbFolders
    from pylyttlebit.lb_doc_comments import LbDocComments
    #head_dir = Path(".") / ".git" / "HEAD"


    #print([x for x in Path(".").iterdir() if x.is_dir()])

    #######
    actual = LbProject()
    assert (actual)

    print('getBranch', actual.getBranch())

    assert (actual.getDevelopmentFromPath() == 'Development')
    assert (actual.getOrganizationFromPath() == 'lyttlebit')
    # print('getWorkspace', actual.getWorkspaceFromPath())
    assert (actual.getWorkspaceFromPath() == '00_std')
    assert (actual.getProjectFromPath() == 'lb_lib')
    assert ( actual.getProjectFolder())
    assert ( actual.hasBranch('main') )
    #assert ( hasBranch('00_init') )
    #assert (actual.hasRemoteProject())
    print(actual.getBranch())
    # write documentation in markdown file
    LbDocComments().setFolder(os.getcwd()).setFilename(str(__file__).split('/')[-1]).open().save()


def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_project')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()


if __name__ == "__main__":
    # execute as script
    main()