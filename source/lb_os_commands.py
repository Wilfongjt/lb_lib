import os
import sys
from lb_recorder import LbRecorder
from lb_util import LbUtil

class LbOsCommands(LbRecorder):
    def __init__(self):
        super().__init__()
        self.state = {}

    def get_file_list(self, folder):
        rc = LbUtil().get_file_list(folder)
        return rc

    def folder_exists(self, folder):
        #### Test if a given folder exists on request
        ##* folder exists when found on drive ... [x] has test
        exists = os.path.isdir('{}'.format(folder))
        ##* returns bool ... [x] has test
        return exists

    def set(self, key, value):
        self.state[key]=value
        return self

    def get(self, key=None):
        rc = None
        if not key:
            rc = self.state
        elif key in self.state:
            rc = self.state[key]

        return rc

    def ch_dir(self, folder):

        print('A ch_dir', folder)
        self.addStep('ch_dir')
        os.chdir(folder)
        return self

    def makedirs(self, folder):
        os.makedirs(folder, exist_ok=True)
        return self

    def set_fail(self, tf, msg=None):
        #### Generalize Fail
        self.set('fail', tf)
        if 'fail_msg' not in self.get():
            self.set('fail_msg',[])

        if msg: self.get('fail_msg').append(msg.replace('\n',' '))
        return self

    def on_fail_exit(self):
        if 'fail' in self.state and  self.state['fail']:
            self.addStep('failed')
            #self.report()
            # print('fails when "{}"'.format(self['fail_msg']))
            sys.exit(1)
        return self

def main():
    actual = LbOsCommands()
    assert (len(actual.get_file_list(os.getcwd())) > 0 )
    assert (actual.folder_exists(os.getcwd()))
    assert (actual.set('temp','xxx').get('temp') == 'xxx')
    assert (actual.set_fail(True).get('fail')==True)
    assert ('abc' in actual.set_fail(True, 'abc').get('fail_msg'))

    print('actual', actual.get_file_list(os.getcwd()))
    print('actual', actual.get())

if __name__ == "__main__":
    # execute as script
    main()