import os
class LbDocFolders(list):
    ## Given a folder, inventory the folder and subfolders including the file names.

    def hello_world(self):
        print("I am LbDocFolders!")
    def __init__(self, folder=None, title='Folders'):
        self.folder = folder
        self.title = title
        self.skip_files = ['.DS_Store','.gitignore']
        self.skip_folders = ['.git','temp','.idea', '__pycache__']
    def open(self):
        ##* Initialize list with folder and file names
        if not self.folder:
            return self

        offset = len(self.folder.split('/'))-1

        for folder, dirs, files in os.walk(self.folder):
            path = folder.split(os.sep)
            padding = (len(path)-offset) * '   '
            #print('folder', folder, self.skipFolder(folder))
            #print('basename', os.path.basename(folder))
            if not self.skipFolder(folder) :
                self.append('{}+ {}'.format(padding,os.path.basename(folder)))
                for file in files:
                    padding = (len(path) - offset) * '   '
                    if file not in self.skip_files:
                        self.append('{}   - {}'.format(padding, file))
        return self

    def skipFolder(self, folder):
        foldernames = folder.split('/')
        for skip in self.skip_folders:
            if skip in foldernames:
                return True
        return False

    def toMarkdown(self):
        ## Convert folders and file names to markdown on request
        return "## {}\n\n```\n{}\n```".format(self.title, '\n'.join(self))
def main():
    #from lib.doc_comments import DocComments

    #print(DocComments(os.getcwd(), 'doc_folders.py').toMarkdown())
    actual = LbDocFolders(os.getcwd(), title='Example')
    # actual = DocFolders('{}/lib'.format(os.getcwd()))
    assert (actual)
    #print(actual.toMarkdown())

if __name__ == "__main__":
    # execute as script
    main()