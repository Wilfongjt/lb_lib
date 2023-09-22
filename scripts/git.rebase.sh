#!/bin/bash
#source ./get_input.sh
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
cd ..
# open _bk.config and load variables
set -o allexport
source .env set
set +o allexport
# show env
#env
# goto project folder
#cd ..

ls

# confirm values
export GH_TRUNK=main
export WS_ORGANIZATION=$(get_input "ws.organization" "${WS_ORGANIZATION}")
export WS_WORKSPACE=$(get_input "ws.workspace" "${WS_WORKSPACE}")
export GH_USER=$(get_input "gh.user" "${GH_USER}")
export GH_PROJECT=$(get_input "gh.project" "${GH_PROJECT}")
export GH_BRANCH=$(get_input "gh.branch" "${GH_BRANCH}")
export GH_MESSAGE=$(get_input "gh.message" "${GH_MESSAGE}")
export PUSH=N
export CONT=N
export CONT=$(get_input "Continue?" "${CONT}")
echo ${GH_TRUNK}
echo ${WS_ORGANIZATION}
echo ${WS_WORKSPACE}
echo ${GH_USER}
echo ${GH_PROJECT}
echo ${GH_BRANCH}
echo ${GH_MESSAGE}
echo ${PUSH}
echo ${CONT}
if [ ${CONT} = "N" ]; then
  echo "Stopping."
  exit 0
fi
echo "Continuing"
ls
# rebase
# prepare to save branch changes
cd ${GH_PROJECT}/   
git checkout ${GH_BRANCH}
git add .
git commit -m "${GH_MESSAGE}"
exit 0
# download any repo changes made by another
git checkout ${GH_TRUNK} 
echo "----"
git pull origin ${GH_TRUNK}    
# change back to my changes
git checkout ${GH_BRANCH}
git branch
# rebase
echo "-- rebase"
git rebase ${GH_BRANCH}
export PUSH=$(get_input "PUSH?" "${PUSH}")
if [ ${PUSH} = "N" ]; then
  echo "Remember to Push later."
  exit 0
fi
echo "-- pushing"
git push origin "${GH_BRANCH}"
# open a browser for convenience
open -a "Google Chrome" "https://github.com/${GH_USER}/${GH_PROJECT}"
# giv user some feedback
git status
