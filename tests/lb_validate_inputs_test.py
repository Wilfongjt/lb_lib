import unittest
#from pylyttlebit.script_lb_rebase import ValidateInputs
from dep.pylyttlebit.lb_constants import LbC
class ValidateInputsTest(unittest.TestCase):
    def setUp(self) -> None:
        print('setup')
        self.stash = {
            LbC().PROMPTS_KEY: {
                LbC().WS_ORGANIZATION_KEY: 'TBD',
                LbC().WS_WORKSPACE_KEY: 'TBD',
                LbC().GH_USER_KEY: 'TBD',
                LbC().GH_PROJECT_KEY: 'TBD',
                LbC().GH_BRANCH_KEY: 'TBD',
                LbC().GH_MESSAGE_KEY: 'TBD'
            },
            LbC().PROJECT_KEY: {
                'repo_url': 'https://github.com/TBD/TBD.git'
            }
        }
        self.actual = ValidateInputs(self.stash).setVerbose(True).setTest(True)

    def tearDown(self):
        print('teardown')
    def test_process(self):

        self.actual.process()

        # top keys

        self.assertTrue(LbC().INVALID_KEY in self.actual.getStash())
        self.assertTrue(LbC().PROJECT_KEY in self.actual.getStash())
        self.assertTrue(LbC().PROMPTS_KEY in self.actual.getStash())

        # should all fail
        print('list',self.actual.getStash(LbC().INVALID_KEY))
        self.assertTrue(LbC().WS_ORGANIZATION_KEY in self.actual.getStash(LbC().INVALID_KEY))
        self.assertTrue(LbC().WS_WORKSPACE_KEY in self.actual.getStash(LbC().INVALID_KEY))
        self.assertTrue(LbC().GH_USER_KEY in self.actual.getStash(LbC().INVALID_KEY))
        self.assertTrue(LbC().GH_PROJECT_KEY in self.actual.getStash(LbC().INVALID_KEY))
        self.assertTrue(LbC().GH_BRANCH_KEY in self.actual.getStash(LbC().INVALID_KEY))
        self.assertTrue(LbC().GH_MESSAGE_KEY in self.actual.getStash(LbC().INVALID_KEY))


if __name__ == "__main__":

    # execute only if run as a script
    unittest.main()