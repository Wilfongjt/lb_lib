import os
import re

from source.utility_script import UtilityScript
from source.template.template_stub import StubTemplate

class Install(UtilityScript):
    def __init__(self):
        super().__init__()
        self.data = [] #nv_list
        self.templates = []

    def dep_set_name_value_list(self, nv_list):
        self.nv_list
        return self

    def dep_get_name_value_list(self):
        return self.nv_list

    def add_template(self, tmpl):
        self.addStep('template')
        #tmpl.validate()
        #print('install folder', tmpl.getFolder())
        #print('tmpl', tmpl)
        #print('add_template ',self.get_data())
        tmpl.set_data(self.get_data())
        self.templates.append(tmpl)
        return self

    def create(self):

        self.addStep('create')
        #print('    1 create', os.getcwd())

        # self.validate()
        #print('    out create', os.getcwd())

        return self

    #def set_data(self,nv_data):
    #    self.data = nv_data
    #def get_data(self):
    #    return self.data

    def get_folder(self):
        return '{}/Development/Temp'.format(os.environ['HOME'])

    #def get_template_name_values(self):
    def get_data(self):
        #### Keep a list of name and value pairs
        #Convert all install keys to template key and value pairs
        ##* push into each template
        #rc = [{'name': '<<{}>>'.format(n), 'value': self[n]} for n in self]
        #return rc
        return self.data

    def merge(self):
        self.addStep('merge')
        return self

    def run(self):
        self.addStep('run')

        self.merge()

        self.create()

        self.validate()

        self.templatize()

        self.save()
        return self

    def set(self, key, value):
        super().set(key,value)
        #### set name and value pairs

        ##* push
        ##* update the template key name and value pairs
        nvkey='<<{}>>'.format(key)
        found=False
        for nv in self.data:
            if nvkey in nv:
                nv[nvkey]=value
                found = True
        ##* key not found then add
        if not found:
            #print('nvkey',nvkey)
            self.data.append({'name': nvkey, 'value': value})

        ##* all upper case keys go into environment
        pattern = re.compile(r'^[A-Z]{2}_[A-Z_]+$')
        if pattern.match(key):
            os.environ[key]=value
        return self

    def depset(self, key, value="TBD"):
        super().set(key,value)
        self.addStep('set')

        ##* add environment variable when not found
        line_list = []

        ##* find "key=" then replace with "key=value"
        i = 0
        found = False
        for ln in line_list:
            if ln.startswith('{}='.format(key)):
                found = True
                line_list[i] = '{}={}'.format(key, value)
                ##* set stash variable
                super().set(key, value)
                # self.addStep('set_env')
                ##* set envioron variable
                os.environ[key] = value
                break
            i += 1

        ##* key not found then append

        if not found:
            line_list.append('{}={}'.format(key, value))
            ##* set stash variable
            super().set(key, value)
            # self.addStep('set_env-add')
            ##* set envioron variable
            os.environ[key] = value

        return self

    def show(self):
        super().show()
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

    def templatize(self):
        self.addStep('templatize')
        for tmpl in self.templates:
            tmpl.setFolder(self.get_folder())
            tmpl.create() \
                .open() \
                .merge() \
                .save() \
                .validate()

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
    '''

    def validate(self):
        self.addStep('validate')
        ## validate templates
        #for tmpl in self.templates:
        #    tmpl.validate()

        return self

    def dep_validate_templates(self):
        #self.addStep('validate')
        # validate templates
        for tmpl in self.templates:
            tmpl.validate()

        return self
    def save(self):
        for tmpl in self.templates:
            tmpl.save()
        return self

def main():
    # the pattern <<*>> is a template key
    #nv_data = [{'name': '<<WS_ORGANIZATION>>', 'value': 'myinstall'}]
    actual = Install()\
        .set('WS_ORGANIZATION','myinstall')
    assert(actual != {})
    tmpl_str = '''
    fail=<<fail>>
    fail_msg=<<fail_msg>>
    '''
    x = StubTemplate()\
            .set_template_str(tmpl_str)
    actual.add_template(x)
    actual.run()
    actual.show()
    actual.assertTrue('fail' in actual)
    actual.assertTrue('fail_msg' in actual)
    actual.assertTrue('WS_ORGANIZATION' in actual)
    actual.assertTrue(actual.get_data() == [{'name': '<<WS_ORGANIZATION>>', 'value': 'myinstall'}])

    #.assertTrue(actual == {'fail': False, 'fail_msg': []})

if __name__ == "__main__":
    # execute only if run as a script
    main()
