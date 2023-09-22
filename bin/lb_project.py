import os
from source.git_script import GitScript

def main():
    #### LyttleBit Project
    ##Generate bin folders and starter scripts for a bin
    ##     Script name: lb_project.py
    ##### Features
    from pprint import pprint
    start_folder = os.getcwd() # script should start and stop in the same folder
    env_file_name = 'runtime.env'
    src_script_rebase = '{}/scripts/git.rebase.sh'.format(start_folder)
    actual = GitScript()
    assert (actual)
    assert (actual.on_fail_exit()) # should be ok

    ##* Load Enviroment Variables from file
    actual  .print('* INITIALIZE') \
            .set('env_file_name', env_file_name) \
            .load_env(folder=os.getcwd(), filename=env_file_name)

    ##* Confirm Environment Variables with User
    ##* Save Environment Variables

    actual  .set_env("GH_TRUNK", "main") \
            .set_env('WS_ORGANIZATION'
                 ,actual.get_input('WS_ORGANIZATION', actual.get_env_value('WS_ORGANIZATION') or 'TBD', hardstop=False)) \
            .set_env('WS_WORKSPACE'
                 ,actual.get_input('WS_WORKSPACE', actual.get_env_value('WS_WORKSPACE') or 'TBD', hardstop=False)) \
            .set_env('GH_USER', actual.get_input('GH_USER', actual.get_env_value('GH_USER') or 'TBD', hardstop=False)) \
            .set_env('GH_PROJECT'
                 ,actual.get_input('GH_PROJECT', actual.get_env_value('GH_PROJECT') or 'TBD', hardstop=False)) \
            .set_env('GH_BRANCH', actual.get_input('GH_BRANCH', actual.get_env_value('GH_BRANCH') or 'TBD', hardstop=False)) \
            .set_env('GH_MESSAGE'
                 ,actual.get_input('GH_MESSAGE', actual.get_env_value('GH_MESSAGE') or 'TBD', hardstop=False))

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

    ##* Provide Custom GIT Scripts in Repository
    actual  .print('* CREATE SCRIPTS FOLDER')\
            .create_folders(actual.get_project_folder('scripts'))

    actual  .print('* COPY bash scripts')\
            .print('    * {}'.format(src_script_rebase))\
            .copy_to(src_script_rebase, actual.get_project_folder('scripts'), overwrite=False)

    ##* Setup a Working Repository Branch
    ##    * <gh_user>/<issue-number>/\<description>
    ##    * wilfongjt/01/init

    actual  .print('* CREATE BRANCH') \
        .create_branch(project_folder=actual.get_project_folder(), branch=os.environ['GH_BRANCH'])

    actual  .print('* USE') \
        .use(actual.get_project_folder() ,actual.get_env_value('GH_BRANCH'))

    ##* Stage Branch
    actual  .print('* STAGE BRANCH') \
            .stage_branch(os.environ['GH_BRANCH']
                          , actual.get_project_folder()).on_fail_exit()
        #.print('  5. cwd        {}'.format(os.getcwd())) \
        #.print('  5. current br {}'.format(actual.get_branch_current())) \
        #.print('  5. branches   {}'.format(actual.get_branches(actual.get_project_folder())))

    # actual.report()
    ##* Commit Branch
    actual  .print('* COMMIT') \
            .commit_branch(os.environ['GH_BRANCH']
                           , actual.get_project_folder())
        #.print('  6. cwd {}'.format(os.getcwd())) \
        #.print('  6. uncommitted {}'.format(actual.getUncommittedFiles()))
    # actual.report()

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