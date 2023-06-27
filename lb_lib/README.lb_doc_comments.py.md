# class LbDocComments(LbTextFile):

 __Open__, __Read__, and __Convert__ "##" comments to Markdown

 Given a folder and filename, __Open__, __Read__, and __Convert__ the double hashed (ie "## ") comment lines to Markdown.

* __Define__ words to __Decorate__ in decoration list

 __Load line list on request__

* __Load__ line __When__ line starts with "class"

* __Convert__ "class" to "## class" __When__ line starts with "class"

* __Load__ comment __When__ line starts with "##"

 __Convert a single comment to Markdown on request__

* comment is ignored __When__ comment starts with a single hash, eg "# "

* markdown is H1 __When__ line starts with "class"

* markdown is normal __When__ comment starts with "## "

* markdown is unordered __When__ comment starts with "##*"

* markdown is H1 __When__ comment starts with "### "

* markdown is H2 __When__ comment starts with "#### "

* markdown is H3 __When__ comment starts with "##### "

__Decorate line on request__

* __Decorate__ word with bold __When__ word is found in decoration list

 __Save markdown on request__

* __Impute__ file name, eg "lb_doc_comments.py" to "README.lb_doc_comments.py.md"

