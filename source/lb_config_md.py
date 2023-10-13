import os
import re
from source.lb_text_file import LbTextFile
from source.stack import Stack
from source.ddict import DDict
from source.lb_recorder import LbRecorder
from pprint import pprint
from decimal import Decimal

class LbConfigMd(LbTextFile):
    def __init__(self):
        super().__init__()
        self.text=''
        self.dictionary=DDict()

    def set_md_text(self, text):
        #### Set a block of Markdown text to be evaluated on request
        ##* Use for testing
        self.text = text
        return self

    def getLevel(self, line):
        #### Determine level of line by counting the leading # on request
        rc = 0
        for ch in line:
            if ch == '#':
                rc += 1
            else:
                break
        return rc

    def getKey(self, line):
        #### Retrive a suitable key value for a name and value pair on request
        if line:
            line = line.strip()
        if not line:
            return None
        if not line.startswith('#') and not line.startswith('1.'): # doenst start with # or 1.
            return None
        # case "# a
        # case "# a:"
        # case "# a: b"
        # case "1. a
        # case "1. a:
        # case "1. a: b

        if ':' in line: # get rid of value part
            line = line.split(':')[0]

        key = line.replace('# ', '') \
            .replace('#', '') \
            .replace('1. ', '') \
            .replace('1.', '') \
            .strip() \
            .replace(': ', '') \
            .replace(':', '') \
            .replace(']', '') \
            .replace('[', '') \
            .replace('{', '') \
            .replace(' ', '_')
        return key

    def depitemize_list(self, str_list):
        ##* Deprecated
        # case "" --> None
        # case "[]" --> []
        # case "[ ]" --> []
        # case "[R,1,1,0,True]" --> ['R', 1, 1.0, True]

        lst = []
        str_list = str_list.strip()
        # case "" --> []
        if not str_list:
            return []
        # case "[ ]" --> []
        if str_list.replace(' ', '') == '[]':
            return []

        # case "R,U,D" --> []
        if not str_list.startswith('['):
            return []
        # case "[R,U,D]"
        # remove '[' and ']' before splitting
        str_list = str_list.replace('[','').replace(']','').strip()
        # convert 'A,B,C' --> ['A', 'B', 'C']
        lst = str_list.split(',')
        # return ['A', 'B', 'C']
        return lst

    def normalize(self, line):
        #### Convert a line string to parsable string on request
        #self.addStep('"{}"'.format(line))
        #print('normalize "{}"'.format(line), end=' ' )
        if not line:  # '' or None
            self.addStep(' -> "{}"\n'.format(None))
            return None

        line = line.strip()  # ' ' --> ''
        if not line:
            self.addStep(' -> "{}"\n'.format(None))
            return None

        if not line.startswith('#') and not line.startswith('1.'):
            self.addStep(' -> "{}"\n'.format(None))
            return None

        # normalize spaces
        norm = line
        # norm = norm.replace('1.', '1. ').replace('  ', ' ')  # '1.a:'          -> '1. a : '
        norm = norm.replace(':', ' : ').replace('  ', ' ')  # '1. a: '        -> '1. a : '
        norm = norm.replace('{', '{ ').replace('}', '} ')  # '1. a : {}'     -> '1. a : { } '
        norm = norm.replace('[', '[ ').replace(']', '] ')  # '1. a : []'     -> '1. a : [ ] '
        norm = norm.replace(',', ' , ')  # '1. a: [ A,B ]' -> '1. a : [ A , B ] '
        norm = norm.replace('  ', ' ')  # remove double spaces
        # print('A norm {} "{}"'.format(len(norm), norm))
        # repairs
        if norm.startswith('#'): norm = self.fix(norm, r'#+\s*\w*\s*', ' : ')  # '# project ' --> '# project : '
        # print('B norm "{}"'.format(norm))
        if norm.startswith('#'): norm = self.fix(norm, r'#+\s*\w*\s*:\s*', ' {} ')  # '# project : ' --> '# project : {}'

        #print('C norm "{}"'.format(norm))
        if norm.startswith('1.'): norm = norm.replace('1.', '1. ', 1).replace('  ', ' ')  # '1.a:'          -> '1. a : '
        #print('D norm "{}"'.format(norm))

        if norm.startswith('1.'): norm = self.fix(norm, r'\d+\.\s*\w*\s*:\s*', " ")  # '1. project:' --> "1. project : "
        #print('E norm "{}"'.format(norm))

        norm = '{} '.format(norm) # force all to have trailing space
        norm = norm.replace('  ', ' ').replace('  ', ' ')

        #self.addStep('"{}"\n'.format(norm.replace('  ', ' ')))
        #print('out norm "{}"'.format(norm))

        return norm

    def getValue(self, line, stringify=None):
        #### Retrieve the value of nome and value pair on request
        #print("getValue   1 '{}'".format(line))

        line = self.normalize(line)
        #print("  getValue 2 '{}'".format(line))
        if not line:
            val = None
        elif self.matches(line, r'((#+)|(\d+\.))\s*\w*\s*:\s*{\s*}\s*'):  # '# a : {} ' or '1. a : {} '
            #print('getValue A', line)
            val = {}
        elif self.matches(line, r'((#+)|(\d+\.))\s*\w*\s*:\s*\[\s*\]\s*'): # '# a : [] ' or '1. a : [] '
            #print('getValue B', line)
            val = []
        elif self.matches(line, r'((#+)|(\d+\.))\s*\w*\s*:\s*\[.*\]\s*'):  # '# a : [] '
            #print('getValue C', line)
            val = []  # create list
            x = line.split(':')  # '# a: [C,B]'     -> ['# a', '[C,B]']
            x = x[1]  # ['# a', '[C,B]'] -> '[C,B]'
            x = x.replace('[', '').replace(']', '')  # '[C,B]'          -> 'C,B'
            for p in x.split(','):  # breakup parts of comma delimited str
                p = p.strip()  # eg p is C
                if p:  # ignore '' and None
                    p = self.typeify(p)  # convert to a proper type
                    val.append(p)  # collect value
        elif self.matches(line, r'^\d+\.\s*((\s*\w+\s*:\s*[^,]*\s*[,]\s*)+\s*\w+\s*:\s*.*)\s*$'):
            # 1. a : , b : , c :
            #print('  getValue D ', line)
            #print('  line       ', line)
            val = {}
            x = line.replace('1.', '', 1)

            for p in x.split(','):
                #print('  p',p)
                p = p.strip()
                p = p.split(':')
                #print('  p',p)
                if p:
                    val[p[0].strip()]=self.typeify(p[1].strip())
                #    p = self.
            #print('  val', val)

        #    #val =
        elif self.matches(line, r'((#+)|(\d+\.))\s*\w*\s*:\s*.*\s*'):  # '# a : abc'
            #print('getValue E', line)
            val = self.typeify(line.split(':')[1].strip())
        #elif self.matches(line, r'\d+\.\s*[^}{\[\]:]*'):  # '1. a-constant'
        elif self.matches(line, r'\d+\.\s*.+'):  # '1. a-constant'

            #print('getValue F', line)
            val = line.replace('1.', '')
            val = self.typeify(val.strip())
            #print('val',val)

        else:
            raise Exception('Invalid line {}'.format(line))
        #print('  out getValue', val, type(val))
        #if stringify:
        #    val = str(val)
        return val

    def is_integer(self, s):
        #### Determine if a string represents a proper integer on request
        try:
            int(s)
            return True
        except ValueError:
            return False
    def is_float(self, s):
        #### Determine if a string represents a proper float on request
        try:
            #print('decimAL', s)
            float(s)
            return True
        except ValueError:
            return False

    def is_boolean(self, s):
        #### Determine if a string represents a proper boolean on request
        s = s.lower()
        return s == "true" or s == "false"
    def is_size(self,s):
        #### Determine if a string represents a size range on request
        ##* eg 3-330
        if self.matches(s, '\d+\-\d+'):
            return True
        return False

    def typeify(self, val_str):
        #### Convert a string to one of the supported types on request
        ##* '1' -> integer
        ##* '1.1' -> float
        ##* '1.1' -> decimal(3,1)
        ##* 'True' -> boolean
        ##* 'False' -> boolean
        ##* '3-330' -> {'max': 330, 'min': 3} -> size-range
        ##* 'abc' -> string

        # print('1 typeify', val_str)
        val = val_str
        if self.is_integer(val_str):
            val = int(val_str)
        elif self.is_float(val_str):
            val = Decimal(val_str)
        elif self.is_boolean(val_str):
            if val_str.lower() == 'true':
                val = True
            else:
                val = False
        elif self.is_size(val_str): # eg 3-330
            val = {'min': 0, 'max': 0}
            val['min'] = int(val_str.split('-')[0])
            val['max'] = int(val_str.split('-')[1])
        elif val_str.startswith("'") and val_str.endswith("'"):
            val = val[1:-1]
        elif val_str.startswith('"') and val_str.endswith('"'):
            val = val[1:-1]
        # print('2 typeify', val)

        return val

    def toJSON(self, show=False):
        #### Convert Markdown text to JSON object on request
        self.dictionary=DDict()
        #print('toJSON DDict', self.dictionary)
        lines = self.text.split('\n')
        stack = Stack()

        if not lines: return None

        for ln in lines:

            self.addStep('"{}"'.format(ln))

            ln = self.normalize(ln)
            #print('ln',ln)
            if ln and ln.startswith('#'):
                #print('1 # ln    ', ln)
                #print('2 # level ', self.getLevel(ln))
                #print('3 # key   ', self.getKey(ln))
                #print('4 # value ', self.getValue(ln))

                level = self.getLevel(ln)
                key = self.getKey(ln)
                value = self.getValue(ln)
                # adjust stack
                while stack.size() > 0 and stack.size() >= level:
                    stack.pop()

                stack.push(key)
                self.dictionary.set(stack, value)
                #print('5 # toJSON stack', stack)
                #print('6 # toJSON dictionary', self.dictionary)
            elif ln and ln.startswith('1.'):
                #
                #print('2 ln   ',ln)
                #print('3 key  ', self.getKey(ln))
                #print('4 value', self.getValue(ln))
                key = self.getKey(ln)
                value = self.getValue(ln)
                stack.push(key)
                self.dictionary.set(stack, value)
                stack.pop()
            #else:
            #    print('ignore line ""'.format(ln))

        #print('toJSON result', self.dictionary)
        #pprint(self.dictionary)
        if show:
            pprint(self.dictionary)

        return self.dictionary

    def fix(self, line, pattern, fix_str):
        #### Fix dangling lines before parsing on request
        ##* '# project ' --> '# project : '
        ##* '# project : ' --> '# project : {}'
        ##* '1. project:' --> "1. project : "

        pattern = pattern  # '# project: {}'
        match = re.match(pattern, line)

        if match:
            if match.group()==line:
                line += fix_str

        return line

    def matches(self, line, pattern):
        #### Match a line to a given regular expression on request

        tf = False
        pattern = pattern  # '# project: {}'
        match = re.match(pattern, line)

        if match:
            if match.group() == line:
                tf = True

        return tf


