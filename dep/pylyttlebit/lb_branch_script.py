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
        # source
        function get_input() {
            if [ $# -ne 2 ]; then
                echo "Usage: get_input <prompt> <default>"
                return 1
            fi
        }
        function get_current_branch() {}
        function has_repo() {}
        function has_changes() {}
        function clone_repo() {}
        function initialize_env() {}
        function create_branch() {}
        function replace_line_in_file() {}
        function rebase_branch() {}
        
        # script
        # clone when .git not found
                
        # initalize .env with WS_ORGANIZATION=TBD when .env is not found
        # initalize .env with WS_WORKSPACE=TBD when .env is not found
        # initalize .env with GH_USER=TBD when .env is not found
        # initalize .env with GH_PROJECT=TBD when .env is not found
        # initalize .env with GH_BRANCH=TBD when .env is not found
        
        # stop when current branch is main
        # stop when current branch is not equal to GH_BRANCH
        
        # stop when GH_BRANCH = TBD
        
        # rebase when 
        
        '''
    def depgetStartText(self):
        rc = '''
        #!/bin/bash
        function get_input()
        {
            if [ $# -ne 2 ]; then
                echo "Usage: get_input <prompt> <default>"
                return 1
            fi
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
              echo "# $line" >> temp.env
              echo $replacement_line >> temp.env
            else
              echo "$line" >> temp.env
            fi
        
          done < "$filename"
          # replace original .env with new temp.env
          cp "temp.env" "$filename"
          # delete the temporary file
          rm "temp.env"
        }


        # open .env and load variables
        set -o allexport
        source .env set
        set +o allexport
        
        export GH_TRUNK=main
        
        # show env
        env
        echo 'A'
        # goto bin folder
        cd ..
        ls
        
        echo 'B'
        
        # never allow a commit to main branch
        
        if [ $(current_git_branch) = ${GH_TRUNK} ]; then
            echo "ProjectScript wont commit changes to main branch ${GH_TRUNK}"
            exit
        fi
        
        echo 'C'
        # check for expected branch ie GH_BRANCH must match current branch
        
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
        
        # update .env with GH_BRANCH=NEXT_BRANCH
        echo ls
        echo $(replaceLineInFile ".env" "GH_BRANCH=${GH_BRANCH}" "GH_BRANCH=${NEXT_BRANCH}")
        export GH_BRANCH=${NEXT_BRANCH}
        
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

        # goto bin folder
        cd ..
        ls
        
        # commit 
        # git checkout <new branch>

        # confirm values
        export GH_TRUNK=main        
        export WS_ORGANIZATION=$(get_input "ws.organization" "${WS_ORGANIZATION}")
        export WS_WORKSPACE=$(get_input "ws.workspace" "${WS_WORKSPACE}")
        export GH_USER=$(get_input "gh.user" "${GH_USER}")
        export GH_PROJECT=$(get_input "gh.bin" "${GH_PROJECT}")
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
    # outputs to the local bin
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

    print('executue in terminal')

if __name__ == "__main__":
    # execute only if run as a script
    main()
    # unittest.main()

