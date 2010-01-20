
import sys

from component_detector import *

class Detector:

    def __init__(self, parameterDict):

        self.dataIdentifier = 'hpf'
        #mode = 'hpf_training'
        self.mode = 'test'

        target = 'mitochondria'
        #target = 'vesicles'
        #target = 'blankInnerCell'
        #defaultStepNumber = 10
        #defaultStepNumber = 3
        defaultStepNumber = 7
        #defaultStepNumber = 106
        contourListClassificationMethod='bayes' # use for mitochondria
        #contourListClassificationMethod='randomForest'
        
        print "identifier: %s" % self.dataIdentifier
        print "mode: %s" % self.mode
        
        if len(sys.argv) < 2:
            print "step not specified, using default step", defaultStepNumber
            stepNumber = defaultStepNumber
        else:
            stepNumber = int(sys.argv[1])    
        
        # process the contours in a small dataset to learn about them
        if self.mode == 'training':
        
            labelFilePaths = odict()
            labelFilePaths['mitochondria'] = odict()
            labelFilePaths['vesicles'] = odict()
        
            labelFilePaths['mitochondria']['process_a1'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/a1"
            labelFilePaths['mitochondria']['process_a2'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/a2"
            labelFilePaths['mitochondria']['process_0'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/0"
            labelFilePaths['mitochondria']['process_1'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/1"
            labelFilePaths['mitochondria']['process_2'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/2"
            labelFilePaths['vesicles']['all'] = "O:/images/HPFcere_vol/HPF_rotated_tif/vesicles/label/one_label/0_to_25"
        
            self.cellComponentDetector = CellComponentDetector(
                dataIdentifier="no_identifier",
                target=target,
                originalImageFilePath="O:/images/HPFcere_vol/HPF_rotated_tif/vesicles/input",
                contourListClassificationMethod=contourListClassificationMethod,
                #contourListExamplesIdentifier="contourPathFeatures" + "_" + target,
                #contourListTrainingExamplesIdentifier="contourPathFeatures" + "_" + target,
                contourListExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
                contourListTrainingExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
                voxelTrainingImageFilePath="data/sbfsem_training/images",
                voxelTrainingLabelFilePath="data/sbfsem_training/label",
                labelFilePaths=labelFilePaths[target])
        
            self.cellComponentDetector.numberOfLayersToProcess = None
            self.cellComponentDetector.numberOfThresholds = 1
            self.cellComponentDetector.firstThreshold = 0.4
            self.cellComponentDetector.thresholdStep = 0.2
        
        # process the contours in a full dataset
        elif self.mode == 'test':
        
            self.cellComponentDetector = CellComponentDetector(
                dataIdentifier="no_identifier",
                target=target,
                originalImageFilePath=parameterDict['originalImageFilePath'],
                contourListClassificationMethod=contourListClassificationMethod,
                #contourListExamplesIdentifier="contourPathFeatures" + "_" + target,
                #contourListTrainingExamplesIdentifier="contourPathFeatures" + "_" + target,
                contourListExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
                contourListTrainingExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
                voxelTrainingImageFilePath=parameterDict['voxelTrainingImageFilePath'],
                voxelTrainingLabelFilePath=parameterDict['voxelTrainingLabelFilePath'])
        
            self.cellComponentDetector.voxelClassificationInputVolumeName =\
                self.cellComponentDetector.blurredVolumeName
            self.cellComponentDetector.voxelClassificationMethod = 'randomForest'

            self.cellComponentDetector.blobImageStackOutputFolder =\
                parameterDict['blobImageStackOutputFolder']

            #self.cellComponentDetector.numberOfLayersToProcess = 10
            self.cellComponentDetector.numberOfLayersToProcess = None
        
            # for mitochondria
            self.cellComponentDetector.numberOfThresholds = 4 #1 #4
            self.cellComponentDetector.firstThreshold = 0.2 #0.4 #0.2
        
            # not for mitochondria
            #self.cellComponentDetector.numberOfThresholds = 1 #4
            #self.cellComponentDetector.firstThreshold = 0.4 #0.2
        
            self.cellComponentDetector.thresholdStep = 0.2
        

    def fullIdentifier(self):

        return self.dataIdentifier + "_" + self.mode


    def run(self):

        self.cellComponentDectector.dataIdentifier = self.fullIdentifier()

        if 1:

            self.cellComponentDetector.runInitialize()
            #self.cellComponentDetector.runStep(stepNumber)
            self.cellComponentDetector.runPreclassificationFilter()
            self.cellComponentDetector.runClassifyVoxels()
            self.cellComponentDetector.runFindContours()
            self.cellComponentDetector.runMakeContourLists()
            self.cellComponentDetector.loadItemsForViewing()
            self.cellComponentDetector.saveContourPathsToJinxFile()
            self.cellComponentDetector.run3DShellActiveContourToDetect3DBlobs()
            self.cellComponentDetector.runWrite3DBlobsVolume()
            #self.cellComponentDetector.runContourProbabilityFilter()
            #self.cellComponentDetector.run3DShellActiveContourToDetect3DBlobsHighProbabilityOnly()
            #self.cellComponentDetector.runVoxelTestSteps()
            #self.cellComponentDetector.runContourTestSteps()
            self.cellComponentDetector.runMainLoop()
        
        else:

            #self.cellComponentDetector.runStep(stepNumber)

            self.cellComponentDetector.runInitialize()
            self.cellComponentDetector.runPreclassificationFilter()
            self.cellComponentDetector.runClassifyVoxels()
            self.cellComponentDetector.loadItemsForViewing()
            self.cellComponentDetector.runMainLoop()
