import os
from pylyttlebit.lb_text_file import LbTextFile
from pylyttlebit.lb_project import LbProject
from pylyttlebit.lb_constants import LbConstants
from pylyttlebit.lb_util import LbUtil

'''
    + --> empty ---> + --> 
    + --> exists --> + --> load from file --> + --> 
    + --> empty ---> + --> load from defaults
    New
    Open
    Create
                
            No File
                (defaults) -> create -> (file) -> open -> (environment) -> save -> (file)
            File  
                (file) -> open -> (environment) -> save -> (file)
                                 (file) -> open -> (environment)      
            LbEnvironment
                    
                
'''
### Development Environment
class LbDevEnv(LbTextFile):
    ##### Create and load an ".env" file
    ##* always load env values from file
    ##* always save from memory
    def hello_world(self):
        print("I am LbDevEnv!")
    def __init__(self, memorize=True):
        super().__init__()

        ##* ".env" is file name, by default
        ##* put ".env" file in the calling function's folder by default
        self.folder = os.getcwd()
        self.filename = '.env'
        self.memorize=memorize # allow calls to 'set' to update os.environ


    def clear(self):
        ###### Clear environment variables on request
        ##> Remove script specific environment variables from memory
        self.addStep('clear')

        ##* remove envirionment variables from memory

        df = self.toDictionary()

        for k in df:
            if k in os.environ:
                os.environ.pop(k)

        ##* remove environment variables from list

        super().clear()

        return self

    def create(self, defaults):
        ###### Create env file on request

        if LbProject().file_exists(self.getFolder(),self.getFilename()):
            ##* skip create when env file exists
            return self

        ##* create file when file doesnt exist

        self.addStep('create')
        self.addStep('(defaults)')
        self.load(['{}={}'.format(k, defaults[k]) for k in defaults])
        self.addStep('(environment)', arrow='*')
        self.save()

        self.addStep('// (environment)')

        self.clear()
        return self

    def get(self, name):
        ##__Get line from list on request__

        ##* return None when <name> is not found ... [x] has test
        rc = None
        for ln in self:
            if ln.startswith(name):
                ##* return ln when line starts with <name> is found ... [x] has test
                rc = ln
        return rc


    '''
    def getEnvironmentAsList(self):

        # #__Get LbEnvironment LbDefaults as a List on request__
        # #> Convert default dictionary to list, ie. {name:value,...} --> [name=value,...]
        defaults_list = []
        #self.addStep('defaults')
        df = self.getEnvironment()
        # #* Convert defaults dictionary to defaults list  ... [] has test
        for i in df:
            defaults_list.append('{}={}'.format(i, df[i]))
        # #* Output: list
        return defaults_list
    '''

    def inMemory(self):
        ##__Put variable into memory on reques__
        rc = False
        df = self.toDictionary()
        ##* Convert defaults dictionary to defaults list  ...  [] has test
        for i in df:
            if i in os.environ:
                rc = True
                # print('{} found in memory'.format(i))
        return rc
    #def memorize(self):
    #    # #__put enviroment variable into os.environemt__
    #    for line in self:
    #        if '=' in line and '#' not in line:
    #            ln = line.strip().split('/')
    #            print('ln',ln)
    #            ##* update variable to os.environ when found in os.environ
    #            ##* add variable in os.environ when not found in os.environ
    #            #os.environ[name] = value
    #    return self
    def load(self, line_list):
        ##__Load list of text on request__
        ##> loads .env's name and value pairs into memory
        self.addStep('load')

        ##* remove line's trailing EOL
        line_list = [ln.replace('\n','') for ln in line_list]

        for ln in line_list:
            if '=' in ln and '#' not in ln:
                #print('load ln', ln)
                self.addStep('(environment)')
                ##* Lines containing an equal sign are environment values
                l = ln.strip().split('=')
                #print('load', l[0],l[1])
                ##* update existing values
                self.set(l[0], l[1])
            else:
                ##* any lines not containing an equal sign "=" are considered a comment
                self.append(ln)

        ##* returns LbDevEnv ... has test
        return self

    def open(self):
        print('folder', self.getFolder())
        print('file  ', self.getFilename())
        ##__Open .env on request__

        self.addStep('open')

        ##* Save env file when file not found and defaults are set
        print('exists',LbProject().file_exists(self.getFolder(),self.getFilename()))
        if not LbProject().file_exists(self.getFolder(),self.getFilename()):

            if len(self) > 0: # defaults are set
                self.addStep('(environment)')
                self.save()

        ##* Open .env from file when .env is found

        with open('{}/{}'.format(self.getFolder(), self.getFilename())) as file:
            self.addStep('(lines)')
            lines = file.readlines()
            print('lines', lines)
            ##* Load environment variables from .env when .env is found  ... [x] has test
            self.load(lines)
        #print('toDicgtionary', self.toDictionary())
        ##* Remember to call Save() to commit to HD
        ##* returns LbDevEnv ... [x] has test
        return self

    def set(self, name, value):
        ##__Set environment variable on request__
        ##* keep os.environ and list in sync
        nv = '{}={}'.format(name,value)
        found = False
        i = 0
        for ln in self:
            ##* update environment variable when variable in list

            if ln.startswith(name):
                self[i]=nv
                found = True
            i += 1

        ##* append variable when not in list

        if not found:
            self.append(nv)

        ##* update variable to os.environ when found in os.environ
        ##* add variable in os.environ when not found in os.environ
        if self.memorize:
            os.environ[name] = value

        ##* output LbDevEnv ... [x] has test
        return self

    def setDictionary(self, dictionary):
        ##__Set environment variables from dictionary on request__

        ##* skip setting environment variables when dictionary parameter is None

        if not dictionary:
            return self

        for k in dictionary:
            ##* set environment variable when found in dictionary parameter
            self.set(k, dictionary[k])
        return self

    def setList(self, line_list):
        ##__Set environment variables from list of file lines on request__
        ##* convience method that encapsulates load method
        self.load(line_list)
        return self

    def toDictionary(self):
        ##__Convert enviroment list to dictionary on request__
        ##* environment list and memory are always in-scync
        rc = {}

        # get expected from environment list
        for ln in self:
            if '#' not in ln and '=' in ln:
                l = ln.strip().split('=')
                rc[l[0]]=l[1]

        return rc

    '''
        def toDictionary(self):
        # #__Convert enviroment list to dictionary on request__
        rc = {}
        for ln in self:
            ln = ln.strip()
            # #* convert lines with equal sign to name:value pair
            if not ln.startswith('#') and '=' in ln:
                l = ln.strip().split('=')
                rc[l[0]]=l[1]
            # #* ignore lines not containing equal sign
        return rc
    '''
    '''
    def upsert(self, values):
        # #__Upsert environment values on request__
        # #> loads a dictionary of name:value pairs into environment
        self.addStep('upsert')
        # #* given a dictionary of variables put them into environment ... [x] has test
        for p in values:
            #os.environ[p] = values[p]
            self.set(p,values[p])
        return self
    '''
    #def save(self):
    #    #print('save', self.getFilename())
    #    #print('env', self.getEnvironment())
    #    self.load(self.getEnvironment())
    #    #print('list', self)
    #    super().save()
    #    return self

