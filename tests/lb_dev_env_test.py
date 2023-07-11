import unittest
import os
from lb_lib.lb_dev_env import LbDevEnv
from lb_lib.lb_util import LbUtil
class LbDevEnvTest(unittest.TestCase):
    def setUp(self):
        self.actual = LbDevEnv()
        self.temp_folder = '/'.join(str(__file__).split('/')[0:-1])
        self.temp_folder = '{}/temp'.format(self.temp_folder)
        self.temp_filename = '{}'.format('test.env')
        self.actual.setFilename(self.temp_filename)
        LbUtil().create_folder(self.temp_folder)


    def tearDown(self):
        #print('tearDown')

        # remove all files in temp folder
        LbUtil().delete_folder_files(self.temp_folder, '*')
        # remove temp folder
        LbUtil().delete_folder(self.temp_folder)

    def test_get(self):
        ##* return None when <name> not found ... [x] has test
        result = self.actual.get('a')
        self.assertTrue(result == None)

        ##* return ln when line starts with <name> found ... [x] has test
        self.actual.append('a=a')
        result = self.actual.get('a')
        self.assertTrue(result == 'a=a')


    def test_getDefaults(self):
        result = self.actual.getDefaults()
        # output dictionary
        self.assertTrue(type(result) is dict)
        self.assertDictEqual(result, {
            'WS_ORGANIZATION': 'TBD',
            'WS_WORKSPACE': 'TBD',
            'GH_USER': 'TBD',
            'GH_PROJECT': 'TBD',
            'GH_BRANCH': 'TBD'
        })

    def test_defaults_as_list(self):
        result = self.actual.getDefaultsAsList()
        self.assertTrue(type(result) is list)

    def test_getEnvironment(self):
        result = self.actual.getEnvironment()
        self.assertDictEqual(result, self.actual.getDefaults())

    def test_load(self):
        #print('env', os.environ)
        # prove test keys not in environment
        self.assertFalse('one' in os.environ)
        self.assertFalse('two' in os.environ)

        result = self.actual.load(['one=1', '# skip', 'two=2'])

        #print('env', os.environ)

        # skip line when not name=value pattern
        self.assertEqual(result, ['one=1', 'two=2'])

        # Load environment with name:value pair
        self.assertTrue('one' in os.environ)
        self.assertTrue('two' in os.environ)

        # load Load list with name=value pairs
        self.assertTrue('one=1' in result)
        self.assertTrue('two=2' in result)

        # return LbDevEnv
        self.assertTrue(type(result) is LbDevEnv)

    def test_open(self):
        result = self.actual.open()
        self.assertNotEqual(result, [])
        # return LbDevEnv
        self.assertTrue(type(result) is LbDevEnv)
        ##* Initialize list/object when file not found

        self.assertTrue('WS_ORGANIZATION=TBD' in result)
        self.assertTrue('WS_WORKSPACE=TBD' in result)
        self.assertTrue('GH_USER=TBD' in result)
        self.assertTrue('GH_PROJECT=TBD' in result)
        self.assertTrue('GH_BRANCH=TBD' in result)

        self.assertTrue('WS_ORGANIZATION' in os.environ)
        self.assertTrue('WS_WORKSPACE' in os.environ)
        self.assertTrue('GH_USER' in os.environ)
        self.assertTrue('GH_PROJECT' in os.environ)
        self.assertTrue('GH_BRANCH' in os.environ)

        ##* Open when .env is found
        stuff = ['one=1','two=2']
        lb = LbDevEnv()\
            .setFolder(self.temp_folder)\
            .setFilename(self.temp_filename)\
            .load(stuff)\
            .save()

        ##* Read .env and load into environment
        result = self.actual.setFolder(self.temp_folder)\
                   .setFilename(self.temp_filename)\
                   .open()
        self.assertTrue('one=1' in result)
        self.assertTrue('two=2' in result)

        #print('open result', result)

        ##* returns LbDevEnv
        self.assertTrue(type(result) is LbDevEnv)

    def test_set(self):
        self.assertFalse('a' in os.environ)    # not in list
        self.assertFalse('a=a' in self.actual) # not in environ

        result = self.actual.set('a', 'a')
        ##* append name=value when "<name>=" is NOT in list
        self.assertTrue('a=a' in result)

        ##* upsert os.environ
        self.assertTrue('a' in os.environ)

        ##* output LbDevEnv
        self.assertTrue(type(result) is LbDevEnv)

    def test_upsert(self):
        values = {'one': 'one', 'two': 'two'}
        result = self.actual.upsert(values)
        self.assertTrue(type(result) is LbDevEnv)
        self.assertTrue('one=one' in result)
        self.assertTrue('two=two' in result)
        self.assertTrue('one' in os.environ)
        self.assertTrue('two' in os.environ)

if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()