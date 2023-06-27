# class LbTextFile(list, LbRecorder):

 __Open__ and __Save__ text file

__Get filename on request__

* returns filename

__Set Filename on request__

* return self

 __Get folder name on request__

* returns folder name

 __Set folder name on request__

* returns self

 __Confirm text file exists on request__

* text file exists __When__ folder and text file are found

* fail __When__ folder is not found

* fail __When__ folder/file is not found

 __Load list of text on request__

* returns self

 __Open text file on request__

* fail __When__ folder is not found

* fail __When__ folder/file is not found

* returns self

__Test folder's existence on request__

* folder does not exist __When__ folder not defined

* folder does not exist __When__ folder is not found

* returns bool

__Test file's existance on request__

* file does not exist __When__ file not defined

* file does not exist __When__ file is not found

* returns bool

 __Save text file on request__

* overwrite file __When__ save

* returns self

 __Save text file with different name on request__

* overwrite file __When__ file exists

* returns self

 __Delete file on request__

* delete __When__ file exists

* returns self

