import os
from lb_lib.lb_text_file import LbTextFile

class LbDevEnv(LbTextFile):
    ## Create and load an .env file
    def hello_world(self):
        print("I am LbDevEnv!")
    #def __init__(self, folder=os.getcwd(),filename='.env'):
    def __init__(self):
        super().__init__()
        ##* by default: .env is file name
        ##* by default: put .env file in the calling function's folder
        self.folder = os.getcwd()
        self.filename = '.env'
        ##* Make environments easy to collect with prefixes ie, ['GH_','WS_'] ... [] has test
        self.prefixList = ['GH_','WS_']
    def get(self, name):
        #### Get line from list on request

        ##* return None when <name> is not found ... [x] has test
        rc = None
        for ln in self:
            if ln.startswith(name):
                ##* return ln when line starts with <name> is found ... [x] has test
                rc = ln
        return rc
    def getDefaults(self):
        #### Get .env defaults on request
        ##> Make a dictionary of name:TBD pairs

        self.addStep('defaults')

        ##* define initial state for environment ... [x] has test
        dflts = {
            'WS_ORGANIZATION': 'TBD',
            'WS_WORKSPACE': 'TBD',
            'GH_USER': 'TBD',
            'GH_PROJECT': 'TBD',
            'GH_BRANCH': 'TBD'
        }
        ##* outputs: dictionary
        return dflts
    def getDefaultsAsList(self):
        #### Get Environment Defaults as a List on request
        ##> Convert default dictionary to list, ie. {name:value,...} --> [name=value,...]
        defaults_list = []
        df = self.getDefaults()
        ##* Convert defaults dictionary to defaults list  ... [] has test
        for i in df:
            defaults_list.append('{}={}'.format(i, df[i]))
        ##* Output: list
        return defaults_list
    def getEnvironment(self):
        #### Collect environment variables on request
        ##> Makes a dictionary of name:value pairs from environment specific to library
        self.addStep('collect')
        ##1. Provide default env variables with default values
        cllct = self.getDefaults() # get defaults
        ##1. Merge env variable values from environment into defaults
        for e in os.environ: # overwrite defaults from environment
            for p in self.prefixList:
                if e.startswith(p):
                    cllct[e] = os.environ[e]
        ##1. Output dictionary of library specific Environment Variables ... [x] has test
        return cllct
    def load(self, line_list):
        #### Load list of text on request
        ##> loads list of name=value pairs into environment
        self.addStep('load')
        ##* remove line's trailing EOL
        line_list = [ln.replace('\n','') for ln in line_list]
        for ln in line_list:
            ##* skip line when line starts with "#" ... [x] has test
            if not ln.startswith('#'): # may contain comments
                ln = ln.split('=')
                # put into environment
                ##* skip line when not name=value pattern ... [x] has test
                if len(ln) == 2:
                    ##* set name value pair ... tested in test_set
                    self.set(ln[0],ln[1])

        ##* returns LbDevEnv ... has test
        return self
    def open(self):
        #### Open .env on request
        ##> Open and load an .env file.
        self.addStep('open')
        ##* Initialize list/object when file not found ... [] has test
        if not self.file_exists():
            self.load(self.getDefaultsAsList())
            return self
        ##* Open when .env is found
        with open('{}/{}'.format(self.folder,self.filename)) as file:
            lines = file.readlines()
            ##* Read .env and load into environment ... [x] has test
            self.load(lines)

        ##* Remember to call Save() to commit to HD
        ##* returns LbDevEnv ... [x] has test
        return self
    def set(self, name, value):
        #### Set a name=value pair on request
        nv = '{}={}'.format(name,value)
        found = False
        i = 0
        for ln in self:
            ##* update name=value when "<name>=" in list ... [] has test
            if ln.startswith(name):
                self[i]=nv
                found = True
            i += 1

        ##* append name=value when "<name>=" is NOT in list ... [x] has test
        if not found:
            self.append(nv)

        ##* upsert os.environ ... [x] has test
        os.environ[name] = value

        ##* output LbDevEnv ... [x] has test
        return self
    def upsert(self, values):
        #### Upsert environment values on request
        ##> loads a dictionary of name:value pairs into environment
        self.addStep('upsert')
        ##* given a dictionary of variables put them into environment ... [x] has test
        for p in values:
            #os.environ[p] = values[p]
            self.set(p,values[p])
        return self


def main():
    from lb_lib.lb_doc_comments import LbDocComments
    print('lb_dev_env')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

if __name__ == "__main__":
    # execute as script
    main()
    # unittest.main()