
import unittest
from typing import TypeVar

Self = TypeVar("Self", bound="Recorder")

class LbRecorder():
    ## Ad Hoc Record of method calls
    def __init__(self) -> None:
        #print('lbRecorder')
        self.step_list = []
        #self.key = ' '
        #self.msgcnt = 1

    def hello_world(self):
        print("I am LbRecorder!")
        return self

    def getClassName(self) -> str:
        ##__Get Class Name on request__
        ##* returns current class name
        return self.__class__.__name__
    def addStep(self, msg, arrow='->'):
        ##* no arrow on first step

        if len(self.step_list) > 0:
            ##* arrow goes before step
            msg = '{} {}'.format(arrow, msg)
        else:
            msg = '[*] -> {}'.format(msg)
        #msg = msg.replace(arrow, '').strip()
        self.step_list.append(msg)
        #print('addStep ', self.step_list)
        return self

    '''
        def addStep(self, msg, arrow='->'):
        msg = msg.replace(arrow, '').strip()
        self.step_list.append(msg)
        #print('addStep ', self.step_list)
        return self
    '''
    def getSteps(self):
        ##__Format Steps on request, eg "one -> two (2)__"
        steps = []
        last_step = None
        cnt = 1
        for s in self.step_list:
            if len(steps) == 0:
                ##* append first step
                steps.append(s)
            else:

                if steps[-1].startswith(s):
                    ##* show count on step message when message repeats
                    cnt += 1
                    steps[-1] = '{} ({})'.format(s, cnt)
                    #steps[-1] = '{} ({})'.format(s, cnt)

                else:
                    ##* add step message
                    cnt = 1
                    steps.append('{}'.format(s))
                    #steps.append('{}'.format(s))
        steps.append(self.getClassName())
        ##* seperate step messages with "->"
        #return ' \n    | \n'.join(['   {}'.format(s) for s in steps])

        return ' '.join(steps)

    '''
        def getSteps(self):
        ##__Format Steps on request, eg "one -> two (2)__"
        steps = []
        last_step = None
        cnt = 1
        for s in self.step_list:
            if len(steps) == 0:
                ##* append first step
                steps.append(s)
            else:

                if steps[-1].startswith(s):
                    ##* show count on step message when message repeats
                    cnt += 1
                    steps[-1] = '{} ({})'.format(s, cnt)
                    #steps[-1] = '{} ({})'.format(s, cnt)

                else:
                    ##* add step message
                    cnt = 1
                    steps.append('{}'.format(s))
                    #steps.append('{}'.format(s))
        steps.append(self.getClassName())
        ##* seperate step messages with "->"
        #return ' \n    | \n'.join(['   {}'.format(s) for s in steps])

        return ' -> '.join(steps)
    '''
    def deppreview(self, terminalMsg: str = None) -> str:
        ##__Show Steps on request__
        if terminalMsg:
            ##* Show preview of Steps
            print('{}: {} {}'.format(self.getSteps(), terminalMsg, self.getClassName()) )
            #print('    {}: {} {}'.format(self.getSteps(), terminalMsg, self.getClassName()) )
        else:
            print('{}: {}'.format(self.getSteps(), self.getClassName()))
            #print('    {}: {}'.format(self.getSteps(), self.getClassName()))

        self.msg = ' '

        return self

    def formulate(self, form, title=None):
        ##__Convert Object to String__
        ##* eg {a:1, b:2} to (a, b)
        keys = []
        for key in form:
            keys.append(key)
        if title:
            return '({}({}))'.format(title, ','.join(keys))

        return '({})'.format(','.join(keys))
def main():
    # dev
    print('lb_recorder')
    actual = LbRecorder()
    actual.addStep('aaa')
    actual.addStep('bbb', arrow='; [*] ->')
    actual.addStep('ccc')
    print('step', actual.getSteps())
    #actual.preview('preview')

def main_document():
    from dep.pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_recorder')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()


if __name__ == "__main__":
    from tests.lb_recorder_test import LbRecorder
    # execute only if run as a script
    main()
    unittest.main()
