from pprint import pprint
from pylyttlebit.lb_step import LbStep
from pylyttlebit.lb_constants import LbC
from pylyttlebit.lb_util import LbUtil
class LbCreateWorkspace(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.setStash(stash)
    def process(self):
        super().process()
        print('process CreateWorkspace')

        #### Create Workspace
        self.addStep('[create]')

        project_folder = self.getStash().getProject(LbC().PROJECT_FOLDER_KEY)
        workspace_folder = '/'.join(project_folder.split('/')[0:-1])
        if len(workspace_folder) == 0:
            workspace_folder = 'TBD'

        #self.getStash().validate()

        ##* Create Workspace folder When folder doesnt exist and parameters are valid

        if self.getStash().isValid():
            print('    * create workspace ', workspace_folder)
            self.addStep('(success)')
            LbUtil().create_folder(workspace_folder)
        else:
            ##* Dont create Workspace folder when lb_stash is invalid
            self.addStep('(failed)')

            print('    * create workspace failed({})'.format(workspace_folder))

        # identify the bin data

        self.addStep(self.formulate(self.getStash().getProject()))

        # record process steps

        self.getStash().setProcess(self.getSteps())

        print('')

        return self
def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('step_lb_create_workspace')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

def main():
    from pprint import pprint
    from pylyttlebit.lb_stash import LbStash

    stash = LbStash()
    actual = LbCreateWorkspace(stash).process()
    #print('lb_stash', actual.getStash())
    pprint(actual.getStash())

if __name__ == "__main__":
    # execute only if run as a script
    main()
    # unittest.main()