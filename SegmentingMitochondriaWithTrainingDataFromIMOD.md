# Using IMOD to create training data and view or edit results #

These instructions show use of the command line on a Linux-based or similar operating system system.

## Introduction ##

[IMOD](http://bio3d.colorado.edu/imod/) is a mature software package widely used for segmentation with 3D electron microscopy. It is suitable for creating training data, editing, and viewing segmentation results.


## Note ##

In this document, ```
/home``` represents your working folder. On your computer, it may be something like /home/yourname. You can use whatever folder you want, as long as you have read/write access.


## Training data ##

This process requires a training data set. In the training data, structures that we are interested in must have been outlined in IMOD. You choose how much training data you want to use. More training data (i.e., more manually traced structures) typically makes the process more accurate. In our example we'll refer to this training data set:

/home/myOriginalData.mrc (the training data file)

/home/myManualSegmentation.mod (the corresponding model file)

You'll also have a full dataset that you want to process automatically. We call this myOriginalData.mrc in this example. This file can be (but does not have to be) the same as the training data file.


## Creating data image stack ##

Convert your image data to an 8bit tif stack:
```

mrcbyte myOriginalData.mrc byteData.mrc
```

Note: origialData.mrc is the 3D image you have traced in IMOD and byteData.mrc is the name of the output file you want to use.


Convert your data to a tif stack
```

mkdir /home/dataFolder
mrc2tif byteData.mrc /home/dataFolder/file
```

## Creating training segmentation image stack ##

You'll need an IMOD model where you have traced objects (such as mitochondria) existing in the data. This will serve as training data.

Convert your IMOD model file to a bitmap form:

Using this command
```
 imodmop model data output ```
model: model file
data: data file that goes with the model (mrc format)
output: output file (mrc format)

```
imodmop -mask 1 /home/myManualSegmentation.mod /home/myOriginalData.mrc trainingSeg.mrc```

For the example, you can look at the output with:
```
 3dmod trainingSeg.mrc ```

Convert to 8 bit:
```
 mrcbyte trainingSeg.mrc trainingSeg8bit.mrc ```

Convert the output mrc file from the last step to tif's with the command mrc2tif

Here's an example, first we are creating the "/home/trainingSegTiffs" folder as a folder to place our files.
```

mkdir /home/trainingSegTiffs
mrc2tif trainingSeg8bit.mrc /home/trainingSegTiffs/file
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

(Inside of the output folder, go to voxelOutput/primaryObject/composite to view your output in a convenient colorized form. This is useful for checking if the output looks correct.)

Inside of the output folder, voxelOutput/blobs/resized has a grayscale image of your output that can be thresholded with a program such as ImageJ to identify the structures of interest. Next, convert this output to IMOD format.

Use tif2mrc to create segmentation.mrc from the tif's in the voxelOutput/blobs/resized folder.

## Converting autosegmentation output into IMOD model ##

```
 imodauto -h 100 segmentation.mrc contours.mod ```

Optional: now you can check it with 3dmod:
```
 3dmod /home/myOriginalData.mrc contours.mod ```

Create mesh:
```
 imodmesh contours.mod ```

Finally, this sorts the contours by the surface # they have been meshed into:

```
 imodsortsurf -s contours.mod sortedContours.mod ```

To view the final result model you can use this:
```
 imod /home/myOriginalData.mrc sortedContours.mod ```



# Acknowledgements #
Thanks Andrew Noske & Alex Perez for the instructions about converting into IMOD format.


# Etc #
Note for new users: use copy and paste heavily to speed up your work with the command line.