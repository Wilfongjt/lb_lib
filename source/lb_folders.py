import os

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
    def getName(self):
        ##* Return the Folder Type Name
        rc = self.split('/')
        rc = rc[-1]
        return rc

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
        f_str = f_str[0:f_str.index('Development') + offset]
        f_str = '/'.join(f_str)
        instance = super().__new__(cls, f_str)
        return instance

class LbScriptsFolder(FolderString):
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

def main():
    ##* Executes sample code
    import os
    from datetime import datetime

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
if __name__ == "__main__":
    # execute as script
    main()