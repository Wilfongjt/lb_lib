# import unittest
import os
from pprint import pprint
from pylyttlebit.lb_step import LbStep
from pylyttlebit.lb_step_list import LbStepList
from pylyttlebit.lb_project import LbProject
from pylyttlebit.lb_constants import LbC
from pylyttlebit.lb_folders import LbFolders

from pylyttlebit.step_lb_initialize_environment import LbInitializeEnvironment
#from pylyttlebit.step_lb_validate_prompt_inputs import LbValidatePromptInputs
from pylyttlebit.step_lb_impute_project_variables import LbImputeProjectVariables
from pylyttlebit.step_lb_validate_input_variables import LbValidateInputVariables
from pylyttlebit.step_lb_create_workspace import LbCreateWorkspace
#from pylyttlebit.step_lb_clone_project import LbCloneProject
from pylyttlebit.step_lb_save_environment import LbSaveEnvironment
from pylyttlebit.step_lb_status import LbStatus
from pylyttlebit.lb_stash import LbStash

####################################

class InitializeEnvironment(LbInitializeEnvironment):
    # ### Initialize LbEnvironment

    def __init__(self, lb_stash):
        super().__init__(lb_stash)

    def process(self):
        super().process()

        print('LbInitializeEnvironment ')

        ##* Ensure git.rebase is running from the scripts folder, ie current folder ends with "scripts"

        ##* set prompts to {}

        ##* set prompts to TBD

        ##* echo lb_stash when verbose is true

        return self

###########################################
class PromptRebaseInputs(LbStep):
    def __init__(self, lb_stash):
        super().__init__()
        self.setStash(lb_stash)
        self.hardstop = False

    def getParameterPrompts(self):

        rc = {
            LbC().WS_ORGANIZATION_KEY: LbProject().prompt(LbC().WS_ORGANIZATION_KEY
                                                                  , LbProject().getOrganizationFromPath()
                                                                  , hardstop=self.hardstop),
            LbC().WS_WORKSPACE_KEY: LbProject().prompt(LbC().WS_WORKSPACE_KEY
                                                               ,LbProject().getWorkspaceFromPath()
                                                               ,hardstop=self.hardstop),
            LbC().GH_USER_KEY: LbProject().prompt(LbC().GH_USER_KEY
                                                          ,LbProject().get_env_value(LbC().GH_USER_KEY)
                                                          ,hardstop=self.hardstop),
            LbC().GH_PROJECT_KEY: LbProject().prompt(LbC().GH_PROJECT_KEY
                                                             ,LbProject().getProjectFromPath()
                                                             ,hardstop=self.hardstop),
            LbC().GH_BRANCH_KEY: LbProject().prompt(LbC().GH_BRANCH_KEY
                                                            , LbProject().getBranch()
                                                            ,hardstop=self.hardstop),
            LbC().GH_MESSAGE_KEY: LbProject().prompt(LbC().GH_MESSAGE_KEY
                                             ,LbProject().get_env_value(LbC().GH_MESSAGE_KEY)
                                             ,hardstop=self.hardstop)
        }

        self.addStep(self.formulate(rc,title=LbC().PROMPTS_KEY))
        #self.addStep('({})'.format(self.formulate(rc)))
        return rc


    def process(self):
        super().process()
        #### Collect Inputs
        print('process PromptRebaseInputs')
        ##* WS_ORGANIZATION is collected from path or user
        ##* WS_WORKSPACE is collected from path or user
        ##* GH_USER is collected from path or user
        ##* GH_PROJECT is collected from path or user
        ##* GH_BRANCH is collected from path or user
        ##* GH_MESSAGE is always collected from user

        self.getStash()[LbC().PROMPTS_KEY] = self.getParameterPrompts()
        #self.setStash(LbC().PROMPTS_KEY,self.getParameterPrompts())

        if self.isVerbose():
            print('verbose LbStash', self.getClassName() )
            pprint(self.getStash())
        return self

