
import sys

from component_detector import *

class ContourSetDetector:

    def __init__(self, parameterDict, voxelClassificationIteration=0,
                 guiVisible=True):

        #testContours()  # crash
        #target_depricated = 'vesicles'
        target_depricated = 'not_set'

        #dataIdentifier = 'hpf'
        dataIdentifier = 'default'
        #mode = 'hpf_training'
        #mode = 'hpf_test'
        mode = 'default_test'
        #defaultStepNumber = 10
        #defaultStepNumber = 3
        defaultStepNumber = 7
        #defaultStepNumber = 106

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
        
        #if len(sys.argv) < 2:
        if True:
            print "step not specified, using default step", defaultStepNumber
            stepNumber = defaultStepNumber
        else:
            stepNumber = int(sys.argv[1])    
        
        # process the contours in a small dataset to learn about them
        #if mode == 'hpf_training':
        
#        labelFilePaths = odict()
#        labelFilePaths['mitochondria'] = odict()
#        labelFilePaths['vesicles'] = odict()
#    
#        labelFilePaths['mitochondria']['process_a1'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/a1"
#        labelFilePaths['mitochondria']['process_a2'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/a2"
#        labelFilePaths['mitochondria']['process_0'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/0"
#        labelFilePaths['mitochondria']['process_1'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/1"
#        labelFilePaths['mitochondria']['process_2'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/2"
#        labelFilePaths['vesicles']['all'] = "O:/images/HPFcere_vol/HPF_rotated_tif/vesicles/label/one_label/0_to_25"
#    
#        self.contourTrainer = ComponentDetector(
#            dataViewer=self.dataViewer,
#            dataIdentifier=mode,
#            target='not_set',
#            originalImageFilePath="O:/images/HPFcere_vol/HPF_rotated_tif/vesicles/input",
#            contourListClassificationMethod=contourListClassificationMethod,
#            #contourListExamplesIdentifier="contourPathFeatures" + "_" + target,
#            #contourListTrainingExamplesIdentifier="contourPathFeatures" + "_" + target,
#            contourListExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
#            contourListTrainingExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
#            voxelTrainingImageFilePath="data/sbfsem_training/images",
#            voxelTrainingLabelFilePath="data/sbfsem_training/label",
#            labelFilePaths=labelFilePaths[target_depricated])
    
        labelFilePaths = odict()
        labelFilePaths['not_set'] = odict()
        labelFilePaths['not_set']['all'] = parameterDict['voxelTrainingLabelFilePath']
    
