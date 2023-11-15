import os

from source.lb_text_file import LbTextFile
from source.lb_util import LbUtil
from source.lb_folders import LbTemplateFolder, LbProjectFolder
from source.lb_exceptions import FileNotFoundException\
                                 ,UninitializedContextException\
                                 ,UninitializedDataException\
                                 ,UnhandledMergeKeysException

class LbTemplate(LbTextFile):
    def __init__(self):
        super().__init__()

        self.context=None
        self.data = [] # eg [{'name': '<<sample>>', 'value': 'sample'}]

    def assertExists(self):
        assert (LbUtil().file_exists(self.getFolder(),self.getFilename()))
        return self

    def set_context(self, context):
        self.context= context
        return self

    def get_context(self):
        return self.context

    def set_data(self, nv_list):
        self.data = nv_list
        return self

    def get_data(self):
        return self.data

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

    def open(self):
        super().open()
        return self

    def merge(self):
        #### Merge list of name value pairs with template
        ##*
        self.addStep('merge')
        if not self.get_data():
            raise UninitializedDataException('Set the template data!')

        #self.clear()
        idx = 0
        for ln in self:
            for nv in self.get_data():
                self[idx] = ln.replace(nv['name'], nv['value'])
            idx += 1
        return self

    def validate(self):
        super().validate()
        # if not LbUtil().file_exists(self.getFolder(), self.getFilename()):
        #    raise FileNotFoundException('File not found {}'.format(self.getFilename()))
        if not self.get_context():
            raise UninitializedContextException('set the template context')

        #print('get_template_key_list',self.get_template_key_list())
        if self.has_unmerged_keys():
            raise UnhandledMergeKeysException('Unmerged keys found {}'.format(self.get_template_key_list()))
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

    def has_unmerged_keys(self):
        #### Get list of keys from self
        rc = False
        keys = []
        #if not lines:
        #    lines = self.get_template_string().split('\n')  # document.split()
        lines = self
        for ln in lines:
            # remove duplicates
            keys = keys + [k for k in self.get_template_scrape_keys(ln) if k not in keys]
        if len(keys) > 0:
            rc = True
        return rc

    def get_template_string(self):

        line_string = '''
        // created: <date-time>
        // author: <gh-user>
        '''
        tmpl_folder = LbTemplateFolder(self.get_context())
        tmpl_file = '{}.tmpl'.format(self.getFilename())
        #print('templatfile {}/{}'.format(tmpl_folder, tmpl_file))
        #print('exits', LbUtil().file_exists(tmpl_folder, tmpl_file))
        #print('tmpl_folder', tmpl_folder)
        #print('tmpl_file', tmpl_file)
        #print('folder_exist', LbUtil().folder_exists(tmpl_folder))
        #print('file exist', LbUtil().file_exists(tmpl_folder, tmpl_file))
        if LbUtil().file_exists(tmpl_folder, tmpl_file):
            fn = '{}/{}'.format(tmpl_folder, tmpl_file)
            with open(fn) as f:
                line_string = f.read()
        #print("line_string", line_string)
        return line_string

    def show(self):
        super().show()
        print('  context          :',self.get_context())
        return self

def main():
    # get template
    # inject into

    import os
    #from source.lb_folders import LbProjectFolder

    nv_data = [
        {'name': '<<GH_PROJECT>>', 'value': 'temp-prj'}]

    target_folder = '{}/Development/temp-org/temp-ws/temp-prj/scripts'.format(os.environ['HOME'])
    target_file = 'git.rebase.sh'
    template_file ='{}.tmpl'.format(target_file)
    template_folder = LbTemplateFolder('bash')

    actual = LbTemplate()
    assert (actual == [])
    #print('  actual', actual)
    actual.setFolder(target_folder, create=True)
    actual.setFilename(target_file)
    actual.set_context('bash')
    actual.set_data(nv_data)
    actual.create()
    actual.show()
    actual.validate()
    actual.assertExists()

    print(' ')
    target_folder = '{}/Development/temp-org/temp-ws/temp-prj'.format(os.environ['HOME'])
    target_file = 'README.md'
    actual = LbTemplate()
    actual.setFolder(target_folder, create=True)
    actual.setFilename(target_file)
    actual.set_context('stub')
    actual.set_data(nv_data)
    actual.create()
    actual.open()
    actual.merge()
    actual.show()
    actual.validate()
    actual.assertExists()

if __name__ == "__main__":
    # execute as script
    main()