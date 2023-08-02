'''
    stepA <-> stepB <-> stepC
    prosess[stepA <-> stepB <-> stepC, stepD <-> stepE <-> stepF]
'''
from pylyttlebit.lb_constants import LbC
from pylyttlebit.lb_recorder import LbRecorder
class LbStepList(list, LbRecorder):
    def __init__(self):
        LbRecorder.__init__(self)
        self.stash = {}
        #self.addStep('LubStepList')
    def getClassName(self) -> str:
        ##__Get Class Name on request__
        ##* returns current class name
        return self.__class__.__name__

    def hello_world(self):
        print("I am LbStepList!")
        return self

    def getStash(self, key=None):
        #print('stash', self.stash)
        if key != None:
            return self.stash[key]
        return self.stash

    def setStash(self, stash, key=None):
        #self.stash = stash
        if key != None:
            self.stash[key] = stash
        else:
            self.stash = stash
        return self
    #def setStash(self, stash):
    #    self.stash = stash
    #    return self
    def add(self, processStep):
        self.addStep(processStep.getClassName())
        #### add step to process list
        self.append(processStep)
        return self

    #def process(self):
    #    return self

    def isValid(self):
        # overload me
        return False

    def run(self):
        for step in self:
            step.run()

        return self

def main():
    from pylyttlebit.lb_step import LbStep
    actual = LbStepList()
    print(actual)
    assert (actual == [])   # empty
    actual.run()            # run empty
    actual.add(LbStep())      # add a step
    steps = LbStep().add(LbStep()).add(LbStep())
    actual.add(steps)       # add linked list of steps
    #print('actual', actual)
    actual.run()
    actual.preview('lb_step_list')


def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_step_list')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()


if __name__ == "__main__":
    # execute only if run as a script
    main()
