
source LbDevEnvTest(unittest.TestCase)

* return None __When__ <name> not found ... [x] has test
* return ln __When__ line starts with <name> found ... [x] has test
* __Initialize__ list/object __When__ file not found
* __Open__ __When__ .env is found
* __Read__ .env and __Load__ into environment
* returns LbDevEnv
* append name=value __When__ "<name>=" is NOT in list
* upsert os.environ
* __Output__ LbDevEnv
