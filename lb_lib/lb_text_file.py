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

    def getLineList(self):
        #### Get all lines in a text file
        line_list = []
        ##* open file and read text lines ... [x] has test
        with open('{}/{}'.format(self.getFolder(),self.getFilename())) as file:
            line_list = file.readlines()
            line_list = [ln.replace('\n','') for ln in line_list]
        ##* return lines from a file
        return line_list

    def folder_exists(self):
        ##__Test folder's existance on request__
        if not self.getFolder():
            ##* folder does not exist when folder is None ... [x] has test
            return False
        if not os.path.isdir(self.getFolder()):
            ##* folder does not exist when folder is not None ... [x] has test
            return False
        ##* true when folder is found ... [x] has test
        return True
    def file_exists(self):
        ##__Test file's existance on request__
        if not self.getFilename():
            ##* file does not exist when filename is None ... [x] has test
            return False
        if not os.path.isfile('{}/{}'.format(self.getFolder(), self.getFilename())):
            ##* file does not exist when filename is not None ... [x] has test
            return False
        ##* file exists when folder and filename is not None and file is found ... [x] has test
        return True
    def exists(self):
        ## __Confirm text file exists on request__

        ##* not exist when folder is not found ... [x] has test
        if not self.folder_exists():
            self.addStep('not-folder')
            return False

        ##* not exist when folder/file is not found ... [x] has test
        if not self.file_exists():
            self.addStep('not-file')
            return False

        ##* text file exists when folder and text file are found ... [x] has test
        return True

    def load(self, line_list):
        ## __Load list of text on request__
        self.addStep('load')
        ##* put lines into object list
        for ln in line_list:
            self.addStep('load')
            self.append(ln)
        ##* returns LbTextFile ... [x] has test
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
        self.validate()
        line_list = self.getLineList()
        ##* load lines from file when available
        self.load(line_list)
        ##* returns LbTextFile
        return self

    def save(self):
        self.addStep('save')
        ## __Save text file on request__
        ##> saves contents of list to a text file

        ##* validate attributes ... tested with validate()
        self.validate()

        ##* create file when file doesnt exist ... [x] has test
        ##* overwrite file when file exists ... [x] has test
        with open('{}/{}'.format(self.getFolder(), self.getFilename()), 'w') as f:
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
        ##* delete when file exists ... [x] has test
        self.addStep('delete')
        ##* clear list ... [x] has test
        self.clear()  # clear list
        if self.exists():
            ##* remove file for drive when file exists ... [] test
            os.remove("{}/{}".format(self.getFolder(), self.getFilename()))
        ##* returns empty LbTextFile ... [x] has test
        return self

    def isEmpty(self):
        ##__Check for empty file on request__
        ##* empty file when file doesnt exist ... [x] has test
        if not self.exists():
            return True

        if os.stat("{}/{}".format(self.getFolder(),self.getFilename())).st_size == 0:
            ##* file is empty when has no lines ... [ ] has test
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
