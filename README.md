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
- ### Method 1: using conda environment
  - Step 1: Make sure Python 3 and Conda are installed on your machine
  - Step 2: Initialize Git
  ```consol
  git init
  ```
  - Step 3: Clone the repository on your machine(this may take a while).
  ```console
  git clone https://github.com/wbradford2001/secureDICOM
  ```
  - Step 4: Navigate to the new Directory
  ```console
  cd secureDICOM
  ```
  -Step 5: Build new environment from "environment.yml"
  ```console
  conda env create --file environment.yml --name env_from_file
  ```
  -Step 6: Activate new environment
  ```console
  conda activate env_from_file
  ```
  - Step 7: Run master.py and enjoy!
  ```console
  python3 master.py
  ```
- ### Method 2: using Docker image
  - Step 1: Make sure Docker is installed on your machine
  - Step 2: Start the Docker Daemon
  - Step 3: Pull down the Docker image onto your machine:
    Docker image: https://hub.docker.com/repository/docker/wjbradfo/securedicom
    As of the time of this writing, the most current tag is "prototype1", however there may be a more recent tag by the time you read this. So feel free to use it.
    ```console
    docker pull wjbradfo/securedicom:prototype1
    ```
  - Step 4: Run the docker container
   NOTE: Because secureDICOM is a graphical application, you need to give the container access to your display. Because this looks different on different operating systems, no command line examples are given here. Also note that you need to create a volume that maps the local DICOM files on your computer into your Docker container.



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



## Task List
- [ ] Encryption Fix:
    > Create "Encryption" Menu to help users choose which Encryption Scheme to Apply to all Elements.
- [ ] Pixel Data Editing:
    > - [ ] Crop
    > - [ ] Make custom pixel Edits(set the value of pixels with the mouse)
    > - [ ] Add/Delete Pixel Overlay Data
- [ ] DICOM Compatability Issue:
    > - [ ] Support all defined VR's
    > - [ ] Sort multiple images for correct 3D interpretation
    > - [ ] Implement Window/Leveling
    > - [ ] Display Overlay Data
    > - [ ] Display warning for deleting mandatory elements
    > - [ ] Change UIDs automatically upon editing
- [ ] DataBase Fix:
    > Store anonymization status and element type (1, 1C, 2, 2C) in centralized database
- [ ] Bug List:
    > - [ ] When there is no private data elements, have the pop up window display a message saying "no private data elements"
    > - [ ] Import Files even with no ".dcm" extension if they have the valid DICM preamble.
    > - [ ] Handle the following DICOM objects gracefully
    > > - [ ] DICOM Datasets
    > > - [ ] Structured Reports
    > > - [ ] DICOM DIR
    > - [ ] Handle the following attributes gracefully
    > > - [ ] parametric map storage
    > > - [ ] Color Palettes
 


- BONUS FEATURES TO IMPLEMENT
  - [ ] Network Capabilities:
   > - [ ] Pull:
     Ability to pull data down from a PACS(Picture Archiving and Communication Systems) Server by specifying IP address and port.
   > - [ ] Push:
     Ability to push data up to a PACS(Picture Archiving and Communication Systems) Server by specifying IP address and port.
  - [ ] TLS Layer:
   > Add TLS to Networking Capabilities
  - [ ] Export Pixel Array:
    > Ability to Export Pixel Array to 
      > - [ ] PNG
      > - [ ] JEG
  - [ ] Complete SQL Database:
   > Right now the SQL database only contains elements from the "basic proficiency" section of the DICOM standard. All columns could be scraped and stored
