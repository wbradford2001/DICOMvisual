#MyDICOMvisual
##Introduction
DICOM(Digital Communications in Medicine) is a way of exchanging data that has been adopted by the majority of healthcare administrators. DICOM governs how patient, study, image, and other objects are described and transported across a network. MyDICOMvisual provides an easy way to view DICOM images(such as CT scan, MRI, ect...) as well as edit any data element or anonymize the whole dataset. See below for all the currently supported features.

##Supported Features
-Importing a stack of DICOM files(as in multiple different files each with an image to compose a 3D volume) 
-Importing a multiframe DICOM file(1 DICOM file with multiple images)
-Viewing DICOM images. If there are multiple frames the users can scroll through the different frames and also choose a monoplanar or multiplanar view.
-View Full Data Frame(all elements within DICOM file) organized by group
-View All Private Data Elements
-Customly Edit any element
-Add any element
-Delete any element
-Export your edited DICOM file to your local computer

##Instructions on how to use
-TBD

##Task List
###Things related to DICOM datasets
-TBD
###DICOM networking
-TBD
###bugs
-TBD
###features in progress
-TBG

##Tutorial
Below is a tutorial for the basic menu buttons.
###File
####Import Files(s)
-Click on this an a File Dialog will appear. Select the files you wish to View. 
####Export
-Export your DICOM file to your local computer.
####Clear
-Clear whatever file you have imported.
####Exit
-Exit the program
###Options
####Edit Data Element(s)
-Allows you to Edit, add, or delete Any Data Element. WARNING: Some data elements are required by the DICOM standard, and deleting them or editing them in a certain way might make your DICOM file unreadable.
####Anonymize
-Checks a cloud database for all the items itentified in the DICOM standard table E.1-1 that need to be deleted or edited for the file to be anonymized(for "basic proficiency". Also selects all private elements. You can delete or edit any element but as with above ^  Some data elements are required by the DICOM standard, and deleting them or editing them in a certain way might make your DICOM file unreadable.
####Load Monoplanar View
-Loads Monoplanar view if Multiplanar View is currently active.(Only available for multiple frames)
####Load Biplanar View
-Loads Biplanar view if Biplanar View is currently active.(Only available for multiple frames)
####View Full DataFrame
-View All Data Elements oragnized by group
####View Private Data Elements
-View all private Data Elements organized by group
