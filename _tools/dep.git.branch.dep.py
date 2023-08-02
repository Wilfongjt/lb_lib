import os
from pylyttlebit.lb_doc_comments import LbDocComments
from pylyttlebit.lb_project import LbProject
from pylyttlebit.lb_dev_env import LbDevEnv
from pylyttlebit.lb_text_file_helper import LbTextFileHelper
from pylyttlebit.lb_util import LbUtil
from pylyttlebit.lb_folders import LbFolders
from pylyttlebit.lb_constants import LbConstants
def getParameterPrompts():
    return {
        LbConstants().WS_ORGANIZATION_KEY: LbProject().prompt(LbConstants().WS_ORGANIZATION_KEY, LbProject().get_env_value(LbConstants().WS_ORGANIZATION_KEY)),
        LbConstants().WS_WORKSPACE_KEY: LbProject().prompt(LbConstants().WS_WORKSPACE_KEY, LbProject().get_env_value(LbConstants().WS_WORKSPACE_KEY)),
        LbConstants().GH_USER_KEY: LbProject().prompt(LbConstants().GH_USER_KEY, LbProject().get_env_value(LbConstants().GH_USER_KEY)),
        LbConstants().GH_PROJECT_KEY: LbProject().prompt(LbConstants().GH_PROJECT_KEY,LbProject().get_env_value(LbConstants().GH_PROJECT_KEY)),
        LbConstants().GH_BRANCH_KEY: LbProject().prompt(LbConstants().GH_BRANCH_KEY, LbProject().get_env_value(LbConstants().GH_BRANCH_KEY)),
    }
'''

+ Applications
    + lbbranch.app 
    + lbrebase.app
    + lbworkspace.app
+ Users
    + ~
        + Development               dev_folder
            + <organization>        org_folder
                + <workspace>       ws_folder
                    + <project>     prj_folder
                        + _tools    tools_folder
                        + pylyttlebit    lib_folder
                        + scripts   scripts_folder
'''


def getDevelopmentFolder():
    rc = '{}/Development'.format(os.path.expanduser('~'))
    #print('development folder', rc)
    return rc

def getWorkspaceFolder(prompts):
    rc = '{}/Development/{}/{}'.format(os.path.expanduser('~'), prompts[LbConstants().WS_ORGANIZATION_KEY],prompts[LbConstants().WS_WORKSPACE_KEY])
    #print('workspace folder', rc)
    return rc
def getProjectFolder(prompts):
    rc = '{}/Development/{}/{}/{}'.format(os.path.expanduser('~'), prompts[LbConstants().WS_ORGANIZATION_KEY],prompts[LbConstants().WS_WORKSPACE_KEY],prompts[LbConstants().GH_PROJECT_KEY])
    #print('project folder', rc)
    return rc
def getGitHubUrl(prompts):
    rc = LbConstants().REPO_URL_TEMPLATE.format(prompts[LbConstants().GH_USER_KEY], prompts[LbConstants().GH_PROJECT_KEY])
    #print('github url', rc)
    return rc
def getScriptsSourceFolder(prompts):
    rc = '{}/scripts'.format(getProjectFolder(prompts))
    #print('script source folder', rc)
    return rc

