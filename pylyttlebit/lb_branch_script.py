from lb_text_file import LbTextFile
from lb_constants import LbC
from lb_util import LbUtil


class LbBranchScript(LbTextFile):
    def __init__(self):
        super().__init__()
        #### create a rebase script file
        ##* create scripts folder when doesnt exist
        self.setFilename(LbC().BRANCH_SCRIPT_FILENAME)
        # self.setFolder()

    def create(self):
        ##* create scripts folder
        if not self.getFolder():
            raise Exception('Unknown folder in LbBranchScript.create')
        LbUtil().create_folder(self.getFolder())

        self.clear()

        ##* add script
        for ln in self.getStartText():
            if len(ln.lstrip(' ')) > 0:
                self.append(ln)

        return self
    def getStartText(self):
        rc = '''
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
        
        '''
        return [ln.replace('        ', '') for ln in rc.split('\n')]

    def depgetStartText(self):
        rc = '''
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

        # open .env and load variables
        set -o allexport
        source .env set
        set +o allexport

        # show env
        #env

        # goto project folder
        cd ..
        ls
        
        # commit 
        # git checkout <new branch>

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

        open -a safari "https://github.com/${GH_USER}/${GH_PROJECT}"

        # giv user some feedback

        git status

        '''
        return [ln.replace('        ', '') for ln in rc.split('\n')]


def main():
    # outputs to the local project
    from pprint import pprint
    script_folder = '{}/scripts'.format('/'.join(str(__file__).split('/')[0:-2]))
    print('script_folder', script_folder)
    actual = LbBranchScript().setFolder(script_folder).create().save()
    # print('actual.getStartText()', actual.getStartText())
    # pprint(actual.getStartText())
    print('folder', actual.getFolder())
    print('filename', actual.getFilename())
    # pprint(actual)
    assert (actual != [])


if __name__ == "__main__":
    # execute only if run as a script
    main()
    # unittest.main()

