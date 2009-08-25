
import sys

from component_detector import *

defaultStepNumber = 0

if len(sys.argv) < 2:
    print "step not specified, using default step", defaultStepNumber
    stepNumber = defaultStepNumber
else:
    stepNumber = int(sys.argv[1])    

cellComponentDetector = CellComponentDetector(
    originalImageFilePath="O:/images/Eric_07-10-09/normalized_tiff_files/cropped_stack/8bit",
    voxelTrainingImageFilePath="data/sbfsem_training/images",
    voxelTrainingLabelFilePath="data/sbfsem_training/label")

cellComponentDetector.runStep(stepNumber)
