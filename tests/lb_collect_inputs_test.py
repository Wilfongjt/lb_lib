import unittest
# from pylyttlebit.script_lb_rebase import PromptRebaseInputs
from dep.pylyttlebit.lb_constants import LbConstants
class CollectInputsTest(unittest.TestCase):
    def setUp(self) -> None:
        print('setup')

        self.stash = {}

        self.actual = PromptRebaseInputs(self.stash).setVerbose(True).setTest(True)

    def tearDown(self):
        print('teardown')
    def test_process(self):
        self.actual.process()

        # added as part of PromptRebaseInputs
        self.assertTrue('GH_MESSAGE' in self.actual.getStash()[LbConstants().PROMPTS_KEY])

        # post collection
        self.assertTrue(self.actual.getStash()[LbConstants().PROMPTS_KEY]['GH_USER'] == 'TBD')
        self.assertTrue(self.actual.getStash()[LbConstants().PROMPTS_KEY]['GH_MESSAGE'] == 'TBD')

        # post collection, path collected values will not be 'TBD'
        self.assertTrue(self.actual.getStash()[LbConstants().PROMPTS_KEY]['WS_ORGANIZATION'] != 'TBD')
        self.assertTrue(self.actual.getStash()[LbConstants().PROMPTS_KEY]['WS_WORKSPACE'] != 'TBD')
        self.assertTrue(self.actual.getStash()[LbConstants().PROMPTS_KEY]['GH_PROJECT'] != 'TBD')
        self.assertTrue(self.actual.getStash()[LbConstants().PROMPTS_KEY]['GH_BRANCH'] != 'TBD')



if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()