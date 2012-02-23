
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
        #defaultStepNumber = 7
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
        #if True:
        #    print "step not specified, using default step", defaultStepNumber
        #    stepNumber = defaultStepNumber
        #else:
        #    stepNumber = int(sys.argv[1])    
        
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
    
        #self.componentDetector.voxelClassificationInputVolumeName =\
        #    self.componentDetector.blurredVolumeName
        self.componentDetector.voxelClassificationMethod = 'randomForest'

        self.componentDetector.blobImageStackOutputFolder =\
            parameterDict['blobImageStackOutputFolder']

        #self.componentDetector.numberOfLayersToProcess = 10
        self.componentDetector.numberOfLayersToProcess = None
    
        # for mitochondria
        self.componentDetector.numberOfThresholds = 7 #5 #2 #5 #1 #1 #4
        self.componentDetector.firstThreshold = 30 #20 #160 #0.05 #0.4 #0.2
    
        # not for mitochondria
        #self.componentDetector.numberOfThresholds = 1 #4
        #self.componentDetector.firstThreshold = 0.4 #0.2
    
        self.componentDetector.thresholdStep = 36 #40 #80 #40 #0.05

        self.setTarget('mitochondria')
        #self.setTarget('vesicles')
        #self.setTarget('blankInnerCell')


    def setTarget(self, target):

        #self.contourTrainer.target = target
        self.componentDetector.target = target


    def run(self, steps):

        if steps == 'classifyVoxels':

            self.componentDetector.runInitialize()
            self.componentDetector.runLoadTrainingData()
            self.componentDetector.runLoadInputImage()
            self.componentDetector.runClassifyVoxels()
            self.componentDetector.runWriteVoxelClassificationResult()
            #self.componentDetector.calculateVoxelClassificationAccuracy_new()
            #self.componentDetector.runFindContours()
            #self.componentDetector.runGroupContoursByConnectedComponents()


        elif steps == 'randonLikeFeaturesVoxelProcess':
            self.componentDetector.runInitialize()
            self.componentDetector.runLoadInputImage()
            #todo:
            #runWriteInputImage()
            #runRadonLikeFeaturesProcess()


        elif steps == 'voxelAccuracy':

            self.componentDetector.runInitialize()
            self.componentDetector.runLoadInputImage()
            self.componentDetector.calculateVoxelClassificationAccuracy_new()

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

        elif steps == 'findInputContours':

            self.componentDetector.runInitialize()
            self.componentDetector.runLoadContourProcessingInputImage()
            self.componentDetector.runLoadInputProbabilityMap()
            self.componentDetector.runFindInputContours()
            #self.componentDetector.runWriteContoursToImageStack()
            #self.componentDetector.runContourProbabilityFilter()


        elif steps == 'findInputContoursTest':

            self.componentDetector.runInitialize()
            self.componentDetector.runLoadContourProcessingTrainingImage()
            self.componentDetector.runLoadTrainingProbabilityMap()
            self.componentDetector.runFindTrainingContours()
            #self.componentDetector.runWriteContoursToImageStack()
            #self.componentDetector.runContourProbabilityFilter()

            self.componentDetector.runLoadContourProcessingInputImage()
            self.componentDetector.runLoadInputProbabilityMap()
            self.componentDetector.runFindInputContours()


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


        elif steps == 'classifyInputContours':

            self.componentDetector.runInitialize()
            self.componentDetector.runLoadContourProcessingTrainingImage()
            self.componentDetector.runLoadInputProbabilityMap()
            self.componentDetector.runLoadContourProcessingInputImage()
            self.componentDetector.runMakeInputContourLists()
            self.componentDetector.runCalculateInputContourListFeaturesTask()
            self.componentDetector.runInputContourListClassifier()


        elif steps == 'writeAllInputContoursToImageStack':

            #self.componentDetector.runWriteContoursToImageStack()
            self.componentDetector.runWriteInputContoursToBinaryImageStack()


        elif steps == 'inputContourListProbabilityFilter':

            self.componentDetector.runLoadContourProcessingInputImage()
            self.componentDetector.runContourListProbabilityFilter()


        elif steps == 'fill3DBlobs':

            #self.componentDetector.runLoadInputImage()
            self.componentDetector.runLoadContourProcessingInputImage()
            self.componentDetector.runInitialize()
            self.componentDetector.runFill3DBlobsFromContourListsHighProbabilityOnly()
            self.componentDetector.runWrite3DBlobsVolume()


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

