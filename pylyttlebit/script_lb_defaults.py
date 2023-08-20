
from pylyttlebit.lb_constants import LbConstants
class LbDefaults(dict):
    #### Default Environment Variables
    ##* Defaults for starting a environment file (.env)
    def __init__(self):

        self[LbConstants().WS_ORGANIZATION_KEY] = 'TBD'
        self[LbConstants().WS_WORKSPACE_KEY] = 'TBD'
        self[LbConstants().GH_USER_KEY] = 'TBD'
        self[LbConstants().GH_PROJECT_KEY] = 'TBD'
        self[LbConstants().GH_BRANCH_KEY] = 'TBD'

def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_exceptions')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()

def main():
    print('no main for lb_exceptions')
if __name__ == "__main__":
    # execute as script
    main()
    # unittest.main()