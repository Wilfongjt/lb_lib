from pprint import pprint
from pylyttlebit.lb_step import LbStep
from pylyttlebit.lb_constants import LbC
from pylyttlebit.lb_dev_env import LbDevEnv

class LbSaveEnvironment(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)
        self.filename = None
        self.folder = None

    def setFolder(self, folder):
        self.folder = folder
        return self

    def getFolder(self):
        return self.folder

    def setFilename(self, name):
        self.filename = name
        return self
    def getFilename(self):
        return self.filename

    def process(self):
        super().process()
        print('process SaveEnvironment')
        self.addStep('[save]')

        if not self.getStash().isValid():
            self.addStep('(failed)')
            #self.getStash(LbC().PROCESS_KEY).append(self.getSteps())
            ##* Dont save .env folder when lb_stash is invalid
            #return self
        else:
            prompts = self.getStash(LbC().PROMPTS_KEY)
            pprint(prompts)
            # env = LbDevEnv(memorize=False).setFilename(self.getFilename()).open().setDictionary(prompts).save()
            env = None
            ##* set prompts to TBD
            if self.getFolder() != None:
                ##* Save env to alternate location when folder is provided
                self.addStep('success-test')
                env = LbDevEnv(memorize=True)\
                        .setFolder(self.getFolder())\
                        .setFilename(self.getFilename())\
                        .setDictionary(prompts)\
                        .save()
            else:
                ##* Save env to default location when no folder is provided
                self.addStep('(success)')

                env = LbDevEnv(memorize=True)\
                        .setDictionary(prompts)\
                        .save()

        # print environment lines
        #for ln in env:
        #    print('    * {}'.format(ln))

        # identify the bin data

        self.addStep(self.formulate(self.getStash().getProject()))

        # record process steps

        self.getStash().setProcess(self.getSteps())

        print('')

        return self
def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('step_lb-save_environment')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

def main():
    from pprint import pprint
    from pylyttlebit.lb_stash import LbStash

    defaults = {'GH_BRANCH': 'TBD',
     'GH_PROJECT': 'TBD',
     'GH_USER': 'TBD',
     'WS_ORGANIZATION': 'TBD',
     'WS_WORKSPACE': 'TBD'}

    env = LbDevEnv(memorize=True).setFolder(LbC().TEMP_FOLDER).setFilename(LbC().TEMP_FILENAME).create(defaults).open()

    stash = LbStash()
    actual = LbSaveEnvironment(stash).setFolder(LbC().TEMP_FOLDER).setFilename(LbC().TEMP_FILENAME).process()
    #print('lb_stash', actual.getStash())
    pprint(actual.getStash())

if __name__ == "__main__":
    # execute only if run as a script
    main()
    # unittest.main()