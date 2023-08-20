from pprint import pprint
from pylyttlebit.lb_step import LbStep
from pylyttlebit.lb_folders import LbFolders
from pylyttlebit.lb_constants import LbConstants, LbC
from pylyttlebit.lb_dev_env import LbDevEnv
from pylyttlebit.script_lb_defaults import LbDefaults
class LbInitializeEnvironment(LbStep):
    #### Initialize LbEnvironment

    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)
        self.filename= None
        self.foldername = None
    def setFolder(self, folder):
        self.foldername = folder
        return self
    def getFolder(self):
        return self.foldername
    def setFilename(self, name):
        self.filename = name
        return self
    def getFilename(self):
        return self.filename

    def process(self):
        super().process()

        print('LbInitializeEnvironment ')
        self.addStep('[initialize]')
        ##* Open and/or create  enviroment file When found in \<SOURCE> folder

        ##* Ensure git.rebase is running from the scripts folder, ie current folder ends with "scripts"

        ##* create the ~/Temp folder

        LbFolders().createTempFolder()

        print('dev    ', LbFolders().getDevelopmentFolder())
        print('org    ', LbFolders().getOrganizationFolder())
        print('ws     ', LbFolders().getWorkspaceFolder())
        print('prj    ', LbFolders().getProjectFolder())
        print('script ', LbFolders().getScriptsFolder())
        print('library', LbFolders().getLibraryFolder())
        print('temp   ', LbFolders().getTempFolder())

        env = None
        ##* set prompts to TBD
        if self.getFolder() != None:
            env = LbDevEnv(memorize=True).setFolder(self.getFolder()).setFilename(self.getFilename()).create(LbDefaults()).open()
        else:
            env = LbDevEnv(memorize=True).create(LbDefaults()).open()

        self.getStash().setPrompts(env.toDictionary())

        ##* echo lb_stash when verbose is true
        if self.isVerbose():
            print('verbose LbStash', self.getClassName())
            pprint(self.getStash())

        # validate changes

        #self.getStash().validate()

        #if self.getStash().isValid():
        #    self.addStep('(valid)')
        #else:
        #    self.addStep('(invalid)')

        # identify lb_stash data

        self.addStep(self.formulate(self.getStash(),title='lb_stash'))

        # record process steps

        self.getStash().setProcess(self.getSteps())

        print('')
        return self

def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('step_lb_initialize_environment')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

def main():
    print('no main for lb_exceptions')
if __name__ == "__main__":
    # execute as script
    main()
    # unittest.main()
def main():
    from pylyttlebit.lb_stash import LbStash
    stash = LbStash()
    actual = LbInitializeEnvironment(stash).setFolder(LbC().TEMP_FOLDER).setFilename(LbC().TEMP_FILENAME).process()
    print('lb_stash', actual.getStash())
    pprint(actual.getStash())

if __name__ == "__main__":
    # execute only if run as a script
    main()
    # unittest.main()