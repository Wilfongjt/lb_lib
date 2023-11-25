import os
import re
from source.lb_exceptions import UnmergedKeyException
from source.lb_util import LbUtil
from source.lb_os_commands import LbOsCommands
from source.git_script import LbGitProcess
#from source.lb_template import LbBashTemplate

class ProjectString(str):
    ##Formalize the naming of commonly used folders
    ##* use the project string as a base eg "~/Development/organization-name/workspace-name/project-name"
    def getClassName(self) -> str:
        ##__Get Class Name on request__
        ##* returns current class name
        return self.__class__.__name__

    def getOrganizationName(self):
        ##* Return the Organization Name
        rc = self.split('/')
        rc = rc[rc.index('Development') + 1]
        return rc

    def getWorkspaceName(self):
        ##* Return the Workspace Name
        rc = self.split('/')
        rc = rc[rc.index('Development') + 2]
        return rc

    def getProjectName(self):
        ##* Return the Project Name
        rc = self.split('/')
        rc = rc[rc.index('Development') + 3]
        return rc

    def getDevelopmentFolder(self):
        ##* Return the Development Folder Name
        return '{}/Development'.format(os.environ['HOME'])

    def getOrganizationFolder(self):
        ##* Return the Organization Folder Name
        rc = self.split('/')
        rc = rc[0:rc.index('Development') + 2]
        return '/'.join(rc)

    def getWorkspaceFolder(self):
        ##* Return the Workspace Folder Name
        rc = self.split('/')
        rc = rc[0:rc.index('Development') + 3]
        return '/'.join(rc)

    def getProjectFolder(self, subfolder=None):
        ##* Return the Project Folder Name
        rc = self.split('/')
        rc = rc[0:rc.index('Development') + 4]
        if subfolder:
            rc.append(subfolder)
        return '/'.join(rc)

    def show(self):
        print(self.getClassName())
        print('    organization-name :', self.getOrganizationName())
        print('    workspace-name    :', self.getWorkspaceName())
        print('    project-name      :', self.getProjectName())
        print('    dev-folder        :', self.getDevelopmentFolder())
        print('    org-folder        :', self.getOrganizationFolder())
        print('    workspace-folder  :', self.getWorkspaceFolder())
        print('    project-folder    :', self.getProjectFolder())

    ##<br/>
    ##__Issues:__
    ##* none
    ##<br/><br/>
'''
class LbProjectFolder(ProjectString):
    ##Extend ProjectString into a template
    def __new__(self, name_value_list):
        ##* name_value_list eg [{'name':'', 'value':''}...]
        string_value = '{}/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<GH_PROJECT>>'.format(os.environ['HOME'])
        for k in name_value_list:
            string_value = string_value.replace(k['name'], k['value'])
        instance = super().__new__(self, string_value)
        return instance

    ##<br/><br/>
    ##__Issues:__
    ##* none
    ##<br/><br/>
'''


class DevelopmentString(str):
    ##Formalize the naming of commonly used folders
    ##* use the development string as a base eg "~/Development/organization-name/workspace-name/project-name"
    def getClassName(self) -> str:
        ##__Get Class Name on request__
        ##* returns current class name
        return self.__class__.__name__

    def getOrganizationName(self):
        ##* Return the Organization Name
        rc = self.split('/')
        rc = rc[rc.index('Development') + 1]
        return rc

    def getWorkspaceName(self):
        ##* Return the Workspace Name
        rc = self.split('/')
        rc = rc[rc.index('Development') + 2]
        return rc

    def getProjectName(self):
        ##* Return the Project Name
        rc = self.split('/')
        rc = rc[rc.index('Development') + 3]
        return rc

    def getDevelopmentFolder(self):
        ##* Return the Development Folder Name
        return '{}/Development'.format(os.environ['HOME'])

    def getOrganizationFolder(self):
        ##* Return the Organization Folder Name
        rc = self.split('/')
        rc = rc[0:rc.index('Development') + 2]
        return '/'.join(rc)

    def getWorkspaceFolder(self):
        ##* Return the Workspace Folder Name
        rc = self.split('/')
        rc = rc[0:rc.index('Development') + 3]
        return '/'.join(rc)

    def getProjectFolder(self, subfolder=None):
        ##* Return the Project Folder Name
        rc = self.split('/')
        rc = rc[0:rc.index('Development') + 4]
        if subfolder:
            rc.append(subfolder)
        return '/'.join(rc)

    def show(self):
        print(self.getClassName())
        print('organization:', self.getOrganizationName())

    ##<br/>
    ##__Issues:__
    ##* none
    ##<br/><br/>


