import settings
import os
import sys
import subprocess
from git_script.lb_recorder import LbRecorder

#from git_script.git_script_01 import GitScript
#from git_script.lb_util import LbUtil
class Expected():
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
    def depvalidate_project_folder(self, folder):
        # is the given folder a bin folder
        # eg ~/Development/organization/workspace/bin
        # must have Development at forth position from end
        rc = True
        fldr = folder.split('/')
        # Development

        if fldr[-4] != 'Development':
            rc = False

        return rc

    def dep_validate_workspace_folder(self, folder):
        # is the given folder a workspace folder
        # eg ~/Development/organization/workspace
        # must have Development at third position from end
        rc = True
        fldr = folder.split('/')
        # Development

        if fldr[-3] != 'Development':
            rc = False

        return rc

class Actual(Expected):
    #def __init__(self):
    #    super().__init__()
    def is_project_folder(self):
        # is the current folder a bin folder
        # eg ~/Development/organization/workspace/bin
        # must have Development at forth position from end

        rc = False

        fldr = os.getcwd()
        dev_pos=-4
        rc = self.validate_folder(fldr, dev_pos)

        return rc
    def is_workspace_folder(self):
        # is the current folder a workspace folder
        # eg ~/Development/organization/workspace/bin
        # must have Development at forth position from end

        rc = False

        fldr = os.getcwd()
        dev_pos=-3
        rc = self.validate_folder(fldr, dev_pos)

        return rc

class Status(LbRecorder):

    def getUncommittedFiles(self):
        rc = ''
        command='git status --porcelain'
        ret = subprocess.run(command, capture_output=True, shell=True)
        #print(ret)
        if ret.returncode != 0:
            #self['stage_branch'] = '"{}"'.format(ret.stdout.decode('ascii').replace('\n', ' '))
            self.addStep('(failed)')
        else:
            #self['stage_branch'] = 'staged for {} @ {}'.format(gh_branch, project_folder)
            self.addStep('(Uncommitted)')
            rc = ret.stdout.decode('ascii')
            rc = rc.split('\n')
            rc = [f.strip().replace('  ',' ').split(' ') for f in rc if f != '']
            rc = [{"track": t[0], "file": t[1]} for t in rc]

        return rc
def main():
    start_folder = os.getcwd()
    print('start folder', start_folder)
    actual = Actual()
    folder=start_folder
    assert(actual.validate_folder(folder,-4))
    assert(actual.is_project_folder())
    assert (not actual.validate_folder(folder,-3))
    assert (not actual.is_workspace_folder())
    folder = '/'.join(folder.split('/')[0:-1])
    assert (actual.validate_folder(folder,-3))
    os.chdir('../..')
    assert (actual.is_workspace_folder())

    folder = start_folder
    os.chdir(folder)
    print('current folder', folder)
    actual = Status()
    print('status getUncommittedChanges', actual.getUncommittedFiles())
    # Initialize GitScript

if __name__ == "__main__":
    # execute as script
    main()