#        self.contourTrainer = ComponentDetector(
#            dataViewer=self.dataViewer,
#            dataIdentifier=mode,
#            target='not_set',
#            originalImageFilePath=parameterDict['originalImageFilePath'],
#            contourListClassificationMethod=contourListClassificationMethod,
#            #contourListExamplesIdentifier="contourPathFeatures" + "_" + target,
#            #contourListTrainingExamplesIdentifier="contourPathFeatures" + "_" + target,
#            contourListExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
#            contourListTrainingExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
#            voxelTrainingImageFilePath="data/sbfsem_training/images",
#            voxelTrainingLabelFilePath="data/sbfsem_training/label",
#            labelFilePaths=labelFilePaths[target_depricated])
#
#        self.contourTrainer.numberOfLayersToProcess = None
#        self.contourTrainer.numberOfThresholds = 1
#        self.contourTrainer.firstThreshold = 0.4
#        self.contourTrainer.thresholdStep = 0.2
        
        # process the contours in a full dataset
        #elif mode == 'hpf_test':
        
        self.contourClassifier = ComponentDetector(
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
    
        #self.contourClassifier.voxelClassificationInputVolumeName =\
        #    self.contourClassifier.blurredVolumeName
        self.contourClassifier.voxelClassificationMethod = 'randomForest'

        self.contourClassifier.blobImageStackOutputFolder =\
            parameterDict['blobImageStackOutputFolder']

        #self.contourClassifier.numberOfLayersToProcess = 10
        self.contourClassifier.numberOfLayersToProcess = None
    
        # for mitochondria
        self.contourClassifier.numberOfThresholds = 2 #5 #1 #1 #4
        self.contourClassifier.firstThreshold = 20 #160 #0.05 #0.4 #0.2
    
        # not for mitochondria
        #self.contourClassifier.numberOfThresholds = 1 #4
        #self.contourClassifier.firstThreshold = 0.4 #0.2
    
        self.contourClassifier.thresholdStep = 80 #40 #0.05

        self.setTarget('mitochondria')
        #self.setTarget('vesicles')
        #self.setTarget('blankInnerCell')


    def setTarget(self, target):

        #self.contourTrainer.target = target
        self.contourClassifier.target = target


    def run(self, steps=True):

        if steps == 'classifyVoxels':

            self.contourClassifier.runInitialize()
            self.contourClassifier.runLoadTrainingData()
            self.contourClassifier.runLoadInputImage()
            self.contourClassifier.runClassifyVoxels()
            self.contourClassifier.runWriteVoxelClassificationResult()
            #self.contourClassifier.calculateVoxelClassificationAccuracy_new()
            #self.contourClassifier.runFindContours()
            #self.contourClassifier.runGroupContoursByConnectedComponents()

        elif steps == 'accuracy':

            self.contourClassifier.runInitialize()
            self.contourClassifier.runLoadInputImage()
            self.contourClassifier.calculateVoxelClassificationAccuracy_new()

        elif steps == 'findTrainingContours':

            self.contourClassifier.runInitialize()
            self.contourClassifier.runLoadInputImage()
            self.contourClassifier.runLoadProbabilityMap()
            #self.contourClassifier.runClassifyVoxels()
            self.contourClassifier.runFindTrainingContours()
            self.contourClassifier.runWriteContoursToImageStack()
            #self.contourClassifier.runContourProbabilityFilter()
            #self.contourClassifier.runGroupContoursByConnectedComponents()

        elif steps == 'findInputContours':

            self.contourClassifier.runInitialize()
            self.contourClassifier.runLoadContourProcessingInputImage()
            self.contourClassifier.runLoadInputProbabilityMap()
            self.contourClassifier.runFindInputContours()
            #self.contourClassifier.runWriteContoursToImageStack()
            #self.contourClassifier.runContourProbabilityFilter()


        elif steps == 'findInputContoursTest':

            self.contourClassifier.runInitialize()
            self.contourClassifier.runLoadContourProcessingTrainingImage()
            self.contourClassifier.runLoadTrainingProbabilityMap()
            self.contourClassifier.runFindTrainingContours()
            #self.contourClassifier.runWriteContoursToImageStack()
            #self.contourClassifier.runContourProbabilityFilter()

            self.contourClassifier.runLoadContourProcessingInputImage()
            self.contourClassifier.runLoadInputProbabilityMap()
            self.contourClassifier.runFindInputContours()


        elif steps == 'classifyTrainingContours':

            self.contourClassifier.runInitialize()
            #self.contourClassifier.runLoadInputImage()
            self.contourClassifier.runLoadContourProcessingTrainingImage()
            self.contourClassifier.runLoadTrainingProbabilityMap()
            self.contourClassifier.runLoadContourProcessingInputImage()
            self.contourClassifier.runComputeContourRegions()
            self.contourClassifier.runMakeTrainingContourLists()
            self.contourClassifier.runCalculateTrainingContourListFeaturesTask()
            self.contourClassifier.runTrainingContourListClassifier()


        elif steps == 'classifyInputContours':

            self.contourClassifier.runInitialize()
            self.contourClassifier.runLoadContourProcessingTrainingImage()
            self.contourClassifier.runLoadInputProbabilityMap()
            self.contourClassifier.runLoadContourProcessingInputImage()
            self.contourClassifier.runMakeInputContourLists()
            self.contourClassifier.runCalculateInputContourListFeaturesTask()
            self.contourClassifier.runInputContourListClassifier()


        #elif steps == True:
        elif steps == 'groupContours':

            self.contourClassifier.runInitialize()
            self.contourClassifier.runLoadInputImage()
            self.contourClassifier.runClassifyVoxels()
            self.contourClassifier.runFindContours()
            self.contourClassifier.runGroupContoursByConnectedComponents()

        else:

            raise Exception, "Invalid steps parameter: %s" % str(steps)

        if self.dataViewer.guiVisible:
            self.app.MainLoop()

