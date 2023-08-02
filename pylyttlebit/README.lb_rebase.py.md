##################################
# class InitializeEnvironment(LbStep)
## __Initialize__ Environment
* Ensure git.rebase is running from the scripts folder, ie current folder ends with "scripts"
* set project to {}
* set prompts to {}
* set prompts to TBD
* echo stash __When__ verbose is true
#########################################
# class PromptInputs(LbStep)
## __Collect__ Inputs as process step
* WS_ORGANIZATION is collected from path or user
* WS_WORKSPACE is collected from path or user
* GH_USER is collected from path or user
* GH_PROJECT is collected from path or user
* GH_BRANCH is collected from path or user
* GH_MESSAGE is always collected from user
# class ImputeProjectVariables(LbStep)
## __Impute__ Variables
* __Impute__ REPO_URL_KEY
* __Impute__ Project Folder
# class ValidatePrompts(LbStep)
* Validate PROMPTS_KEY
* Validate Prompts
* Invalid __When__ WS_ORGANIZATION in ['', None, 'TBD']
* Invalid WS_WORKSPACE in ['', None, 'TBD']
* Invalid GH_USER in ['', None, 'TBD']
* Invalid GH_PROJECT in ['', None, 'TBD']
* Invalid GH_BRANCH in ['', None, 'TBD']
* Invalid GH_MESSAGE in ['', None, 'TBD']
# class ValidateProject(LbStep)
* Validate PROJECT_KEY
* Invalid __When__ Project folder is not found
# class ValidateRepo(LbStep)
* Validate REPO_URL_KEY
* Invalid Repo __When__ remote repo is not found
# class ValidateBranch(LbStep)
* Validate BRANCH_KEY
* Invalid Branch __When__ branch does not exist
* Invalid Branch __When__ branch is equal to "TBD"
* Invalid Branch __When__ branch is equal to "main"
# class Rebase(LbStep)
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
# class LbRebaseProcess(LbStepList)
1. Initilaize Enviromment
1. Prompt Inputs
1. __Impute__ Project Variables
1. Validate Prompts
1. Validate Project
1. Validate Repo
1. Validate Branch
1. Rebase
