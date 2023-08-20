# Branch Process

 Goal - __Download a GitHub Project__

* Create Development folder on developer's computer

* Set a branch


source LbEnvironment(LbDefaults)


## LbEnvironment Variables

* __Collect__ environment variables from memory using default keys


source PromptBranchInputs(LbStep)


## __Prompt__ user for __Inputs__ on request

## __Collect__ __Inputs__

* WS_ORGANIZATION

* WS_WORKSPACE

* GH_USER

* GH_PROJECT

* GH_BRANCH


source LbBranch(LbStepList)


## Download GitHub Branch

1. __Initialize__ Environment

1. __Prompt__ for __Inputs__

1. __Impute__ Project Variables

1. __Validate__ __Input__ Variables

1. Create Workspace

1. __Clone__ Project

1. __Save__ Environment

1. __Show__ Status

##

