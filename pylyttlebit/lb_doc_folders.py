import os
from pylyttlebit.lb_text_file import LbTextFile
from pylyttlebit.lb_exceptions import FolderNotFoundException,BadFolderNameException
class LbDocFolders(LbTextFile):
    ## Given a folder, generate a text graphic of folders and files

    def hello_world(self):
        print("I am LbDocFolders!")
    def __init__(self):
        super().__init__()
        self.folder = None
        self.title = 'Folders'
        self.ignore_files = ['.DS_Store', '.gitignore']
        self.ignore_folders = ['.git', 'temp', '.idea', '__pycache__']

    def getLineList(self):
        #### Get Line List
        ##* make list of folders and files
        line_list = []

        line_list.append('```')
        offset = len(self.getFolder().split('/')) - 1

        for folder, dirs, files in os.walk(self.getFolder()):
            path = folder.split(os.sep)
            padding = (len(path) - offset) * '   '
            ##* ignore unnessessary folders when found ... no test
            if not self.ignore(folder):
                ##* add folders when found ... [] has test
                line_list.append('{}+ {}'.format(padding, os.path.basename(folder)))
                for file in files:
                    ##* add files when found ... [] has test
                    padding = (len(path) - offset) * '   '
                    if file not in self.ignore_files:
                        line_list.append('{}   - {}'.format(padding, file))
        line_list.append('```')
        ##* return list
        return line_list

    def setTitle(self, title):
        #### Set Title on request
        self.title = title
        ##* return LbDocFolders ... no test
        return self

    def getTitle(self):
        #### Get Title on request
        ##* return title/str  ... no test
        return self.title

    def ignore(self, folder):
        #### Test if folder should be ignored on request
        ##* dont ignore when not in ignore list ... [] test
        rc = False
        foldernames = folder.split('/')
        for skip in self.ignore_folders:
            if skip in foldernames:
                ##* ignore when folder in ignore list ... [x] has test
                rc = True
        ##* return bool ... [x] has test
        return rc

    def save(self):
        #### Dont save
        return self

    def validate(self):
        ##__Validate folder attributes on request__
        ##* throw BadFolderNameException when folder is None ... [x] has test
        if not self.getFolder():
            raise BadFolderNameException('Bad folder name {}'.format(self.getFolder()))

        ##* throw FolderNotFoundException when folder doesnt exist ... [x] has test
        if not self.folder_exists():
            raise FolderNotFoundException('Folder not found {}'.format(self.getFolder()))

        return self

def main():
    from pprint import pprint
    from pylyttlebit.lb_doc_comments import LbDocComments
    #from lib.doc_comments import DocComments

    #print(DocComments(os.getcwd(), 'doc_folders.py').toMarkdown())
    actual = LbDocFolders() #os.getcwd(), title='Example')
    # actual = DocFolders('{}/lib'.format(os.getcwd()))
    assert (actual==[])
    assert (actual.setFolder(os.getcwd())==[])
    assert (actual.open() != [])
    #pprint(actual)


    # write documentation in markdown file
    LbDocComments().setFolder(os.getcwd()).setFilename(str(__file__).split('/')[-1]).open().save()


def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_doc_folders')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()


if __name__ == "__main__":
    # execute as script
    main()