class depImputeProjectVariables(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.verbose = False
        self.setStash(stash)
    def process(self):
        super().process()
        #### Impute Variables
        print('process ImputeProjectVariables')
        ##* Impute REPO_URL_KEY
        self.getStash().getProject()[LbC().REPO_URL_KEY] = LbC().REPO_URL_TEMPLATE.format(
            self.getStash(LbC().PROMPTS_KEY)[LbC().GH_USER_KEY],
            self.getStash()[
                LbC().PROMPTS_KEY][
                LbC().GH_PROJECT_KEY])

        if self.isVerbose():
            print('verbose LbStash', self.getClassName())
            pprint(self.getStash())
        self.addStep(self.formulate(self.getStash().getProject(),LbC().PROJECT_KEY))
        #self.addStep('({}({}))'.format(LbC().PROJECT_KEY, self.formulate(self.getStash().getProject())))
        #self.addStep(self.formulate(self.getStash()))

        ##* Impute Project Folder

        devfolder = '{}/Development'.format(os.path.expanduser('~'))
        folder = '{}/{}'.format(devfolder, self.getStash(LbC().PROMPTS_KEY)[LbC().WS_ORGANIZATION_KEY])
        folder = '{}/{}'.format(folder, self.getStash(LbC().PROMPTS_KEY)[LbC().WS_WORKSPACE_KEY])
        folder = '{}/{}'.format(folder, self.getStash(LbC().PROMPTS_KEY)[LbC().GH_PROJECT_KEY])
        self.getStash().getProject()[LbC().PROJECT_FOLDER_KEY] = folder
        return self

class depValidateRebasePromptImputs(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.verbose = False
        self.setStash(stash)
    def process(self):

        print('process Validate Prompts')

        ##* Validate PROMPTS_KEY

        if LbC().PROMPTS_KEY not in self.getStash():  # check for missing key
            self.setInvalid(LbC().PROMPTS_KEY, 'unknown_key')
            if self.isVerbose():
                print('verbose LbStash', self.getClassName())
                pprint(self.getStash())
            return self

        ##* Validate Prompts

        for p in self.getStash(LbC().PROMPTS_KEY):
            self.addStep('validate')
            ##* Invalid when WS_ORGANIZATION in ['', None, 'TBD']
            ##* Invalid WS_WORKSPACE in ['', None, 'TBD']
            ##* Invalid GH_USER in ['', None, 'TBD']
            ##* Invalid GH_PROJECT in ['', None, 'TBD']
            ##* Invalid GH_BRANCH in ['', None, 'TBD']
            ##* Invalid GH_MESSAGE in ['', None, 'TBD']
            if self.getStash(LbC().PROMPTS_KEY)[p] in LbC().INVALID_VALUES:
                self.setInvalid(p, 'bad_value')
                print('    * invalid {}'.format(p))
            else:
                print('    * valid {}'.format(p))

        self.getStash(LbC().PROCESS_KEY).append(self.getSteps())
        print('')
        return self

class depValidateProject(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.verbose = False
        self.setStash(stash)
    def process(self):
        print('Validate Project')
        ##* Validate PROJECT_KEY

        if LbC().PROJECT_KEY not in self.getStash(): # check for missing key
            self.setInvalid(LbC().PROJECT_KEY,'missing_key')
            if self.isVerbose():
                print('verbose LbStash', self.getClassName())
                pprint(self.getStash())
            #return self

        ##* Invalid when Project folder is not found

        folder = self.getStash().getProject()[LbC().PROJECT_FOLDER_KEY]
        if not LbProject().folder_exists(folder): # check for project folder
            self.setInvalid(folder, 'unknown_folder')

        return self

class ValidateRepo(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.verbose = False
        self.setStash(stash)
    def process(self):
        print('Validate Repo')
        self.addStep(self.formulate(self.getStash(),title='lb_stash'))

        ##* Validate REPO_URL_KEY
        if LbC().REPO_URL_KEY  not in self.getStash().getProject(): # check for missing key
            self.setInvalid(LbC().REPO_URL_KEY, 'unknown_key')
            if self.isVerbose():
                print('verbose LbStash', self.getClassName())
                pprint(self.getStash())
            #return self

        ##* Invalid Repo when remote repo is not found

        repo_url = self.getStash().getProject()[LbC().REPO_URL_KEY]
        print('A repo_url', repo_url)
        if not LbProject().hasRemoteProject(repo_url):
            print('B repo_url', repo_url)

            self.setInvalid(LbC().REPO_URL_KEY, 'not_found')

        return self

class ValidateBranch(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.verbose = False
        self.setStash(stash)

    def process(self):
        print('Validate Branch')

        ##* Invalid BRANCH_KEY when value is '', None, or TBD

        if LbC().GH_BRANCH_KEY not in self.getStash(LbC().PROMPTS_KEY):  # check for missing key
            self.setInvalid(LbC().GH_BRANCH_KEY, 'unknown_key')
            if self.isVerbose():
                print('verbose LbStash', self.getClassName())
                pprint(self.getStash())

        ##* Invalid Branch when git branch does not exist

        prompts = self.getStash()[LbC().PROMPTS_KEY]
        if not LbProject().hasBranch(prompts[LbC().GH_BRANCH_KEY]):
            self.setInvalid(LbC().GH_BRANCH_KEY, 'unknown_branch')

        ##* Invalid Branch when branch name is equal to "TBD"

        if LbProject().getBranch() == 'TBD':
            self.setInvalid(LbC().GH_BRANCH_KEY,'undefined_branch')

        ##* Invalid Branch when branch is equal to "main"...as rule don't update main

        if LbProject().getBranch() == 'main':
            self.setInvalid(LbC().GH_BRANCH_KEY,'main_branch_not_updatable')

        return self

class Rebase(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.verbose = False
        self.setStash(stash)

    def depisValid(self):
        ####
        if LbC().INVALID_KEY in self.getStash():
            return False
        return True

    def process(self):
        super().process()
        #### Rebase Project
        print('Rebase')
        #pprint(self.getStash())

        ##* Stop when invalid
        if not self.getStash().isValid():
            pprint(self.getStash())
            print('Terminate Rebase due to invalid settings!')
            exit(0)

        prompts = self.getStash(LbC().PROMPTS_KEY)
        ##*  Checkout branch
        command = 'git checkout {}'.format(prompts[LbC().GH_BRANCH_KEY])
        os.system(command)
        ##* Add files to git
        os.system('git add .')
        ##* Commit with <MESSAGE>
        command = 'git commit -m {}'.format(prompts['GH_MESSAGE'])
        os.system(command)
        ##* Checkout main branch
        os.system('git checkout main')
        ##* Pull origin main
        os.system('git pull origin main')
        ##* Checkout branch
        command = 'git checkout {}'.format(prompts[LbC().GH_BRANCH_KEY])
        os.system(command)
        # feedback
        os.system('git branch')
        ##* Rebase repo
        command = 'git rebase {}'.format(prompts[LbC().GH_BRANCH_KEY])
        os.system(command)
        ##* Push to origin
        if LbProject().prompt('PUSH?', 'N') not in ['N','n']:
            command = 'git push origin {}'.format(prompts[LbC().GH_BRANCH_KEY])
            os.system(command)
        return self

class LbRebaseProcess(LbStepList):
    def __init__(self, lb_stash):
        #LbStepList.__init__(self)
        super().__init__()
        print('============= run')
        self.setStash(lb_stash)  # set shared variables
        ##1. Initilaize Enviromment
        self.add(LbInitializeEnvironment(lb_stash))
        ##1. Prompt Rebase Inputs
        self.add(PromptRebaseInputs(lb_stash).setVerbose(True))
        # #1. Validate Prompts Inputs
        # self.add(LbValidatePromptInputs(lb_stash))
        ##1. Impute Project Variables
        self.add(LbImputeProjectVariables(lb_stash)) # assemble variables before validating
        ##1. Validate Project
        self.add(LbValidateInputVariables(lb_stash))
        ##1. Validate Repo
        self.add(ValidateRepo(lb_stash))
        ##1. Validate Branch
        self.add(ValidateBranch(lb_stash))
        ##1. Rebase
        self.add(Rebase(lb_stash))
        ##1. Status
        self.add(LbStatus(lb_stash).setVerbose(True))
    def isValid(self):
        if self.getStash(LbC().INVALID_KEY) == []:
            return True
        return False
    def hello_world(self):
        print("I am LbRebase!")
        return self

    #def preview(self, msg):
    #    super().preview(msg)
    #    for step in self:
    #        step.preview()
    def run(self):
        super().run()
        return self

def main():
    # will rebase this project
    print('lb_rebase')
    lb_stash = LbStash()
    actual = LbRebaseProcess(lb_stash).run()

    #actual.preview('Run')
def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('script_lb_rebase')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

if __name__ == "__main__":
    # execute as script
    main()