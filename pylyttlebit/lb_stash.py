import os
from pprint import pprint
from lb_constants import LbC
from script_lb_defaults import LbDefaults
from lb_project import LbProject


class LbStash(dict):
    #### Stash environment variables in memory

    # eg {project:{folder: 'TBD', repo_url: 'TBD' },
    #     process:[],
    #     prompts:{'GH_BRANCH': '00_init',
    #              'GH_PROJECT': 'pylyttlebit',
    #              'GH_USER': 'wilfongjt',
    #              'WS_ORGANIZATION': 'lyttlebit',
    #              'WS_WORKSPACE': '00_lyttlebit'}}
    #

    def __init__(self):
        ##* set stash values to TBD by default

        #self[LbC().INVALID_KEY]=[]
        self[LbC().SOURCE_KEY]= {'folder': '/'.join(str(__file__).split('/')[0:-1])}
        self[LbC().PROJECT_KEY]={'folder': 'TBD',
                                 'repo_url': 'TBD',
                                 'script_folder': 'TBD'}
        self[LbC().PROMPTS_KEY]= LbDefaults()
        self[LbC().PROCESS_KEY]=[]

    def getInvalid(self):
        return self[LbC().INVALID_KEY]

    def setInvalid(self, invalid_str):
        self[LbC().INVALID_KEY].append(invalid_str)

    def getPromptKeys(self):
        keys = []
        for k in self[self[LbC().PROMPTS_KEY]]:
            keys.append(k)
        return keys

    def getPrompts(self, key=None):
        if key:
            return self[LbC().PROMPTS_KEY][key]
        return self[LbC().PROMPTS_KEY]

    def setPrompts(self, prompts):
        self[LbC().PROMPTS_KEY]=prompts
        return self

    def getProject(self, key=None):
        if key:
            #print('key', key)
            #print('PROJECT_KEY', LbC().PROJECT_KEY)
            #pprint(self)
            return self[LbC().PROJECT_KEY][key]
        return self[LbC().PROJECT_KEY]

    def setProject(self, key, value):
        if key in self[LbC().PROJECT_KEY]:
            self[LbC().PROJECT_KEY][key]=value
        return self

    def getProcess(self):
        return self[LbC().PROCESS_KEY]

    def setProcess(self, process_str):
        self[LbC().PROCESS_KEY].append(process_str)
        return self

    def getSource(self, key=None):
        if key:
            return self[LbC().SOURCE_KEY][key]
        return self[LbC().SOURCE_KEY]

    def validate(self, d=None):

        if d == None:
            # revalidate the entire lb_stash
            d = self
            # add or reset invalid:[]
            d[LbC().INVALID_KEY]=[]

        for k, v in d.items():
            # skips arrays
            if isinstance(v, dict):
                self.validate(d=v)
            else:
                #print('k',k, ' v',v)
                if v in LbC().INVALID_VALUES:
                    #self.invalid.append(k)
                    #print('bad k', k)
                    self[LbC().INVALID_KEY].append(k)

        return self

    def isValid(self):
        #print('has invalid', LbC().INVALID_KEY in self)
        #print('has values ',not self[LbC().INVALID_KEY])

        if LbC().INVALID_KEY in self and len(self[LbC().INVALID_KEY]) > 0:
            return False

        return True
    '''
    def setFromPath(self, path):
        #### Set Stash from path on request
        ##< Use when committing pylyttlebit project to git
        #print('setFromPath', path)
        #print(path.split('/'))
        i = 0
        dFound = False
        path = path.split('/')
        d = path.index(LbC().DEV_KEY)
        for k in path:
            if i >= d:
                #if i-d == 0:
                #    print(i - d, 'k development ', k)
                if i-d == 1:
                    ##* set WS_ORGANIZATION from path eg '~/Development/\<organization>'
                    self[LbC().PROMPTS_KEY][LbC().WS_ORGANIZATION_KEY]=k
                elif i-d == 2:
                    ##* set WS_WORKSPACE from path eg '~/Development/\<organization>/\<workspace>'
                    self[LbC().PROMPTS_KEY][LbC().WS_WORKSPACE_KEY]=k
                elif i - d == 3:
                    ##* set GH_PROJECT from path eg '~/Development/\<organization>/\<workspace>/\<project>'
                    self[LbC().PROMPTS_KEY][LbC().GH_PROJECT_KEY]=k
            ##* set GH_BRANCH from '~/Development/\<organization>/\<workspace>/\<project>/.git/HEAD'
            self[LbC().PROMPTS_KEY][LbC().GH_BRANCH_KEY]=LbProject().getBranch()
            i += 1

        ##* set GH_USER to developer's username from '~/.gitconfig'
        self[LbC().PROMPTS_KEY][LbC().GH_USER_KEY] = LbProject().getGHUser()

        ##* set project folder
        self[LbC().PROJECT_KEY][LbC().PROJECT_FOLDER_KEY]='/'.join(str(os.getcwd()).split('/')[0:-1])
        ##* set repo url
        self[LbC().PROJECT_KEY][LbC().REPO_URL_KEY]=LbC().GIT_URL_TEMPLATE.format(LbProject().getGHUser(),self[LbC().PROMPTS_KEY][LbC().GH_PROJECT_KEY])

        return self
        '''

