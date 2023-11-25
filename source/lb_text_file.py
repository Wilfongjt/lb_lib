import os
import warnings
from source.lb_recorder import LbRecorder
from source.lb_exceptions import BadFileNameException, BadFolderNameException, FolderNotFoundException
from source.lb_exceptions import FileNotFoundException,UninitializedContextException
from source.lb_folders import LbProjectFolder
from source.lb_util import LbUtil

class LbTextFile(list, LbRecorder):
    ## Open, Load and Save text file

    def __init__(self):
        LbRecorder.__init__(self)
        self.filename = None
        self.folder = None
        self.visible=True

    def hello_world(self):
        print("I am LbTextFile!")

    def is_show(self):
        return self.visible

    def set_show(self, tf):
        if tf:
            self.addStep('show')
        self.visible = tf
        return self

    def create(self, defaults):
        ###### Create env file on request

        if LbUtil().file_exists(self.getFolder(),self.getFilename()):
            ##* skip create when env file exists
            return self

        ##* create file when file doesnt exist

        self.addStep('create')
        self.addStep('(defaults)')
        #self.load(['{}={}'.format(k, defaults[k]) for k in defaults])
        self.addStep('(environment)', arrow='*')
        self.save()

        self.addStep('// (environment)')

        self.clear()
        return self

    def getStartText(self):
        rc = '''
        
        '''
        return rc
    def getFolder(self):
        ## __Get folder name on request__
        ##* returns folder name ... [x] has test
        return self.folder

    def setFolder(self, name, create=False):
        ## __Set folder name on request__
        self.folder= name
        ##* returns self ... [x] has test
        if create:
            LbUtil().create_folder(name)
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

    '''
    def folder_exists(self):
        ##__Test folder's existance on request__
        if not self.getFolder():
            ##* folder does not exist when folder is None ... [x] has test
            return False
        if not LbUtil().folder_exists(self.getFolder()):
            ##* folder does not exist when folder is not None ... [x] has test
            return False

        #if not os.path.isdir(self.getFolder()):
        #    ##* folder does not exist when folder is not None ... [x] has test
        #    return False

        ##* true when folder is found ... [x] has test
        return True

    def file_exists(self):
        ##__Test file's existance on request__
        if not self.getFilename():
            ##* file does not exist when filename is None ... [x] has test
            return False

        if not LbUtil().
        if not os.path.isfile('{}/{}'.format(self.getFolder(), self.getFilename())):
            ##* file does not exist when filename is not None ... [x] has test
            return False
        ##* file exists when folder and filename is not None and file is found ... [x] has test
        return True
    '''
    '''
    def exists(self):
        #print('  exists 1')
        ## __Confirm text file exists on request__

        ##* not exist when folder is not found ... [x] has test
        #if not self.folder_ exists():
        #print('** folder_exists', LbUtil().folder_exists(self.getFolder()))
        if LbUtil().folder_exists(self.getFolder()):
            self.addStep('not-folder')
            return False
        print('  exists 2')
        ##* not exist when folder/file is not found ... [x] has test
        #if not self.file_ exists():
        print('  exists 3 file {}/{}'.format(self.getFolder(),self.getFilename()))
        print('  exists 3.1 find filename {}/{}'.format(self.getFolder(),self.getFilename()))
        print('  exists 4 file_exists', LbUtil().file_exists(self.getFolder(), self.getFilename()))

        exists = os.path.isfile('{}/{}'.format(self.getFolder(), self.getFilename()))
        print('exits 5a exists', exists)

        exists = os.path.isfile(__file__)
        print('exits 5b exists', exists)

        fl = '/'.join(str(__file__).split('/')[0:-1])
        fi = str(__file__).split('/')[-1]
        assert(fl == self.getFolder())
        print('exits 5c', fl)

        exists = os.path.isfile('{}/{}'.format(fl, fi))

        print('exits 5d exists', exists)

        if not LbUtil().file_exists(self.getFolder(), self.getFilename()):
            self.addStep('not-file')
            return False
        print('  exists out')
        ##* text file exists when folder and text file are found ... [x] has test
        return True
    '''
    def exists(self):
        return LbUtil().file_exists(self.getFolder(),self.getFilename())

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
        #print('LbTextFile validate', self.getFolder())
        if not LbUtil().folder_exists(self.getFolder()):
            #raise FolderNotFoundException('Folder not found {} {}'.format(self.getClassName(),self.getFolder()))
            #warnings.warn('Warning Message: 4')
            print('Warning: !!! Target folder does not exist {}'.format(self.getFolder()))
        ##* throw BadFileNameException when filename is None ... [x] has test
        if self.getFilename() == None:
            raise BadFileNameException('Bad file name {}'.format(self.getFilename()))

        return self

    def open(self):
        ## __Open text file on request__
        self.addStep('open')
        #self.validate()
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
            self.addStep('(file)')
        ##* returns LbTextFile ... [x] has test
        return self

    def saveAs(self, folder, filename):
        ## __Save text file with different name on request__

        self.addStep('save-as')
        ##* return the new LbTextFile ... [x] has test
        return LbTextFile().setFolder(folder).setFilename(filename).load(self).save()
    '''
    def show(self, terminalMsg=None):
        ##__Show Steps on request__
        if terminalMsg:
            ##* Show preview of file
            print('    {}: {} {}'.format(self, terminalMsg, self.getClassName()))
            print('    ', self.getSteps())
        else:
            print('    {}: {}'.format(self, self.getClassName()))
            print('    ', self.getSteps())
        return self
    '''

    def show(self):
        if not self.is_show():
            return self
        print(self.getClassName())
        print('  target-filename  :', self.getFilename())
        print('  target-foldername:', (str(self.getFolder())))
        print('  source           :', (LbProjectFolder()))
        print('  steps            :')
        print('                   :', (self.getSteps()))
        print('  actual           :')
        print('                    ', (str(self)))

        return self

    def delete(self):
        ## __Delete file on request__
        ##* delete when file exists ... [x] has test
        self.addStep('delete')
        ##* clear list ... [x] has test
        self.clear()  # clear list
        ##* remove file for drive when file exists ... [] test
        LbUtil().delete_file(self.getFolder(),self.getFilename())
        #if self.exists():
        #    ##* remove file for drive when file exists ... [] test
        #    os.remove("{}/{}".format(self.getFolder(), self.getFilename()))
        ##* returns empty LbTextFile ... [x] has test
        return self

    def isEmpty(self):
        ##__Check for empty file on request__
        ##* empty file when file doesnt exist ... [x] has test
        is_empty = LbUtil().is_empty(self.getFolder(), self.getFilename())

        ##* returns bool ... [ ] has test
        return is_empty

    def toString(self):
        return '\n'.join(self)


def main():

    actual = LbTextFile()
    actual.setFolder(os.getcwd())
    actual.setFilename('lb_text_file.py')
    actual.validate()
    actual.open()
    actual.show()


def main_document():
    from dep.pylyttlebit import LbDocComments
    print('lb_text_file')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()


if __name__ == "__main__":
    # execute as script
    main()