class FolderString(str):
    def __init__(self):
        super().__init__()
        self.data = []
        self.context=None
    def getClassName(self) -> str:
        ##__Get Class Name on request__
        ##* returns current class name
        return self.__class__.__name__

    def set_context(self, context):
        self.context = context
        return self

    def getFolder(self):
        return self

    def get_context(self):
        return self.context

    def set_data(self, nv_data):
        self.data = nv_data
        return self
    def get_data(self, name=None):
        ##* plug in name and value data
        rc = None
        if not name:
            rc = self.data
        else:
            for t in self.data:
                #print('t',t)
                if name == t['name']:
                    #rc = self.data[name]
                    rc = t['value']

        return rc
    def getName(self):
        ##* Return the Folder Type Name
        rc = self.split('/')
        rc = rc[-1]
        return rc

    def get_unmerged_keys(self):
        input_text = self
        pattern = r"<<([A-Za-z_-]+)>>|<<([A-Za-z]+_[A-Za-z_-]+)>>"
        matches = re.findall(pattern, input_text)
        # Flatten the list of tuples
        matches = [match[0] if match[0] else match[1] for match in matches]
        return matches

    def has_unmerged_keys(self):
        #### Get list of keys from self
        rc = False
        keys = self.get_unmerged_keys()
        if len(keys) > 0:
            rc = True
        return rc

    def create(self):
        self.validate()
        os.makedirs(self, exist_ok=True)
        return self

    def exists(self):
        folder = self
        #### Test if a given folder exists on request
        ##* folder exists when found on drive ... [x] has test
        exists = os.path.isdir('{}'.format(folder))
        ##* returns bool ... [x] has test
        #print('exists', folder, exists)

        return exists
    def merge(self):
        return self

    def validate(self):
        if self.has_unmerged_keys():
            raise UnmergedKeyException('Unmerged name {}'.format(self.get_unmerged_keys()))
        return self

    def open(self):
        return self
    def save(self):
        return self

    def assertExists(self):
        #### Test that file gets written
        #assert (LbUtil().folder_exists(self))
        assert (self.exists())
        return self

    def show(self):
        print(self.getClassName())
        print('  actual       : ', self)
        print('  unmerged-keys:', self.get_unmerged_keys())
        print('  unmerged     :', self.has_unmerged_keys())

    def process(self):
        print('process', self)
        return self



class LbDevelopmentFolder(FolderString):
    def __new__(cls,folder_string=None):
        if not folder_string:
            folder_string = os.getcwd()
        offset = 1
        f_str = folder_string.split('/')
        f_str = f_str[0:f_str.index('Development')+offset]
        f_str = '/'.join(f_str)
        instance = super().__new__(cls, f_str)
        return instance

class LbOrganizationFolder(FolderString):
    def __new__(cls,folder_string=None):
        if not folder_string:
            folder_string = os.getcwd()
        offset = 2
        f_str = folder_string.split('/')
        f_str = f_str[0:f_str.index('Development') + offset]
        f_str = '/'.join(f_str)
        instance = super().__new__(cls, f_str)
        return instance

class LbWorkspaceFolder(FolderString):
    def __new__(cls,folder_string=None):
        if not folder_string:
            folder_string = os.getcwd()
        offset = 3
        f_str = folder_string.split('/')
        f_str = f_str[0:f_str.index('Development') + offset]
        f_str = '/'.join(f_str)
        instance = super().__new__(cls, f_str)
        return instance

