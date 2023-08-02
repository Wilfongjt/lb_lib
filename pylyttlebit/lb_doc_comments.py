import os
from pprint import pprint
from pylyttlebit.lb_text_file import LbTextFile
class LbDocComments(LbTextFile):
    ## Convert a python file to a Markdown document

    def __init__(self):
        super().__init__()
        ##* Define words to decorate in decoration list
        self.decoration_list = ['change',
                         'checkout',
                         'clone',
                         'confirm',
                         'convert',
                         'copy'
                         'create',
                         'collect',
                         'decorate',
                         'define',
                         'delete',
                         'generate',
                         'ignore',
                         'impute',
                         'initialize',
                         'input',
                         'install',
                         'load',
                         'loads',
                         'make',
                         'makes',
                         'markdown',
                         'merge',
                         'navigate',
                         'open',
                         'output',
                         'provide',
                         'read',
                         'save',
                         'skip',
                         'stop',
                         'when'
                         ]
    def hello_world(self):
        print("I am LbDocComments!")
        return self

    def decorate(self, line):
        #### Decorate line on request
        ##> Bold the key words
        nline = []
        line = line.replace(',',' ,').replace(':', '')
        line = str(line).split(' ')
        for word in line:
            if word.lower() in self.decoration_list:
                ##* decorate word with bold when word is found in decoration list ... [x] has test
                nline.append('__{}__'.format(word.title()))
            else:
                nline.append(word)
        ##* output: string/line ... [x] has test
        return ' '.join(nline).replace(' ,',',')

    def load(self, line_list):
        #### Load line list on request
        ##> collect the double hash lines and strip the comment hashes
        self.addStep('load')
        for ln in line_list:

            ln = ln.strip(' ')
            if ln.startswith('class'):
                ##* load line when line starts with "class" ... [x] has test
                self.append(self.markdown(ln))

            elif ln.startswith('##'):
                ##* load comment line when line starts with "##" ... [x] has test
                self.append(self.markdown(ln))

        ##* ignore comment when comment line starts with a single hash, eg "# " ... [x] has test
        ##* ignore uncommented line ... [x] has test

        ##* output: LbDocComments ... [x]
        return self
    #
    # Convert comments to markdown on request
    #
    def markdown(self, ln):
        #### Convert a single comment to Markdown on request
        ##> markdown is encoded after the double hash
        if ln.startswith('class'):
            ##* make the class line bigger, eg "class Abc()" -> "# class Abc()"
            markdown = '# {}'.format(ln)
        else:
            ##* strip the double hash "##" from line, eg. "##* hi" --> "* hi"
            markdown = '{}'.format(ln[2:])

        markdown = self.decorate(markdown)

        return markdown


    def save(self):
        #### Save markdown on request
        ##> change file name, dont overwrite the source file
        ##* impute file name, eg "lb_doc_comments.py" to "README.lb_doc_comments.py.md"
        self.saveAs(self.getFolder(),'README.{}.md'.format(self.getFilename()))
        return self


def main():
    from pylyttlebit.lb_text_file import LbTextFile
    folder = os.getcwd()
    filename = str(__file__).split('/')[-1]
    actual = LbDocComments() #.setFolder(os.getcwd()).setFilename(filename)
    # pprint(actual)
    assert (actual == [])
    assert (actual.setFolder(folder) == [])
    assert (actual.setFilename(filename) == [])
    #print(LbConstants().app_folder, folder)
    #print('file', filename)
    print('class "{}"'.format(actual.markdown('class LbDocComments(LbTextFile)')))
    assert (actual.markdown('class LbDocComments(LbTextFile)')=='# class LbDocComments(LbTextFile)')
    assert (actual.markdown('##* hi ')=='* hi ')
    assert (actual.markdown('### hi ')=='# hi ')
    assert (actual.markdown('##__hi on request__')=='__hi on request__')

    assert (actual.open() != [])
    #pprint(actual)
    #tfile = LbTextFile().setFolder(os.getcwd()).setFilename(filename).open()

    #assert (actual.load(tfile))
    assert (actual.save() != [])
    actual.preview()


def main_document():
    from pylyttlebit.lb_doc_comments import LbDocComments
    print('lb_doc_commmentsv')
    folder = '/'.join(str(__file__).split('/')[0:-1])
    filename = str(__file__).split('/')[-1]
    LbDocComments().setFolder(folder).setFilename(filename).open().save()


if __name__ == "__main__":
    # execute as script
    main()
