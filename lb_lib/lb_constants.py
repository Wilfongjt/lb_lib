import os
class LbConstants():

    def __init__(self):

        ##* name a temp_folder in users home folder, eg "~/temp"
        self.temp_folder = '{}/temp'.format(os.path.expanduser('~'))
        ##* name a disposable_folder in temp folder, eg "~/temp/disposable"
        self.disposable_folder = '{}/disposable'.format(self.temp_folder)
        self.temp_filename = 'temp_file.txt.env'
        self.empty_filename = 'empty.txt.env'
def main():
    from lb_lib.lb_doc_comments import LbDocComments
    print('lb_constants')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()


if __name__ == "__main__":
    # execute as script
    main()