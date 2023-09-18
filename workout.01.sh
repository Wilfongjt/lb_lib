#!/bin/bash

echo "... Functions ..."
function is_ok() {
    if [ $# -ne 1 ]; then
        echo "Usage: is_ok <return_code_number>"
        return 1
    fi
    local rc=$1
    if [ $rc -eq 0 ]; then
        echo "ok"
    else
        echo "bad"
    fi

    return 0
};
echo $(is_ok 0);
echo $(is_ok "0");
echo $(is_ok 1);
echo $(is_ok "1");
#exit
#valid_inputs=1 # global to indicate valid inputs
# base independent functions
function get_input() {
    # prompt user for input or return default when no user value is given

    if [ $# -ne 2 ]; then
        echo "Usage: get_input <prompt> <default>"
        return 1
    fi
    # $1 is prompt
    # $2 is default value
    local prompt=$1
    local default=$2
    local answer

    if [ -z "$default" ]; then
      default="TBD"
    fi
    prompt="....$prompt"
    prompt+="[${default}]"
    read -p $prompt answer

    if [ -z "$answer" ]; then
      answer=$default
    fi
    echo $answer
    return 0
};    echo $(get_input);
# echo $(get_input "GH_PROJECT" "$GH_PROJECT")
#
function has_repo() {
    if [ $# -ne 0 ]; then
        echo "Usage: has_repo "
        return 1
    fi
    local folder_name='.git'
    # create file when doesnt exist
    if [ ! -d "$folder_name" ]; then
        #echo "repo $folder_name doesnt exist."
        echo 0
        return 0
    fi
    #echo "repo exists"
    echo 1
    return 0
};     echo $(has_repo "help");
#
function has_branch() {
    if [ $# -ne 1 ]; then
        echo "Usage: has_branch <branch_name>"
        return 1
    fi
    local branch_name="$1"
    local result

    # Check if the branch exists
    if git show-ref --quiet --verify "refs/heads/$branch_name"; then
        result=true
    else
        result=false
    fi

    echo "$result"
}; echo $(has_branch); #echo $(has_branch "main"); echo $(has_branch "00_init"); echo $(has_branch "01_bad")
#
function has_branch_changes() {

    if [ $# -ne 0 ]; then
        echo "Usage: has_branch_changes"
        return 1
    fi

    if [ -n "$(git status --porcelain)" ]; then
        echo "true"
    else
        echo "false"
    fi
    return 0
};
#
function count_branches() {
  # get branch count for the current repo
  if [ $# -ne 0 ]; then
        echo "Usage: count_branches"
        return 1
    fi
    # Use git branch command to list branches and count them
  local branch_count=$(git branch | wc -l)

  # Print the branch count
  echo "$branch_count"
}; echo $(count_branches "help"); #echo "branches...$(count_branches)"
#if [$(count_branches) -eq 2 ]; then
#  echo "True"
#fi
#
function create_branch() {
  # create branch when new branch not eq main
  # create branch when new branch not eq current_branch
   if [ $# -ne 1 ]; then
        echo "Usage: create_branch <branch-name>"
        return 1
  fi

  local new_branch="$1"

  # Get the current branch name
  local current_branch=$(git symbolic-ref --short HEAD 2>/dev/null)

  # branch already exists
  if [[ "$(has_branch $new_branch)" = "true" ]]; then
    echo "No need to create branch $new_branch"
    return 0
  fi

  #if [[ $(count_branches) -ne 1 ]]; then
  #  echo "Cannot create more than 1 branch"
  #  return 1
  #fi

  git branch "$new_branch"
  echo "new branch $new_branch"
  return 0
}; echo $(create_branch); #echo $(create_branch "main"); #echo $(create_branch "x01");
#
function checkout_branch() {
  # "* Checkout branch when current branch is main"

  # fail checkout when current branch has uncommitted changes
  # fail checkout when new_branch is main
  # checkout first branch when current_branch is main and branch count is 1
  # checkout next branch when new_branch is not eq to current branch
  #                                      and current branch has no changes
  # checkput_branch when current branch is main
  #                                     and branch_name not main
  #                                     and branch_count is 1

   if [ $# -ne 1 ]; then
        echo "Usage: checkout_branch <branch-name>"
        return 1
  fi

  local branch_name="$1"
  local current_branch=$(git symbolic-ref --short HEAD 2>/dev/null)
  # branch must exist
  if [[ "$(has_branch $branch_name)" = "false" ]]; then
    echo "    Cannot checkout branch, branch not found: $branch_name"
    return 1
  fi
  #
  #if [[ "$branch_name" = "main" ]]; then
  #  echo "    Already checkedout $branch_name"
  #  return 0
  #fi

  # already checked out
  if [[ "$branch_name" = "$current_branch" ]]; then
    echo "    Already checkedout $branch_name"
    return 0
  fi
  # current branch has changes
  if [ "$(has_branch_changes)" = 'true' ]; then
    echo "    Uncommited changes"
    return 1
  fi

  git checkout "$branch_name"

}; echo $(checkout_branch "main"); echo $(checkout_branch); #echo $(checkout_branch "00_init");
#
function stage_branch_current() {
  # Stage files...add . when current branch is not main
  if [ $# -ne 0 ]; then
        echo "Usage: stage_branch_current"
        return 1
  fi
  local current_branch=$(git symbolic-ref --short HEAD 2>/dev/null)

  # dont stage the main bRANCH

  if [[ "$current_branch" = "main" ]]; then
      echo "Dont stage main branch"
      return 0
  fi

  git add .

  echo "staged $current_branch"
  return 0
};
#
function commit_branch_current() {
  # Commit branch when current branch is not main

  if [ $# -ne 1 ]; then
        echo "Usage: commit_branch_current <commit-message>"
        return 1
  fi
  if [[ "$current_branch" = "main" ]]; then
      echo "Dont commit main branch"
      return 1
  fi
  local commit_message="$1"

  git commit -m "$commit_message"
  echo "commited $current_branch"

  return 0
};
#

function create_env() {
    if [ $# -ne 1 ]; then
        echo "Usage: create_env <file_name> "
        return 1
    fi
    local file_name=$1
    local rc=0
    # create file when doesnt exist
    if test -f "$file_name"; then
        echo "    $file_name exists."
    else
        echo "# environment" > "$file_name"
        rc=$(add_env_variable "$file_name" "WS_ORGANIZATION" "TBD")
        rc=$(add_env_variable "$file_name" "WS_WORKSPACE" "TBD")
        rc=$(add_env_variable "$file_name" "GH_PROJECT" "TBD")
        rc=$(add_env_variable "$file_name" "GH_USER" "TBD")
        rc=$(add_env_variable "$file_name" "GH_BRANCH" "TBD")
    fi

    return 0
};   echo $(create_env);
#
function add_env_variable() {
  # echo $# $1 $2 $3
    if [ $# -ne 3 ]; then
        echo "Usage: add_env_variable <filename> <variable_name> <variable_value>"
        return 1
    fi
    # write original file (.env) one line at a time to temporaty file (temp.env)
    # replace line with replacement_line when line equals target_line
    # overwrite original file (.env) with temporary file ()
    # delete temporary file

    local filename="$1"
    local var_name="$2"
    local replacement_line="$var_name=$3"

    #echo "file $filename"
    #echo "var_name $target_line"
    #echo "replacement_line $replacement_line"
    #echo "B"
    if [ ! -f "$filename" ]; then
      echo "File '$filename' not found."
      return 1
    fi
    #echo "C"
    local line=""
    local replaced="0"
    #local backup="$filename.bak"
    #echo "# date: " > temp.env
    while IFS= read -r line; do
      if [[ "$line" == "$var_name"* ]]; then
        if [[ "$line" != "$replacement_line" ]]; then
          echo "# $line" >> temp.env
        fi

        echo "$replacement_line" >> temp.env
        replaced="1"
            # do nothing echo "$line" >> temp.env
      else
        if [[ "$line" != "$replacement_line" ]]; then
          echo "$line" >> temp.env
        fi
      fi

    done < "$filename"
    if [[ $replaced = "0" ]]; then
       echo "$replacement_line" >> temp.env
    fi
    # replace original .env with new temp.env
    cp "temp.env" "$filename"
    # delete the temporary file
    rm "temp.env"
    return 0
}; echo $(add_env_variable);
#

function show_inputs() {
  if [ $# -ne 1 ]; then
        echo "Usage: show_inputs <prefix>"
        return 1
    fi

    local prefix=$1

    for var in $(env | cut -d '=' -f1); do
      # starts with
      if [[ "$var" == "$prefix"* ]]; then
          echo "    $var=${!var} / "
      fi
    done

}; #echo $(show_inputs "X");

#
function validate_inputs() {
    if [ $# -ne 1 ]; then
        echo "Usage: validate_inputs <prefix>"
        return 1
    fi

    local prefix=$1
    local found=0

    for var in $(env | cut -d '=' -f1); do
      # starts with
      if [[ "$var" == "$prefix"* ]]; then
        found=1
        if [[ ${!var} == "TBD" ]]; then
          #echo "Invalid input $var=${!var}"
          echo 0
          return 1
        fi
      fi
    done

    if [[ $found -eq 0 ]]; then
      #echo "env var not found $prefix"
      echo 0
      return 2
    fi
    echo 1
    return 0
}; echo $(validate_inputs "GH_");
#
function create_workspace() {
   if [ $# -ne 2 ]; then
        echo "Usage: create_workspace <organization_name> <workspace_name>"
        return 1
    fi

    local org_name=$1
    local workspace_name=$2
    local folder_name="$HOME/Development/$org_name/$workspace_name"
    if [ -d "$folder_name" ]; then
      echo "....ok, Found workspace $folder_name"
      return 0
    fi

    if mkdir -p "$folder_name"; then
      echo "....ok... Workspace directory '$folder_name' created successfully."
    else
      echo "....Failed to create workspace directory '$folder_name'."
      return 1
    fi
    return 0
}; $(create_workspace);

function clone_project() {
    # aka clone

    if [ $# -ne 4 ]; then
        echo "Usage: clone_project <ws_organization> <ws_workspace> <gh_project> <gh_user>"
        return 1
    fi

    local wsOrganization=$1
    local wsWorkspace=$2
    local ghProject=$3
    local ghUser=$4

    local project_url="https://github.com/$ghUser/$ghProject.git"
    local workspace_folder="$HOME/Development/$wsOrganization/$wsWorkspace"
    local project_git_folder="$HOME/Development/$wsOrganization/$wsWorkspace/$ghProject"
    #echo "$username"
    #echo "$project_name"
    #echo "$project_url"
    #echo "$project_git_folder"
    #echo $(has_repo)
    if [[ -d "$project_git_folder" ]]; then
        # clone not found
          #echo "....ok"
          return 0
    fi

    #echo "Cloning"
    # stash current folder
    local last_folder=$PWD
    # change workspace folder
    cd "$workspace_folder/"
    # clone
    git clone "$project_url"
    # reset to original folder
    cd "$last_folder/"
    return 0
};     echo $(clone_project);
#
function get_branch_current() {
    if [ $# -ne 0 ]; then
        echo "Usage: get_branch_current "
        return 1
    fi

    echo $(git symbolic-ref --short HEAD 2>/dev/null)

    return 0
}; echo $(get_branch_current "help");

function set_branch() {
    if [ $# -ne 1 ]; then
        echo "Usage: set_branch <branch_name> "
        return 1
    fi
    #local branch_name="$1"
    #git checkout "$branch_name"
    return 0
}; echo $(set_branch);
#
function rebase_branch() {
    if [ $# -ne 1 ]; then
        echo "Usage: rebase_branch <branch_name> "
        return 1
    fi
    return 0
}; echo $(rebase_branch);

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
echo "* Initialize from environment file when .env found"
env_file_name="xxxx.env"
if test -f "$env_file_name"; then
    #if [ -f "$env_file_name" ]; then
    echo "    Load environment from file $env_file_name"
    set -o allexport
    source $env_file_name set
    set +o allexport
fi
#
# env
#
#echo "............"
#exit
# Create an environment file when .env not found

echo "* Create an environment file when .env not found"
rc=$(create_env "$env_file_name")

#exit
#
# Confirm Inputs
#
echo "* Confirm Inputs"
export GH_TRUNK=main
export WS_ORGANIZATION=$(get_input "ws.organization" "${WS_ORGANIZATION}")
export WS_WORKSPACE=$(get_input "ws.workspace" "${WS_WORKSPACE}")
export GH_USER=$(get_input "gh.user" "${GH_USER}")
export GH_PROJECT=$(get_input "gh.project" "${GH_PROJECT}")
export GH_BRANCH=$(get_input "gh.branch" "${GH_BRANCH}")
export GH_MESSAGE=$(get_input "gh.message" "${GH_MESSAGE}")
#echo "----"
#
# Validate Inputs
#
echo "* Validate Inputs"
rc=$(validate_inputs "WS_")

echo "    validate WS $(is_ok $?)"
rc=$(validate_inputs "GH_")

echo "    validate GH $(is_ok $?)"

if [[ $(validate_inputs "WS_") -eq 0 || $(validate_inputs "GH_") -eq 0 ]]; then
  echo "* Invalid Input"
  echo "$(show_inputs "WS_")"
  echo "$(show_inputs "GH_")"
  echo "    ...stopped"
  exit 1
fi

#echo "----"
#
# Update the environment file
#
echo "* Update the environment file"

rc=$(add_env_variable "$env_file_name" "WS_ORGANIZATION" "$WS_ORGANIZATION")

rc=$(add_env_variable "$env_file_name" "WS_WORKSPACE" "$WS_WORKSPACE")
rc=$(add_env_variable "$env_file_name" "GH_PROJECT" "$GH_PROJECT")
rc=$(add_env_variable "$env_file_name" "GH_USER" "$GH_USER")
rc=$(add_env_variable "$env_file_name" "GH_BRANCH" "$GH_BRANCH")
echo "    Updated updated environment file: $env_file_name"

#
# Create the workspace when folder is not found
#
echo "* Create workspace when folder is not found"

rc=$(create_workspace "$WS_ORGANIZATION" "$WS_WORKSPACE")
echo "    workspace is $(is_ok $?)"

#echo "----"
#
# Clone GitHub Project Repository when repo is not found
#

echo "* Clone GitHub Project"
echo "    url      : https://github.com/${GH_USER}/${GH_PROJECT}.git"
echo "    workspace: ${HOME}/Development/${WS_ORGANIZATION}/${WS_WORKSPACE}"
echo "    project  :   ${HOME}/Development/${WS_ORGANIZATION}/${WS_WORKSPACE}/${GH_PROJECT}"
rc=$(clone_project "$WS_ORGANIZATION" "$WS_WORKSPACE" "$GH_PROJECT" "$GH_USER")
echo "    clone is $(is_ok $?)"

# Stage files...add . when current branch is not main
#
echo "* Stage Files when current branch is not main"
echo "    current branch: $(get_branch_current)"
rc=$(stage_branch_current)
echo "    $GH_PROJECT staging: $(is_ok $?)"

#
# Commit branch when current branch is not main
#
echo "* Commit branch when current branch is not main"
echo "    current branch: $(get_branch_current)"
rc=$(commit_branch_current "$GH_MESSAGE")
echo "    $GH_PROJECT commit: $(is_ok $?)"

# Create branch when it doesnt exist
echo "* Create branch when it doesnt exist"
echo "    branch $GH_BRANCH exists: $(has_branch $GH_BRANCH)"
rc=$(create_branch "$GH_BRANCH")
echo "    branch: $(is_ok $?)"

#
# Checkout branch when current branch is main
#
echo "* Checkout branch when current branch is main"
rc=$(checkout_branch "$GH_BRANCH")
echo "    checked out $GH_BRANCH: $(is_ok $?)"

git status
exit


#
# Rebase when current branch has changes
#                            and is not main

# Push branch when branch has committed changes


# Open GitHub

#git status