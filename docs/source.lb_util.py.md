
source LbUtil()

## Copy source folder and files on request
* Copy fails __When__ source folder doesnt exist ... [x] has test
* Copy fails __When__ destination folder is contained in source folder ... [x] has test
* dont overwrite destination folder __When__ found ... [x] has test
* copy source folder, subfolders, and files to destination folder __When__ source folder is found ... [x] has test
* return LbUtil ... [x] has test
## Create all folders in a given path on request
* create all folders __When__ needed ... [x] has test
* return LbUtil ... [x] has test
## Get the Current Folder Name on request
* remove "_scripts" folder name __When__ found
* return str
## __Delete__ file on request
* __Delete__ file __When__ folder and file are found ... [x] has test
* __Skip__ file __Delete__ __When__ folder and file are NOT found ... [x] has test
* return LbUtil ... [x] has test
## __Delete__ folder on request
* remove all files and folders in folder ... [x] has test
* return LbUtil ... [x] has test
## __Delete__ all files in a folder on request
* __Delete__ all files __When__ files are found in a folder ... [x] has test
* return LbUtil ... [x] has test
## Get an LbEnvironment Value by name
* use name to find key in os.environ
* return value __When__ found ... [x] has test
* return "TBD" __When__ not found ... [x] has test
* returns str ... [x] has test
## Calculate the age of a file
* age is system datetime - file datetime ... no test
* age is greater than or equal to zero ... [x] has test
* returns a float  ... [x] has test
## Test if a given folder and file exist on request
* file exists __When__ folder exists and file exists ... [x] has test
* return bool ... [x] has test
## Test if a given folder exists on request
* folder exists __When__ found on drive ... [x] has test
* returns bool ... [x] has test
## Get file extension on request
* return extension/string ... [x] has test
## Get List of File Names on request
* return [] __When__ folder is None ... [x] has test
* returns [] __When__ folder NOT found ... [x] has test
* returns [] __When__ no files found ... [ ] has test
* return all files __When__ ext = "*" ... [x] has test
* return files __When__ file has specified extention ... [x] has test
* return list of filenames __When__ files found [x] has test
## Get List of Folder Names on request
* return [] __When__ folder is None ... [x] has test
* returns [] __When__ folder NOT found ... [x] has test
* returns [] __When__ no folders found ... [x] has test
 return list ... [x] has test
__Check for empty file on request__
* empty __When__ folder is None
* empty __When__ filename is None
* empty __When__ folder not found
* empty __When__ file is not found
* empty __When__ size of file is 0
* file is empty __When__ has no lines ... [ ] has test
* not empty __When__ size of file is NOT 0
