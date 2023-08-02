import os
class LbConstants():

    def __init__(self):
        #### Constants
        ##* name a temp_folder in users home folder, eg "~/temp"
        self.TEMP_FOLDER = '{}/Temp'.format(os.path.expanduser('~'))
        ##* name a DISPOSABLE_FOLDER in temp folder, eg "~/temp/disposable"
        self.DISPOSABLE_FOLDER = '{}/disposable'.format(self.TEMP_FOLDER)
        ##* TEMP_FILENAME
        self.TEMP_FILENAME = 'temp_file.txt.env'
        ##* APP_KEY
        self.APP_KEY = 'app'
        ##* APP_FOLDER_KEY
        self.APP_FOLDER_KEY = 'app_folder'
        ##* DEV_KEY
        self.DEV_KEY = 'Development'
        ##* DEV_FOLDER_KEY
        self.DEV_FOLDER_KEY = 'dev_folder'
        ##* FAILED_KEY
        self.FAILED_KEY = 'failed'
        ##* EMPTY_FILENAME
        self.EMPTY_FILENAME = 'empty.txt.env'
        ##* INVALID_KEY
        self.INVALID_KEY = 'invalid'
        ##* invalid_values
        self.INVALID_VALUES = ['', None, 'TBD']
        ##* REPO_URL_KEY
        self.REPO_URL_KEY = 'repo_url'
        ##* repo_url_template_key
        self.REPO_URL_TEMPLATE = 'https://github.com/{}/{}.git'
        ##* PROJECT_KEY
        self.PROJECT_KEY = 'project'
        ##* PROJECT_FOLDER_KEY
        self.PROJECT_FOLDER_KEY= 'folder'
        ##* PROMPTS_KEY
        self.PROMPTS_KEY = 'prompts'
        ##* WORKSPACE_FOLDER_KEY
        self.WORKSPACE_FOLDER_KEY= 'workspace_folder'
        ##* WS_ORGANIZATION_KEY
        self.WS_ORGANIZATION_KEY = 'WS_ORGANIZATION'
        ##* WS_WORKSPACE_KEY
        self.WS_WORKSPACE_KEY = 'WS_WORKSPACE'
        ##* GH_USER_KEY
        self.GH_USER_KEY = 'GH_USER'
        ##* GH_PROJECT_KEY
        self.GH_PROJECT_KEY = 'GH_PROJECT'
        ##* GH_BRANCH_KEY
        self.GH_BRANCH_KEY = 'GH_BRANCH'
        ##* GH_MESSAGE_KEY
        self.GH_MESSAGE_KEY = 'GH_MESSAGE'
    def hello_world(self):
        print("I am LbConstants!")
        return self

class LbC(LbConstants):
    #### Short version of LbConstants
    def __init__(self):
        super().__init__()
def main():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_constants')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

    #print('LbC',LbC())


def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_constants')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()


if __name__ == "__main__":
    # execute as script
    main()