# class LbTextFile(list, LbRecorder):

 Open and Save text file

__Get filename on request__

* returns filename

__Set Filename on request__

* return self

 __Get folder name on request__

* returns folder name

 __Set folder name on request__

* returns self

 __Confirm text file exists on request__

* text file exists when folder and text file are found

* fail when folder is not found

* fail when folder/file is not found

 __Load list of text on request__

* returns self

 __Open text file on request__

* fail when folder is not found

* fail when folder/file is not found

* returns self

__Test folder's existence on request__

* folder does not exist when folder not defined

* folder does not exist when folder is not found

* returns bool

__Test file's existance on request__

* file does not exist when file not defined

* file does not exist when file is not found

* returns bool

 __Save text file on request__

* overwrite file when save

* returns self

 __Save text file with different name on request__

* overwrite file when file exists

* returns self

 __Delete file on request__

* delete when file exists

* returns self

