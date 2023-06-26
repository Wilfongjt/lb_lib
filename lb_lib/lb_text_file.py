import os
from lb_lib.lb_recorder import LbRecorder

class LbTextFile(list, LbRecorder):
    ## Open and Save text file
    def hello_world(self):
        print("I am LbTextFile!")
    def __init__(self):
        LbRecorder.__init__(self)

        self.filename = None
        self.folder = None
    def getFilename(self):
        ##__Get filename on request__
        ##* returns filename
        return self.filename

    def setFilename(self, name):
        ##__Set Filename on request__
        self.filename = name
        ##* return self
        return self

    def getFolder(self):
        ## __Get folder name on request__
        ##* returns folder name
        return self.folder

    def setFolder(self, name):
        ## __Set folder name on request__
        self.folder= name
        ##* returns self
        return self

    def exists(self):
        ## __Confirm text file exists on request__
        ##* text file exists when folder and text file are found

        ##* fail when folder is not found
        if not self.folder_exists():
            self.addStep('not-folder')
            return False

        ##* fail when folder/file is not found
        if not self.file_exists():
            self.addStep('not-file')
            return False

        return True

    def load(self, line_list):
        ## __Load list of text on request__
        self.addStep('load')
        for ln in line_list:
            self.addStep('load')
            self.append(ln)
        ##* returns self
        return self

    def open(self):
        ## __Open text file on request__
        self.addStep('open')
        ##* fail when folder is not found
        if not self.folder_exists():
            self.addStep('not-folder')
            raise Exception('Folder not found')
            return self

        ##* fail when folder/file is not found
        if not self.file_exists():
            self.addStep('not-file')
            raise Exception('File not found')
            return self

        with open('{}/{}'.format(self.getFolder(),self.getFilename())) as file:
            lines = file.readlines()
            self.load(lines)

        ##* returns self
        return self
    def folder_exists(self):
        ##__Test folder's existence on request__
        if not self.getFolder():
            ##* folder does not exist when folder not defined
            return False
        if not os.path.isdir('{}'.format(self.getFolder())):
            ##* folder does not exist when folder is not found
            return False
        ##* returns bool
        return True
    def file_exists(self):
        ##__Test file's existance on request__
        if not self.getFilename():
            ##* file does not exist when file not defined
            return False
        if not os.path.isfile('{}/{}'.format(self.getFolder(), self.getFilename())):
            ##* file does not exist when file is not found
            return False
        ##* returns bool
        return True
    def save(self):
        self.addStep('save')
        ## __Save text file on request__
        ##* overwrite file when save
        with open('{}/{}'.format(self.folder, self.filename), 'w') as f:
            f.writelines(['{}\n'.format(ln) for ln in self])
        ##* returns self
        return self
    def saveAs(self, folder, filename):
        self.addStep('save-as')
        ## __Save text file with different name on request__
        ##* overwrite file when file exists

        with open('{}/{}'.format(folder, filename), 'w') as f:
            f.writelines(['{}\n'.format(ln) for ln in self])
        ##* returns self
        return self
    def delete(self):
        ## __Delete file on request__
        ##* delete when file exists
        self.addStep('delete')
        if self.exists():
            os.remove("{}/{}".format(self.getFolder(), self.getFilename()))
        ##* returns self
        return self

def main():
    from lb_doc_comments import LbDocComments
    lines = [
        'one',
        'two'
    ]
    folder = os.getcwd()

    filename = '{}.bak'.format(str(__file__).split('/')[-1])
    actual = LbTextFile()
    assert(actual == [])
    #try:
    #    assert (actual.open() == [])
    #except:
    #    print('ok')

    assert (actual.setFolder(folder) == [])
    assert (not actual.exists())
    assert (actual.getFolder() == folder)
    #assert (not actual.exists())
    assert (actual.setFilename(filename) == [])
    assert (actual.getFilename() == filename)
    #print('exi', actual.exists())
    #print('folder',folder)
    #print('filename',filename)
    #print('exists', actual.exists())
    assert (not actual.exists())
    assert (actual.load(lines) == ['one','two'])
    assert (actual.save() == ['one','two'])
    assert (actual.exists())
    assert (actual.open() != ['one','two'])
    assert (actual.delete())

    actual.preview()
    # write documentation in markdown file
    LbDocComments().setFolder(os.getcwd()).setFilename(str(__file__).split('/')[-1]).open().save()

if __name__ == "__main__":
    # execute as script
    main()