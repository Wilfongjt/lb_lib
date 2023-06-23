import os
from pprint import pprint

class LbDocComments(list):
    ## Given a folder and filename, Open and read the double hashed (ie "## ") comment lines in the file.
    def hello_world(self):
        print("I am LbDocComments!")
    def __init__(self, folder=os.getcwd(), filename='lb_doc_comments.py'):

        self.folder = folder
        self.filename = filename

    def open(self):
        ## Open and Load the file's double hashed comments on request.
        #print('folder', self.folder)
        #print('filename', self.filename)
        with open('{}/{}'.format(self.folder, self.filename)) as f:

            lines = f.read()
            lines = lines.split('\n')

            for ln in lines:
                ln = ln.strip(' ')
                if ln.startswith('class'):
                    ##* load line when line starts with "class", convert "class" to "## class"
                    self.append('## {}'.format(ln.replace(':','')))
                    #print('a ln', ln)

                else:
                    if ln.startswith('##'):
                        ##* load line when line is double comment... eg "##"
                        self.append(ln)
                        #print('b ln', ln)

                #print('open out', ln)
        return self
    #
    # Convert comments to markdown on request
    #
    def toMarkdown(self):
        ## Convert comments to markdown on request
        markdown = []
        for ln in self:
            #print('ln',ln)
            ##* comment is ignored when comment starts with a single hash, eg "# "
            if ln.startswith('1. '):

                ##* ordered item is bold when comment starts with "1. ", eg. "1. Something" --> "1. __Something__"
                ln = '1. __{}__'.format(ln[2:].strip(' '))

            if ' on request' in ln:
                ##* method name is bold when comment contains " on request"
                if markdown[len(markdown)-1].startswith('*'):
                    markdown.append(' ')
                markdown.append('__{}__ '.format(ln[2:].strip(' ')))
                markdown.append(' ')
            elif ' when ' in ln:
                ##* unordered list item is bulleted when comment contains "when"
                markdown.append('{}'.format(ln[2:]))
            elif '## class' in ln:
                #elif ln.startswith('## class'):
                ##* class name is H1 when comment starts with "## class"
                markdown.append('# {}'.format(ln[2:].strip()))
                markdown.append(' ')
            else:
                ##* markdown is normal when comment starts with "## "
                #markdown.append('{}'.format(ln.replace('##','')))
                markdown.append('{}'.format(ln[2:]))
                markdown.append(' ')
                ##* markdown is unordered when comment starts with "##*"
                ##* markdown is H1 when comment starts with "### "
                ##* markdown is H2 when comment starts with "#### "
                ##* markdown is H3 when comment starts with "##### "

        return '\n'.join(markdown)

def main():
    actual = LbDocComments(os.getcwd(), 'lb_doc_comments.py')
    # pprint(actual)
    assert (actual == [])
    assert (actual.open() != [])

    print(actual.toMarkdown())

if __name__ == "__main__":
    # execute as script
    main()
