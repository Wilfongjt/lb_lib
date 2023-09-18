import os


class Util():
    def assertTrue(self, expr):
        assert (expr==True)
        return self
    def assertFalse(self, expr):
        assert (expr==False)
        return self
    def get_input(self, msg, default, hardstop=True):
        #### Prompt user for input
        rc = '{} [{}] : '.format(msg, default)
        rc = input(rc)
        if not rc:
            rc = default
        ##* hard stop when user types 'n','N','x','X','q' or 'Q'
        if rc in ['n','N','x','X','q','Q','TBD']:
            if hardstop:
                print('stopping...Stopped')
                exit(0)
        ##* return str
        return rc
    def folder_exists(self, folder):
        #### Test if a given folder exists on request
        ##* folder exists when found on drive ... [x] has test
        exists = os.path.isdir('{}'.format(folder))
        ##* returns bool ... [x] has test
        return exists

    def file_exists(self, folder, filename):
        #### Test if a given folder and file exist on request

        ##* file exists when folder exists and file exists ... [x] has test
        exists = os.path.isfile('{}/{}'.format(folder, filename))

        ##* return bool ... [x] has test
        return exists

def main():
    actual=Util()

    #actual.get_input()
    this_folder_name='/'.join(str(__file__).split('/')[0:-1])
    this_file_name=str(__file__).split('/')[-1]

    # files and folders
    assert (actual.folder_exists(this_folder_name) == True)
    assert (actual.folder_exists('{}xxx'.format(this_folder_name)) == False)

    assert (actual.file_exists(this_folder_name, this_file_name) == True)
    assert (actual.file_exists(this_folder_name, '{}.xxx'.format(this_file_name)) == False)

    # get Inputs
    assert (actual.get_input('hi','default') == 'default')
    assert (actual.get_input('enter abc','default') == 'abc')

    #assert (actual.get_input('hi','TBD') == 'TBD')


if __name__ == "__main__":
    # execute as script
    main()