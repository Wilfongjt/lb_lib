
'''
### Branch Process
## Goal - __Download a GitHub Project__

##* Create Development folder on developer's computer
##* Set a branch

'''
import os
from pprint import pprint
from pylyttlebit.lb_step import LbStep
from pylyttlebit.lb_step_list import LbStepList
from pylyttlebit.lb_project import LbProject
from pylyttlebit.lb_dev_env import LbDevEnv
from pylyttlebit.lb_util import LbUtil
from pylyttlebit.lb_constants import LbConstants
class InitializeEnvironment(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)

    def process(self):
        #### Initialize LyttleBit Application
        print('process IntializeEnvironment')
        ##* Open enviroment file When found in \<SOURCE> folder
        LbDevEnv().setFilename('.env').open()
        #self.getStash()['app']['env'] = LbDevEnv().setFilename('.env').open(),  # put in /pylyttlebit
        ##* Impute the Developement folder name (aka /<DEVELOPMENT>), eg ~/Development
        self.getStash()[LbConstants().DEV_FOLDER_KEY] = '{}/Development'.format(os.path.expanduser('~'))
        ##* Impute the Project folder name (aka \<DEVELOPMENT>/\<Project>), eg ~/Development/\<workspace>/\<project>
        self.getStash()['app'][LbConstants().APP_FOLDER_KEY] = os.getcwd().replace('/pylyttlebit', '').replace('/_tools', '')  # aka current_project_folder

        return self

class CollectInputs(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)

    def getParameterPrompts(self):
        return {
            LbConstants().WS_ORGANIZATION_KEY: LbProject().prompt(LbConstants().WS_ORGANIZATION_KEY,
                                                                  LbProject().get_env_value(LbConstants().WS_ORGANIZATION_KEY)),
            LbConstants().WS_WORKSPACE_KEY: LbProject().prompt(LbConstants().WS_WORKSPACE_KEY,
                                                               LbProject().get_env_value(LbConstants().WS_WORKSPACE_KEY)),
            LbConstants().GH_USER_KEY: LbProject().prompt(LbConstants().GH_USER_KEY,
                                                          LbProject().get_env_value(LbConstants().GH_USER_KEY)),
            LbConstants().GH_PROJECT_KEY: LbProject().prompt(LbConstants().GH_PROJECT_KEY,
                                                             LbProject().get_env_value(LbConstants().GH_PROJECT_KEY)),
            LbConstants().GH_BRANCH_KEY: LbProject().prompt(LbConstants().GH_BRANCH_KEY,
                                                            LbProject().get_env_value(LbConstants().GH_BRANCH_KEY)),
        }

    def process(self):
        #### Collect Inputs
        print('process PromptInputs')
        ##* WS_ORGANIZATION
        ##* WS_WORKSPACE
        ##* GH_USER
        ##* GH_PROJECT
        ##* GH_BRANCH

        self.getStash()[LbConstants().PROMPTS_KEY] = self.getParameterPrompts()
        return self


class ImputeVariables(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)
    def process(self):
        #### Impute Variables
        print('process ImputeProjectVariables')
        ##* Impute project url
        self.getStash()[LbConstants().PROJECT_KEY]['github_url'] = LbConstants().REPO_URL_TEMPLATE.format(self.getStash()[LbConstants().PROMPTS_KEY][LbConstants().GH_USER_KEY],
                                                                                                          self.getStash()[LbConstants().PROMPTS_KEY][LbConstants().GH_PROJECT_KEY])
        return self

class VerifyInputs(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)
    def process(self):
        #### Verify Inputs

        print('process VerifyInputs')
        ##* Stop When workspace ('WS_') settings are invalid
        if not LbProject().verify(self.getStash()[LbConstants().PROMPTS_KEY], prefix='WS_'):  #
            print('Stop...Invalid WS value found')
            exit(0)

        ##* Stop When GitHub ('GH_') settings are invalid
        if not LbProject().verify(self.getStash()[LbConstants().PROMPTS_KEY], prefix='GH_'):  #
            #print(prompts)
            print('Stop...Invalid GH value found')
            exit(0)

        ##* Stop When remote repo is not found
        url = LbConstants().REPO_URL_TEMPLATE.format(self.getStash()[LbConstants().PROMPTS_KEY][LbConstants().GH_USER_KEY],
                                                     self.getStash()[LbConstants().PROMPTS_KEY][LbConstants().GH_PROJECT_KEY])
        if not LbProject().hasRemoteProject(url):
            print('Stop...Repo doenst exist')
            exit(0)

        return self

