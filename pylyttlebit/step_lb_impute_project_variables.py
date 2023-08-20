import os
from pprint import pprint
from pylyttlebit.lb_step import LbStep
from pylyttlebit.lb_constants import LbC

class LbImputeProjectVariables(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.verbose = False
        self.setStash(stash)
    def process(self):
        super().process()
        #### Impute Variables
        print('process ImputeProjectVariables')

        self.addStep('[impute]')

        ##* Impute REPO_URL_KEY

        key = LbC().REPO_URL_KEY
        val = LbC().REPO_URL_TEMPLATE.format(self.getStash().getPrompts(LbC().GH_USER_KEY),
                                             self.getStash().getPrompts(LbC().GH_PROJECT_KEY) )
        self.getStash().setProject(key, val)

        print('    * impute repo url', self.getStash().getProject(LbC().REPO_URL_KEY))
        if self.isVerbose():
            print('verbose LbStash', self.getClassName())
            pprint(self.getStash())

        ##* Impute Project Folder

        devfolder = '{}/Development'.format(os.path.expanduser('~'))
        folder = '{}/{}'.format(devfolder, self.getStash().getPrompts(LbC().WS_ORGANIZATION_KEY))
        folder = '{}/{}'.format(folder, self.getStash().getPrompts(LbC().WS_WORKSPACE_KEY))
        folder = '{}/{}'.format(folder, self.getStash().getPrompts(LbC().GH_PROJECT_KEY))

        print('    * impute project folder', folder)

        #if self.getStash().isValid():
        #    self.addStep('(success)')
        #else:
        #    self.addStep('(invalid)')

        self.getStash().setProject(LbC().PROJECT_FOLDER_KEY, folder)

        #self.addStep('impute')

        # validate

        #self.getStash().validate()

        # identify the project data

        self.addStep(self.formulate(self.getStash().getProject(), title='project'))

        # record process steps

        self.getStash().setProcess(self.getSteps())

        print('')

        return self

def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('step_lb_impute_project_variables')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

def main():
    from pylyttlebit.lb_stash import LbStash

    stash = LbStash()
    actual = LbImputeProjectVariables(stash).process()
    print('lb_stash', actual.getStash())
    pprint(actual.getStash())

if __name__ == "__main__":
    # execute only if run as a script
    main()
    # unittest.main()