import unittest
from pylyttlebit.lb_doc_comments import LbDocComments

class LbDocCommentsTest(unittest.TestCase):
    def setUp(self):
        self.actual = LbDocComments()
    def test_decorate(self):
        line = 'change the load function when needed'
        result = self.actual.decorate(line)

        self.assertEqual(result, '__Change__ the __Load__ function __When__ needed')
        self.assertTrue(type(result) is str)
    def test_load(self):

        # load line when line starts with "class"
        result = self.actual.load(['class LbDocComments(LbTextFile):'])
        self.assertTrue('## class LbDocComments(LbTextFile)', result)

        # load comment when line starts with "##"
        result = self.actual.load(['## load me'])
        self.assertTrue(' __Load__ me' in result)

        ##* comment is ignored when comment starts with a single hash, eg "# "
        result = self.actual.load(['# dont load me'])
        self.assertTrue(' dont load me' not in result)

        ##* uncommented line is ignored
        result = self.actual.load(['dont load me either'])
        self.assertTrue('dont load me either' not in result)

        ##* output: LbDocComments
        self.assertTrue(type(result) is LbDocComments)

    def test_markdown(self):
        ##* comment is ignored when comment starts with a single hash, eg "# "
        ##* markdown is H1 when line starts with "class"
        ##* markdown is encoded after the "##", eg. "##* hi" --> "* hi"

        pass

    def test_save(self):
        pass


if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()