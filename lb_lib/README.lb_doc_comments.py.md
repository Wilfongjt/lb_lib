# class LbDocComments(LbTextFile):

 Read and convert "##" comments to Markdown

 Given a folder and filename, Open, read, and convert the double hashed (ie "## ") comment lines to Markdown.

* save to README.md

 __Load line list on request__

* load markdown line when line starts with "class", convert "class" to "## class"

* load markdown line when line is double comment... eg "##"

 __Convert a single comment to Markdown on request__

* comment is ignored when comment starts with a single hash, eg "# "

* markdown is H1 when line starts with "class"

* markdown is normal when comment starts with "## "

* markdown is unordered when comment starts with "##*"

* markdown is H1 when comment starts with "### "

* markdown is H2 when comment starts with "#### "

* markdown is H3 when comment starts with "##### "

 __Save markdown on request__

* change name

