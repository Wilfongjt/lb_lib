
source LbProject(LbUtil)


## Determine a GitHub user name

* 1. find the ~/.gitconfig file and __Read__ "name = " value

* 1. default github user to TBD

## Get branch name on request

* branch is found in .git repo eg (HEAD ref refs/heads/00_init)

* returns str

## Get Development Folder Name on request

* Split the current folder name

* retrieve  from folder name eg "/User/~/Development/\<organization>/\<workspace>/\<project>/"

* return str

## Get the Organization Name on request

* retrieve \<organization> from path eg "~/Development/\<organization>/\<workspace>/\<project>/"

* return str ... [x] has test

## Get the Project Name on request

* retrieve \<project> from path eg "~/Development/\<organization>/\<workspace>/\<project>/"

* return str ... [x] has test

## Get the Workspace Name on request

* retrieve \<workspace> from path eg "~/Development/\<organization>/\<workspace>/\<project>/"

* return str ... [x] has test

## Test for a branch by name on request

* use "git branch" command and search for branch name in result

* True is not testable because

* return bool ... [x] has test

## Test for Project on GitHub on request

* use "git ls-remote" command and search for branch name in result

* return bool

## Test for".git" in Project

* return bool

## __Prompt__ user for __Input__

* hard __Stop__ __When__ user types 'n','N','x','X','q' or 'Q'

* return str

## Verify List of __Prompt__ Values

* eg []

#####

