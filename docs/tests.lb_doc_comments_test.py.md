
source LbDocCommentsTest(unittest.TestCase)

* comment is ignored __When__ comment starts with a single hash, eg "# "
* uncommented line is ignored
* __Output__ LbDocComments
* comment is ignored __When__ comment starts with a single hash, eg "# "
* __Markdown__ is H1 __When__ line starts with "class"
* __Markdown__ is encoded after the "##", eg. "##* hi" --> "* hi"
