import unittest
from pylyttlebit.lb_rebase import InitializeEnvironment

class InitializeEnvironmentTest(unittest.TestCase):
    def setUp(self) -> None:
        print('setup')

        self.stash = {
            'project': {},
            'prompts': {
                'WS_ORGANIZATION': 'TBD',
                'WS_WORKSPACE': 'TBD',
                'GH_USER': 'TBD',
                'GH_PROJECT': 'TBD',
                'GH_BRANCH': 'TBD'
        }}
        self.actual = InitializeEnvironment(self.stash).setVerbose(True).setTest(True)
    def tearDown(self):
        print('teardown')
    def test_process(self):
        self.actual.process()
        self.assertTrue('failed' in self.actual.getStash())
        self.assertTrue('InitializeEnvironment' in self.actual.getStash()['failed'])
        print('stash', self.stash)
        self.assertTrue('WS_ORGANIZATION' in self.actual.getStash()['prompts'])
        self.assertTrue('WS_WORKSPACE' in self.actual.getStash()['prompts'])
        self.assertTrue('GH_USER' in self.actual.getStash()['prompts'])
        self.assertTrue('GH_PROJECT' in self.actual.getStash()['prompts'])
        self.assertTrue('GH_BRANCH' in self.actual.getStash()['prompts'])



if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()