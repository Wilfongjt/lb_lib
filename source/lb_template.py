
from source.lb_text_file import LbTextFile
from source.lb_util import LbUtil

class LbTemplate(LbTextFile):
    def __init__(self):
        super().__init__()
        self.template_str = '''
        // created: <date-time>
        // author: <gh-user>
        
        '''

    def load_template_string(self, folder=None, filename=None):
        #### Load Template from a File
        ##* Store template files in ./data/
        # template files are stored in /data folder
        self.addStep('(file: {})'.format(filename))
        self.addStep('load_template_string')
        if folder and filename and LbUtil().file_exists(folder, filename):
            with open('{}/{}'.format(folder, filename)) as f:
                lines = ''.join(f.readlines())
                self.set_template_string(lines)
                self.addStep('loaded')
        return self

    def create(self, overwrite=True):
        ###### Create empty file on request

        if overwrite: #and LbUtil().file_exists(self.getFolder(),self.getFilename()):
            ##* delete file when env file exists and overwrite is True
            self.addStep('delete')

            LbUtil().delete_file(self.getFolder(),self.getFilename())

        if LbUtil().file_exists(self.getFolder(),self.getFilename()):
            ##* skip create when file_exists and overwrite is False
            self.addStep('created')
            return self

        ##* create file when file doesnt exist

        #self.addStep('(defaults)')
        #self.load(['{}={}'.format(k, defaults[k]) for k in defaults])
        #self.addStep('(environment)', arrow='*')
        self.save()

        #self.addStep('// (environment)')

        self.clear()
        return self

    def merge(self, lst, template_str=None):
        #### Merge list of name value pairs with template
        ##* list eg [{name: "<some-name>", value: "abc"}]
        ##* clear template
        self.addStep('merge')
        self.clear()
        ##* get default template string when string not provided
        if template_str:
            rc = template_str
        else:
            rc = self.get_template_string()
        # apply merge_list to template
        for nv in lst:
            rc = rc.replace(nv['name'], nv['value'])

        # load template into template
        for ln in rc.split('\n'):
            self.append(ln)

        return self

    def get_template_scrape_keys(self, ln):
        #### Scrape the key names from a ln of test
        ##* eg abcd<key-name>efg
        lst = []
        collect = False
        key = ''
        for ch in ln:
            #print('ch',ch)
            if ch == '<':
                collect = True

            if collect:
                key += ch

            if ch == '>':
                collect = False
                if key != '' and key not in lst:
                    lst.append(key)
                key = ''

        return lst

    def get_template_key_list(self, lines = None):
        #### Get list of keys in a given template string
        keys = []
        if not lines:
            lines = self.get_template_string().split('\n') # document.split()
        for ln in lines:
            # remove duplicates
            keys = keys + [k for k in self.get_template_scrape_keys(ln) if k not in keys]
        return keys

    def set_template_string(self, tmpl_str):
        self.template_str=tmpl_str
        return self

    def get_template_string(self):
        return self.template_str

    #def clearInjections(self):
    #    return self

    def insert(self, key, block):

        return self

    def dep_get_template_string(self):
        return '''
        // created: <date-time>
        // author: <gh-user>
        '''
def get_multi_line_example():
    multi_line = '''
class zbh() {    
    line1
    "line2"
    'line3'
}    
    '''
    #multi_line = [ln.replace('    ', '') for ln in multi_line.split('\n')]
    #print('multi_line', multi_line)
    #multi_line = multi_line.replace('    ', '')
    #print('multi_line', multi_line)
    return multi_line

def main():
    import os
    test_file = 'lb_template.js'
    temp_api = 'test_lb_template'
    temp_folder = '{}/Development/{}'.format(os.environ['HOME'], temp_api)
    multi_line = '''
    line1
    "line2"
    'line3'
    '''
    merge_list=[{'name': '<date-time>', 'value': 'testdate'},
                {'name':'<gh-user>', 'value':'jw'}]
    data_folder = os.getcwd()
    #  hack a path to /data/hapi_templates
    data_folder = data_folder.replace('/template','').replace('/source','')
    data_folder = '{}/data/example_templates'.format(data_folder)

    print('data_folder', data_folder)
    actual = LbTemplate()

    assert(actual == [])
    assert(actual.get_template_scrape_keys('abc<tmpl-key>defg') == ['<tmpl-key>'])

    print('get_template_key_list',actual.get_template_key_list())
    assert(actual.get_template_key_list() == ['<date-time>', '<gh-user>'])

    #name_values=[{'name': '<date-time>', 'value': 'testdate'},{'name':'<gh-user>', 'value':'jw'}]
    #print('merge',actual.merge(name_values))

    actual = LbTemplate()\
                .setFolder(temp_folder, create=True)\
                .setFilename(test_file)\
                .merge(merge_list, '# <date-time> <gh-user>')\
                .create(overwrite=True) \
                .show(terminalMsg='LbTemplate')

    assert(actual.exists())

    # load from file
    test_file = 'lb_template.txt'
    multi_line = '''
    class zbh() {    
        line1=['a',"b"]
        "line2"
        'line3'
    }    
        '''
    merge_list = [{'name': '<date-time>', 'value': 'testdate'},
                  {'name': '<gh-user>', 'value': 'jw'},
                  {'name': '<multi-line>', 'value': multi_line},
                  {'name': '<ml2>', 'value': multi_line},
                  {'name': '<ml3>', 'value': multi_line}]
    actual = LbTemplate() \
                .load_template_string(data_folder, 'lb_template.txt.tmpl') \
                .setFolder(temp_folder, create=True) \
                .setFilename(test_file) \
                .merge(merge_list) \
                .create(overwrite=True) \
                .show(terminalMsg='LbTemplate')

if __name__ == "__main__":
    # execute as script
    main()