
source LbDocComments(LbTextFile)

## __Convert__ a python file to a __Markdown__ document
* __Define__ words to __Decorate__ in decoration list
## __Decorate__ line on request
> Bold the key words
* __Decorate__ word with bold __When__ word is found in decoration list ... [x] has test
* __Output__ string/line ... [x] has test
## __Load__ line list on request
> __Collect__ the double hash lines and strip the comment hashes
* __Load__ line __When__ line starts with "class" ... [x] has test
* __Load__ comment line __When__ line starts with "##" ... [x] has test
* __Ignore__ comment __When__ comment line starts with a single hash, eg "# " ... [x] has test
* __Ignore__ uncommented line ... [x] has test
* __Output__ LbDocComments ... [x]
## __Convert__ a single comment to __Markdown__ on request
> __Markdown__ is encoded after the double hash
* __Make__ the class line bigger, eg "class Abc()" -> "# class Abc()"
* strip the double hash "##" from line, eg. "##* hi" --> "* hi"
## __Save__ __Markdown__ on request
> __Change__ file name, dont overwrite the source file
* __Impute__ file name, eg "lb_doc_comments.py" to "README.lb_doc_comments.py.md"
