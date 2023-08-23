from pprint import pprint
from pylyttlebit.lb_step import LbStep
from pylyttlebit.lb_constants import LbC


class depLbValidatePromptInputs(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.verbose = False
        self.setStash(stash)

    def process(self):
        super().process()
        print('process Validate Prompts')

        ##* Validate PROMPTS_KEY

        if LbC().PROMPTS_KEY not in self.getStash():  # check for missing key
            self.getStash().setInvalid('unknown_key({})'.format(LbC().PROMPTS_KEY))
            if self.isVerbose():
                print('verbose LbStash', self.getClassName())
                pprint(self.getStash())
            #return self

        ##* Validate Prompts
        self.addStep('[validate]')
        self.getStash().validate()
        #self.getStash().validate(d=self.getStash().getPrompts())

        if self.getStash().isValid():
            self.addStep('(valid)')
        else:
            self.addStep('(invalid)')
            pprint(self.getStash())

        # identify the lb_stash data

        self.addStep(self.formulate(self.getStash().getPrompts(), title='prompts'))

        # reocord process steps

        self.getStash().setProcess(self.getSteps())

        print('')

        return self

def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('step_lb_validate_prompt_imputs')
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

    actual = LbValidatePromptInputs(LbStash()).process()
    print('lb_stash', actual.getStash())
    pprint(actual.getStash())

if __name__ == "__main__":
    # execute only if run as a script
    main()
    # unittest.main()