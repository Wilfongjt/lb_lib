import os
import sys
from lb_util import LbUtil
class GitScript():
    def __init__(self):
        self.fail = False
        self.fail_msg = None
        self.env = {
            "env_folder_name": os.getcwd(),
            "env_file_name": ".env"
        }

    def assertTrue(self, expression):
        assert (expression == True)
        return self

    def setFail(self, tf, msg=None):
        #### Generalize Fail
        self.fail = tf
        self.fail_msg = msg
        return self

    def showTitle(self, title):
        print('title: {}'.format(title))
        return self

    def get(self, key):
        if key not in self.env:
            self.setFail(True, '{} Not Found'.format(key))
            raise Exception('{} Not Found'.format(key))
        return self.env[key]

    def set(self, key, value):
        self.env[key] = value
        return self

    #def create_env(self, key, value="TBD"):
    def set_env(self, key, value="TBD"):

        line_list = []

        ##* open file and read text lines
        env_file_name=self.get('env_file_name')
        env_folder_name=self.get('env_folder_name')
        if LbUtil().file_exists(env_folder_name, env_file_name):
            with open('{}/{}'.format(env_folder_name, env_file_name)) as file:
                line_list = file.readlines()
                line_list = [ln.replace('\n', '') for ln in line_list]
        ##* find "key=" then replace with "key=value"
        i=0
        found=False
        for ln in line_list:
            if ln.startswith('{}='.format(key)):
                line_list[i]='{}={}'.format(key,value)
                found = True
                break
            i+=1
        ##* key not found then append

        if not found:
            line_list.append('{}={}'.format(key,value))

        ## save after every set
        print('env_folder_name',env_folder_name)
        print('env_file_name  ',env_file_name)
        with open('{}/{}'.format(env_folder_name, env_file_name), 'w') as f:
            f.writelines(['{}\n'.format(ln) for ln in line_list])

        # #* create environment file when it doesnt exist
        #if LbUtil().folder_exists(self.get('env_folder_name'), self.get('env_file_name')):
        #    return self
        #rc =$(add_env_variable "$file_name" "WS_ORGANIZATION" "TBD")
        #rc =$(add_env_variable "$file_name" "WS_WORKSPACE" "TBD")
        #rc =$(add_env_variable "$file_name" "GH_PROJECT" "TBD")
        #rc =$(add_env_variable "$file_name" "GH_USER" "TBD")
        #rc =$(add_env_variable "$file_name" "GH_BRANCH" "TBD")
        return self

    '''
    function create_env() {
    if [ $# -ne 1 ]; then
        echo "Usage: create_env <file_name> "
        return 1
    fi
    local file_name=$1
    local rc=0
    # create file when doesnt exist
    if test -f "$file_name"; then
        echo "    $file_name exists."
    else
        echo "# environment" > "$file_name"
        rc=$(add_env_variable "$file_name" "WS_ORGANIZATION" "TBD")
        rc=$(add_env_variable "$file_name" "WS_WORKSPACE" "TBD")
        rc=$(add_env_variable "$file_name" "GH_PROJECT" "TBD")
        rc=$(add_env_variable "$file_name" "GH_USER" "TBD")
        rc=$(add_env_variable "$file_name" "GH_BRANCH" "TBD")
    fi

    return 0
};   #echo $(create_env);
#
    '''

    def export(self, var_name, value):
        return self

    def validateInputs(self, prefix=['WS_', 'GH_']):
        ## fail when inputs are invalid
        return self

    def onFailExit(self):
        if self.fail:
            print('failed with "{}"'.format(self.fail_msg))
            sys.exit(1)
        return self
def main():
    from pprint import pprint

    actual = GitScript()
    assert (actual)
    assert (actual.onFailExit()) # should be ok
    pprint(actual.env)
    actual.set('env_file_name', 'git.script.env')
    actual.set_env('TEST','TBD')
    actual.set_env('TEST2','TBD')
    actual.set_env('TEST2','XXXX')


if __name__ == "__main__":
    # execute as script
    main()