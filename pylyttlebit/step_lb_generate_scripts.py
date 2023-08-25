import os
from pprint import pprint
from pylyttlebit.lb_step import LbStep
from pylyttlebit.lb_constants import LbC
from lb_rebase_script import LbRebaseScript
from lb_project import LbProject

class LbGenerateScripts(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)

    def process(self):
        super().process()
        self.addStep('generate_rebase')
        print('process generate rebase script')

        pprint(self.getStash())
        script_folder = self.getStash(LbC().PROJECT_KEY)[LbC().SCRIPT_FOLDER_KEY]
        print('script_folder', script_folder)

        ##* Create script folder when cloned and not found

        if LbProject().isCloned(self.getStash(LbC().PROJECT_KEY)[LbC().PROJECT_FOLDER_KEY]):
            LbProject().create_folder(script_folder)

        ##* Generate rebase script in target project folder

        actual = LbRebaseScript().setFolder(script_folder).create().save()

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
    print('step_lb_generate_rebase_script')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

def main():
    # output into local scripts folder
    from pprint import pprint
    from pylyttlebit.lb_stash import LocalStash

    stash = LocalStash() # force output into local scripts folder
    actual = LbGenerateScripts(stash).setVerbose(False).process()
    #print('lb_stash', actual.getStash())
    #pprint(actual.getStash())

if __name__ == "__main__":
    # execute only if run as a script
    main()
    # unittest.main()