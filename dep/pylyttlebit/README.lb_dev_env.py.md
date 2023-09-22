# Development Environment


source LbDevEnv(LbTextFile)


### Create and __Load__ an ".env" file

* always __Load__ env values from file

* always __Save__ from memory

* ".env" is file name, by default

* put ".env" file in the calling function's folder by default

#### Clear environment variables on request

> Remove script specific environment variables from memory

* remove envirionment variables from memory

* remove environment variables from list

#### Create env file on request

* __Skip__ create __When__ env file exists

* create file __When__ file doesnt exist

__Get line from list on request__

* return None __When__ <name> is not found ... [x] has test

* return ln __When__ line starts with <name> is found ... [x] has test

__Put variable into memory on reques__

* __Convert__ defaults dictionary to defaults list  ...  [] has test

__Load list of text on request__

> __Loads__ .env's name and value pairs into memory

* remove line's trailing EOL

* Lines containing an equal sign are environment values

* update existing values

* any lines not containing an equal sign "=" are considered a comment

* returns LbDevEnv ... has test

__Open .env on request__

* __Save__ env file __When__ file not found and defaults are set

* __Open__ .env from file __When__ .env is found

* __Load__ environment variables from .env __When__ .env is found  ... [x] has test

* Remember to call Save() to commit to HD

* returns LbDevEnv ... [x] has test

__Set environment variable on request__

* keep os.environ and list in sync

* update environment variable __When__ variable in list

* append variable __When__ not in list

* update variable to os.environ __When__ found in os.environ

* add variable in os.environ __When__ not found in os.environ

* __Output__ LbDevEnv ... [x] has test

__Set environment variables from dictionary on request__

* __Skip__ setting environment variables __When__ dictionary parameter is None

* set environment variable __When__ found in dictionary parameter

__Set environment variables from list of file lines on request__

* convience method that encapsulates __Load__ method

__Convert enviroment list to dictionary on request__

* environment list and memory are always in-scync

