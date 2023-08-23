from lb_text_file import LbTextFile
from lb_constants import LbC
from lb_util import LbUtil

class LbRebaseScript(LbTextFile):
    def __init__(self):
        super().__init__()
        #### create a rebase script file
        ##* create scripts folder when doesnt exist
        self.setFilename(LbC().REBASE_SCRIPT_FILENAME)
        #self.setFolder()

    def create(self):
        ##* create scripts folder
        if not self.getFolder():
            raise Exception('Unknown folder in LbRebaseScript.create')
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
        
        # open _bk.config and load variables
        set -o allexport
        source .env set
        set +o allexport
        
        # show env
        #env
        
        # goto project folder
        cd ..
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
        
        cd ..
        ls
        
        # source ./config.sh
        #source ../../git.config.sh
        
        export MY_TRUNK=${GIT_TRUNK}
        export MY_BRANCH=${GIT_BRANCH}
        export MY_APPNAME=${GIT_PROJECT}
        export MY_PREFIX=${GIT_PREFIX}
        export MY_GIT_OWNERNAME=${GIT_OWNERNAME}
        export MY_GIT_PROJECT=${GIT_PROJECT}
        # export MY_DATA_FOLDER=~/.data/aad_db
        # Prerequisites:
        #   1. have a cloned repo
        #   2. Open a command window
        #   3. create a config.sh file
        
        # get a commit message
        
        export MY_GIT_PROJECT=$(get_input "Git.Project.Name" "${MY_GIT_PROJECT}")
        export MY_TRUNK=$(get_input "Git.Trunc.Name" "${MY_TRUNK}")
        export MY_BRANCH=$(get_input "Your.Branch.Name" "${MY_BRANCH}")
        export COMMIT_MSG=$(get_input "Commit.Message" "${MY_BRANCH}")
        export PUSH=N
        export CONT=N
        export CONT=$(get_input "Continue?" "${CONT}")
        
        if [ ${CONT} = "N" ]; then
          echo "Stopping."
          exit 0
        fi
        echo "Continuing"
        ls
        
        cd ${MY_GIT_PROJECT}/           
        git checkout ${MY_BRANCH}
                                        
        git add .
        git commit -m "${COMMIT_MSG}"
                                      
        git checkout ${MY_TRUNK} 
        echo "----"
        git pull origin ${MY_TRUNK}    
        git checkout ${MY_BRANCH}
        git branch
        echo "-- rebase"
        git rebase ${MY_BRANCH}
                                                   
        export PUSH=$(get_input "PUSH?" "${PUSH}")
        
        if [ ${PUSH} = "N" ]; then
          echo "Remember to Push later."
          exit 0
        fi
        echo "-- pushing"
        git push origin "${MY_BRANCH}"

        open -a safari "https://github.com/${MY_GIT_OWNERNAME}/${MY_GIT_PROJECT}"
        
        git status
        
        # open a browser for convenience
        '''
        return [ln.replace('        ', '') for ln in rc.split('\n')]
def main():
    from pprint import pprint
    script_folder = '{}/scripts'.format('/'.join(str(__file__).split('/')[0:-2]))
    print('script_folder', script_folder)
    actual = LbRebaseScript().setFolder(script_folder).create().save()
    #print('actual.getStartText()', actual.getStartText())
    # pprint(actual.getStartText())
    print('folder', actual.getFolder())
    print('filename', actual.getFilename())
    #pprint(actual)
    assert (actual != [])

if __name__ == "__main__":
    # execute only if run as a script
    main()
    # unittest.main()

