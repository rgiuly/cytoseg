# data location configuration file

import sys
sys.path.append("..")

from contour_set_detector import ContourSetDetector

param = {}

# each volume is a stack of 8 bit tiff images


#subfolder = "/small_crop"
#subfolder = "/tiny_crop"
subfolder = ""

# full input volume
#param['originalImageFilePath']="data/sbfsem_080309/data_tifs"
param['originalImageFilePath']="/ncmirdata1/rgiuly/sbfsem/data_tiny"

# training data image volume
#param['voxelTrainingImageFilePath']="data/sbfsem_080309/data_tifs"
param['voxelTrainingImageFilePath']="/ncmirdata1/rgiuly/sbfsem/data_tiny"

# training data labels
# this should have the exact same dimensions as param['voxelTrainingImageFilePath'] 
param['voxelTrainingLabelFilePath']="/ncmirdata1/rgiuly/sbfsem/seg_tiny"

# output volume
param['blobImageStackOutputFolder']="/tmp"

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