def main():
    from pprint import pprint
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_dev_env')
    #folder = '/'.join(str(__file__).split('/')[0:-1])
    #filename = str(__file__).split('/')[-1]
    #LbDocComments().setFolder(folder).setFilename(filename).open().save()

    lst = ['WS_ORGANIZATION=xyz',
            'WS_WORKSPACE=TBD',
            'GH_USER=TBD',
            'GH_PROJECT=TBD',
            'GH_BRANCH=TBD']
    #print('---C')


    print('---')

    # initialize with NO defaults

    actual = LbDevEnv()\
        .setFilename('0.env')

    assert(actual == [])
    assert (actual.toDictionary() == {})
    assert (actual.inMemory() == False)
    assert (not actual.get('A'))

    # initialize with New defaults

    actual = LbDevEnv()\
        .setFilename('0.env') \
        .set('A', 'a')
    assert(actual == ['A=a'])
    #print('actual.toDictionary()', actual.toDictionary())
    assert (actual.toDictionary() == {'A': 'a'})
    assert (actual.inMemory() == True)
    assert (actual.get('A')=='A=a')

    pprint(os.environ)

    # initialize with New defaults from dictionary

    actual = LbDevEnv() \
        .setFilename('0.env') \
        .setDictionary({'A': 'a', 'B': 'b'})

    assert (actual == ['A=a', 'B=b'])
    assert (actual.toDictionary() == {'A': 'a', 'B': 'b'})
    assert (actual.inMemory() == True)
    assert (actual.get('A')=='A=a')
    assert (actual.get('B')=='B=b')


    # initialize with New defaults from list

    actual = LbDevEnv() \
        .setFilename('0.env') \
        .setList(['A=a', 'B=b', '#a=b'])

    assert (actual == ['A=a', 'B=b', '#a=b'])
    assert (actual.inMemory() == True)

    # save

    actual = LbDevEnv() \
        .setFilename('0.env') \
        .setList(['A=a', 'B=b', '#a=b']) \
        .save()\
        .clear()\
        .open()
    assert (actual == ['A=a', 'B=b', '#a=b'])
    assert (actual.inMemory() == True)
    actual.delete()

    # initialize and clear

    actual = LbDevEnv() \
        .setFilename('0.env') \
        .setList(['A=a', 'B=b', '#a=b'])\
        .clear()

    assert (actual == [])
    assert (actual.inMemory() == False)

    # initialize with defaults
    defaults = {
            'C': 'TBD',
            'D': 'TBD'
        }

    actual = LbDevEnv() \
        .setFilename('_0.env') \
        .create(defaults) \
        .open() \
        .show()

    #print('actual', actual)
    assert (actual == ['C=TBD', 'D=TBD'])
    assert (actual.inMemory() == True)
    assert (actual.toDictionary() == {'C': 'TBD', 'D': 'TBD'})
    assert (actual.get('C') == 'C=TBD')
    assert (actual.get('D') == 'D=TBD')


    actual = LbDevEnv() \
        .setFilename('_0.env') \
        .open() \
        .show()

    #print('actual', actual)
    assert (actual == ['C=TBD', 'D=TBD'])
    assert (actual.inMemory() == True)
    assert (actual.toDictionary() == {'C': 'TBD', 'D': 'TBD'})
    assert (actual.get('C') == 'C=TBD')
    assert (actual.get('D') == 'D=TBD')

    actual = LbDevEnv() \
        .setFilename('_0.env') \
        .open() \
        .set('C', 'c')\
        .set('D', 'd')\
        .save()\
        .show()

    #print('actual', actual)
    assert (actual == ['C=c', 'D=d'])
    assert (actual.inMemory() == True)
    assert (actual.toDictionary() == {'C': 'c', 'D': 'd'})
    assert (actual.get('C') == 'C=c')
    assert (actual.get('D') == 'D=d')
    assert (actual.get('C') == 'C=c')

    actual = LbDevEnv() \
        .setFilename('_0.env') \
        .delete()\
        .show()

    print('---')
    pprint(os.environ)
def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_dev_env')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()


if __name__ == "__main__":
    # execute as script
    main()
    # unittest.main()