import os

import lb_lib.lb_exceptions
from lb_lib.lb_recorder import LbRecorder
from lb_lib.lb_exceptions import BadFileNameException, BadFolderNameException, FileNotFoundException, FolderNotFoundException
from lb_lib.lb_util import LbUtil
class LbTextFile(list, LbRecorder):
    ## Open, Load and Save text file
    def hello_world(self):
        print("I am LbTextFile!")
    def __init__(self):
        LbRecorder.__init__(self)

        self.filename = None
        self.folder = None
    def getFolder(self):
        ## __Get folder name on request__
        ##* returns folder name ... [x] has test
        return self.folder
    def setFolder(self, name):
        ## __Set folder name on request__
        self.folder= name
        ##* returns self ... [x] has test
        return self

    def getFilename(self):
        ##__Get filename on request__
        ##* returns filename  ... [x] has test
        return self.filename
    def setFilename(self, name):
        ##__Set Filename on request__
        self.filename = name
        ##* return self ... [x] has test
        return self

    def folder_exists(self):
        ##__Test folder's existance on request__
        if not self.getFolder():
            ##* folder does not exist when folder not defined ... [x] has test
            return False
        if not os.path.isdir(self.getFolder()):
            ##* folder does not exist when folder is not found ... [x] has test
            return False
        ##* true when folder is found ... [x] has test
        return True
    def file_exists(self):
        ##__Test file's existance on request__
        if not self.getFilename():
            ##* file does not exist when file not defined ... [x] has test
            return False
        if not os.path.isfile('{}/{}'.format(self.getFolder(), self.getFilename())):
            ##* file does not exist when file is not found ... [x] has test
            return False
        ##* true when folder and file are found ... [x] has test
        return True
    def exists(self):
        ## __Confirm text file exists on request__
        ##* text file exists when folder and text file are found

        ##* fail when folder is not found ... [x] has test
        if not self.folder_exists():
            self.addStep('not-folder')
            return False

        ##* fail when folder/file is not found ... [x] has test
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
        ##* returns self ... [x] has test
        return self

    def validate(self):
        ##__Validate file attributes on request__
        ##* throw BadFolderNameException when folder is None ... [x] has test
        if not self.getFolder():
            raise BadFolderNameException('Bad folder name {}'.format(self.getFolder()))

        ##* throw FolderNotFoundException when folder doesnt exist ... [x] has test
        if not self.folder_exists():
            raise FolderNotFoundException('Folder not found {}'.format(self.getFolder()))

        ##* throw BadFileNameException when filename is None ... [x] has test
        if self.getFilename() == None:
            raise BadFileNameException('Bad file name {}'.format(self.getFilename()))

        return self

    def open(self):
        ## __Open text file on request__
        self.addStep('open')
        ##* fail when folder does not exist ... [x] has test
        if not self.folder_exists():
            self.addStep('not-folder')
            raise FolderNotFoundException('Folder not found {}'.format(self.getFolder()))

        ##* fail when file does not exist ... [x] has test
        if not self.file_exists():
            self.addStep('not-file')
            raise FileNotFoundException('File not found {}'.format(self.getFilename()))

        with open('{}/{}'.format(self.getFolder(),self.getFilename())) as file:
            lines = file.readlines()
            ##* load lines from file when available
            self.load(lines)

        ##* returns LbTextFile
        return self

    def save(self):
        self.addStep('save')
        ## __Save text file on request__
        ##* validate attributes
        ##* create new file when file doesnt exist ... [x] has test
        ##* overwrite file when file exists ... [x] has test
        self.validate()
        with open('{}/{}'.format(self.folder, self.filename), 'w') as f:
            f.writelines(['{}\n'.format(ln) for ln in self])
        ##* returns LbTextFile ... [x] has test
        return self
    def saveAs(self, folder, filename):
        ## __Save text file with different name on request__

        self.addStep('save-as')
        ##* return the new LbTextFile ... [x] has test
        return LbTextFile().setFolder(folder).setFilename(filename).load(self).save()

    def delete(self):
        ## __Delete file on request__
        ##* delete when file exists ... [ ] has test
        self.addStep('delete')
        ##* clear list ... [] test
        self.clear()  # clear list
        if self.exists():
            ##* remove file for drive when file exists ... [] test
            os.remove("{}/{}".format(self.getFolder(), self.getFilename()))
        ##* returns empty LbTextFile ... [x] has test
        return self

    def isEmpty(self):
        if not self.exists():
            return True
        ##__Check for empty file on request__
        if os.stat("{}/{}".format(self.getFolder(),self.getFilename())).st_size == 0:
            ##* file is empty when all lines in file are blank or EOL ... [ ] has test
            self.addStep('empty')
            return True

        self.addStep('!empty')
        ##* returns bool ... [ ] has test
        return False


def main():
    from lb_doc_comments import LbDocComments
    print('lb_text_file')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

if __name__ == "__main__":
    # execute as script
    main()
