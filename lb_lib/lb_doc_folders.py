import os
from lb_lib.lb_text_file import LbTextFile
class LbDocFolders(LbTextFile):
    ## Given a folder, generate a list of folders and files

    def hello_world(self):
        print("I am LbDocFolders!")
    def __init__(self):
        super().__init__()
        self.folder = None
        self.title = 'Folders'
        self.ignore_files = ['.DS_Store', '.gitignore']
        self.ignore_folders = ['.git', 'temp', '.idea', '__pycache__']

    def setTitle(self, title):
        ##__Set Title on request__
        self.title = title
        ##* return self
        return self
    def getTitle(self):
        ##__Get Title on request__
        ##* return title
        return self.title
    def open(self):
        ## __Open folder on request__
        self.addStep('open')
        ##* fail when source folder is not found
        if not self.folder_exists():
            self.addStep('not-folder')
            raise Exception('Folder not found')
            return self

        #with open('{}/{}'.format(self.getFolder(),self.getFilename())) as file:
        #    lines = file.readlines()
        #    self.load(lines)
        self.append('```')
        offset = len(self.folder.split('/'))-1

        for folder, dirs, files in os.walk(self.folder):
            path = folder.split(os.sep)
            padding = (len(path)-offset) * '   '
            ##* skip unnessessary folders when found
            if not self.ignore(folder) :
                ##* add folders when found
                self.append('{}+ {}'.format(padding,os.path.basename(folder)))
                for file in files:
                    ##* add files when found
                    padding = (len(path) - offset) * '   '
                    if file not in self.ignore_files:
                        self.append('{}   - {}'.format(padding, file))
        self.append('```')
        ##* return self
        return self

    def ignore(self, folder):
        ##__Test if folder should be ignored on request__
        foldernames = folder.split('/')
        for skip in self.ignore_folders:
            if skip in foldernames:
                ##* ignore when folder in ignore list
                return True
        ##* return bool
        return False

    #def toMarkdown(self):
    #    ##__Convert folders and file names to markdown on request__
    #    return "## {}\n\n```\n{}\n```".format(self.title, '\n'.join(self))
def main():
    from pprint import pprint
    from lb_lib.lb_doc_comments import LbDocComments
    #from lib.doc_comments import DocComments

    #print(DocComments(os.getcwd(), 'doc_folders.py').toMarkdown())
    actual = LbDocFolders() #os.getcwd(), title='Example')
    # actual = DocFolders('{}/lib'.format(os.getcwd()))
    assert (actual==[])
    assert (actual.setFolder(os.getcwd())==[])
    assert (actual.open() != [])
    pprint(actual)


    # write documentation in markdown file
    LbDocComments().setFolder(os.getcwd()).setFilename(str(__file__).split('/')[-1]).open().save()

if __name__ == "__main__":
    # execute as script
    main()