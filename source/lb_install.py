import os
import re

from source.utility_script import UtilityScript
from source.lb_util import LbUtil
#from source.template.template_stub import StubTemplate
from source.lb_template import LbTemplate
from source.lb_folders import LbTemplateFolder,LbProjectFolder,ScriptsFolderTemplate

class LbInstall(UtilityScript):
    def __init__(self):
        super().__init__()
        self.data = [] #nv_list
        self.templates = []

    def assertTrue(self, tf):
        assert(tf)
        return self

    def get_templates(self):
        return self.templates

    def add_template(self, tmpl):
        self.addStep('add({})'.format(tmpl.getClassName()))

        tmpl.set_data(self.get_data())

        self.templates.append(tmpl)
        return self

    #def create(self):
    #    self.addStep('create')
    #    return self

    def get_template_folder(self, context=None):
        ##* get the local folder
        f_str = os.getcwd()
        offset = 4
        if context: cntxt = context.split('/')
        # print('context', cntxt)
        f_str = f_str.split('/')
        f_str = f_str[0:f_str.index('Development') + offset]
        f_str.append('source')
        f_str.append('template')
        if context: f_str.extend(cntxt)
        f_str = '/'.join(f_str)
        return f_str
    #def get_template_name_values(self):
    def get_data(self):
        #### Keep a list of name and value pairs
        #Convert all install keys to template name and value pairs
        ##* push into each template
        #rc = [{'name': '<<{}>>'.format(n), 'value': self[n]} for n in self]
        #return rc
        return self.data

    #def merge(self):
    #    self.addStep('merge')
    #    return self

    def run(self):
        self.addStep('run')
        for tmpl in self.get_templates():

            self.addStep('template({})'.format(tmpl.getClassName()))
            print('tmpl', tmpl.getClassName())
            tmpl.process()

        return self

    def set(self, key, value):
        super().set(key,value)
        self.addStep('set({},{})'.format(key, value))
        #### set name and value pairs

        ##* push
        ##* update the template name name and value pairs
        nvkey='<<{}>>'.format(key)
        found=False
        for nv in self.data:
            if nvkey in nv:
                nv[nvkey]=value
                found = True
        ##* name not found then add
        if not found:
            #print('nvkey',nvkey)
            self.data.append({'name': nvkey, 'value': value})

        ##* all upper case keys go into environment
        pattern = re.compile(r'^[A-Z]{2}_[A-Z_]+$')
        if pattern.match(key):
            os.environ[key]=value
        return self

    def show(self):
        print(self.getClassName())
        #super().show()
        print('  steps :')
        print('        ', self.getSteps())
        print('  actual: ')
        print('          ', (str(self)))
        print('  template-keys:')
        print('          ',(str(self.get_data())))
        #print('  template-keys: {}'.format(self.get_template_name_values()))
        if not self.templates:
            print('      templates: none')
        else:
            for tmpl in self.templates:
                tmpl.show()
        return self

    '''
    def templatize(self):
        self.addStep('templatize')
        for tmpl in self.templates:
            tmpl.setFolder(self.get_folder())\
                .merge(self.get_name_values())\
                .validate()\
                .create()\
                .open()\
                .save()

        return self
    
    def validate(self):
        self.addStep('validate')
        ## validate templates
        #for tmpl in self.templates:
        #    tmpl.validate()

        return self

    def save(self):
        for tmpl in self.templates:
            tmpl.save()
        return self
    '''
