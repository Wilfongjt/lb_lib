
'''
### Branch Process
## Goal - __Download a GitHub Project__

##* Create Development folder on developer's computer
##* Set a branch

'''
import os
import subprocess
from pprint import pprint
from pylyttlebit.lb_step import LbStep
from pylyttlebit.lb_step_list import LbStepList
from pylyttlebit.lb_project import LbProject
from pylyttlebit.lb_dev_env import LbDevEnv
from pylyttlebit.lb_util import LbUtil
from pylyttlebit.lb_constants import LbC
# from pylyttlebit.lb_folders import LbFolders
from pylyttlebit.script_lb_defaults import LbDefaults
from pylyttlebit.step_lb_initialize_environment import LbInitializeEnvironment
from pylyttlebit.step_lb_validate_prompt_inputs import LbValidatePromptInputs
from pylyttlebit.step_lb_impute_project_variables import LbImputeProjectVariables
from pylyttlebit.step_lb_validate_input_variables import LbValidateInputVariables
from pylyttlebit.step_lb_create_workspace import LbCreateWorkspace
from pylyttlebit.step_lb_clone_project import LbCloneProject
from pylyttlebit.step_lb_save_environment import LbSaveEnvironment
from pylyttlebit.step_lb_status import LbStatus
from pylyttlebit.lb_stash import LbStash
'''
class LbEnvironment(LbDefaults):
    #### LbEnvironment Variables
    ##* Collect environment variables from memory using default keys
    def __init__(self):
        super().__init__()
        for k in self:
            if k in os.environ:
                self[k] = os.environ[k]
'''
class PromptBranchInputs(LbStep):
    def __init__(self, lb_stash):
        super().__init__()
        self.setStash(lb_stash)
        self.hardstop = False

    def getParameterPrompts(self):
        #### Prompt user for inputs on request
        rc = {}

        for p in self.getStash(LbC().PROMPTS_KEY):
            self.addStep('[prompt]')
            rc[p] =LbProject().prompt(p
                                      ,LbProject().get_env_value(p)
                                      ,hardstop=self.hardstop)

        # identify lb_stash data

        self.addStep(self.formulate(self.getStash().getPrompts(), title='prompts'))

        # record process steps

        self.getStash().setProcess(self.getSteps())

        print('')
        return rc

    def process(self):
        super().process()
        #self.addStep('[prompts]')
        #### Collect Inputs
        print('process PromptRebaseInputs')
        ##* WS_ORGANIZATION
        ##* WS_WORKSPACE
        ##* GH_USER
        ##* GH_PROJECT
        ##* GH_BRANCH

        self.getStash()[LbC().PROMPTS_KEY] = self.getParameterPrompts()
        if self.getStash().isValid():
            self.addStep('(valid)')
        else:
            self.addStep('(invalid)')
        print('')
        return self

class LbBranch(LbStepList):
    #### Download GitHub Branch
    def __init__(self, lb_stash):
        super().__init__()
        # passive load of steps
        self.setStash(lb_stash) # set shared variables
        ##1. Initialize Environment
        self.add(LbInitializeEnvironment(lb_stash))
        ##1. Prompt for Inputs
        self.add(PromptBranchInputs(lb_stash))
        ##1. Impute Project Variables
        self.add(LbImputeProjectVariables(lb_stash))
        ##1. Validate Input Variables
        self.add(LbValidateInputVariables(lb_stash))
        ##1. Create Workspace
        self.add(LbCreateWorkspace(lb_stash))
        ##1. Clone Project
        self.add(LbCloneProject(lb_stash))
        ##1. Save Environment
        self.add(LbSaveEnvironment(lb_stash))
        ##1. Show Status
        self.add(LbStatus(lb_stash))

    def hello_world(self):
        print("I am LbBranch!")
        return self

    def isValid(self):
        ####
        if LbC().INVALID_KEY in self.getStash():
            return False
        return True
def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_branch')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

def main():
    # shared variables
    #lb_stash = {
    #    'app': {
    #    },
    #    LbC().PROJECT_KEY:{}
    #}
    print('defaults   ', LbDefaults())
    #print('environment', LbEnvironment())
    stash = LbStash()
    actual = LbBranch(stash)

    actual.run()
    #print('Outputs')
    #pprint(actual.getStash())

if __name__ == "__main__":
    # execute only if run as a script
    main()
    #unittest.main()
