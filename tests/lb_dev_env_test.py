import unittest
import os
from lb_lib.lb_dev_env import LbDevEnv

class LbDevEnvTest(unittest.TestCase):
    def setUp(self):
        self.lb_dev_env = LbDevEnv()
        self.folder = os.getcwd()
        self.filename = '{}'.format('test.env')
        self.lb_dev_env.setFilename(self.filename)

    def test_defaults_as_list(self):
        self.assertTrue(type(self.lb_dev_env.getDefaultsAsList()) is list)

    def test_collect(self):
        result = self.lb_dev_env.collect()
        self.assertDictEqual(result, self.lb_dev_env.getDefaults())
    def test_load(self):
        result = self.lb_dev_env.load(['one=1', 'two=2'])
        self.assertEqual(result, ['one=1', 'two=2'])
    def test_open(self):
        result = self.lb_dev_env.open()
        self.assertNotEqual(result, [])
    def test_save(self):
        result = self.lb_dev_env.open()
        result = self.lb_dev_env.save()
        self.assertEqual(result, self.lb_dev_env.getDefaultsAsList())
        self.assertEqual(result, self.lb_dev_env)

    def test_delete(self):
        result = self.lb_dev_env.delete()
        self.assertEqual(result, [])
        self.assertFalse(self.lb_dev_env.exists())


if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()