class CreateWorkspaceFolder(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)
    def process(self):
        print('process CreateProjectFolders')
        #### Create Workspace
        workspace_folder = '{}/Development/{}/{}'.format(os.path.expanduser('~'),
                                                         self.getStash()[LbConstants().PROMPTS_KEY][LbConstants().WS_ORGANIZATION_KEY],
                                                         self.getStash()[LbConstants().PROMPTS_KEY][LbConstants().WS_WORKSPACE_KEY])
        project_folder = '{}/Development/{}/{}/{}'.format(os.path.expanduser('~'),
                                                          self.getStash()[LbConstants().PROMPTS_KEY][LbConstants().WS_ORGANIZATION_KEY],
                                                          self.getStash()[LbConstants().PROMPTS_KEY][LbConstants().WS_WORKSPACE_KEY],
                                                          self.getStash()[LbConstants().PROMPTS_KEY][LbConstants().GH_PROJECT_KEY])

        ##* Create Workspace folder When folder doesnt exist
        LbUtil().create_folder(workspace_folder)
        ##* Store Workspace folder name in Stash
        self.getStash()[LbConstants().PROJECT_KEY]['workspace_folder']=workspace_folder
        ##* Store Projcet folder name in Stash
        self.getStash()[LbConstants().PROJECT_KEY]['project_folder']=project_folder
        return self

class UpdateEnvironment(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)
    def process(self):
        #### Update Environment
        print('process UpdateEnvironment')
        ##* Load settings into environment variables
        LbDevEnv().setFilename('.env').open().upsert(self.getStash()[LbConstants().PROMPTS_KEY])

        return self

class SaveEnv(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)
    def process(self):
        print('process SaveEnv')
        return self

class CloneProject(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)
    def process(self):
        print('process CloneProject')
        return self

def depgetDevelopmentFolder():
    rc = '{}/Development'.format(os.path.expanduser('~'))
    #print('development folder', rc)
    return rc
def depgetProjectFolder(prompts):
    rc = '{}/Development/{}/{}/{}'.format(os.path.expanduser('~'), prompts[LbConstants().WS_ORGANIZATION_KEY],prompts[LbConstants().WS_WORKSPACE_KEY],prompts[LbConstants().GH_PROJECT_KEY])
    #print('project folder', rc)
    return rc
def depgetRemoteProjectUrl():
    gituser = 'gituser'
    projectname = 'projetname'
    rc = LbConstants().REPO_URL_TEMPLATE.format(gituser, projectname)
    print('getRemoteProjectUrl', rc)
    return rc

def depgetScriptsSourceFolder(prompts):
    rc = '{}/scripts'.format(getProjectFolder(prompts))
    #print('script source folder', rc)
    return rc

class LbBranch(LbStepList):

    def __init__(self, stash={}):
        self.setStash(stash) # set shared variables
        self.add(InitializeEnvironment(stash))
        self.add(CollectInputs(stash))
        self.add(ImputeVariables(stash)) # miss values substituted with TBD
        self.add(VerifyInputs(stash))
        self.add(CreateWorkspaceFolder(stash))
        self.add(UpdateEnvironment(stash))
        #self.add(CloneProject(stash))
    def hello_world(self):
        print("I am LbBranch!")
        return self
def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_branch')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

def main():
    # shared variables
    stash = {
        'app': {
        },
        LbConstants().PROJECT_KEY:{}
    }
    actual = LbBranch(stash)
    actual.run()
    pprint(actual.getStash())

if __name__ == "__main__":
    # execute only if run as a script
    main()
    #unittest.main()
