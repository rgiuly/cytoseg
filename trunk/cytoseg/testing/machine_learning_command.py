# data location configuration file

import sys
sys.path.append("..")

from machine_learning_tutorial import MachineLearningTutorial
from label_identifier import *

param = {}

# each volume is a stack of 8 bit tiff images


# full input volume
param['originalImageFilePath'] = sys.argv[1]

# training data image volume
param['voxelTrainingImageFilePath'] = sys.argv[2]

# training data labels
# this should have the exact same dimensions as param['voxelTrainingImageFilePath'] 
param['voxelTrainingLabelFilePath'] = sys.argv[3]

# output volume
param['blobImageStackOutputFolder'] = sys.argv[4]

detector = MachineLearningTutorial(param)
detector.dataIdentifier = "sbfsem_080309"
#detector.dataViewer.mainDoc.dataTree.rootFolderPath = "G:/cytoseg_data/sbfsem"
import default_path
detector.dataViewer.mainDoc.dataTree.rootFolderPath = sys.argv[5]
defaultTemporaryFolder = sys.argv[5]
cytosegDataFolder = defaultTemporaryFolder
contourOutputTemporaryFolder = defaultTemporaryFolder
defaultOutputPath = defaultTemporaryFolder
detector.contourClassifier.numberOfLayersToProcess = 14
detector.contourClassifier.numberOfTrainingLayersToProcess = 7

detector.contourClassifier.labelIdentifierDict['blankInnerCell'] =\
        LabelIdentifier(min=0, max=0)
detector.contourClassifier.labelIdentifierDict['membranes'] =\
        LabelIdentifier(min=1, max=255)

detector.setTarget('membranes')
detector.run(runAllSteps=0)