def main():
    print('')
    ### Branch Process
    ##1. __Initialize Environment__
    this_folder = os.getcwd()

    ##      * Create default environment file When .env not found
    ##      * Open enviroment file When found in <SOURCE> folder
    devEnv = LbDevEnv().setFilename('.env').open()
    #
    ##      * Impute the Develpment folder name (aka <DEVELOPMENT>), eg ~/Development/
    #
    current_project_folder = os.getcwd().replace('/_tools','')
    #
    ##1. __Collect and Define Inputs__
    #
    ##      * Confirm and Update Inputs with User
    #
    prompts = getParameterPrompts()

    #
    ##      * Stop When workspace ('WS_') settings are invalid
    #
    if not LbProject().verify(prompts, prefix='WS_'): #
        print(prompts)
        print('Stop...Invalid WS value found')
        exit(0)

    #
    ##      * Stop When GitHub ('GH_') settings are invalid
    #
    if not LbProject().verify(prompts, prefix='GH_'):  #
        print(prompts)
        print('Stop...Invalid GH value found')
        exit(0)

    #
    ##      * Stop When remote repo is not found
    #

    if not LbProject().hasRemoteProject(getGitHubUrl(prompts)):
        print('Stop...Repo doenst exist')
        exit(0)

    #
    ##1. __Setup for Develpment__
    #
    ##      * Create Workspace folder When folder doesnt exist
    #
    LbUtil().create_folder(getWorkspaceFolder(prompts))
    #
    ##      * Load settings into environment variables
    #
    devEnv.upsert(prompts)
    #
    ##      * Save environment to .env file in py_workspace folder
    #
    print('* save .env')
    devEnv.save()
    #
    # Start moving files...Switch to workspace folder
    #
    print('* switch to workspace ',  getWorkspaceFolder(prompts))
    os.chdir(getWorkspaceFolder(prompts))
    #
    ##      * Clone the repository (aka Project) When repository is not cloned
    #
    print('* project ',  getProjectFolder(prompts))

    if not LbProject().isCloned(getProjectFolder(prompts)):
        print('* cloning...', end='')
        command = 'git clone {}'.format(getGitHubUrl(prompts))
        os.system(command)
    else:
        print('* skipping...clone. "{}" is already cloned.'.format(prompts[LbConstants().GH_PROJECT_KEY]))
    #
    # Switch to project/repo folder
    #
    os.chdir(getProjectFolder(prompts))
    print('* switch to project/repo', getProjectFolder(prompts))
    #
    ##      * CHECKOUT branch ... get ready for development
    #
    print('branch', LbProject().getCurrentBranch(getProjectFolder(prompts)))
    if LbProject().getCurrentBranch(getProjectFolder(prompts)) != prompts[LbConstants().GH_BRANCH_KEY]:
        command = 'git checkout -b {}'.format(prompts[LbConstants().GH_BRANCH_KEY])
        print('* command', command, end='')
        os.system(command)
        #print('')
    else:
        print('* skipping...checkout. "{}" is already checked out.'.format(prompts[LbConstants().GH_BRANCH_KEY]))

    #
    ##1. __Install Utility Scripts__
    ##      * Create scripts folder in repository clone eg <PROJECT>/scripts
    #
    #scriptsfolder = getScriptsSourceFolder(prompts)
    LbUtil().create_folder(getScriptsSourceFolder(prompts))

    #
    ##      * Copy _tools/scripts/*.sh to <PROJECT>/scripts
    #
    file_names = LbProject().get_file_list(getScriptsSourceFolder(prompts),'sh')
    #file_names = LbProject().get_file_list('{}/scripts'.format(srcFolder),'sh')

    print('* script source folder', getScriptsSourceFolder(prompts))
    #print('* ', '{}_tools'.format())
    print('* scripts', file_names)
    print('* scripts source folder', getScriptsSourceFolder(prompts))
    fn = 'git.branch.sh'
    #currProject = '{}/scripts'.format(getCurrentProject())
    #print('A script', '{}/scripts'.format(srcFolder))
    print('Current Project', current_project_folder)
    #if 1==1: exit(0)
    LbTextFileHelper('{}/scripts'.format(current_project_folder), fn).copyTo(getScriptsSourceFolder(prompts), fn)
    #LbTextFileHelper('{}/scripts'.format(srcFolder), fn).copyTo(getScriptsSourceFolder(prompts), fn)
    fn = 'git.rebase.sh'
    LbTextFileHelper('{}/scripts'.format(current_project_folder), fn).copyTo(getScriptsSourceFolder(prompts), fn)

    #for fn in file_names:
    #    print('fn', fn)
    #    LbTextFileHelper('{}/scripts'.format(srcFolder), fn).copyTo(getScriptsSourceFolder(prompts), fn)

    #
    # # Copy bk.sh to repo/scripts
    #
    #LbTextFileHelper('{}/{}'.format(srcFolder), 'bk.sh').copyTo(getScriptsSourceFolder(prompts), 'bk.sh')

    #print('\n* confirm current branch', LbProject().getCurrentBranch(ws_folder))
    print('* update environment')

    #
    ##      * Save environment to <PROJECT>/scripts
    #
    wsEnv = LbDevEnv().setFolder(getScriptsSourceFolder(prompts)).setFilename('.env').open().save()


if __name__ == "__main__":
    # execute as script
    main()