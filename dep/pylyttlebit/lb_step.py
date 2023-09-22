from lb_recorder import LbRecorder


class LbStep(LbRecorder):
    def __init__(self):
        LbRecorder.__init__(self)
        self.id = 0
        self.name = None
        self.prev = None
        self.next = None
        self.stash = {} # consolidation of step data
        self.verbose = False
        self.test = False
        self.parent = None

    def hello_world(self):
        print("I am LbStep!")
        return self
    def setParent(self, parent):
        self.parent = parent
        return self
    def getParent(self):
        return self.parent

    def depsetInvalid(self, key, msg):
        #self.addStep('invalid')
        #print('key', key)
        #print('msg', msg)
        if 'invalid' not in self.stash:
            self.stash['invalid']={}
        if key not in self.stash['invalid']:
            self.stash['invalid'][key]=[]

        #print(self.lb_stash)

        self.stash['invalid'][key].append(msg)
        return self

    def depsetInvalid(self, key):
        self.addStep('invalid')
        if 'invalid' not in self.stash:
            self.stash['invalid'] = []
        self.stash['invalid'].append(key)
        return self
    def depgetInvalid(self):
        #self.addStep('getInvalid')
        if 'invalid' not in self.stash:
            return ['No Exceptions']
        return self.stash['invalid']

    #def isValid(self):
        ####
    #    if LbC().INVALID_KEY in self.getStash():
    #        return False
    #    return True

    def setFailure(self, msg):
        self.addStep('failure')
        if 'failed' not in self.stash:
            self.stash['failed']=[]
        self.stash['failed'].append(msg)
        return self
    def getFailure(self):
        #self.addStep('getFailure')
        if 'failed' not in self.stash:
            return ['No Exceptions']
        return self.stash['failed']

    def setTest(self, tf):
        self.addStep('test')
        #### set test mode on request
        self.test = tf
        return self

    def isTest(self):
        #self.addStep('isTest')
        #### check the test state on request
        return self.test
    def setVerbose(self,tf):
        self.addStep('verbose')
        #### set verbose feeback state on request
        ##* set verbose to True or False
        self.verbose = tf
        return self

    def isVerbose(self):
        #self.addStep('isVerbose')
        #### check verbose state on request
        ##* returns bool
        return self.verbose

    def getClassName(self) -> str:
        #self.addStep('getClassName')
        ##__Get Class Name on request__
        ##* returns current class name
        return self.__class__.__name__

    def getKey(self):
        #self.addStep('getKey')
        rc = '{}_{}'.format(self.getId(), self.getClassName())
        return rc

    def getStash(self, key=None):
        #self.addStep('lb_stash')
        if key != None:
            #pprint(self.lb_stash)
            #print('key',key)
            return self.stash[key]
        return self.stash

    def setStash(self, stash, key=None):
        self.addStep('(lb_stash)')
        #self.lb_stash = lb_stash
        if key != None:
            self.stash[key] = stash
        else:
            self.stash = stash
        return self

    def getId(self):
        #self.addStep('getId')
        return self.id
    def setId(self,id):
        self.addStep('id')
        self.id = id
        return self

    def getName(self):
        #self.addStep('getName')
        return self.name
    def setName(self, name):
        self.addStep('name')
        self.name = name
        return self

    def getNext(self):
        #self.addStep('getNext')
        return self.next
    def setNext(self, nxt):
        self.addStep('next')
        self.next = nxt
        return self

    def getPrev(self):
        #self.addStep('getPrev')
        return self.prev
    def setPrev(self, prv):
        self.addStep('prev')
        self.prev = prv
        return self

    def add(self, processStep):
        self.addStep('add')
        #### add Step to Last Step
        processStep.setId(self.getId() + 1)
        if self.getNext():
            self.getNext().add(processStep)
        else:
            self.setNext(processStep)
            processStep.setPrev(self)

        return self

    def process(self):
        #print('key',self.getKey(),'id',self.getId(), 'prev:',self.getPrev(),'self', self, 'next:',self.getNext())
        #self.addStep('process')
        return self

    def run(self):
        #self.addStep('run')
        self.process()
        if self.getNext():
            self.getNext().run()

        return self

def main():

    actual = LbStep().setId(0)
    assert (actual)
    assert (not actual.getNext())
    assert (not actual.getPrev())

    actual.add(LbStep())
    assert(actual.getNext())
    assert(not actual.getPrev())

    actual.add(LbStep())
    assert(actual.getNext())
    assert(not actual.getPrev())

    print('getKey', actual.getKey())
    #print('next', actual.getNext())
    #print('prev', actual.getPrev())
    actual.setFailure('F1').setFailure('F2')
    assert (actual.getStash()['failed'] == ['F1', 'F2'])

    #actual.setInvalid('v1','bad1').setInvalid('v2','bad2')
    #print(actual.getStash()['invalid'])
    #assert (actual.getStash()['invalid'] == {'v1': ['bad1'], 'v2': ['bad2']})
    #assert (actual.getStash()['invalid'] == ['v1', 'v2'])

    actual.run()


def main_document():
    from dep.pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_step')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()


if __name__ == "__main__":
    # execute only if run as a script
    main()
