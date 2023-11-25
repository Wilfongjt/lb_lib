import os
import source.api.hapi.server_js
from source.git_script import LbGitProcess

class HAPIScript(LbGitProcess):
    def __init__(self):
        super().__init__()
        #self.template_keys_and_values = None
    '''
    def getKeyValues(self):
        return self.template_keys_and_values
    
    def setKeyValues(self, template_keys_and_values):
        self.template_keys_and_values=template_keys_and_values
        return self
    '''
    def create_hapi(self, no_yes, template_keys_and_values):
        #print('HAPIScript', self)
        self.addStep('create_hapi')
        if no_yes in ['N']:
            self.addStep('skipped')
            self['api']='skipped'
            return self
        project_folder = self.get_project_folder()
        actual = source.api.hapi.server_js.ServerMainJs()
        actual      .setFolder(project_folder, create=True)\
                    .merge(template_keys_and_values)\
                    .create(overwrite=True)
        #self.addStep('ok')
        return self

def main():
    import os
    temp_api = 'hapi_script'
    temp_folder = '{}/Development/{}'.format(os.environ['HOME'], temp_api)
    template_keys_and_values = [{"name": "<project-name>", "value": temp_api}]

    actual = HAPIScript()
    actual      .set("WS_ORGANIZATION", "hapi")\
                .set("WS_WORKSPACE", "00_hapi")\
                .set("GH_PROJECT", "hapi_script")\
                .print('hapi folders {}'.format(actual.get_project_folder('lib')))\
                .create_folders(actual.get_project_folder('lib'))\
                .create_hapi('Y',template_keys_and_values)\
                .showSteps()

    #print('', source.api.hapi.server_js.ServerMainJs().get_template_key_list())
    #env_list = ["GH_TRUNK", "WS_ORGANIZATION","WS_WORKSPACE","GH_USER","GH_PROJECT","GH_BRANCH","GH_MESSAGE"]
    #for env_title in env_list:
    #    actual.set_env(env_title,actual.get_input(env_title, actual.get_env_value(env_title) or 'TBD', hardstop=False) )

    #actual.create_hapi()
    #actual.setFolder(temp_folder, create=True)

    #print('HapiScript', actual)
    #print('', actual.get_)
    assert(actual)

if __name__ == "__main__":
    # execute as script
    main()