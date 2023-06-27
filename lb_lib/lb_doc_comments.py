import os
from pprint import pprint
from lb_lib.lb_text_file import LbTextFile
class LbDocComments(LbTextFile):
    ## Open, Read, and convert "##" comments to Markdown
    ## Given a folder and filename, Open, read, and convert the double hashed (ie "## ") comment lines to Markdown.

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
                         'decorate',
                         'define',
                         'generate',
                         'impute',
                         'install',
                         'load',
                         'navigate',
                         'open',
                         'read',
                         'save',
                         'stop',
                         'when'
                         ]
    def hello_world(self):
        print("I am LbDocComments!")
        return self

    def load(self, line_list):
        ## __Load line list on request__
        self.addStep('load')
        for ln in line_list:

            ln = ln.strip(' ')
            if ln.startswith('class'):
                ##* load line when line starts with "class"
                ##* convert "class" to "## class" when line starts with "class"
                #self.append('## {}'.format(ln.replace(':','')))
                self.append(self.markdown(ln))
            else:
                if ln.startswith('##'):
                    ##* load comment when line starts with "##"
                    self.append(self.markdown(ln))

        return self
    #
    # Convert comments to markdown on request
    #
    def markdown(self, ln):
        ## __Convert a single comment to Markdown on request__
        ##* comment is ignored when comment starts with a single hash, eg "# "

        #    markdown = 'x{}'.format(ln[2:])
        if ln.startswith('class'):
            ##* markdown is H1 when line starts with "class"
            markdown = '# {}'.format(ln)
        else:
            ##* markdown is normal when comment starts with "## "
            markdown = '{}'.format(ln[2:])

        ##* markdown is unordered when comment starts with "##*"
        ##* markdown is H1 when comment starts with "### "
        ##* markdown is H2 when comment starts with "#### "
        ##* markdown is H3 when comment starts with "##### "

        markdown = self.decorate(markdown)

        return markdown

    def decorate(self, line):
        ##__Decorate line on request__
        nline = []
        line = line.replace(',',' ,')
        line = str(line).split(' ')
        for word in line:
            if word.lower() in self.decoration_list:
                ##* decorate word with bold when word is found in decoration list
                nline.append('__{}__'.format(word.title()))
            else:
                nline.append(word)
        return ' '.join(nline).replace(' ,',',')

    def save(self):
        ## __Save markdown on request__
        ##* impute file name, eg "lb_doc_comments.py" to "README.lb_doc_comments.py.md"
        self.saveAs(self.getFolder(),'README.{}.md'.format(self.getFilename()))
        return self


def main():
    from lb_lib.lb_text_file import LbTextFile
    folder = os.getcwd()
    filename = str(__file__).split('/')[-1]
    actual = LbDocComments() #.setFolder(os.getcwd()).setFilename(filename)
    # pprint(actual)
    assert (actual == [])
    assert (actual.setFolder(folder) == [])
    assert (actual.setFilename(filename) == [])
    #print('folder', folder)
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

if __name__ == "__main__":
    # execute as script
    main()
