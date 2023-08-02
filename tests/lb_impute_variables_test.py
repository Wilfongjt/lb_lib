import unittest
from pylyttlebit.lb_rebase import CollectInputs
from pylyttlebit.lb_constants import LbConstants
class CollectInputsTest(unittest.TestCase):
    def setUp(self) -> None:
        print('setup')

        self.stash = {}

        self.actual = CollectInputs(self.stash).setVerbose(True).setTest(True)

    def tearDown(self):
        print('teardown')
    def test_process(self):
        self.actual.process()

        # added as part of CollectInputs
        self.assertTrue('GH_MESSAGE' in self.actual.getStash()[LbConstants().prompts_key])

        # post collection
        self.assertTrue(self.actual.getStash()[LbConstants().prompts_key]['GH_USER'] == 'TBD')
        self.assertTrue(self.actual.getStash()[LbConstants().prompts_key]['GH_MESSAGE'] == 'TBD')

        # post collection, path collected values will not be 'TBD'
        self.assertTrue(self.actual.getStash()[LbConstants().prompts_key]['WS_ORGANIZATION'] != 'TBD')
        self.assertTrue(self.actual.getStash()[LbConstants().prompts_key]['WS_WORKSPACE'] != 'TBD')
        self.assertTrue(self.actual.getStash()[LbConstants().prompts_key]['GH_PROJECT'] != 'TBD')
        self.assertTrue(self.actual.getStash()[LbConstants().prompts_key]['GH_BRANCH'] != 'TBD')



if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()