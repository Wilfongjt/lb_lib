
from source.lb_template import LbTemplate

class LbEnvTemplate(LbTemplate):
    #### Provide environment variables
    ##* generate target .env file when target .env doesnt exist
    ##* Allow manually add new key and value in target .env
    ##* Allow manually updated keys in target .env
    ##* Set system environment key when .env key is all caps

    def __init__(self):
        super().__init__()
        self.setFilename('.env')
        self.set_overwrite(False)

    def process(self):
        #print('X process', self.getFilename())
        self.create()   # create .env when .env file doesnt exist
        self.open()     # open .env when .env file exists
        self.merge()    # merge keys and values with templage
        #self.validate() # ignore the validation. set values manually
        self.save()     # save to the target folder
        self.show()     # show the state of the .env file
        self.assertExists() # fail when .env file doesnt exist
        return self

    def save(self):
        self.addStep('save')
        #### Save .env file on request
        ##* saves contents of list to the .env file

        with open('{}/{}'.format(self.getFolder(), self.getFilename()), 'w') as f:
            f.writelines(['{}\n'.format(ln) for ln in self])
            self.addStep('(file)')
        return self

def main():
    import os
    # FOLDERS
    target_folder = '{}/Development/temp-org/temp-ws/temp-prj/scripts'.format(os.environ['HOME'])

    actual = LbEnvTemplate()
    assert (actual == [])
    print('getFilename', actual.getFilename())
    assert (actual.getFilename()=='.env')

if __name__ == "__main__":
    # execute as script
    main()