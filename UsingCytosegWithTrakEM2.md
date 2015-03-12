# Using TrakEM2 for training data and viewing results in ImageJ / Fiji #


## Introduction ##

Fiji (with TrakEM2) is a software package widely used for segmentation with 3D electron microscopy. It is suitable for creating training data, editing, and viewing segmentation results.

If you are new to TrakEM2, there are tutuorials here: http://www.ini.uzh.ch/~acardona/trakem2.html

## Note ##

In this document, ```
/home``` represents your working folder. On your computer, it may be something like /home/yourname. You can use whatever folder you want, as long as you have read/write access.



## Creating data image stack ##

Convert your image data to an 8bit tif stack and place it in /home/dataFolder


## Creating training segmentation image stack ##

You'll need a TrakEM2 project open where you have traced mitochondria existing in the data. This will serve as training data.

Right click in TrakEM2 and export your labels to TIFF format:

Use ImageJ to convert the TIFF stack to 8bit and save the stack here:
```

/home/trainingSegTiffs
```



## Running the script ##

Make sure you have python installed according to instructions for installation at cytoseg.googlecode.com

You'll need python to run the scripts.

You can download from the command line with:
```

svn checkout http://cytoseg.googlecode.com/svn/trunk/ cytoseg-read-only
```

At your command line, go into the cytoseg/testing directory

```

cd cytoseg
cd testing
```

Create and output folder:
```

mkdir /home/outputFolder
mkdir /home/outputFolder/cytoseg_data
```

Next we'll use the run\_pipeline\_test.py command.

[CommandLine](CommandLine.md) information

For our example, the particular command would be:

```



python run_pipeline_test.py /home/dataFolder /home/outputFolder --trainingImage=/home/dataFolder --trainingSeg=/home/trainingSegTiffs  --voxelTrainingLowerBound=*,*,* --voxelTrainingUpperBound=*,*,* --voxelProcessingLowerBound=*,*,* --voxelProcessingUpperBound=*,*,* --contourTrainingLowerBound=*,*,* --contourTrainingUpperBound=*,*,* --contourProcessingLowerBound=*,*,* --contourProcessingUpperBound=*,*,* --accuracyCalcLowerBound=*,*,* --accuracyCalcUpperBound=*,*,* --labelConfigFile=settings2.py --voxelWeights=0.0130,0.00064 --contourListWeights=7,1 --contourListThreshold=0.8 --step1 --step2 --step3

```



During the process, new folders and files will be created in the output folder you specified (/home/outputFolder).

(Inside of the output folder, go to voxelOutput/mitochondria/composite to view your output in a convenient colorized form. This is useful for checking if the output looks correct.)

Inside of the output folder, voxelOutput/blobs/resized has a grayscale image of your output that can be thresholded with a program such as ImageJ to identify the structures of interest.


## Editing Cytoseg output in TrakEM2 ##

You'll want to load both the original images and the (1) automatic segmentation and (2) Cytoseg output into TrakEM2.

### (1) Loading your original images into TrakEM2 ###

Use ImageJ to convert your input stack into an AVI and then open the AVI in TrakEM2.

Reason for this: During my testing, for some reason TrakEM2 did not load a stack of PNGs. So I converted them to an AVI (with ImageJ). When I opened the AVI in TrakEM2, it worked fine.


### (2) Loading the output from Cytoseg into Fiji's TrakEM2 as labels ###

In Fiji, open the output stack located here voxelOutput/blobs/resized

Threshold the stack to make the blobs white and the background black.

Use the connected components tool (Plugins->Process->Find Connected Regions) in plugins to create separate labels for each blob. Now you have a label volume that can be imported into TrakEM2 and edited.