def main():
    from source.lb_util import LbUtil

    # '# a'     --> '# a : {}'
    # '# a: '   --> '# a : {}'
    # '# a: {}' --> '# a : {}' match

    # '1. a'    --> "1. a"  match
    # '1. a:'   --> "1. a : ''"
    # '1. a: A'  --> "1. a : 'A'" match
    # '1. a: 1'    --> "1. a : 1" match
    # '1. a: 1.0'  --> "1. a : 1.0" match
    # '1. a: True' --> "1. a : True" match
    # '1. a:A, b:B' --> "1. a : 'A' , b : 'B'"

    example_folder = os.getcwd().replace('source','data/example_templates')
    print('example_folder', example_folder)
    example_file = 'example.config.md'
    example_md = LbTextFile().setFolder(example_folder).setFilename(example_file).open()
    print('example_md.toString()\n', example_md.toString())
    #pprint(example_md)


    #exit(0)

    actual = LbConfigMd()
    print('LbConfigMd',LbConfigMd)
    #assert (actual)
    assert (actual.normalize(None) == None) # ignore
    assert (actual.normalize('') == None) # ignore
    assert (actual.normalize(' ') == None) # ignore
    assert (actual.normalize('a') == None)  # ignore

    #print('norm', actual.normalize('#a:,b:'))
    #assert (actual.normalize('# a:,b:') == None)
    #assert (actual.normalize('# a:,b:') == "# a: {}, b: {}")
    #print('norm', actual.normalize('# a'))
    assert (actual.normalize('# a')=='# a : {} ')
    assert (actual.normalize('# a:')=='# a : {} ')
    assert (actual.normalize('# a: {}')=='# a : { } ')

    assert (actual.normalize('1. a') == '1. a ')
    assert (actual.normalize('1. a:') == "1. a : ")
    #assert (actual.normalize('1. a:') == "1. a : ''")

    assert (actual.normalize('1. a:abc') == "1. a : abc ")
    assert (actual.normalize('1.a:,b:') == "1. a : , b : ")
    #assert (actual.normalize('1.a:,b:') == "1. a : '' , b : ''")

    assert (actual.normalize('1.a:,b:abc,c:def') == "1. a : , b : abc , c : def ")

    assert (actual.normalize('1. a:,b:') == "1. a : , b : ")
    assert (actual.normalize('1. a: ,b:') == "1. a : , b : ")
    assert (actual.normalize('1. a: ,b: ') == "1. a : , b : ")

    assert ('1. name: id, type:C, size:3-330, validate:R', '1. name : id , type : C , size : 3-330 , validate : R ')

    #exit(0)
    #print('key', actual.getKey(''))
    assert (actual.getKey('')==None) # ignore
    assert (actual.getKey(' ')==None) # ignore
    assert (actual.getKey('a') == None) # ignore
    assert (actual.getKey('# a')=='a')
    assert (actual.getKey('# a ')=='a')
    assert (actual.getKey('# a:')=='a')
    assert (actual.getKey('# a: ')=='a')

    assert (actual.getValue('')==None)
    assert (actual.getValue(' ')==None)
    assert (actual.getValue('abc')==None)
    assert (actual.getValue(':abc')==None)
    assert (actual.getValue('# a: abc') == 'abc') # never use hash level lines for constants
    assert (actual.getValue('# a:abc') == 'abc')
    assert (actual.getValue('# a : abc') == 'abc')

    #exit(0)
    assert (actual.getValue('# a:') == {})
    assert (actual.getValue('# a:1') == 1)
    assert (actual.getValue('# a: 1') == 1)
    #print('getValue', actual.getValue('# a:1.1', stringify=True)=='1.1')
    assert (actual.getValue('# a:1.1') == Decimal('1.1'))
    assert (actual.getValue('# a: 1.1') == Decimal('1.1'))
    assert (actual.getValue('# a:True') == True)
    assert (actual.getValue('# a: True') == True)
    assert (actual.getValue('# a: False') == False)
    #print('getValue', actual.getValue('# a:, b:, c:'))
    #assert (actual.getValue('# a:, b:, c:') == None)

    #exit(0)
    assert (actual.getValue('# a:') == {})
    assert (actual.getValue('## a:') == {})
    assert (actual.getValue('### a:') == {})

    assert (actual.getValue('# a:{}') == {})
    assert (actual.getValue('# a: {}') == {})
    #print(actual.getSteps())
    assert (actual.getValue('# a:[]') == [])

    assert (actual.getValue('# a: [C]') == ['C'])
    assert (actual.getValue('# a: [C,R,U,D]') == ['C', 'R', 'U', 'D'])
    assert (actual.getValue('# a: [1]') == [1])
    assert (actual.getValue('# a: [1,2]') == [1,2])
    assert (actual.getValue('# a: [1,a]') == [1, 'a'])
    assert (actual.getValue('# a: [1,a,2.0]') == [1, 'a', 2.0])
    assert (actual.getValue('# a: [1,a,2.0,True]') == [1, 'a', 2.0, True])

    #assert (actual.getValue('# a: [[]]') == [[]])

    assert (actual.getValue('1. a:abc') == 'abc')
    assert (actual.getValue('1. a: abc') == 'abc')
    assert (actual.getValue('1. a:1') == 1)
    assert (actual.getValue('1. a: 1') == 1)
    assert (actual.getValue('1. a:1.1') == Decimal('1.1'))
    assert (actual.getValue('1. a: 1.1') == Decimal('1.1'))
    assert (actual.getValue('1. a:"1.1"') == '1.1')
    assert (actual.getValue('1. a: "1.1"') == '1.1')
    assert (actual.getValue('1. a:True') == True)
    assert (actual.getValue('1. a: True') == True)
    assert (actual.getValue('1. a:, b:, c:') == {'a': '', 'b': '', 'c': ''})
    assert (actual.getValue('1. a:, b:B') == {'a': '', 'b': 'B'})
    assert (actual.getValue('1. a:, b:B, c:True') == {'a': '', 'b': 'B', 'c': True})
    assert (actual.getValue('1. a:, b:B, c:True, d:False') == {'a': '', 'b': 'B', 'c': True, 'd': False})
    assert (actual.getValue('1. a:, b:B, c:True, d:False, e:1') == {'a': '', 'b': 'B', 'c': True, 'd': False, 'e': 1})
    assert (actual.getValue('1. a:, b:B, c:True, d:False, e:1, f:1.1') == {'a': '', 'b': 'B', 'c': True, 'd': False, 'e': 1, 'f': Decimal('1.1')})
    #assert (actual.getValue('1. name: id, type:C, size:3-330, validate:R') == {'name': 'id', 'type': 'C', 'size': {'min':3, 'max': 330}, 'validate': 'R'})

    #exit(0)

    assert (actual.getValue('1. a:{}') == {})
    assert (actual.getValue('1. a: {}') == {})
    assert (actual.getValue('1. a:[]') == [])
    assert (actual.getValue('1. a: []') == [])
    #exit(0)

    actual = LbConfigMd()

    actual.set_md_text(example_md.toString())
    pprint(actual.toJSON())

if __name__ == "__main__":
    # execute as script
    main()