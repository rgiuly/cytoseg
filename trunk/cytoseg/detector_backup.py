
import sys

from component_detector import *

class Detector:

    def __init__(self, parameterDict):

        dataIdentifier = 'hpf'
        #mode = 'hpf_training'
        mode = 'hpf_test'
        target = 'mitochondria'
        #target = 'vesicles'
        #target = 'blankInnerCell'
        #defaultStepNumber = 10
        #defaultStepNumber = 3
        defaultStepNumber = 7
        #defaultStepNumber = 106
        contourListClassificationMethod='bayes' # use for mitochondria
        #contourListClassificationMethod='randomForest'
        
        print "mode: %s" % mode
        
        if len(sys.argv) < 2:
            print "step not specified, using default step", defaultStepNumber
            stepNumber = defaultStepNumber
        else:
            stepNumber = int(sys.argv[1])    
        
        # process the contours in a small dataset to learn about them
        if mode == 'hpf_training':
        
            labelFilePaths = odict()
            labelFilePaths['mitochondria'] = odict()
            labelFilePaths['vesicles'] = odict()
        
            labelFilePaths['mitochondria']['process_a1'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/a1"
            labelFilePaths['mitochondria']['process_a2'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/a2"
            labelFilePaths['mitochondria']['process_0'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/0"
            labelFilePaths['mitochondria']['process_1'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/1"
            labelFilePaths['mitochondria']['process_2'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/2"
            labelFilePaths['vesicles']['all'] = "O:/images/HPFcere_vol/HPF_rotated_tif/vesicles/label/one_label/0_to_25"
        
            cellComponentDetector = CellComponentDetector(
                dataIdentifier=mode,
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
        
            cellComponentDetector.numberOfLayersToProcess = None
            cellComponentDetector.numberOfThresholds = 1
            cellComponentDetector.firstThreshold = 0.4
            cellComponentDetector.thresholdStep = 0.2
        
        # process the contours in a full dataset
        elif mode == 'hpf_test':
        
            cellComponentDetector = CellComponentDetector(
                dataIdentifier=mode,
                target=target,
                originalImageFilePath=parameterDict['originalImageFilePath'],
                contourListClassificationMethod=contourListClassificationMethod,
                #contourListExamplesIdentifier="contourPathFeatures" + "_" + target,
                #contourListTrainingExamplesIdentifier="contourPathFeatures" + "_" + target,
                contourListExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
                contourListTrainingExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
                voxelTrainingImageFilePath=parameterDict['voxelTrainingImageFilePath'],
                voxelTrainingLabelFilePath=parameterDict['voxelTrainingLabelFilePath'])
        
            cellComponentDetector.voxelClassificationInputVolumeName =\
                cellComponentDetector.blurredVolumeName
            cellComponentDetector.voxelClassificationMethod = 'randomForest'

            cellComponentDetector.blobImageStackOutputFolder =\
                parameterDict['blobImageStackOutputFolder']

            #cellComponentDetector.numberOfLayersToProcess = 10
            cellComponentDetector.numberOfLayersToProcess = None
        
            # for mitochondria
            cellComponentDetector.numberOfThresholds = 4 #1 #4
            cellComponentDetector.firstThreshold = 0.2 #0.4 #0.2
        
            # not for mitochondria
            #cellComponentDetector.numberOfThresholds = 1 #4
            #cellComponentDetector.firstThreshold = 0.4 #0.2
        
            cellComponentDetector.thresholdStep = 0.2
        
        if 1:
            cellComponentDetector.runInitialize()
            #cellComponentDetector.runStep(stepNumber)
            cellComponentDetector.runPreclassificationFilter()
            cellComponentDetector.runClassifyVoxels()
            cellComponentDetector.runFindContours()
            cellComponentDetector.runMakeContourLists()
            cellComponentDetector.loadItemsForViewing()
            cellComponentDetector.saveContourPathsToJinxFile()
            cellComponentDetector.run3DShellActiveContourToDetect3DBlobs()
            cellComponentDetector.runWrite3DBlobsVolume()
            #cellComponentDetector.runContourProbabilityFilter()
            #cellComponentDetector.run3DShellActiveContourToDetect3DBlobsHighProbabilityOnly()
            #cellComponentDetector.runVoxelTestSteps()
            #cellComponentDetector.runContourTestSteps()
            cellComponentDetector.runMainLoop()
        
        #cellComponentDetector.runStep(stepNumber)
