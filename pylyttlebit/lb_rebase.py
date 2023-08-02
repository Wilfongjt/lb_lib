# import unittest
import settings
import os
from pprint import pprint
from pylyttlebit.lb_step import LbStep
from pylyttlebit.lb_step_list import LbStepList
from pylyttlebit.lb_project import LbProject
from pylyttlebit.lb_dev_env import LbDevEnv
from pylyttlebit.lb_util import LbUtil
from pylyttlebit.lb_constants import LbC
from pylyttlebit.lb_folders import LbFolders

####################################
class InitializeEnvironment(LbStep):
    #### Initialize Environment

    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)
    def process(self):
        super().process()
        #self.addStep('process')
        ##* Ensure git.rebase is running from the scripts folder, ie current folder ends with "scripts"

        print('dev    ', LbFolders().getDevelopmentFolder())
        print('org    ', LbFolders().getOrganizationFolder())
        print('ws     ', LbFolders().getWorkspaceFolder())
        print('prj    ', LbFolders().getProjectFolder())
        print('script ', LbFolders().getScriptsFolder())
        print('library', LbFolders().getLibraryFolder())

        #if not os.getcwd().endswith('scripts'):  # development runs from /ws_lib
        #    self.setFailure(self.getClassName()) # record the exception source
        #    print('Stopping... Will not run from repo folder.')
        #    print('            Not a project/repo scripts folder.')
        #    print('            Install to _tools and run from git.rebase.sh.dep. {}'.format(os.getcwd()))
        #    if not self.isTest():
        #        exit(0)

        ##* set project to {}
        print('InitializeEnvironment ')
        self.getStash()[LbC().PROJECT_KEY]={}
        self.getStash()[LbC().PROMPTS_KEY]={}
        #self.getStash()[LbC().PROJECT_KEY]={}
        #self.setStash({}, LbC().PROJECT_KEY)
        ##* set prompts to {}
        #self.get={}

        ##* set prompts to TBD
        self.getStash(LbC().PROMPTS_KEY)[LbC().WS_ORGANIZATION_KEY] = 'TBD'
        self.getStash(LbC().PROMPTS_KEY)[LbC().WS_WORKSPACE_KEY] = 'TBD'
        self.getStash(LbC().PROMPTS_KEY)[LbC().GH_USER_KEY] = 'TBD'
        self.getStash(LbC().PROMPTS_KEY)[LbC().GH_PROJECT_KEY] = 'TBD'
        self.getStash(LbC().PROMPTS_KEY)[LbC().GH_BRANCH_KEY] = 'TBD'

        ##* echo stash when verbose is true
        if self.isVerbose():
            print('verbose Stash', self.getClassName())
            pprint(self.getStash())

        self.addStep(self.formulate(self.getStash()))
        #self.addStep('({})'.format(self.formulate(self.getStash())))
        return self

###########################################
class PromptInputs(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)
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
        #### Collect Inputs as process step
        print('process PromptInputs')
        ##* WS_ORGANIZATION is collected from path or user
        ##* WS_WORKSPACE is collected from path or user
        ##* GH_USER is collected from path or user
        ##* GH_PROJECT is collected from path or user
        ##* GH_BRANCH is collected from path or user
        ##* GH_MESSAGE is always collected from user

        self.getStash()[LbC().PROMPTS_KEY] = self.getParameterPrompts()
        #self.setStash(LbC().PROMPTS_KEY,self.getParameterPrompts())

        if self.isVerbose():
            print('verbose Stash', self.getClassName() )
            pprint(self.getStash())
        return self

