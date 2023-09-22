
source LbUtilTest(unittest.TestCase)

## Get List of File Names on request
## Test if a given folder exists on request
* folder exists __When__ found on drive ... [x] has test
* return LbUtil ... [] has test
* return [] __When__ folder is None
* returns [] __When__ folder NOT found
* return all files __When__ ext = "*"
* return files __When__ file has specified extention
* return [] __When__ folder is None
* returns [] __When__ folder NOT found
* returns [] __When__ no folders found
* return list
