#!/bin/bash
source functions.sh
echo "* Script"
echo "    - run folder: $PWD"

#readLinesFromFile

echo "GH_BRANCH=GH_BRANCH" > workout.env
echo "GH_BRANCH2=GH_BRANCH" >> workout.env
echo "GH_BRANCH3=GH_BRANCH" >> workout.env

#
# SCRIPT START
#
echo "... Initialize Environment ..."

#
# Initialize from environment file when .env found
#
echo "* Initialize environment from environment file when environment file is found"
env_file_name="xxxx.env"
if test -f "$env_file_name"; then
    #if [ -f "$env_file_name" ]; then
    echo "    - environment file $env_file_name"
    set -o allexport
    source $env_file_name set
    set +o allexport
fi

# Create an environment file when .env not found

echo "* Create an environment file when environment file not found"
rc=$(create_env "$env_file_name")

#
# Confirm Inputs
#
echo "    Confirm Inputs"
export GH_TRUNK=main
export WS_ORGANIZATION=$(get_input "ws.organization" "${WS_ORGANIZATION}")
export WS_WORKSPACE=$(get_input "ws.workspace" "${WS_WORKSPACE}")
export GH_USER=$(get_input "gh.user" "${GH_USER}")
export GH_PROJECT=$(get_input "gh.project" "${GH_PROJECT}")
export GH_BRANCH=$(get_input "gh.branch" "${GH_BRANCH}")
export GH_MESSAGE=$(get_input "gh.message" "${GH_MESSAGE}")

# Validate Inputs
#
echo "* Validate Inputs"
rc=$(validate_inputs "WS_");
msg1=$(is_ok $? "invalid")
echo "    - validate WS $msg1"

rc=$(validate_inputs "GH_");
msg2=$(is_ok $? "invalid")
echo "    - validate GH $msg2"

if [[ msg2 -ne "ok" ]]; then
  echo "* A Invalid Input stopping..."
  echo "$(show_inputs "WS_")"
  echo "$(show_inputs "GH_")"
  echo "    ...stopped"
  exit 1
fi


if [[ $(validate_inputs "WS_") -eq 0 || $(validate_inputs "GH_") -eq 0 ]]; then
  echo "* Invalid Input stopping..."
  echo "$(show_inputs "WS_")"
  echo "$(show_inputs "GH_")"
  echo "    ...stopped"
  exit 1
fi

#
# Update the environment file
#
echo "* Update the environment file when environment file is found"
# echo "hio $env_file_name $WS_ORGANIZATION"
rc=$(add_env_variable "$env_file_name" "WS_ORGANIZATION" "$WS_ORGANIZATION")
rc=$(add_env_variable "$env_file_name" "WS_WORKSPACE" "$WS_WORKSPACE")
rc=$(add_env_variable "$env_file_name" "GH_PROJECT" "$GH_PROJECT")
rc=$(add_env_variable "$env_file_name" "GH_USER" "$GH_USER")
rc=$(add_env_variable "$env_file_name" "GH_BRANCH" "$GH_BRANCH")
echo "    - env is updated"
#echo "H folder: $PWD"


#
# Create the workspace when folder is not found
#
echo "* Create workspace when workspace doesnt exist"
rc=$(create_workspace "$WS_ORGANIZATION" "$WS_WORKSPACE")
echo "    - workspace is $(is_ok $? 'unavailable')"
#echo "I folder: $PWD"
# GS.create_workspace("$WS_ORGANIZATION" "$WS_WORKSPACE")
#echo "----"

# Change dir to workspace folder
echo "* Change to workspace folder"
cd "${HOME}/Development/${WS_ORGANIZATION}/${WS_WORKSPACE}/"
echo "    - folder: $PWD"
#
# Clone GitHub Project Repository when repo is not found
#

echo "* Clone GitHub Project when clone hasn't been downloaded"
echo "    - url      : https://github.com/${GH_USER}/${GH_PROJECT}.git"
echo "    - workspace: ${HOME}/Development/${WS_ORGANIZATION}/${WS_WORKSPACE}"
echo "    - project  :   ${HOME}/Development/${WS_ORGANIZATION}/${WS_WORKSPACE}/${GH_PROJECT}"
rc=$(clone_project "$WS_ORGANIZATION" "$WS_WORKSPACE" "$GH_PROJECT" "$GH_USER")
echo "    - clone is $(is_ok $? 'bad')"

# Change dir to project folder
echo "* Change to project folder"
cd "${HOME}/Development/${WS_ORGANIZATION}/${WS_WORKSPACE}/${GH_PROJECT}"
echo "    - folder: $PWD"

# Stage files...add . when current branch is not main
#
echo "* Stage Files when branch is not main"
cur_branch=$(get_branch_current)
echo "    - current branch is $cur_branch"
rc=$(stage_branch_current);
echo "    - staging is $rc"

#
# Commit branch when current branch is not main
#
echo "* Commit branch when current branch is not main"
cur_branch=$(get_branch_current)
echo "    - current branch is $cur_branch"
rc=$(commit_branch_current "$GH_MESSAGE")
echo "    - commit is $rc"

exit
# Create branch when it doesnt exist

echo $(create_branch "$GH_BRANCH")

#
# Checkout branch when current branch is main
#
echo $(checkout_branch "$GH_BRANCH")

exit
#
# Add & Commit branch when current branch is not main
#                          and current branch has uncommitted changes
#echo $(add_commit_branch "$GH_BRANCH" "$GH_MESSAGE")
#
# Create Branch when current branch is main
#
#echo $(add_branch  "$GH_BRANCH")

#
# Rebase when current branch has changes
#                            and is not main

# Push branch when branch has committed changes


# Open GitHub

#git status