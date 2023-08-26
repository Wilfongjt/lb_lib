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
function replaceLineInFile() {
  if [ $# -ne 3 ]; then
    echo "Usage: replaceLineInFile <filename> <target_line> <replacement_line>"
    return 1
  fi
  local filename="$1"
  local target_line="$2"
  local replacement_line="$3"
  if [ ! -f "$filename" ]; then
    echo "File '$filename' not found."
    return 1
  fi
  local line=""
  local backup="$filename.bak"
  echo "# start" > temp.env
  while IFS= read -r line; do
    # Process each line here, you can replace this with your own logic.
    #echo "Line: $line"
    if [ $line = $target_line ]; then
      echo $replacement_line >> temp.env
    else
      echo "$line" >> temp.env
    fi
  done < "$filename"
  cp "temp.env" "$filename"
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
echo 'C'
# check for expected branch ie GH_BRANCH must match current branch
git branch
if [ $(current_git_branch) != ${GH_BRANCH} ]; then
    echo "expected branch ${GH_BRANCH} found $(current_git_branch)"
    echo "...stopping"
    exit
fi
echo 'D'
# dont allow new branch when changes are outstanding
if [ $(hasGitBranchChanges) != 0 ]; then
    echo "${GH_BRANCH} has uncommited changes ... Run git.rebase.sh before opening a new branch"
    echo "...stopping"
    exit
fi
echo 'E'
# change to new branch
export NEXT_BRANCH=$(get_input "gh.branch" "${GH_BRANCH}")
echo $(createGitBranch "${NEXT_BRANCH}")
echo 'F'
git branch
#echo "new branch ${NEXT_BRANCH}"
# update .env with GH_BRANCH=NEXT_BRANCH
echo $(replaceLineInFile ".env" "GH_BRANCH=${GH_BRANCH}" "GH_BRANCH=${NEXT_BRANCH}")
export GH_BRANCH=${NEXT_BRANCH}
