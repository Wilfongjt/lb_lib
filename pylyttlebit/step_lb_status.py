import os
from pprint import pprint
from pylyttlebit.lb_step import LbStep
from pylyttlebit.lb_constants import LbC

class LbStatus(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)

    def process(self):
        super().process()
        self.addStep('status')
        print('process Status')
        print('    * curr dir', os.getcwd())
        print('    * valid', self.getStash().isValid())
        for k in self.getStash():
            print('    * {}'.format(k))
            isD = True
            if type(self.getStash(k)) is list:
                isD = False
            for kk in self.getStash(k):
                if isD:
                    print('        * {}: {}'.format(kk.ljust(15), self.getStash(k)[kk]))
                else:
                    print('        * {}'.format(kk.ljust(15)))

        print('    * verbose',self.isVerbose())

        if self.isVerbose():
            pprint(self.getStash())

        # identify the project data

        self.addStep(self.formulate(self.getStash().getProject()))

        # record process steps

        self.getStash().setProcess(self.getSteps())

        print('')

        return self

def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('step_lb_status')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

def main():
    from pprint import pprint
    from pylyttlebit.lb_stash import LbStash

    stash = LbStash()
    actual = LbStatus(stash).setVerbose(False).process()
    #print('lb_stash', actual.getStash())
    #pprint(actual.getStash())

if __name__ == "__main__":
    # execute only if run as a script
    main()
    # unittest.main()