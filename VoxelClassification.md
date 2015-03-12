[Voxel Classification Rough Notes and Flowchart](http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/voxel_classification.pdf)

To run this example

  * change directory to cytoseg/testing/
  * run the command python voxel\_classification.py

In this example variables are set to the following default values:

```
voxelTrainingImageFilePath = "data/membrane_training/image"
voxelTrainingLabelFilePath = "data/membrane_training/label"
inputImageFilePath = "data/membrane"
```

You can edit voxel\_classification.py to change these parameters:

  * voxelTrainingImageFilePath - set this to the path of the image stack that will train the classifier
  * voxelTrainingLabelFilePath - set this to the path of the training pixel stack. This stack should have pixels with value 1 were the membrane is and 0 where it is not.
  * inputImageFilePath - set this to the path of your input data set

A window will pop up when this file runs.

Processing takes some time and the console output will report progress.

Note:
To use the full gui, you'll need to resize the window labeled `ParticleMotionTool`, this will make scroll bars appear. (This is a work around for a bug - the scroll bars don't appear at startup.)

To view output as it is generated,
  * make sure data tree for volume selection is set to `outputDataLabel1_ProbabilityVolume`
  * adjust zIndex in the `imageControls` window

When processing completes, to save the the output to an image stack:
  * make sure data tree for volume selection is set to `outputDataLabel1_ProbabilityVolume`
  * press `saveCurrentlyDisplayedVolume` button, you will have to scroll down to find it



![http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/voxel_classification_progress.png](http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/voxel_classification_progress.png)