class LocalStash(LbStash):
    def __init__(self):
        super().__init__()

        path = '/'.join(str(__file__).split('/')[0:-1])
        self.setFromPath(path)

    def setFromPath(self, path):
        #### Set Stash from path on request
        ##< Use when committing pylyttlebit project to git
        #print('setFromPath', path)
        #print(path.split('/'))
        i = 0
        dFound = False
        path = path.split('/')
        d = path.index(LbC().DEV_KEY)
        for k in path:
            if i >= d:
                #if i-d == 0:
                #    print(i - d, 'k development ', k)
                if i-d == 1:
                    ##* set WS_ORGANIZATION from path eg '~/Development/\<organization>'
                    self[LbC().PROMPTS_KEY][LbC().WS_ORGANIZATION_KEY]=k
                elif i-d == 2:
                    ##* set WS_WORKSPACE from path eg '~/Development/\<organization>/\<workspace>'
                    self[LbC().PROMPTS_KEY][LbC().WS_WORKSPACE_KEY]=k
                elif i - d == 3:
                    ##* set GH_PROJECT from path eg '~/Development/\<organization>/\<workspace>/\<project>'
                    self[LbC().PROMPTS_KEY][LbC().GH_PROJECT_KEY]=k
            ##* set GH_BRANCH from '~/Development/\<organization>/\<workspace>/\<project>/.git/HEAD'
            self[LbC().PROMPTS_KEY][LbC().GH_BRANCH_KEY]=LbProject().getBranch()
            i += 1

        ##* set GH_USER to developer's username from '~/.gitconfig'
        self[LbC().PROMPTS_KEY][LbC().GH_USER_KEY] = LbProject().getGHUser()

        ##* set project folder
        self[LbC().PROJECT_KEY][LbC().PROJECT_FOLDER_KEY]='/'.join(str(os.getcwd()).split('/')[0:-1])

        ##* set repo url
        self[LbC().PROJECT_KEY][LbC().REPO_URL_KEY]=LbC().REPO_URL_TEMPLATE.format(LbProject().getGHUser(),self[LbC().PROMPTS_KEY][LbC().GH_PROJECT_KEY])

        ##* set script_folder
        self[LbC().PROJECT_KEY][LbC().SCRIPT_FOLDER_KEY] = '{}/scripts'.format('/'.join(str(os.getcwd()).split('/')[0:-1]))


        return self

def main():
    from pprint import pprint

    actual = LbStash()
    pprint(actual)

    assert (actual.isValid())
    actual.validate()

    pprint(actual)

    assert (not actual.isValid())

    #actual.getProject()
    #path = '/'.join(str(__file__).split('/')[0:-1])
    #actual.setFromPath(path)

    print('Local Stash')
    actual = LocalStash()

    pprint(actual)


if __name__ == "__main__":
    # execute only if run as a script
    main()
    # unittest.main()