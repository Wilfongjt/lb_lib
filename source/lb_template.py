import os

from source.lb_text_file import LbTextFile
from source.lb_util import LbUtil
from source.lb_folders import LbTemplateFolder, LbProjectFolder
from source.lb_exceptions import FileNotFoundException,UnInitializedContextException


class LbTemplate(LbTextFile):
    def __init__(self):
        super().__init__()
        #self.setFilename('{}.txt'.format(self.getClassName()))
        #self.template_str = '''
        #// created: <date-time>
        #// author: <gh-user>

        #'''
        self.context=None

    def assertExists(self):
        assert (LbUtil().file_exists(self.getFolder(),self.getFilename()))
        return self

    def set_context(self, context):
        self.context= context
        return self

    def get_context(self):
        return self.context

    def depload_template_string(self, folder=None, filename=None):
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

        if overwrite:  # and LbUtil().file_exists(self.getFolder(),self.getFilename()):
            ##* delete file when env file exists and overwrite is True
            self.addStep('delete')
            LbUtil().delete_file(self.getFolder(), self.getFilename())

        if LbUtil().file_exists(self.getFolder(), self.getFilename()):
            ##* skip create when file_exists and overwrite is False
            self.addStep('created')
            return self

        ##* create file when file doesnt exist

        with open('{}/{}'.format(self.getFolder(), self.getFilename()), 'w') as f:
            f.write(self.get_template_string())

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

    def validate(self):
        super().validate()
        # if not LbUtil().file_exists(self.getFolder(), self.getFilename()):
        #    raise FileNotFoundException('File not found {}'.format(self.getFilename()))
        if not self.get_context():
            raise UnInitializedContextException('set the template context')

        return self

    def get_template_scrape_keys(self, ln):
        #### Scrape the key names from a ln of test
        ##* eg abcd<key-name>efg
        lst = []
        collect = False
        key = ''
        for ch in ln:
            # print('ch',ch)
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

    def get_template_key_list(self, lines=None):
        #### Get list of keys in a given template string
        keys = []
        if not lines:
            lines = self.get_template_string().split('\n')  # document.split()
        for ln in lines:
            # remove duplicates
            keys = keys + [k for k in self.get_template_scrape_keys(ln) if k not in keys]
        return keys

    def depset_template_string(self, tmpl_str):
        self.template_str = tmpl_str
        return self

    def get_template_string(self):

        line_string = '''
        // created: <date-time>
        // author: <gh-user>
        '''
        tmpl_folder = LbTemplateFolder(self.get_context())
        tmpl_file = '{}.tmpl'.format(self.getFilename())
        #print('templatfile {}/{}'.format(tmpl_folder, tmpl_file))
        #print('exits', LbUtil().file_exists(tmpl_folder, tmpl_file))
        print('tmpl_folder', tmpl_folder)
        print('tmpl_file', tmpl_file)
        print('folder_exist', LbUtil().folder_exists(tmpl_folder))
        print('file exist', LbUtil().file_exists(tmpl_folder, tmpl_file))
        if LbUtil().file_exists(tmpl_folder, tmpl_file):
            fn = '{}/{}.tmpl'.format(tmpl_folder, tmpl_file)
            with open(fn) as f:
                line_string = f.read()
        print("line_string", line_string)
        return line_string

    def show(self):
        super().show()
        print('  context          :',self.get_context())
        return self

def main():
    # get template
    # inject into

    import os
    from source.lb_folders import LbProjectFolder
    target_folder = '{}/Development/temp-org/temp-ws/temp-prj'.format(os.environ['HOME'])
    target_file = 'git.rebase.sh'
    template_file ='{}.tmpl'.format(target_file)
    template_folder = LbTemplateFolder('bash')
    print('template folder', template_folder)
    print('file exist', LbUtil().file_exists(template_folder, template_file))
    print(LbUtil().get_file_list(template_folder, ext='tmpl'))
    #print('folder', LbProjectFolder())
    actual = LbTemplate()
    assert (actual == [])
    print('  actual', actual)
    actual.setFolder(target_folder, create=True)
    actual.setFilename(target_file)
    actual.set_context('bash')
    actual.get_template_string()
    #actual.create()
    actual.show()
    actual.validate()
    actual.assertExists()

if __name__ == "__main__":
    # execute as script
    main()