import os
from pprint import pprint
import subprocess
from pylyttlebit.lb_step import LbStep
from pylyttlebit.lb_constants import LbC
from pylyttlebit.lb_dev_env import LbDevEnv
from pylyttlebit.lb_project import LbProject


class LbCloneProject(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)

    def getPrompts(self):
        return self.getStash(LbC().PROMPTS_KEY)

    def getRepoUrl(self):

        rc = self.getStash().getProject()[LbC().REPO_URL_KEY]
        return rc
    def getWorkspaceFolder(self):

        workspace_folder = self.getStash().getProject()[LbC().PROJECT_FOLDER_KEY]
        workspace_folder = workspace_folder.split('/')[0:-1]
        workspace_folder = '/'.join(workspace_folder)
        if len(workspace_folder) == 0:
            workspace_folder = 'TBD'
        return workspace_folder

    def getProjectFolder(self):
        project_folder = self.getStash().getProject()[LbC().PROJECT_FOLDER_KEY]
        return project_folder

    def process(self):
        super().process()
        print('process CloneProject')

        ##      * Clone the repository (aka Project) into workspace When repository is not cloned
        self.addStep('[clone]')

        #self.getStash().validate()

        if not self.getStash().isValid():
            self.addStep('(failed)')

            ##* Dont clone repo when lb_stash is invalid
            print('    !!!! invalid lb_stash')
            print('')

        else:
            org_dir = os.getcwd()  # get current folder
            pprint(self.getStash())
            print('    * run     ', LbProject().getProjectFolder())

            # change to the new workspace folder
            os.chdir(self.getWorkspaceFolder())

            ##* Dont clone repo when clone folder exists

            if LbProject().isCloned(self.getProjectFolder()):
                print('    * skipping...clone. "{}" is already cloned.'.format(self.getPrompts()[LbC().GH_PROJECT_KEY]))
                os.chdir(org_dir)
                print('')
                return self

            print('    * cloning...', end='')

            # clone repo
            command = 'git clone {}'.format(self.getRepoUrl())
            ret = subprocess.run(command, capture_output=True, shell=True)

            # change back to original folder
            os.chdir(org_dir)
            self.addStep('(success)')


        # identify the bin data

        self.addStep(self.formulate(self.getStash().getProject()))

        # record process steps

        self.getStash().setProcess(self.getSteps())

        print('')

        return self
def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('step_lb_clone_project')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()


def main():
    from pprint import pprint
    from pylyttlebit.lb_stash import LbStash

    stash = LbStash()
    actual = LbCloneProject(stash).process()
    #print('lb_stash', actual.getStash())
    pprint(actual.getStash())

if __name__ == "__main__":
    # execute only if run as a script
    main()
    # unittest.main()