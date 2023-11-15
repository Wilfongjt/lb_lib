import os
from source.lb_template import LbTemplate

class ServerMainJs(LbTemplate):
    def __init__(self):
        super().__init__()
        ##* initialize filename with 'server.js'
        self.filetype = 'js'
        self.setFilename('server.js')

    def get_template_string(self):

        rc = '''
        // 'use strict';
        // generated from <project-name>

        const { start } = require('./lib/server');

        start();
        '''
        rc = rc.split('\n')
        rc = [ln.replace('        ', '    ') for ln in rc]
        return '\n'.join(rc)
            #.replace('${project_name}', self.getProjectName())
def main():
    temp_api = 'test_api'
    temp_folder = '{}/Development/{}'.format(os.environ['HOME'],temp_api)
    merge_list=[{'name': '<project-name>', 'value': 'test_api'}, {'name':'<gh-user>', 'value':'jw'}]
    print('temp_folder', temp_folder)
    actual = ServerMainJs().setFolder(temp_folder, create=True).merge(merge_list).create(overwrite=True)

if __name__ == "__main__":
    # execute as script
    main()