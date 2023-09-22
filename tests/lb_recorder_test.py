import unittest
from dep.pylyttlebit.lb_recorder import LbRecorder
class LbRecorderTest(unittest.TestCase):
    def setUp(self):
        self.actual = LbRecorder()

    def test_getSteps(self):
        self.actual = LbRecorder()

        result = self.actual.getSteps()
        self.assertEqual(result, '')

        self.actual.addStep('one')
        result = self.actual.getSteps()
        self.assertEqual(result, 'one')

        self.actual.addStep('two')
        result = self.actual.getSteps()
        self.assertEqual(result, 'one -> two')

    def test_preview(self):
        pass

if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()