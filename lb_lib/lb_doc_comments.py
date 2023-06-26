import os
from pprint import pprint
from lb_lib.lb_text_file import LbTextFile
class LbDocComments(LbTextFile):
    ## Read and convert "##" comments to Markdown
    ## Given a folder and filename, Open, read, and convert the double hashed (ie "## ") comment lines to Markdown.
    ##* save to README.md
    def __init__(self):
        super().__init__()
    def hello_world(self):
        print("I am LbDocComments!")
        return self

    def load(self, line_list):
        ## __Load line list on request__
        self.addStep('load')
        for ln in line_list:

            ln = ln.strip(' ')
            if ln.startswith('class'):
                ##* load markdown line when line starts with "class", convert "class" to "## class"
                #self.append('## {}'.format(ln.replace(':','')))
                self.append(self.markdown(ln))
            else:
                if ln.startswith('##'):
                    ##* load markdown line when line is double comment... eg "##"
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

        return markdown

        return markdown

    def save(self):
        ## __Save markdown on request__
        ##* change name
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
