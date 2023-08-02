# class LbDocFolders(LbTextFile)
 Given a folder, __Generate__ a text graphic of folders and files
## Get Line List
* __Make__ list of folders and files
* __Ignore__ unnessessary folders __When__ found ... no test
* add folders __When__ found ... [] has test
* add files __When__ found ... [] has test
* return list
## Set Title on request
* return LbDocFolders ... no test
## Get Title on request
* return title/str  ... no test
## Test if folder should be ignored on request
* dont __Ignore__ __When__ not in __Ignore__ list ... [] test
* __Ignore__ __When__ folder in __Ignore__ list ... [x] has test
* return bool ... [x] has test
## Dont __Save__
__Validate folder attributes on request__
* throw BadFolderNameException __When__ folder is None ... [x] has test
* throw FolderNotFoundException __When__ folder doesnt exist ... [x] has test
