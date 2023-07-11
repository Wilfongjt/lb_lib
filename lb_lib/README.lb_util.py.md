# class LbUtil()
## Copy source folder and files on request
* Copy fails __When__ source folder doesnt exist ... [x] has test
* Copy fails __When__ destination folder is contained in source folder ... [x] has test
* dont overwrite destination folder __When__ found ... [x] has test
* copy source folder, subfolders, and files to destination folder __When__ source folder is found ... [x] has test
* return LbUtil ... [x] has test
## Create all folders in a given path on request
* create all folders __When__ needed ... [x] has test
* return LbUtil ... [x] has test
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
