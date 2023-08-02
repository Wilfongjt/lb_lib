# Branch Process
 Goal - __Download a GitHub Project__
* Create Development folder on developer's computer
* Set a branch
# class InitializeEnvironment(LbStep)
## __Initialize__ LyttleBit Application
* __Open__ enviroment file __When__ found in \<SOURCE> folder
* __Impute__ the Developement folder name (aka /<DEVELOPMENT>), eg ~/Development
* __Impute__ the Project folder name (aka \<DEVELOPMENT>/\<Project>), eg ~/Development/\<workspace>/\<project>
# class CollectInputs(LbStep)
## __Collect__ Inputs
* WS_ORGANIZATION
* WS_WORKSPACE
* GH_USER
* GH_PROJECT
* GH_BRANCH
# class ImputeVariables(LbStep)
## __Impute__ Variables
* __Impute__ project url
# class VerifyInputs(LbStep)
## Verify Inputs
* __Stop__ __When__ workspace ('WS_') settings are invalid
* __Stop__ __When__ GitHub ('GH_') settings are invalid
* __Stop__ __When__ remote repo is not found
# class CreateWorkspaceFolder(LbStep)
## Create Workspace
* Create Workspace folder __When__ folder doesnt exist
* Store Workspace folder name in Stash
* Store Projcet folder name in Stash
# class UpdateEnvironment(LbStep)
## Update Environment
* __Load__ settings into environment variables
# class SaveEnv(LbStep)
# class CloneProject(LbStep)
# class LbBranch(LbStepList)
