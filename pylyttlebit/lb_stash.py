from pprint import pprint
from lb_constants import LbC
from script_lb_defaults import LbDefaults
class LbStash(dict):
    # eg {project:{folder: 'TBD', repo_url: 'TBD' },
    #     process:[],
    #     prompts:{'GH_BRANCH': '00_init',
    #              'GH_PROJECT': 'pylyttlebit',
    #              'GH_USER': 'wilfongjt',
    #              'WS_ORGANIZATION': 'lyttlebit',
    #              'WS_WORKSPACE': '00_lyttlebit'}}
    def __init__(self):
        #self[LbC().INVALID_KEY]=[]
        self[LbC().PROJECT_KEY]={'folder': 'TBD',
                                 'repo_url': 'TBD'}

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
    #def setPrompts(self, key, value):
    #    if key in self[LbC().PROJECT_KEY]:
    #        self[LbC().PROJECT_KEY][key]=value
    #    return self

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

        #self.validate()
        #if len(self[LbC().INVALID_KEY]):
        #    print('B')
        #    return False
        #print('C')
        return True
    '''
     def isValid(self):
        if not LbC().INVALID_KEY in self:
            print('A')
            return False
        #self.validate()
        if len(self[LbC().INVALID_KEY]):
            print('B')
            return False
        print('C')
        return True
    '''

def main():
    from pprint import pprint
    actual = LbStash()
    pprint(actual)

    assert (actual.isValid())
    actual.validate()

    pprint(actual)

    assert (not actual.isValid())
    actual.getProject()


if __name__ == "__main__":
    # execute only if run as a script
    main()
    # unittest.main()