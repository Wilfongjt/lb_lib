
source LbTextFile(list, LbRecorder)

 __Open__, __Load__ and __Save__ text file
#### Create env file on request
* __Skip__ create __When__ env file exists
* create file __When__ file doesnt exist
 __Get folder name on request__
* returns folder name ... [x] has test
 __Set folder name on request__
* returns self ... [x] has test
__Get filename on request__
* returns filename  ... [x] has test
__Set Filename on request__
* return self ... [x] has test
## Get all lines in a text file
* __Open__ file and __Read__ text lines ... [x] has test
* return lines from a file
__Test folder's existance on request__
* folder does not exist __When__ folder is None ... [x] has test
* folder does not exist __When__ folder is not None ... [x] has test
* true __When__ folder is found ... [x] has test
__Test file's existance on request__
* file does not exist __When__ filename is None ... [x] has test
* file does not exist __When__ filename is not None ... [x] has test
* file exists __When__ folder and filename is not None and file is found ... [x] has test
 __Confirm text file exists on request__
* not exist __When__ folder is not found ... [x] has test
* not exist __When__ folder/file is not found ... [x] has test
* text file exists __When__ folder and text file are found ... [x] has test
 __Load list of text on request__
* put lines into object list
* returns LbTextFile ... [x] has test
__Validate file attributes on request__
* throw BadFolderNameException __When__ folder is None ... [x] has test
* throw FolderNotFoundException __When__ folder doesnt exist ... [x] has test
* throw BadFileNameException __When__ filename is None ... [x] has test
 __Open text file on request__
* __Load__ lines from file __When__ available
* returns LbTextFile
 __Save text file on request__
> saves contents of list to a text file
* __Validate__ attributes ... tested with validate()
* create file __When__ file doesnt exist ... [x] has test
* overwrite file __When__ file exists ... [x] has test
* returns LbTextFile ... [x] has test
 __Save text file with different name on request__
* return the new LbTextFile ... [x] has test
__Show Steps on request__
* __Show__ preview of file
 __Delete file on request__
* __Delete__ __When__ file exists ... [x] has test
* clear list ... [x] has test
* remove file for drive __When__ file exists ... [] test
* returns empty LbTextFile ... [x] has test
__Check for empty file on request__
* empty file __When__ file doesnt exist ... [x] has test
* returns bool ... [ ] has test
