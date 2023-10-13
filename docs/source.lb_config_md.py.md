
source LbConfigMd(LbTextFile)

## Set a block of __Markdown__ text to be evaluated on request
* Use for testing
## Determine level of line by counting the leading # on request
## Retrive a suitable key value for a name and value pair on request
* Deprecated
## __Convert__ a line string to parsable string on request
## Retrieve the value of nome and value pair on request
## Determine if a string represents a proper integer on request
## Determine if a string represents a proper float on request
## Determine if a string represents a proper boolean on request
## Determine if a string represents a size range on request
* eg 3-330
## __Convert__ a string to one of the supported types on request
* '1' -> integer
* '1.1' -> float
* '1.1' -> decimal(3,1)
* 'True' -> boolean
* 'False' -> boolean
* '3-330' -> {'max' 330, 'min' 3} -> size-range
* 'abc' -> string
## __Convert__ __Markdown__ text to JSON object on request
## Fix dangling lines before parsing on request
* '# project ' --> '# project  '
* '# project  ' --> '# project  {}'
* '1. project' --> "1. project  "
## Match a line to a given regular expression on request