class ImputeProjectVariables(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.verbose = False
        self.setStash(stash)
    def process(self):
        super().process()
        #### Impute Variables
        print('process ImputeProjectVariables')
        ##* Impute REPO_URL_KEY
        self.getStash()[LbC().PROJECT_KEY][LbC().REPO_URL_KEY] = LbC().REPO_URL_TEMPLATE.format(
            self.getStash(LbC().PROMPTS_KEY)[LbC().GH_USER_KEY],
            self.getStash()[
                LbC().PROMPTS_KEY][
                LbC().GH_PROJECT_KEY])

        if self.isVerbose():
            print('verbose Stash', self.getClassName())
            pprint(self.getStash())
        self.addStep(self.formulate(self.getStash(LbC().PROJECT_KEY),LbC().PROJECT_KEY))
        #self.addStep('({}({}))'.format(LbC().PROJECT_KEY, self.formulate(self.getStash(LbC().PROJECT_KEY))))
        #self.addStep(self.formulate(self.getStash()))

        ##* Impute Project Folder

        devfolder = '{}/Development'.format(os.path.expanduser('~'))
        folder = '{}/{}'.format(devfolder, self.getStash(LbC().PROMPTS_KEY)[LbC().WS_ORGANIZATION_KEY])
        folder = '{}/{}'.format(folder, self.getStash(LbC().PROMPTS_KEY)[LbC().WS_WORKSPACE_KEY])
        folder = '{}/{}'.format(folder, self.getStash(LbC().PROMPTS_KEY)[LbC().GH_PROJECT_KEY])
        self.getStash(LbC().PROJECT_KEY)[LbC().PROJECT_FOLDER_KEY] = folder
        return self

class ValidatePrompts(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.verbose = False
        self.setStash(stash)
    def process(self):
        print('Validate Development')
        ##* Validate PROMPTS_KEY

        if LbC().PROMPTS_KEY not in self.getStash():  # check for missing key
            self.setInvalid(LbC().PROMPTS_KEY, 'unknown_key')
            if self.isVerbose():
                print('verbose Stash', self.getClassName())
                pprint(self.getStash())
            return self
        ##* Validate Prompts
        for p in self.getStash(LbC().PROMPTS_KEY):
            ##* Invalid when WS_ORGANIZATION in ['', None, 'TBD']
            ##* Invalid WS_WORKSPACE in ['', None, 'TBD']
            ##* Invalid GH_USER in ['', None, 'TBD']
            ##* Invalid GH_PROJECT in ['', None, 'TBD']
            ##* Invalid GH_BRANCH in ['', None, 'TBD']
            ##* Invalid GH_MESSAGE in ['', None, 'TBD']
            if self.getStash(LbC().PROMPTS_KEY)[p] in LbC().INVALID_VALUES:
                #self.setInvalid('x')
                self.setInvalid(p, 'bad_value')
                #self.setInvalid('{}={}'.format(p, self.getStash(LbC().PROMPTS_KEY)[p]))

        return self

class ValidateProject(LbStep):
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
                print('verbose Stash', self.getClassName())
                pprint(self.getStash())
            #return self

        ##* Invalid when Project folder is not found

        folder = self.getStash(LbC().PROJECT_KEY)[LbC().PROJECT_FOLDER_KEY]
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
        ##* Validate REPO_URL_KEY
        if LbC().REPO_URL_KEY  not in self.getStash(LbC().PROJECT_KEY): # check for missing key
            self.setInvalid(LbC().REPO_URL_KEY, 'unknown_key')
            if self.isVerbose():
                print('verbose Stash', self.getClassName())
                pprint(self.getStash())
            #return self

        ##* Invalid Repo when remote repo is not found

        repo_url = self.getStash()[LbC().PROJECT_KEY][LbC().REPO_URL_KEY]
        if not LbProject().hasRemoteProject(repo_url):
            self.setInvalid(LbC().REPO_URL_KEY, 'not_found')

        return self

class ValidateBranch(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.verbose = False
        self.setStash(stash)

    def process(self):
        print('Validate Branch')
        ##* Validate BRANCH_KEY

        if LbC().GH_BRANCH_KEY not in self.getStash(LbC().PROMPTS_KEY):  # check for missing key
            self.setInvalid(LbC().GH_BRANCH_KEY, 'unknown_key')
            if self.isVerbose():
                print('verbose Stash', self.getClassName())
                pprint(self.getStash())

        ##* Invalid Branch when branch does not exist

        prompts = self.getStash()[LbC().PROMPTS_KEY]
        if not LbProject().hasBranch(prompts[LbC().GH_BRANCH_KEY]):
            self.setInvalid(LbC().GH_BRANCH_KEY, 'unknown_branch')

        ##* Invalid Branch when branch is equal to "TBD"

        if LbProject().getBranch() == 'TBD':
            self.setInvalid(LbC().GH_BRANCH_KEY,'undefined_branch')

        ##* Invalid Branch when branch is equal to "main"

        if LbProject().getBranch() == 'main':
            self.setInvalid(LbC().GH_BRANCH_KEY,'main_branch_not_updatable')

        return self

class Rebase(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.verbose = False
        self.setStash(stash)

    def isValid(self):
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
        if not self.isValid():
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
    def __init__(self, stash={}):
        LbStepList.__init__(self)
        print('============= run')
        self.setStash(stash)  # set shared variables
        ##1. Initilaize Enviromment
        self.add(InitializeEnvironment(stash))
        ##1. Prompt Inputs
        self.add(PromptInputs(stash).setVerbose(True))
        ##1. Impute Project Variables
        self.add(ImputeProjectVariables(stash)) # assemble variables before validating
        ##1. Validate Prompts
        self.add(ValidatePrompts(stash))
        ##1. Validate Project
        self.add(ValidateProject(stash))
        ##1. Validate Repo
        self.add(ValidateRepo(stash))
        ##1. Validate Branch
        self.add(ValidateBranch(stash))
        ##1. Rebase
        self.add(Rebase(stash))

    def isValid(self):
        if self.getStash(LbC().INVALID_KEY) == []:
            return True
        return False
    def hello_world(self):
        print("I am LbRebase!")
        return self

    def preview(self, msg):
        super().preview(msg)
        for step in self:
            step.preview()
    def run(self):
        super().run()
        return self

def main():
    # will rebase this project
    print('lb_rebase')
    actual = LbRebaseProcess().run()

    actual.preview('Run')
def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_doc_folders')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

if __name__ == "__main__":
    # execute as script
    main()