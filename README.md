# secureDICOM
## Introduction
DICOM(Digital Communications in Medicine) is a way of exchanging data that has been adopted by the majority of healthcare administrators. DICOM governs how patient, study, image, and other objects are described and transported across a network, and transmitted and store. secureDICOM provides an easy way to view DICOM images(such as CT scan, MRI, ect...) as well as edit any data element or anonymize the whole dataset. See below for all the currently supported features.

## Supported Features
- Importing a stack of DICOM files(as in multiple different files each with an image to compose a 3D volume) 
- Importing a multiframe DICOM file(1 DICOM file with multiple images)
- Viewing DICOM images. If there are multiple frames the users can scroll through the different frames and also choose a monoplanar or multiplanar view.
- View Full Data Frame(all elements within DICOM file) organized by group
- View All Private Data Elements(compare current dataset with a cloud database of know elements and select those not in the collection of known elements as private data elements)
- Customly Edit any element
- Add any element
- Delete any element
- Anonymize DICOM file(compare current dataset with a cloud database of elements identified in appendix E of the DICOM standard that need to be altered or anonymized. Private data elements are also selected for anonymization)
- Export your edited DICOM file to your local computer

## Instructions on how to use
- Docker image: https://hub.docker.com/repository/docker/wjbradfo/securedicom
- Users can pull the above image by first starting the Docker Daemon, then pulling it to their local machine: docker pull wbradfo/securedicom:prototype1
- NOTE: this application uses a graphical user interface. Thus, to use it you need to allow docker to use your screen. This is a different process on different operating systems, so no description is given here, but note that you will need to run the container as you would any other GUI image from docker.
- NOTE: to upload images from your computer, you must create a volume that links wherever the DICOM files are to your container

## Tutorial
Below is a tutorial for the basic menu buttons.
### File
#### Import Files(s)
- Click on this an a File Dialog will appear. Select the files you wish to View. NOTE: you will need to have created a volume that links your images to your repository.
#### Export
- Export your DICOM file to your local computer. 
#### Clear
- Clear whatever file you have imported.
#### Exit
- Exit the program
### Options
#### Edit Data Element(s)
- Allows you to Edit, add, or delete Any Data Element. WARNING: Some data elements are required by the DICOM standard, and deleting them or editing them in a certain way might make your DICOM file unreadable or violate the DICOM standard.
#### Anonymize
- Checks a cloud database for all the items itentified in the DICOM standard table E.1-1 that need to be deleted or edited for the file to be anonymized(for "basic proficiency"). Also selects all private elements. You can delete or edit any element but as with above ^  Some data elements are required by the DICOM standard, and deleting them or editing them in a certain way might make your DICOM file unreadable.
#### Load Monoplanar View
- Loads Monoplanar view if Multiplanar View is currently active.(Only available for multiple frames)
#### Load Biplanar View
- Loads Biplanar view if Biplanar View is currently active.(Only available for multiple frames)
#### View Full DataFrame
- View All Data Elements oragnized by group
#### View Private Data Elements
- View all private Data Elements organized by group(private elements are selected by comparasin with a cloud database of known elements)

