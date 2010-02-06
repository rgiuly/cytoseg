# data location configuration file

import sys
sys.path.append("..")

from label_identifier import *

from contour_set_detector import ContourSetDetector

param = {}

# each volume is a stack of 8 bit tiff images


subfolder = ""
#subfolder = "/small_crop"
#subfolder = "/tiny_crop"

# full input volume
#param['originalImageFilePath'] = "data/sbfsem_080309/data_tifs"
param['originalImageFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/data_tifs/last/8bit/350x350/crop" + subfolder

# training data image volume
#param['voxelTrainingImageFilePath'] = "data/sbfsem_080309/data_tifs"
param['voxelTrainingImageFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/data_tifs/last/8bit/350x350/crop" + subfolder

# training data labels
# this should have the exact same dimensions as param['voxelTrainingImageFilePath'] 
param['voxelTrainingLabelFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/seg_tifs/350x350/membrane_edges/crop" + subfolder

# output volume
param['blobImageStackOutputFolder'] = "O:/temp/blobOutput_080309"

#detector = Detector(param)
detector = ContourSetDetector(param)
detector.dataIdentifier = "sbfsem_080309"
detector.dataViewer.mainDoc.dataTree.rootFolderPath = "G:/cytoseg_data/sbfsem" + subfolder
#detector.contourClassifier.numberOfLayersToProcess = 50
detector.contourClassifier.numberOfLayersToProcess = 7
detector.contourClassifier.numberOfTrainingLayersToProcess = 7
#detector.contourClassifier.minVoxelLabelValue['mitochondria'] = 3
#detector.contourClassifier.minVoxelLabelValue['membranes'] = 2
#detector.contourClassifier.maxVoxelLabelValue['membranes'] = 2
#detector.contourClassifier.labelIdentifierDict['membranes'] = LabelIdentifier(min=2, max=2)
#detector.contourClassifier.labelIdentifierDict['mitochondria'] = LabelIdentifier(min=3)
detector.contourClassifier.labelIdentifierDict['membranes'] = LabelIdentifier(min=1)
detector.setTarget('membranes')
#detector.setTarget('membranes_test')
detector.run(runAllSteps=0)
