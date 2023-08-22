import os
import subprocess
import webbrowser

from pylyttlebit.lb_doc_comments import LbDocComments
from pylyttlebit.lb_project import LbProject
from pylyttlebit.lb_constants import LbConstants

def getParameterPrompts():
    return {
        LbConstants().WS_ORGANIZATION_KEY: LbProject().prompt(LbConstants().WS_ORGANIZATION_KEY, LbProject().getOrganizationFromPath()),
        LbConstants().WS_WORKSPACE_KEY: LbProject().prompt(LbConstants().WS_WORKSPACE_KEY, LbProject().getWorkspaceFromPath()),
        LbConstants().GH_USER_KEY: LbProject().prompt(LbConstants().GH_USER_KEY, LbProject().get_env_value(LbConstants().GH_USER_KEY)),
        LbConstants().GH_PROJECT_KEY: LbProject().prompt(LbConstants().GH_PROJECT_KEY, LbProject().getProjectFromPath()),
        LbConstants().GH_BRANCH_KEY: LbProject().prompt(LbConstants().GH_BRANCH_KEY, LbProject().getBranch()),
        'GH_MESSAGE': LbProject().prompt('GH_MESSAGE', LbProject().get_env_value('GH_MESSAGE'))
    }

def main():
    this_folder = os.getcwd()
    this_file_name = str(__file__).split('/')[-1]
    if this_folder.endswith('/pylyttlebit'):
        print('test mode')
    else:
        print('prod mode')
    # shift from dev to prod configuration
    this_folder = this_folder.replace('/scripts', '/ws_lib')

    if 1==1: exit(0)
    ### Rebase Process
    #### Dependencies
    ##* pylyttlebit

    ##1. __Initialize Environment__

    print('Development', LbProject().getDevelopmentFromPath())
    print('Organization', LbProject().getOrganizationFromPath())
    print('Workspace', LbProject().getWorkspaceFromPath())
    print('Project', LbProject().getProjectFromPath())
    print('Branch', LbProject().getBranch())
    #
    # only run from the <PROJECT-SCRIPTS> folder eg <DEVELOPEMENT>/<ORGANIZATION>/<WORKSPACE>/<PROJECT>/scripts
    #
    ##      * Ensure git.rebase is running from the scripts folder, ie current folder ends with "scripts"
    #

    if not os.getcwd().endswith('scripts'): # runs from /scripts folder
        print('Stopping... Will not run from repo folder.')
        print('            Not a project/repo scripts folder.')
        print('            Install to _tools and run from git.rebase.sh.dep. {}'.format(os.getcwd()))
        exit(0)
    #
    ##1. __Collect and Define Inputs__
    #
    ##      * Confirm and Update Inputs with User
    # OK
    prompts = getParameterPrompts()
    #
    ##      * Impute the Develpment folder name (aka <DEVELOPMENT>), eg ~/Development/
    # ok
    devfolder = '{}/Development'.format(os.path.expanduser('~'))
    #
    ##      * Impute remote repo URL eg https://github.com/<GH_USER>/<GH_PROJECT>.git
    # ok
    url = LbConstants().REPO_URL_TEMPLATE.format(prompts[LbConstants().GH_USER_KEY], prompts[LbConstants().GH_PROJECT_KEY])

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

    print('Development', LbProject().getDevelopmentFromPath())
    print('Organization', LbProject().getOrganizationFromPath())
    print('Workspace', LbProject().getWorkspaceFromPath())
    print('Project', LbProject().getProjectFromPath())
    #exit(0)
    #
    ##      * Stop when Development folder in not found, eg ~/Development
    # ok
    folder = devfolder
    print('* checking folder {} '.format(folder), end='')
    if not LbProject().folder_exists(folder):
        print('stopping...development not found')
        exit(0)
    print('ok')
    #
    # Switch to development folder
    #
    os.chdir(folder)
    #
    ##      * Stop when Organization fold is not found, eg ~/Development/<WS_ORGANIZATION>
    # ok test for project instead
    folder = '{}/{}'.format(folder,prompts[LbConstants().WS_ORGANIZATION_KEY])
    print('* checking folder {} '.format(folder), end='')
    if not LbProject().folder_exists(folder):
        print('stopping...organization not found')
        exit(0)
    print('ok')
    #
    # Switch to organization folder
    #
    os.chdir(folder)
    #
    ##      * Stop when Workspace folder is not found, eg ~/Development/<WS_ORGANIZATION>/<WS_WORKSPACE>
    # # ok test for project instead
    folder = '{}/{}'.format(folder,prompts[LbConstants().WS_WORKSPACE_KEY])
    print('* checking folder {} '.format(folder), end='')
    if not LbProject().folder_exists(folder):
        print('stopping...workspace not found')
        exit(0)
    print('ok')
    #
    ##      * Stop when Project folder is not found, eg ~/Development/<WS_ORGANIZATION>/<WS_WORKSPACE>/<GH_PROJECT>
    # ok test for project instead
    folder = '{}/{}'.format(folder,prompts[LbConstants().GH_PROJECT_KEY])
    print('* checking folder {} '.format(folder), end='')
    if not LbProject().folder_exists(folder): # check for project folder
        print('stopping...project/repo not found')
        exit(0)
    #print('ok')
    #print('* checking for project repo', url, end='')
    #
    ##      * Stop when remote repo is not found
    # Ok
    if not LbProject().hasRemoteProject(url):
        print('Stop...Repo doesnt exist')
        exit(0)
    print(' ok')
    #
    # Switch to repo folder
    #
    os.chdir(folder)
    print('* Switch to ', folder)
    #
    ##      * Stop when branch does not exist
    # ok
    if not LbProject().hasBranch(prompts[LbConstants().GH_BRANCH_KEY]):
        print('stopping...Branch "{}" not found'.format(prompts[LbConstants().GH_BRANCH_KEY]))
        exit(0)
    #
    ##      * Stop when branch is equal to "TBD"
    # ok
    if LbProject().getBranch() == 'TBD':
        print('stopping...Bad branch')
        exit(0)
    #
    ##      * Stop when branch is equal to "main"
    # ok
    if LbProject().getBranch() == 'main':
        print('stopping...Cannot rebase the "main" branch')
        exit(0)
    #
    ##      * Stop when current branch is "main"
    # not needed
    if LbProject().getCurrentBranch(folder) == 'main':
        print('stopping... commit to "main" branch not allowed!')
        exit(0)
    #
    ##      * Stop when current branch is 'TBD'
    # not needed
    if LbProject().getCurrentBranch(folder) == 'TBD':
        print('stopping... branch not found {} how about {}'.format(prompts[LbConstants().GH_BRANCH_KEY], LbProject().getCurrentBranch(folder)))
        exit(0)

    #if LbProject().getCurrentBranch(folder) != prompts[LbConstants().GH_BRANCH_KEY]:
    #    print('stopping... branch not found {} how about {}'.format(prompts[LbConstants().GH_BRANCH_KEY], LbProject().getCurrentBranch(folder)))
    #    exit(0)

    ##

    print('* current branch', LbProject().getCurrentBranch(folder))
    ##1. __Run Git__
    ##      *  Checkout branch
    command = 'git checkout {}'.format(prompts[LbConstants().GH_BRANCH_KEY])
    os.system(command)
    ##      * Add files to git
    os.system('git add .')
    ##      * Commit with <MESSAGE>
    command = 'git commit -m {}'.format(prompts['GH_MESSAGE'])
    os.system(command)
    ##      * Checkout main branch
    os.system('git checkout main')
    ##      * Pull origin main
    os.system('git pull origin main')
    ##      * Checkout branch
    command = 'git checkout {}'.format(prompts[LbConstants().GH_BRANCH_KEY])
    os.system(command)
    # feedback
    os.system('git branch')
    ##      * Rebase repo
    command = 'git rebase {}'.format(prompts[LbConstants().GH_BRANCH_KEY])
    os.system(command)
    ##      * Push to origin
    if LbProject().prompt('PUSH?', 'N') not in ['N','n']:
        command = 'git push origin {}'.format(prompts[LbConstants().GH_BRANCH_KEY])
        os.system(command)

    #print('* update environment')
    #devEnv.upsert(prompts)
    #print('* save .env')
    #devEnv.save()

    ##      * Open Repo on GitHub
    print('open browser')
    #command = 'open -a safari "https://github.com/{}/{}"'.format(prompts[LbConstants().GH_USER], prompts[LbConstants().GH_PROJECT_KEY])
    #os.system(command)
    url = "https://github.com/{}/{}".format(prompts[LbConstants().GH_USER_KEY], prompts[LbConstants().GH_PROJECT_KEY])
    command =['open', '-a', 'safari', url]
    #subprocess.Popen(command)

    os.system('git status')
    print('done')

    # the webbrowser blocks the funtioning of the command window while the browser is open
    webbrowser.get('safari').open(url, new=2)

if __name__ == "__main__":
    # execute as script
    main()
