##################################


source depInitializeEnvironment(LbStep)


## __Initialize__ LbEnvironment

* Ensure git.rebase is running from the scripts folder, ie current folder ends with "scripts"

* set project to {}

* set prompts to {}

* set prompts to TBD

* echo lb_stash __When__ verbose is true

#########################################


source PromptRebaseInputs(LbStep)


## __Collect__ __Inputs__ as process step

* WS_ORGANIZATION is collected from path or user

* WS_WORKSPACE is collected from path or user

* GH_USER is collected from path or user

* GH_PROJECT is collected from path or user

* GH_BRANCH is collected from path or user

* GH_MESSAGE is always collected from user


source depImputeProjectVariables(LbStep)


## __Impute__ Variables

* __Impute__ REPO_URL_KEY

* __Impute__ Project Folder


source depValidateRebasePromptImputs(LbStep)


* __Validate__ PROMPTS_KEY

* __Validate__ Prompts

* Invalid __When__ WS_ORGANIZATION in ['', None, 'TBD']

* Invalid WS_WORKSPACE in ['', None, 'TBD']

* Invalid GH_USER in ['', None, 'TBD']

* Invalid GH_PROJECT in ['', None, 'TBD']

* Invalid GH_BRANCH in ['', None, 'TBD']

* Invalid GH_MESSAGE in ['', None, 'TBD']


source depValidateProject(LbStep)


* __Validate__ PROJECT_KEY

* Invalid __When__ Project folder is not found


source ValidateRepo(LbStep)


* __Validate__ REPO_URL_KEY

* Invalid Repo __When__ remote repo is not found


source ValidateBranch(LbStep)


* Invalid BRANCH_KEY __When__ value is '', None, or TBD

* Invalid Branch __When__ git branch does not exist

* Invalid Branch __When__ branch name is equal to "TBD"

* Invalid Branch __When__ branch is equal to "main"...as rule don't update main


source Rebase(LbStep)


##

## Rebase Project

* __Stop__ __When__ invalid

*  __Checkout__ branch

* Add files to git

* Commit with <MESSAGE>

* __Checkout__ main branch

* Pull origin main

* __Checkout__ branch

* Rebase repo

* Push to origin


source LbRebaseProcess(LbStepList)


1. Initilaize Enviromment

1. __Prompt__ Rebase __Inputs__

1. __Impute__ Project Variables

1. __Validate__ Project

1. __Validate__ Repo

1. __Validate__ Branch

1. Rebase

1. Status

