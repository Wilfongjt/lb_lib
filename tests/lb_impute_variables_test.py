import unittest
from pprint import pprint
# from pylyttlebit.script_lb_rebase import ImputeProjectVariables
from pylyttlebit.lb_constants import LbConstants
class ImputeVariablesTest(unittest.TestCase):
    def setUp(self) -> None:
        print('setup')
        self.stash = {
            'prompts': {
                LbConstants().WS_ORGANIZATION_KEY: 'TBD',
                LbConstants().WS_WORKSPACE_KEY: 'TBD',
                LbConstants().GH_USER_KEY: 'TBD',
                LbConstants().GH_PROJECT_KEY: 'TBD',
                LbConstants().GH_BRANCH_KEY: 'TBD',
                LbConstants().GH_MESSAGE_KEY: 'TBD'
            },
            'project': {}
        }
        self.actual = ImputeProjectVariables(self.stash).setVerbose(True).setTest(True)

    def tearDown(self):
        print('teardown')
    def test_process(self):
        self.actual.process()
        # added repo url as part of ImputeProjectVariables

        self.assertTrue(LbConstants().REPO_URL_KEY in self.actual.getStash()[LbConstants().PROJECT_KEY])
        self.assertTrue('https://github.com/TBD/TBD.git' == self.actual.getStash()[LbConstants().PROJECT_KEY][LbConstants().REPO_URL_KEY])


if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()