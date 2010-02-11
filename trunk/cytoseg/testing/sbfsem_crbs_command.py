# data location configuration file

import sys
sys.path.append("..")

from machine_learning_tutorial import MachineLearningTutorial

param = {}

# each volume is a stack of 8 bit tiff images


#subfolder = "/small_crop"
#subfolder = "/tiny_crop"
subfolder = ""

# full input volume
#param['originalImageFilePath']="data/sbfsem_080309/data_tifs"
param['originalImageFilePath']=sys.argv[0]

# training data image volume
#param['voxelTrainingImageFilePath']="data/sbfsem_080309/data_tifs"
param['voxelTrainingImageFilePath']=sys.argv[1]

# training data labels
# this should have the exact same dimensions as param['voxelTrainingImageFilePath'] 
param['voxelTrainingLabelFilePath']=sys.argv[2]

# output volume
param['blobImageStackOutputFolder']=sys.argv[3]

#detector = Detector(param)
detector = ContourSetDetector(param)
detector.dataIdentifier = "sbfsem_080309"
#detector.dataViewer.mainDoc.dataTree.rootFolderPath = "G:/cytoseg_data/sbfsem"
detector.contourClassifier.numberOfLayersToProcess = 14
detector.contourClassifier.numberOfTrainingLayersToProcess = 7
detector.contourClassifier.minVoxelLabelValue['mitochondria'] = 3
detector.contourClassifier.minVoxelLabelValue['membranes'] = 2
detector.contourClassifier.maxVoxelLabelValue['membranes'] = 2
detector.setTarget('membranes')
detector.run(runAllSteps=0)
