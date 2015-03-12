# How to Break the Process Down into Steps #

You can run all three steps at once as in the example above (using --step1 --step2 --step3), but it takes some time to get through all of them. Sometimes you'll want to break things down more and run the steps separately to experiment. To run one step at a time, just use a command line like the one in the example above, but only include --step1, --step2, or --step3, rather than all three. After each step, Cytoseg puts the intermediate results in files on disk that will be used for the next step.


### Step 1 ###

Processing input data can take a long time, so you probably want to start by process just a small part of it to see how well it works and adjust parameters. The step 1 (specified with --step1) just classifies the input data. You can make the input data small or use --voxelProcessingUpperBound and --contourTrainingLowerBound to set what subvolume of the input data you want to process. You can run step 1 over and over by itself adjusting parameters to see what the effect is on the data in the voxelOutput folder.

Results from step 1 can be found as a stack of images representing a probability map in the folder: ```
 <your_output_folder>\voxelOutput\mitochondria\resized ```


### Step 2 ###

Step 2 (specified with --step2) will classify the training image data. This is a step that needs to be done before step 3 will run. It classifies the training data in the same way that step 1 classifies the input data.


### Step 3 ###

Step 3 finds contours, classifies them, and generates 3D blobs. This step usually runs much faster than steps 1 and 2 because it does not involved classification of every voxel. It just involves classification of contours pairs. (There are far fewer contour pairs than voxels.) Assuming you have run step 1 and step 2, and you are adjusting --contourListWeights or --contourListThreshold=0.8, you only need to run step 3 to get the change.

Results from step 3 can be found as a stack of binary images in the folder: ```
 <your_output_folder>\voxelOutput\blobs\resized ```