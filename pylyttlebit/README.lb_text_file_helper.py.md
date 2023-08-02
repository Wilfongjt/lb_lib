# class LbTextFileHelper()
 Test that filename exists in folder
 return __When__ filename undefined
 False __When__ folder dosent exist
 False __When__ filename doesnt exist
 copy source file to another location, or name, or both
 fail __When__ source folder and source filename equal destination folder and destination filename
 print to screen __When__ nocopy == True
 remove destination file __When__ destination file exists
 __Delete__ file __When__ file is found
* throw exception __When__ trying to __Delete__ this file
 __Delete__ __When__ file exists
