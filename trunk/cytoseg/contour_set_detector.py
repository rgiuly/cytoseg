
import sys

from component_detector import *

class ContourSetDetector:

    def __init__(self, parameterDict):

        #testContours()  # crash
        target_depricated = 'mitochondria'

        #dataIdentifier = 'hpf'
        dataIdentifier = 'default'
        #mode = 'hpf_training'
        #mode = 'hpf_test'
        mode = 'default_test'
        #defaultStepNumber = 10
        #defaultStepNumber = 3
        defaultStepNumber = 7
        #defaultStepNumber = 106
        contourListClassificationMethod='bayes' # use for mitochondria
        #contourListClassificationMethod='randomForest'
        
        self.app = wx.PySimpleApp()
        self.dataViewer = ClassificationControlsFrame(makeClassifyGUITree())
        self.dataViewer.Show()

        print "mode: %s" % mode
        
        if len(sys.argv) < 2:
            print "step not specified, using default step", defaultStepNumber
            stepNumber = defaultStepNumber
        else:
            stepNumber = int(sys.argv[1])    
        
        # process the contours in a small dataset to learn about them
        #if mode == 'hpf_training':
        
        labelFilePaths = odict()
        labelFilePaths['mitochondria'] = odict()
        labelFilePaths['vesicles'] = odict()
    
        labelFilePaths['mitochondria']['process_a1'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/a1"
        labelFilePaths['mitochondria']['process_a2'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/a2"
        labelFilePaths['mitochondria']['process_0'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/0"
        labelFilePaths['mitochondria']['process_1'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/1"
        labelFilePaths['mitochondria']['process_2'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/2"
        labelFilePaths['vesicles']['all'] = "O:/images/HPFcere_vol/HPF_rotated_tif/vesicles/label/one_label/0_to_25"
    
        self.contourTrainer = CellComponentDetector(
            dataViewer=self.dataViewer,
            dataIdentifier=mode,
            target='not_set',
            originalImageFilePath="O:/images/HPFcere_vol/HPF_rotated_tif/vesicles/input",
            contourListClassificationMethod=contourListClassificationMethod,
            #contourListExamplesIdentifier="contourPathFeatures" + "_" + target,
            #contourListTrainingExamplesIdentifier="contourPathFeatures" + "_" + target,
            contourListExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
            contourListTrainingExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
            voxelTrainingImageFilePath="data/sbfsem_training/images",
            voxelTrainingLabelFilePath="data/sbfsem_training/label",
            labelFilePaths=labelFilePaths[target_depricated])
    
        self.contourTrainer.numberOfLayersToProcess = None
        self.contourTrainer.numberOfThresholds = 1
        self.contourTrainer.firstThreshold = 0.4
        self.contourTrainer.thresholdStep = 0.2
        
        # process the contours in a full dataset
        #elif mode == 'hpf_test':
        
        self.contourClassifier = CellComponentDetector(
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
            voxelClassificationIteration=2)
    
        #self.contourClassifier.voxelClassificationInputVolumeName =\
        #    self.contourClassifier.blurredVolumeName
        self.contourClassifier.voxelClassificationMethod = 'randomForest'

        self.contourClassifier.blobImageStackOutputFolder =\
            parameterDict['blobImageStackOutputFolder']

        #self.contourClassifier.numberOfLayersToProcess = 10
        self.contourClassifier.numberOfLayersToProcess = None
    
        # for mitochondria
        self.contourClassifier.numberOfThresholds = 1 #1 #4
        self.contourClassifier.firstThreshold = 0.05 #0.4 #0.2
    
        # not for mitochondria
        #self.contourClassifier.numberOfThresholds = 1 #4
        #self.contourClassifier.firstThreshold = 0.4 #0.2
    
        self.contourClassifier.thresholdStep = 0.05

        self.setTarget('mitochondria')
        #self.setTarget('vesicles')
        #self.setTarget('blankInnerCell')


    def setTarget(self, target):

        self.contourTrainer.target = target
        self.contourClassifier.target = target


    def run(self, runAllSteps=True):

        if runAllSteps:

            self.contourClassifier.runInitialize()
            self.contourClassifier.runPreclassificationFilter()
            self.contourClassifier.runClassifyVoxels()
            self.contourClassifier.runFindContours()
            self.contourClassifier.runGroupContoursByConnectedComponents()
            self.app.MainLoop()

        else:

            self.contourClassifier.runInitialize()
            self.contourClassifier.runPreclassificationFilter()
            self.contourClassifier.runClassifyVoxels()
            #self.contourClassifier.runFindContours()
            #self.contourClassifier.runGroupContoursByConnectedComponents()
            self.app.MainLoop()
