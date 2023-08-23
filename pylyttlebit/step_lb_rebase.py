import os
from pprint import pprint
from pylyttlebit.lb_step import LbStep
from pylyttlebit.lb_constants import LbC
from pylyttlebit.lb_project import LbProject

class LbRebase(LbStep):
    def __init__(self, stash):
        super().__init__()
        self.verbose = False
        self.setStash(stash)

    def depisValid(self):
        ####
        if LbC().INVALID_KEY in self.getStash():
            return False
        return True

    def process(self):
        super().process()

        #### Rebase Project

        print('')
        print('process Rebase')
        # pprint(self.getStash())
        print('source', self.getStash())

        ##* Stop when invalid

        if not self.getStash().isValid():
            pprint(self.getStash())
            print('Terminate Rebase due to invalid settings!')
            exit(0)

        prompts = self.getStash(LbC().PROMPTS_KEY)

        # cd ${MY_GIT_PROJECT}/

        ##* Change folder to project folder

        last_dir = os.getcwd()  # save for switching back later

        project_folder = self.getStash(LbC().PROJECT_KEY)[LbC().PROJECT_FOLDER_KEY]
        print('project_folder', project_folder)
        os.chdir(project_folder)
        command = 'ls'
        os.system(command)

        ##*  Checkout branch ... git checkout ${MY_BRANCH}

        command = 'git checkout {}'.format(prompts[LbC().GH_BRANCH_KEY])
        print('git checkout ... ', command)
        os.system(command)

        ##* Add files to git  ... git add .

        command = 'git add .'
        print('git add .  .................... ', command)
        os.system('git add .')

        ##* Ask User for GitHub Message

        print('prompts', prompts)
        if LbC().GH_MESSAGE_KEY not in prompts:
            prompts[LbC().GH_MESSAGE_KEY] = LbProject().prompt(LbC().GH_MESSAGE_KEY
                                                     , LbProject().get_env_value(LbC().GH_MESSAGE_KEY)
                                                     , hardstop=True)

        ##* Commit with <MESSAGE> ... git commit -m "${COMMIT_MSG}"

        command = 'git commit -m {}'.format(prompts['GH_MESSAGE'])
        print('Commit with <MESSAGE> ......... ', command)
        os.system(command)

        ##* Checkout main branch ... git checkout ${MY_TRUNK}

        command = 'git checkout main'
        print('git checkout main ............. ', command)
        os.system(command)

        ##* Pull origin main ... git pull origin ${MY_TRUNK}

        command = 'git pull origin main'
        print('git pull origin ${MY_TRUNK} ... ', command)
        os.system(command)

        ##* Checkout branch ... git checkout ${MY_BRANCH}

        command = 'git checkout {}'.format(prompts[LbC().GH_BRANCH_KEY])
        print('git checkout <GH_BRANCH> ...... ', command)
        os.system(command)

        # feedback
        # git branch
        command = 'git branch'
        print('git branch .................... ', command)
        os.system(command)

        ##* Rebase repo ... git rebase ${MY_BRANCH}

        command = 'git rebase {}'.format(prompts[LbC().GH_BRANCH_KEY])
        print('git rebase <GH_BRANCH_KEY> .... ', command)
        # os.system(command)

        ##* Push to origin

        if LbProject().prompt('PUSH?', 'N') not in ['N', 'n']:
            command = 'git push origin {}'.format(prompts[LbC().GH_BRANCH_KEY])
            print('git push origin <GH_BRANCH_KEY>')
            #os.system(command)

        ##* Reset folder

        os.chdir(project_folder)

        return self

def main():
    from pprint import pprint
    from lb_stash import LocalStash
    # rebase this project
    from pylyttlebit.lb_stash import LbStash
    stash = LocalStash()
    #path = '/'.join(str(__file__).split('/')[0:-1])
    # configure for local rebase
    #stash.setFromPath(path)
    pprint(stash)
    actual = LbRebase(stash)
    actual.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()
    #unittest.main()