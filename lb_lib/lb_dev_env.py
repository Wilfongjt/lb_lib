import os
#from pprint import pprint
from lb_lib.lb_recorder import LbRecorder
class LbDevEnv(LbRecorder):
    ## Create and load an .env file
    def hello_world(self):
        print("I am LbDevEnv!")
    def __init__(self, folder=os.getcwd(),filename='.env'):
        super().__init__()
        ## by default: put .env in the calling function's folder
        self.folder = folder
        self.filename = filename
        self.prefixList = ['GH_','WS_']
        if not self.exists():
            ## Create .env file when .env not found
            if self.folder:
                self.save()
            else:
                print('LbDevEnv.__init__', self.collect())

        else:
            if self.isEmpty():
                ## Recreate .env when .env file is empty
                self.delete()
                self.save()
    def delete(self):
        ## Delete file on request
        if self.exists():
             # Delete when .env exists
            self.addStep('delete')
            os.remove("{}/{}".format(self.folder, self.filename))
        return self

    def isEmpty(self):
        ## Check for empty .env file on request
        with open('{}/{}'.format(self.folder,self.filename)) as file:
            lines = file.readlines()
            lines = [ln.strip('\n') for ln in lines if ln != '\n']

        if lines == []:
            ## .env is empty when when all lines in file are blank or EOL
            self.addStep('empty')
            return True

        self.addStep('!empty')
        return False

    def show(self):
        self.addStep('show')
        print('DevEnv:')
        print('* folder : ', self.folder)
        print('* file   : ', self.filename)

        print(self.getSteps())
        return self

    def upsert(self, values):
        # Upsert environment values on request

        self.addStep('upsert')

        for p in values:
            os.environ[p] = values[p]
        return self

    def getDefaults(self):
        ## Get .env defaults on request
        self.addStep('defaults')

        # define initial state for environment
        dflts = {
            'WS_ORGANIZATION': 'TBD',
            'WS_WORKSPACE': 'TBD',
            'GH_USER': 'TBD',
            'GH_PROJECT': 'TBD',
            'GH_BRANCH': 'TBD'
        }
        return dflts

    def exists(self):
        ## Confirm .env file exists on request
        ## .env file exists when .env file is found
        self.addStep('exists')

        return os.path.isfile('{}/{}'.format(self.folder, self.filename))

    def open(self):
        ## Open .env on request
        ## Open when .env is found
        self.addStep('open')
        if not self.folder:
            return self
        with open('{}/{}'.format(self.folder,self.filename)) as file:
            lines = file.readlines()
            #print('lines', len(lines), lines)
            for ln in lines:
                if not ln.startswith('#'):
                    ln = ln.split('=')
                    # put into environment
                    if len(ln) == 2:
                        ## Load .env variable when "<name>=<value>" pattern found in .env
                        os.environ[ln[0]] = ln[1].strip('\n')

        return self

    def save(self):
        self.addStep('save')
        ## Save .env on request
        ## Get fresh values from environment when found
        ## Provide default .env file when .env NF
        ## Collect param-values from environment when .env is found
        # Convert json to lines
        # write lines to .env file
        # return self

        env = self.collect()  # get current env-vars or defaults
        # should have all the file values at this point
        #print('save 2')
        #pprint(env)
        # convert json to lines
        lines = []
        for e in env:
            ln = '{}={}'.format(e,env[e])
            lines.append(ln)
            #print('env ln', ln)

        with open('{}/{}'.format(self.folder, self.filename), 'w') as f:
            f.writelines(['{}\n'.format(ln) for ln in lines])

        return self

    def collect(self):
        ## Collect environment variables on request
        ## Collect environment variables from memory when env-name starts with "GH" or "WS"
        ## Provide default .env variable value when expected variable are not found in environment

        self.addStep('collect')
        cllct = self.getDefaults() # get defaults

        for e in os.environ: # overwrite defaults from environment
            for p in self.prefixList:
                if e.startswith(p):
                    cllct[e] = os.environ[e]

        return cllct

def main():
    #from doc_comments import DocComments
    #print(os.getcwd(), __file__)

    #print(DocComments(os.getcwd(), os.path.basename(__file__).split('/')[-1]).toMarkdown())
    #srcFolder = os.getcwd()
    #print('srcFolder')
    #dstFolder = '{}/temp'.format(srcFolder)
    actual = LbDevEnv(folder=None,filename='.env').show()
    #actual.show()
    assert ( actual)
    #assert ( actual.exists())

    assert ( actual.open())
    #assert ( actual.collect() != {})

    #actual.show()
    #print('B actual.collect ', actual.collect())


if __name__ == "__main__":
    # execute as script
    main()