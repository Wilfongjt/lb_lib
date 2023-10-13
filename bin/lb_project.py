import os

import source.api.hapi.server_js
from source.git_script import GitScript
from source.hapi_script import HAPIScript

class TemplateKeysAndValues(list):
    # eg {"<some-name>": "somevalue",...}
    def __init__(self):
        for k in os.environ:
            if k.startswith('GH_') or k.startswith('WS_'):
                nm = '<{}>'.format(k.lower().replace('_','-'))
                vl = os.environ[k]
                self.append({"name": nm, "value": vl})
'''
class EnvironmentKeysAndValues(dict):
    # eg {"WS_ORGANIZATION": "lyttlebit",...}
    def __init__(self):
        for k in os.environ:
            if k.startswith('GH_') or k.startswith('WS_'):
                self[k] = os.environ[k]
'''

def main():
    #### LyttleBit Project
    ##Generate bin folders and starter scripts for a bin
    ##     Script name: lb_project.py
    ##### Features

    from pprint import pprint

    start_folder = '/'.join(os.getcwd().split('/')[0:-1]) # script should start and stop in the same folder
    env_file_name = 'runtime.env'
    src_script_rebase = '{}/scripts/git.rebase.sh'.format(start_folder)
    src_script_issues = '{}/scripts/git.issues.sh'.format(start_folder)

    # actual = GitScript()
    actual = HAPIScript()
    assert (actual)
    assert (actual.on_fail_exit()) # should be ok

    ##* Load Enviroment Variables from file
    actual  .print('* INITIALIZE') \
            .set('env_file_name', env_file_name) \
            .load_env(folder=start_folder, filename=env_file_name)

    ##* Confirm Environment Variables with User
    ##* Save Environment Variables

    env_list = ["GH_TRUNK", "WS_ORGANIZATION","WS_WORKSPACE","GH_USER","GH_PROJECT","GH_BRANCH","GH_MESSAGE"]
    for env_title in env_list:
        actual.set_env(env_title,actual.get_input(env_title, actual.get_env_value(env_title) or 'TBD', hardstop=False) )

    ##* Validate Environment Variables
    actual  .print('* VALIDATE INPUTS') \
        .validate_inputs(prefix=['WS_', 'GH_']).on_fail_exit()

    ##* Create Project Folders when bin folder is not found
    actual  .print('* CREATE WORKSPACE') \
        .create_workspace(actual.get_workspace_folder()).on_fail_exit()

    ##* Clone Existing Repository when clone is not found
    actual  .print('* CLONE') \
        .clone_project_in(actual.get('GH_USER')
                          , actual.get('GH_PROJECT')
                          , actual.get_workspace_folder()).on_fail_exit()

    actual  .print('* CREATE BRANCH') \
        .create_branch(project_folder=actual.get_project_folder(), branch=os.environ['GH_BRANCH'])

    actual  .print('* USE') \
        .use(actual.get_project_folder() ,actual.get_env_value('GH_BRANCH'))

    ##* Provide Custom GIT Scripts in Repository
    actual  .print('* CREATE SCRIPTS FOLDER')\
            .create_folders(actual.get_project_folder('scripts'))

    actual  .print('* COPY bash scripts')\
            .print('    * {}'.format(src_script_rebase)) \
            .print('    * {}'.format(src_script_issues)) \
            .copy_to(src_script_rebase, actual.get_project_folder('scripts'), overwrite=True) \
            .copy_to(src_script_issues, actual.get_project_folder('scripts'), overwrite=True)

    ##* Create HAPI code
    #print('actual', TemplateKeysAndValues())
    #print('env nv',EnvironmentKeysAndValues())
    actual  .print('* API HAPI')\
            .create_hapi( actual.get_input('Api', 'N', hardstop=False),TemplateKeysAndValues())

    ##* Stage Branch
    actual  .print('* STAGE BRANCH') \
            .stage_branch(os.environ['GH_BRANCH']
                          , actual.get_project_folder()).on_fail_exit()

    ##* Commit Branch
    actual  .print('* COMMIT') \
            .commit_branch(os.environ['GH_BRANCH']
                           , actual.get_project_folder())

    #actual  .print('* REBASE') \
    #    .rebase(actual.get_project_folder() ,os.environ['GH_BRANCH'])

    # actual.report()

    #actual  .print('* PUSH BRANCH') \
    #    .push_branch(actual.get_input('Push', 'N', hardstop=False)
    #                 , actual.get_project_folder()
    #                 , os.environ['GH_BRANCH'])
    actual.report()
    ##### Project Folders
    ##```
    ##<user>
    ##    + Development
    ##        + <workspace>
    ##            + <bin-name>
    ##                + scripts
    ##```
    #actual  .write_to(actual.get_project_folder(), "test_file.txt", "hello world\n") \
    #    .show_git_hub(os.environ['GH_USER'], os.environ['GH_PROJECT'])
    #        .copy_to('{}/{}'.format(actual['env_folder_name'],actual['env_file_name']), actual.get_project_folder())\

    #print('final folder {}'.format(os.getcwd()))
    # assert(start_folder==os.getcwd()) # script should start and stop in the same folder
    #print('curr folder', os.getcwd())

def main_document():
    from source.lb_doc_comments import LbDocComments
    print('lb_project')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()


if __name__ == "__main__":
    # execute as script
    main()
    #mainProjectScript()