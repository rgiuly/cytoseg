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
param['originalImageFilePath']="O:/images/stem_cell/3D/tif/400x300/crop"

# training data image volume
#param['voxelTrainingImageFilePath']="data/sbfsem_080309/data_tifs"
param['voxelTrainingImageFilePath']="O:/images/stem_cell/3D/tif/400x300/crop"

# training data labels
# this should have the exact same dimensions as param['voxelTrainingImageFilePath'] 
param['voxelTrainingLabelFilePath']="O:/images/stem_cell/3D/tif/seg/400x300/crop"

# output volume
param['blobImageStackOutputFolder']="/tmp"

#detector = Detector(param)
detector = ContourSetDetector(param)
detector.dataIdentifier = "stem_cell"
detector.dataViewer.mainDoc.dataTree.rootFolderPath = "G:/cytoseg_data/stem_cell"
detector.contourClassifier.numberOfLayersToProcess = 14
detector.contourClassifier.numberOfTrainingLayersToProcess = 7
detector.contourClassifier.minVoxelLabelValue['mitochondria'] = 3
detector.contourClassifier.minVoxelLabelValue['membranes'] = 1
detector.contourClassifier.maxVoxelLabelValue['membranes'] = 1000
detector.setTarget('membranes')
detector.run(runAllSteps=0)
