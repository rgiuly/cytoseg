
import sys

from component_detector import *

dataIdentifier = 'hpf'
mode = 'hpf_training'
#mode = 'hpf_test'
target = 'mitochondria'
#target = 'vesicles'
#target = 'blankInnerCell'
defaultStepNumber = 10
#defaultStepNumber = 106
contourListClassificationMethod='bayes' # use for mitochondria
#contourListClassificationMethod='randomForest'

print "mode: %s" % mode

# process the contours in a small dataset to learn about them
if mode == 'hpf_training':

    cellComponentDetector = CellComponentDetector(
        dataIdentifier=mode,
        target=target,
        originalImageFilePath="O:/images/HPFcere_vol/HPF_rotated_tif/vesicles/input",
        contourListClassificationMethod=contourListClassificationMethod,
        contourListExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
        contourListTrainingExamplesIdentifier="contourPathFeatures" + "_" + dataIdentifier,
        voxelTrainingImageFilePath="data/sbfsem_training/images",
        voxelTrainingLabelFilePath="data/sbfsem_training/label",
        labelFilePaths=None)

    cellComponentDetector.voxelClassificationInputVolumeName =\
        cellComponentDetector.originalVolumeName
    cellComponentDetector.voxelClassificationMethod = 'neuralNetwork'

    cellComponentDetector.numberOfLayersToProcess = None
    cellComponentDetector.numberOfThresholds = 1
    cellComponentDetector.firstThreshold = 0.4
    cellComponentDetector.thresholdStep = 0.2


cellComponentDetector.runInitialize()
cellComponentDetector.runClassifyVoxels()
cellComponentDetector.runMainLoop()