def main():
    import datetime
    from source.lb_folders import WorkspaceFolderTemplate
    from source.lb_folders import GitProjectFolderTemplate
    from source.lb_folders import ScriptsFolderTemplate

    #tmpl_folder = LbTemplateFolder('bash')
    print('1 cwd', os.getcwd())
    # the pattern <<*>> is a template name
    #nv_data = [{'name': '<<WS_ORGANIZATION>>', 'value': 'myinstall'}]
    actual = LbInstall()\
        .set('WS_ORGANIZATION','temp-org')\
        .set('WS_WORKSPACE','temp-ws')\
        .set('GH_PROJECT','py_test')\
        .set('GH_USER','wilfongjt')\
        .set('date-time', str(datetime.datetime.now()))\
        .set("POSTGRES_DB", 'TBD')

    print('Install get_template_folder', actual.get_template_folder())
    nv_list = actual.get_data()
    # Folder Templates
    actual.add_template(WorkspaceFolderTemplate(nv_list))
    actual.add_template(GitProjectFolderTemplate(nv_list))
    #script_folder = ScriptsFolderTemplate(nv_list)
    #print('tmpl_folder',LbTemplateFolder('bash'))
    #print('script_folder', script_folder)
    actual.add_template(ScriptsFolderTemplate(nv_list))
    # Document Templates
    #print('GitProjectFolderTemplate(nv_list)', GitProjectFolderTemplate(nv_list))

    # BASH
    actual.add_template(LbTemplate()
                        .set_context('bash')
                        .set_data(nv_list)
                        .setFolder(ScriptsFolderTemplate(nv_list))
                        .setFilename('bk.sh')
                        .validate())

    actual.add_template(LbTemplate()
                        .set_context('bash')
                        .set_data(nv_list)
                        .setFolder(ScriptsFolderTemplate(nv_list))
                        .setFilename('documentation.sh')
                        .validate())

    actual.add_template(LbTemplate()
                        .set_context('bash')
                        .set_data(nv_list)
                        .setFolder(ScriptsFolderTemplate(nv_list))
                        .setFilename('functions.sh')
                        .validate())

    actual.add_template(LbTemplate()
                        .set_context('bash')
                        .set_data(nv_list)
                        .setFolder(ScriptsFolderTemplate(nv_list))
                        .setFilename('git.branch.sh')
                        .validate())

    actual.add_template(LbTemplate()
                        .set_context('bash')
                        .set_data(nv_list)
                        .setFolder(ScriptsFolderTemplate(nv_list))
                        .setFilename('git.issues.sh')
                        .validate())

    actual.add_template(LbTemplate()
                        .set_context('bash')
                        .set_data(nv_list)
                        .setFolder(ScriptsFolderTemplate(nv_list))
                        .setFilename('git.rebase.sh')
                        .validate())

    actual.add_template(LbTemplate()
                        .set_context('bash')
                        .set_data(nv_list)
                        .setFolder(ScriptsFolderTemplate(nv_list))
                        .setFilename('tests.sh')
                        .validate())
    # DOCKER
    actual.add_template(LbTemplate()
                        .set_context('docker')
                        .set_data(nv_list)
                        .setFolder(GitProjectFolderTemplate(nv_list))
                        .setFilename('Dockerfile')
                        .validate())

    actual.add_template(LbTemplate()
                        .set_context('docker')
                        .set_data(nv_list)
                        .setFolder(GitProjectFolderTemplate(nv_list))
                        .setFilename('docker-compose.yml')
                        .validate())
    # ENV
    # env, write a first draft of the .env file

    '''
    .set("POSTGRES_DB", 'TBD')
    .set("POSTGRES_USER", "TBD")
    .set("POSTGRES_PASSWORD", "TBD")
    .set("POSTGRES_JWT_SECRET", "TBD")
    .set("POSTGRES_API_PASSWORD", "TBD")
    .set("POSTGRES_JWT_CLAIMS", "TBD")
    .set("NODE_ENV", "TBD")
    .set("HOST", "TBD")
    .set("PORT", "TBD")
    .set("DATABASE_URL", "TBD")
    .set("API_TOKEN", "TBD")
    .set("JWT_SECRET", "TBD")
    .set("JWT_CLAIMS", "TBD")
    .set("ACCEPTED_ORIGINS", "TBD")
    .set("HEROKU_API_KEY", "TBD")
    '''

    actual.add_template(LbEnvTemplate()
                        .set_context('env')
                        .set_data(nv_list)
                        .setFolder(GitProjectFolderTemplate(nv_list))
                        .setFilename('.env')
                        .validate()
                        )

    print('2 cwd', os.getcwd())

    actual.run()
    print('3 cwd', os.getcwd())

    actual.show()
    #actual.show()
    #actual.assertTrue('fail' in actual)
    #actual.assertTrue('fail_msg' in actual)
    actual.assertTrue('WS_ORGANIZATION' in actual)

    #actual.assertTrue(actual.get_data() == [{'name': '<<WS_ORGANIZATION>>', 'value': 'temp-org'}])

    #.assertTrue(actual == {'fail': False, 'fail_msg': []})

if __name__ == "__main__":
    # execute only if run as a script
    main()
