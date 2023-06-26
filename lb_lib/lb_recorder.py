import re
import typing
from typing import TypeVar

Self = TypeVar("Self", bound="Recorder")

class LbRecorder():
    ## Ad Hoc Record of method calls
    def __init__(self) -> None:
        self.step_list = []
        #self.msg = ' '
        #self.msgcnt = 1

    def hello_world(self):
        print("I am LbRecorder!")
        return self
    def getClassName(self) -> str:
        ##__Get Class Name on request__
        ##* returns current class name
        return self.__class__.__name__
    def addStep(self, msg, arrow='->'):
        msg = msg.replace(arrow, '').strip()
        self.step_list.append(msg)
        #print('addStep ', self.step_list)
        return self

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
                else:
                    ##* add step message
                    cnt = 1
                    steps.append('{}'.format(s))
        ##* seperate step messages with "->"
        return ' -> '.join(steps)

    def preview(self, terminalMsg: str = None) -> str:
        ##__Show Steps on request__
        if terminalMsg:
            ##* Show preview of Steps
            print('    {}: {} {}'.format(self.getSteps(), terminalMsg, self.getClassName()) )
        else:
            print('    {}: {}'.format(self.getSteps(), self.getClassName()))

        self.msg = ' '

        return self


def main():
    import os
    from pprint import pprint
    from lb_lib.lb_doc_comments import LbDocComments

    actual = LbRecorder()
    assert (actual)
    assert (type(actual) is LbRecorder)
    assert (actual.getSteps() == '')

    assert (actual.addStep('one'))
    assert (actual.getSteps() == 'one')

    #print('A',actual.getSteps())

    assert (actual.addStep('two').addStep('two'))
    assert (actual.getSteps() == 'one -> two (2)')
    #print('B',actual.getSteps())

    assert (actual.addStep('three').addStep('three').addStep('three'))
    assert (actual.getSteps() == 'one -> two (2) -> three (3)')
    #print('C', actual.getSteps())

    #assert(actual.msg == ' ')
    #assert(actual.msgcnt == 1)

    #actual = LbRecorder().addStep('SayHey')
    #pprint(actual)
    #print('Recorder actual "{}"'.format(actual.getSteps()))

    #assert(actual)
    #assert(type(actual) is LbRecorder)
    #assert(actual.msg == '  -> SayHey')
    #assert(actual.msgcnt == 1)
    #print(actual.getSteps())
    #assert(actual.getSteps() == '      -> SayHey' )
    #actual.addStep('again')
    #print('Recorder actual ', actual.getSteps())
    #assert(actual.getSteps() == '      -> SayHey -> again' )
    #actual.addStep('again')
    #print('Recorder actual ', actual.getSteps())
    #actual.showSteps('somefilename')

    # write documentation in markdown file
    LbDocComments().setFolder(os.getcwd()).setFilename(str(__file__).split('/')[-1]).open().save()


if __name__ == "__main__":
    # execute only if run as a script
    main()