
import unittest
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
    # dev
    print('lb_recorder')

if __name__ == "__main__":
    from tests.lb_recorder_test import LbRecorder
    # execute only if run as a script
    main()
    unittest.main()
