
import sys

from component_detector import *

#mode = 'training'
mode = 'test'
defaultStepNumber = 10

print "mode: %s" % mode

if len(sys.argv) < 2:
    print "step not specified, using default step", defaultStepNumber
    stepNumber = defaultStepNumber
else:
    stepNumber = int(sys.argv[1])    

if mode == 'training':

    labelFilePaths = odict()
    labelFilePaths['process_a1'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/a1"
    labelFilePaths['process_a2'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/a2"
    labelFilePaths['process_0'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/0"
    labelFilePaths['process_1'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/1"
    labelFilePaths['process_2'] = "O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/set/2"

    cellComponentDetector = CellComponentDetector(
        identifier=mode,
        originalImageFilePath="O:/images/Eric_07-10-09/process_traces/Working crop x116 y105 w362 h315/original",
        contourListExamplesFilename="o:/temp/contourPathFeatures.tab",
        contourListTrainingExamplesFilename="o:/temp/contourPathFeatures.tab",
        voxelTrainingImageFilePath="data/sbfsem_training/images",
        voxelTrainingLabelFilePath="data/sbfsem_training/label",
        labelFilePaths=labelFilePaths)

    cellComponentDetector.numberOfLayersToProcess = 8
    cellComponentDetector.numberOfThresholds = 1
    cellComponentDetector.firstThreshold = 0.4
    cellComponentDetector.thresholdStep = 0.2

elif mode == 'test':

    cellComponentDetector = CellComponentDetector(
        identifier=mode,
        originalImageFilePath="data/sbfsem",
        contourListExamplesFilename=None,
        contourListTrainingExamplesFilename="o:/temp/contourPathFeatures.tab",
        voxelTrainingImageFilePath="data/sbfsem_training/images",
        voxelTrainingLabelFilePath="data/sbfsem_training/label")

    cellComponentDetector.numberOfLayersToProcess = 8
    cellComponentDetector.numberOfThresholds = 1
    cellComponentDetector.firstThreshold = 0.4
    cellComponentDetector.thresholdStep = 0.2

cellComponentDetector.runStep(stepNumber)