class LbProjectFolder(FolderString):
    def __new__(cls,folder_string=None):
        if not folder_string:
            folder_string = os.getcwd()
        offset = 4
        f_str = folder_string.split('/')
        print('LbProjectFolder', f_str)
        f_str = f_str[0:f_str.index('Development') + offset]
        f_str = '/'.join(f_str)
        instance = super().__new__(cls, f_str)
        return instance

class depLbScriptsFolder(FolderString):
    def __new__(cls,folder_string=None):
        if not folder_string:
            folder_string = os.getcwd()
        offset = 4
        f_str = folder_string.split('/')
        f_str = f_str[0:f_str.index('Development') + offset]
        f_str.append('scripts')
        f_str = '/'.join(f_str)
        instance = super().__new__(cls, f_str)
        return instance

class LbTemplateFolder(FolderString):
    def __init__(self, context, folder_string=None):
        super().__init__()

    def __new__(cls,context, folder_string=None):
        # context eg "bass" or "bash/special"
        if not folder_string:
            folder_string = os.getcwd()
        offset = 4
        cntxt = context.split('/')
        #print('context', cntxt)
        f_str = folder_string.split('/')
        f_str = f_str[0:f_str.index('Development') + offset]
        f_str.append('source')
        f_str.append('template')
        f_str.extend(cntxt)
        f_str = '/'.join(f_str)
        instance = super().__new__(cls, f_str)
        return instance
'''
class LbWorkspaceFolder(str):
    def __new__(cls,folder_string=None):
        if not folder_string:
            folder_string = os.getcwd()
        hm = '{}'.format(os.environ['HOME'])
        org = folder_string.split('/')
        org = org[org.index('Development') + 1]
        ws = folder_string.split('/')
        ws = ws[ws.index('Development') + 2]
        inst = '{}/Development/{}/{}'.format(hm, org, ws)
        instance = super().__new__(cls, inst)
        return instance

    def getName(self):
        ##* Return the Organization Name
        rc = self.split('/')
        rc = rc[rc.index('Development') + 2]
        return rc

class LbProjectFolder(str):
    def __new__(cls,folder_string=None):
        if not folder_string:
            folder_string = os.getcwd()
        hm = '{}'.format(os.environ['HOME'])
        print('folder_string', folder_string)
        org = folder_string.split('/')
        org = org[org.index('Development') + 1]
        ws = folder_string.split('/')
        ws = ws[ws.index('Development') + 2]
        prj = folder_string.split('/')
        prj = prj[prj.index('Development') + 3]
        inst = '{}/Development/{}/{}'.format(hm, org, ws, prj)
        instance = super().__new__(cls, inst)
        return instance

    def getName(self):
        ##* Return the Organization Name
        rc = self.split('/')
        print('rc',rc)
        rc = rc[rc.index('Development') + 3]
        return rc
'''
class WorkspaceFolderTemplate(FolderString):
    def __init__(self, name_value_list):
        super().__init__()
        self.set_data(name_value_list)

    def __new__(self, name_value_list):
        ##* name_value_list eg [{'name':'', 'value':''}...]
        string_value = '{}/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>'.format(os.environ['HOME'])
        for k in name_value_list:
            string_value = string_value.replace(k['name'], k['value'])
        instance = super().__new__(self, string_value)
        return instance

    def create(self):
        ## Make workspace folder when folder doenst exist
        super().create()
        #self.makedirs(self) # (self, exist_ok=True)
        return self
    def process(self):
        super().process()
        self.create()
        return self
    #def assertExists(self):
    #    #### Test that file gets written
    #    #assert (LbUtil().file_exists(self.getFolder(),self.getFilename()))
    #    super().assertExists()
    #    return self

