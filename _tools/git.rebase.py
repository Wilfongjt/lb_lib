import os
import subprocess
import webbrowser

from lb_lib.lb_doc_comments import LbDocComments
from lb_lib.lb_project import LbProject

def getParameterPrompts():
    return {
        'WS_ORGANIZATION': LbProject().prompt('WS_ORGANIZATION', LbProject().getOrganization()),
        'WS_WORKSPACE': LbProject().prompt('WS_WORKSPACE', LbProject().getWorkspace()),
        'GH_USER': LbProject().prompt('GH_USER', LbProject().get_env_value('GH_USER')),
        'GH_PROJECT': LbProject().prompt('GH_PROJECT',LbProject().getProject()),
        'GH_BRANCH': LbProject().prompt('GH_BRANCH', LbProject().getBranch()),
        'GH_MESSAGE': LbProject().prompt('GH_MESSAGE', LbProject().get_env_value('GH_MESSAGE'))
    }

def main():
    this_folder = os.getcwd()
    this_file_name = str(__file__).split('/')[-1]
    if this_folder.endswith('/lb_lib'):
        print('test mode')
    else:
        print('prod mode')
    # shift from dev to prod configuration
    this_folder = this_folder.replace('/scripts', '/ws_lib')

    if 1==1: exit(0)
    ### Rebase Process
    #### Dependencies
    ##* lb_lib

    ##1. __Initialize Environment__

    print('Development', LbProject().getDevelopment())
    print('Organization', LbProject().getOrganization())
    print('Workspace', LbProject().getWorkspace())
    print('Project', LbProject().getProject())
    print('Branch', LbProject().getBranch())
    #
    # only run from the <PROJECT-SCRIPTS> folder eg <DEVELOPEMENT>/<ORGANIZATION>/<WORKSPACE>/<PROJECT>/scripts
    #
    ##      * Ensure git.rebase is running from the scripts folder, ie current folder ends with "scripts"
    #

    if not os.getcwd().endswith('scripts'): # development runs from /ws_lib
        print('Stopping... Will not run from repo folder.')
        print('            Not a project/repo scripts folder.')
        print('            Install to _tools and run from git.rebase.sh. {}'.format(os.getcwd()))
        exit(0)
    #
    ##1. __Collect and Define Inputs__
    #
    ##      * Confirm and Update Inputs with User
    #
    prompts = getParameterPrompts()
    #
    ##      * Impute the Develpment folder name (aka <DEVELOPMENT>), eg ~/Development/
    #
    devfolder = '{}/Development'.format(os.path.expanduser('~'))
    #
    ##      * Impute remote repo URL eg https://github.com/<GH_USER>/<GH_PROJECT>.git
    #
    url = 'https://github.com/{}/{}.git'.format(prompts['GH_USER'], prompts['GH_PROJECT'])

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

    print('Development', LbProject().getDevelopment())
    print('Organization', LbProject().getOrganization())
    print('Workspace', LbProject().getWorkspace())
    print('Project', LbProject().getProject())
    #exit(0)
    #
    ##      * Stop when Development folder in not found, eg ~/Development
    #
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
    #
    folder = '{}/{}'.format(folder,prompts['WS_ORGANIZATION'])
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
    #
    folder = '{}/{}'.format(folder,prompts['WS_WORKSPACE'])
    print('* checking folder {} '.format(folder), end='')
    if not LbProject().folder_exists(folder):
        print('stopping...workspace not found')
        exit(0)
    print('ok')
    #
    ##      * Stop when Project folder is not found, eg ~/Development/<WS_ORGANIZATION>/<WS_WORKSPACE>/<GH_PROJECT>
    #
    folder = '{}/{}'.format(folder,prompts['GH_PROJECT'])
    print('* checking folder {} '.format(folder), end='')
    if not LbProject().folder_exists(folder):
        print('stopping...project/repo not found')
        exit(0)
    #print('ok')
    #print('* checking for project repo', url, end='')
    #
    ##      * Stop when remote repo is not found
    #
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
    #
    if not LbProject().hasBranch(prompts['GH_BRANCH']):
        print('stopping...Branch "{}" not found'.format(prompts['GH_BRANCH']))
        exit(0)
    #
    ##      * Stop when branch is equal to "main"
    #
    if LbProject().getBranch() == 'TBD':
        print('stopping...Bad branch')
        exit(0)
    #
    ##      * Stop when branch is equal to "TBD"
    #
    if LbProject().getBranch() == 'main':
        print('stopping...Cannot rebase the "main" branch')
        exit(0)
    #
    ##      * Stop when current branch is "main"
    #
    if LbProject().getCurrentBranch(folder) == 'main':
        print('stopping... commit to "main" branch not allowed!')
        exit(0)
    #
    ##      * Stop when current branch is 'TBD'
    #
    if LbProject().getCurrentBranch(folder) == 'TBD':
        print('stopping... branch not found {} how about {}'.format(prompts['GH_BRANCH'], LbProject().getCurrentBranch(folder)))
        exit(0)

    #if LbProject().getCurrentBranch(folder) != prompts['GH_BRANCH']:
    #    print('stopping... branch not found {} how about {}'.format(prompts['GH_BRANCH'], LbProject().getCurrentBranch(folder)))
    #    exit(0)

    ##

    print('* current branch', LbProject().getCurrentBranch(folder))
    ##1. __Run Git__
    ##      *  Checkout branch
    command = 'git checkout {}'.format(prompts['GH_BRANCH'])
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
    command = 'git checkout {}'.format(prompts['GH_BRANCH'])
    os.system(command)
    # feedback
    os.system('git branch')
    ##      * Rebase repo
    command = 'git rebase {}'.format(prompts['GH_BRANCH'])
    os.system(command)
    ##      * Push to origin
    if LbProject().prompt('PUSH?', 'N') not in ['N','n']:
        command = 'git push origin {}'.format(prompts['GH_BRANCH'])
        os.system(command)

    #print('* update environment')
    #devEnv.upsert(prompts)
    #print('* save .env')
    #devEnv.save()

    ##      * Open Repo on GitHub
    print('open browser')
    #command = 'open -a safari "https://github.com/{}/{}"'.format(prompts['GH_USER'], prompts['GH_PROJECT'])
    #os.system(command)
    url = "https://github.com/{}/{}".format(prompts['GH_USER'], prompts['GH_PROJECT'])
    command =['open', '-a', 'safari', url]
    #subprocess.Popen(command)

    os.system('git status')
    print('done')

    # the webbrowser blocks the funtioning of the command window while the browser is open
    webbrowser.get('safari').open(url, new=2)

if __name__ == "__main__":
    # execute as script
    main()
