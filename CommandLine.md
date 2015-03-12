This page is under construction (October 2012)


In general, the command is used like this:


python run\_pipeline\_test.py input output --trainingImage=test1 --trainingSeg=test2 --trainingLowerBound=X1,Y1,Z1 --trainingUpperBound=X2,Y2,Z2 --processingLowerBound=X1,Y1,Z1 --processingUpperBound=X2,Y2,Z2


input: the input folder with a stack of 8bit data image files (We created this in the "Creating data image stack section" above.)

output: toplevel folder for output of the process (We created this with the mkdir command above.)

--traningImage specifies the folder with training data (can be the same as input)

--trainingSeg specifies the folder with 8bit segmentation bitmap stack (We created this in the "Creating segmentation image stack" section above.)

--trainingLowerBound specifies X1,Y1,Z1 corner of training data

--trainingUpperBound specifies X2,Y2,Z2 corner of training data

--processingLowerBound specifies X1,Y1,Z1 corner of input data to be processed

--processingUpperBound specifies X2,Y2,Z2 corner of input data to be processed

<b>Use ImageJ to determine X, Y, and Z coordinates of the corners.</b>