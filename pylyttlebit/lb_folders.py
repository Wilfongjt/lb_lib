import os

class LbFolders():
    def hello_world(self):
        print("I am LbFolders!")
        return self

    def getDevelopmentFolder(self):
        #### Get Development folder on request
        ##* return str
        return '{}/Development'.format(os.path.expanduser('~'))

    def getFolder(self, pos, subfolder=None):
        #### Get Folder on request
        ##* start with the current folder of the calling script
        rc = os.getcwd().split('/')
        idx = rc.index('Development')  # os.getcwd().split('/').index('Development')
        # pad with TBD
        while idx + pos > len(rc):
            rc.append('TBD')
        rc = rc[0:idx + pos]
        if subfolder:
            rc.append(subfolder)
        #print('folder {}'.format(pos), '/'.join(rc))
        ##* return str
        return '/'.join(rc)
    def getOrganizationFolder(self):
        #### Get Organization Folder on request
        ##* return str
        return self.getFolder(2)

    def getWorkspaceFolder(self):
        #### Get Workspace Folder on request
        ##* return str
        return self.getFolder(3)
    def getProjectFolder(self):
        #### Get Project Folder on request
        ##* return str
        return self.getFolder(4)
    def getToolsFolder(self):
        #### Get Tools Folder on request
        ##* return str
        return self.getFolder(4,'_tools')
    def getLibraryFolder(self):
        #### Get Library Folder on request
        ##* return str
        return self.getFolder(4,'pylyttlebit')
    def getScriptsFolder(self):
        #### Get Scripts Folder on request
        ##* return str
        return self.getFolder(4,'scripts')

def main():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_folders')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

    actual = LbFolders()
    assert (type(actual.getDevelopmentFolder()) is str)
    assert (actual.getDevelopmentFolder() != os.getcwd())

    assert (type(actual.getOrganizationFolder()) is str)
    assert (actual.getOrganizationFolder() != os.getcwd())

    assert (type(actual.getWorkspaceFolder()) is str)
    assert (actual.getWorkspaceFolder() != os.getcwd())

    assert (type(actual.getProjectFolder()) is str)
    assert (actual.getProjectFolder() != os.getcwd())

    assert (type(actual.getToolsFolder()) is str)
    assert (actual.getToolsFolder() != os.getcwd())
    print('library',actual.getLibraryFolder())
    print('cwd    ', os.getcwd())
    assert (type(actual.getLibraryFolder()) is str)
    assert (actual.getLibraryFolder() == os.getcwd()) # yes this is correct

    assert (type(actual.getScriptsFolder()) is str)
    assert (actual.getScriptsFolder() != os.getcwd())


def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_folders')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()


if __name__ == "__main__":
    # execute as script
    main()
    # unittest.main()