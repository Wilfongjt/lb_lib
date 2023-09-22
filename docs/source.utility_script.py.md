
source UtilityScript(dict, LbRecorder)

## copy file to another folder
## Test if a given folder exists on request
* folder exists __When__ found on drive ... [x] has test
* returns bool ... [x] has test
## Test if a given folder and file exist on request
* file exists __When__ folder exists and file exists ... [x] has test
* return bool ... [x] has test
## Get List of File Names on request
* return [] __When__ folder is None ... [x] has test
* returns [] __When__ folder NOT found ... [x] has test
* returns [] __When__ no files found ... [ ] has test
* return all files __When__ ext = "*" ... [x] has test
* return files __When__ file has specified extention ... [x] has test
* return list of filenames __When__ files found [x] has test
## Generalize Fail
