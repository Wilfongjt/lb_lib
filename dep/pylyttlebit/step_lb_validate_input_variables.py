from pprint import pprint
from dep.pylyttlebit.lb_step import LbStep
from dep.pylyttlebit.lb_constants import LbC
from dep.pylyttlebit.lb_project import LbProject

class LbValidateInputVariables(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.verbose = False
        self.setStash(stash)
    def process(self):
        super().process()
        print('process Validate Project')
        self.addStep('[validate]')

        ##* Validate PROJECT_KEY

        if LbC().PROJECT_KEY not in self.getStash(): # check for missing name
            self.getStash().setInvalid('unknown_key({})'.format(LbC().PROJECT_KEY))
            if self.isVerbose():
                print('verbose LbStash', self.getClassName())
                pprint(self.getStash())

        ##* Validate PROMPTS_KEY

        if LbC().PROMPTS_KEY not in self.getStash():  # check for missing name
            self.getStash().setInvalid('unknown_key({})'.format(LbC().PROMPTS_KEY))
            if self.isVerbose():
                print('verbose LbStash', self.getClassName())
                pprint(self.getStash())

        ##* Validate Inputs

        self.getStash().validate()

        # #* Invalid when Project folder is not found

        #folder = self.getStash().getProject()[LbC().PROJECT_FOLDER_KEY]
        #if not LbProject().folder_exists(folder): # check for bin folder
        #    self.getStash().setInvalid('unknown_folder {}'.format(folder))

        ##* Invalid when remote Project is not found
        repo_url = self.getStash().getProject('repo_url')
        if not LbProject().hasRemoteProject(repo_url):
            self.getStash().setInvalid('remote repo not found')

        if self.getStash().isValid():
            self.addStep('(valid)')
        else:
            pprint(self.getStash())
            self.addStep('(invalid)')

        # identify the lb_stash data

        self.addStep(self.formulate(self.getStash().getProject(), title='bin'))

        # reocord process steps

        self.getStash().setProcess(self.getSteps())

        print('')

        return self

def main_document():
    from dep.pylyttlebit.lb_doc_comments import LbDocComments
    print('step_lb_validate_inputs_variables')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

def main():
    from pprint import pprint
    from dep.pylyttlebit.lb_stash import LbStash

    stash = LbStash()
    actual = LbValidateInputVariables(stash).process()

    pprint(actual.getStash())

if __name__ == "__main__":
    # execute only if run as a script
    main()
    # unittest.main()