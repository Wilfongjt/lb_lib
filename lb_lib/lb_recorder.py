import typing
from typing import TypeVar

Self = TypeVar("Self", bound="Recorder")

class LbRecorder():
    def __init__(self) -> None:
        self.msg = ' '
        self.msgcnt = 1

    def hello_world(self):
        print("I am LbRecorder!")

    def getClassName(self) -> str:
        return self.__class__.__name__

    def addStep(self, msg, arrow='->') -> Self:
        msg = msg.replace(arrow, '').strip()
        if self.msgcnt == 1:
            r = '{} {}'.format(arrow, msg)
        else:
            r = '{} {} ({})'.format(arrow, msg, self.msgcnt)
        # if not self.msg.strip().endswith(msg.strip()):
        if not self.msg.strip().endswith(r):
            self.msg += ' {} {}'.format(arrow, msg.strip())
            self.msgcnt = 1
        else:
            self.msgcnt += 1
            w = '{} {} ({})'.format(arrow, msg, self.msgcnt)
            # print('   ',self.msg)
            # print('***** replace "{}" with "{}"'.format(r, w))
            self.msg = self.msg.replace(r, w)
            # print('   ',self.msg)
        return self

    def getSteps(self) -> str:
        return '    {}'.format(self.msg)

    def showSteps(self, terminalMsg: str = None) -> str:
        if terminalMsg:
            print('    {}: {} {}'.format(self.getSteps(), terminalMsg, self.getClassName()) )
        else:
            print('    {}: {}'.format(self.getSteps(), self.getClassName()))

        self.msg = ' '

        return self


def main():

    actual = LbRecorder()
    #print('Recorder actual ', type(actual))
    assert(actual)
    assert(type(actual) is LbRecorder)
    assert(actual.msg == ' ')
    assert(actual.msgcnt == 1)

    actual = LbRecorder().addStep('SayHey')
    #print('Recorder actual "{}"'.format(actual.getSteps()))

    assert(actual)
    assert(type(actual) is LbRecorder)
    assert(actual.msg == '  -> SayHey')
    assert(actual.msgcnt == 1)
    assert(actual.getSteps() == '      -> SayHey' )
    actual.addStep('again')
    #print('Recorder actual ', actual.getSteps())
    assert(actual.getSteps() == '      -> SayHey -> again' )
    actual.addStep('again')
    #print('Recorder actual ', actual.getSteps())
    actual.showSteps('somefilename')

if __name__ == "__main__":
    # execute only if run as a script
    main()