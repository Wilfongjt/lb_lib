import os
from lb_lib.lb_doc_comments import LbDocComments
from lb_lib.lb_project import LbProject
from lb_lib.lb_dev_env import LbDevEnv
from lb_lib.lb_text_file_helper import LbTextFileHelper
from lb_lib.lb_util import LbUtil
def getParameterPrompts():
    return {
        'WS_ORGANIZATION': LbProject().prompt('WS_ORGANIZATION', LbProject().get_env_value('WS_ORGANIZATION')),
        'WS_WORKSPACE': LbProject().prompt('WS_WORKSPACE', LbProject().get_env_value('WS_WORKSPACE')),
        'GH_USER': LbProject().prompt('GH_USER', LbProject().get_env_value('GH_USER')),
        'GH_PROJECT': LbProject().prompt('GH_PROJECT',LbProject().get_env_value('GH_PROJECT')),
        'GH_BRANCH': LbProject().prompt('GH_BRANCH', LbProject().get_env_value('GH_BRANCH')),
    }

def main():
    ### Branch Process
    ##1. __Initialize Environment__
    this_folder = os.getcwd()
    py_mode = 'test'
    if this_folder.endswith('/lb_lib'):
        print('test mode', os.getcwd())
        ##      * Change from test to prod configuration When current folder ends with "/scripts"
        this_folder = this_folder.replace('/scripts', '/lb_lib')
        ##      * Generate script documentation, README.git.branch.py.md When in test mode
    else:
        py_mode = 'prod'
        print('prod mode', os.getcwd())

    ##      * Create default environment file When .env not found
    ##      * Open enviroment file When found in <SOURCE> folder

    devEnv = LbDevEnv().setFilename('.env').open()
    #
    ##      * Impute the Develpment folder name (aka <DEVELOPMENT>), eg ~/Development/
    #
    devfolder = '{}/Development'.format(os.path.expanduser('~'))
    print('devfolder', devfolder)
    #
    ##      * Impute the Application folder name (aka <APP>), eg ~/Development/_tools
    #
    srcFolder =
    if py_mode == 'prod':
        srcFolder = '{}/Development/_tools'.format(os.path.expanduser('~'))
    print('srcFolder', srcFolder)

    if 1 == 1: exit(0)
    #
    ##1. __Collect and Define Inputs__
    #
    ##      * Confirm and Update Inputs with User
    #
    prompts = getParameterPrompts()
    #
    ##      * Impute WS_WORKSPACE URI eg ~/Development/<WS_ORGANIZATION>/<WS_WORKSPACE>
    #
    folder = '{}/{}/{}'.format(devfolder, prompts['WS_ORGANIZATION'], prompts['WS_WORKSPACE'])
    print('* check for workspace folder {} '.format(folder))
    #
    ##      * Impute remote repo URL eg https://github.com/<GH_USER>/<GH_PROJECT>.git
    #
    url = 'https://github.com/{}/{}.git'.format(prompts['GH_USER'], prompts['GH_PROJECT'])
    print('* checking for project repo', url)

    #
    ##1. __Validate Inputs__
    #

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
    if not LbProject().hasRemoteProject(url):
        print('Stop...Repo doenst exist')
        exit(0)
    #
    ##1. __Setup for Develpment__
    #
    #
    ##      * Create Workspace folder When folder doesnt exist
    #
    LbUtil().create_folder(folder)

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
    print('* switch to workspace ', folder)
    os.chdir(folder)
    #
    ##      * Clone the repository (aka Project) When repository is not cloned
    #
    folder = '{}/{}'.format(folder, prompts['GH_PROJECT'])
    if not LbProject().isCloned(folder):
        print('* cloning...', end='')
        command = 'git clone {}'.format(url)
        os.system(command)
    else:
        print('* skipping...clone. "{}" is already cloned.'.format(prompts['GH_PROJECT']))
    #
    # Switch to project/repo folder
    #
    os.chdir(folder)
    print('* switch to project/repo', folder)
    #
    ##      * CHECKOUT branch ... get ready for development
    #
    print('branch', LbProject().getCurrentBranch(folder))
    if LbProject().getCurrentBranch(folder) != prompts['GH_BRANCH']:
        command = 'git checkout -b {}'.format(prompts['GH_BRANCH'])
        print('* command', command, end='')
        os.system(command)
        #print('')
    else:
        print('* skipping...checkout. "{}" is already checked out.'.format(prompts['GH_BRANCH']))

    #
    ##1. __Install Utility Scripts__
    ##      * Create scripts folder in repository clone eg <PROJECT>/scripts
    #
    scriptsfolder = '{}/scripts'.format(folder)
    LbUtil().create_folder(scriptsfolder)

    #
    ##      * Copy _tools/scripts/*.sh to <PROJECT>/scripts
    #
    file_names = LbProject().get_file_list('{}/scripts'.format(srcFolder),'sh')

    for fn in file_names:
        print('fn', fn)
        LbTextFileHelper('{}/scripts'.format(srcFolder), fn).copyTo(scriptsfolder, fn)

    #
    # # Copy bk.sh to repo/scripts
    #
    #LbTextFileHelper('{}/{}'.format(srcFolder), 'bk.sh').copyTo(scriptsfolder, 'bk.sh')

    print('\n* confirm current branch', LbProject().getCurrentBranch(folder))
    print('* update environment')

    #
    ##      * Save environment to <PROJECT>/scripts
    #
    wsEnv = LbDevEnv().setFolder(scriptsfolder).setFilename('.env').open().save()


if __name__ == "__main__":
    # execute as script
    main()