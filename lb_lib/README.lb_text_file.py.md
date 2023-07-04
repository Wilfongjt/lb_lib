# class LbTextFile(list, LbRecorder):

 __Open__, __Load__ and __Save__ text file

__Get filename on request__

* returns filename  ... [x] has test

__Set Filename on request__

* return self ... [x] has test

 __Get folder name on request__

* returns folder name ... [x] has test

 __Set folder name on request__

* returns self ... [x] has test

 __Confirm text file exists on request__

* text file exists __When__ folder and text file are found

* fail __When__ folder is not found ... [x] has test

* fail __When__ folder/file is not found ... [x] has test

 __Load list of text on request__

* returns self ... [x] has test

 __Open text file on request__

* fail __When__ folder does not exist ... [x] has test

* fail __When__ file does not exist ... [x] has test

* __Load__ lines from file __When__ available

* returns LbTextFile

__Test folder's existance on request__

* folder does not exist __When__ folder not defined ... [x] has test

* folder does not exist __When__ folder is not found ... [x] has test

* true __When__ folder is found ... [x] has test

__Test file's existance on request__

* file does not exist __When__ file not defined ... [x] has test

* file does not exist __When__ file is not found ... [x] has test

* true __When__ folder and file are found ... [x] has test

 __Save text file on request__

* validate attributes

* create new file __When__ file doesnt exist ... [x] has test

* overwrite file __When__ file exists ... [x] has test

* returns LbTextFile ... [x] has test

 __Save text file with different name on request__

* return the new LbTextFile

 __Save text file with different name on request__

* fail __When__ bad folder name ... [x] has test

* fail __When__ bad file name ... [x] has test

* fail __When__ folder doesnt exist ... [x] has test

* write file with a different name __When__ new name is provided

* overwrite file __When__ file exists ... [ ] has test

* returns the new text file ... [x] has test

 __Delete file on request__

* delete __When__ file exists ... [ ] has test

* returns self ... [ ] has test

__Check for empty file on request__

* file is empty __When__ all lines in file are blank or EOL ... [ ] has test

* returns bool ... [ ] has test

__Validate file attributes on request__

* throw BadFolderNameException __When__ folder is None

* throw FolderNotFoundException __When__ folder doesnt exist

* throw BadFileNameException __When__ filename is None

