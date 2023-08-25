#!/bin/bash
function get_input()
{
  # prompt for input
  # $1 is prompt
  # $2 is default value
  local prompt=$1
  local default=$2
  local answer
  prompt+="[${default}]"
  read -p $prompt answer
  if [ "$answer" = "" ]; then
    answer=$default
  fi
  echo $answer
}
function current_git_branch() {
  git symbolic-ref --short HEAD 2>/dev/null
}
function hasGitBranchChanges() {
  local rc 
  # Get the current branch name
  current_branch=$(git symbolic-ref --short HEAD 2>/dev/null)
  # Check if the branch exists and is not empty
  if [ -n "$current_branch" ]; then
    # Check if there are any changes in the branch
    if [[ $(git status --porcelain) ]]; then
      #echo "Branch '$current_branch' has uncommitted changes."
      rc=1
    else
      #echo "Branch '$current_branch' is clean with no uncommitted changes."
      rc=0
    fi
  else
    #echo "Not in a Git branch."
    rc=2
  fi
  echo $rc
}
function createGitBranch() {
  if [ $# -ne 1 ]; then
    echo "Usage: createGitBranch <branch-name>"
    return 1
  fi
  local branch_name="$1"
  # Check if the branch already exists
  if git show-ref --quiet "refs/heads/$branch_name"; then
    echo "Branch '$branch_name' already exists."
    return 1
  fi
  # Create and switch to the new branch
  git checkout -b "$branch_name"
  echo "Created and switched to branch '$branch_name'."
}
# open .env and load variables
set -o allexport
source .env set
set +o allexport
export GH_TRUNK=main
# show env
env
echo 'A'
# goto project folder
cd ..
ls
echo 'B'
# never allow a commit to main branch
if [ $(current_git_branch) = ${GH_TRUNK} ]; then
    echo "Script wont commit changes to main branch ${GH_TRUNK}"
    exit
fi
# check for expected branch ie GH_BRANCH must match current branch
if [ $(current_git_branch) != ${GH_BRANCH} ]; then
    echo "expected branch ${GH_BRANCH} found $(current_git_branch)"
    echo "...stopping"
    exit
fi
echo 'C'
# dont allow new branch when changes are outstanding
if [ $(hasGitBranchChanges) != 0 ]; then
    echo ${GH_BRANCH}
    echo "${GH_BRANCH} has uncommited changes ... Run git.rebase.sh before opening a new branch"
    exit
fi
echo 'D'
# change to new branch
export NEXT_BRANCH=$(get_input "gh.branch" "${GH_BRANCH}")
$(createGitBranch "${NEXT_BRANCH}")
git branch
echo "new branch ${NEXT_BRANCH}"
# update .env
