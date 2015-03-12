# Introduction #

The Cytoseg command line takes a set of parameters to specify the input, the training, and various processing parameters.

### Training Data ###
Cytoseg uses a training image and training segmentation to learn about how to segment the structures of interest. Training images and training segmentations are represented as image stacks and they must align exactly, and they should have the same dimensions This means that the size of the images and the number of images in the stack should be the same.

Note: If your training labels use nonzero values for the object, and 0 for other, you should use the parameter --labelConfigFile=settings2.py


## Example Tutorial for Segmenting Mitochondria: ##

(Input and training images for this example are included in the svn download.)

Parameters used in this example:
  * Input images folder (data that is to be processed): data\example\input
  * Output folder: output
  * Training images folder: data\example\train\_images
  * Training segmentation folder: data\example\train\_seg


(You will have the test data for this sample if you checked out via svn.)

Example (for Windows):
```

svn checkout http://cytoseg.googlecode.com/svn/trunk/ cytoseg-read-only
cd cytoseg-read-only
cd cytoseg
cd testing
mkdir output
python run_pipeline.py data\example\input output --trainingImage=data\example\train_images --trainingSeg=data\example\train_seg  --voxelTrainingLowerBound=*,*,* --voxelTrainingUpperBound=*,*,* --voxelProcessingLowerBound=*,*,* --voxelProcessingUpperBound=*,*,* --contourTrainingLowerBound=*,*,* --contourTrainingUpperBound=*,*,* --contourProcessingLowerBound=*,*,* --contourProcessingUpperBound=*,*,* --accuracyCalcLowerBound=*,*,* --accuracyCalcUpperBound=*,*,* --labelConfigFile=settings3.py --voxelWeights=0.0130,0.00164 --contourListWeights=7,1 --contourListThreshold=0.5 --step1 --step2 --step3
```

Example (for Linux):
```

svn checkout http://cytoseg.googlecode.com/svn/trunk/ cytoseg-read-only
cd cytoseg-read-only
cd cytoseg
cd testing
mkdir output
python run_pipeline.py data/example/input output --trainingImage=data/example/train_images --trainingSeg=data/example/train_seg  --voxelTrainingLowerBound=*,*,* --voxelTrainingUpperBound=*,*,* --voxelProcessingLowerBound=*,*,* --voxelProcessingUpperBound=*,*,* --contourTrainingLowerBound=*,*,* --contourTrainingUpperBound=*,*,* --contourProcessingLowerBound=*,*,* --contourProcessingUpperBound=*,*,* --accuracyCalcLowerBound=*,*,* --accuracyCalcUpperBound=*,*,* --labelConfigFile=settings3.py --voxelWeights=0.0130,0.00164 --contourListWeights=7,1 --contourListThreshold=0.5 --step1 --step2 --step3
```


In this example, the result stack will be written to output\voxelOutput\blobs\resized

To view the results superimposed on the original images, view the result stack in the folder output\voxelOutput\blobs\composite

Note: An intermediate result, the probability map, will be in the folder output\voxelOutput\primaryObject\resized


### Example Result: ###

Here is the result image stack from output\voxelOutput\blobs\composite

![http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/mito_example_animated.gif](http://cytoseg.googlecode.com/svn/trunk/cytoseg/docs/mito_example_animated.gif)

Note: there is a 30 pixel border around the image that is not processed. It has been cropped from the animated stack above.



<pre>


</pre>

# Topics #

  1. [Breaking the process down into steps for more efficient testing](Steps.md)
  1. [Balancing examples to improve accuracy](BalancingExamples.md)
  1. [Using bounds in the command line](Bounds.md)