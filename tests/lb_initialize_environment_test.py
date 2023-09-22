import unittest
from dep.pylyttlebit import InitializeEnvironment
from dep.pylyttlebit.lb_constants import LbConstants
class InitializeEnvironmentTest(unittest.TestCase):
    def setUp(self) -> None:
        print('setup')

        self.stash = {}

        self.actual = InitializeEnvironment(self.stash).setVerbose(True).setTest(True)
    def tearDown(self):
        print('teardown')
    def test_process(self):
        self.actual.process()

        # expect failure when initialized alone
        self.assertTrue('failed' in self.actual.getStash())
        self.assertTrue('LbInitializeEnvironment' in self.actual.getStash()['failed'])

        # injected keys
        self.assertTrue(LbConstants().PROJECT_KEY in self.actual.getStash())
        self.assertTrue(LbConstants().PROMPTS_KEY in self.actual.getStash())
        # injected prompt keys
        self.assertTrue('WS_ORGANIZATION' in self.actual.getStash()[LbConstants().PROMPTS_KEY])
        self.assertTrue('WS_WORKSPACE' in self.actual.getStash()[LbConstants().PROMPTS_KEY])
        self.assertTrue('GH_USER' in self.actual.getStash()[LbConstants().PROMPTS_KEY])
        self.assertTrue('GH_PROJECT' in self.actual.getStash()[LbConstants().PROMPTS_KEY])
        self.assertTrue('GH_BRANCH' in self.actual.getStash()[LbConstants().PROMPTS_KEY])
        self.assertTrue('GH_MESSAGE' not in self.actual.getStash()[LbConstants().PROMPTS_KEY])

        # set lb_stash prompts to TBD
        self.assertTrue(self.actual.getStash()[LbConstants().PROMPTS_KEY][LbConstants().WS_ORGANIZATION_KEY] == 'TBD')
        self.assertTrue(self.actual.getStash()[LbConstants().PROMPTS_KEY][LbConstants().WS_WORKSPACE_KEY] == 'TBD')
        self.assertTrue(self.actual.getStash()[LbConstants().PROMPTS_KEY][LbConstants().GH_USER_KEY] == 'TBD')
        self.assertTrue(self.actual.getStash()[LbConstants().PROMPTS_KEY][LbConstants().GH_PROJECT_KEY] == 'TBD')
        self.assertTrue(self.actual.getStash()[LbConstants().PROMPTS_KEY][LbConstants().GH_BRANCH_KEY] == 'TBD')




if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()