class GitProjectFolderTemplate(LbGitProcess, FolderString):
    def __init__(self, name_value_list):
        LbGitProcess.__init__(self)
        self.set_data(name_value_list)
        #self.data = name_value_list

    def __new__(self, name_value_list):
        ##* name_value_list eg [{'name':'', 'value':''}...]
        string_value = '{}/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<GH_PROJECT>>'.format(os.environ['HOME'])
        for k in name_value_list:
            string_value = string_value.replace(k['name'], k['value'])
        instance = super().__new__(self, string_value)
        return instance

    def create(self):
        ##*Create project folder by cloning from github when folder doesnt exist
        # super().create()
        if not self.exists():
            print('-clone start')
            print('a cwd',os.getcwd())

            last_dir= os.getcwd()
            gh_user=self.get_data('<<GH_USER>>')
            gh_project=self.get_data('<<GH_PROJECT>>')
            workspace_folder = '/'.join(self.split('/')[0:-1])
            self.clone_project_in(gh_user, gh_project, workspace_folder=workspace_folder)
            print('b cwd',os.getcwd())
            self.ch_dir(last_dir)
            print('c cwd',os.getcwd())

            print('-clone done')
        return self

    def process(self):
        super().process()
        self.create()
        return self

class ScriptsFolderTemplate(LbOsCommands, FolderString):
    #### Target folder for scripts
    def __init__(self, name_value_list):
        LbOsCommands.__init__(self)
        self.set_data(name_value_list)

    def __new__(self, name_value_list):
        print('---')
        ##* name_value_list eg [{'name':'', 'value':''}...]
        string_value = '{}/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>/<<GH_PROJECT>>/scripts'.format(os.environ['HOME'])
        print('name_value_list',name_value_list)
        for k in name_value_list:
            print('k',k, type(k))
            print('name', k['name'])
            print('value',k['value'])
            string_value = string_value.replace(k['name'], k['value'])
        print('string_value', string_value)
        instance = super().__new__(self, string_value)
        print('out new')
        return instance

    def create(self):
        ##* Create project/scripts folder in project when folder doesnt exist
        super().create()
        #self.makedirs(self)
        #template_list = [] #self.get_file_list(LbTemplateFolder(self.get_context()))
        #for tmpl in template_list:
        #    print('target', self)
        #    print('tmpl', tmpl)
            #LbBashTemplate().setFolder(self)
        #if not self.exists():
            ##* create bash scripts from templates
            #gh_user=self.get_data('<<GH_USER>>')
            #gh_project=self.get_data('<<GH_PROJECT>>')
            #workspace_folder = '/'.join(self.split('/')[0:-1])
            #self.clone_project_in(gh_user, gh_project, workspace_folder=workspace_folder)

        return self

def mainFolderString(nv_list):
    print('mainFolderString')
    actual = FolderString()
    print(actual)
    assert(actual=='')
    assert (actual.getName() == '')
    assert (actual.get_unmerged_keys() == [])
    assert (actual.has_unmerged_keys() == False)
    actual.show()

    print('---')
def mainWorkspaceFolderTemplate(nv_list):
    print('mainWorkspaceFolderTemplate')

    actual = WorkspaceFolderTemplate([])
    assert (actual == '{}/Development/<<WS_ORGANIZATION>>/<<WS_WORKSPACE>>'.format(os.environ['HOME']))
    assert (actual.has_unmerged_keys() == True)
    assert (actual.get_unmerged_keys() == ['WS_ORGANIZATION', 'WS_WORKSPACE'])
    actual.show()
    ###
    actual = WorkspaceFolderTemplate(nv_list)
    assert (actual == '{}/Development/temp-org/temp-ws'.format(os.environ['HOME']))
    assert (actual.getName() == 'temp-ws')
    assert (actual.get_unmerged_keys()==[])
    assert (actual.has_unmerged_keys()==False)
    #actual.validate()
    actual.create()
    actual.open()
    actual.merge()
    actual.save()
    actual.show()
    actual.assertExists()

    print('---')
def mainProjectFolderTemplate(nv_list):
    print('mainProjectFolderTemplate')
    ###
    actual = GitProjectFolderTemplate(nv_list)
    assert (actual == '{}/Development/temp-org/temp-ws/py_test'.format(os.environ['HOME']))
    assert (actual.getName() == 'py_test')
    assert (actual.get_unmerged_keys()==[])
    assert (actual.has_unmerged_keys()==False)
    actual.create()
    actual.open()
    actual.merge()
    actual.save()
    actual.show()
    actual.validate()

    actual.assertExists()

    print('---')
