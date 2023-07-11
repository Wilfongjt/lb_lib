# class LbDevEnv(LbTextFile)

 Create and __Load__ an .env file

* by default .env is file name

* by default put .env file in the calling function's folder

* __Make__ environments easy to __Collect__ with prefixes ie, ['GH_','WS_'] ... [] has test

## Get line from list on request

* return None __When__ <name> is not found ... [x] has test

* return ln __When__ line starts with <name> is found ... [x] has test

## Get .env defaults on request

> __Make__ a dictionary of nameTBD pairs

* __Define__ initial state for environment ... [x] has test

* outputs dictionary

## Get Environment Defaults as a List on request

> __Convert__ default dictionary to list, ie. {namevalue,...} --> [name=value,...]

* __Convert__ defaults dictionary to defaults list  ... [] has test

* __Output__ list

## __Collect__ environment variables on request

> __Makes__ a dictionary of namevalue pairs from environment specific to library

1. __Provide__ default env variables with default values

1. __Merge__ env variable values from environment into defaults

1. __Output__ dictionary of library specific Environment Variables ... [x] has test

## __Load__ list of text on request

> __Loads__ list of name=value pairs into environment

* remove line's trailing EOL

* __Skip__ line __When__ line starts with "#" ... [x] has test

* __Skip__ line __When__ not name=value pattern ... [x] has test

* set name value pair ... tested in test_set

* returns LbDevEnv ... has test

## __Open__ .env on request

> __Open__ and __Load__ an .env file.

* __Initialize__ list/object __When__ file not found ... [] has test

* __Open__ __When__ .env is found

* __Read__ .env and __Load__ into environment ... [x] has test

* Remember to call Save() to commit to HD

* returns LbDevEnv ... [x] has test

## Set a name=value pair on request

* update name=value __When__ "<name>=" in list ... [] has test

* append name=value __When__ "<name>=" is NOT in list ... [x] has test

* upsert os.environ ... [x] has test

* __Output__ LbDevEnv ... [x] has test

## Upsert environment values on request

> __Loads__ a dictionary of namevalue pairs into environment

* given a dictionary of variables put them into environment ... [x] has test

