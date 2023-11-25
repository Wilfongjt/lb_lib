import os
import re
from source.lb_text_file import LbTextFile
from source.lb_util import LbUtil
from source.lb_folders import LbTemplateFolder, \
                              LbProjectFolder,\
                              ScriptsFolderTemplate,\
                              GitProjectFolderTemplate
from source.lb_exceptions import FileNotFoundException\
                                 ,UninitializedContextException\
                                 ,UninitializedDataException\
                                 ,UnhandledMergeKeysException\
                                 ,FolderNotFoundException

class LbTemplate(LbTextFile):
    def __init__(self):
        super().__init__()

        self.context=None
        self.data = [] # eg [{'name': '<<sample>>', 'value': 'sample'}]
        self.overwrite = False

    def assertExists(self):
        #### Test that file gets written
        assert (LbUtil().file_exists(self.getFolder(),self.getFilename()))
        return self


    def is_overwrite(self):
        return self.overwrite
    def set_overwrite(self, tf):
        if tf:
            self.addStep('overwrite')
        self.overwrite = tf
        return self

    def set_context(self, context):
        self.context= context
        return self

    def get_context(self):
        return self.context

    def set_data(self, nv_list):
        #### Allow name and value data ["name":"<<abc_xyz>>","value":"12345",...]
        self.data = nv_list
        return self

    def get_data(self):
        return self.data


    def create(self):
        ###### Create empty file on request
        ##* dont overwrite by default
        if self.is_overwrite():  # and LbUtil().file_exists(self.getFolder(),self.getFilename()):
            ##* delete file when env file exists and overwrite is True
            self.addStep('delete')
            LbUtil().delete_file(self.getFolder(), self.getFilename())

        if LbUtil().file_exists(self.getFolder(), self.getFilename()):
            ##* skip create when file_exists and overwrite is False
            self.addStep('created')
            return self

        ##* create file when file doesnt exist
        self.addStep('create')
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
                #print('merge ', self.getFilename(),nv)
                ln = ln.replace(nv['name'], nv['value'])

            self[idx] = ln

            idx += 1
        #print('merge out ', self)
        return self

    def validate(self):
        super().validate()
        # if not LbUtil().file_exists(self.getFolder(), self.getFilename()):
        #    raise FileNotFoundException('File not found {}'.format(self.getFilename()))
        if not self.get_context():
            raise UninitializedContextException('set the template context')

        if self.has_unmerged_keys():
            raise UnhandledMergeKeysException('Unmerged keys found file {}, keys {}'.format(self.getFilename(),self.get_unmerged_keys()))
        #lb_template_folder = LbTemplateFolder(self.get_context())
        #if not lb_template_folder.exists():
        #    raise FolderNotFoundException('Template folder Not Found {}'.format(lb_template_folder))

        return self

    def find_substrings(self, input_text):
        pattern = r"<<([A-Za-z_-]+)>>|<<([A-Za-z]+_[A-Za-z_-]+)>>"
        matches = re.findall(pattern, input_text)
        # Flatten the list of tuples
        matches = [match[0] if match[0] else match[1] for match in matches]
        return matches

    def get_merge_keys(self):
        rc = self.find_substrings(self.get_template_string())
        return rc

    def get_unmerged_keys(self):
        rc = self.find_substrings('\n'.join(self))

        return rc

    def has_unmerged_keys(self):
        #### Get list of keys from self
        rc = False
        keys = self.get_unmerged_keys()
        if len(keys) > 0:
            rc = True
        return rc

    def get_template_string(self):

        line_string = '''
        // created: <<date-time>>
        // author: <<GH_USER>>
        '''
        #tmpl_folder = LbTemplateFolder()
        print('A cwd',os.getcwd())
        tmpl_folder = LbTemplateFolder(self.get_context())
        tmpl_file = '{}.tmpl'.format(self.getFilename())
        print('tmpl_folder',tmpl_folder, LbUtil().folder_exists(tmpl_folder) )
        print('tmpl_file',tmpl_file, LbUtil().file_exists(tmpl_folder, tmpl_file))
        #print('exists', LbUtil().file_exists(tmpl_folder, tmpl_file))
        # load the template file
        if LbUtil().file_exists(tmpl_folder, tmpl_file):
            fn = '{}/{}'.format(tmpl_folder, tmpl_file)
            with open(fn) as f:
                line_string = f.read()
        return line_string

    def process(self):
        print('process', self.getFilename())
        self.create()
        self.open()
        self.merge()
        self.validate()
        self.save()
        self.show()
        self.assertExists()

        return self

    def show(self):
        super().show()
        if not self.is_show():
            return self
        print('  context          :',self.get_context())
        print('  overwrite        :', self.is_overwrite())

        return self


class LbBashTemplate(LbTemplate):
    def __init__(self):
        super().__init__()
        self.set_context('bash')
        self.setFilename('*.sh')
        self.set_overwrite(True)

class LbStubTemplate(LbTemplate):
    def __init__(self):
        super().__init__()
        self.set_context('stub')
        self.setFilename('stub.md')
        self.set_overwrite(True)

def main():
    # get template
    # inject into

    import os
    import datetime
    #from source.lb_folders import LbProjectFolder
    '''
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
    actual.set_overwrite(True)
    actual.create()
    actual.show()
    actual.validate()
    actual.assertExists()
    #exit(0)

    
    print(' ')
    target_folder = '{}/Development/temp-org/temp-ws/temp-prj'.format(os.environ['HOME'])
    target_file = 'README.md'
    
    actual = LbTemplate()
    actual.setFolder(target_folder, create=True)
    actual.setFilename(target_file)
    actual.set_context('stub')
    actual.set_data(nv_data)
    actual.set_overwrite(False)
    actual.create()
    actual.open()
    print('merge keys', actual.get_merge_keys())
    print('unmerged keys', actual.get_unmerged_keys())

    actual.merge()
    actual.show()
    actual.validate()
    actual.assertExists()
    '''

    nv_data = [
        {'name': '<<WS_ORGANIZATION>>', 'value': 'temp-org'},
        {'name': '<<WS_WORKSPACE>>', 'value': 'temp-ws'},
        {'name': '<<GH_PROJECT>>', 'value': 'temp-prj'},
        {'name': '<<GH_USER>>', 'value': 'temp-user'},
        {'name': '<<date-time>>', 'value': str(datetime.datetime.now())}
    ]
    # FOLDERS
    target_folder = '{}/Development/temp-org/temp-ws/temp-prj/scripts'.format(os.environ['HOME'])
    # OUTPUT to projects /scripts folder
    #target_folder = GitProjectFolderTemplate(nv_data)

    print('target_folder',target_folder)

    ######### STUB

    actual = LbStubTemplate()
    actual.setFolder(target_folder,create=True)
    actual.set_data(nv_data)
    actual.set_show(True)
    actual.process()

    ######### BASH
    #print('templates',template_fns)
    '''
    target_folder = ScriptsFolderTemplate(nv_data)
    template_fns = LbUtil().get_file_list(template_folder)
    template_folder = LbTemplateFolder('bash')

    for target_file in template_fns:
        actual = LbBashTemplate()
        actual.setFolder(target_folder, create=True)
        actual.setFilename(target_file.replace('.tmpl',''))
        #actual.set_context('bash')
        actual.set_data(nv_data)
        actual.set_overwrite(False)
        actual.create()
        actual.open()
        actual.merge()
        actual.show()
        actual.validate()
        actual.save()
        actual.assertExists()
        print('---')
    '''
    #print('\n'.join(actual))



if __name__ == "__main__":
    # execute as script
    main()