# SegmentationManager class, which is used to run segmentation steps

import sys

from component_detector import *

class SegmentationManager:
    """Runs segmentation steps"""

    def __init__(self, parameterDict, voxelClassificationIteration=0,
                 guiVisible=True):
        """
        Initialize segmentation manager.
        Parameters:
        parameterDict: segmentation parameters as described in run_step.py
        voxelClassificationIteration: current iteration when using series architecture
        guiVisible: True if GUI is to be shown, False otherwise
        """

        target_depricated = 'not_set'

        dataIdentifier = 'default'
        mode = 'default_test'

        # use for old mitochondria detection
        #contourListClassificationMethod='bayes'

        contourListClassificationMethod='randomForest'
        
        if guiVisible:
            self.app = wx.PySimpleApp()
        self.dataViewer = ClassificationControlsFrame(makeClassifyGUITree(),
                                                      guiVisible=guiVisible)
        if guiVisible:
            self.dataViewer.Show()

        print "mode: %s" % mode
        
    
        labelFilePaths = odict()
        labelFilePaths['not_set'] = odict()
        labelFilePaths['not_set']['all'] = parameterDict['voxelTrainingLabelFilePath']
    
        
        
        self.componentDetector = ComponentDetector(
            dataViewer=self.dataViewer,
            dataIdentifier=mode,
            target='not_set',
            originalImageFilePath=parameterDict['originalImageFilePath'],
            contourListClassificationMethod=contourListClassificationMethod,
            #contourListExamplesIdentifier="contourPathFeatures" + "_" + target,
            #contourListTrainingExamplesIdentifier="contourPathFeatures" + "_" + target,
            contourListExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
            contourListTrainingExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
            voxelTrainingImageFilePath=parameterDict['voxelTrainingImageFilePath'],
            voxelTrainingLabelFilePath=parameterDict['voxelTrainingLabelFilePath'],
            voxelClassificationIteration=voxelClassificationIteration,
            labelFilePaths=labelFilePaths[target_depricated])
    
        self.componentDetector.voxelClassificationMethod = 'randomForest'

        self.componentDetector.blobImageStackOutputFolder =\
            parameterDict['blobImageStackOutputFolder']

        self.componentDetector.numberOfLayersToProcess = None
    
        # tested with mitochondria
        self.componentDetector.numberOfThresholds = 7 #5 #2 #5 #1 #1 #4
        self.componentDetector.firstThreshold = 30 #20 #160 #0.05 #0.4 #0.2
    
        self.componentDetector.thresholdStep = 36 #40 #80 #40 #0.05

        self.setTarget('mitochondria')


    def setTarget(self, target):
        """Set name of target object. e.g. 'mitochondria'"""

        self.componentDetector.target = target


    def run(self, steps):
        """Run a step set"""

        # Load input image and classify voxels
        if steps == 'classifyVoxels':

            self.componentDetector.runInitialize()
            self.componentDetector.runLoadTrainingData()
            self.componentDetector.runLoadInputImage()
            self.componentDetector.runClassifyVoxels()
            self.componentDetector.runWriteInputVoxelClassificationResult()


        # Classify voxels in training data set and output to training output folder.
        # This is needed because training contour lists are extracted based on this
        # output.
        elif steps == 'classifyVoxelsAndUseTrainingOutputFolder':

            self.componentDetector.runInitialize()
            self.componentDetector.runLoadTrainingData()
            self.componentDetector.runLoadInputImage()
            self.componentDetector.runClassifyVoxels()
            self.componentDetector.runWriteTrainingVoxelClassificationResult()


        # Run radon-like features voxel classification process.
        # Used for comparison to cytoseg. Uses matlab code from external authors.
        elif steps == 'randonLikeFeaturesProcess':
            self.componentDetector.runInitialize()
            self.componentDetector.runLoadInputImage()
            #todo:
            #runWriteInputImage()
            self.componentDetector.runRadonLikeFeaturesProcess()


        # Compute accuracy on voxel by voxel basis.
        elif steps == 'voxelAccuracy':

            self.componentDetector.runInitialize()
            self.componentDetector.runLoadInputImage()
            self.componentDetector.calculateVoxelClassificationAccuracy_new()


        # Extract training contours.
        elif steps == 'findTrainingContours':

            self.componentDetector.runInitialize()
            #self.componentDetector.runLoadInputImage()
            self.componentDetector.runLoadContourProcessingTrainingImage()
            self.componentDetector.runLoadTrainingProbabilityMap()
            #self.componentDetector.runClassifyVoxels()
            self.componentDetector.runFindTrainingContours()
            #self.componentDetector.runWriteContoursToImageStack()
            #self.componentDetector.runContourProbabilityFilter()
            #self.componentDetector.runGroupContoursByConnectedComponents()


        # Extract input contours.
        elif steps == 'findInputContours':

            self.componentDetector.runInitialize()
            self.componentDetector.runLoadContourProcessingInputImage()
            self.componentDetector.runLoadInputProbabilityMap()
            self.componentDetector.runFindInputContours()
            #self.componentDetector.runWriteContoursToImageStack()
            #self.componentDetector.runContourProbabilityFilter()


        # Test find input contours process.
        elif steps == 'findInputContoursTest':

            self.componentDetector.runInitialize()
            self.componentDetector.runLoadContourProcessingTrainingImage()
            self.componentDetector.runLoadTrainingProbabilityMap()
            self.componentDetector.runFindTrainingContours()

            self.componentDetector.runLoadContourProcessingInputImage()
            self.componentDetector.runLoadInputProbabilityMap()
            self.componentDetector.runFindInputContours()


        # Classify training contours.
        elif steps == 'classifyTrainingContours':

            self.componentDetector.runInitialize()
            #self.componentDetector.runLoadInputImage()
            self.componentDetector.runLoadContourProcessingTrainingImage()
            self.componentDetector.runLoadTrainingProbabilityMap()
            self.componentDetector.runLoadContourProcessingInputImage()
            self.componentDetector.runComputeContourRegions()
            self.componentDetector.runMakeTrainingContourLists()
            self.componentDetector.runCalculateTrainingContourListFeaturesTask()
            self.componentDetector.runTrainingContourListClassifier()


        # Classify input contours.
        elif steps == 'classifyInputContours':

            self.componentDetector.runInitialize()
            self.componentDetector.runLoadContourProcessingTrainingImage()
            self.componentDetector.runLoadInputProbabilityMap()
            self.componentDetector.runLoadContourProcessingInputImage()
            self.componentDetector.runMakeInputContourLists()
            self.componentDetector.runCalculateInputContourListFeaturesTask()
            self.componentDetector.runInputContourListClassifier()


        # Write all input contours to image stack for viewing.
        elif steps == 'writeAllInputContoursToImageStack':

            #self.componentDetector.runWriteContoursToImageStack()
            self.componentDetector.runWriteInputContoursToBinaryImageStack()


        # Filter out contour lists that have low probability of belonging to a single object.
        elif steps == 'inputContourListProbabilityFilter':

            self.componentDetector.runLoadContourProcessingInputImage()
            self.componentDetector.runContourListProbabilityFilter()


        # Fill 3D blobs will level set operation
        elif steps == 'fill3DBlobs':

            #self.componentDetector.runLoadInputImage()
            self.componentDetector.runLoadContourProcessingInputImage()
            self.componentDetector.runInitialize()
            self.componentDetector.runFill3DBlobsFromContourListsHighProbabilityOnly()
            self.componentDetector.runWrite3DBlobsVolume()


        # Compute accuracy for a single biological structure type
        elif steps == 'accuracy':

            #self.componentDetector.runLoadAccuracyCalcData()
            self.componentDetector.runCalculateVoxelClassificationAccuracySingleComponent()


        #elif steps == True:
        elif steps == 'groupContours':

            self.componentDetector.runInitialize()
            self.componentDetector.runLoadInputImage()
            self.componentDetector.runClassifyVoxels()
            self.componentDetector.runFindContours()
            self.componentDetector.runGroupContoursByConnectedComponents()

        else:

            raise Exception, "Invalid steps parameter: %s" % str(steps)

        if self.dataViewer.guiVisible:
            self.app.MainLoop()