def mainScriptsFolderTemplate(nv_list):
    print('ScriptsFolderTemplate')
    ###
    actual = ScriptsFolderTemplate(nv_list)
    assert (actual == '{}/Development/temp-org/temp-ws/py_test/scripts'.format(os.environ['HOME']))
    assert (actual.getName() == 'scripts')
    assert (actual.get_unmerged_keys() == [])
    assert (actual.has_unmerged_keys() == False)
    actual.create()

    #actual.open()
    #actual.merge()
    #actual.save()
    actual.show()
    actual.validate()

    actual.assertExists()

    print('---')


def main():
    ##* Executes sample code
    import os
    from datetime import datetime

    print('A')
    nv_list = [{'name': '<<WS_ORGANIZATION>>', 'value': 'temp-org'},
               {'name': '<<WS_WORKSPACE>>', 'value': 'temp-ws'},
               {'name': '<<GH_PROJECT>>', 'value': 'py_test'},
               {'name': '<<GH_USER>>', 'value': 'wilfongjt'}
               ]
    mainFolderString(nv_list)
    mainWorkspaceFolderTemplate(nv_list)
    mainProjectFolderTemplate(nv_list)
    mainScriptsFolderTemplate(nv_list)


    exit(0)
    ddd = '{}/Development'.format(os.environ['HOME'])

    '''
    actual = ProjectString(os.getcwd())
    print('ProjectString')
    actual.show()

    nv_list = [{'name': '<<WS_ORGANIZATION>>', 'value': 'temp-org'},
               {'name': '<<WS_WORKSPACE>>', 'value': 'temp-ws'},
               {'name': '<<GH_PROJECT>>', 'value': 'temp-api'},
               {'name': '<<GH_USER>>', 'value': 'wilfongjt'}
               ]
    #actual = LbProjectFolder(nv_list)
    '''
    org_name = 'lyttlebit'
    ws_name = '00_std'
    prj_name = 'lb_lib'

    expected='{}/Development'.format(os.environ['HOME'])
    actual = LbDevelopmentFolder()
    assert(actual == expected)
    assert(actual.getName()=='Development')

    #dd = '{}/lyttlebit'.format(dd)
    expected='{}/Development/{}'.format(os.environ['HOME'],org_name)
    actual = LbOrganizationFolder()
    assert (actual == expected)
    assert (actual.getName() == org_name)

    #dd = '{}/00_std'.format(dd)
    expected='{}/Development/{}/{}'.format(os.environ['HOME'],org_name, ws_name)

    actual = LbWorkspaceFolder()
    assert (actual == expected)
    assert (actual.getName() == ws_name)

    #dd = '{}/lb_lib'.format(dd)
    expected='{}/Development/{}/{}/{}'.format(os.environ['HOME'],org_name, ws_name, prj_name)
    actual = LbProjectFolder()
    assert (actual == expected)
    assert (actual.getName() == prj_name)

    #dd = '{}/scripts'.format(dd)
    expected='{}/Development/{}/{}/{}/scripts'.format(os.environ['HOME'],org_name, ws_name, prj_name)
    actual = LbScriptsFolder()
    print('actual',actual)
    assert (actual == expected)
    assert (actual.getName() == 'scripts')

    #dd = '{}/source/template'.format(os.environ['HOME'])
    expected='{}/Development/{}/{}/{}/source/template/bash'.format(os.environ['HOME'],org_name, ws_name, prj_name)

    print('expected', expected)
    actual = LbTemplateFolder('bash')
    print('actual',actual)
    assert (actual == expected)
    assert (actual.getName() == 'bash')

    #print('dev-folder', actual)
    nv_list = [{'name': '<<WS_ORGANIZATION>>', 'value': 'temp-org'},
               {'name': '<<WS_WORKSPACE>>', 'value': 'temp-ws'},
               {'name': '<<GH_PROJECT>>', 'value': 'temp-api'},
               {'name': '<<GH_USER>>', 'value': 'wilfongjt'}
               ]
    actual = GitProjectFolderTemplate(nv_list).validate()
    print('GitProjectFolderTemplate', actual)
    actual = ScriptsFolderTemplate(nv_list).validate()
    print('ScriptsFolderTemplate', actual)

if __name__ == "__main__":
    # execute as script
    main()