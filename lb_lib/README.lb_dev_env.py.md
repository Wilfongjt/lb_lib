# class LbDevEnv(LbRecorder):

 Create and load an .env file

* by default: put .env in the calling function's folder

* Create .env file when .env not found

* Recreate .env when .env file is empty

__Delete file on request__

* Delete .env when .env exists

__Check for empty .env file on request__

* open and look for lines

* .env is empty when when all lines in file are blank or EOL

__Upsert environment values on request__

* given a set of variable put them into environment

__Get .env defaults on request__

* define initial state for environment

__Confirm .env file exists on request__

* .env file exists when .env file is found

__Open .env on request__

* Open when .env is found

* Read .env and load into environment

* Load .env variable when "<name>=<value>" pattern found in .env

__Save .env on request__

* Provide default .env file when .env NF

* Collect param-values from environment when .env is found

* Get fresh values from environment when found

 __Collect environment variables on request__

* Provide default .env variable value when expected variable are not found in environment

* Collect env variables from environment

