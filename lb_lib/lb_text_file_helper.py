import os
import shutil
# from _functions import file_exists

class LbTextFileHelper():
    def __init__(self, srcFolder=os.getcwd(), srcName=None):
        self.folder = srcFolder
        self.filename = srcName

    def hello_world(self):
        print("I am LbTextFileHelper!")

    def exists(self):

        ## Test that filename exists in folder
        ## return when filename undefined
        if not self.filename:
            return False
        ## False when folder dosent exist
        exists = os.path.isdir('{}'.format(self.folder))
        if not exists:
            return False
        ## False when filename doesnt exist
        exists = os.path.isfile('{}/{}'.format(self.folder, self.filename))
        if not exists:
            return False
        return True

    def deleteWhenFound(self, delfolder=None, delfilename=None):
        ## delete file when file is found
        folder = self.folder
        filename = self.filename
        if delfilename:
            filename = delfilename
        if delfolder:
            folder = delfolder
        if delfolder == self.folder and delfilename == self.filename:
            raise Exception('Cannot delete source', delfolder, delfilename)
        # delete when exists
        if self.exists():
            os.remove("{}/{}".format(folder, filename))
        return self

    def copyTo(self, dstfolder, dstfilename, nocopy=False):
        ## copy source file to another location, or name, or both
        if dstfolder == self.folder and dstfilename == self.filename:
            ## fail when source folder and source filename equal destination folder and destination filename
            raise Exception('failed copy... source and destination are the same.')

        if nocopy:
            ## print to screen when nocopy == True
            print('copyTo ({}/{}) to ({}/{})'.format(self.folder, self.filename, dstfolder, dstfilename))
            return self

        #if self.exists(self.folder, self.filename):
        if self.exists():

            ## remove destination file when destination file exists
            self.deleteWhenFound(dstfolder, dstfilename)
            shutil.copy2('{}/{}'.format(self.folder, self.filename),
                         '{}/{}'.format(dstfolder, dstfilename))
        return self


def main():
    #from _functions import createFolder
    filename = 'lb_text_file_helper.py'
    srcfolder = os.getcwd()
    #dstfolder = '{}/temp'.format(os.getcwd())
    dstfolder = os.getcwd()
    #createFolder(dstfolder)
    print('cwd',os.getcwd())
    actual = LbTextFileHelper( srcfolder, filename)
    assert( actual )
    assert( actual.exists() )
    try:
        actual.copyTo(dstfolder, filename, nocopy=True)
    except:
        print('exception')
    #assert( LbTextFileHelper( dstfolder, filename).exists() )
    #assert( LbTextFileHelper( dstfolder, filename).deleteWhenFound() )
    #assert( not LbTextFileHelper( dstfolder, filename).exists() )

if __name__ == "__main__":
    # execute as script
    main()

